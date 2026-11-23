# The startup type registry

**Bottom line.** The first substantial game code in the binary is not gameplay. It is a
generated, encrypted type/object registry: roughly eight thousand records that declare a
name, an object size, an alignment, a category and method/data pointers, followed by
builders that instantiate those types and small tables that map numeric ids back to them.
It occupies `0x1400fbcb0`–`0x14054ea50` and is closed: the registration machine stops in
pass 27, and every later pass reads code that consumes the objects it built.

The main evidence is the pass-27 record
[`0x1404bfe00-0x14054ea50.md`](../ranges/0x1404bfe00-0x14054ea50.md), the pass-15
synthesis in [`CODE_MAP_ARCHIVE.md`](../CODE_MAP_ARCHIVE.md) §"The registry machine", and
the cumulative counts in [`CODE_MAP.md`](../CODE_MAP.md).

## Where it sits

In address order the client starts with four non-game layers:

| layer | range | what it is |
|---|---|---|
| 1 | `0x140001000`–`0x140039fc0` | ISA-L/igzip inflate, NVAPI bootstrap and wrappers |
| 2 | `0x14003a230`–`0x14003d330` | NVIDIA driver-loading `LoadLibrary` shim |
| 3 | `0x14003ffe0`–`0x1400fa760` | CRT/C++ static-initialisation sea |
| 4 | `0x1400fbcb0`–`0x14054ea50` | this registry |

Layer 4 ends where the runtime bootstrap begins. Pass 27 contains the transition: four
plaintext registrar calls and the first runtime code appear at the end of the registry
range, around `0x14053f6b0`. From pass 28 onward there are no ciphertext registrations and
no `{id,hash}` records; see [`engine-runtime.md`](engine-runtime.md).

## What one registration contains

The names are not stored as plain strings. Each name buffer has the same layout:

- 8-byte XOR key at `+0`;
- 24-bit length in the low bytes of the `uint32` at `+8`;
- a done/decoded flag at `+0xb`;
- ciphertext payload at `+0xc`.

The decoder XORs `payload[i]` with `key[i & 7]` and clears the flag/length header. That
layout recurs in almost every later subsystem, so it is worth recognising: it is the
client's standard obfuscated-name page, not a registry-only format. The pages are listed
in `CODE_MAP.md` under "Where the data lives"; the decoded pool is `strpool.tsv`, queried
with [`scripts/strlookup.py`](../scripts/strlookup.py).

A registration call has the shape:

```text
func_0x1421cd360(out, name_ciphertext, hash32, 0, size, align, flags, 0,
                 token, a10, a11, a12, a13, a14, 0, 0, a17, base)
```

The registrar body itself is **not in the dump** (`func_0x…` means a later, unread
region or a function Ghidra did not emit). The call shape, not the callee, is the
evidence. The arguments are:

- `size` — the constructed object's size; the measured span is 3 B to `0x3bc0` B;
- `align` — normally 8, with a few 4 and 16 exceptions;
- `flags` — normally 0, with a small number of 1/2/3/10 rows;
- `token` — a category id; nonzero tokens usually select one fixed five-pointer set,
  zero tokens select a generic container set;
- `hash32` — the registration hash. Across the ciphertext rows these are unique:
  7,952 registrations with zero hash reuse. Four later plaintext registrations
  (`"teStructuredData"`, `"MirrorData"`, `"TrackedData"`) deliberately break the rule:
  one hash is used twice with different flags. The final count is 7,956 registration
  calls and 7,955 distinct hashes.
- args 10–14 and 17 — per-registration method/data pointers. They advance in parallel
  index bands, one entry per registration, which is the strongest evidence that this is
  generated code rather than hand-written tables.

## The cooperating constructs

The registry is not one function. It is a set of templates that always appear together.

**Registration rows.** The `func_0x1421cd360` calls above. They declare a type. Final
cumulative class count: 7,956 registration rows (`reg`), against 1,717 builders, 1,954
copy wrappers, 280 sorted-insert builders, 261 nested-atexit builders and 326 id/hash
records. These are machine counts from `state.json`; do not add them by hand.

**Builders.** A builder allocates an object, decrypts a name page, calls one of the two
decryptor helpers (`func_0x140fd4f30` or `func_0x140fd4f70`), publishes the result with
`func_0x140fd4fb0`, and stores a row containing the class root, the instance pointer and a
live flag. The decryptor hash is a *type name*, so many builders can share one hash — the
opposite of the registration-hash regime. The exact row slots differ between the builder
family and the later row layout; the pass-15 synthesis quotes `+0`/`+8`/`+0x78`, while the
cumulative conventions table quotes `+0x20`/`+0x28`/`+0x98`/`+0x9c`. Treat the slots as
record-specific, not universal.

**Copy wrappers.** A wrapper does not decrypt anything. It copies an existing row with
`func_0x000140fd2d70`, publishes it with `func_0x140fd4fb0`, and marks it as not newly
constructed. This is how one built object is published under several roots. A small
variant also writes the one plaintext symbol family in the range, the
`PTR_s_CompilerIDFilter_*` pointers.

**Sorted-insert builders.** Two-entry tables, sorted by a `uint` key at `+8`, built with
two decrypts and a count of 2. They look like tiny startup lookup tables, not general
containers.

**`{id,hash}` records.** Each row stores a small numeric id, a 32-bit hash, and usually a
zero alias field. The hash is the registration hash; 326 records are known and the
machine ledger tracks every match. Many ids may point at one registration hash, so the
natural reading is `enum value → registered type`, with the third field as an optional
alias. The strongest many-to-one case is four ids (`0x8f`, `0x12b`, `0xd`, `0x8e`) →
`0xce1a4d26`; this is evidence that the ids are not a second name space but an alias
surface.

**Nested-atexit builders.** Rows that register shutdown for the objects they build. The
shared shutdown pointer slots are scattered by the linker, not one table. The function
pointer in each row selects one of several initialiser families; the `atexit` targets sit
in the undumped `0x142f0xxx` region.

**CompilerIDFilter shells and struct schemas.** Two special cases matter:

- Twelve small functions store a flag and one of the twelve
  `&PTR_s_CompilerIDFilter_*` labels, and four 244-B wrappers root registration rows on
  those payloads. This is the only readable symbol family in the registry and the direct
  evidence that the registry writes the shader/compiler filter machinery.
- At `0x140519090` (pass 27, chunk 0235) the registry registers physics/reflection
  schemas in plaintext: field tables of `{&name, offset, size}` followed by
  `{&name, &fields, size, flag, handler}`. Types include `bcMtx44`, `bcPQTransform`,
  `dmWorld` (0x194 B), `dmManifold` (0x100 B), `dmContact`, `dmSphere`, `dmPolytope`.
  This is the clearest evidence that the registry feeds a runtime type/serialisation system,
  not just a name list. The names and field layouts are evidence; the "physics engine"
  label is an inference from the `dm*`/`bc*` prefixes.

## How it is wired

Registration outputs are written into data bands, one fresh band per generated block:
`0x143d2xxxx` through `0x143e5xxxx` in the pass-15 synthesis, and the later rows continue
in `0x143e…`/`0x1441e…`. Builders increasingly root themselves on those registration
outputs rather than on static addresses; from pass 14 onward the old static roots are the
minority. The regime alternates by block, so "static-root era" and "output-root era" are
not chronological phases — they are per-generated-block choices. The pass-15 record notes
the shift, and the archive corrections retire the older timeline claim.

The `0x143cf…`/`0x143d…` band that early records called "class roots" is actually RTTI
`type_info`: every 181-B catch descriptor stores one of those addresses at `+0x18`
alongside `&SUB_140551380`. That correction is in the archive (item 17) and matters when
reading the catch-descriptor families.

## What it is for

The evidence supports this reading:

- the registry *declares* types with a name, size, alignment, category and method set;
- builders *instantiate* the named types into rows;
- wrappers *publish* instances under roots;
- id/hash rows *expose* the types to an integer-keyed consumer;
- the consumer appears after `0x14054fea0` and looks types up rather than registering
  them.

That consumer is the engine runtime. The registry is therefore the boundary between
generated startup data and behaviour. The label "type/object registry" is an inference
from the shape; the measurement of the shape is evidence. The pass-27 record is the
strongest single source because it catches the transition and the plaintext schemas in
the same range.

## Known limits

- The registrar `func_0x1421cd360`, both decryptors, the publisher, the record writer and
  the copy helper have no decompiled bodies in this corpus. Reading more chunks cannot
  produce them; they belong to the dump's `func_0x…` set.
- The names are encrypted per record. The decoded pool can answer "what is this page?",
  but the registry's exact name-to-hash mapping is still partly a lookup exercise.
- The nested-atexit targets are in `0x142f0xxx`, which is not in the dump.
- Some labels in the archive ("type registry", "shutdown table", "lookup table") are
  shape-based inference. The counts and addresses are measured; the purpose labels are
  not.
- The registry's own consumer is only partly read. The engine-runtime page lists the
  service and type-table machinery that resolves these objects.

If you need to check a claim, start with the pass-27 record and the pass-15 synthesis,
then use `scripts/crossref.py <symbol>` for the defining entry and every later mention.
