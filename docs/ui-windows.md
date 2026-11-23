# The UI window engine

**Bottom line.** The client's UI is not a retained-mode renderer with a scene graph that
the decompiler simply exposes. It is a data-driven screen system: a per-window object
owns child lists and animation state; screens are built as trees of typed nodes; every
node is identified by a field id; and the screen code pushes values into nodes or reads
them back. The engine room is in pass 38
([`0x140785e30-0x1407a2800.md`](../ranges/0x140785e30-0x1407a2800.md)); the screen tier
that uses it is in pass 43
([`0x140849a10-0x140874660.md`](../ranges/0x140849a10-0x140874660.md)). The row model is
the `0x1421exxx` list API.

Two things are easy to confuse:

- the **window object** (the engine-side object that owns a window's state, child tables,
  animation rings and input bindings);
- the **window cache** (the `_DAT_143b795a0/a8/b0` tables that map a hashed call site to a
  cached window object).

The cache is an optimisation and a decompiler artifact generator. The object is the real
data structure. This page describes both, then the screen tier built on top.

## The window cache and the giants

The cache is keyed by a return-address hash. The recurring prologue computes a hash from
`0x2d1d7705` and the caller's return address, then binary-searches
`_DAT_143b795a0`/`_DAT_143b795a8`/`_DAT_143b795b0`. The matching epilogue appears in
destructors as a `0xfd749dd6ef1fd0d4` tail. Pass 38 found this prologue on the six giant
functions:

- `FUN_140786360` — 140,705 B of text, `size=` 238 (ratio ~590)
- `FUN_1407880b0` — 106,292 B / 147
- `FUN_140789970` — 75,166 B / 3,163
- `FUN_140786b60` — 72,856 B / 56
- `FUN_140786760` — 62,877 B / 56
- `FUN_14078f550` — 57,552 B / 505

These are **decompilation windows, not six real 100-KB functions**. The body is one
window-cache probe plus an inlined body; the `size=` field is the real function size. The
ratio `chunk_bytes / size=` is the tell (see ledger 47). The `max refs:` line can name
earlier callers even when the body is one window, so "many callers" does not make it a
shared helper.

The same pattern appears later in the name-window family from pass 42
(`FUN_1408314b0` through `FUN_1408493b0`, shared `^0xeb + 0x2d1d7705` triple-mix, ratios
up to ~755). The pass-42 record
([`0x14081d520-0x1408493b0.md`](../ranges/0x14081d520-0x1408493b0.md)) treats that family
as one hash/name resolution construct, not fourteen independent functions. By contrast,
pass 43's three largest bodies are real: `FUN_1408551d0` 35,000 B / 4,899,
`FUN_140867e90` 27,431 B / 4,692, `FUN_140861ab0` 25,193 B / 4,792 (ratios 5–7, well below
the window threshold). Do not apply the window label just because a function is large.

## The window object

Pass 38 identifies the canonical per-window object as a **0x22d0-B** construction in
`FUN_140795a40`. It has:

- a vtable (`PTR_FUN_142fac490`) and a magic value `0xbd3de6fbb1c6c733`;
- a 0x800-B pointer table and a 0x200-B pointer table;
- five ring buffers with `0x80000004` capacities at `+0x2bc`/`+0x2ec`/`+0x31c`/`+0x33c`/
  `+0x36c`;
- `0xbd` input rows backed by `DAT_143b8ecd8` (the input-axis count), and `0xbd` hash-C
  maps;
- registration `FUN_141fd8b30(0xac, FUN_14079f3b0, obj, 0)` for the input-binding
  callback.

`FUN_1407871b0` is the same construction in the decompilation window: the body is the
per-window object plus the input binding and entity-slot tables. The 0x22d0-B size is the
real object; the large text is the inlined window.

Around it:

- `FUN_14078a160`/`FUN_14078a310`/`FUN_14078cb20`/`FUN_14078d3f0` build the **0x268-B
  widget-manager** layer (vtable `PTR_FUN_142f95e58`, magic
  `0xca3e1a1d3d45d5ca`, 0x100-B message buffer at `+0x18`, `0x80000032` capacity).
- `FUN_14078dd50` builds the **0x368-B nine-ring animation object**;
- `FUN_14078aa40` splits a trail frame into sub-frames and appends 0x600-B rows;
- `FUN_14078bbe0`/`FUN_14078ba00` append the 0x650-B per-entity and 0x600-B camera trail
  rows. Pass 38 closed the open question about these rows: 0x650 = entity animation/scale
  trail, 0x600 = camera trail.
- `FUN_14078b230` is the 17-case animation-value getter; `FUN_14078c220` computes the
  camera-relative yaw/pitch/distance; `FUN_1407884b0` builds the quaternion-to-basis
  matrix. These are the math bodies passed 37/38 were missing.

The object's animation state is real and per-window. It is not a shared global renderer.

## The typed row model

From pass 42/43, the dominant UI data structure is the **`0x1421exxx` list API**. It is
the client's tree/row model, not a generic container. Pass 43 alone calls
`FUN_1421e5100` 380 times, `FUN_1421e4620` 166, `FUN_1421e41d0` 142, `FUN_1421e52c0`
141, `FUN_1421e40c0` 133, `FUN_1421e47b0` 105, and `FUN_1421e3de0` 103. Those counts are
the evidence that this is the UI's backbone.

The important members:

- `FUN_1421e40c0`, `FUN_1421e3c20`, `FUN_1421e3330`, `FUN_1421e3420` — child-list getters;
- `FUN_1421e5100` — begin/walk;
- `FUN_1421e52c0` — node at index;
- `FUN_1421e3de0`/`3d70`/`3d00`/`3810`/`3920` — field getters;
- `FUN_1421e41d0`/`4620`/`4580`/`4480`/`4860`/`4910`/`49a0`/`4270`/`43e0`/`4170` — field
  setters;
- `FUN_1421e52a0`/`5370`/`5310` — list operations;
- `FUN_1421e51d0`/`5130`/`51a0`/`5230` — typed row constructors;
- `FUN_1421e4140` — type test; `FUN_1421e4af0` — node by type; `FUN_1421e3810` — node by
  key.

The field ids that recur across screens are the closest thing to a UI schema:

- `0x3ff3` and `0x6003` are child-list fields;
- `0x229a` is a value GUID;
- `0x2d95` is a row key;
- node types are GUIDs in the `0xa88000000000xxx` family;
- screen constructors add another `0xa88000000000xxx` GUID per screen.

The list API definitions live at `0x1421e0000+`, about 26.7 MB ahead of the current
cursor. The `window reach:` line tracks calls into that region. Until those defining
chunks are read, the API is known by its consumer-side behaviour only. That is a real
limit: the names "child list", "row key" and "value GUID" are shape-based labels, while
the call counts and field ids are measured.

## How a screen is built

A typical screen constructor:

1. calls a base constructor, for example `FUN_1405648e0(param, guid, flag)` in the
   pass-43 belt,
2. installs a vtable,
3. creates the screen's root node with a unique `0xa88000000000xxx` type GUID,
4. builds children by calling `FUN_1421e4af0(parent, field_id, node_type, 0)` or the
   typed row constructors,
5. reconciles rows against the previous frame with `FUN_140726c50` (remove),
   `FUN_1405df280` (insert) and `FUN_1421e5310` (replace),
6. pushes values through the setters, or reads them back through the getters.

The tree iterator for this is `FUN_14084d390` (fields `0x3ff3`/`0x6003`); the
search-by-field helper is `FUN_14084c9d0` (`0x229a`). Both are used across the settings
and hero-select screens, which is why they are treated as general UI primitives.

The screen belt in pass 43 contains roughly 40 constructors. They cover audio settings,
team compare, payload/objective timers, kill-cam target, hero detail, team status,
scoreboard, BattlePass, friends/invite, queue, chat, career stats and hero-select. The
belt is not a framework with a registry; it is a repeated constructor pattern over the
same list API.

## The screen families

**Settings.** The settings tier is a good concrete example of the whole system:

- `FUN_14084a3a0` is a 12,924-B switch over `0xd8000000000xxxx` settings GUIDs; its
  default arm logs `Missing guid [0x%llX] in switch statement` from the XOR-8 page
  `0x14385f5e8`.
- `FUN_14084b060` builds the settings screen and enumerates devices.
- `FUN_14084b750`/`FUN_14084bfb0` are the pull/commit pair: read the screen fields into
  the model, then read them back and apply per-cvar callbacks.
- `FUN_14084c540` is the interdependency engine: enable/disable propagation over about 30
  fields, with inverse gates from the getters `FUN_140914680`/`FUN_140913960`.
- `FUN_14084dc10` builds device rows; `FUN_14084c9d0` and `FUN_14084d390` are the search
  and iterator helpers.

The settings-field GUID catalogue is still open (T43-3). The get/set family at
`0x140912xxx`–`0x140916xxx` is the next region to read; pass 43 saw about 100 field GUIDs
consumer-side.

**Kill feed and scoreboard.** `FUN_1408551d0` is the 35,000-B match-event/kill-feed screen.
It collects 0x20-B per-player stat rows, overrides them from the summary service's
0xe0-B rows, computes a ratio, deduplicates through the open-addressing set
`FUN_140857980`, sorts with the 0x20-B intro-sort `FUN_140856550`, and mints one
`0xa880000000006dc` node per sorted row. The seen-set uses the hash chain
`(~x + x*0x40000 → (^>>0x1f)*0x15 → (^>>0xb)*0x41) & 0x7fffffff`, which is a distinct
hash family from hash C/D.

**BattlePass.** The BattlePass tier is not a separate framework; it is a set of screens
over the same row model:

- `FUN_14085f600` decodes the eight page names (`BattlePassMainPage`,
  `BattlePassDetailedPage`, `BattlePassUpgradePage`, `BattlePassBuyTiersPage`,
  `BattlePassInfoPage`, `BattlePassRewardsPage`, `BattlePassHeroInspectPage`,
  `BattlePassStoryPage`) plus `UNKNOWN` into `_DAT_143b94e80..eb8`. That is the navigation
  table, in plaintext.
- `FUN_14085c850` is the 21,987-B main screen: tier ladder, rewards, JSON summary posted
  through `FUN_140840db0`.
- `FUN_140861ab0` is the 25,193-B career-profile giant: tier ladder, claim records,
  premium reward rows, and JSON-in-node posts through `FUN_1421e3810`/`FUN_1421e33b0`.
- `FUN_14085c450` writes the field-id set `{0x681d, 0x9ff0, 0x9fb8, 0xa3a4, 0x12cbd,
  0x9fb7, 0x9fb6, 0x7e5a, 0xa470, 0x639f, 0x13338}` that pass 42's summary writer reads —
  the writer/reader pair confirmation.
- The store client is the masked-key family `FUN_140995xxx`/`FUN_140598xxx`; its bodies
  are unread, but the consumer side is clear (product lookup `FUN_140993710`, image
  getters `FUN_1409958c0`/`FUN_140993820`).

**Social and hero-select.** The friends/invite/queue tier uses the same row model over
service state:

- `FUN_140865270` refreshes invite rows (hero GUID, party count, invite state, expiry,
  enemy and invited-by lists);
- `FUN_140867e90` is the 27,431-B group-invite collector;
- `FUN_14086ac30` is the chat-entry object with two compiled regexes
  (`^/[^\s]*$` and `^(/([^\s]+)\s+)`, pages `0x1438604d0`/`0x1438604e8`);
- the hero-select screens are covered in [`hero-tier.md`](hero-tier.md).

## How the UI talks to the game

The UI does not read raw game memory directly. It resolves services through the same
per-session type table as the rest of the runtime, then reads/writes rows through the
list API. When it needs to change game state it posts events or JSON:

- event posts use the standard group-service vtable call (`+0x18`) or the app event
  queue;
- summary and BattlePass screens build JSON through the `FUN_140693130`/
  `FUN_1406935f0` writers or the compact `func_0x00014213ee60` family, then post it with
  `FUN_140840db0` or the app vtable;
- the UI receives data by walking service rows (0x20/0x28/0x58/0xe0 strides are common)
  and minting typed nodes.

This is why the same field ids appear in a writer in one pass and a screen in a later
pass: the field id is the contract between the UI row model and the service-side
serializer.

## What this tells us

The UI is a large, data-driven consumer, not the source of the game's behaviour. Its
screens are assembled from typed rows, its state comes from services, and its actions go
back through events and JSON. The engine-side window object and cache are real, but the
giant bodies that dominate `.text` in pass 38 are decompiler windows. Read them for the
one inlined body, not as separate functions.

## Evidence

- Pass 37:
  [`0x140760c30-0x140784fd0.md`](../ranges/0x140760c30-0x140784fd0.md) — first UI window
  manager, mod tables, interpolator.
- Pass 38:
  [`0x140785e30-0x1407a2800.md`](../ranges/0x140785e30-0x1407a2800.md) — window cache,
  giants, springs, trail rows, widget manager, descriptor unpack.
- Pass 39:
  [`0x1407a28c0-0x1407cc6a0.md`](../ranges/0x1407a28c0-0x1407cc6a0.md) — session object
  with the same window-cache epilogue and handle tables.
- Pass 41:
  [`0x1407f6a30-0x14081d3e0.md`](../ranges/0x1407f6a30-0x14081d3e0.md) — widget factory
  belt, screen factories, entity-view/HUD.
- Pass 42:
  [`0x14081d520-0x1408493b0.md`](../ranges/0x14081d520-0x1408493b0.md) — HUD binding,
  name-window family, summary field-id set.
- Pass 43:
  [`0x140849a10-0x140874660.md`](../ranges/0x140849a10-0x140874660.md) — screen belt,
  list API dominance, settings, kill feed, BattlePass, social, hero-select.

Open threads that matter for this page: T43-3 (settings-field GUID catalogue), T43-2
(list-API definition region `0x1421e0000+`), T42-4 (name-window family boundary), and
the map/mode enum table (`crossref.py 142d37920`). See `CODE_MAP.md` §"Open threads".
