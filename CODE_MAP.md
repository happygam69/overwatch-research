# CODE_MAP — cumulative map of the systematic `.text` read

**Read in full before every pass; update after every pass. Hard budget: ≤300 lines** (raised
from 250→300→350 across passes 23–39; re-tightened to 300 at pass 40 — see Corrections 56).
Per-pass narrative lives ONLY in `ranges/`; cumulative numbers come from `state.json` (via
`scripts/pass_measure.py`) — never hand-add. Long-form archive: `CODE_MAP_ARCHIVE.md`.

## Files

| file | role |
|---|---|
| `chunks/chunk_NNNN.txt` | corpus, address order; unreachable-block warnings stripped 2026-11-21 (per-chunk counts in `index.json`, pre-strip `index.pre_strip.json`) |
| `index.json` / `state.json` | per-chunk bytes / first / last (coverage truth) / machine ledger: next_chunk, per-pass entries, cumulative totals, all registration hashes, all 326 `{id,hash}` rows with match flags |
| `scripts/pass_next.py` / `NEXT.txt` | resume range (chunk range, `.text` range, commands) from `state.json.next_chunk` + the `--max` cap; `NEXT.txt` is its generated output — read it, never hand-edit |
| `scripts/pass_measure.py` / `ranges/*.md` | canonical per-pass measurement (block quoted verbatim in records or `--json` digest cited; `max refs:` = automatic crossref of the range max; `largest (text)` vs `sum_size (binary)`) / per-pass records — the evidence base |
| `scripts/gap_report.py` | per-range gap classes (`giant`/`offcut`/`hole`; `--offcuts` = corpus sweep) + `window reach:` far-window watch list (ledger 53) |
| `rdata_names.tsv` / `scripts/rdata_names.py` | plaintext `.rdata` strings (16,832 rows) / regenerator; query via `strlookup.py --pool rdata_names.tsv` |

## Coverage

Corpus: 2,228 chunks, 119,757 functions, 42,864,695 B `.text`. Passes 1–22 archived in
`CODE_MAP_ARCHIVE.md`; `state.json` is the truth for cumulative numbers; pending range is `NEXT.txt`.

| pass | chunks | `.text` range | functions | record |
|---|---|---|---|---|
| 23–33 | `0193`–`0306` | `0x1404192e0`–`0x14069b460` | 5,537 | `ranges/` rows 23–33 (archived detail) |
| 34–38 | `0307`–`0359` | `0x14069bb80`–`0x1407a2800` | 1,563 | `ranges/0x14069bb80-…` … `0x140785e30-…` |
| 39 (8-chunk) | `0360`–`0367` | `0x1407a28c0`–`0x1407cc6a0` | 468 | `ranges/0x1407a28c0-0x1407cc6a0.md` |
| 40 (8-chunk) | `0368`–`0375` | `0x1407cce30`–`0x1407f68b0` | 611 | `ranges/0x1407cce30-0x1407f68b0.md` |
| **total** | **375, contiguous** | `0x140001000`–`0x1407f68b0` | **22,002** | machine-verified (`state.json`) |

Machine-verified (`state.json` after pass 40): files 22,002 (18.37 %), Σ `size=` 6,043,772
(14.12 %); classes reg 7,956 / wrapper 1,954 / builder 1,717 / sorted 280 / atexit 261 /
record 326 / other **9,508**; 7,956 distinct ciphertext registrations + 4 plaintext rows
(one hash ×2 — Corrections 16); `d4f30` 1,188 / `d4f70` 1,350 / `d4fb0` 4,492 / `c2d70`
4,212 / `c2d50` 326 / `c7880` 261 / `atexit` 315; records 326. Passes 27–40 = consumer
only, zero registration (fourteen consecutive).

## Corrections ledger (machine-derived; supersedes prose in older records)
5. **`--update` is forward-only; `--init` wipes the pass list.** `--update` over a counted range double-counts and rewinds `next_chunk`; repair is `--init`.
7. **`pass_measure.py` prints no `ciphertext band:` line** — its `CTXT` regex needs `DAT_1438` + 6 hex digits; the band is now `0x1439a…`–`0x143b…`. Ciphertext extremes are read from the text, both addresses cited.
8. **`zones:` filter** prints only class `reg`/`record` runs with `cnt>=3`; 1–2-function builder/wrapper runs are absent from the skeleton.
13. **Allocator symbol ≠ allocator** — key on the shape; container allocator is `func_0x141c23490(&PTR_PTR_143a01d18,size[,align])` + free `func_0x000140578190`.
15. **Minimum registered size is 3** (`FUN_1404aad50`); span 3–0x3bc0. 20. **Decompiler fabrications:** `0x826eb8xx`, `0xca334801`, `0x38046856305b946b`, `0x0a13cb7c…`, `0x09e1c148…`, `func_0x000102d05da9`/`func_0x00010161e575` — never add to a band table.
22. **2-entry vtables at `0x140556eb3`/`FUN_14057ad20/57b2c0/57e220`; both arms known.** 23. **`files=` counts functions, not chunks.**
24. **The corpus is missing functions** (pass 29: 113 gaps / 81,067 B). Record gaps, never assume padding. 27. **`0x14384b7b0–b7bc` are plaintext floats on an XOR-8 page** — pages are not homogeneous.
30. **`sum_size` is not coverage** — quote the address range and count gaps from headers. 31. **Pass 30: 332 alignment + 142 under-reported + 12 × >1 KiB = 48,640 B un-decompiled.**
32. **Hash families:** D `(k0+k1)`-style double-mix `-0xae502812aa7333/-0x3b314601e57a13ad`; E descending buckets; **pass 40 adds three D variants** (GUID-pair-sum rehash `FUN_1407da2d0`, FNV-string `FUN_1407da500`, inline 16-byte FNV-1a `FUN_1407da6c0`).
33. **Match-queue error enum 0–12** = `UserRequest … Invalid` (`FUN_1405ddb40`). 34. **Event-name table `0x143851c90` is `.data`, pointer-shaped/encoded** — not inline names.
36. **Masked chains coexist** (component decode `0x4d79452d…` heaviest; per-session type table `(x+0x3fa981c8e7192fa6) ror31 ^ 0x8784b4333a580288 → ror23 + 0x37a9e6a2eedd5214 + type*8`; per-frame handle `(p^0x73cc01350b9bc072)+0x704e4dbd364c5bd3 >> 0x26 | 0x4000000`; store row `0xba397115a070ffa9+0x4094aaa9c7911a89`; service roots `0x622b95327b2e6d1e ^ 0xd6c0ac78d0e44481`, `0x1439aef88/e08/028` (+`0xb2485ad1cf871d2c ^ 0x89d3e0b8c0994abf + 0x820b88e340ab6eb0`); pass 37/39 chains; **pass 40 adds** the group-svc post `(svc+0x3c3b9d672a4416a4)^0xf9798462dc0addd7`, the roster slot-0 `+0x37a9e6a2eedd545c` (no `+type*8`), the summary slot table `+0x37a9e6a2eedd5614`, the layout chain `0x4c5f671fd43f24d6`, and the present gate `(x+0xb441a9797379a3c4)^0x4d06fcd25c0c008e ≠ 0x93c55e9cc7a8c196` (pass-37 `0x60e93ab59bc621f8` sibling).
39. **Overlapping decompilation windows** (pass 33/35/47/49 class); treat giant duplicates as one cascade each. 41. **Per-frame handle rows 16 B `{u32 handle,u32 pad,u64 entity_ptr}`.**
43. **Gap totals are hand-computed as distances** — always re-run `gap_report.py` before quoting. 44. **Pass 34: 4 real holes / 11,844 B.**
45. **`FUN_1406232f0` is the replay/demo frame reader too** — replay format IS the entity bitstream. 46. **`FUN_1406b7500` ×211** canonical open-chaining table grow (16-B rows) + twin `FUN_140727340`.
47. **Window chunks: `size=` can be ~50× smaller than chunk text** (`FUN_14074d1e0` class; `chunk_bytes/size= > 20` ⇒ window chunk). Far-window stamps are unread-region pointers, never coverage; `window reach:` line is generated.
48. **Corpus maxima were range maxima** — `--maxscan` ranks: `FUN_142b567b0` 571,552 B > `FUN_1423add80` 414,426 > `FUN_142b4e520` 398,819 > `FUN_140a17da0` 345,153; a NEW max is a claim until `max refs:` shows no second namer.
49. **Pass 35's 223,308-B `FUN_1407174e0` is one decompilation window**; its 24 >1 KiB "gaps" are real bodies; 6 corpus holes / 18,531 B. 50. **Second JSON parser** (rapidjson-style `FUN_140612090` + DOM verify `FUN_1422ee440`; errors 1–0x11 in `FUN_140734260`, second site `FUN_140778120`) — distinct from the pass-32 text engine.
51. **`FUN_14099xxxx` is the store's platform/purchase API** (confirmed pass 35; `FUN_140993710` product lookup now CALLED from pass-40's roster build `FUN_1407d36c0` — consumer side confirmed, bodies still unread).
52. **Resume range and measurement provenance are generated** — `NEXT.txt` from `pass_next.py`, `--json` digest for records; `max refs:` auto-crossrefs.
53. **Window chunks + `window reach:`** — see 47; pass-37/38 window-cache giant set treated as one cascade each.
54. **UI-window cache** `_DAT_143b795a0/a8/b0` + `0x2d1d7705`-family hash, binary-searched by giants (prologue) and walked by dtors (`0xfd749dd6ef1fd0d4` tail) — treat namers as the same construct.
55. **Pass 39: first window-free, zero-gap consumer pass; XOR-8 carries ASCII code constants** (Battle.net product band `0x14385c898`–`0x14385c9b4`). **Pass 40 extends the readable bands decisively** — ruleset enum `0x14385cdd8`–`0x14385cf68` (16 names), result enums `0x14385cfc0`–`0x14385d080` (match-join, 8) and `0x14385d0c0`–`0x14385d160` (code-redemption, 6), formats `'%x'/',%x'` `0x14385cb48/cb58`, render descriptors `0x14385cbe8`/`0x14385d180`, `PTR_DAT` ladders `0x14385cf80–cfb0`/`0x14385d098–d0b8`.
56. **Retyping a measure block is a transcription hazard — and so is anchoring on the previous
record's block.** Pass 40's quote re-keyed two lines (zone 6 `x87` vs correct `x78`;
zero-padded header `0368-0375` vs `368-375`) and inherited a phantom `1426c3d40 x33/x34`
token from the pass-39 record's calls line that the script does not print (`canary x%d`
already displays that count). All three caught by diffing the record quote against a saved
copy of the current script output. Quote by paste from a saved run, diff record-vs-output
before committing, and never treat an older record's block as the format template.

**Closed/superseded (archive):** items 1–4, 6, 9–12, 14, 17–19, 21, 25, 28, 29, 35, 37, 38, 40, 42 — full text in `CODE_MAP_ARCHIVE.md` §Corrections archive.

## What the code is — cumulative synthesis (40 passes; evidence unless marked [inference])

`.text` is catalogued in entry-address order. After 375 chunks the cursor is at `0x1407f68b0`
(18.37 % of functions, 14.12 % of `.text`). Names printed `func_0x…` have **no decompiled body
in this dump** — registrar, decryptors `d4f30`/`d4f70`, writer `c2d50`, helpers `c2d70`/`c7880`,
the `0x140543xx0`/`0x1405674xx` decoder family, settings accessors, component getters, the hotfix
HTTP client, CSV iterator, pass-32 cipher `FUN_142454xxx`, the render tier `FUN_141ff40f0`/
`141ff44a0`/`142033480`/`142028370`/`142036530` (protocol now known from pass-40 consumers),
`FUN_141d11f60`/`FUN_141c4efa0` time/random, `func_0x0001407e5d00`/`5990` (slot maps), the
`0x140f49xxx`/`0x140f1exxx` families — as does `tls_callback_0`. **Six layers, in address order:**

1. **Library preamble** `0x140001000`–`0x140039fc0`: ISA-L/igzip inflate, NVAPI bootstrap + 53 wrappers.
2. **NVIDIA driver-loading shim** `0x14003a230`–`0x14003d330`: replacement `LoadLibrary` for `nv*.dll`.
3. **CRT/C++ static-init sea** `0x14003ffe0`–`0x1400fa760`: five generator templates (181-B magic-static ×2,451; 209-B locale ×354; 58-B event thunks ×284; 134-B XOR-40 ×61; 37-B `_onexit`).
4. **Typed registry machine** `0x1400fbcb0`–`0x14054ea50` (CLOSED): nine constructs (name buffers, registration, builder, copy wrapper, sorted-insert, `{id,hash}` ×326, nested-atexit, settings registrar, CompilerIDFilter).
5. **Runtime bootstrap + obfuscated dispatchers** `0x14053f6b0`–`0x14058200x`: PE entry, sig scanner, anti-tamper, masked-pointer layer.
6. **Engine runtime** `0x14054fea0`→ (passes 28–40, **OPEN**). Cumulative halves, newest first:
   **(40) match/join/redemption + hero-select + media/overlay tier** — the 0x90-B hero-select
   team-composition manager (0x250-B hero rows + 0xe8-B loadout sub-rows, 0x180-B name rows,
   400-B member rows, two team-full checks, event 0x4d); the 0xac8-B match event logger
   (0x68-B typed rows 0–6, pause/match history); the 0x58-B match-history list (real import
   + `"TEST_MATCH_%zu"` synthetic generator with random entity picks); the 16-name ruleset
   mappers `FUN_1407f0c00/f1370`; the result-enum summary builders `FUN_1407f2660` (redeem)
   /`FUN_1407f2a00` (join) with a presence-bitmask wire object; the media/render rows 0xf0-B
   (`FUN_141ff40f0` create / `FUN_141ff44a0` destroy / `FUN_1407e0c30` present /
   `FUN_1407f4ad0` layout solver — thread-28 protocol read from consumers); the
   0x1738-B generational-handle manager (0x2000 slots, 16-bit generations); the roster tier
   (hash-D core, 0x10a8-B roster manager, GUID pin/unpin, 0x360-B GUID-table object,
   `FUN_140993710` license read); the 0x460-B social manager + 0x98-B range-gated kill feed;
   (39) party/group/voice/chat client (session object 0x14f8 B, spawn solver, chat dispatch,
   social/group managers, channel parser, party slot engine, product-code table);
   (38) UI-window engine room (window-cache giants, springs, trails, descriptor unpack);
   (37) map/scene lifecycle, live-ops feed, capability manager, 0x18a0-B hero record, UI windows;
   (36) store purchase/VC completion, telemetry, SAPI/Steam, effect/impulse engine;
   (35) social + monetization (StoreSystem_C, stats/sabotage); (34) replay/highlight/cinematic;
   (33) presentation (VFX, widget binding); (32) live gameplay loop (event bus, entity runtime,
   match flow, JSON text engine); (31) match-lifecycle receive; (28–30) infra (~150-subsystem
   app composition, containers, cvars, chat/voice, hotfix, workers, HUD, spatial runtime,
   bitstream, CSV, Steam/XInput).
   [inference: `0x14054fea0` marks the end of data registration and the start of behaviour.]

**Layer 6 construct index (per-pass detail + addresses in the records):** *infra* (28–30),
*match receive* (31: bitstream ×341/×248, dispatcher, saved-match, JSON serializer), *gameplay
loop* (32: event bus, entity runtime, connection state, master tick, world-to-screen, JSON
text engine), *presentation/social* (33: VFX engine, 0x18a0-B record, widget binding),
*replay/cinematic* (34: demo system, sequence machine, chat/Markdown, hash-grow ×211),
*store/social* (35: StoreSystem_C 0x390 B, ruleset enum ids, stat layer), *store completion*
(36: `__PlaceOrderWithVirtualCurrency`, perf schema, SAPI, hot-plug), *map/live-ops* (37:
12-state load machine, patch-note client, capability trio), *UI engine* (38: window cache,
springs, descriptor unpack `FUN_140798f80`), *party tier* (39: session 0x14f8 B, spawn
solver, word-list filter, slot engine, product codes), *match/media tier* (40: hero-select
manager `FUN_1407e1e40`-family, event logger `FUN_1407ea990`, match-history
`FUN_1407ed2e0`/`ee060`, result builders `FUN_1407f2660/2a00`, media rows
`FUN_1407dfdd0`/`1407f4c70` + layout `FUN_1407f4ad0`, generational handles
`FUN_1407dd910/9c0/a70`, roster `FUN_1407ce150`/`1407d4b00`, kill feed `FUN_1407dac50`/
`db590`/`db710`, 0x318-B group manager `FUN_1407e8ed0`, 0x6f8-B factory
`FUN_1407d6310`).

**Where the data lives** (full table in the archive; live additions):

| band | content |
|---|---|
| `0x143848d40`–`0x14385d178` | XOR-8 name/payload ciphertext, extending pass by pass: settings/logger/hotfix/cvar names (≤ pass 35), UI/dialogue (33–34), party/store (35–36), map/live-ops (37), widget clones (38), product codes (39), and **pass 40**: expiry formats `0x14385cb48/cb58`, ruleset names `0x14385cdd8`–`0x14385cf68`, match-join result `0x14385cfc0`–`0x14385d080`, redeem result `0x14385d0c0`–`0x14385d160`, render descriptors `0x14385cbe8`/`0x14385d180`, `PTR_DAT` ladders `0x14385cf80–cfb0`/`d098–d0b8`, 8-entry listener table `DAT_14385cc30` |
| `0x1438b8e50`–`0x1439fa330` | registry ciphertext; triplet-stub page |
| `0x143a155xx`–`0x143b81a0x` | XOR-40 keys, settings names, runtime block (~250 feature flags `0x143b945b8–0x143b9c5c0`), **pass 40: settings/observer block `0x143b90c30–0x143b90ea8`** |
| `0x143cf0000`+ | RTTI, reg outputs, settings descriptors, config globals; **pass 40: null-match GUID `0x143b83da0–dc`, default-GUID pair `0x1442a31d0–dc`** |
| `0x1441e18f0`+ | plaintext reg outputs, struct schemas, record pools; **pass 40: TLS RNG base `0x144180fa0` (0xe0-stride states), time scale `0x14415f7c8/f7f8`** |

**What it is for.** Layers 1–2 are a vendored NVIDIA/igzip preamble; layer 3 compiled-in C++
static init; layer 4 registers ~8 k encrypted type names; layers 5–6 are the client —
settings, telemetry, schemas, chat/voice, hotfix, HUD, spatial/entity runtime, match receive,
gameplay loop, presentation, replay/cinematic, social/store, map-load, UI windows, party/
voice/chat (39), and now (40) the match/join/redemption summaries, the hero-select team
composer, the range-gated kill feed, and the media/overlay render lifecycle. No plaintext
game protocol (entity traffic is the bitstream; replays reuse it); the render device is
`FUN_141ff40f0` with its lifecycle now mapped; gameplay *rules* remain ahead.
Confidence: counts/shapes/bands measured; construct labels are shape-based inference;
obfuscated bodies read structurally only.

**Known limits.** (a) `func_0x…` bodies absent (see synthesis list; offcuts: `0x14068xxxx`
(33), `FUN_141da/141db` emitters (33), `FUN_14099xxxx` store API (35), `FUN_140d1xxxx` sound
(36), render tier (37→protocol known 40), `0x140f49xxx`/`0x140f1exxx` (40)). (b) XOR-8 keys
are per-record salts. (c) `0x142f0…`–`0x142f2b…` thunks absent. (d) Corpus gaps: pass 30's
12 × >1 KiB; pass 34: 4 holes / 11,844 B; pass 35: 6 / 18,531 B; pass 36: 2 / 6,068 B;
pass 37–39: 0 holes; **pass 40: 1 hole / 1,033 B (`0x1407efae0→0x1407eff20`)** — first since
ledger 44. (e) Window chunks per ledgers 39/47/49/53: pass-37/38 window-cache giant set =
one cascade each; **pass 40's range max `FUN_1407f5710` (ratio ~34) is a window chunk** —
one present/update body, not 34× coverage.

## Cross-cutting conventions (one line each; per-pass deltas in the records)

| convention | rule | first seen |
|---|---|---|
| TLS guard + 181-B descriptor | `*(TLS+0x50) < epoch` → init/footer; descriptor ×2,451 | `0x140001000` |
| Registry primitives | XOR-40/XOR-8 decryptors; `{id,hash}` ×326; builder row `{+0x20 root,+0x28 inst,+0x30 0,+0x98 1,+0x9c 0}`; canary `d4f30/d4f70` builders only; nested-atexit 261 | `0x1400fbf70` |
| Layer-4 rows | catch descriptor 181-B ×272; triplet stub 66-B; component ids 1–0x19; struct schema `{&name,off,size}`; metric `func_0x000141d23660` | `0x1404f8720` |
| Masked ptr + sig scan | masked pointer → `func_0x140543xx0` → `^ *(u64*)(_DAT_143b79598+n)`; overlapping-instruction dispatchers; patch record `0x143b79640` | `0x14053f9a0` |
| App object + settings | app `_DAT_143b7f410`; ~150 children; XOR-8 settings via `FUN_141c295b0`-family | `0x140554220` |
| Logger/hash/handles | per-site logger; hash A/B/C; handle table 0xfff buckets; **pass 40: generational 0x2000-slot table `FUN_1407dd9c0` + mint `FUN_1407dd910` (third handle construct)** | `0x1405601c0` |
| Containers | allocator `func_0x141c23490`/free `func_0x000140578190`; worker pool; hash-D (five variants, ledger 32/40) | `0x140558120` |
| Hotfix/components/spatial | 0x30-B hotfix record → SHA-256; component access `func_0x140c503d0`; spatial ray | `0x14056cd40` |
| Cvar/HUD/bitstream | cvar registrar 3-copy; reader `FUN_1406232f0`/writer `FUN_1406264c0`; replay = bitstream | `0x140596b00` |
| Hash C + dispatchers | `h=(k*0x200000+~k)…& (cap-1)`; `(**(*disp+0x10))(disp,fn,id,0)` | `0x140599970` |
| Net/cipher/JSON (32) | 0x22-bit header; cipher `FUN_142454xxx`; JSON `FUN_140673120`; `"--name {json}"` | `0x140654c50` |
| Entity/VFX/widgets (33) | record 0x18a0 B; VFX `FUN_140681360`; JSON→widget `FUN_141940ef0` | `0x140687fe0` |
| Replay/chat (34) | demo magic `0x7495174655b5d763`; Markdown escaper; hash-grow ×211 | `0x1406a7b40` |
| Party/store (35–36) | member rows; ruleset ids; `__PlaceOrderWithVirtualCurrency`; hosts us/eu/kr | `0x1406c7b50` |
| Telemetry/voice (36) | FNV change-hash; perf-counter schema; SAPI; screenshots | `0x140738d00` |
| Map/live-ops/UI (37–38) | 12-state load machine; Mongo feed queries; window-cache giants; spring `FUN_140784fd0` | `0x1407691f0` |
| Party client (39) | session 0x14f8 B; spawn solver `FUN_1407a8a70`; slot engine `FUN_1407c9480` | `0x1407a28c0` |
| **Event post (40)** | `func_0x000140c28eb0(_DAT_143b7f410)` or group svc `(svc+0x3c3b9d672a4416a4)^0xf9798462dc0addd7` → `(**vt+0x18)(svc,id)`, ids 0x22–0x54 (~60 sites/pass); the app-service event bus convention | `0x1407d06a0` |
| **Retire idiom (34→40)** | `0x20000`-flag guard + `(**vt+0x158)/200/0x160` + `FUN_1421522e0`/`func_0x00014214eb70`/`FUN_14214d400` + `+0x914` sentinel; also fully inlined in obfuscated giants | `0x1406xxxx` |

## Open threads (cheapest next query each; check/update every pass)

2. **0x19c-B/entity transport framing** — client framing found (32); socket layer still ahead.
5. **Command ids** — base `0x48/0x53/0x7c/0x7d/0xa5/0xb2/0x3a`; grown 32–37; **pass 40 adds the event-post id set 0x22–0x54** (see conventions).
7. **`FUN_141c295b0`/`FUN_141c58170`/`FUN_142d2cf30` bodies** — unread (~chunk `15xx`).
9. **`0x143b945b8`–`0x143b9c5c0` flags** — grep readers forward.
11. **Channel list renderer** — writer found (32), renderer unfound. 12. **Hotfix record dump** — `_DAT_1439d98c0`.
13. **Gaps** — pass 40: 1 hole / 1,033 B (`0x1407efae0→0x1407eff20`, T40-6); `0x14059a007–0x14059c350` (9,033 B) and `0x1401a4e02–0x1401abad0` (27,854 B) still open.
15. **Event-name table `0x143851c90`** — still encoded. 16. **Pass-32/33/34 machinery bodies** — cipher, event-hash, emitters, anim samplers.
17. **Handle-table writers** — grep `0x18317a531d116c`; pass 40 adds the generational table readers (conventions).
18. **`FUN_14099xxxx` store API** — consumer confirmed twice (35, 40 `FUN_1407d36c0`→`FUN_140993710`); bodies unread.
19. **Widget/enum pages** — name bands extend to `0x14385beb0` (all 'Unknown'); pool-side decode pending (T38-1).
21. **Store endpoint labels** — decode `0x1438595b0–0x1438597c8`. 22. **`FUN_140d1xxxx` sound assets** — `crossref.py 140d1bcc0`. 23. **Audio-channel ids** — `crossref.py 142044960`.
24. **`0x8784b4333a5802xx` masked chain** — `strlookup --band 0x1439dc5c0 0x1439dc630`.
25. **Component-message ids** — `0xd8…`/`0x5800…`/`0xde…`/`0x46…` families; grep forward.
26–30. Widget names / UI-cache tables / render tier (**partially closed 40**: lifecycle mapped, bodies `FUN_141ff40f0`-family unread) / trail rows (closed 38) / live-ops flags.
31–35. Widget-name band decode / material family `crossref.py 142cb4c20` / `FUN_140c6xxxx` input / `FUN_1409bxxxx` appliers / `0xbd` input rows.
36–40. `0x142f2df90` fn-ptr table / `FUN_1407b0e90` stat fold / 18-key channel ladder / toast table `0x143059b80` / `0x14213f7df` far-window region (23 more stamps from `FUN_1407f5710` this pass; sweep when `window reach:` names it).
41. **T40-1 result-summary serializer** — presence bitmask `+0x30`, type tag `+0x58`; who serializes it? `crossref.py 1407f2a00`.
42. **T40-2 `FUN_141d11f60`/`FUN_141c4efa0`** time/random sources behind the event logger. `crossref.py 141d11f60`.
43. **T40-3 `0x143b90c30–ea8` settings/observer block** — commit/rollback `FUN_1407cf220/f3c0`; dump observers.
44. **T40-4 `0x140f49xxx` context family** (`FUN_140f49550/500`, `0x140f1e990/ee20`). `crossref.py 140f49550`.
45. **T40-5 media render descriptors** — decode `0x14385cbe0–0x14385d190` (XOR-8, strscan names headers only).
46. **T40-6 the pass-40 hole** `0x1407efae0→0x1407eff20` — `gap_report.py 368 375 --offcuts` when neighbours gain mentions.
47. **T40-7 `func_0x0001407e5d00`/`func_0x0001407e5990`** — GUID hash + team-full checks, no bodies; grep forward.

CLOSED (machine): fd9670 recount; provenance; `0x1411b8070`; thread 43; T20 (`max refs:`);
JSON writer/parser/CSV (31/32); XOR-8 salt keys; presence-failure events; ledgers 1–4, 6,
9–12, 14, 17–21, 25, 28–29, 35, 37–38, 40 (archive). Pass 36 closes T35-1/T35-3; 37 closes
T36-3 partially + pass-36 (a); 38 closes T37-4 + pass-37 (a); 39 closes T38-1 negatively-
positively + pass-38 (e); **pass 40 reads T37-3's render lifecycle from the consumer side
(four `FUN_141ff40f0`-family call sites with create/attach/present/destroy protocol).**

## Next pass

Resume range: **`NEXT.txt`** — written by `python scripts/pass_next.py` from `state.json` +
`--max`; regenerate after every `--update`, never hand-edit. Pass 40 ends at `FUN_1407f68b0`
(ptr-array bulk append + retire walk, the second media-object list manager); engine-runtime
stratum `0x14054fea0` OPEN. Run `pass_measure.py 376 384`, quote the block or cite its
`--json` digest, run `--update`, refresh `NEXT.txt` and this file. Watch for: (a) **match/
media-tier continuation** — the resume range starts at `0x1407f6a30`, right past the media
manager; expect the `FUN_1407f4c70`-family siblings and more `FUN_141ff40f0` consumers;
(b) the **`func_0x0001407e5d00`/`5990` bodies** (T40-7) may land in-range; (c) the
**`FUN_14099xxxx` store API** (thread 18) — now ~2.2 MB of `.text` ahead; (d) the
**`0x14213f7df` far-window region** (32+23 stamps from two passes; sweep for the defining
chunk when `window reach:` names it); (e) whether the match/hero-select tier gives way to a
new subsystem past `0x14081d3e0` (the NEXT.txt range end). Do not re-run a counted range
through `--update` (ledger 5); no ciphertext script line (ledger 7); never treat
`0x826e…`/`0xca334801`/`0x4343ffa4`-family or offcut-call addresses as data (ledger 20);
ledgers 24/31/39/43/44/47/49/53/54/55 for gaps; `size=` is not coverage (ledger 30);
overlapping windows per ledgers 39/47/49 — **paste, never re-type, the measure block
(ledger 56)**, and check the zone counts sum to `files=`.
