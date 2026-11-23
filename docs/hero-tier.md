# The hero tier

**Bottom line.** The hero tier is the part of the client that turns a player's selected
hero into a live entity: an ability container, a stack of stat modifiers, a cooldown and
charge state machine, a projectile path, and a set of presentation/query objects. It is
read in three slices:

- the hero entity and ability system in pass 41
  ([`0x1407f6a30-0x14081d3e0.md`](../ranges/0x1407f6a30-0x14081d3e0.md));
- the hero actor, status-effect store and lobby hero rules in pass 42
  ([`0x14081d520-0x1408493b0.md`](../ranges/0x14081d520-0x1408493b0.md));
- the hero-select and team-assembly engine in pass 43
  ([`0x140849a10-0x140874660.md`](../ranges/0x140849a10-0x140874660.md)).

The UI side of hero-select uses the typed row model described in
[`ui-windows.md`](ui-windows.md). This page is about the hero data and the gameplay
semantics.

## The hero entity

The central object is a **0x2a10-byte hero entity**, constructed by
`FUN_140802620`/`FUN_140802660` and destroyed by `FUN_140809280`. Its most important
fields are six **0x110-byte ability slots**:

- slot 0 starts at `+0x60`;
- the next slots follow at `+0x110` stride;
- a mirrored alternative set starts at `+0x2300` and is selected by `FUN_140804550`.

Evidence: the constructor writes the six slots and the mirror, and the guards in the
ability functions compare the slot index against 6. The natural reading is six slots =
primary, secondary, ability 1, ability 2, ultimate, and an empty/none slot. That label is
**inference**; the count, offsets and stride are evidence.

Each slot owns **0x50-byte charge/cooldown rows**. The backlog walk
(`FUN_140803490`/`35e0`/`3640`/`36c0`/`3720`/`3790`) reads:

- the slot/charge index;
- time remaining;
- charge count;
- a `0x80` flag that selects a 6-vs-20 stack split;
- a 64-bit compaction id.

The `0x80` flag is the kind of detail that matters: the same ability can have a small
stack cap and a large one, and the flag chooses which. Do not normalise it away.

## Stats and modifiers

`FUN_1408038e0` is the **~2,000-case stat getter**. It switches over id bands roughly
`0x196`–`0x837` and returns:

- per-slot fields at the slot's `+0x110` offsets;
- curve samples at `+0x10`/`+0x20`;
- projectile/spread floats at `+0x40`–`+0x48`;
- a fallback result from `FUN_140d368d0`.

The function is large because the stat schema is large, not because it is doing 2,000
different things. The id bands are the schema. If you need a stat, start from the id and
trace which branch reads it.

The stat modifier path is separate:

- `FUN_1408045f0` and `FUN_1408050d0` are the charge/apply pair;
- they build `0x11`-stride stat stacks through `FUN_140805620`/`FUN_1408051a0`;
- the stacks are looked up in the `FUN_142044820` bank;
- spin-lock epoch counters at `0x1000` granularity guard the mutation.

`FUN_14080d850` is the clean 48-row × `0x18`-byte stat fold: three 16-row banks at
`+0x18`/`+0xa8`/`+0x138` aggregate into a 16-float result, with the `+0x15`/`+0x16`
selectors choosing percent versus flat. `FUN_14080e720` is the charge-full SIMD test
(eight-wide float accumulation over a `0x40`-stride row set, count at `param_1[0xbd]`).
`FUN_14080e870` is the progress-ratio getter (ids `0x79`–`0x7f`, `0x99a`, `0x151`,
`0x80`, using current/max pairs from vtable slots `+0x78`/`+0x70`/`+0x50`/`+0x40`).

## Tick, charges and casts

The per-frame ability tick is `FUN_140804070`. For each of the six slots it calls the
per-slot tick `FUN_140d29c60` at the `0x110` stride, gates VFX emission on
`_DAT_142f84b18`, and uses the time scales `_DAT_142f841e8`/`_DAT_143871e08`.

The charge/cast flow:

1. `FUN_1408038e0` supplies the ability's stat values.
2. `FUN_1408045f0`/`FUN_1408050d0` consume/add a charge and push the stat stacks.
3. `FUN_14080a730` is the ability-cast broadcast. It normalises two quaternions, pushes
   `0x40`-stride rows into `FUN_140558120` vectors, uses type id `0x240000000001927`, and
   ends in the `FUN_140d45d20` emitter.
4. `FUN_140807240`/`FUN_1408077e0` are the projectile-fire path. They build `0xe0`-byte
   projectile rows, resolve the weapon through `FUN_1407a740`, and push modifiers through
   `FUN_14214a390`.

The ability scheduler is the group `FUN_14080fc10`/`FUN_1408100f0`/`FUN_1408105c0`: a
`0x18`-stride triple-flag row walk at `param_1+0x3ee`, a `0x16`-row bank, and the same
window-cache probe as the UI giants. `FUN_140811150` is the first-charge gate
(`FUN_140c86190` test, `0x2be1c148` rounding bias). `FUN_140811340`/`FUN_140812140` are
config-driven behaviour setters: state 0/1/2 writes `+0x118` = `0x101`/1/0.

The ability/stat evaluation giants `FUN_14080c740` (114,446 B of text), `FUN_14080e570`
(72,227 B) and `FUN_14080e870` (59,234 B) are **decompilation windows**, not real
functions of that size. They share the `0x2d1d7705` window-cache probe and a ~60-entry
`0x18`-stride modifier/stat ladder. Read them as one inlined stat-evaluation body. The
clean bodies between them (`FUN_14080d850`, `FUN_14080e720`, `FUN_14080e870`,
`FUN_14080a730`) are the semantics.

## Hero records, actors and effects

There are three different "hero" objects in the read:

- the **0x18a0-B hero/entity record** first seen in pass 37; it carries animation rings
  and the entity/hero data used by the UI and the match result tier;
- the **0x4b0-B hero actor** (`FUN_14083f2c0`/`FUN_14083fd40`, pass 42); it owns child
  descriptors, inline sub-arrays, a `0x318` pending list of `{id, handle, flags=2}` rows,
  and a `0x2a8` event-text queue. `FUN_14083ba80` is its 19-KB hero-skin/voice query;
  `FUN_140841d00`/`FUN_14083fee0`/`FUN_140840330` resolve the parent hero record;
- the **hero-select screen object** (see below), which is UI, not simulation.

The lobby rules tier from pass 42 works over **seven `0xd0`-stride hero-record banks**.
`FUN_140827680` collects the selected-hero GUIDs; `FUN_140827790` deduplicates them in a
hash-D set; `FUN_140827b70` removes one entity's slots. The team predicates
`FUN_1408282f0`/`FUN_1408283d0` compare the local-player GUID at service `+0x1b0`/`+0x1b8`
against the default `DAT_144188150`; this is the tier's identity gate.

The **status-effect store** is a `0x58`-stride row set collected through
`FUN_140bf36c0`. `FUN_1408464a0`/`FUN_1408466f0` look up and remove effects by GUID;
`FUN_1421be120` updates, `FUN_1421be7b0`/`FUN_1421bf280` add/remove. The `0x140bfxxxx`
row API is named from this consumer but its bodies are unread — that is the main
limitation on the effect store.

The scoreboard/kill-cam side of the same tier is also hero-aware:
`FUN_140843440`/`1408436b0`/`140843800` collect players matching a filter (global player
list `PTR_DAT_14385f3b0`, 0x10 stride, `DAT_143b945b0` spinlock); `FUN_140843a20` picks
the kill-cam entity; `FUN_1408460e0` maps the mode table to a victory-music id;
`FUN_140849320` sets the speed multiplier. These are presentation consumers of the hero
records, not the ability simulation.

## Hero select and team assembly

The hero-select screen object is a **0x1b00-byte** construction in `FUN_1408722a0`
(pass 43). It contains:

- `0x40` rows of `0x20` bytes at `+0x100`;
- `0x40` 0x40-byte string pairs at `+0x900`;
- two function pointers `PTR_FUN_142f7d730`/`740` at `+0x640`/`+0x648`;
- `0x40`/`0x18`-entry arrays at `+0x1980`/`+0x1a10`;
- `-1.0` slot offsets;
- the sentinel **`0x13e`** (318) at `+0x345`/`+0x1a28`.

That constant is the "none" value used by the auto-fill/hero-kind checks, not a measured
roster size. The pass-43 record's parenthetical "= 62" is an arithmetic slip: the chunk
text writes and compares the literal `0x13e` (318) at `+0x345`/`+0x1a28`/`+0x1a2c`, never
`0x3e` (Correction 59). Whether `0x13e` is also a
hero-table size is still open (T43-7); do not quote 62 as the number of playable heroes.

The team-assembly path:

- `FUN_14086f130` is the hero-select dispatcher; it walks the `DAT_143049d10` 20-GUID
  stat-page array and opens events `0x664e`/`0x66b7`.
- `FUN_14086f590` rebuilds the roster from the eight tab getters
  `FUN_14079a2d0(svc, 0..7, 0)` and the `0x28`-stride slot rows
  (`FUN_140796170` init, `FUN_14079d660` fill, `FUN_14079d5b0` read).
- `FUN_14086f8a0` collects bans: it walks the `0x66f6` tree with `FUN_14084d390`, reads
  the per-locale hero availability through `func_0x140c70eb0` +
  `FUN_140c71110`, and upserts the ban list at service `+0x290` (0x18-stride
  `{player, hero, value}` rows).
- `FUN_140872b90` is the 20,069-B hero-row resolver: ban check, take-free-slot arm, row
  types `&DAT_143ea1210`/`1370`/`18f0`, stat arms `0x2ab4`/`0xd0ea`, colour quad
  `+0x28..+0x34`, four-band level thresholds, team-name format, row register.
- `FUN_1408741d0` is the team-swap handler (8-slot arrays at `+0x1ad0`/`+0x1b10`, field
  `0x646f`, group rows `0xd672`).
- `FUN_140874660` is the 21,156-B auto-fill/suggest engine: slot walk, media-service
  hero-kind getter (`0x13e` = none sentinel), hero suggest pair `FUN_141b28910`/`141b28190`, role
  counts, and the role-kind family `0xc880000000000cd` = `{0xcd7425, 0xcd1601,
  0xcd32f4, 0xcd64c0, 0xcd7423, 0xcd7424, 0xcd7503, 0xcd8d23, 0xcdb0b3, 0xcdb106}`.
  The tank/support/DPS labels are **inference** from the role-count call and the
  auto-fill context, not from a name table.

The 13-stat team-comparison event `FUN_1408701b0` collects the stat GUIDs `{0xd12c,
0xd12a, 0xd12b, 0x115fc, 0x12194, 0xd12d, 0x12a70, 0xe736, 0xd12e, 0xcfa4, 0xd12f,
0x106bd, 0xd130}` as a 0x7b-bit mask test. The enable matrix `FUN_1408704c0` reads/writes
about 30 settings field pairs through `FUN_140916330`/`FUN_1409164d0` and
`FUN_140913960`. The hero career stats screen `FUN_14086efc0` (9,838 B) uses about 20
stat fields with two GUID variants per stat (mode 0 `0x2ab4…0x48d0`, mode 1
`0xd0e1…0xd0eb`) and hero kinds `0x8e6161`/`0x8e6126`/`0x8e7cb1`/`0x8ed436`.

## How the pieces connect

The intended live path, inferred from the constructors and consumers, is:

```text
selected hero / roster
  → hero record (0x18a0 or 0xd0-stride bank)
  → hero entity (0x2a10) with six 0x110-stride ability slots
  → charge/cooldown rows (0x50) and stat stacks (0x11 stride)
  → cast/projectile path (0x40/0xe0 rows)
  → presentation (actor 0x4b0, effects 0x58, HUD/scoreboard)
```

The UI path is:

```text
hero-select screen (0x1b00)
  → typed UI nodes (0x1421exxx list API)
  → per-locale availability, ban list, roster slots
  → service events / JSON
```

The two paths meet at the hero record and at the service events. That is why the same
hero GUIDs and field ids appear in pass 41's gameplay code, pass 42's lobby rules, and
pass 43's screen code.

## Confidence and limits

- The object sizes, slot stride, row strides, field offsets and counts are evidence from
  the constructor/destructor and the row walks.
- The names "primary/secondary/ability/ultimate", "tank/support/DPS", and "status
  effect" are shape-based inference. The code does not carry readable names for them.
- The ability-config families `0x140d2xxxx`/`0x140d5xxxx` are named from this tier but
  their bodies are unread.
- The `0x140bfxxxx` hero-record row API is named from the effect store but its bodies are
  unread.
- The exact meaning of the `0x13e` sentinel is open (T43-7). It is 318; the chunk text
  writes the full literal, not a low byte. If it is a hero-table size, cross-check it
  against the pass-42 hero banks before using it.
- The network side of abilities is the bitstream, not a separate schema. The ability
  ids/events are catalogued in `CODE_MAP.md`, but the wire format remains open.

## Evidence

- Pass 41:
  [`0x1407f6a30-0x14081d3e0.md`](../ranges/0x1407f6a30-0x14081d3e0.md) — hero entity
  constructor/destructor, six slots, stat getter, charge/apply, cast, projectile,
  stat fold, scheduler.
- Pass 42:
  [`0x14081d520-0x1408493b0.md`](../ranges/0x14081d520-0x1408493b0.md) — hero actor,
  status effects, seven hero-record banks, hero rules, scoreboard.
- Pass 43:
  [`0x140849a10-0x140874660.md`](../ranges/0x140849a10-0x140874660.md) — hero-select
  screen, roster/ban collector, row resolver, team swap, auto-fill, career stats.
- Pass 37:
  [`0x140760c30-0x140784fd0.md`](../ranges/0x140760c30-0x140784fd0.md) — first 0x18a0-B
  hero/entity record and animation-ring API.

Open threads: T43-7 (hero-select sentinel 0x13e), T43-3 (settings-field GUID catalogue), T41-3
(entity-root chain), T41-6/T41-7 (`FUN_142044820` bank objects, observer block fn-ptrs).
See `CODE_MAP.md` §"Open threads".
