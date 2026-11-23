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

Corpus: 2,228 chunks, 119,757 functions, 42,864,695 B `.text`. Passes 1–22 archived in `CODE_MAP_ARCHIVE.md`; `state.json` is the truth; pending range is `NEXT.txt`.

| pass | chunks | `.text` range | functions | record |
|---|---|---|---|---|
| 23–33 | `0193`–`0306` | `0x1404192e0`–`0x14069b460` | 5,537 | `ranges/` rows 23–33 (archived detail) |
| 34–38 | `0307`–`0359` | `0x14069bb80`–`0x1407a2800` | 1,563 | `ranges/0x14069bb80-…` … `0x140785e30-…` |
| 39–42 | `0360`–`0394` | `0x1407a28c0`–`0x1408493b0` | 2,076 | `ranges/0x1407a28c0-…` … `ranges/0x14081d520-0x1408493b0.md` |
| 43 (8-chunk) | `0395`–`0402` | `0x140849a10`–`0x140874660` | 316 | `ranges/0x140849a10-0x140874660.md` |
| **total** | **402, contiguous** | `0x140001000`–`0x140874660` | **23,415** | machine-verified (`state.json`) |

Machine-verified (`state.json` after pass 43): files 23,415 (19.55 %), Σ `size=` 6,486,312
(15.12 %); classes reg 7,956 / wrapper 1,954 / builder 1,717 / sorted 280 / atexit 261 /
record 326 / other **10,921**; 7,956 distinct ciphertext registrations + 4 plaintext rows
(one hash ×2 — Corrections 16); `d4f30` 1,188 / `d4f70` 1,350 / `d4fb0` 4,492 / `c2d70`
4,212 / `c2d50` 326 / `c7880` 261 / `atexit` 315; records 326. Passes 27–43 = consumer only.

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
51. **`FUN_14099xxxx` is the store's platform/purchase API** (confirmed 35; `FUN_140993710` product lookup called from pass-40's roster build; **pass 43: the store client `0x140995xxx`/`0x140598xxx` + product images `FUN_1409958c0/140993820` read consumer-side; bodies still unread**).
52. **Resume range and measurement provenance are generated** — `NEXT.txt` from `pass_next.py`, `--json` digest for records; `max refs:` auto-crossrefs.
53. **Window chunks + `window reach:`** — see 47; pass-37/38 window-cache giant set treated as one cascade each.
54. **UI-window cache** `_DAT_143b795a0/a8/b0` + `0x2d1d7705`-family hash, binary-searched by giants (prologue) and walked by dtors (`0xfd749dd6ef1fd0d4` tail) — treat namers as the same construct.
55. **XOR-8 carries ASCII code constants** (pass-39 Battle.net band `0x14385c898`–`0x14385c9b4`; pass-40 ruleset/result enums to `0x14385d180`).
56. **Retyping a measure block is a transcription hazard — and so is anchoring on the
previous record's block** — paste from a saved run, diff before committing (pass-40 story in
the archive).
57. **Window families grow by cascade** — pass 41's `FUN_14080c740` set (114 KB, ratio ~27,
zero namers) and **pass 42's name-window family (`FUN_1408314b0`…`FUN_1408493b0`, shared
triple-mix, ratios to ~755, one far namer `FUN_140adcec0` chunk 0545) are the two largest;
treat per ledgers 39/49; `size=` there is meaningless.**
58. **The `0x1421exxx` family is the UI row model; the pass-42 144-stamp "ground" is one
overlapping window** (pass 43): the stamps land inside `FUN_140867b30`'s span — per
ledgers 39/47/49, call sites of one window, not a separate body. ~50 members read
consumer-side (fields `0x3ff3/0x6003` child lists, `0x229a` value GUID, `0x2d95` row key;
nodes minted as `0xa88000000000xxx` GUIDs); **the pass-42 summary field-id set is the
shared UI schema** (`FUN_14085c450`/`FUN_140861ab0` write the same ids).

**Closed/superseded (archive):** items 1–4, 6, 9–12, 14, 17–19, 21, 25, 28, 29, 35, 37, 38, 40, 42 — full text in `CODE_MAP_ARCHIVE.md` §Corrections archive.

## What the code is — cumulative synthesis (43 passes; evidence unless marked [inference])

`.text` is catalogued in entry-address order. After 402 chunks the cursor is at `0x140874660`
(19.55 % of functions, 15.12 % of `.text`). Names printed `func_0x…` have **no decompiled body
in this dump** — registrar, decryptors `d4f30`/`d4f70`, writer `c2d50`, helpers `c2d70`/`c7880`,
the `0x140543xx0`/`0x1405674xx` decoder family, settings accessors, component getters, the
hotfix HTTP client, CSV iterator, pass-32 cipher `FUN_142454xxx`, the render tier
`FUN_141ff40f0`-family (protocol known from pass-40 consumers), `FUN_141d11f60`/
`FUN_141c4efa0` time/random, `func_0x0001407e5d00`/`5990` slot maps, the
`0x140f49xxx`/`0x140f1exxx`/`0x140d2xxxx`/`0x140d5xxxx` families (named, unread) — as does
`tls_callback_0`. **Six layers, in address order:**

1. **Library preamble** `0x140001000`–`0x140039fc0`: ISA-L/igzip inflate, NVAPI bootstrap + 53 wrappers.
2. **NVIDIA driver-loading shim** `0x14003a230`–`0x14003d330`: replacement `LoadLibrary` for `nv*.dll`.
3. **CRT/C++ static-init sea** `0x14003ffe0`–`0x1400fa760`: five generator templates (181-B magic-static ×2,451; 209-B locale ×354; 58-B event thunks ×284; 134-B XOR-40 ×61; 37-B `_onexit`).
4. **Typed registry machine** `0x1400fbcb0`–`0x14054ea50` (CLOSED): nine constructs (name buffers, registration, builder, copy wrapper, sorted-insert, `{id,hash}` ×326, nested-atexit, settings registrar, CompilerIDFilter).
5. **Runtime bootstrap + obfuscated dispatchers** `0x14053f6b0`–`0x14058200x`: PE entry, sig scanner, anti-tamper, masked-pointer layer.
6. **Engine runtime** `0x14054fea0`→ (passes 28–43, **OPEN**). Cumulative halves, newest first:
   **(43) settings/menu/social/BattlePass/hero-select UI tier** — the settings screen
   trio + interdependency engine + GUID switch `FUN_14084a3a0`; the screen-builder
   belt (~40 screen ctors, `0xa88000000000xxx` type GUIDs); the kill-feed giant
   `FUN_1408551d0` (35 KB + the 0x20-row intro-sort + the open-addressing seen-set,
   new chain `(x*0x40000+~x)*0x15*0x41`); the **BattlePass system** (tier ladder,
   claim records, the plaintext page-name table `FUN_14085f600`, the store client
   by masked key `0x74a810779e8bc160`, JSON summaries mirroring the pass-42
   field-id schema); the social tier (invites, hero-group ladder table, queue, the
   chat-entry object with two compiled regexes); and the **hero-select
   team-assembly engine** (0x1b00-B screen object, hero count 0x13e=62, ban list,
   per-locale availability, role kinds `0xc880000000000cd` family, auto-fill
   suggest `FUN_140874660`);
   **(42) lobby/match-state rules tier + voice client + name-window family +
   hero-actor object** — 5-slot HUD binding, 'VoiceClient' + the 18-id audio-cvar
   set, ~200-fn lobby rules over seven 0xd0-stride hero-record banks, the
   `FUN_1408314b0`…`FUN_1408493b0` name-window family, the 0x4b0-B hero-actor +
   status-effect store + scoreboard enumerator + the summary giant
   `FUN_1408493b0` (25-field id set; its 144 stamps resolved pass 43 as one
   window, ledger 58);
   (41) hero ability/weapon/stat system + widget-factory belt + entity-view/HUD
   tier — 0x2a10-B hero entity, ~2000-case stat getter `FUN_1408038e0`,
   charge/apply `FUN_1408045f0/1408050d0`; the **114-K window family**
   `FUN_14080c740`-set; the 62-call factory registrar `FUN_141c4b050`; the sound
   pair `FUN_1407ff5c0/1407ffc50`; the 0x3b60-B entity-view object;
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
`FUN_1407e1e40`, event logger `FUN_1407ea990`, match-history `FUN_1407ed2e0`, result
builders `FUN_1407f2660/2a00`, media `FUN_1407dfdd0/1407f4c70`+layout `FUN_1407f4ad0`,
generational handles `FUN_1407dd910/9c0/a70`, roster `FUN_1407ce150`/`1407d4b00`, kill
feed `FUN_1407dac50/db590/db710`, group `FUN_1407e8ed0`, factory `FUN_1407d6310`),
*hero-ability tier* (41: hero entity `FUN_140802620/2660`+dtor `FUN_140809280`, stat
getter `FUN_1408038e0/ed0`, tick `FUN_140804070`, charge/apply `FUN_1408045f0/1408050d0`,
cast `FUN_14080a730`, window family `FUN_14080c740`-set, stat fold `FUN_14080d850`,
screens `FUN_140808f30/…/1408168c0`, sound `FUN_1407ff5c0/1407ffc50`, entity-view
`FUN_140818260/14081a3b0/140819290`); *lobby/rules tier* (42: HUD `FUN_14081dfe0`,
voice `FUN_140837fa0`, rules `FUN_140827790`-set, name windows `FUN_1408446e0`-family,
hero actor `FUN_14083f2c0`, effects `FUN_1408464a0`, summary `FUN_1408493b0`);
*UI/menu tier* (43: settings `FUN_14084b060/b750/bfb0`, kill-feed `FUN_1408551d0`+sort
`FUN_140856550`, BattlePass `FUN_14085c850/da80/61ab0/e5f0`+pages `FUN_14085f600`,
invite `FUN_140865270`, groups `FUN_140867e90`, chat `FUN_14086ac30`, stats
`FUN_14086efc0`, hero-select `FUN_1408722a0/872b90`, suggest `FUN_140874660`).

**Where the data lives** (full table in the archive; live additions):

| band | content |
|---|---|
| `0x143848d40`–`0x143860660` | XOR-8 name/payload ciphertext, extending pass by pass (settings/UI/party/store/map/widget names ≤ 41; pass 41's 'Unknown' factory belt `0x14385d1a0`–`0x14385ddf0`; pass 42's voice/device band `0x14385f158`–`0x14385f348`) — **pass 43 adds the Battle Pass page-name band `0x14385f9e8`–`0x14385fc24` (9 plaintext pages, `FUN_14085f600`), the chat-regex pair `0x1438604d0/4e8`, and 12 inline log pages `0x14385f560`–`0x14386066c` with no strpool row** |
| `0x1438b8e50`–`0x1439fa330` | registry ciphertext; triplet-stub page |
| `0x143a155xx`–`0x143b81a0x` | XOR-40 keys, settings names, runtime block (~250 feature flags `0x143b945b8–0x143b9c5c0`), **pass 40: settings/observer block `0x143b90c30–0x143b90ea8`** |
| `0x143cf0000`+ | RTTI, reg outputs, settings descriptors, config globals; pass-40 null-match GUID `0x143b83da0–dc` |
| `0x1441e18f0`+ | plaintext reg outputs, struct schemas, record pools; TLS RNG base `0x144180fa0`, time scale `0x14415f7c8/f7f8` |

**What it is for.** Layers 1–2 are a vendored NVIDIA/igzip preamble; layer 3 compiled-in C++
static init; layer 4 registers ~8 k encrypted type names; layers 5–6 are the client —
settings, telemetry, schemas, chat/voice, hotfix, HUD, spatial/entity runtime, match
receive, gameplay loop, presentation, replay/cinematic, social/store, map-load, UI windows,
party/voice/chat (39), match/join/redemption + hero-select + media (40), the hero
ability/weapon/stat system (41), the lobby rules tier + voice client (42), and now (43)
**the settings/menu/social/BattlePass/hero-select UI tier** — the consumer side of every
service named above: audio cvar screens, the screen belt, BattlePass with its page-name
table and store client, the party/queue/chat social tier (with the compiled chat-command
regexes), and the hero-select team-assembly engine. No plaintext game protocol (entity
traffic is the bitstream; replays reuse it); the render device is `FUN_141ff40f0`
(lifecycle mapped). Confidence: counts/shapes/bands measured; construct labels are
shape-based inference; obfuscated bodies read structurally only.

**Known limits.** (a) `func_0x…` bodies absent (see synthesis list; offcuts: `0x14068xxxx`
(33), `FUN_141da/141db` emitters (33), `FUN_14099xxxx` store API (35, now 3 consumer sites),
`FUN_140d1xxxx` sound (36), render tier (37→protocol known 40), `0x140f49xxx`/`0x140f1exxx`
(40), `0x140d2xxxx`/`0x140d5xxxx` ability-config family (41 — named from the hero tier,
bodies unread), **`0x140bfxxxx` hero-record row API (42 — named from the effect store,
bodies unread; `crossref.py 140bf36c0`)**). (b) XOR-8 keys
are per-record salts. (c) `0x142f0…`–`0x142f2b…` thunks absent. (d) Corpus gaps: pass 30's
12 × >1 KiB; pass 34: 4 holes / 11,844 B; pass 35: 6 / 18,531 B; pass 36: 2 / 6,068 B;
pass 37–39: 0 holes; pass 40: 1 hole / 1,033 B (`0x1407efae0→0x1407eff20`, T40-6);
pass 41: 0 holes; pass 42: 1 hole / 8,015 B (`0x14083d280→0x14083f2c0`, T42-1 —
`--offcuts` pending); **pass 43: 1 hole / 1,601 B (`0x14084b750→0x14084bfb0`, T43-1)**.
(e) Window chunks per ledgers 39/47/49/53: pass-37/38
window-cache giant set = one cascade each; pass-40 range max `FUN_1407f5710` (ratio ~34);
pass 41's `FUN_14080c740` set (ratio ~27, zero namers, 90 stamps at `0x141c4b29c`); the
**pass-42 name-window family (`FUN_1408314b0`…`FUN_1408493b0`, shared `^0xeb+
0x2d1d7705` triple-mix, ratios up to ~755, one far namer `FUN_140adcec0` chunk 0545)
is the largest window family yet — ledgers 49/57 extended (T42-4)**; **pass 43's three
giants (35,000/27,431/25,193 B, ratios 5–7, no namers) are real bodies — no new window
family; the 144-stamp overlap resolved as one window (ledger 58)**.

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
| **List API `0x1421exxx` (42→43)** | the **UI row model** (~50 members, ledger 58): `40c0/3c20/3330/3420` child-list get, `5100` begin, `52c0` node-at, `3de0/3d70/3d00/3810/3920` getters, `41d0/4620/4580/4480/4860/4910/49a0/4270/43e0/4170` setters, `52a0/5370/5310` list ops, `51d0/5130/51a0/5230` row ctors, `4140` type test, `4af0` node-by-type, `3810` node-by-key; fields `0x3ff3/0x6003` child lists, `0x229a` value GUID, `0x2d95` row key; nodes = `0xa88000000000xxx` GUIDs; `FUN_1421e5100` ×380 pass 43 (record) | `0x1408493b0` |
| **Player-list lock (42)** | `DAT_143b945b0` 0x400-spinlock (`FUN_141c5c3d0` escalate) + `DAT_143b945b4` disable flag over the three global arrays `PTR_DAT_14385f3b0/3f480/3f4f0` — the scoreboard's data source (T9's flag block, protocol read) | `0x140842fe0` |
| **JSON DOM + writers (43)** | node ctors/readers fully mapped consumer-side: `FUN_141940c00/ea0/e00` + `141940ef0` property set + `141941360/141941440` array + `14193e0d0/93e940/93ef80/93f510/93f560/93e5c0` readers + `FUN_140693130/1406935f0/1406934c0` writers + `func_0x00014213ee60` compact writer (0x14213f7df siblings) + posters `FUN_140840db0/140840e90` + pools `DAT_144137230/250` | `0x14084f530` |
| **UI screen tier (43)** | ctor = base + vtable + `0xa88000000000xxx` guid; node mint `__RegisterWaitForSingleObject(list,type,0)`/`FUN_140726800`; widget chain `FUN_1422544f0`→`1421f1780/1610`→`142255180/330`→`1421ee370/7d0`→`FUN_14224eec0/14224f390`; reconcile `FUN_140726c50`+`FUN_140565db0/1421e5310`; sorts `FUN_140856550/1408666c0/140871270`; hash-set `(x*0x40000+~x)*0x15*0x41` — a fourth hash family | `0x140849a10` |

## Open threads (cheapest next query each; check/update every pass)

2/5. **Entity transport framing** (client found 32, socket ahead) + **command ids** — base `0x48/0x53/0x7c/0x7d/0xa5/0xb2/0x3a`; grown 32–41 (pass 41: audio 0x8d, ability ids 0x6b/0x655/0xf5/0x580/0x1e; **pass 43: queue events 0x631b/0x6334, hero events 0x664e/0x66b7/0x6521, claim events 0x12e58–0x13223**).
7/9. `FUN_141c295b0`/`FUN_141c58170`/`FUN_142d2cf30` bodies unread (~chunk `15xx`); the `0x143b945b8`–`0x143b9c5c0` flags' writers pending (lock protocol read pass 42).
11–12. Channel-list renderer (writer found 32, renderer unfound); hotfix record dump `_DAT_1439d98c0`.
13. **Gaps** — pass 43: 1 hole / 1,601 B (T43-1); pass 42: 1 hole / 8,015 B (T42-1); pass-40 T40-6 hole; `0x14059a007–0x14059c350` (9,033 B), `0x1401a4e02–0x1401abad0` (27,854 B) open.
15–16. Event-name table `0x143851c90` still encoded; pass-32–34 machinery bodies (cipher, event-hash, emitters, samplers).
17. **Handle-table writers** — grep `0x18317a531d116c`; pass 40 adds the generational table readers (conventions).
18. **`FUN_14099xxxx` store API** — consumers 35/40/41 + **pass 43 store client `0x140995xxx`/`0x140598xxx` read consumer-side**; bodies unread.
19. **Widget/enum pages** — 'Unknown' belt `0x14385d1a0`–`0x14385ddf0` (122 pages, pass 41); pool-side decode pending (T38-1/T41-1).
21–23. Store endpoint labels (decode `0x1438595b0–0x1438597c8`); `FUN_140d1xxxx` sound assets (`crossref.py 140d1bcc0`); audio-channel ids (partially closed 41; the id enum's full table remains).
24–25. `0x8784b4333a5802xx` masked chain (`strlookup --band 0x1439dc5c0 0x1439dc630`); component-message ids (`0xd8…`/`0x5800…`/`0xde…`/`0x46…` families).
26–30. Widget names / UI-cache tables / render tier (**partially closed 40**: lifecycle mapped, bodies `FUN_141ff40f0`-family unread) / trail rows (closed 38) / live-ops flags.
31–35. Widget-name band decode / material family `crossref.py 142cb4c20` / `FUN_140c6xxxx` input / `FUN_1409bxxxx` appliers / `0xbd` input rows.
36–40. `0x142f2df90` fn-ptr table / `FUN_1407b0e90` stat fold / 18-key channel ladder / toast table `0x143059b80` / `0x14213f7df` far-window region (**27 more stamps pass 41** from `FUN_1408100f0`; plus new regions `0x142045667` ×5 and `0x141c4b29c` ×90 — sweep when `window reach:` names a defining chunk).
41–47. T40-1…T40-7 — result-summary serializer (`crossref.py 1407f2a00`); time/random
`FUN_141d11f60/141c4efa0`; the `0x143b90c30–ea8` observer block; `0x140f49xxx` context
family (`crossref.py 140f49550`); media descriptors `0x14385cbe0–d190` decode; the
pass-40 hole `0x1407efae0→0x1407eff20` (`--offcuts`); `func_0x0001407e5d00/5990` GUID
hash/team-full bodies.
48–55. T41-1…T41-8 — 'Unknown' belt `0x14385d1a0–ddf0` decode (122 pages); the c740
window-family boundary (`crossref.py 14080c740`); entity-root chain `0x1e2421a4798a328`
name; `func_0x000142388ab0/af0/bf0` serializer twin (`crossref.py 142388ab0`);
`0x142045667` far region; `0x143b93510` observer block fn-ptrs; `FUN_142044820` bank
objects (`crossref.py 142044820`); the big factory screens' update bodies (grep
`PTR_FUN_142fe6328`/`142fea6b0`).
56–63. T42-x — the 8,015-B hole `0x14083d280→0x14083f2c0` (`gap_report.py 385 394
--offcuts`); ~~T42-2 CLOSED pass 43~~ (the 144 stamps are one window, ledger 58);
T42-3 → T43-2 (list-API def region `0x1421e0000+`, ~+26.7 MB; `crossref.py 1421e5100`);
name-window boundary (`crossref.py 140adcec0`); the map/mode enum table
(`crossref.py 142d37920`); `0x140bfxxxx` hero-record row API (`crossref.py 140bf36c0`);
the global player-array writers (grep the literals); `0x141bba761` string-builder region.
64. **T43-1 the 1,601-B hole `0x14084b750→0x14084bfb0`** (pass 43's only hole) — `gap_report.py 395 402 --offcuts` when neighbours gain mentions.
65. **T43-3 the settings-field GUID catalogue** — ~20 categories / ~100 field GUIDs over the `0x140912xxx–0x140916xxx` get/set family; def region 0x1409124b0+ = **chunk 0403+ (next pass's ground; look-ahead `FUN_140876110`)**.
66. **T43-4 hero-select object's fn-ptrs `PTR_FUN_142f7d730/740`** (ctor +0x640/+0x648, the 0x1b00-B object's row factory pair); `crossref.py 142f7d730`.
67. **T43-5 the regex family's match side** — ctor/compile/finalize read (`func_0x000141b1ab00`/`FUN_141b39f70`/`FUN_141b3a510`), match bodies unread; `crossref.py 141b39f70`.
68. **T43-6 the locale system** — `func_0x000140c70eb0` index + `FUN_140c71110` row + `FUN_142ca5bf0` compare + the per-locale hero availability table; `crossref.py 140c71110`.
69. **T43-7 hero-count 0x13e (62)** — the default/none kind in the hero-select engine; cross-check vs the pass-42 hero banks (the hero-table size?).
70. **T43-8 the `0x14091a2xx/0x14091bxxx` party-row family** (`FUN_14091a200` init, `FUN_14091b6a0/91b790` invite accept/decline; def region ~0x14091a000, chunk 0410+); `crossref.py 14091b6a0`.

CLOSED (machine): fd9670 recount; provenance; `0x1411b8070`; thread 43; T20 (`max refs:`);
JSON writer/parser/CSV (31/32); XOR-8 salt keys; presence-failure events; ledgers 1–4, 6,
9–12, 14, 17–21, 25, 28–29, 35, 37–38, 40 (archive). Pass 36 closes T35-1/T35-3; 37 closes
T36-3 partially + pass-36 (a); 38 closes T37-4 + pass-37 (a); 39 closes T38-1 negatively-
positively + pass-38 (e); pass 40 reads T37-3's render lifecycle from the consumer side;
**pass 41 reads T23's audio usage consumer-side and closes the 'Unknown' belt extent;
pass 42 reads T9's flag-block protocol, names the voice client, and resolves the
summary field-id set; pass 43 resolves T42-2 (one window, ledger 58), reads the list
API as the UI row model, and names the BattlePass page table, the chat regexes, and
the JSON DOM family.**

## Next pass

Resume range: **`NEXT.txt`** — written by `pass_next.py` from `state.json` + `--max`;
regenerate after every `--update`, never hand-edit. Pass 43 ends at `FUN_140874660`
(the auto-fill/suggest engine); stratum `0x14054fea0` OPEN. Run `pass_measure.py 403
410`, quote the block, `--update`, refresh `NEXT.txt` and this file. Watch for: (a)
**the settings-field API ground** — the `0x140912xxx–0x140916xxx` get/set family's
def region starts at ~0x1409124b0 (chunk 0403+; look-ahead pages `0x143861180/1200`,
`FUN_140876110`); pass 43's ~100 field GUIDs resolve there (T43-3); (b) the
`0x14091a2xx/0x14091bxxx` party-row family (invite accept/decline, def
~0x14091a000, chunk 0410 — T43-8); (c) the hero-tab/stat-page continuation
(`DAT_143049d10`/`DAT_143049ac8` GUID arrays → the `0x140913xxx/0x140914xxx` bodies
ahead); (d) whether the screen belt gives way to a new subsystem after `0x140874660`;
(e) the `0x1421e0000+` list-API def region (~+26.7 MB) and `0x141bba761` — sweep
candidates when a defining chunk is named. Do not re-run a counted range through
`--update` (ledger 5); no ciphertext script line (ledger 7); never treat `0x826e…`/
`0xca334801`/`0x4343ffa4`-family or offcut-call addresses as data (ledger 20);
ledgers 24/31/39/43/44/47/49/53/54/55/57/58 for gaps and windows; `size=` is not
coverage (ledger 30); overlapping windows per ledgers 39/47/49/58 — **paste, never
re-type, the measure block (ledger 56)**, and check the zone counts sum to `files=`.
