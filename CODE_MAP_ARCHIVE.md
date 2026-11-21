# CODE_MAP — cumulative map of the systematic `.text` read

**Read this file in full before every pass. Update it after every pass.** It replaces the old ledger in
`PROTOCOL.md`; per-pass detail lives in `ranges/<first>-<last>.md`. Never start a pass from the ledger
numbers alone — the range documents carry the evidence, the inferences and the open threads.

**Reconciliation revision (2026-11-20b, no new chunks read).** All 13 range records were re-read
end-to-end and every cumulative number re-derived directly from the chunk text. Corrections:
pass 5's Σ `size=` is **116,193 B** (the 931,009 carried in that record and in the old table was
decompiled-text size, not `.text` bytes); `{id,hash}` static records total **50**, not 44
(pass 2's six had never been added); sorted-insert builders total **74**, not 29;
CompilerIDFilter shells total **12**, not 9 (pass 3's three had been dropped). Newly measured for
this revision: **2,940** `func_0x1421cd360` call sites with **2,940 distinct hashes** (zero
registration-hash reuse across the whole read; superseded by pass 14 below: 3,227/3,227); **50/50** record hashes match a registration
(superseded by pass 14: 66/66);
**1,339** textual `0x140fd9670` occurrences and **726** `0x140f7b210` occurrences (the old 438
counted only passes 5–13); **146** distinct `atexit` targets. A cumulative synthesis
(**"What the code is"**) is now the primary reading; the per-pass list is the evidence index.

Pass-level update (pass 15): after pass 15 (chunks `0116`–`0123`, ended at `0x1402c16e0`;
510 functions, Σ `size=` 143,192; **registry machine keeps alternating: TWO more big registration
blocks + the biggest single-name run yet + the CompilerIDFilter chain written again** — 351
registrations / 351 distinct hashes in THREE blocks (H 184 regs `0x14029a6e0`–`0x1402a6130`,
I 114 regs `0x1402ae630`–`0x1402b5aa0`, J 46 regs `0x1402bac50`–`0x1402be000`) plus block K ≥7 regs
open at `0124`; outputs sweep `0x143e0f480`→`0x143e5bb40` (NEW bands `0x143e4`, `0x143e5`); **first
flags=10 registration ever (`FUN_1402bcb90`)**, flags=1 ×9, align-0x10 ×8, size-8 regs ×~10, new
267-B reg shape ×5, new 471-B builder ×1, first `&SUB_` arg17s; 9 `{id,hash}` records 8/9 (75
cumulative; id `0x3` = NEW MINIMUM; `0x3fd91271` matched NO registration — first unmatched record
hash); `0x3faff222` ×~21 builders on root `&DAT_143e185e0` (pass-14's ×7 run beaten) with 15
distinct per-builder pre-steps `FUN_141247af0`–`FUN_141248930`; ALL roots are registration outputs
(second static-root-free pass) and the **builder→row fill convention measured: root at row+0x20,
instance ptr at row+0x28, flag at row+0x98**; nested-atexit ×6 (156 cumulative) with THREE new
initializer families (`14314a698`, `14315bb50`, `14314f9b8` → 11 known) and SIX new atexit labels
(35 total, band `0x142f0ad80`–`0x142f0cab0`); the shutdown table MOVED to `0x143e2b`–`0x143e42`;
3 × 244-B wrappers write THREE new `PTR_s_CompilerIDFilter_*` (1438de790/1438dd4b8/1438de9d0) into
reg rows — registry→filter link now 4 instances; helpers 28 → ≥34, allocators 25 call sites
(8–0x500), `FUN_140f80f80` ×0 again; two unlisted gaps (`0x140298fd9`–`0x14029a6e0` 5,895 B,
`0x1402bf899`–`0x1402c10c0` 6,183 B); token `0x9825b6271dce1d31`-style exception now ×2 —
`0x808844973e17d0fd` ×11 across ≥3 pointer sets. Record: `pass15_0x140298b20-0x1402c16e0.md`.
*Method note:* all 8 chunks read with the identical unreachable-block warning boilerplate filtered
(7,522 lines dropped, every code line read); records/wrappers/novel shapes re-read unfiltered;
all counts script-derived (`scripts/pass15_measure.py`, `pass15_census.py`, `pass15_verify.py`).

Prior entry (pass 14): after pass 14 (chunks `0108`–`0115`, ended at `0x140298b11; 465 functions, Σ `size=` 129,912;
**registration sea fully self-rooted + the registry's first named consumer** — 287 registrations / 287 distinct hashes in
SEVEN blocks sweeping outputs `0x143de6b80`→`0x143e107d0`, first flags≠0 regs ever (1 and 3), first align-16 regs (×2), new
270-B shape (263-B + nonzero arg16 `FUN_141232440`), token `0x9825b6271dce1d31` ×29 ACROSS TWO DIFFERENT pointer sets
(breaks the token=pointer-set convention), 16 `{id,hash}` records 16/16 (cumulative 66/66) with the strongest many-to-one
(4 ids `0x8f`/`0x12b`/`0xd`/`0x8e` → `0xce1a4d26`) and the FIRST nonzero record third fields (one = another registration's
hash), 23 sorted-insert builders (97 cumulative; first 512/515/523-B variants; first dual-decryptor 515-B mixing `d4f30`+`d4f70`),
`FUN_140f80f80` ×0 — allocator pre-steps are now 14 per-block one-arg functions, first call sites for helpers
`FUN_140f81de0`/`FUN_140f94900`/`FUN_1410f5b30` (helpers 25 → 28), 12 × nested-atexit (150 cumulative; labels 17 → 29, band
`0x142f0ad80`–`0x142f0bf10`; six-plus initializer families; first 2-arg `c7880`; first rootless 558-B; new 542/574-B row-count
variants), **static class roots ABSENT — every root is a registration output (`&DAT_143de6b80` mega-roots ≥15 builders;
`&DAT_143e00ac0/0x143e00c20` root all 24 chunk-0113 wrappers) or a far band (`0x143eb6xxx` CompilerIDFilter payloads,
`0x143ecee70`, `0x143ee0cd0`)**, and the 244-B wrapper `FUN_140298920` stores `&PTR_s_CompilerIDFilter_1438d9ff0` (first
readable symbol since pass 5) into a registration row — the sea demonstrably writes the CompilerIDFilter chain.
*Method note:* chunks `0108`–`0113` read line-by-line in full; the twelve identical wrappers closing `0113` and chunks
`0114`–`0115` read with the identical decompiler warning boilerplate filtered out (every code line read); all counts
re-derived by script (`scripts/pass14_measure.py`) — see the record's method note. Record: `pass14_0x140275450-0x140298b11.md`.

Prior entry (pass 13): after pass 13 (chunks `0100`–`0107`, ended at `0x140275350` ≈ `0x140275451`; 258
functions, Σ `size=` 74,840; **wrapper-majority sea + a new self-contained registration block** —
151 × 241-B copy wrappers (58 %, majority again) + 61 × 397-B builders, `d4f70`↔397-B exact again
(61/61), 22 registrations in a SIXTH output band `0x143de2xxx`–`0x143de6xxx` with a NEW 242-B
registration shape (arg17/18 = 0, arg10 = container helper `FUN_140548d00`) and the first align-4
registration ever (`FUN_140273ff0`), 5 `{id,hash}` static records back after five passes at zero
(44/44 at the time; **50/50 cumulative** once pass 2's six are restored; FIRST many-to-one: ids 0x49+0x91 → hash `0x1b872806`; ids 0x3a/0x49/0x4a below
the old 0x4b minimum; pass 2's id 6 is lower still), 2 × 507-B sorted-insert builders (29 recorded then; **74 cumulative overall**; 8th pre-step recipe
{`FUN_1421c63b0`+`FUN_1421c76c0`}), 25th two-buffer helper `FUN_141212ed0` (first size-8; its hash
`0x4d28219d` triples as registration hash + record hash + helper hash), a rootless-builder ladder
(231/365/377/479/507-B variants all rooted on registration outputs), 3 × 558-B nested-atexit
(+3 labels `0x142f0b3b0/3e0/3f0` → 17 labels, `PTR_FUN_14314b5b0` ×18), measured NEW layout fact:
wrapper guard src = root-slot − 0x20 (152/153), ciphertext crosses `0x1438d00000`. *Method note:*
pass 13 was read with a full-fidelity extractor + skeleton-conformance check (19 skeletons/258 fns,
all new shapes then read raw) — see the record's method note. Prior entry (pass 12): pure
builder-sea continuation — 0 registrations, `d4f70`↔397-B exact 118/118, 4 × 558-B nested-atexit,
2 new allocators `FUN_1411dfda0`/`FUN_1411e00c0`, far root `&DAT_143f8e270` ×20, 3 new 373-B
pre-steps, first 558-B with a dynamic root `&DAT_143dcbd30`. *Housekeeping 2026-11-20 (no
re-read):* the pass-8 record `ranges/0x1401d2660-0x1401ef8e0.md` was installed, every "lost in
recycle / absent" provenance note was checked against the tree (all records + 2,228 chunks +
`index.json` present), pass numbering re-verified as chronological by chunk, and the pass-1
`0009`–`0013` unread span acknowledged in its record and in the table above. **The numbers
re-derive:** pass 1 2,303 fns / Σ `size=` 412,670; pass 8 401 / 115,925; pass 9 218 / 78,716;
pass 10 235 / 74,025; pass 11 765 / 205,857; pass 12 226 / 74,834; pass 13 258 / 74,840 — all
match. Pass-6–13 numbers stay *chunk-file* measurements ("disk bytes" / Σ `size=`) and must not
be mixed with the pass-1–5 `index.json` numbers. Pass numbering is **chronological by chunk
order**: pass 7 = `0053`–`0060`, pass 8 = `0061`–`0067`, pass 9 = `0068`–`0075`,
pass 10 = `0076`–`0083`, pass 11 = `0084`–`0091`, pass 12 = `0092`–`0099`,
pass 13 = `0100`–`0107`.

## Coverage

| pass | chunks | `.text` range | functions | bytes | Σ `size=` (`.text` B) | source range doc |
|---|---|---|---|---|---|---|
| 1 (**only `0000`–`0008` read**; `0009`–`0013` pending) | `0000`–`0013` | `0x140001000`–`0x1400c2ed0` | 2,303 | 1,838,252 (index) | 412,670 | `ranges/0x140001000-0x1400c2ed0.md` — 1,438 fns read, 865 fns at `0x140093150`–`0x1400c2ed0` census-only |
| 2 (partial, ended early) | `0014`–`0022` | `0x1400c2f90`–`0x14010bf30` | 1,183 | 1,194,249 (index) | 228,057 | `ranges/0x1400c2f90-0x14010bf30.md` |
| 3 (consolidated) | `0023`–`0029` | `0x14010c120`–`0x14012bcd0` | 408 | 936,081 (index) | 117,713 | `ranges/0x14010c120-0x14012bcd0.md` |
| 4 | `0030`–`0037` | `0x14012bee0`–`0x140156840` | 524 | 1,060,477 (index) | 155,444 | `ranges/0x14012bee0-0x140156840.md` |
| 5 (7 of ~12 chunks; user-named range) | `0038`–`0044` | `0x140156950`–`0x140175867` | 375 | 970,608 disk | 116,193 | `ranges/0x140156950-0x140175867.md` |
| 6 (8 of ~12 chunks; user-named range) | `0045`–`0052` | `0x140175ab0`–`0x14019d080` (ends `0x14019d171`) | 519 | 1,079,136 disk | 146,118 | `ranges/0x140175ab0-0x14019d080.md` |
| 7 (8 chunks; user-named range) | `0053`–`0060` | `0x14019d180`–`0x1401d265d` | 740 | 1,117,655 disk | 186,305 | `ranges/0x14019d180-0x1401d265d.md` |
| 8 (7 chunks; user-named range) | `0061`–`0067` | `0x1401d2660`–`0x1401ef8e0` | 401 | 953,445 disk | 115,925 | `ranges/0x1401d2660-0x1401ef8e0.md` |
| 9 (8 chunks; user-named range) | `0068`–`0075` | `0x1401efa00`–`0x1402039cd` | 218 | 1,076,638 disk | 78,716 | `ranges/0x1401efa00-0x1402039cd.md` |
| 10 (8 chunks; user-named range) | `0076`–`0083` | `0x1402039d0`–`0x1402169b5` | 235 | 1,095,039 disk | 74,025 | `ranges/0x1402039d0-0x1402169b5.md` |
| 11 (8 chunks; user-named range) | `0084`–`0091` | `0x140217cf0`–`0x14024f2ad` | 765 | 1,096,611 disk | 205,857 | `ranges/0x140217cf0-0x14024f2ad.md` |
| 12 (8 chunks; user-named range) | `0092`–`0099` | `0x14024f2c0`–`0x14026204e` | 226 | 1,075,206 disk | 74,834 | `ranges/0x14024f2c0-0x14026204e.md` |
| 13 (8 chunks; user-named range) | `0100`–`0107` | `0x140262050`–`0x140275350` (ends ≈`0x140275451`) | 258 | 1,102,614 disk | 74,840 | `ranges/0x140262050-0x140275350.md` |
| 14 (8 chunks; user-named range) | `0108`–`0115` | `0x140275450`–`0x140298b11` | 465 | 1,119,190 disk | 129,912 | `pass14_0x140275450-0x140298b11.md` |
| 15 (8 chunks; user-named range) | `0116`–`0123` | `0x140298b20`–`0x1402c16e0` | 510 | 1,117,178 disk | 143,192 | `pass15_0x140298b20-0x1402c16e0.md` |
| **total covered** | **124 chunks, contiguous** | `0x140001000`–`0x1402c16e0` | **9,130 catalogued / 8,265 read** | — | **2,259,801 Σ `size=`** | — |
| pending | `0124`–… | `0x1402c16e0`→ | — | — | — | resume here (block K regs open at chunk end) |

Corpus: 320,439,739 index bytes, 42,864,695 `.text` bytes, 119,757 functions, 2,228 chunks.
Passes 1–5 numbers are the pre-existing ledger/index numbers; passes 6–15 numbers are chunk-file
measurements and are not byte-comparable to them. Functions covered 9,130 = 4,793 (passes 1–5)
+ 519 (pass 6) + 740 (pass 7) + 401 (pass 8) + 218 (pass 9) + 235 (pass 10) + 765 (pass 11)
+ 226 (pass 12) + 258 (pass 13) + 465 (pass 14) + 510 (pass 15).
Σ `size=` total = 2,116,609 + 143,192 = **2,259,801** (5.27 % of `.text`) — covered by address, of
which **2,103,283 (4.91 %)** is actually read (pass-1 `0009`–`0013` = 865 fns / 156,518 Σ `size=`
is unread; pass 13 read via full-fidelity extractor + skeleton check; pass 14 read with warning
boilerplate filtered on chunks `0114`–`0115` + the `0113` tail — see both records' method notes).
Pass 5's row was corrected from 931,009 to 116,193 in this revision (see header).

**Provenance caveats:** pass 1 spans `0000`–`0013` by address, but only `0000`–`0008` were read
line-by-line — `0009`–`0013` (`0x140093150`–`0x1400c2ed0`, 865 fns) are census-only and still owe a
read (the record's own read-state table says so; its earlier "all 12 chunks read" line was wrong and
is fixed). Every pass 2–13 has its record in `ranges/` and regenerates from the chunk files.

## What the code is — cumulative synthesis (all 13 passes)

*Distilled reading of the 13 range records; the pass-by-pass list below is the chronological
evidence index. Claims are evidence unless marked [inference].*

### The sweep, and what "outside the range" means

`.text` is catalogued in **entry-address order** (2,228 chunks; 119,757 functions; 42,864,695 B).
After 124 chunks the cursor is at `0x1402c16e0`: **9,130 headers** (7.6 % of all functions),
Σ `size=` **2,259,801 B** (5.27 % of `.text`), of which 8,265 functions / 2,103,283 B are actually
read (pass-1 `0009`–`0013` pending). Because the order is by address, every routine referenced by
the read code but living at a higher address is simply **later, unread corpus** — not missing.
Examples, with the chunk that defines them: `FUN_140548d00` (container helper) `0237`,
`FUN_140f80f80` (allocator) `0836`, `FUN_140f94220` (allocator) `0839`, `FUN_141142f90`
(two-buffer helper) `0894`, `FUN_14114df10` `0896`, `FUN_1411a31e0` (arg17 callback) `0903`,
`FUN_1411c7cf0` (helper) `0915`, `FUN_1411d3e70` (allocator) `0916`, `FUN_1411dc260` (token-set
member) `0917`, `FUN_1411dfda0`/`FUN_1411e00c0` `0919`, `FUN_141212ed0` (helper) `0928`,
`FUN_141216c60` (pre-step) `0929`, `FUN_1421c69e0` (pre-step) `1596`, `FUN_1421c72e0`/
`FUN_1421c7780` `1597`, `FUN_1426c3bcc` (TLS init) `1834`. Pass 14 adds a new class of later-corpus
references — per-block allocator pre-steps and arg10 callback runs in the `0x1410f`–`0x14126xxxx`
bands (`FUN_14121a070`, `FUN_141227b30/cc0/e60/f30/8000`, `FUN_14122e070`, `FUN_14123fdb0`,
`FUN_141244840/4910`, `FUN_1412564e0/5b0`, `FUN_1410fbba0/fbc70`, callbacks
`FUN_1412254f0`–`FUN_141268980`) and two far class-root/payload bands (`0x143ecee70`,
`0x143ee0cd0`, `0x143e1/e3/f3xxxx`) — all in chunks ≈`0929`–`0990`/data corpus, ahead of the
cursor.

The other spelling matters: names printed `func_0x…` have **no decompiled body anywhere in this
dump** — the registrar `func_0x1421cd360`, both decryptors `d4f30`/`d4f70`, the record writer
`c2d50`, the copy helper `c2d70`, the shutdown registration `c7880`, the raw pointers
`0x140fd9670`/`0x140f7b210`, and `SUB_140551380`. Their bodies must come from the full Ghidra
project/EXE, not from the chunk stream; "decompile it" is not achievable by reading more chunks.

### Four layers, in address order

1. **Library preamble** `0x140001000`–`0x140039fc0`. ISA-L/igzip-shaped DEFLATE inflate (12 fns;
   64-bit MSB-aligned bit buffers, 8-byte litlen+dist pair entries, `vpinsrb` fast path); an
   `nvapi_QueryInterface` bootstrap with lazy per-id caches and a Wine probe; 53 identical NVAPI
   entry wrappers (lock → refcount++ → lazy `QueryInterface(id)` → call → `Direct_GetMethod`
   hooks); `Initialize`/`Unload`.
2. **NVIDIA driver-loading shim** `0x14003a230`–`0x14003d330`. A replacement `LoadLibrary` for
   `nv*.dll`: enumerate the GPU through D3DKMT (`QueryAdapterInfo(0x1f)` = user-mode driver name,
   vendor `0x10de`), SetupAPI device properties, service image paths and the Khronos Vulkan/OpenCL
   registry keys, then load the installed driver instead of the search-path copy. The 45 string
   literals of pass 1 all come from this layer and the NVAPI layer; after that the only readable
   names are the 12 `PTR_s_CompilerIDFilter_*` symbols and two `s_` ciphertext labels. There are no
   game strings anywhere in the read range.
3. **CRT/C++ static-init sea** `0x14003ffe0`–`0x1400fa760`. Five generator templates: the 181-B
   MSVC magic-static descriptor (**2,451** instances), 209-B std locale/facet statics (354), 58-B
   event-registration thunks (284), 134-B XOR-40 + cipher registrations (61), 37-B `_onexit`
   stubs. The 181-B template is the single largest construct read:
   `{+0x20 tag 1|2, +0x40 per-instance ctor FUN_140af…, +0x48 per-instance LAB_140b0…, +0x50
   shared &SUB_140551380 (usually) or per-instance label, +0x58 payload &DAT_143d…/143f…, +0x60
   shared PTR_DAT_14386…}` under a TLS guard. Reading [inference]: a generated table of
   per-record class/vtable descriptors; its consumer is ahead (`0x140551380`), so the table's
   purpose is not yet evidenced.
4. **Typed registry machine** `0x1400fbcb0`–`0x1402c16e0` (passes 2-tail–15). This is the
   substance of the read: one startup-time type/object registry, described next.

### The registry machine — six cooperating constructs

**Name buffers.** Every registration/builder carries its own XOR-8 ciphertext: 8-byte key at `+0`,
24-bit length in the low bytes of the uint32 at `+8`, done-flag at `+0xb`, payload at `+0xc`;
`buf[i] ^= key[i & 7]`, then the flag/length is cleared. Plaintext = the registered name (still
never decoded). Band: **`0x1438b8e50`–`0x1438da71c`** (crossed `0x1438d00000` in pass 13,
`0x1438da000` in pass 14).

**Registration** — `func_0x1421cd360(out, ciphertext, hash32, 0, size, align, flags, 0, token,
a10…a14, 0, 0, a17, base)`. **3,578 instances, 3,578 distinct hash32** — zero registration-hash
reuse across the entire read (pass 15 adds 351/351). `size` = object size 8…0x1150 (pass 15: 8 ×~14 and outliers to 0xda8/0xdc8/0x1150);
`align` 8 except one align-4 (`FUN_140273ff0`) and ten align-0x10 (pass 14 ×2 + pass 15 ×8);
`flags` 0 except flags 1 ×11 (pass 14 ×2 + pass 15 ×9) and **flags 10 ×1 (`FUN_1402bcb90`, pass 15
— first value outside {0,1,3} ever)**; `token` (arg9) is a category id: a nonzero token almost always pairs with one
fixed five-pointer set, **but pass 14 measured an exception — `0x9825b6271dce1d31` ×29 across two
different pointer sets (a `&DAT_141197ec0`-family block and an fd9670-quad block)**; a zero token
uses the generic container quad (`0x140f7b210` + `FUN_140548f80/FUN_14053a070/FUN_140548d00`), the
fd9670 quad, or the `&DAT_141197ec0`-family (`0x141142890` raw + `&DAT_14100e120/6710`). Args
10–14/17 advance in **parallel index bands, one entry per registration in address order** (no gaps
or reorders through 3,227 instances; pass 14: 283 distinct arg10 callbacks
`FUN_1412254f0`–`FUN_141268980`, one per reg). Reading: a generated registry of types, each
carrying a name, size, alignment, category and method/data pointers. Shape variants: 253-B
(arg17/18 set), 242-B (arg17/18 = 0, arg10 = container helper), 263-B (nonzero token, `&LAB_`
pairs), 270-B (263-B + nonzero arg16 `FUN_141232440` — pass 14), **267-B ×5 (pass 15: flags=1
carrier, `FUN_14029abe0` + four block-J/K siblings), 257/252-B**; pass 15 arg17 also carries
`&SUB_1412d2490`/`&SUB_1412d4350` (first SUB_-labeled arg17).

**Builder** — 397-B (`d4f70`, 620 instances), 373-B (`d4f30`, fixed pre-step, 116), 389-B (`d4f30`,
allocator variant, 39), 369-B rootless ×3 (pass 14), plus 472/475/480-B two-buffer and the rootless
365/374/377/479-B ladder. Shape: allocator/pre-step → inline XOR-8 decrypt → `d4f30/d4f70(&out,&buf,hash,0)`
→ `d4fb0` → store class root at `+0`, instance pointer at `+8`, flag 1 at `+0x78`; stack cookie. The decrypt
hash is reused by many builders (**hash = a type name; many instances per name**), the opposite of
the registration-hash regime. **Pass 14 regime changes: (a) allocator pre-steps abandon the shared
`FUN_140f80f80` (×0 this pass) for 14 per-block one-arg functions (`FUN_14121a070`,
`FUN_14121aae0`, `FUN_141227b30/cc0/e60/f30/8000`, `FUN_14122e070`, `FUN_14123fdb0`,
`FUN_141244840/4910`, `FUN_1412564e0/5b0`, `FUN_1410fbba0/fbc70`, plus `FUN_140f7b550(0x30)` ×3) —
one allocator per registration block, sizes matching the block's registered objects; (b) `d4f70`
is no longer exclusive to 397-B — five 558-B nested-atexit builders and one 574-B use it (the
558-B shape splits 5×`d4f30` / 5×`d4f70`); (c) one decrypted name (`0x45a7a69c`) is instantiated
seven times under one root by seven 373-B builders with different bare pre-steps.**

**Copy wrapper** — 241-B (848) / 231-B rootless (67) / **244-B ×1** (pass 14): no decrypt; `c2d70(&dst,&src)`
+ `d4fb0`; publishes an existing object with flag 0. Measured: `src = row slot − 0x20`, so each row is an
object header (root, ptr, flag, zeros) and the copy source is the row's own object. 231-B = the
same minus the class-root store; 244-B = 241-B plus a flag-1 store of `&PTR_s_CompilerIDFilter_1438d9ff0`
(the CompilerIDFilter write — see below).

**Sorted-insert builder** — 507-B (75) / 523-B (15) / 524-B (5) / 512-B (1) / 515-B (1) = **112** (pass 15: 523-B ×8, 507-B ×3, 515-B ×2, 524-B ×2 — 4 dual-decryptor incl. the first
`d4f70`-first 524-B),
every one sorting exactly **2** 56-B records keyed by the `uint` at `+8`; two decrypts + `d4fb0` +
count = 2. Eight pre-step recipes; pass 14's 515-B is the first to mix both decryptors
(`d4f30` + `d4f70`), and its decrypted-name pairs repeat across containers
({`0x15be7741`, `0xf29e4f35`} and {`0x909ee308`, `0xa321ebe9`} ×5 each). Reading [inference]: tiny
2-entry lookup tables built at startup.

**`{id,hash}` record** — 169-B / 178-B; **75 instances, 74/75 hashes equal a registration hash**
(pass 2: 6, pass 3: 14, pass 4: 1, pass 5: 15, pass 6: 7, pass 7: 2, pass 13: 5, pass 14: 16,
pass 15: 9 with the FIRST unmatched hash `0x3fd91271` — id `0x35`; all pass-15 178-B third fields
are 0).
Stores `{id, hash[, third]}` then `c2d50(&dst,&src)`. Ids span **3–0x18d** (pass 15: id `0x3` = new minimum, `0x122` within span); many-to-one is now normal — strongest: **four ids (`0x8f`,
`0x12b`, `0xd`, `0x8e`) → hash `0xce1a4d26`** (registration hash of `FUN_1402881d0`, size `0xe8`);
and the 178-B third field is nonzero twice (`0xa3c35f6d` in `FUN_140275450`; `0x79a00d3a` in
`FUN_140281230` = the hash of `FUN_140281130`), so a 178-B record can bind **two** registrations.
Reading [inference]: enum id → registered name, possibly id → (primary name, alias).

**Nested-atexit builder** — 558-B ×154, 542-B ×1, 574-B ×1 = **156 instances** (pass 14 adds the
542-B one-row and 574-B three-row variants and the first rootless 558-B): writes a row into the
shared shutdown table (`0x1438c6c68`–`0x1438cffc0`, plus `0x143db0208/0240` and pass-14 rows) whose
carried function pointer is one of six-plus initializer families — `PTR_FUN_14314b5b0` (×18),
`PTR_FUN_14315fba0`, `PTR_FUN_143149258`, `PTR_FUN_14314a748`, `PTR_FUN_14314a5e8`,
`PTR_FUN_14314bae8` + `PTR_LAB_14314bb98`, `PTR_FUN_1431be9f0`, `PTR_FUN_143167258` — calls
`atexit(&LAB_142f0b3xx…f1x)` (**35 labels now**, band `0x142f0ad80`–`0x142f0cab0`; pass 15 adds `0x142f0c070/c430/c6f0/c980/
caa0/cab0` and the shutdown table MOVES to `0x143e2b`–`0x143e42`) and
`c7880(&data)` (pass 14 also makes the first **2-arg** `c7880` call). Reading [inference]: static-object
destructor/shutdown registration; targets are labels in the undumped `0x142f0xxx` region.

Also present: **CompilerIDFilter shells** — 12 functions storing a flag and one of 12
`&PTR_s_CompilerIDFilter_*` labels (`14388ce90/cf68/d010`, `1438926c8/770/848/938/f38`,
`1438aca20/a68/ab0/b10`) plus payloads `&DAT_143eb63c0/67e0/6aa0/6940`; the only readable names
in the range, so this path bypasses the XOR-8 naming. **Passes 14–15 connect the registry to it: FOUR 244-B wrappers total (pass 14 `FUN_140298920`
`→PTR_s_CompilerIDFilter_1438d9ff0`; pass 15 `FUN_1402ac690/990/a90` → three NEW pointers
`1438de790/1438dd4b8/1438de9d0`, rooted on `&DAT_143eb6aa0`/`&DAT_143eb67e0`) store the pointer +
flag 1 into registration rows, and builders/wrappers root directly on the `0x143eb6xxx` payloads —
the payloads now double as class roots. [inference: a whole sub-block of the sea publishes
CompilerIDFilter objects into registered rows.] [inference: the sea registers at least part of the CompilerIDFilter/shader-filter machinery.]** And the guard furniture: every builder and
wrapper uses MSVC magic-static guards (TLS epoch + `_Init_thread_header/footer`) and a stack
cookie; registration functions carry neither.

### Where the data lives

| band | content |
|---|---|
| `0x1438b8e50`–`0x1438e7afc` | XOR-8 name/payload ciphertext (grows with the read; crosses `0x1438d00000` pass 13, `0x1438da000` pass 14, `0x1438e0000` pass 15; pass 15 also drops 3 new `PTR_s_CompilerIDFilter_*` labels into the band) |
| `0x143d2xxxx` … `0x143d90xxx`–`0x143d915xx`, `0x143d9`, `0x143da`, `0x143db`, `0x143dc`, `0x143dd`, `0x143de2–6`, `0x143de6`–`0x143e10` | registration outputs / instance slots; one fresh band per registration block (pass 14: a continuous seven-block sweep `0x143de6b80`–`0x143e107d0`; pass 15: `0x143e0f480`–`0x143e5bb40` in four blocks, bands `0x143e1/2/3/4/5`) |
| `0x143cf0000`–`0x143d05000` (± `0x143ce2090`; far `0x143f8e270`, `0x143f93cd0`, and pass-14 far `0x143eb6xxx`, `0x143ecee70`, `0x143ee0cd0`) | static class roots (vtable/type-descriptor pointers) — **pass 14 adds none of the old static roots; it uses only far bands** |
| `0x143da5c80`–`0x143e12020` | TLS guards / guard temps, extending with the sea |
| `0x1438c6c68`–`0x1438cffc0` (old) + **`0x143e2b–0x143e42` (pass 15, moved)** | shared nested-atexit/shutdown pointer table |
| `0x143c39f28`–`0x143e44970` (pass 15) | `{id,hash}` record storage (pass 15 rows interleave with output bands: `0x143e11548`, `0x143e2b570`–`0x143e2ba40`, `0x143e42b30`–`0x143e44970`) |

Dynamic roots: from pass 11 on, builders increasingly root themselves on **registration outputs**
(e.g. `&DAT_143d93520` ×51, `&DAT_143dcbd30`, `&DAT_143dc6920`), and pass 13's rootless ladder is
fed entirely by same-chunk registration rows. **Pass 14 completes the transition: not one of the
old static roots (`0x143cf0000`–`0x143d05xxx`, `0x143f8e270`, `0x143f93cd0`) appears in its 8
chunks — every root is a same-or-previous-block registration output (`&DAT_143de6b80` acts as a
≥15-builder mega-root; `&DAT_143e00ac0`/`0x143e00c20` root all 24 chunk-0113 wrappers) or a far
band (`0x143eb6xxx` CompilerIDFilter payloads, `0x143ecee70`, `0x143ee0cd0`, plus nested-atexit
payload slots in `0x143e1xxxx`/`0x143e3xxxx`/`0x143f3xxxx`).** Reading [inference]: the
registrations *declare* the types and the following chunk's builders *instantiate* them; the class
objects are runtime products, and the static-root era (passes 8–12) was the first generation.

### What it is for (reading conclusion)

Everything in `0x14003ffe0`–`0x1402c16e0` is **startup-time type/object registration**, not gameplay,
network, asset or UI code. The pattern is a generated, heavily templated registry: encrypted type
names are decrypted and registered with size/alignment/category/method tables; builders then
instantiate the named types into object rows; wrappers clone rows; 2-entry sorted tables and
`{id,hash}` rows expose the types to an id-based consumer that lives later in `.text`. **Passes 14–15's
decisive find: the registry writes into the one named subsystem in the file — the CompilerIDFilter
chain (four 244-B wrappers rooted on CompilerIDFilter payloads store `&PTR_s_CompilerIDFilter_*`
pointers + flag 1 into registration rows; pass 15's three live in the ciphertext band itself). [inference: what is registered here is, at least in part, the
shader/compiler filter machinery.]** No consumer, no name plaintext and no gameplay logic has been
read yet. Confidence: counts/shapes/bands/correlations are measured; the "type registry / shutdown
table / lookup table" labels are shape-based inference.

**Known limits.** (a) The registrar and both decryptors are `func_0x…` — no body in the dump.
(b) No name buffer has been decrypted. (c) The atexit label region (`0x142f0xxx`) is not in the
dump. (d) Four unlisted gaps inside the read range are uninspected (`0x1401828e8`, `0x140190298`,
`0x1401a4e02`–`0x1401abad0` 27,854 B, `0x140229be7`–`0x14022dcc0` 16,601 B). (e) Pass-1
`0009`–`0013` remain unread.

## Complete image of the code read so far

*Chronological evidence index (the synthesis above is the distilled reading).* Everything read
(124 contiguous chunks, `0x140001000`–`0x1402c16e0`) belongs to **static
initialization / registration machinery**. No gameplay, network protocol, asset parsing or readable
user-facing string (the only string-like symbols in the whole range remain the undecoded
`s_JIubLB__1438b8f04` label at `FUN_1401d85c0`, pass 8, and `s_d____WQ_1438cd11c` at
`FUN_1402300d0`, pass 11; the only *named* symbol since pass 5 is `PTR_s_CompilerIDFilter_1438d9ff0`,
written by pass 14's `FUN_140298920`). The image, by zone:

1. **Library preamble** `0x140001000`–`0x1400034b1` — ISA-L/igzip-like DEFLATE inflate (12 functions).
2. **NVAPI layer** `0x1400372f0`–`0x140039fc0` — `nvapi_QueryInterface` bootstrap, Wine probe, wrappers.
3. **Driver redirection shim** `0x14003a230`–`0x14003d330` — D3DKMT/SetupAPI/registry loader.
4. **CRT/C++ static-init sea** `0x14003ffe0`–`0x1400c2ed0` — ~2,000 copies of five templates;
   XOR-40 string decryptors; descriptor run.
5. **Descriptor sea continuation** `0x1400c2f90`–`0x1400fa760` — same 181-B template.
6. **Typed registry** `0x1400fbcb0`–`0x14010bf30` — XOR-8 names, `{id,hash}` tables, 18-arg
   `func_0x1421cd360` registrations, TLS-guarded builders, sorted 56-B records.
7. **Consolidated pass 3** `0x14010c120`–`0x14012bcd0` — 265 registrations, 129 builders, 14
   `{id,hash}` tables, 28 sorting builders; 0x14100xxx callback band.
8. **Pass 4** `0x14012bee0`–`0x140156840` — 524 functions; zones Z20–Z32: 387 registrations +
   136 builders + 1 `{id,hash}` table; nested-atexit builder family (51 × 558 B, hash `0xf891229f`,
   base `&DAT_143c834d0`); 5 CompilerIDFilter shells.
9. **Pass 5** `0x140156950`–`0x140175867` — zones Z35–Z44: 222 registrations (137 zero-token /
   85 nonzero), container quadruple ×108, 50 × 558-B nested-atexit builders, 241/231-B two-guard
   copy wrappers, 373-B pre-step builders, 507-B two-decrypt sorted-insert builders (8, all sorting
   2 records), 15 `{id,hash}` static records (all hash-matching), 9 CompilerIDFilter shells total.
10. **Pass 6** `0x140175ab0`–`0x14019d171` — zones Z45–Z61 (range doc lost; highlights preserved):
    367 registrations, 367 distinct hashes; 146 × size 8 band; container quadruple ×235; fd9670 quad
    ×105; five-pointer sets ×5; `&DAT_14100e120/&DAT_141006710` as args 13–14 (first); arg17 runs
    (~100 labels); builders dominating second half; `{id,hash}` ×7 (37/37); 13th two-buffer helper
    `FUN_141142f90` with hash `0x7e82c4d1` = registration hash of `FUN_14019afc0`; two unlisted gaps.
11. **Pass 7** `0x14019d180`–`0x1401d265d` — zones Z62–Z64. Highlights:
    - **Z62 `0x14019d180`–`0x1401a4b90`: 123 two-guard copy wrappers** (122 × 241 B at 0x100 stride +
      1 × 231 B), **all with base `&DAT_143d13560`**; guard DAT bands sweep `0x143d107xx`–`0x143d134xx`,
      `0x143d20axx`–`0x143d20d58`, `0x143d0fbb8`–`0x143d118d0`.
    - **Z63 `0x1401a4ca0`–`0x1401a4d50`: 2 `{id,hash}` static records** — ids `0x188`/`0x187`; id
      `0x188` carries hash **`0x7e82c4d1`**, the shared registry hash (registration + two-buffer
      helper + now static record). **39/39 cumulative hash-match.**
    - **Unlisted gap `0x1401a4e02`–`0x1401abad0`** (27,854 B, no function headers).
    - **Z64 `0x1401abad0`–`0x1401d2560`: 615 registrations**, all 253/263 B, no TLS guards, no
      pre-steps, no atexit. 615 distinct hashes (zero reuse). Sizes 0x10–0x68 (0x18 ×218, 0x20 ×124,
      0x10 ×91, 0x28 ×85, 0x30 ×45…) with two outliers **0x230 / 0x228**. align 8 ×615, flag 0 ×615.
    - **arg9 nonzero: 73 regs / 44 distinct** — reuse now normal: `0x66fa7db7cdf09bc0` ×7,
      `0x69894cb48700fe3d` ×7, `0x2a62b23214ee5032` ×5, `0x9bc9e1bfd09cf4b5` ×5,
      `0xacc6d84b47a8a9d7` ×5, `0xc6846d31948dd076` ×3, 4 ×2, 36 singletons.
    - **Pointer sets**: fd9670 quad (args 11–14) ×**504**; `0x140f7b210`+container-triple quad ×**32**
      (375 cumulative uses of the raw pointer); `&DAT_14100e120/&DAT_141006710` at args 13–14 ×8;
      five-pointer sets whose args 11–14 walk four parallel DAT/FUN bands in registration order
      (`&DAT_141197c90→&DAT_141198830`, `FUN_1411b8130→FUN_1411b9780`, `&DAT_1411c6550→&DAT_1411c6ae0`,
      `&DAT_141189990→&DAT_141189eb0`).
    - **Parallel per-registration runs**: arg10 `FUN_1411ad470`–`FUN_1411b4ee0` (546/614 fixed-stride
      steps, small local reorders) and arg17 `FUN_1411a31e0`–`FUN_1411aa4d0` (610/614).
    - `FUN_`/`&DAT_` label alternation for the same 0x1411b8xxx–b97xx addresses at arg12.
12. **Pass 8** `0x1401d2660`–`0x1401ef8e0` — zones Z65–Z66 (record
    `ranges/0x1401d2660-0x1401ef8e0.md`; 401 fns, Σ `size=` 115,925 — re-derived from chunks
    `0061`–`0067` on 2026-11-20, matches the record exactly):
    - **Z65 `0x1401d2660`–`0x1401e2669`: 255 registrations** (253 B ×238 + 263 B ×17), direct
      continuation of Z64 — `func_0x1421cd360` ×255, 252/252 distinct hashes (zero reuse), sizes
      0x10 ×111+, 0x18 ×63, 0x20 ×37+1, 0x28 ×25, …, **0x118 ×1** (`FUN_1401e2570` — third large
      outlier after 0x230/0x228), two **size-8** regs. align 8 ×255, flag 0 ×255.
    - **First named string symbol** in the read range: `s_JIubLB__1438b8f04` passed as arg2 by
      `FUN_1401d85c0`.
    - **arg9 nonzero: 17 regs / 16 distinct (6.7 % rate)** — first in-band token reuse:
      `0x33783e799338f436` ×2 shared by `FUN_1401dfbf0` (0x58) + `FUN_1401dfd00` (0x50) with one
      five-pointer set; pass-7 top `0x66fa7db7cdf09bc0` recurs ×1. Each nonzero-token reg pairs 1:1
      with a fixed set (args 10–14).
    - **Parallel per-registration runs extended**: arg10 `FUN_1411b4f20`–`FUN_1411b8070` (236
      instances, 0x30 stride, continuing pass-7's run); arg17 `FUN_1411aa500`–`FUN_1411ad3c0` (248,
      0x30 stride, continuing `FUN_1411aa4d0`). Lock-step over the full block — no gaps, no reorders.
    - **arg11–14 families**: fd9670 quad ×227 raw (731 cumulative per the pass-8 record; the pass-6
      ×105 + pass-7 ×504 rows sum with it to 836 — counting-unit mismatch to resolve);
      container quad ×4 (379 cumulative); **new sub-family ×5** with raw arg12 `0x141142890` and
      args 13–14 `&DAT_14100e120`/`&DAT_141006710` (13 cumulative). FUN_/LAB_ alternation continues
      at args 12/13/14/17 (e.g. `FUN_1401e0220`, `FUN_1401e2150`/`FUN_1401e2360`, `FUN_1401defd0`).
    - **Z66 `0x1401e26f0`–`0x1401ef8e0`: builder sea** — 102 builders + 44 copy wrappers (146):
      397-B ×80 (pre-step = allocator `FUN_140f80f80` 0x10 ×69 / 0x20 ×9 / 0x38 ×1 / 0x50 ×1;
      `d4f70` ×80), 373-B ×18 (pre-step = one fixed call: `FUN_1421c7480()` ×6 + 11 single-use
      pre-steps; `d4f30` ×18), **558-B nested-atexit ×2** (`FUN_1401e7be0` hash `0xe56f0386`,
      `FUN_1401edef0` hash `0x6f93c9ce`; `PTR_PTR_1438c6fc8/6ff8 = &PTR_FUN_14314b5b0`,
      `PTR_DAT_1438c6ff0/7020 = &DAT_143d2fc18/143d2fc48`, `atexit(&LAB_142f0add0/142f0ada0)`,
      `c7880(&DAT_143d90a08/143d90a20)`), **523-B two-decrypt sorted-insert ×2** (`FUN_1401e7e20`,
      `FUN_1401e8030`; pre-steps `FUN_14114de40(0x10)` + `FUN_14114dca0(0x1f0)`/`FUN_14114dd70(0x1f0)`
      — new allocator trio; hashes `0x5efe267`/`0xbc2a8da3`; sort 2 records — **22 cumulative, all
      2-record**), 241-B wrappers ×44 (mixed bases).
    - **Builder decrypt hashes: 53 distinct / 104 calls — heavy reuse** (`0xa83c2c26` ×23,
      `0x7dd813e` ×10, `0x903303` ×7, `0x176ed263` ×4, 11 hashes ×2, 41 singletons). `0x89440237`
      shared by two builders with the same base but different output slots; `0x903303` by three.
    - **Builder base pointers** (146 assignments): `&DAT_143d013b0` ×27, `&DAT_143d01930` ×23,
      `&DAT_143d030a0` ×19, `&DAT_143d01a90` ×16, `&DAT_143cfa130` ×13, `&DAT_143d03780` ×12,
      `&DAT_143d03620` ×10, `&DAT_143cfc6a0` ×9, `&DAT_143d087a0` ×4, `&DAT_143d04970` ×4,
      `&DAT_143d70e30` ×2, `&DAT_143d02c80` ×2 + singles — **10 roots cover 133/146**.
    - No strings (except the one `s_` label), no CompilerIDFilter shells, no `{id,hash}` records,
      `c2d50` ×0 (39/39 cumulative stays). Canary ×102; `FUN_1426c3bcc` ×296 (registrations ×0).
13. **Pass 9** `0x1401efa00`–`0x1402039cd` — zones Z67–Z68. Highlights:
    - **Z67 `0x1401efa00`–`0x1401f6570`: pure pre-step-builder run**, 48 fns, all 389/397 B.
    - **Z68 `0x1401f6580`–`0x1402039cd`: builders interleaved with 52 × 241-B copy wrappers**
      (irregular stride, ~13 bases, src = same-family DATs `0x143d5xxxx`–`0x143d7xxxx`) and
      **2 × 558-B nested-atexit builders** (`FUN_1401f7600` hash `0x16b04af1`, `FUN_1401ff220`
      hash `0x7e2a700b`) writing shared pointer-table rows `0x1438c6db8`–`0x1438c6ed0` with
      `PTR_PTR … = &PTR_FUN_14314b5b0` and `atexit(&LAB_142f0adb0/142f0ade0)`.
    - **Size census: 241 ×52, 389 ×5, 397 ×159, 558 ×2.**
    - **Allocators: `FUN_140f80f80(0x10)` ×122, `(0x20)` ×37; `FUN_14114df10(0x10)` ×5** — the
      389-B sub-family is exactly {FUN_14114df10, d4f30, hash `0x539f7774`} (5/5).
    - **Decrypt hashes: 41 distinct / 166 uses** — top `0xa83c2c26` ×82 (49 %), `0x37ab13d3` ×12,
      `0x4e87690f` ×7; `0x7e2a700b` crosses shapes (397-B ×2 + 558-B ×1).
    - **13 recurring class bases** in `0x143cfa130`–`0x143d04cf0` (+ far `&DAT_143f8e270` ×4)
      — **17 distinct roots combined with pass 8**.
    - Guards 440 in `0x143d210c8`–`0x143d90988`; ciphertext band 332 refs in
      `0x1438b8e50`–`0x1438c6fxx`; warnings 51–52/function (11,170 total).
    - **Builder sea combined (Z66+Z67+Z68): `0x1401e26f0`–`0x1402039cd`, 364 builders/wrappers.**
      `d4f70` ↔ 397-B strictly (239/239 cumulative); `d4f30` ↔ all other shapes (31 cumulative).
      The nested-atexit pointer table now spans `0x1438c6db8`–`0x1438c7020` (×6
      `PTR_FUN_14314b5b0` initializers, all `PTR_PTR`-carried, never called); atexit labels
      `0x142f0ada0/adb0/add0/ade0`.
14. **Pass 10** `0x1402039d0`–`0x1402169b5` — zones Z69–Z70 (full record:
    `ranges/0x1402039d0-0x1402169b5.md`). Highlights:
    - **235 fns, Σ `size=` 74,025; size census: 241 ×119, 397 ×88, 253 ×8, 373 ×11, 558 ×5,
      507 ×1, 524 ×1, 231 ×2.** Call targets: `FUN_1426c3bcc` ×464, `c2d70` ×227, `d4fb0` ×229,
      `d4f70` ×89, `d4f30` ×19, `c7880` ×5, canary ×106, warnings 11,672.
    - **Z69 `0x1402039d0`–`0x140213b50`: builder-sea continuation.**
      - **`&DAT_143d013b0` mega-run ×131 (57 % of the pass's functions)** — one dominant class root
        across ~`0x140208830`–`0x140214560`; tightest cluster = 6 × hash `0x91a9d4cc` on the
        **new recurring root `&DAT_143cfe0d0`** at `0x1402063c0`–`0x140206b90`.
      - **373-B fixed-call pre-steps ×11** with 14 fixed pre-steps total: recurring
        `FUN_1421c7480` ×5; new single-use `FUN_141520a50`, `FUN_1414134c0`, `FUN_140f817e0`,
        `FUN_140f818a0`, `FUN_141530ba0`, `FUN_14132a2b0`; `FUN_1421c7220` ×2, `FUN_1421c7780` ×1
        (in sorted-insert builders). `0x6a928816` ×2 with two different pre-steps, same base —
        hash = name, pre-step = instance wiring.
      - **Sorted-insert variants diversify**: `FUN_140209910` (507 B; pre-steps `FUN_1421c7220()` ×2,
        no allocator; hashes `0xf81f4386`/`0xfbebad6f`) and `FUN_14020b7a0` (524 B; pre-steps
        `FUN_140f80f80(0x10)` + `FUN_1421c7780()`; hashes `0x21ed0bc3`/`0x8f4a353d`) — **24
        cumulative, all still exactly 2 records**; four distinct pre-step recipes now known.
      - **5 × 558-B nested-atexit builders** (`FUN_140203ed0`, `14020ac30`, `140211a20`,
        `140212e20`, `140214b00`) with **new atexit labels `0x142f0ad80/ae00/ae10/ae20/ae60`**
        (band now `0x142f0ad80`–`0x142f0ae60`, 9 labels cumulative), `PTR_PTR … = &PTR_FUN_14314b5b0`
        ×5 (**11 cumulative**), new `PTR_DAT` rows → `&DAT_143d2fa68/fbe8/f888/f978/fbb8`;
        the `PTR_PTR`/`PTR_DAT` rows now interleave in `0x1438c6c68`–`0x1438c6fc0`.
      - **`FUN_140f80f80(8)` ×2** — first size-8 allocations in the sea.
      - **231-B wrapper + local-base pair** (new sub-shape): `FUN_140213540` (231 B; first line
        `_DAT_143d3bb80 = 0`, c2d70 src `&DAT_143d3bb60`) ↔ `FUN_1402133b0` (397 B, base
        `&DAT_143d3bb60`, hash `0x53cb5d89`, alloc 8); `FUN_140215140` (231 B; `_DAT_143d6ba30 = 0`,
        c2d70 src `&DAT_143d6ba10`) ↔ `FUN_140215240` (397 B, base `&DAT_143d6ba10`, hash
        `0xfcc616fc`, alloc 8). A 231-B wrapper = 241-B wrapper minus the class-root store; the
        "class" is a locally-built object.
      - **Base census: 23 distinct roots + 2 base-less 231-B wrappers.** `&DAT_143d013b0` ×131,
        `&DAT_143d01a90` ×19, `&DAT_143cfc6a0` ×13, `&DAT_143d03780` ×11, `&DAT_143d01930` ×10,
        `&DAT_143d030a0` ×6, `&DAT_143cfe0d0` ×6 (new root → **18 recurring roots**), `&DAT_143d02c80`
        ×5, `&DAT_143d087a0` ×5, `&DAT_143d03620` ×4, `&DAT_143d03a40` ×2, `&DAT_143d04970` ×2,
        11 singles (incl. first builder bases in the `0x143d6xxxx` band `&DAT_143d6e370`, and
        `&DAT_143d937e0`, `&DAT_143d04cf0`, `&DAT_143d30820`, `&DAT_143d06950`, `&DAT_143d93520`,
        `&DAT_143d3bb60`, `&DAT_143d6df50`, `&DAT_143d6ba10`).
      - **Allocators: `FUN_140f80f80(0x10)` ×62, `(0x20)` ×16, `(0x30)` ×1, `(8)` ×2.**
      - **Decrypt hashes: 49 distinct / 108 uses** — top `0xa83c2c26` ×20, `0x57cbdd1e` ×8,
        `0x903303` ×7, `0x91a9d4cc` ×6, `0x7dd813e` ×6, `0xe0c06cf7` ×5, `0x548e5344` ×4;
        name-reuse regime unchanged.
    - **Z70 `0x140215530`–`0x1402169b5`: the `0x143d9xxxx` registration band — FIRST registrations
      since pass 8** (cumulative `func_0x1421cd360` 1,245):
      - **8 × 253-B registrations** at `0x100` stride, all size `0x20` (uniform — pass 7–8 blocks
        mixed sizes), align 8, flag 0, arg9 = 0 ×8, 8 distinct hashes (`0x273660c3`, `0x5b95082f`,
        `0x5324de6b`, `0xe2c1e392`, `0xe81930f3`, `0xe10b6ed8`, `0x8db8e9c2`, `0x78cc2064`).
        fd9670 quad ×8 (cumulative 739 by pass-8 statement / 844 by summed rows); args 12–14 =
        fixed triple `0x14064fec0 / &LAB_140aa6750 / &SUB_14064feb0` (new values).
      - **New data band `0x143d90xxx`–`0x143d915xx`**: registration outputs (arg1) and arg18 slots
        both live there; ciphertext extends to `≥0x1438c7194`.
      - **Parallel runs extended into a new callback band**: arg10 `FUN_1411c71e0`–`FUN_1411c73a0`
        (8 × stride `0x40`); arg17 `FUN_1411c7060`–`FUN_1411c71b0` (8 × stride `0x30`); arg17 band
        precedes arg10 (as in passes 7–8). Gap `0x1411b8070`→`0x1411c7060` unaccounted.
      - **Immediately after: 8 × 397-B builders** (`FUN_140215d30`–`FUN_140216820`), all base
        **`&DAT_143cfc6a0` ×8**, all hash **`0x57cbdd1e` ×8**, allocator **`FUN_140f94220(0x10)`
        ×8 (new allocator)**, result stores in the same `0x143d9xxxx` rows — one
        registration→build unit for 8 like-typed objects.
    - No `{id,hash}` records, no CompilerIDFilter shells, no `s_` strings, `c2d50` ×0,
      `0x140f7b210` ×0 (cumulative stays 379).

15. **Pass 11** `0x140217cf0`–`0x14024f2ad` — zones Z71–Z75 (full record:
    `ranges/0x140217cf0-0x14024f2ad.md`). Highlights:
    - **765 fns, Σ `size=` 205,857; size census: 253 ×633, 263 ×40, 241 ×24, 397 ×18, 475 ×14,
      389 ×13, 480 ×8, 472 ×5, 373 ×6, 524 ×2, 507 ×1, 558 ×1.** Call targets: `cd360` ×673,
      `FUN_1426c3bcc` ×186, `d4fb0` ×95, `c2d70` ×92, `d4f30` ×43, `d4f70` ×28, canary ×68,
      `c7880` ×1, `atexit` ×1, `c2d50` ×0, warnings 4,677.
    - **Z71 `0x140217cf0`–`0x140221773`: 154 zero-token registrations** (block A, outputs still all
      `0x143d9xxxx`); arg10 run restarted at **`FUN_1411d9c60`**, arg17 at **`FUN_1411d7f10`**.
    - **Z72 `0x140221780`–`0x14022993d`: builder sea A, 80 builders.** **11 new two-buffer helpers**
      (all `(0x20,&buf,0,hash)`: `FUN_140f94720/94810/94900/949f0`, `FUN_141011270`, `FUN_1410f5950/
      f5b30`, `FUN_141108870`, `FUN_140fa5220`, `FUN_1411c7c00/c7cf0`; helper count 13 → **24**;
      helper hashes 11 distinct / 27 uses, top `0x2c162b97` ×5). **New allocator `FUN_1411d3e70(0x20)`
      ×17** + `FUN_140f80f80(0x10)` ×8 / `(0x20)` ×8. 8 new bare pre-steps (`FUN_14190dbc0/dc80/
      dd40`, `FUN_1413dc060`, `FUN_1410eae80`, `FUN_1421c6920` ×2, `FUN_1421c76c0` ×2,
      `FUN_1421c72e0`). Sorted-insert 24 → **27** (7 recipes; 507-B `FUN_140228790` =
      {`FUN_1421c72e0()` + `FUN_1421c76c0()`} — first no-allocator recipe; 524-B `FUN_140223cf0`/
      `FUN_140225930` = {`FUN_140f80f80(0x20 or 0x10)` + `FUN_1421c6920()`}; shared hash
      `0x3b171026` on both 524-B). **`&DAT_143d93520` = new dominant class root ×51 — and it is a
      Z71 registration output (dynamic root); c2d70 sources are 0x143d9 outputs ×32/43** — the
      pass-10 local-base pair convention is now the majority regime.
    - **Z73 `0x1402299d0`–`0x140229bf0`: 2 regs sharing token `0x292f8ed1cad53cdb`** (size 0x20
      both, different per-member sets, outputs `0x143daxxxx` — first band-b jump), followed by
      **unlisted gap `0x140229be7`–`0x14022dcc0` = 16,601 B** (third gap; pass 7's was 27,854 B).
    - **Z74 `0x14022dcc0`–`0x14024e34c`: registration block B, 517 regs** — outputs move to new
      bands `0x143dbxxxx` ×162, `0x143dcxxxx` ×186, `0x143ddxxxx` ×169. **arg10 run
      `FUN_1411d9c60`–`FUN_14120a3d0`** (673 entries, stride 0x30 ×449 / 0x40 ×213), **arg17
      `FUN_1411d7f10`–`&LAB_141203d50`** (stride 0x30 ×661), lock-step, no gaps. **Token regime:
      40 nonzero / 23 distinct with heavy reuse** (`0xc1bcbc118749a288` ×5, `0x395a90533815064c` ×4,
      `0xcd762a89f2ca61d7` ×4, `0x71977bedc4df7a42` ×4, 4 ×2, 15 singletons) — shared token always
      = same five-pointer set; zero-token sets: fd9670 quad ×445, `DAT_141197ec0`-family ×145,
      **`0x140f7b210`+container-triple ×40 (cumulative raw uses 379 → 419)**, and 3 zero-token regs
      with a *five-pointer* set (new). **Second `s_` string: `s_d____WQ_1438cd11c`** (arg2 of
      `FUN_1402300d0`). Last regs' sets/arg17 use `&LAB_` labels incl. far `&LAB_140f7d580/140f7cbd0`
      and arg17 `&LAB_141203d40/141203d50`.
    - **Z75 `0x14024e3d0`–`0x14024f2ad`: builder tail.** 8 × 241-B wrappers (bases `&DAT_143d013b0`
      ×6 + `&DAT_143d01a90` ×2; c2d70 sources = new `0x143db` outputs); **1 × 558-B nested-atexit
      builder `FUN_14024e5d0`** (base `&DAT_143cfa130`, hash `0x277a0ae4`) with a **new row kind**:
      `_DAT_143db0230 = &DAT_143eeb240`, `_DAT_143db0208 = &PTR_FUN_14315fba0` (**not** 14314b5b0),
      **`atexit(&LAB_142f0b450)` — new atexit label outside `0x142f0ad80`–`0x142f0ae60`**,
      `c7880(&DAT_143db0240)`; 3 × 397-B builders (bases `&DAT_143d03a40`, `&DAT_143d03780`,
      **`&DAT_143d04130` new**), hashes `0xae2d8911`, `0xc3e03c7f` ×2 across different bases.
    - No `{id,hash}` records, no CompilerIDFilter shells, `c2d50` ×0. Decrypt hashes 49 distinct /
      71 uses (top `0xe2bf1226` ×5). Guard bands `0x143d91b38`–`0x143de1eac`; ciphertext band
      `0x1438c71b`–`0x1438cfd2`.

16. **Pass 12** `0x14024f2c0`–`0x14026204e` — zone Z76 (full record:
    `ranges/0x14024f2c0-0x14026204e.md`). Highlights:
    - **226 fns, Σ `size=` 74,834; size census: 397 ×118, 241 ×99, 558 ×4, 373 ×3, 389 ×2.**
      Call targets: `FUN_1426c3bcc` ×460, canary ×127 (exactly the non-wrapper builders),
      `FUN_140f80f80` ×118, `d4f70` ×118, `d4f30` ×9, `d4fb0` ×226, `c2d70` ×226, `c7880` ×4,
      `atexit` ×4, `cd360` **×0 (no registrations at all)**, `c2d50` ×0, warnings 11,625 (≈51.4/fn).
    - **`d4f70` ↔ 397-B correlation EXACT again: 118/118; `d4f30` ×9 = 558×4 + 373×3 + 389×2.**
      Pass 12 contains zero two-buffer helpers — the passes 10–11 deviations were entirely
      attributable to them.
    - **4 × 558-B nested-atexit builders**, all `PTR_PTR = &PTR_FUN_14314b5b0` (×15 cumulative),
      all payloads `0x143dbxxxx` slots, rows at `0x1438cfd50`–`0x1438cff88`:
      `FUN_14024fef0` (base `&DAT_143d01a90`, hash `0x4ce56bc0`, **atexit `LAB_142f0b410`**,
      payload `&DAT_143db1e68`), `FUN_1402545a0` (base `&DAT_143d01930`, `0x7ac92ddc`,
      **`LAB_142f0b360`**, `&DAT_143db1d48`), `FUN_14025f650` (base **`&DAT_143dcbd30` — first
      nested-atexit member with a dynamic root**, `0xc3e03c7f`, **`LAB_142f0b390`**,
      `&DAT_143db1f58`), `FUN_140261e20` (base `&DAT_143d013b0`, `0x454d41e3`,
      **`LAB_142f0b400`**, `&DAT_143db1dd8`).
    - **2 new allocators, both ×1, both in 389-B builders on the `d4f30` side:**
      `FUN_1411dfda0(0x10)` (`FUN_14024f450`) and `FUN_1411e00c0(0x10)` (`FUN_140258050`) —
      third/fourth members of the `0x1411d/e` allocator family next to `FUN_1411d3e70`.
      `FUN_140f80f80` ×118 (0x10 ×77, 0x20 ×41), all inside 397-B builders.
    - **3 new 373-B fixed pre-steps** (each ×1): `FUN_14190de00` (`FUN_14024fb70`),
      `FUN_1421c6860` (`FUN_140253590`), `FUN_14158bcf0` (`FUN_140259de0`).
    - **Bases: 21 distinct.** Recurring: `&DAT_143d03780` ×49, `&DAT_143d01a90` ×33,
      `&DAT_143d03a40` ×29, `&DAT_143d013b0` ×25, `&DAT_143cfa130` ×25,
      **`&DAT_143f8e270` ×20 (far; now 6th overall)**, `&DAT_143d01930` ×10, `&DAT_143d04970` ×10,
      `&DAT_143d02c80` ×4, `&DAT_143d03d10` ×3, `&DAT_143d030a0` ×2 + singles
      (`&DAT_143d02700`, `&DAT_143d02de0`, `&DAT_143d30820`, `&DAT_143d03bb0`, `&DAT_143d03620`,
      **`&DAT_143f93cd0` new far root**, 2 addresses from the long-open `0x143f93e30`).
      Dynamic roots: `&DAT_143dc8fb0` ×4, `&DAT_143dcbd30` ×3 (558-B + 2 wrappers),
      `&DAT_143db8170` ×2, `&DAT_143dde5b0` ×1. All `c2d70` copy sources are one-off
      `0x143db/c/d` slots (each used exactly once).
    - **Decrypt hashes: 55 distinct / 127 uses — two dominant names: `0x37ab13d3` ×24**
      (chunks 0094–0095 run) **and `0xf5087894` ×21** (chunks 0098–0099 run); then
      `0x227307c8` ×6, `0x5dc61e59` ×6, `0x8f80faa`/`0xa83c2c26`/`0x67465e75`/`0x91a9d4cc` ×4,
      `0x4a672fc3`/`0xe41699c9` ×3, `0x1d993f9`/`0x216ea6da` ×2, 41 singletons.
      `0xde3c867c` is the only hash seen through both decryptors (d4f30 + d4f70).
    - No `{id,hash}`, no CompilerIDFilter, no `s_` strings, no sorted-insert builders, no
      231-B wrappers, no `0x140f7b210` uses, `c2d50` ×0. Guards span
      `0x143da5cf0`–`0x143de2c78`; ciphertext extends to `0x1438cffxx`.

17. **Pass 13** `0x140262050`–`0x140275350` — zones Z77–Z78 (full record:
    `ranges/0x140262050-0x140275350.md`). Highlights:
    - **258 fns, Σ `size=` 74,840; size census: 241 ×151 (majority again), 397 ×61, 253 ×12,
      242 ×8, 373 ×6, 558 ×3, 169 ×3, 365 ×3, 178 ×2, 507 ×2, 263 ×2, 389/374/377/231/479 ×1.**
      Call targets: `FUN_1426c3bcc` ×478, canary ×79 (exactly the 79 decrypt-carrying fns),
      `FUN_140f80f80` ×62 (0x10 ×54, 0x20 ×7, **8 ×1**), `FUN_1411dfda0(0x10)` ×1 (2nd use),
      `cd360` ×22, `c2d70` ×231, `d4fb0` ×233, `d4f70` ×63, `d4f30` ×18, `c2d50` ×5,
      `c7880` ×3, `atexit` ×3, warnings 11,907 (≈46.2/fn).
    - **Z77 `0x140262050`–`0x140272d33`: wrapper/builder sea (224 fns).** Roots: `&DAT_143d013b0`
      ×156, `&DAT_143d03780` ×10, `&DAT_143cfc6a0` ×8, `&DAT_143d01a90` ×7, far `&DAT_143f8e270` ×7
      (5 wrappers + 2 builders), `&DAT_143cfa130` ×7, `&DAT_143d03d10` ×5, `&DAT_143d02c80` ×4,
      `&DAT_143d04cf0` ×3, `&DAT_143d04130` ×3 (now recurring), `&DAT_143d04970` ×3,
      `&DAT_143d03a40` ×3, `&DAT_143d03bb0` ×3 + singles `&DAT_143d03620`,
      **`&DAT_143d03fd0` (new)**, **`&DAT_143ce2090` (new band, 507-B)**, dynamic `&DAT_143dd2600`,
      `&DAT_143dc6920`. **MEASURED: two-arg c2d70 src = root-slot − 0x20 in 152/153 cases** —
      one object row per wrapper; pass-12's "one-off sources" subsumed.
    - **Hash-run census: `0x8f80faa` ×15 (new dominant), `0x861c6fe6` ×8 (new; 8-builder run in
      chunk `0104`), `0x37ab13d3` ×6, `0xf5087894`/`0x7dd813e`/`0xa4339167` ×4,
      `0x5dc61e59`/`0xc9ad5769` ×3** — 39 distinct / 81 uses. `0x7dd813e` now seen through BOTH
      decryptors (d4f30 ×3 + d4f70 ×1, 377-B `FUN_140272ae0`).
    - **373-B fixed pre-steps ×6, every pre-step NEW single-use**: `FUN_14154b9a0` ×2,
      `FUN_1413fb970`, `FUN_14140e210`/`FUN_14140e2d0` (0xC0-stride run), `FUN_1418b7c60`.
      **365-B ×3** (`FUN_140274700/48a0/4a10`): rootless 373-B-minus-root variant, pre-step
      **`FUN_141216c60(0)` — first pre-step with an argument**, each rooted on a 242-B
      registration output. **374-B ×1** (`FUN_14026c6a0`): 373-B with 2-arg c2d70.
      **377-B ×1** (`FUN_140272ae0`): 397-B minus root store, alloc 8.
    - **3 × 558-B nested-atexit** (`FUN_1402627e0`, `FUN_140272360`, `FUN_140272690` — the last
      with dynamic root `&DAT_143dc6920` = wrapper `FUN_140272590`'s output slot),
      `PTR_PTR = &PTR_FUN_14314b5b0` ×3 (**×18 cumulative**), rows `0x1438cfed0`–`0x1438cffc0`,
      payloads `&DAT_143db1ec8/1ef8/1fb8`, **c7880 args now guard-band slots `0x143de2b/c`** (first),
      **3 NEW atexit labels `0x142f0b3b0/3e0/3f0`** (17 labels).
    - **Z78 `0x140272d40`–`0x140275350+`: registration block (22 regs: 12 × 253-B, 8 × 242-B,
      2 × 263-B) + 5 `{id,hash}` records + mixed builders.** Outputs in SIXTH band
      `0x143de2xxx`–`0x143de6xxx`; buffers `0x1438d0044`–`0x1438d0d04` (ciphertext crosses
      `0x1438d00000`); **242-B = new shape** (arg17/18 = 0, arg10 = container helper
      `FUN_140548d00`, f7b210+container-triple at 11–14; sizes 0x10 ×6/0x18/0x40);
      **first align-4 reg ever `FUN_140273ff0`** (align 8 ×899, align 4 ×1 cumulative);
      **new size outlier 0xd8** (`FUN_1402741f0`); tokens 2 nonzero / 20 zero
      (`0x3a24f546e9d16e40`, `0xd762317b5bb92e97`, both 263-B with `&LAB_` arg pairs);
      arg10/arg17 runs restart in NEW band `FUN_141212500`–`FUN_14121a5a0` (+ `&LAB_141215aa0`–
      `14121a480`), 11/12 253-B regs carry raw `0x140f7b210` at arg11 (**438 at the time;
      726 textual occurrences overall**);
      `FUN_140272d40` has raw arg12 **`0x1410e8010`** (second raw arg12 after fd9670).
    - **5 `{id,hash}` records** (44 at the time; **50/50 overall**): ids **0x83/0x4a** (178-B, third field 0) and
      **0x3a/0x49/0x91** (169-B); hashes `0x88a321f1`, `0xd3b71231`, `0x4d28219d`,
      `0x1b872806` ×2 — **first many-to-one (0x49+0x91 → same hash)**; storage
      `0x143de2fe0`–`0x143de4158`.
    - **2 × 507-B sorted-insert** (29 at the time; **74 overall**, all 2-record; recipe #7 {`FUN_1421c72e0()` ×2}
      reused by `FUN_140272f00` — new root `&DAT_143ce2090`, src = reg output `0x143de2e50`;
      **recipe #8 {`FUN_1421c63b0()` + `FUN_1421c76c0()`}** in rootless `FUN_140274b90`, src =
      reg output `0x143de45f0`). **479-B two-buffer builder ×1** (`FUN_140273b40`): rootless,
      src = reg output `0x143de30f0`, **helper #25 `FUN_141212ed0(8,&buf,0,0x4d28219d)` — first
      size-8 helper; hash `0x4d28219d` triples as registration hash (FUN_1402732c0) + record hash
      (id 0x3a) + helper hash**. **231-B wrapper ×1** (`FUN_140273a00`) rooted on reg output
      `0x143de3670` — the rootless ladder (231/365/377/479/507-B) is entirely fed by Z78
      registration outputs.

18. **Pass 14** `0x140275450`–`0x140298b11` — zones Z79–Z86 (full record:
    `pass14_0x140275450-0x140298b11.md`). Highlights:
    - **465 fns, Σ `size=` 129,912; size census: 253 ×196, 241 ×85, 263 ×82, 507 ×20, 373 ×17,
      558 ×10, 178 ×10, 231 ×9, 169 ×6, 397 ×6, 472 ×4, 242 ×4, 369 ×3, 389/257/270 ×2,
      512/515/523/542/574/244/252 ×1.** Call targets: `cd360` ×287, `FUN_1426c3bcc` ×380,
      `c2d70` ×162, `d4fb0` ×185, `d4f30` ×77, `d4f70` ×13, `c2d50` ×16, `c7880` ×12 (one 2-arg),
      `atexit` ×12, canary ×67, `FUN_140f80f80` **×0**, warnings 8,058.
    - **Seven registration blocks (287 regs, 287 distinct hashes)** sweeping outputs
      `0x143de6b80`→`0x143e107d0` continuously: A 0108 (48), B 0109 (27), C 0110 (24), D 0111 (36),
      E 0112 (30), F 0113 (38, uniform `&DAT_141197ec0` set), G 0114 (84, token
      `0x9825b6271dce1d31` ×29). Firsts: flags 1/3, align-0x10 ×2, 270-B shape, token exception
      (×29 across two pointer sets), size outliers to `0x1e8`.
    - **16 `{id,hash}` records 16/16** (cumulative 66/66): ids `0x10`–`0x15b`; 4 ids →
      `0xce1a4d26`; first nonzero third fields (`0xa3c35f6d`; `0x79a00d3a` = another reg's hash).
    - **Builders:** 23 sorted-insert (97 cumulative; 512/515/523-B new; 515-B dual-decryptor;
      name pairs {`0x15be7741`,`0xf29e4f35`} / {`0x909ee308`,`0xa321ebe9`} ×5 each), 7×373-B run
      on one name `0x45a7a69c` + one root, helpers 25→28 (first call sites
      `FUN_140f81de0`/`FUN_140f94900`/`FUN_1410f5b30`; helpers size-flexible), allocators switch
      to 14 per-block one-arg pre-steps.
    - **Nested-atexit ×12 (150 cumulative):** 542-B and 574-B row-count variants, first rootless
      558-B, first 2-arg `c7880`; labels 17→29 (band `0x142f0ad80`–`0x142f0bf10`); six-plus
      initializer families; far payloads `0x143f3xxxx`, `0x143e3xxxx`, `0x143e1xxxx`.
    - **Roots: static-root era over** — all roots are registration outputs (`&DAT_143de6b80`
      mega-root ≥15; `&DAT_143e00ac0`/`0x143e00c20` root 24 wrappers) or far bands (`0x143eb6xxx`
      CompilerIDFilter payloads, `0x143ecee70`, `0x143ee0cd0`). **`FUN_140298920` (244-B wrapper)
      stores `&PTR_s_CompilerIDFilter_1438d9ff0` into a registration row — the registry's first
      named consumer.**

19. **Pass 15** `0x140298b20`–`0x1402c16e0` — zones Z87–Z99 (full record:
    `pass15_0x140298b20-0x1402c16e0.md`). Highlights:
    - **510 fns, Σ `size=` 143,192; construct census: 253 ×221, 263 ×113, 241 ×54, 373 ×30,
      397 ×16, 231 ×10, 523 ×8, 472 ×8, 558 ×6, 169 ×5, 267 ×5, 389 ×5, 257 ×5, 178 ×4, 242 ×4,
      507 ×3, 244 ×3, 252 ×3, 515 ×2, 524 ×2, 369 ×2, 471 ×1 (all 510 = 351 regs + 67 wrappers +
      62 builders + 15 sorted-insert + 6 nested-atexit + 9 records).**
    - **Block H (184 regs, two phases: 0x500–0x1150 sizes on 4-point advancing families, then
      uniform small-size regs on `&LAB_14129b770` + raw arg12 `0x1412a93a0` + container pair);
      block I (114 regs, `&DAT_1412c1d00`+`DAT_1412c7860` family, sizes 0xb0–200); block J (46
      regs: flags=1 ×9 pass-wide, FIRST flags=10, align-0x10 ×8, size-8 ×~10, `&SUB_` arg17s);
      block K (≥7 regs, open into `0124`, raw arg11 `&DAT_141308990`).**
    - **Builders fill registration rows in place: root at +0x20, instance ptr at +0x28, flag at
      +0x98 — the registered row IS the object header.** Mega-roots all reg outputs:
      `&DAT_143e1af40`, `&DAT_143e185e0`, `&DAT_143e12980`, `&DAT_143e32f90`, `&DAT_143e45cb0`,
      `&DAT_143e3a780` ×9 wrappers.
    - **`0x3faff222` ×~21 builders (biggest single-name run) + `0x7dd813e` ×6 + `0x64f87f5e` ×8
      `d4f70` + `0x619c597` across 3 shapes/both decryptors + `0x73bb2f3a` triple-role
      (reg hash of the flags-10 reg + record hash id 0x3 + helper hash).**
    - **Nested-atexit ×6: 3 new initializer families (14314a698, 14315bb50, 14314f9b8), 6 new
      atexit labels (band → `0x142f0cab0`), shutdown rows moved to `0x143e2b–0x143e42`, 2-arg
      `c7880` again, far payload `&DAT_143fa8040`.**
    - **3 × 244-B CompilerIDFilter wrappers write 3 new `PTR_s_CompilerIDFilter_*`
      (`1438de790/dd4b8/de9d0`) into reg rows, rooted on `&DAT_143eb6aa0`/`&DAT_143eb67e0`.**
    - 9 `{id,hash}` records 8/9; ids `0x3`(new min)/`0x35`/`0x52`/`0x60`/`0x6c`/`0x74`/`0xa0`/
      `0xb8`/`0x122`; storage `0x143e11548`, `0x143e2b570`–`0x143e2ba40`, `0x143e42b30`–
      `0x143e44970`. Helpers 28 → ≥34; allocators 25 sites (8–0x500); `FUN_140f80f80` ×0;
      warnings 7,522; gaps `0x140298fd9`–`0x14029a6e0`, `0x1402bf899`–`0x1402c10c0`.

### Cross-cutting conventions (cumulative)

| convention | evidence | first seen |
|---|---|---|
| TLS init guard | `*(int *)(TLS + 0x50) < epoch` → `FUN_1426c3bcc(&epoch)` → … / `_Init_thread_footer` | pass 1 |
| 181-B descriptor | `{+0x20=1 or 2, +0x40=ctor, +0x48=vtable-or-FUN, +0x50=third field, +0x58=payload, +0x68=shared ptr}` | pass 1 |
| XOR-40 decryptor | 8-byte key, 24-bit length, `FUN_141c47cc0` or `func_0x1421cd360` | pass 1 |
| XOR-8 decryptor | 8-byte key, 24-bit length, `func_0x1421d4f30/d4f70(&out,&buf,hash,0)`; **pass 12: `d4f70` ↔ 397-B EXACT (118/118) and `d4f30` ×9 = 558×4 + 373×3 + 389×2 in a pass with zero two-buffer helpers — the passes 10–11 deviations were entirely two-buffer builders; `0xde3c867c` is the first hash seen through both decryptors; pass 13: exact again (397-B 61/61 + 377-B/479-B on d4f70; `d4f30` ×18 = 558×3+507×4+373×6+365×3+374/389×2), second cross-shape hash `0x7dd813e` (d4f30 ×3 + d4f70 ×1); **cumulative over the 124 read chunks: 397-B ×636, `d4f70` 690 calls, `d4f30` 626 — pass 15: `d4f70` ×22 = 397×16 + 515×2 + 524×2 + 558×2; `d4f30` ×76 = 373×30 + 523×16calls + 472×8 + 507×6calls + 558×4 + 389×5 + 369×2 + 515×2 + 524×2 + 471×1; names `0x64f87f5e` ×8 `d4f70`, `0x3faff222` ×23 `d4f30`, `0x619c597` across both decryptors and three shapes** | `0x1400fbf70` |
| `{id,hash}` table entry | two TLS guards, `func_0x1421c2d50(&dst,&src)`; **75 static records through pass 15, 74/75 hashes equal a registration hash** (`0x3fd91271`, id `0x35`, matched nothing in `0116`–`0123` — first exception; ids now **3**–0x18d) (pass 2: 6, pass 3: 14, pass 4: 1, pass 5: 15, pass 6: 7, pass 7: 2, pass 13: 5, pass 14: 16); ids **6–0x18d**; FIRST many-to-one: ids 0x49+0x91 share hash `0x1b872806` = registration hash of `FUN_1402734d0`; storage `0x143c39f28`–`0x143de4158`; **pass 14: +16 → 66/66, ids `0x10`–`0x15b` (within the known span), many-to-one strengthened to FOUR ids (`0x8f`/`0x12b`/`0xd`/`0x8e`) → `0xce1a4d26` (= reg hash of `FUN_1402881d0`), and FIRST nonzero third fields — `0xa3c35f6d` (`FUN_140275450`) and `0x79a00d3a` (`FUN_140281230` = hash of `FUN_140281130`, i.e. a record binding TWO registrations); storage now extends to `0x143dfd9xx`** | `0x1400fbeb0` |
| Builder | two guards + `func_0x1421c2d70` + decrypt + `func_0x1421d4fb0` + store ptr/flag | `0x1400fbf70` |
| Sorted registry | insertion sort of 56-B records keyed by `uint` at `+8`; **74 cumulative through pass 13 (97 through pass 14: 507-B ×75 + 523-B ×15 + 524-B ×5 + 512-B ×1 + 515-B ×1), all exactly 2 records; 8 pre-step recipes known (allocator trio; 2 fixed calls; allocator+fixed; 2×`FUN_1421c7220()`; `FUN_140f80f80(0x10)`+`FUN_1421c7780()`; `FUN_140f80f80(0x20 or 0x10)`+`FUN_1421c6920()`; `FUN_1421c72e0()`+`FUN_1421c76c0()`; pass 13 adds `FUN_1421c63b0()`+`FUN_1421c76c0()` — both no-allocator; pass-13 builders consume registration outputs directly and one is rootless; **pass 14: +23 → 97 (507-B ×75, 523-B ×15, 524-B ×5, NEW 512-B ×1, NEW 515-B ×1), all 2-record; the 515-B is the FIRST dual-decryptor sorted-insert (`d4f30` + `d4f70`); its name pairs repeat across containers ({`0x15be7741`,`0xf29e4f35`} ×5, {`0x909ee308`,`0xa321ebe9`} ×5)** | `0x1400ff280` |
| Stack canary in builders | `_DAT_143ac5f40 ^ stack` → `FUN_1426c3d40` | `0x1400fbf70` |
| Nested atexit guard | extra guards set a `PTR_FUN`/`LAB_142f0…` pair, call `atexit` and `func_0x1421c7880`; **passes 8–10: 9 more, writing a shared pointer table spanning `0x1438c6c68`–`0x1438c7020` (rows now interleaved, scattered slots) with `PTR_PTR … = &PTR_FUN_14314b5b0` (×11 cumulative, carried not called); atexit labels `LAB_142f0ada0/adb0/add0/ade0` + new `ad80/ae00/ae10/ae20/ae60` — band `0x142f0ad80`–`0x142f0ae60`; pass 11: 1 more (`FUN_14024e5d0`) with a NEW row kind — `&PTR_FUN_14315fba0` initializer + payload `&DAT_143eeb240` at `0x143db0208/0230` and a NEW atexit label `LAB_142f0b450` outside the old band; pass 12: +4 all with `PTR_FUN_14314b5b0` (×15 cumulative), payloads all `0x143dbxxxx` slots, rows at `0x1438cfd50`–`0x1438cff88`, NEW atexit labels `0x142f0b360/390/400/410` — label set now `0x142f0ad80`–`0x142f0ae60` + `0x142f0b360/390/400/410/450` (14 labels)**; pass 13: +3 (`FUN_1402627e0`, `FUN_140272360`, `FUN_140272690`) all `PTR_FUN_14314b5b0` (**×18 cumulative**), rows `0x1438cfed0`–`0x1438cffc0`, payloads `0x143db1ec8/1ef8/1fb8`, c7880 args = guard-band slots `0x143de2b/c` (first), **NEW labels `0x142f0b3b0/3e0/3f0` — set now 17 labels**, and `FUN_140272690` takes a dynamic root `&DAT_143dc6920` (= 241-B wrapper `FUN_140272590`'s output slot, 2nd dynamic-root member); **pass 14: +12 → 150 — 10 × 558-B + NEW 542-B one-row variant (`FUN_140285700`) + NEW 574-B three-row variant (`FUN_14028a570`) + first rootless 558-B (`FUN_14028ad00`); atexit labels 29 → **35** (band `0x142f0ad80`–`0x142f0cab0`; pass 15 adds `0x142f0c070/c430/c6f0/c980/caa0/cab0`); initializer families now 11 — pass 15 adds `14314a698` ×2, `14315bb50`, `14314f9b8` — `143149258` ×4, `14314a748`, `1431be9f0`, `14315fba0`, `14314a5e8`, `14314bae8` + `PTR_LAB_14314bb98`, `143167258`; 2-arg `c7880` again (`FUN_1402ad130`, pass 15 — ×2 total); pass 15 far payload `&DAT_143fa8040`; pass-15 payloads are 5/6 reg outputs; **the shutdown table rows MOVED to `0x143e2b–0x143e42` (pass 15) — the old `0x1438c6c68`–`0x1438cffc0` table is no longer written**; roots are registration outputs** | `0x1401003f0` |
| Decompilation limit | ~40–55 "Removing unreachable block (ram,0x1421cd…)" warnings per builder; pass 10: 11,672/235 ≈ 50; pass 12: 11,625/226 ≈ 51.4; pass 13: 11,907/258 ≈ 46.2; pass 14: 8,058/465 = 17.3 per fn overall; pass 15: 7,522/510 = 14.8 per fn overall, ≈47.6 per builder/wrapper (158 non-reg, non-record fns) | `0x1400fbf70` |
| Two-buffer builder | helper `(size,&buf,0,hash)` decrypt before the inline XOR-8 decrypt; **25 helpers through pass 13, 28 through pass 14** (pass 11 adds 11, all `(0x20,&buf,0,hash)`, defined in `0x140f9xxxx`–`0x1411c7xxx`; pass 13 adds `FUN_141212ed0(8,&buf,0,0x4d28219d)` — first size-8, in the 0x14121xxxx band; **pass 15: ≥34 helpers — first observed call sites `FUN_140f7b6f0(0x18,…,0xb792564)`, `FUN_140fa4e60(0x30,…,0x9cadf2ec)`, `FUN_140fb3a90(0x30,…,0x92389e46)`, `FUN_14126ec90(0x30,…,0xc6a37088)` ×2, `FUN_140f94810(8,…,0x73bb2f3a)`, `FUN_1411c7840(8,…,0x1b872806)`; new sizes for known helpers (`FUN_140f81de0` 0x30 AND 0x90); helpers remain size-flexible** | `0x14010c120` |
| Shared registry hash | one hash shared across shapes: **`0x7e82c4d1`** (registration + two-buffer helper + static record), **`0x7e2a700b`** (397-B builder ×2 + 558-B nested-atexit ×1, pass 9), and **`0x4d28219d` (pass 13: registration hash of `FUN_1402732c0` + `{id,hash}` record id 0x3a + two-buffer helper `FUN_141212ed0`'s decrypt hash — one name, three roles; pass 14: `0x23a59d55`/`0x25274294`/`0x801bc827`/`0x131257cd` multi-shape; **pass 15: `0x619c597` spans 373-B d4f30 + 524-B d4f30 + 558-B d4f70 (three shapes, both decryptors), `0x73bb2f3a` triples as reg hash (flags-10 reg `FUN_1402bcb90`) + record hash (id 0x3) + helper hash (`FUN_140f94810`), and pass-13's reg hash `0x1b872806` decrypts again via helper `FUN_1411c7840`**)** | `0x14010f4f0` |
| Token → category band | one token pairs with a fixed five-pointer set; passes 7–8: 90 nonzero regs / 60 distinct; pass 10: 8 zero-token regs with the fixed triple `0x14064fec0/&LAB_140aa6750/&SUB_14064feb0` at args 12–14; **pass 11: 40 nonzero regs / 23 distinct with heavy reuse across chunk boundaries — `0xc1bcbc118749a288` ×5, `0x395a90533815064c` ×4 (recurring from pass 8), `0xcd762a89f2ca61d7` ×4, `0x71977bedc4df7a42` ×4, 4 ×2, 15 singletons; a shared token always implies the identical five-pointer set; 3 zero-token regs also carry a five-pointer set (first); pass 13: 2 nonzero / 20 zero — both nonzero on 263-B regs (`0x3a24f546e9d16e40`, `0xd762317b5bb92e97`) with `&LAB_` arg pairs, each seen once; pass 14: 85 nonzero / 50 distinct with the first multi-set token `0x9825b6271dce1d31` ×29; **pass 15: 121 nonzero uses / 104 distinct — `0x808844973e17d0fd` ×11 across blocks H/I/J and ≥3 pointer sets (second confirmed multi-set token), `0x9825b6271dce1d31` ×2 again, 7 more ×2 tokens; multi-set tokens are now a pattern, not an exception** | `0x140126f90` |
| Non-zero flags / unusual align | pass 7–10: flag 0 ×878, align 8 ×878 (registrations; pass 10 adds 8); **pass 13: align 8 ×899, flag 0 ×900, and the FIRST align-4 registration `FUN_140273ff0` (size 0x18); pass 14: first nonzero flags 1/3 and align-0x10 ×2; **pass 15: flags 1 ×9, FIRST flags=10 (`FUN_1402bcb90`, size 0x58, token `0x26f82dfb6aa1eaee`), align-0x10 ×8, size-8 regs ×~14 pass-wide — the flag/align axes are now populated** | `0x140112c20` |
| Conditional pre-steps | bare `FUN_1421cxxxx()` calls; **pass 10: 14 fixed pre-steps / 12 distinct pre-step functions in 13 builders (373-B ×11 + sorted-insert ×2): `FUN_1421c7480` ×5 recurring, 6 new single-use (`FUN_141520a50`, `FUN_1414134c0`, `FUN_140f817e0`, `FUN_140f818a0`, `FUN_141530ba0`, `FUN_14132a2b0`), `FUN_1421c7220` ×2, `FUN_1421c7780` ×1; pass 13: 6 new single-use bare pre-steps — `FUN_14154b9a0` ×2, `FUN_1413fb970`, `FUN_14140e210`/`FUN_14140e2d0` (0xC0-stride run), `FUN_1418b7c60` — plus `FUN_141216c60(0)` ×3, the FIRST pre-step carrying an argument (in the 365-B builders), and `FUN_1421c63b0()` (sorted-insert recipe #8); pass 14: bare pre-steps proliferate per block; **pass 15: 15 distinct one-per-builder bare pre-steps `FUN_141247af0`–`FUN_141248930` (new band) on the `0x3faff222` run; `FUN_1412477f0/970/8630/270/330/c70` singles; 373-B ×30 total** | `0x14010c400` |
| **Size-tagged allocator** | `FUN_140fca550(0x288)` (pass 5); **passes 8–10: `FUN_140f80f80` ×320 cumulative (pass 10: 0x10 ×62, 0x20 ×16, 0x30 ×1, 8 ×2 — first size-8); `FUN_14114df10(0x10)` ×5 exclusive to 389-B; 523-B trio `FUN_14114de40(0x10)`+`FUN_14114dca0/dd70(0x1f0)`; pass 10 new `FUN_140f94220(0x10)` ×8 exclusive to the `0x143d9xxxx` band builders; pass 11: `FUN_1411d3e70(0x20)` ×17 (the Z72 sea's default), `FUN_140f80f80` 0x10 ×8 / 0x20 ×8; pass 12: `FUN_140f80f80` ×118 (0x10 ×77, 0x20 ×41, all 397-B) → ×454 cumulative, plus NEW `FUN_1411dfda0(0x10)` ×1 and `FUN_1411e00c0(0x10)` ×1 — both exclusive to 389-B builders (allocator family in the `0x1411d/e` band now 3 members: `1411d3e70` ×17, `1411dfda0` ×1, `1411e00c0` ×1); pass 13: `FUN_140f80f80` ×62 (0x10 ×54, 0x20 ×7, 8 ×1 — third size-8, in the 377-B) → **×516 cumulative**, `FUN_1411dfda0(0x10)` ×1 again (2nd use, still 389-B-only); **pass 14: `FUN_140f80f80` ×0 — the shared allocator is GONE from the sea; allocator pre-steps are now 14 per-block one-arg functions (28 calls: `FUN_1410fbba0`/`FUN_1410fbc70`, `FUN_14121a070`/`FUN_14121aae0`, `FUN_141227b30/cc0/e60/f30/8000`, `FUN_14122e070`, `FUN_14123fdb0`, `FUN_141244840/4910`, `FUN_1412564e0`/`FUN_1412565b0`) plus `FUN_140f7b550(0x30)` ×3; **pass 15: regime confirmed and spread — `FUN_140f80f80` ×0 again; 25 distinct one-arg sites, sizes 8–0x500 (`FUN_141244840` ×15 reused across blocks with DIFFERENT sizes, `FUN_141270050` ×7, `FUN_14126f690` ×4, `FUN_1412564e0` ×3, `FUN_14123faf0`/`1412b5370`/`1412d9dd0` ×2 each, +`141244910`/`14126ef60`/`14126ff80`/`141270600/0940/0a10`); one allocator per builder-pair, argument = the registered object size** | `0x140123f10` |
| 0x14100xxx callback band | callbacks `FUN_141009xxx`–`FUN_14100bxxx`; **`&DAT_14100e120`/`&DAT_141006710` recur as registration args 13–14 ×13 cumulative (pass 8 sub-family ×5 pairs them with raw arg12 `0x141142890`); pass 14: the family IS a whole block — 38 regs (block F, chunk 0113) all carry `&DAT_141197ec0, 0x141142890, &DAT_14100e120, &DAT_141006710` (45 uses this pass)** | `0x1401251e0` |
| Nested-atexit builder family | 558 B; pass-4 family hash `0xf891229f` base `&DAT_143c834d0`; **passes 8–12 family: hashes `0xe56f0386`/`0x6f93c9ce`/`0x16b04af1`/`0x7e2a700b` + pass 10 `0x7567e07d`/`0x574bbf5a`/`0x124b9839`/`0x96a05257`/`0x1a69e234`, bases `&DAT_143d030a0`/`&DAT_143d03a40`/`&DAT_143d013b0`/`&DAT_143d01a90`, shared `PTR_FUN_14314b5b0` table; pass 11: `0x277a0ae4` base `&DAT_143cfa130` (new `PTR_FUN_14315fba0` row kind); pass 12: 4 more — `0x4ce56bc0` (`&DAT_143d01a90`), `0x7ac92ddc` (`&DAT_143d01930`), `0xc3e03c7f` (**base `&DAT_143dcbd30`, dynamic root**), `0x454d41e3` (`&DAT_143d013b0`); pass 13: 3 more — `0xb1e7fc90` (`&DAT_143d013b0`), `0x7dd813e` ×2 (`&DAT_143d04cf0` and **dynamic root `&DAT_143dc6920`** = wrapper `FUN_140272590`'s output slot); **pass 14: 12 more — all on registration-output roots (`&DAT_143de6b80`, `&DAT_143df7bc0`, `&DAT_143dfe150`, `&DAT_143df8640`, `&DAT_143e0eda0`, …), far payload slots `0x143e12c40/138a0`, `0x143e3c1b0/c310`, `0x143f372b0/381e0`, new hashes incl. `0x4ff98d41`, `0x431fa158`, `0x801bc827`, `0xd4575583`, `0xe7dd13a4`; the CompilerIDFilter payload band now doubles as class roots** | `0x140145400` |
| Builder base-pointer families | pass 7 wrapper-only base `&DAT_143d13560` (123 fns, 0x100 stride); **passes 8–12 recurring class roots now 18 + far: `0x143cfa130`, `0x143cfc6a0`, `0x143cfe0d0`, `0x143d013b0` (pass-10 mega-run ×131), `0x143d01930`, `0x143d01a90`, `0x143d02c80`, `0x143d030a0`, `0x143d03620`, `0x143d03780` (pass-12 top ×49), `0x143d03a40`, `0x143d04970`, `0x143d04cf0`, `0x143d06950`, `0x143d087a0`, `0x143d30560`, `0x143d70e30` + far `0x143f8e270` (pass 12 ×20 — now a top-6 root), `0x143f93cd0` (new far root, pass 12), `0x143d93520`/`0x143d937e0`; pass 12 singles: `0x143d02700`, `0x143d02de0`, `0x143d03bb0`, `0x143d30820` (recurs from pass 10); wrappers are irregular-stride multi-base; pass 13: `0x143d013b0` ×156 top again, `0x143d03780` ×10, far `0x143f8e270` ×7 (5 wrappers + 2 builders), `0x143d04130` ×3 now recurring, `0x143d03bb0`/`0x143d03d10` ×3/×5 now recurring, NEW roots `0x143d03fd0` and **`0x143ce2090` (first class root below 0x143cf0000)**, dynamic `0x143dd2600`/`0x143dc6920`** | `0x140136b60` |
| Registration callback bands | shapes per band; passes 7–8: 878 registrations in one shape (253/263 B) with parallel index bands; **pass 10: 8 more, uniform size 0x20, arg10/arg17 runs extended into new band `0x1411c7060`–`0x1411c73a0`; pass 13: 22 regs in THREE shapes — 253-B (12), 263-B (2, nonzero token), NEW 242-B (8: arg17/18 = 0, arg10 = container helper `FUN_140548d00`, container triple at args 11–14); arg10/17 band restarts at `0x14121xxxx` (`FUN_141212500`–`FUN_14121a5a0`); pass 14: 287 regs in seven blocks; **pass 15: 351 regs in FOUR blocks (H 184, I 114, J 46, K ≥7) across shapes 253 ×221, 263 ×113, 267 ×5, 257 ×5, 242 ×4, 252 ×3; arg10 band `FUN_14129d870`→`FUN_1412c47a0`→`FUN_1412cc200`→`FUN_1412db220`–`FUN_1412dbb80`→`FUN_14130e3f0`–`FUN_14130e4f0` (345 distinct, lock-step per block); arg17 `&LAB_1412a15d0`→`&LAB_1412c2c60`–`c4780`→`&LAB_1412dade0`–`db1f0` (first `&SUB_1412d2490`/`&SUB_1412d4350` arg17s); 242-B regs carry arg10 = container helper `FUN_140548d00`** | `0x14012c830` |
| Two-guard copy wrapper | 241/231 B; guard1 `c2d70(&dst,&src)`, guard2 `d4fb0`; no decrypt; store ptr + 0; pass 7: +123 (single base, 0x100 stride); **passes 8–10: +217 multi-base irregular-stride (pass 10: 241 ×119 + 231 ×2); pass 11: +24 all 241-B at 0x100 stride (16 inside the Z72 sea, 8 in the Z75 tail with c2d70 sources in the new `0x143db` band); the 231-B variant has NO class-root store (first line `_DAT_x = 0`) and pairs with a "local-base" builder; pass 12: +99 all 241-B, multi-base irregular, c2d70 sources all one-off `0x143db/c/d` slots (each source used exactly once); pass 13: +151 all 241-B (majority shape again, 58 %) + 1 × 231-B, roots re-diversified (13 static + 1 far), and MEASURED: c2d70 src = root-slot − 0x20 in 152/153 cases — one object row per wrapper; the single exception `FUN_14026b680` copies into far temp `0x143dac4d8`; pass 14: +85 × 241-B + 9 × 231-B + FIRST 244-B; **pass 15: +54 × 241-B + 10 × 231-B + 3 × 244-B (`FUN_1402ac690/990/a90` — three NEW `PTR_s_CompilerIDFilter_*` into reg rows, roots `&DAT_143eb6aa0`/`&DAT_143eb67e0`); roots cluster on same-block reg outputs (`&DAT_143e3a780` ×9, `&DAT_143e33250` ×4, `&DAT_143e358f0` ×4, `&DAT_143e33bf0` ×3)** | `0x14015f9a0` |
| Pre-step builder | 369/373/377/389/397/472/475/480-B variants; **passes 8–10: 397-B (allocator pre-step, `d4f70`); 373-B (fixed-call pre-step, `d4f30`); 389-B = `FUN_14114df10`+`d4f30`+hash `0x539f7774`; pass 10: 373-B ×11 with 9 distinct pre-step functions; pass 11: 475/472/480-B two-buffer builders dominate (47 + 475-B), pre-steps = one of 24 helpers or allocator `FUN_1411d3e70(0x20)`; 8 new bare fixed pre-steps incl. the `FUN_14190dbc0/dc80/dd40` run; pass 12: 373-B ×3 with 3 NEW single-use pre-steps (`FUN_14190de00` extending the `0x14190xxxx` run, `FUN_1421c6860`, `FUN_14158bcf0`), 389-B ×2 with NEW allocators `FUN_1411dfda0`/`FUN_1411e00c0` + `d4f30` (hashes `0x9e30262e`/`0x2f709539`), 397-B ×118 all allocator pre-steps; pass 13: 397-B ×61 all allocator pre-steps, 373-B ×6 with 6 NEW single-use pre-steps, **365-B = rootless 373-B-minus-root ×3 (pre-step `FUN_141216c60(0)`, first pre-step with an argument)**, **374-B = 373-B with 2-arg c2d70 ×1**, **377-B = 397-B minus root store ×1 (alloc 8)**, **479-B = two-buffer builder rootless ×1 (helper `FUN_141212ed0`, size 8)**, 389-B ×1 reuses `FUN_1411dfda0`+`0x9e30262e` recipe; pass 14: per-block allocators + 7-builder run; **pass 15: 397-B ×16 (roots now reg outputs incl. small size-8/0x10 rows), 373-B ×30 (two single-name runs: `0x3faff222` ×21 on `&DAT_143e185e0`, `0x7dd813e` ×4 on `&DAT_143e12980`), 369-B rootless ×2 (fed by reg outputs), 472-B ×8 two-buffer (helpers incl. `FUN_140f7b6f0`/`fa4e60`/`fb3a90`/`14126ec90`), 471-B ×1 (`FUN_1402bed50`, helper `FUN_140f94810(8)`, hash `0x73bb2f3a`), 389-B ×5 (allocators `FUN_141270600(0x500)`/`141270050(8)`/`1412b5370(0xb0)`/`1412d9dd0(8)`/`14123faf0(0x30)`)** | `0x14015faa0` |
| Two-decrypt sorted-insert builder | 507/523/524/512/515 B; 2 pre-steps + 2 decrypts + 2-record insertion sort over 56-B records; **97 cumulative through pass 14, **112 through pass 15** (507-B ×78, 523-B ×23, 524-B ×7, 512-B ×1, 515-B ×3), all 2-record; pass 15: 4 dual-decryptor incl. FIRST `d4f70`-first 524-B (`0xdc1aee1b`+`0x44150fbd`), roots are reg outputs (`&DAT_143e1af40` ×6 in one chunk), allocators sized to the registered objects (0x500/0x538/0x540/0x568/0xb0/0xf0); pass 10 adds recipes {2 × `FUN_1421c7220()`} and {`FUN_140f80f80(0x10)` + `FUN_1421c7780()`}; pass 13: +2 both consuming registration outputs (root `&DAT_143ce2090` on `FUN_140272f00` reusing recipe {`FUN_1421c72e0()` ×2}; rootless `FUN_140274b90` with NEW recipe #8 {`FUN_1421c63b0()`+`FUN_1421c76c0()`}); pass 14: 97 cumulative, first dual-decryptor 515-B; **pass 15: +15 → 112 (523 ×8, 507 ×3, 515 ×2, 524 ×2); 4 dual-decryptor (515-B `0x210de6cb`+`0x64f87f5e`, `0xb48f1d22`+`0x801bc827`; 524-B `0xdc1aee1b` d4f70-FIRST + `0x44150fbd`, `0x9102d364`+`0x619c597`); one 523-B reuses allocator `FUN_1412d9dd0(8)` with the 389-B (`0x33e51fdc` ×2)** | `0x14015fc20` |
| `{id,hash}` static-record builder | 169/178 B; +2 in pass 7 (ids 0x187/0x188) | `0x140166880` |
| **arg17 FUN-run** | registration arg17 is a contiguous fixed-stride FUN run parallel to registration order; **passes 7–10: `FUN_1411a31e0`–`FUN_1411ad3c0` (pass 7–8) + `FUN_1411c7060`–`FUN_1411c71b0` (pass 10, stride 0x30, 8 entries); pass 11: extended to `FUN_1411d7f10`–`&LAB_141203d50` (673 entries, stride 0x30 ×661), ends with two `&LAB_` labels (`141203d40/141203d50`); arg17 band precedes arg10 band in both; pass 13: NEW band `0x14121xxxx` — `FUN_1412124d0` + `&LAB_141215aa0/ab0/ad0/b00/b30/b50` + `&LAB_1412187c0` + `&LAB_14121a3e0/400/420/440/460/480`; the 242-B regs have arg17 = 0; **pass 14: band extends to `FUN_1412254f0`–`FUN_141268980` (arg10, 283 distinct) / `&LAB_141224be0`–`FUN_1412689d0` (arg17)** | `0x14017ce10` |
| **Five-pointer registration set** | args 10–14 pointers; **pass 10: arg10 run continues into new band `FUN_1411c71e0`–`FUN_1411c73a0` (stride 0x40); zero-token regs here carry the fixed triple at args 12–14 instead of the pass-6–8 five-pointer sets; pass 11: arg10 `FUN_1411d9c60`–`FUN_14120a3d0` (stride 0x30 ×449 / 0x40 ×213); arg10 is now always a FUN_ (fd9670 quad moved to args 11–14: ×445; `DAT_141197ec0`-family ×145; `0x140f7b210`+container-triple ×40; pass 13: arg10 = `FUN_140548d00` (a container helper) on all 8 × 242-B regs — first non-callback arg10; 19/22 regs carry raw `0x140f7b210` at arg11 (**726 textual occurrences measured over all 108 chunks; the old 438 counted only passes 5–13**); `FUN_140272d40` carries raw arg12 `0x1410e8010` (2nd raw arg12 after fd9670); pass 14: arg11 census raw f7b210 ×144; **pass 15 arg11 census over 351 regs: raw `0x140f7b210` ×115, `&LAB_14129b770` ×81 (block-H small phase), `&DAT_1412c1d00` ×41 (block I), `&DAT_14129b3d0` ×32 + `&DAT_14129b630` ×31 (block-H large phase), raw `0x140fd9670` ×13, advancing pairs `1412c1c40/1412c1c80` ×5 each, raw arg12 `0x1412a93a0` ×~112, raw arg11 `&DAT_141308990` (block K)** | `0x140179e10` |
| **Parallel index bands** | arg10/11/12/13/14/17 all advance in lock-step with registration address order (886 + 673 regs) — one entry per registration, no gaps, no reorders across the pass-7/8, pass-8/10 and pass-10/11 boundaries; **pass 13: lock-step again over 22 regs in the new `0x14121xxxx` band; the `0x141203d50`→`0x141212500` span is unread chunks ~`0919`–`0928`, not a gap; pass 14: lock-step over 287 regs; **pass 15: lock-step per block over 351 regs — arg10 `FUN_14129d870`…`FUN_14130e4f0` (345 distinct; `FUN_140548d00` container-helper arg10 on 242-B regs), arg17 in `&LAB_`/FUN_/`&SUB_` mix; the `0x14121a5a0`→`0x1412254f0` and `0x141268980`→`0x1412c47a0` spans are unread corpus (chunks ≈`0929`–`0956`), now partially consumed by this pass's bands** | `0x1401abad0` |
| **FUN_/DAT_ label ambiguity** | same addresses appear as `FUN_…`/`&DAT_…`/`&LAB_…` across args 12/13/14/17 (pass 8 rows) | `0x1401b9660` |
| **Decrypt-hash reuse regime** | builder sea reuses hashes heavily (top `0xa83c2c26` ×125+ cumulative; pass 8: 53 distinct/104 uses, pass 9: 41/166, pass 10: 49/108, pass 11: 49/71 with top `0xe2bf1226` ×5 and shared `0x3b171026`/`0xc3e03c7f` across different bases — per-pass distinct sets overlap, do not add; **pass 12: 55 distinct / 127 uses with two dominant names `0x37ab13d3` ×24 (contiguous 0094–0095 run) and `0xf5087894` ×21 (0098–0099 run); the pass-8/9 dominant `0xa83c2c26` is down to ×4 — the name pool rotates as the sea advances**; **pass 13: 39 distinct / 81 uses — NEW dominant `0x8f80faa` ×15 and `0x861c6fe6` ×8 (8-builder run in chunk 0104), `0x37ab13d3` ×6 continuing; `0xa83c2c26` down to ×1**) — opposite of the registration blocks' zero-reuse regime (pass 11: 40 nonzero tokens / 23 distinct with heavy reuse — the token regime now ALSO reuses; a hash is a name, not an instance id); pass 14: `0x45a7a69c` ×7; **pass 15: 41 distinct `d4f30` / 14 distinct `d4f70` / ~30 uses per run — `0x3faff222` ×23 (largest run), `0x7dd813e` ×6, `0x64f87f5e` ×8, `0xe1d625b8` ×4, `0xb48f1d22`/`0xf97609c8`/`0x267b9b97`/`0x619c597`/`0x33e51fdc`/`0xc1d43c` ×2; name pools rotate as the sea advances** | `0x1401e26f0` |
| **Class-base pointer band** | first line of every builder/wrapper stores one of the recurring `&DAT_` class roots; per-instance result stores are one-off `&DAT_0x143d2xxx`–`0x143d9xxx` slots; **pass 10: the mega-root `&DAT_143d013b0` ×131 in one run; 231-B wrappers have no root store; pass 11: new dominant root `&DAT_143d93520` ×51 — a Z71 registration output, i.e. a runtime-built class object; local-base regime now majority; new root `&DAT_143d04130`; Z75 wrapper c2d70 sources = `0x143dbxxxx` outputs; pass 12: no single mega-root — usage spread across the recurring set with `&DAT_143d03780` ×49 top; far roots `&DAT_143f8e270` ×20 / `&DAT_143f93cd0` ×1 (the `0x143f9xxxx` band is now provably a class-root band); dynamic roots `&DAT_143dc8fb0` ×4 / `&DAT_143dcbd30` ×3 / `&DAT_143db8170` ×2 / `&DAT_143dde5b0` ×1, all in the registration-output bands; **pass 13: `&DAT_143d013b0` ×156 top again; far `&DAT_143f8e270` ×7; `&DAT_143d04130` ×3 now recurring; NEW roots `&DAT_143d03fd0` + `&DAT_143ce2090` (first below 0x143cf0000); dynamic `&DAT_143dd2600` (373-B) / `&DAT_143dc6920` (558-B nested-atexit); result stores now also land in the `0x143de` registration band; pass 14: STATIC ROOTS ABSENT; **pass 15: static roots absent AGAIN — every root is a registration output; mega-roots `&DAT_143e1af40` (≥12), `&DAT_143e185e0` (≥21, the `0x3faff222` run), `&DAT_143e12980` (≥8), `&DAT_143e32f90` (≥8), `&DAT_143e45cb0` (≥7), `&DAT_143e3a780` (×9 wrappers), `&DAT_143e33250`/`33bf0`/`358f0`/`13cd0`/`38a90` ×3–4 each; MEASURED builder→row fill: class root at reg-row+0x20, instance ptr at +0x28, flag at +0x98 — the registered row IS the object header; result stores sweep `0x143e0f480`–`0x143e49090`; wrapper roots can forward-reference outputs written later in the same chunk (`FUN_140298e30` → `0x143e21c30` written by `FUN_1402a5100`)** | `0x1401d2660` |
| **Local-base pair** (pass 10) | a 397-B builder with a one-off local class base (`&DAT_143d3bb60`, `&DAT_143d6ba10`, `&DAT_143d6df50`) is paired with a 231-B/241-B wrapper whose c2d70 src is that same local DAT; the "class" is built at runtime, not a static vtable root. **Pass 11: generalized — the dominant root `&DAT_143d93520` (×51) and the `&DAT_143d94c90/bda0/95370/9a630` roots are all registration outputs; c2d70 sources are registration outputs in 32/43 Z72 uses. Pass 12: the local-base convention now reaches the nested-atexit family — 558-B `FUN_14025f650` is rooted on `&DAT_143dcbd30` and two of its sibling 241-B wrappers share it; other pass-12 local clusters: `&DAT_143dc8fb0` ×4 wrappers, `&DAT_143db8170` ×2, `&DAT_143dde5b0` ×1**; **pass 13: generalized to a rootless-builder ladder — 231-B `FUN_140273a00` (src = reg output `0x143de3670`), 365-B ×3 (src = 242-B reg outputs `0x143de4830/48f0/4530`), 479-B `FUN_140273b40` (src = `0x143de30f0`), 507-B ×2 (src = `0x143de2e50`/`0x143de45f0`), 558-B `FUN_140272690` (root = wrapper `FUN_140272590`'s slot `0x143dc6920`), 373-B `FUN_140264e00` (root = wrapper `FUN_140264d00`'s src slot `0x143dd2600`) — every rootless builder in Z78 is fed by a same-chunk registration or wrapper row; **pass 14: the regime is total — no static roots at all; each block's outputs feed the following builders/wrappers directly (`&DAT_143de6b80` → ≥15 builders; 24 of chunk-0113's wrappers root on two outputs; nested-atexit builders root on outputs too)** | `0x1402133b0` |
| **Registration data bands** | registration outputs land in distinct DAT bands per block: pass 7–8 `0x143d2xxxx`-ish, pass 10: `0x143d90xxx`–`0x143d915xx` (new band, first written this pass), **pass 11: `0x143d9xxxx` ×148 (Z71/Z72), then four new bands `0x143daxxxx` ×8, `0x143dbxxxx` ×162, `0x143dcxxxx` ×186, `0x143ddxxxx` ×169 — five bands total in one pass; arg1 and arg18 both move; pass 13: SIXTH band `0x143de2xxx`–`0x143de6xxx` (22 regs; arg18 slots ~0xA0 below arg1 on the 253-B shape, = 0 on the 242-B shape); ciphertext band crosses `0x1438d00000` (`0x1438d0044`–`0x1438d0d04`); pass 14: continuous sweep `0x143de6b80`–`0x143e107d0`; **pass 15: four blocks sweep `0x143e0f480`–`0x143e5bb40` (arg1 and arg18 both move; outputs interleaved non-monotonically inside each block; ciphertext crosses `0x1438e0000` — band now `0x1438d0b20`–`0x1438e7afc`; `{id,hash}` rows and shutdown rows now interleave with the output bands at `0x143e2b`/`0x143e42`)** | `0x140215530` |

Top call targets across all read chunks: `FUN_1426c3bcc` (TLS init check), `SUB_140551380`
(descriptor third field), `FUN_140548d00`/`FUN_14053a070`/`FUN_140548f80` (container helpers — also
registration arguments), `FUN_1426c3d40` (stack check). Pass-13 additions (over its 8 chunks):
`FUN_1426c3bcc` ×478, `_Init_thread_footer` ×478, canary ×79 (exactly the decrypt carriers),
`c2d70` ×231, `d4fb0` ×233, `d4f70` ×63, `FUN_140f80f80` ×62, `d4f30` ×18, `cd360` ×22,
`c2d50` ×5, `c7880` ×3, `atexit` ×3, new pre-step `FUN_141216c60(0)` ×3, new helper
`FUN_141212ed0` ×1, warnings 11,907. Pass-14 additions (over its 8 chunks): `cd360` ×287,
`FUN_1426c3bcc` ×380, `d4fb0` ×185, `c2d70` ×162, `d4f30` ×77, `d4f70` ×13, `c2d50` ×16,
`c7880` ×12 (one 2-arg), `atexit` ×12, canary ×67, `FUN_140f80f80` ×0 (regime change), new
helpers `FUN_140f94900` ×2 / `FUN_1410f5b30` / `FUN_140f81de0`, new per-block allocators ×28,
warnings 8,058. Pass-15 additions (over its 8 chunks): `cd360` ×351, `FUN_1426c3bcc` ×330,
`d4fb0` ×165, `c2d70` ×150, `d4f30` ×76, `d4f70` ×22, `c2d50` ×9, `c7880` ×6 (one 2-arg),
`atexit` ×6, canary ×83, `FUN_140f80f80` ×0, container helpers as text `FUN_140548d00` ×217 /
`FUN_14053a070` ×210 / `FUN_140548f80` ×115 (mostly registration args), allocators 25 sites,
warnings 7,522.

## Open threads (check/update before every pass)

1. `func_0x1421cd360` body (18 args) — **not obtainable from this corpus**: it is spelled
   `func_0x…`, i.e. no decompiled body exists in any of the 2,228 chunks (verified by header
   scan). Needs the full Ghidra project/EXE. Schema derived from call sites instead: **3,578
   instantiations over all 15 passes, 3,578 distinct hashes** (zero reuse); schema stable except
   pass 13's 242-B shape (arg17/18 = 0), pass 14's 270-B shape (nonzero arg16 `FUN_141232440`),
   pass 15's 267-B shape (flags-1 carrier ×5), one align-4 reg (`FUN_140273ff0`), ten align-0x10
   regs, flags 1 ×11 / **3 ×1 / 10 ×1 (`FUN_1402bcb90` — decode its ciphertext
   `0x1438e452c` first)** and size outliers 0xd8 → **0x1150**.
2. Meaning of the 64-bit arg9 values — **pass 11: heavy reuse; pass 14: first multi-set token
   `0x9825b6271dce1d31` ×29; pass 15: 121 nonzero uses / 104 distinct and a SECOND multi-set
   token — `0x808844973e17d0fd` ×11 across blocks H/I/J and ≥3 pointer sets. Multi-set tokens are
   now a pattern. Next: decrypt one `0x808844973e17d0fd` ciphertext (e.g. `0x1438dea68`,
   `FUN_14029af00`); decompile `FUN_1411dc260` (body at chunk `0917`) and `FUN_14120a760`;
   also the consumers of `0x9825b6271dce1d31`.**
3. Decrypt the XOR-8 buffers to recover registered names; no readable literals exist. Cheapest
   batches: pass 11's 27 two-buffer-helper calls, Z74's `0x1438cd1xx` band incl.
   `s_d____WQ_1438cd11c`, and the still-open `s_JIubLB__1438b8f04`; pass 13's Z78 buffers;
   **pass 15: block J (43 regs, buffers `0x1438e2abxx`–`0x1438e45xx`) — it contains the flags=10
   reg (`FUN_1402bcb90`, buffer `0x1438e452c`) and the id-`0x3` record's registration; then the
   `0x3faff222` run's ~23 builder buffers (`0x1438d…`, root `&DAT_143e185e0`) — one decrypt
   names the biggest single-name family; and record id `0x35`'s unmatched hash `0x3fd91271`.**
4. `+0x48` slot holding `FUN_` code pointers vs `&LAB_` data labels — inspect `FUN_140e955a0` and
   `FUN_140eb2350`. No new evidence in passes 8–10.
5. Pass-1 chunks `0009`–`0013` — **confirmed unread**, not a mere provenance gap: 865 fns,
   `0x140093150`–`0x1400c2ed0`, Σ `size=` 156,518 B, same 181-B descriptor sea. Cheapest close:
   read `chunk_0009`–`chunk_0013` and append five appendices to the pass-1 record.
6. `{id,hash}` consumer — **75 records, 74/75** (pass 2: 6/6; pass 3: 14/14; pass 4: 1/1; pass 5:
   15/15; pass 6: 7/7; pass 7: 2/2; passes 8–12: 0/0; pass 13: 5/5; pass 14: 16/16; pass 15: 9 (8/9 — NEW MINIMUM id `0x3` = the flags-10 reg's hash `0x73bb2f3a`, which also triples as the 471-B helper's decrypt hash; FIRST unmatched hash `0x3fd91271`, id `0x35`) — incl.
   many-to-one ids 0x49+0x91 → `0x1b872806`, now FOUR ids `0x8f`/`0x12b`/`0xd`/`0x8e` →
   `0xce1a4d26`, and the first nonzero third fields: `0xa3c35f6d`, `0x79a00d3a` = another
   registration's hash; ids now **3–0x18d**). Next: `func_0x1421c2d50` has no body
   in the corpus, so search the data corpus for the 75 known `{id,hash[,third]}` triples as one
   table (storage `0x143c39f28`–`0x143e44970`; pass-13 rows at `0x143de2fe0`–`0x143de4158`,
   pass-14 rows at `0x143de66b8`–`0x143dfd9xx`; pass-15 rows `0x143e11548`, `0x143e2b570`–`0x143e2ba40`, `0x143e42b30`–`0x143e44970`); resolve `0x3fd91271` against chunks `0000`–`0115`).
7. Unmatched helper-decrypt hashes: `0x51c522ac`, `0x9e7bf152`, `0x871bd3d0`, `0x7a0b33da` remain;
   helper bodies **do exist** ahead of the cursor — `FUN_140f81de0` chunk `0023`, `FUN_140fb39a0`
   chunk `0031`, `FUN_141142f90` `0894`, `FUN_1411c7cf0` `0915`, `FUN_141212ed0` `0928` — read them
   when the sweep reaches `0x140f8xxxx`–`0x1412xxxx`. The band hosts 24 two-buffer helpers plus
   the allocators (`FUN_140f80f80` ×516 cumulative, `FUN_1411d3e70` ×17, `FUN_140f94220` ×8).
8. Compiler-ID filter: **12 shells total** (pass 3: 3; pass 4: 5; pass 5: 4), 12 distinct
   `PTR_s_CompilerIDFilter_*` labels (`14388ce90/cf68/d010`, `1438926c8/770/848/938/f38`,
   `1438aca20/a68/ab0/b10`) + payloads `DAT_143eb63c0/67e0/6aa0/6940`. **Pass 14 makes the first
   registry→filter link: 244-B wrapper `FUN_140298920` roots on payload `&DAT_143eb67e0` and
   stores `&PTR_s_CompilerIDFilter_1438d9ff0` + flag 1 into a registration row (`0x143e095xx`);
   other builders/wrappers root directly on the payload band; the payloads now double as class
   roots. Decompile `FUN_140298920`'s neighborhood and dump `0x143e09560`–`0x143e095f8` plus
   `0x143eb63c0/67e0/6940/6aa0`.**
9. What is at `LAB_142f08c40`–`LAB_142f0acd0` (the atexit handlers)? **Measured over the read
   range: 149 `atexit` call sites, 146 distinct targets** (the old "~113" was an early estimate).
   The 558-B nested-atexit family contributes the tight `0x142f0ad80`–`0x142f0ae60` +
   `0x142f0b360/390/3b0/3e0/3f0/400/410/450` set (17 labels); the rest form the long runs
   `0x142f08c40`–`0x142f09b90` and `0x142f0a130`–`0x142f0acd0`. Labels only, live outside
   `.text`; pass 12 adds
   `0x142f0b360/390/400/410`; pass 13 adds `0x142f0b3b0/3e0/3f0`; **pass 14 adds
   `0x142f0b620/630/640/7f0/9b0/ae0/af0/b20/b40/c70/f00/f10` — the label set is now 29 labels,
   band `0x142f0ad80`–`0x142f0bf10`**; labels
   only, live outside `.text`; the `0x142f0b3xx` stretch fills densely — looks like a jump table.
   Check when the region enters the corpus.
10. Two-buffer helpers: **28 known** (pass 11 adds 11, all `(0x20,&buf,0,hash)`; pass 13 adds
    `FUN_141212ed0(8,&buf,0,0x4d28219d)` — first size-8; pass 14 gives the first call sites for
    `FUN_140f94900` (sizes 8 and 0x30), `FUN_1410f5b30(8)` and `FUN_140f81de0(0x30)` — helpers
    are size-flexible; see convention row). Bodies are in the
    corpus ahead of the cursor: `FUN_141142f90` chunk `0894`, `FUN_1411c7cf0` `0915`,
    `FUN_141212ed0` `0928`; read them when the sweep reaches that band.
11. `0x140f7b210` — raw code pointer never called in-range; **870 textual occurrences over the 116
    read chunks** (the old "438" counted only passes 5–13; pass 13 +19: 11 of 12 253-B regs + all
    8 242-B regs as arg11; **pass 14 +144**). Still the highest-value single lead — but it is a raw address, so no
    body exists in the corpus. The raw arg12 family grows: `0x141142890` (pass 8; **45 uses in
    pass 14's block F**), `0x1410e8010`
    (`FUN_140272d40`, pass 13).
12. `0x143f93e30` (far data referenced by `FUN_140171a10`) — check the data corpus.
13. The `{id,hash}` static records — find the consumer array indexed by ids 0x4b–0x188 in the data
    corpus.
14. Sorted-insert builders: **97 cumulative instances (507-B ×75 + 523-B ×15 + 524-B ×5 + 512-B
    ×1 + 515-B ×1), all sort exactly 2 records**; pass 10 adds
    recipes {2 × `FUN_1421c7220()`} (`FUN_140209910`, hashes `0xf81f4386`/`0xfbebad6f`) and
    {`FUN_140f80f80(0x10)` + `FUN_1421c7780()`} (`FUN_14020b7a0`, hashes `0x21ed0bc3`/`0x8f4a353d`);
    pass 13 adds {`FUN_1421c72e0()` ×2} reuse (root `&DAT_143ce2090`) and NEW recipe #8
    {`FUN_1421c63b0()`+`FUN_1421c76c0()`} (rootless).
    **Pass 14: first dual-decryptor 515-B (`FUN_1402817f0`, `d4f30` `0x201671c` + `d4f70`
    `0x8c4782e9`), new sizes 512/523, and repeated name pairs across containers
    ({`0x15be7741`,`0xf29e4f35`} ×5, {`0x909ee308`,`0xa321ebe9`} ×5).**
    Are the two 56-B records always a {name, hash} pair of one category? Decrypt the pairs.
15. Pass-6 two unlisted gaps `0x1401828e8`–`0x1401834a0` and `0x140190298`–`0x140191680` — padding or
    non-`FUN_` code? Inspect in the raw Ghidra listing.
16. Pass-6 data pointers `PTR_FUN_14314b5b0` (×2), `PTR_FUN_143149258`, `PTR_FUN_14314a5e8`,
    `PTR_FUN_14314bae8`, `PTR_LAB_14314bb98`, `PTR_FUN_143173ad0` — data-corpus check.
    **Updated (passes 8–13): `PTR_FUN_14314b5b0` gains 3 more uses as `PTR_PTR` initializer inside
    the three pass-13 558-B nested-atexit builders → cumulative ×18; carried, never called. The
    shared table now spans `0x1438c6c68`–`0x1438cffc0` with interleaved rows; pass 13 payloads are
    `&DAT_143db1ec8/1ef8/1fb8` (pass-11 Z74 band) and pass-13 c7880 args are guard-band slots
    `0x143de2b/c` (first time, was data rows); pass 11 added a SECOND initializer
    family: `PTR_FUN_14315fba0` at row `0x143db0208` with payload `&DAT_143eeb240` and atexit label
    `0x142f0b450`. Decompile the targets of both `0x14314b5b0` and `0x14315fba0` and dump the
    table.**
17. Pass-6 far-data bases `&DAT_143fa0780` / `&DAT_143fa0e70` — check the 0x143fa0xxx band. **Pass-9
    far base `&DAT_143f8e270`; pass 10 far-ish bases `&DAT_143d93520`/`&DAT_143d937e0` — check the
    0x143f8xxxx and 0x143d9xxxx bands (the latter is now registration-writable).**
18. Parallel per-registration runs — **confirmed through pass 11** (arg17 `FUN_1411a31e0`–
    `FUN_1411ad3c0` + `FUN_1411c7060`–`FUN_1411c71b0` + `FUN_1411d7f10`–`&LAB_141203d50`;
    arg10 `FUN_1411ad470`–`FUN_1411b8070` + `FUN_1411c71e0`–`FUN_1411c73a0` +
    `FUN_1411d9c60`–`FUN_14120a3d0`; lock-step across the pass-7/8, pass-8/10 and pass-10/11
    boundaries). The `0x1411b8070`→`0x1411c7060` span is **not an unaccounted gap** — it is simply
    unread corpus: those addresses fall in chunks `0907`–`0914` (first headers `0x1411b6c20` …
    `0x1411c43b0`), ahead of the cursor. **Pass 13: lock-step again over 22 regs in a NEW
    band `FUN_141212500`–`FUN_14121a5a0` (arg10) / `&LAB_14121xxxx` (arg17); the
    `0x141203d50`→`0x141212500` span likewise sits in unread chunks ~`0919`–`0928`. Pass 14:
    lock-step over 287 regs — arg10 `FUN_1412254f0`–`FUN_141268980` (283 distinct, 0x30 stride) +
    5 × container-helper arg10s; the `0x14121a5a0`→`0x1412254f0` span sits in unread chunks
    ~`0929`–`0931`.**
19. The 27,854-B unlisted gap `0x1401a4e02`–`0x1401abad0` (pass 7) — inspect the raw Ghidra listing.
    **Pass 11 adds a third gap: `0x140229be7`–`0x14022dcc0` (16,601 B); the Z73 token pair
    (`0x292f8ed1cad53cdb` ×2) sits immediately before it — the gap may hold their shared consumer.**
20. FUN_ vs `&DAT_`/`&LAB_` label alternation — check the listing; if data, arg12 may not be code at
    all in some rows.
21. Registration size outliers: 0x230/0x228 (pass 7), 0x118 (`FUN_1401e2570`, pass 8) — pass 10's
    block is uniform (0x20 ×8), so outliers remain unexplained. **Pass 13 adds 0xd8
    (`FUN_1402741f0`, 253-B) and the first align-4 reg (`FUN_140273ff0`).**
22. **Allocator/decryptor bodies.** `FUN_140f80f80` (×516 cumulative, **×0 in pass 14**),
    `FUN_14114df10` (×5, 389-B), `FUN_140f94220` (×8), `FUN_1411d3e70` (×17), `FUN_1411dfda0`
    (×2), `FUN_1411e00c0` (×1), the 523-B trio `FUN_14114de40`/`dca0`/`dd70`, **and pass 14's 14
    per-block allocators (`FUN_1410fbba0/fbc70`, `FUN_14121a070/aae0`, `FUN_141227b30/cc0/e60/
    f30/8000`, `FUN_14122e070`, `FUN_14123fdb0`, `FUN_141244840/4910`, `FUN_1412564e0/5b0`)**
    all have bodies in the corpus ahead of the
    cursor (`FUN_140f80f80` chunk `0836`, `FUN_140f94220` `0839`, `FUN_14114df10` `0896`,
    `FUN_1411d3e70` `0916`, `FUN_1411dfda0`/`FUN_1411e00c0` `0919`, pass-14's in ≈`0929`–`0955`)
    — read them when the sweep reaches `0x140f8xxxx`–`0x1412xxxx`. **`func_0x1421d4f30`/`d4f70`
    are `func_0x…`: no body in the dump. The d4f70↔397-B correlation held through pass 13
    (614/614 in helper-free stretches) but pass 14 breaks the exclusivity — 558-B ×5 + 574-B ×1 +
    515-B ×1 also use `d4f70`.**
23. **The `0xa83c2c26` mega-hash (×20 pass-10 instances; ×125+ cumulative) — one object class with
    many named members, or one name? Cheapest probe: decrypt two of its ciphertexts and diff.**
24. **The recurring class roots — dump `0x143cf0000`–`0x143d05000` from the data corpus; they should
    be the vtable/type descriptors of the builder sea's object classes (also `0x143d70e30`,
    `0x143d30560`, `0x143f8e270`, `0x143cfe0d0`, `0x143d93520`, `0x143d937e0`). `&DAT_143d013b0`
    ×131 (pass 10) and `&DAT_143d93520` ×51 (pass 11) are the top dump targets — note `0x143d93520`
    is a Z71 registration output, i.e. a runtime-built class object, so dump it too; new pass-11
    root `0x143d04130`. Updated (pass 12): the far band is now confirmed as class roots —
    `&DAT_143f8e270` ×20 this pass (6th overall) and NEW `&DAT_143f93cd0` ×1 (2 addresses from the
    long-open `0x143f93e30` pointer); extend the dump to `0x143f8xxxx`–`0x143f94xxx`.**
    **Updated (pass 14): the static-root era is over — pass 14 uses NONE of these roots; its roots
    are registration outputs (`0x143de6b80` mega-root, `0x143e00ac0/0x143e00c20`, `0x143df6450`)
    and NEW far bands to dump: `0x143eb63c0/67e0/6940/6aa0` (CompilerIDFilter payloads as class
    roots), `0x143ecee70`, `0x143ee0cd0`, and nested-atexit payload slots `0x143e12c40/138a0`,
    `0x143e3c1b0/c310`, `0x143f372b0/381e0`.**
25. **`0x7e2a700b` cross-shape hash — find its consumer (who decrypts by name).**
26. **`s_JIubLB__1438b8f04` (arg2 of `FUN_1401d85c0`, pass 8) — decode it (lives in the 0x1438b8xxx
    ciphertext band).**
27. **CLOSED — fd9670 count resolved by direct recount.** Total textual occurrences of
    `0x140fd9670` over the 108 read chunks = **1,339**: pass 2 ×10, 3 ×11, 4 ×6, 5 ×23, 6 ×105,
    7 ×504, 8 ×227, 9 ×0, 10 ×8, 11 ×445, 12 ×0, 13 ×0. The pass-8 record's "731 cumulative"
    was an arithmetic slip (105+504+227 = 836); the old "1,289" omitted passes 2–5. Unit is
    textual occurrences in `func_0x1421cd360` argument sets; pass 13 uses none. **Pass 14: +54
    (all arg11 of block-G regs) → 1,393 over the 116 read chunks.**
28. **CLOSED — provenance is complete.** All 12 records are in `ranges/`, all 2,228 chunk files
    (`0000`–`2227`) and `index.json` are present, and the per-pass numbers re-derive from the
    chunks: pass 8 401 / 115,925, pass 9 218 / 78,716, pass 10 235 / 74,025, pass 11 765 /
    205,857, pass 12 226 / 74,834, pass 13 258 / 74,840. Nothing needs re-uploading; the only open provenance item left
    is pass-1 `0009`–`0013` (thread 5).
29. **CLOSED as a non-gap (pass 10): the `0x1411b8070`→`0x1411c7060` span is unread corpus, not
    missing code.** It is in chunks `0907`–`0914` (which start at `0x1411b6c20` / end
    `0x1411c5940`); the earlier note claiming 0x1411xxxx is "outside the entry-address order" was
    backwards — it is simply later in the same order, far ahead of the `0x140275350` cursor.
30. **New (pass 10): decompile the fixed pre-step functions `FUN_141520a50`, `FUN_1414134c0`,
    `FUN_140f817e0`, `FUN_140f818a0`, `FUN_141530ba0`, `FUN_14132a2b0`, `FUN_1421c7220`,
    `FUN_1421c7780`; pass 11 adds `FUN_14190dbc0/dc80/dd40` (a `0x14190xxxx` run), `FUN_1413dc060`,
    `FUN_1410eae80`, `FUN_1421c6920` ×2, `FUN_1421c76c0` ×2, `FUN_1421c72e0` — do they init a
    container, or guard another builder?**
31. **New (pass 11): the Z73 token pair `0x292f8ed1cad53cdb` ×2 straddles the 16,601-B unlisted gap
    `0x140229be7`–`0x14022dcc0`; the gap may hold the pair's shared consumer. Inspect first when
    raw listings are available.**
32. **New (pass 11): second `s_` string `s_d____WQ_1438cd11c` (arg2 of `FUN_1402300d0`) — decode
    together with pass 8's `s_JIubLB__1438b8f04`; both live in the `0x1438cxxxx` ciphertext band
    and suggest these registrations carry human-readable labels.**
33. **New (pass 11): `FUN_1411d3e70(0x20)` ×17 vs `FUN_140f80f80(0x10/0x20)` ×16 — two allocators
    with the same call shape side by side in Z72; two heap paths or two arenas? Updated (pass 12):
    the `0x1411d/e` band family grows — `FUN_1411dfda0(0x10)` ×1 and `FUN_1411e00c0(0x10)` ×1,
    both exclusive to 389-B builders (vs `FUN_14114df10(0x10)` ×5, exclusive to 389-B since
    pass 9) — suggests one allocator per 389-B sub-family; decompile all three together.**
34. **New (pass 13): the rootless-builder ladder (231/365/377/479/507-B) is entirely fed by Z78
    registration outputs — decompile `FUN_141216c60` (the first pre-step with an argument, ×3) and
    `FUN_141212ed0` (the size-8 two-buffer helper) to see how the registration product flows into
    the builders.**
35. **New (pass 13): `FUN_14026b680` — the only wrapper whose guard-1 dst is a far temp
    (`0x143dac4d8`) instead of the usual slot-adjacent temp; check whether its row is aliased.**
36. **New (pass 13): the `0x861c6fe6` (×8, chunk 0104 run) and `0xa4339167` (×4, chunk 0106 run)
    hash families — decrypt two of each as the cheapest probe of whether a hash run = one object
    class with many members (extends thread 23's `0xa83c2c26` probe).**
37. **New (pass 14): the 7-builder `0x45a7a69c` run** — `FUN_140282e50/fd0/250/3d0/550/6d0/850`
    all root `&DAT_143df6450` (reg output of `FUN_140282420`) and each uses a DIFFERENT bare
    pre-step (`FUN_1421c6f20/c6e60/c69e0/c76c0/c6b60/c6c20/c6ce0`). Decrypt its ciphertext
    (`0x1438d44xx`) and dump the root — seven instances of one name under one root is the
    sharpest probe of the name/instance model.
38. **New (pass 14): the first 2-arg `c7880` call** (`FUN_14028ad00`:
    `c7880(&DAT_143dfd5f8, &DAT_143dfd5b8)`) and the new nested-atexit row-count variants
    (542-B `FUN_140285700`, 574-B `FUN_14028a570`) — decompile `c7880`'s consumers (it is
    `func_0x…`, so instead map the two argument slots against the shutdown table rows
    `0x1438c6c68`–`0x1438cffc0`).
39. **New (pass 14): per-block allocators** — decompile `FUN_14121a070`, `FUN_141227b30`,
    `FUN_141244840`, `FUN_1412565b0` (+ the rest of the 14) to see whether they are wrappers of
    one heap path or per-block arenas, and why each block stopped using `FUN_140f80f80`.
40. **New (pass 14): the far-band write set** — nested-atexit payload slots moved to
    `0x143e12c40/138a0` (band `0x143e1`), `0x143e3c1b0/c310` (band `0x143e3`),
    `0x143f372b0/381e0` (band `0x143f3`), plus roots `0x143ecee70`/`0x143ee0cd0` — dump these
    bands; they extend the shutdown/class-root picture past `0x143f0`. **Pass 15 adds
    `&DAT_143fa8040` (nested-atexit payload, band `0x143fa8`).**
41. **New (pass 15): unlisted gaps #5 and #6** — `0x140298fd9`–`0x14029a6e0` (5,895 B, between
    chunk-0116's record and block H) and `0x1402bf899`–`0x1402c10c0` (6,183 B, between the Z98
    tail and block K). Inspect in the raw Ghidra listing.
42. **New (pass 15): the moved shutdown table** — rows now written at `0x143e2bc08/18/28/58`,
    `0x143e31d50/78/88/98`, `0x143e41d10/38/48`, `0x143e420b8/90/c8`, `0x143e2e970/998/a8`. Dump
    `0x143e2b000`–`0x143e43000`; check who consumes the old `0x1438c6c68`–`0x1438cffc0` rows.
43. **New (pass 15): `0x3fd91271`** — the only `{id,hash}` record hash (id `0x35`) with no
    matching registration in `0116`–`0123`; grep chunks `0000`–`0115` for it before declaring it
    unmatched corpus-wide.
44. **New (pass 15): the `0x3faff222` family** — ~21 373-B builders + sorted-insert use, all
    rooted on `&DAT_143e185e0` (output of size-0x30 reg `FUN_1402a0ff0`), each with a different
    bare pre-step in the new `FUN_141247af0`–`FUN_141248930` band. Decrypt its buffer (e.g.
    `0x1438da8fc`, `FUN_1402a8e80`) — biggest single-name family found; extends thread 23/36.
45. **New (pass 15): block K is open at the `0123` boundary** — ≥7 regs, outputs `0x143e533a0`–
    `0x143e5bb40`, ciphertexts to `0x1438e7afc`, arg10 band `FUN_14130e3f0`+; resume at `0124`.
46. **New (pass 15): the 471-B builder `FUN_1402bed50`** — one byte under 472-B; helper
    `FUN_140f94810(8,…,0x73bb2f3a)`; its hash equals the flags-10 reg `FUN_1402bcb90`'s
    registration hash (also record id `0x3`'s hash). Decompile `FUN_140f94810` and `FUN_1402bcb90`
    together.

## Next pass

Start at **`chunk_0124.txt`**, first entry after `0x1402c16e0`. Protocol pass = 8 chunks
(~1.5 MB) unless the user names a range; stop at a chunk boundary and state it. Before starting:
read this file and `pass15_0x140298b20-0x1402c16e0.md`. After finishing: write
`ranges/<first>-<last>.md`, append its row to the Coverage table above, refresh the synthesis,
"Complete image", "Cross-cutting conventions" and "Open threads", and note the new cumulative
counts. If a new construct appears, give it an address boundary here. Watch for: (a) block K's
continuation — how many regs, where its outputs land (past `0x143e5bb40`?); (b) whether the
block→sea alternation continues (H→sea→I→sea→J→sea→K suggests a period of ~100 regs per block);
(c) whether `flags` 10 recurs and what align-0x10/size-8 regs become; (d) whether the
`0x3faff222`-style runs continue and whether another record id below `0x3` appears; (e) whether
the shutdown-table band keeps growing (`0x143e2b–0x143e42`) and a 12th+ initializer family
appears; (f) whether the arg10 band reaches the `0x14130c–0x14131` band's end and a new callback
band opens; (g) whether the ciphertext band crosses `0x1438e8000`; (h) whether the two new gaps
(`0x140298fd9`, `0x1402bf899`) get explained by listing data.

## Coverage archive (passes 16–22, moved from `CODE_MAP.md` 2026-11-21 to keep it ≤300 lines)

Rows 1–15 are in the Coverage table above; passes 23+ remain in `CODE_MAP.md`. Source of truth: `state.json`.

| pass | chunks | `.text` range | functions | Σ `size=` | record |
|---|---|---|---|---|---|
| 16 | `0124`–`0131` | `0x1402c17e0`–`0x1402e9f70` | 541 | 147,915 | `ranges/0x1402c17e0-0x1402e9f70.md` |
| 17 (10-chunk override) | `0132`–`0141` | `0x1402ea070`–`0x1403220c0` | 777 | 209,051 | `ranges/0x1402ea070-0x1403220c0.md` |
| 18 (9-chunk) | `0142`–`0150` | `0x1403222e0`–`0x14034ed30` | 562 | 162,088 | `ranges/0x1403222e0-0x14034ed30.md` |
| 19 (10-chunk) | `0151`–`0160` | `0x14034ede0`–`0x1403857a0` | 727 | 196,086 | `ranges/0x14034ede0-0x1403857a0.md` |
| 20 (10-chunk) | `0161`–`0170` | `0x1403858a0`–`0x1403ac1e0` | 522 | 144,458 | `ranges/0x1403858a0-0x1403ac1e0.md` |
| 21 (11-chunk) | `0171`–`0181` | `0x1403ac370`–`0x1403e7590` | 771 | 214,614 | `ranges/0x1403ac370-0x1403e7590.md` |
| 22 (11-chunk) | `0182`–`0192` | `0x1403e7730`–`0x1404191d0` | 630 | 181,579 | `ranges/0x1403e7730-0x1404191d0.md` |
