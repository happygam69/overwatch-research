# The engine runtime

**Bottom line.** After the registry machine ends, `.text` becomes the client itself. The
runtime is a single large service-oriented application: one global app object owns roughly
150 child subsystems, objects are looked up through a per-session type table and opaque
handle tables, and nearly every feature talks through an event bus. The read has followed
that runtime from the bootstrap at `0x14053f6b0` to the hero-select UI at `0x140874660`
and is still open.

This page gives the shape and the recurring idioms. The per-tier detail is in the pass
records linked below; [`ui-windows.md`](ui-windows.md) and [`hero-tier.md`](hero-tier.md)
cover those two subsystems separately.

## Where the runtime starts

The boundary is not a single function. The last registry constructs run through pass 27,
and the same pass contains the first runtime machinery:

- `0x14053f6b0`–`0x14058200x` is the bootstrap/obfuscation zone: module resolution,
  signature scanning, anti-tamper checks, the PE entry trampoline `0x140540fd0`, and the
  masked-pointer layer.
- `FUN_140541200` is the signature scanner (VirtualProtect + byte-pattern `memcmp`).
- `FUN_140541450` and `FUN_1405414a0` are the large obfuscated anti-tamper bodies.
- `FUN_140541b50` is an obfuscated job dispatcher over a readiness bitfield; it is the
  bridge from startup work to runtime handlers.
- `func_0x1421cd360` registrations stop here. Pass 28 onward contains no ciphertext
  registration and no `{id,hash}` record.

Pass 27 is therefore a transition record
([`0x1404bfe00-0x14054ea50.md`](../ranges/0x1404bfe00-0x14054ea50.md)); pass 28
([`0x14054fea0-0x14057fe40.md`](../ranges/0x14054fea0-0x14057fe40.md)) is the first
runtime-only range.

## The app object and its services

The client has one global app object at `_DAT_143b7f410`. It is created by
`FUN_140585220` in pass 29: allocate `0x470` B, run the constructor `FUN_1405838c0`,
store the pointer in `_DAT_143b7f410`, then bind it to the engine.

Two large composition functions attach the children:

- `FUN_140554220` (pass 28) allocates and attaches about 90 subsystems and reads 33
  console variables.
- `FUN_1405559c0` (pass 28) attaches about 60 more through a second container, with two
  distinct child lists.

That is the source of the "~150 subsystems" figure in `CODE_MAP.md`. The composition
functions are the best map of what the client considers a service: settings, voice/chat,
hotfix, spatial queries, entity/component access, HUD, workers, store, social, UI, and so
on.

Services are usually reached through the app object's type table, not by direct global
references. The dominant resolver is a per-session table:

```text
app + 0x160
  → (x + 0x3fa981c8e7192fa6) ror 31 ^ 0x8784b4333a580288
  → ror 23 + 0x37a9e6a2eedd5214 + type_index * 8
```

Pass 42 saw this chain at about 150 sites through 25 different type-index fetchers, which
is why it is treated as the runtime's main service lookup. A second common root is the
group-service chain
`0x1439aef88/e08/028` plus `0xb2485ad1cf871d2c ^ 0x89d3e0b8c0994abf + 0x820b88e340ab6eb0`;
a third is the store-row chain `0xba397115a070ffa9 + 0x4094aaa9c7911a89`. The exact chain
you see in a function tells you which service family it is talking to. These are
conventions, not guesses: the records quote the arithmetic at the call sites.

## The recurring primitives

Several low-level patterns appear in every later tier. They are worth knowing before
reading a pass record.

**Containers.** The allocator is `func_0x141c23490(&PTR_PTR_143a01d18, size[, align])`
and the free is `func_0x000140578190`. Vectors, hash maps and sorted arrays are
specialisations over that allocator. Do not key on a symbol name such as "allocator";
key on the call shape.

**Hash maps.** There are several families. The ones named in `CODE_MAP.md` are
hash A (64-bit keys), hash B (32-bit keys), hash C (the `0x200000`/`~key` family), hash D
(the `-0xae502812aa7333`/`-0x3b314601e57a13ad` double-mix), and a later open-addressing
set using `(x*0x40000+~x)*0x15*0x41`. The families are distinct; do not merge them just
because two call sites look similar.

**Handles.** A common 16-byte row is `{u32 handle, u32 pad, u64 entity_ptr}`. The main
handle table has 0xfff buckets and a generation/lease helper that packs a page and a
thread id. Pass 40 added a second, generational `0x2000`-slot table (`FUN_1407dd9c0` is the
table, `FUN_1407dd910` mints, `FUN_1407dda70` releases). Handles are opaque; resolve them
through the table helper, never by pointer arithmetic on the handle value.

**Events.** The canonical post is either
`func_0x000140c28eb0(_DAT_143b7f410)` or a group-service vtable call:

```text
(svc + 0x3c3b9d672a4416a4) ^ 0xf9798462dc0addd7
  → (**vt + 0x18)(svc, event_id)
```

Event ids in the 0x22–0x54 range recur (about 60 sites per pass), and later tiers add
larger blocks. The event bus itself is the `0xb0` descriptor + `0x30` listener idiom first
mapped in pass 32 and refined in pass 35.

**Retire/lifetime.** A repeated teardown idiom uses a `0x20000`-flag guard, vtable slots
`+0x158`/`+0x200`/`+0x160`, the helpers `FUN_1421522e0`/`func_0x00014214eb70`/
`FUN_14214d400`, and a `+0x914` sentinel. It appears in destructors from pass 34 onward
and is most dense in the participant tier. If you see that shape, you are looking at
object retirement, not gameplay logic.

**Bitstream and JSON.** The bitstream reader is `FUN_1406232f0` and the writer is
`FUN_1406264c0`. Replays reuse the same bitstream format as the live entity stream; there
is no separate replay codec. JSON has more than one parser: the pass-32 text engine
(`FUN_140673120`) and a later rapidjson-style parser (`FUN_140612090`, DOM verify
`FUN_1422ee440`). The writer family used by the UI is the `FUN_140693130`/
`FUN_1406935f0`/`FUN_1406934c0` group plus the compact `func_0x00014213ee60` writer.

## The runtime tier by tier

The table is the chronological reading order, not a call graph. Each row links the record
that contains the zone walk and the evidence.

| pass | `.text` range | what the range actually contains |
|---|---|---|
| 28 | `0x14054fea0`–`0x14057fe40` | app composition, containers, settings readers, voice/chat, hotfix, spatial queries, component access |
| 29 | `0x14057ff10`–`0x1405b2ee0` | app methods, entity tables, tracked entities, hotfix downloader, per-entity parallel update, HUD, event bridge, cvar registration |
| 30 | `0x1405b3080`–`0x140610980` | spawn queue, social roster/presence, Steam/job/HTTP, stats/input, RNG/bitsets, JSON parser and object model |
| 31 | `0x140610c60`–`0x1406446c0` | match-lifecycle receive: lobby/instance handlers, bitstream deserializer, entity delta apply, match phases, saved matches, JSON writer, JamMessage dispatch, event-bus subscription |
| 32 | `0x140644930`–`0x140676370` | gameplay loop: event bus core, connection/lifecycle, client entity runtime, NetworkEventSystem, match handlers, per-frame tick/visibility/HUD, JSON text layer |
| 33 | `0x140676e90`–`0x14069b460` | presentation: tick helpers, visual actors, VFX keyframe engine, animation rings, widget data binding |
| 34 | `0x14069bb80`–`0x1406c7080` | replay/highlight/cinematic, progression reports, voice-channel manager, hash-grow |
| 35 | `0x1406c7b50`–`0x140738b30` | party/presence, stats, store/monetization (`StoreSystem_C`), OAuth, Steam microtransactions, product catalog |
| 36 | `0x140738d00`–`0x140760880` | store completion, telemetry, SAPI voice, screenshots, controller layer, sound/impulse/spatial |
| 37 | `0x140760c30`–`0x140784fd0` | input walker, map/scene lifecycle, live-ops feed, capability manager, 0x18a0-B hero record, UI windows |
| 38 | `0x140785e30`–`0x1407a2800` | UI-window engine room: window-cache giants, springs, trail rows, widget manager, descriptor/event machinery |
| 39 | `0x1407a28c0`–`0x1407cc6a0` | session object, spawn solver, command dispatch, social object, group/party lifecycle, slot engine |
| 40 | `0x1407cce30`–`0x1407f68b0` | roster/session, match/join/redemption, hero-select, event logger, match history, result builders, media, kill feed, generational handles |
| 41 | `0x1407f6a30`–`0x14081d3e0` | participant/tracked entities, widget factory belt, hero ability/weapon/stat system, ability scheduler, entity-view/HUD |
| 42 | `0x14081d520`–`0x1408493b0` | HUD binding, voice client, lobby rules, name-window family, hero actor, status effects, scoreboard, summary writer |
| 43 | `0x140849a10`–`0x140874660` | settings/menu screens, screen-builder belt, kill feed, BattlePass, friends/invite/queue, hero-select/team assembly |

The one-line summaries are compressed from the records. Use the record links in the
"Evidence" section below for the exact functions and addresses.

## What the runtime is for

The cumulative picture is a complete game client, not an engine library:

- It boots, binds the platform (NVIDIA, Steam, Battle.net, SAPI), and composes its
  services.
- It receives matches over a bitstream, applies entity deltas, runs the per-frame tick,
  and renders through a presentation layer.
- It records and replays the same bitstream, builds highlights and cinematics, and
  reports results.
- It talks to the store, live-ops feeds, hotfix service, party/voice/chat, and the
  BattlePass backend.
- It builds its entire UI from data: typed nodes, field ids, and service-backed rows.

No plaintext game protocol has been found. Entity traffic is the bitstream; replays reuse
it. The render device is the `FUN_141ff40f0` family. Its lifecycle is mapped from the
consumer side, but the bodies are unread. The store API at `0x14099xxxx` and the UI list
API at `0x1421e0000+` are also consumer-side only.

## What is still open

- **The runtime stratum itself.** Pass 43 ends at `FUN_140874660`; the cursor is at
  `0x140874660` (19.55 % of functions, 15.12 % of declared `.text` bytes). The next range
  is chunks `0403`–`0410`, `.text` `0x140875440`–`0x1408a6750` (see `NEXT.txt`).
- **The protocol.** Command ids, event ids and message ids are catalogued, but the wire
  format is known only as "the bitstream". There is no plaintext schema.
- **Obfuscated bodies.** Several large functions are read structurally only: the
  overlapping-instruction dispatchers, some window giants, and the anti-tamper bodies.
- **Undumped bodies.** `func_0x…` names have no decompiled body in this corpus. The
  registrar/decryptors, the store API, the render tier, the time/random helpers and the
  `0x140f49xxx`/`0x140f1exxx`/`0x140d2xxxx`/`0x140d5xxxx` families are in this class.
- **Gaps.** The corpus is missing functions in places. `scripts/gap_report.py` is the
  authority; do not assume a gap is padding. The open holes are tracked in
  `CODE_MAP.md` under "Open threads".

## Evidence

- Pass 28: [`0x14054fea0-0x14057fe40.md`](../ranges/0x14054fea0-0x14057fe40.md) — app
  composition, settings, containers, voice.
- Pass 29: [`0x14057ff10-0x1405b2ee0.md`](../ranges/0x14057ff10-0x1405b2ee0.md) — entity
  tables, hotfix, HUD, event bridge.
- Pass 30: [`0x1405b3080-0x140610980.md`](../ranges/0x1405b3080-0x140610980.md) — social,
  Steam, input, JSON.
- Pass 31: [`0x140610c60-0x1406446c0.md`](../ranges/0x140610c60-0x1406446c0.md) — match
  receive.
- Pass 32: [`0x140644930-0x140676370.md`](../ranges/0x140644930-0x140676370.md) — gameplay
  loop.
- Pass 33: [`0x140676e90-0x14069b460.md`](../ranges/0x140676e90-0x14069b460.md) —
  presentation.
- Pass 34: [`0x14069bb80-0x1406c7080.md`](../ranges/0x14069bb80-0x1406c7080.md) — replay.
- Pass 35: [`0x1406c7b50-0x140738b30.md`](../ranges/0x1406c7b50-0x140738b30.md) — party
  and store.
- Pass 36: [`0x140738d00-0x140760880.md`](../ranges/0x140738d00-0x140760880.md) — store
  completion, telemetry, sound.
- Pass 37: [`0x140760c30-0x140784fd0.md`](../ranges/0x140760c30-0x140784fd0.md) — map,
  live-ops, UI windows.
- Pass 38: [`0x140785e30-0x1407a2800.md`](../ranges/0x140785e30-0x1407a2800.md) — UI
  engine room.
- Pass 39: [`0x1407a28c0-0x1407cc6a0.md`](../ranges/0x1407a28c0-0x1407cc6a0.md) — party
  client.
- Pass 40: [`0x1407cce30-0x1407f68b0.md`](../ranges/0x1407cce30-0x1407f68b0.md) — match
  and media.
- Pass 41: [`0x1407f6a30-0x14081d3e0.md`](../ranges/0x1407f6a30-0x14081d3e0.md) — hero
  ability tier.
- Pass 42: [`0x14081d520-0x1408493b0.md`](../ranges/0x14081d520-0x1408493b0.md) — lobby
  rules and hero actor.
- Pass 43: [`0x140849a10-0x140874660.md`](../ranges/0x140849a10-0x140874660.md) — menu,
  BattlePass, social, hero-select.

The cumulative conventions and counts are in [`CODE_MAP.md`](../CODE_MAP.md); the
machine ledger is [`state.json`](../state.json).
