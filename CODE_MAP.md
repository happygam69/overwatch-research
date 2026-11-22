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
| 41 (9-chunk) | `0376`–`0384` | `0x1407f6a30`–`0x14081d3e0` | 531 | `ranges/0x1407f6a30-0x14081d3e0.md` |
| 42 (10-chunk) | `0385`–`0394` | `0x14081d520`–`0x1408493b0` | 566 | `ranges/0x14081d520-0x1408493b0.md` |
| **total** | **394, contiguous** | `0x140001000`–`0x1408493b0` | **23,099** | machine-verified (`state.json`) |

Machine-verified (`state.json` after pass 42): files 23,099 (19.29 %), Σ `size=` 6,328,321
(14.76 %); classes reg 7,956 / wrapper 1,954 / builder 1,717 / sorted 280 / atexit 261 /
record 326 / other **10,605**; 7,956 distinct ciphertext registrations + 4 plaintext rows
(one hash ×2 — Corrections 16); `d4f30` 1,188 / `d4f70` 1,350 / `d4fb0` 4,492 / `c2d70`
4,212 / `c2d50` 326 / `c7880` 261 / `atexit` 315; records 326. Passes 27–42 = consumer
only, zero registration (sixteen consecutive).

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
36. **Masked chains coexist** (component decode `0x4d79452d…` heaviest; per-session type table `(x+0x3fa981c8e7192fa6) ror31 ^ 0x8784b4333a580288 → ror23 + 0x37a9e6a2eedd5214 + type*8`; per-frame handle `(p^0x73cc01350b9bc072)+0x704e4dbd364c5bd3 >> 0x26 | 0x4000000`; store row `0xba397115a070ffa9+0x4094aaa9c7911a89`; service roots `0x622b95327b2e6d1e ^ 0xd6c0ac78d0e44481`, `0x1439aef88/e08/028` (+`0xb2485ad1cf871d2c ^ 0x89d3e0b8c0994abf + 0x820b88e340ab6eb0`); pass 37–41 chains in the records). **Pass 42: the type table is the dominant resolve (~150 sites, 25 fetchers), and the store-row chain gains the sorted-table cache variant** (conventions: name-window triple-mix).
39. **Overlapping decompilation windows** (pass 33/35/47/49 class); treat giant duplicates as one cascade each. 41. **Per-frame handle rows 16 B `{u32 handle,u32 pad,u64 entity_ptr}`.**
43. **Gap totals are hand-computed as distances** — always re-run `gap_report.py` before quoting. 44. **Pass 34: 4 real holes / 11,844 B.**
45. **`FUN_1406232f0` is the replay/demo frame reader too** — replay format IS the bitstream. 46. **`FUN_1406b7500` ×211** canonical open-chaining table grow + twin `FUN_140727340`.
47. **Window chunks: `size=` can be ~50× smaller than chunk text** (`FUN_14074d1e0` class; `chunk_bytes/size= > 20` ⇒ window chunk). Far-window stamps are unread-region pointers, never coverage; `window reach:` line is generated.
48. **Corpus maxima were range maxima** — `--maxscan` ranks: `FUN_142b567b0` 571,552 B > `FUN_1423add80` 414,426 > `FUN_142b4e520` 398,819 > `FUN_140a17da0` 345,153; a NEW max is a claim until `max refs:` shows no second namer.
49. **Pass 35's 223,308-B `FUN_1407174e0` is one decompilation window**; its 24 >1 KiB "gaps" are real bodies; 6 corpus holes / 18,531 B. 50. **Second JSON parser** (rapidjson-style `FUN_140612090` + DOM verify `FUN_1422ee440`; errors 1–0x11 in `FUN_140734260`, second site `FUN_140778120`) — distinct from the pass-32 text engine.
51. **`FUN_14099xxxx` is the store's platform/purchase API** (confirmed pass 35; `FUN_140993710` product lookup now CALLED from pass-40's roster build `FUN_1407d36c0` — consumer side confirmed, bodies still unread).
52. **Resume range and measurement provenance are generated** — `NEXT.txt` from `pass_next.py`, `--json` digest for records; `max refs:` auto-crossrefs.
53. **Window chunks + `window reach:`** — see 47; pass-37/38 window-cache giant set treated as one cascade each.
54. **UI-window cache** `_DAT_143b795a0/a8/b0` + `0x2d1d7705`-family hash, binary-searched by giants (prologue) and walked by dtors (`0xfd749dd6ef1fd0d4` tail) — treat namers as the same construct.
55. **XOR-8 carries ASCII code constants** (pass-39 Battle.net band `0x14385c898`–`0x14385c9b4`; pass-40 ruleset/result enums to `0x14385d180`).
56. **Retyping a measure block is a transcription hazard — and so is anchoring on the previous
record's block.** Quote by paste from a saved run, diff record-vs-output before committing,
never treat an older record's block as the format template (pass-40 incident, full story in
the archive).
57. **Window families grow by cascade** — pass 41's `FUN_14080c740` set (114 KB, ratio ~27,
zero namers) and **pass 42's name-window family (`FUN_1408314b0`…`FUN_1408493b0`, shared
triple-mix, ratios to ~755, one far namer `FUN_140adcec0` chunk 0545) are the two largest;
treat per ledgers 39/49; `size=` there is meaningless.**

**Closed/superseded (archive):** items 1–4, 6, 9–12, 14, 17–19, 21, 25, 28, 29, 35, 37, 38, 40, 42 — full text in `CODE_MAP_ARCHIVE.md` §Corrections archive.

## What the code is — cumulative synthesis (42 passes; evidence unless marked [inference])

`.text` is catalogued in entry-address order. After 394 chunks the cursor is at `0x1408493b0`
(19.29 % of functions, 14.76 % of `.text`). Names printed `func_0x…` have **no decompiled body
in this dump** — registrar, decryptors `d4f30`/`d4f70`, writer `c2d50`, helpers `c2d70`/`c7880`,
the `0x140543xx0`/`0x1405674xx` decoder family, settings accessors, component getters, the hotfix
HTTP client, CSV iterator, pass-32 cipher `FUN_142454xxx`, the render tier `FUN_141ff40f0`/
`141ff44a0`/`142033480`/`142028370`/`142036530` (protocol now known from pass-40 consumers),
`FUN_141d11f60`/`FUN_141c4efa0` time/random, `func_0x0001407e5d00`/`5990` (slot maps), the
`0x140f49xxx`/`0x140f1exxx` families, the `0x140d2xxxx`/`0x140d5xxxx` ability-config bodies
(named pass 41, unread) — as does `tls_callback_0`. **Six layers, in address order:**

1. **Library preamble** `0x140001000`–`0x140039fc0`: ISA-L/igzip inflate, NVAPI bootstrap + 53 wrappers.
2. **NVIDIA driver-loading shim** `0x14003a230`–`0x14003d330`: replacement `LoadLibrary` for `nv*.dll`.
3. **CRT/C++ static-init sea** `0x14003ffe0`–`0x1400fa760`: five generator templates (181-B magic-static ×2,451; 209-B locale ×354; 58-B event thunks ×284; 134-B XOR-40 ×61; 37-B `_onexit`).
4. **Typed registry machine** `0x1400fbcb0`–`0x14054ea50` (CLOSED): nine constructs (name buffers, registration, builder, copy wrapper, sorted-insert, `{id,hash}` ×326, nested-atexit, settings registrar, CompilerIDFilter).
5. **Runtime bootstrap + obfuscated dispatchers** `0x14053f6b0`–`0x14058200x`: PE entry, sig scanner, anti-tamper, masked-pointer layer.
6. **Engine runtime** `0x14054fea0`→ (passes 28–42, **OPEN**). Cumulative halves, newest first:
   **(42) lobby/match-state rules tier + voice client + player-name window family +
   hero-actor object** — the 5-slot HUD binding object (generational-handle banks,
   rebind engine, entity-colour pack); the **voice chat client** ('VoiceClient'
   plaintext band, device ring queue, worker pump, 18-id audio-cvar set); the
   **lobby rules** (~200 fns: hero GUID sets, team/colour enum tables, permission
   lattice, seven 0xd0-stride hero-record banks, map/mode enum + queue bands); the
   **player-name window family** (`FUN_1408314b0`…`FUN_1408493b0`, shared
   `^0xeb+0x2d1d7705` triple-mix, range max 45 KB ratio ~755, far namer
   `FUN_140adcec0` chunk 0545); the **0x4b0-B hero-actor object** (event-text
   queue, factory-store cache `DAT_143b943a0`); the **status-effect store**
   (0x58-stride GUID rows, `0x140bfxxxx` row API); the **scoreboard enumerator**
   (global player arrays + `DAT_143b945b0/b4` spinlock); and the **gameplay-rule
   summary window giant `FUN_1408493b0`** (25-field id set, 23-member
   `0x1421exxx` list API, 144 stamps into `0x140867cd6`);
   (41) hero ability/weapon/stat system + widget-factory belt + entity-view/HUD tier —
   the 0x2a10-B hero entity (six 0x110-stride ability slots, 0x50-B charge rows,
   ~2000-case stat getter `FUN_1408038e0`, cooldown tick `FUN_140804070`,
   charge/apply pair `FUN_1408045f0/1408050d0`); the **114-K window family**
   `FUN_14080c740`-set (0x2d1d7705 probe + 0x18-stride modifier ladder +
   0x110-stride ability-row serializer); the 62-call factory registrar
   `FUN_141c4b050` (sizes 0x18–0x31868); the sound pair `FUN_1407ff5c0/1407ffc50`
   (T23 consumer-side); the 0x3b60-B entity-view object + tracked-participant tier
   (retire walk ~10 sites);
   (40) match/join/redemption + hero-select + media/overlay tier; (39) party/group/
   voice/chat client; (38) UI-window engine room; (37) map/scene lifecycle, live-ops
   feed, capability manager, 0x18a0-B hero record, UI windows; (36) store purchase/VC
   completion, telemetry, SAPI/Steam, effect/impulse engine; (35) social + monetization
   (StoreSystem_C, stats/sabotage); (34) replay/highlight/cinematic; (33) presentation
   (VFX, widget binding); (32) live gameplay loop (event bus, entity runtime, match
   flow, JSON text engine); (31) match-lifecycle receive; (28–30) infra (~150-subsystem
   app composition, containers, cvars, chat/voice, hotfix, workers, HUD, spatial
   runtime, bitstream, CSV, Steam/XInput).
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
`FUN_1407d6310`), *lobby/rules tier* (42: HUD binding `FUN_14081dfe0`, voice client `FUN_140837fa0`,
  lobby rules `FUN_140827790`-set, name windows `FUN_1408446e0`-family, hero actor
  `FUN_14083f2c0`, effects `FUN_1408464a0`, summary writer `FUN_1408493b0`); *hero-ability tier* (41: hero entity `FUN_140802620/2660` +
dtor `FUN_140809280`, stat getter `FUN_1408038e0/ed0`, tick `FUN_140804070`,
charge/apply `FUN_1408045f0/1408050d0`, cast broadcast `FUN_14080a730`,
window family `FUN_14080c740`-set, stat fold `FUN_14080d850`, screens
`FUN_140808f30/140811f10/140813510/140816540/1408168c0`, sound pair
`FUN_1407ff5c0/1407ffc50`, entity-view `FUN_140818260/14081a3b0/140819290`).

**Where the data lives** (full table in the archive; live additions):

| band | content |
|---|---|
| `0x143848d40`–`0x14385ddf0` | XOR-8 name/payload ciphertext, extending pass by pass (settings/UI/party/store/map/widget names ≤ 41; pass 41's 'Unknown' factory belt `0x14385d1a0`–`0x14385ddf0`, 122 pages, pool-side decode pending T19/T41-1) — **pass 42 adds the voice/device band `0x14385f158`–`0x14385f348` ('VoiceClient', device names, colour config; decoded in place) and the `'{0}'` roster formats `0x143864F90/FA0`** |
| `0x1438b8e50`–`0x1439fa330` | registry ciphertext; triplet-stub page |
| `0x143a155xx`–`0x143b81a0x` | XOR-40 keys, settings names, runtime block (~250 feature flags `0x143b945b8–0x143b9c5c0`), **pass 40: settings/observer block `0x143b90c30–0x143b90ea8`** |
| `0x143cf0000`+ | RTTI, reg outputs, settings descriptors, config globals; **pass 40: null-match GUID `0x143b83da0–dc`, default-GUID pair `0x1442a31d0–dc`** |
| `0x1441e18f0`+ | plaintext reg outputs, struct schemas, record pools; **pass 40: TLS RNG base `0x144180fa0` (0xe0-stride states), time scale `0x14415f7c8/f7f8`** |

**What it is for.** Layers 1–2 are a vendored NVIDIA/igzip preamble; layer 3 compiled-in C++
static init; layer 4 registers ~8 k encrypted type names; layers 5–6 are the client —
settings, telemetry, schemas, chat/voice, hotfix, HUD, spatial/entity runtime, match receive,
gameplay loop, presentation, replay/cinematic, social/store, map-load, UI windows, party/
voice/chat (39), match/join/redemption summaries + hero-select + media lifecycle (40),
the hero ability/weapon/stat system (41), and now (42) **the lobby/match-state
rules tier + the voice chat client** — HUD slot binding, the 'VoiceClient'
subsystem, the ~200-fn rule set over seven hero-record banks, the player-name
window family, the hero-actor object with its effect store, and the summary
writer. No plaintext game protocol (entity traffic is the bitstream; replays
reuse it);
the render device is `FUN_141ff40f0` with its lifecycle mapped; gameplay rules are **now
being read** (ability config lives in the `0x140d2xxxx`/`0x140d5xxxx` offcut bodies).
Confidence: counts/shapes/bands measured; construct labels are shape-based inference;
obfuscated bodies read structurally only.

**Known limits.** (a) `func_0x…` bodies absent (see synthesis list; offcuts: `0x14068xxxx`
(33), `FUN_141da/141db` emitters (33), `FUN_14099xxxx` store API (35, now 3 consumer sites),
`FUN_140d1xxxx` sound (36), render tier (37→protocol known 40), `0x140f49xxx`/`0x140f1exxx`
(40), `0x140d2xxxx`/`0x140d5xxxx` ability-config family (41 — named from the hero tier,
bodies unread), **`0x140bfxxxx` hero-record row API (42 — named from the effect store,
bodies unread; `crossref.py 140bf36c0`)**). (b) XOR-8 keys
are per-record salts. (c) `0x142f0…`–`0x142f2b…` thunks absent. (d) Corpus gaps: pass 30's
12 × >1 KiB; pass 34: 4 holes / 11,844 B; pass 35: 6 / 18,531 B; pass 36: 2 / 6,068 B;
pass 37–39: 0 holes; pass 40: 1 hole / 1,033 B (`0x1407efae0→0x1407eff20`, T40-6);
pass 41: 0 holes; **pass 42: 1 hole / 8,015 B (`0x14083d280→0x14083f2c0`, T42-1 —
`--offcuts` pending)**. (e) Window chunks per ledgers 39/47/49/53: pass-37/38
window-cache giant set = one cascade each; pass-40 range max `FUN_1407f5710` (ratio ~34);
pass 41's `FUN_14080c740` set (ratio ~27, zero namers, 90 stamps at `0x141c4b29c`); the
**pass-42 name-window family (`FUN_1408314b0`…`FUN_1408493b0`, shared `^0xeb+
0x2d1d7705` triple-mix, ratios up to ~755, one far namer `FUN_140adcec0` chunk 0545)
is the largest window family yet — ledgers 49/57 extended (T42-4)**.

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
| **Retire idiom (34→41)** | `0x20000`-flag guard + `(**vt+0x158)/200/0x160` + `FUN_1421522e0`/`func_0x00014214eb70`/`FUN_14214d400` + `+0x914` sentinel; also fully inlined in obfuscated giants — **pass 41: ~10 verbatim copies in the participant tier, its highest density** | `0x1406xxxx` |
| **Widget factory (41)** | create-stub pair (`func_0x000141c4b270(param+0x10)` & `& 0x10` guard / plain create) + XOR-8 name page (0x18-stride name+key pair, 'Unknown' belt `0x14385d1a0+`) + `FUN_141c4b050(&desc,&name,0x14,size,0,id)` — 62 calls pass 41, sizes 0x18–0x31868 | `0x1407fd0a0` |
| **Entity-root chain (41)** | `(x+0x1e2421a4798a328>>0x22|x*0x40000000)^0xe1379e3cb308170d` → `>>0x2b|<<0x15` root, second stage `^0x254cd67c7af97e9f`; index via `func_0x000142043150/142001f80/c618a0/cac960` — the hero tier's component decode (66 hits pass 41), sibling of `0x4d79452d486f9431` | `0x140801400` |
| **Name-window triple-mix (42)** | `((x^0xeb)+0x2d1d7705)>>0xb|x*0x200000 ^ [0x143b79598+0xb5] ^ 0x998fae39` → `>>0x15|x<<0xb +0xd2e288fb ^ DAT_143847f0a`; sorted-table binary search + `0x4d79452d486f9431` root + `_DAT_143b795a8` LOCK-cache — the shared hash of the whole player-name window family (`FUN_1408314b0`…`FUN_1408493b0`, ~14 bodies) | `0x14082f100` |
| **List API `0x1421exxx` (42)** | 23-member family: `1421e40c0/5100/52c0/52a0/5310/5370` list ops + `1421e4620(int)/47b0(id)/41d0(bool)/4860(str)/4480(int)` typed setters + `1421e34a0/4f30/50b0/50c0` resolve — the summary writer's row model (`FUN_1408493b0`), writer twin of the pass-41 `0x140c88fd0` parser | `0x1408493b0` |
| **Player-list lock (42)** | `DAT_143b945b0` 0x400-spinlock (`FUN_141c5c3d0` escalate) + `DAT_143b945b4` disable flag over the three global arrays `PTR_DAT_14385f3b0/3f480/3f4f0` — the scoreboard's data source (T9's flag block, protocol read) | `0x140842fe0` |

## Open threads (cheapest next query each; check/update every pass)

2. **0x19c-B entity transport framing** — client framing found (32); socket layer ahead.
5. **Command ids** — base `0x48/0x53/0x7c/0x7d/0xa5/0xb2/0x3a`; grown 32–40; **pass 41 adds audio id 0x8d (T23, consumer-side) and ability-component ids 0x6b/0x655/0xf5/0x580/0x1e**.
7. **`FUN_141c295b0`/`FUN_141c58170`/`FUN_142d2cf30` bodies** — unread (~chunk `15xx`).
9. **`0x143b945b8`–`0x143b9c5c0` flags** — lock protocol read pass 42; writers pending.
11. **Channel list renderer** — writer found (32), renderer unfound. 12. **Hotfix record dump** — `_DAT_1439d98c0`.
13. **Gaps** — pass 42: 1 hole / 8,015 B (T42-1); pass-40 T40-6 hole; `0x14059a007–0x14059c350` (9,033 B), `0x1401a4e02–0x1401abad0` (27,854 B) open.
15. **Event-name table `0x143851c90`** — still encoded. 16. **Pass-32–34 machinery bodies** — cipher, event-hash, emitters, samplers.
17. **Handle-table writers** — grep `0x18317a531d116c`; pass 40 adds the generational table readers (conventions).
18. **`FUN_14099xxxx` store API** — consumers 35/40 + **pass 41 `FUN_140804bc0`→`FUN_140996c60/140996c10`**; bodies unread.
19. **Widget/enum pages** — 'Unknown' belt now `0x14385d1a0`–`0x14385ddf0` (122 pages, pass 41); pool-side decode pending (T38-1/T41-1).
21. **Store endpoint labels** — decode `0x1438595b0–0x1438597c8`. 22. **`FUN_140d1xxxx` sound assets** — `crossref.py 140d1bcc0`. 23. **Audio-channel ids — partially closed 41** (`FUN_142044960(entity,0x8d,&v)` consumer read from `FUN_1407ffc50`); remaining: the id enum's full table.
24. **`0x8784b4333a5802xx` masked chain** — `strlookup --band 0x1439dc5c0 0x1439dc630`.
25. **Component-message ids** — `0xd8…`/`0x5800…`/`0xde…`/`0x46…` families; grep forward.
26–30. Widget names / UI-cache tables / render tier (**partially closed 40**: lifecycle mapped, bodies `FUN_141ff40f0`-family unread) / trail rows (closed 38) / live-ops flags.
31–35. Widget-name band decode / material family `crossref.py 142cb4c20` / `FUN_140c6xxxx` input / `FUN_1409bxxxx` appliers / `0xbd` input rows.
36–40. `0x142f2df90` fn-ptr table / `FUN_1407b0e90` stat fold / 18-key channel ladder / toast table `0x143059b80` / `0x14213f7df` far-window region (**27 more stamps pass 41** from `FUN_1408100f0`; plus new regions `0x142045667` ×5 and `0x141c4b29c` ×90 — sweep when `window reach:` names a defining chunk).
41. **T40-1 result-summary serializer** — presence bitmask `+0x30`, type tag `+0x58`; who serializes it? `crossref.py 1407f2a00`.
42. **T40-2 `FUN_141d11f60`/`FUN_141c4efa0`** time/random sources behind the event logger. `crossref.py 141d11f60`.
43. **T40-3 `0x143b90c30–ea8` settings/observer block** — commit/rollback `FUN_1407cf220/f3c0`; dump observers.
44. **T40-4 `0x140f49xxx` context family** (`FUN_140f49550/500`, `0x140f1e990/ee20`). `crossref.py 140f49550`.
45. **T40-5 media render descriptors** — decode `0x14385cbe0–0x14385d190` (XOR-8, strscan names headers only).
46. **T40-6 the pass-40 hole** `0x1407efae0→0x1407eff20` — `gap_report.py 368 375 --offcuts` when neighbours gain mentions.
47. **T40-7 `func_0x0001407e5d00`/`func_0x0001407e5990`** — GUID hash + team-full checks, no bodies; grep forward.
48. **T41-1 'Unknown' widget-enum belt decode** — `0x14385d1a0`–`0x14385ddf0`, 122 pages; pool-side `strlookup` or resolve one factory name (`FUN_1407fd0a0`'s `DAT_14385d1c4` vs key `0x14385d1b8`).
49. **T41-2 window-giant family boundary** — one function re-decompiled or a real family? `crossref.py 14080c740` (no namer); `gap_report.py 380 381 --offcuts` later.
50. **T41-3 entity-root chain `0x1e2421a4798a328`** (66 hits pass 41) — name the root; `strlookup --band` on the `_DAT_143b79598+0x1c4` region.
51. **T41-4 the `func_0x000142388ab0/af0/bf0` serializer target** — the pass-50 parser's writer twin (c740 window). `crossref.py 142388ab0`.
52. **T41-5 `0x142045667` far region** (5 stamps from `FUN_1408050d0`) — charge/apply bank write-out. `crossref.py 1408050d0`.
53. **T41-6 `0x143b93510` observer block** — `DAT_143b93548` flag + `_DAT_143b93518/50/58` callbacks (`FUN_140818f40`); dump the fn-ptrs.
54. **T41-7 `FUN_142044820` bank objects** — id→8×0x10-row bank resolve (charge/apply pair); def chunk unread. `crossref.py 142044820`.
55. **T41-8 the big factory screens' update bodies** — 0x12c70/0x16f0/0x2a10/0x31580/0x31868 B products constructed but their present/update bodies were not in range; grep forward for `PTR_FUN_142fe6328`/`PTR_FUN_142fea6b0` users.
56. **T42-1 the 8,015-B hole** `0x14083d280→0x14083f2c0` — `gap_report.py 385 394 --offcuts` (or re-run when neighbours gain mentions); largest hole since pass 34.
57. **T42-2 `0x140867cd6` (144 stamps from `FUN_1408493b0`)** — the summary writer's own window, inside chunks 0395+; next pass reads its ground directly — compare the stamp count.
58. **T42-3 the `0x1421exxx` list API (23 members)** — def region is the unread `0x1408493b0`–`0x140867xxx` cluster; `crossref.py 1421e4620` once read.
59. **T42-4 name-window family boundary** — one cascade (shared triple-mix) or a real family? The single far namer `FUN_140adcec0` (chunk 0545) of `FUN_1408446e0` is the first cross-cluster datapoint: `crossref.py 140adcec0`.
60. **T42-5 the map/mode enum table** behind `FUN_14082b700/14082b940` (~10 display ids via `FUN_140832720/1408357e0`); name it: `strlookup --band` on the `+0x4c0` block, or `crossref.py 142d37920`.
61. **T42-6 the `0x140bfxxxx` hero-record row API** (8 members) — def chunk unread; `crossref.py 140bf36c0`.
62. **T42-7 the global player arrays `PTR_DAT_14385f3b0/3f480/3f4f0`** — who writes them besides `FUN_140847b10/be0/cc0/d20`? grep the corpus for the literals.
63. **T42-8 `0x141bba761` (8 stamps, `window reach:` debut)** — the string-builder region (`FUN_141bba790` ×42 target); sweep when a defining chunk is named.

CLOSED (machine): fd9670 recount; provenance; `0x1411b8070`; thread 43; T20 (`max refs:`);
JSON writer/parser/CSV (31/32); XOR-8 salt keys; presence-failure events; ledgers 1–4, 6,
9–12, 14, 17–21, 25, 28–29, 35, 37–38, 40 (archive). Pass 36 closes T35-1/T35-3; 37 closes
T36-3 partially + pass-36 (a); 38 closes T37-4 + pass-37 (a); 39 closes T38-1 negatively-
positively + pass-38 (e); pass 40 reads T37-3's render lifecycle from the consumer side;
**pass 41 reads T23's audio usage consumer-side and closes the 'Unknown' belt extent
(122 pages); pass 42 reads T9's flag-block protocol (the `DAT_143b945b0/b4`
player-list spinlock), names the voice client ('VoiceClient' plaintext band), and
resolves the summary field-id set.**

## Next pass

Resume range: **`NEXT.txt`** — written by `pass_next.py` from `state.json` + `--max`;
regenerate after every `--update`, never hand-edit. Pass 42 ends at `FUN_1408493b0` (the
summary window giant); stratum `0x14054fea0` OPEN. Run `pass_measure.py 395 402`, quote
the block, `--update`, refresh `NEXT.txt` and this file. Watch for: (a) **the summary writer's own ground** —
`FUN_1408493b0`'s 144 far stamps land at `0x140867cd6`, inside chunks 0395–0402
(`0x140849a10–0x140874660`): the `0x1421exxx` list API's definitions and the
25-field writer bodies should be readable directly (T42-2/T42-3); (b) **the
`0x140d5xxxx` replay-audio family** (`FUN_140d5e9b0/140d5e8c0/140d5ea30/140d60680/
140d5fdd0` named pass 42 from the spectate callbacks — T41's `0x140d1xxxx` sibling,
bodies unread); (c) **the spectator/observer tier continuation** — the
`FUN_140847990` permission table and `FUN_140846300` alive-counter suggest the
spectate rules engine follows immediately; (d) whether the **name-window family**
continues past `0x140849a10` or gives way to a new subsystem (the strscan
look-ahead row `0x14385F5E8 'Missing guid [0x%llX] in switch statement'`,
`FUN_14084a3a0`, promises a GUID switch nearby); (e) the `0x14099c1d5` store
region (14 stamps pass 42, third sighting) and `0x141bba761` string-builder
region (8 stamps, debut) — both sweep candidates when `window reach:` names a
defining chunk. Do not re-run a counted range through `--update` (ledger 5); no
ciphertext script line (ledger 7); never treat `0x826e…`/`0xca334801`/
`0x4343ffa4`-family or offcut-call addresses as data (ledger 20); ledgers
24/31/39/43/44/47/49/53/54/55/57 for gaps and windows; `size=` is not coverage
(ledger 30); overlapping windows per ledgers 39/47/49 — **paste, never re-type,
the measure block (ledger 56)**, and check the zone counts sum to `files=`.
