# The HUD/UI data-provider belt

**Bottom line.** Between the screen tier (pass 43, `0x140849a10`–`0x140874660`) and the
render band there is a binding layer that the 2026-11 sweep read across passes 60–63
(`0x140ac1e70`–`0x140b478f0`, chunks 0542–0579). It is not screens and it is not
rendering: it is the machinery that resolves a service row, reads one field, and pushes
a typed value into the UI DOM — plus, at its far end, the row engine that lays out the
overhead world-space UI (nameplates, health bars, party frames, killcam overlays). The
belt closes at `0x140b478f0`: the row-engine arm band read in pass 63
([`0x140b2b800-0x140b478f0.md`](../ranges/0x140b2b800-0x140b478f0.md)) completes it. The
records that carry the evidence are the pass-60
([`0x140ac1e70-0x140afbb10.md`](../ranges/0x140ac1e70-0x140afbb10.md)), pass-61
([`0x140afbfb0-0x140b13530.md`](../ranges/0x140afbfb0-0x140b13530.md)), pass-62
([`0x140b135a0-0x140b2b5d0.md`](../ranges/0x140b135a0-0x140b2b5d0.md)) and pass-63
records.

## The provider shape

The belt's unit is a five-parameter function — `(handle, panel, view, args, out)` —
that does exactly three things:

1. resolves a service through one of the obfuscated chains (the per-session type
   table, the store-row chain, or the `(id & 0xfff) * 0x10` bucket table);
2. reads one field of the row;
3. emits it as a typed DOM value.

The typed emitters are the same family the screen tier already used
(`FUN_141940c00` bool, `FUN_141941360` u64, `FUN_140940ea0`/`FUN_141940ea0` int,
`FUN_1419413b0` string) — the DOM is the same contract as the pass-43 field ids.
Pass 60 counted 560 of these providers in the `0x140ac–0x140b1` band; passes 61–63
add the service definitions they resolve through, the emit masters that anchor them
to the world, and the row engine that consumes their output.

Almost every provider front door also carries the probe/trace pair
(`func_0x000140c28eb0` / `func_0x000140c29850`) with a small integer id — the belt's
own tracing convention, one id per provider family.

## The service + emit tiers (pass 61)

Behind the providers sits a set of named services, read in pass 61:

- the group-tree serializer `FUN_140b0a390` and name resolver `FUN_140b0a940`;
- the HUD-config pair `FUN_140b0ae00/140b0aba0` and session binder `FUN_140b0b750`;
- the state master `FUN_140b0af80` and the view-state emit/set `FUN_140b18c30`
  (a three-way `FUN_140b18c30(1|2|3)` emit — the last def of the T54-3 band);
- a 703-stub singleton factory belt (vtables `0x143077108`–`0x143082cf0`, 41-B
  constructors, one per service accessor);
- the world-anchoring emit masters: nameplate pose `FUN_140b0bc10`, 6-probe anchor
  `FUN_140b0ddb0`, view-model binder `FUN_140b0e640`, nameplate/health-bar
  `FUN_140b0efb0`, attachment-pose `FUN_140b12fd0`, health-bar `FUN_140b132d0`,
  progress/ring `FUN_140b13530`.

The emit masters are where the belt touches the world: each resolves a row, reads a
world position or transform, and emits a marker record that the render side (the
`0x140cc–ce` camera band) consumes. This is the boundary between "UI data" and
"game render" in this client.

## The refresh cascade + row engine (pass 62)

Pass 62 found the belt's active half: a refresh dispatcher set
(`FUN_140b15030` + change detectors + an 8-handle spring decay), the entity-view build
master `FUN_140b19270` (Euler→matrix over the `0xd8000000000439b–439e` property
namespace, 0x2c-B rows, double marker insert), the refresh-cascade window hosts
(`FUN_140b1aed0/1b230/1d6a0/…`), the raycast hit collector `FUN_140b18960`
(0x50-stride hit rows), and the overhead-UI row engine itself:

- **0xc0-B rows** `{+0x0 target, +0x8 id, +0x70 depth, +0x78 tag 0x1021f102b|0x1021f2287,
  +0xb8 render}` — ctor `FUN_140b28a70`, depth introsort `FUN_140b28340`, layout/diff
  pair `FUN_140b28db0/295b0` (pose interpolation + push-apart redistribute so
  overlapping bars do not z-fight);
- **23-argument DOM emit `FUN_140b29e00`** — 19 link + 19 unlink list memberships per
  row, then the full typed setter set per row;
- **release `FUN_140b2b5d0`** — tag-switch teardown with swap-with-last erase;
- a **0xa0-B pose pool** (`FUN_140b289e0` append, `FUN_140b2b800` grow) — each pool
  unit is two 0x50-B sub-records, not a row plus a snapshot (pass-63 correction of
  ledger 80);
- camera-bounds resolver `FUN_140b2ac40` and radial-slot allocator `FUN_140b1cb80`.

## The arm band + factory waves (pass 63)

Pass 63 read the band the cascade hosts were pointing into. The row-engine arms all
became real entries: the pose-interp helper `FUN_140b2b9a0`, the 73-K frame-emit
walker `FUN_140b2bde0`, the icon-angle recompute `FUN_140b2c9f0`, the DOM dumper
`FUN_140b2cc60`, and a *fourth* copy of the entity-view build master shape
(`FUN_140b35230/35590/34920/34370` — one construct emitted four times, each a
window master with a real 1.5-K body). The world→row bridge is `FUN_140b30b50`:
the member-list iterator quartet walks the world, and `FUN_140b35c20` appends
0x50-stride rows.

Beyond `0x140b37c22` the stratum continues rather than ending (the fourth
consecutive pass with that lesson): the 0576–0579 tier holds the hotfix applier
`FUN_140b387a0` (the pass-28 hotfix record's consumer, with the
`'unknown hotfix'`/`'hotfix failed'` XOR-8 pages), the killcam keyframe-track
builders `FUN_140b3f080` (three row tracks at 0x38/0x1a0/0x150 stride), the
15-state party member state machine `FUN_140b45640`, the session enter/exit pair
`FUN_140b45410/455e0`, and a third singleton-factory wave (~65 more stubs, vtable
band extended to `0x1430900a0`). The killcam **recorder/encoder** trio
`FUN_140b49430/49bd0/4a190` sits in chunk 0580, beyond the belt's close — that is
the next subsystem, not part of this one.

## What this tells us

The belt is the answer to "how does a game state become a UI value" in this client:
not direct reads, and not events alone, but a standing population of ~560 small
resolvers, each bound to one field of one service, feeding a DOM whose row layout
is itself a small engine (depth sort, pose interpolation, push-apart). The overhead
UI is therefore a *rendered projection of the same service rows* the screens read —
the same contract on both sides of the DOM.

The main open question left by the belt is a consumer, not a mechanism: which widget
consumes the 19-property DOM object that `FUN_140b29e00` writes (thread T62-1,
`crossref.py 1421571e0`). The mechanisms are all read.

## Evidence

- Pass 60: [`0x140ac1e70-0x140afbb10.md`](../ranges/0x140ac1e70-0x140afbb10.md) — the
  560-provider band, the array-iterator streaming protocol, the 18-arm filter
  dispatcher, the 8-point world-probe walker.
- Pass 61: [`0x140afbfb0-0x140b13530.md`](../ranges/0x140afbfb0-0x140b13530.md) — the
  703-stub factory belt, the service def set, the emit masters.
- Pass 62: [`0x140b135a0-0x140b2b5d0.md`](../ranges/0x140b135a0-0x140b2b5d0.md) — the
  refresh cascade, the entity-view build master, the row engine's definition.
- Pass 63: [`0x140b2b800-0x140b478f0.md`](../ranges/0x140b2b800-0x140b478f0.md) — the
  arm band closure, the hotfix applier, the killcam track builders, the third factory
  wave.

Cumulative coverage numbers live in `state.json` (machine ledger); the coverage row
in `CODE_MAP.md` is the index. This page deliberately does not repeat them.
