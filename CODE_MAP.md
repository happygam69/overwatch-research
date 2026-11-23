# CODE_MAP — cumulative map of the systematic `.text` read

**Read in full before every pass; update after every pass. Hard budget: ≤300 lines** (raised from 250→300→350 across passes 23–39; re-tightened to 300 at pass 40 — see Corrections 56).
Per-pass narrative lives ONLY in `ranges/`; cumulative numbers come from `state.json` (via
`scripts/pass_measure.py`) — never hand-add. Long-form archive: `CODE_MAP_ARCHIVE.md`.

## Files

| file | role |
|---|---|
| `chunks/chunk_NNNN.txt` | corpus, address order; unreachable-block warnings stripped 2026-11-21 (counts in `index.json`) |
| `index.json` / `state.json` | per-chunk bytes/first/last (coverage truth) / machine ledger: next_chunk, passes, totals, reg hashes, 326 `{id,hash}` rows |
| `scripts/pass_next.py` / `NEXT.txt` | resume range from `state.json.next_chunk` + the `--max` cap; `NEXT.txt` is its generated output — never hand-edit |
| `scripts/pass_measure.py` / `ranges/*.md` | canonical per-pass measurement (quoted verbatim or `--json` digest; `max refs:` = auto-crossref of the range max) / per-pass records — the evidence base |
| `scripts/gap_report.py` | per-range gap classes (`giant`/`offcut`/`hole`; `--offcuts` = corpus sweep) + `window reach:` far-window watch list (ledger 53) |
| `rdata_names.tsv` + `scripts/rdata_names.py` | plaintext `.rdata` strings (16,832 rows) / regenerator; query via `strlookup.py --pool rdata_names.tsv` |
| `docs/*.md` | reader-facing findings: plain-prose subsystem pages (registry, engine, UI, hero); no line budget, milestone-only; conclusions cite records |

## Coverage

Corpus: 2,228 chunks, 119,757 functions, 42,864,695 B `.text`. Passes 1–22 archived; `state.json` is the truth; pending range is `NEXT.txt`.

| pass | chunks | `.text` range | functions | record |
|---|---|---|---|---|
| 23–33 | `0193`–`0306` | `0x1404192e0`–`0x14069b460` | 5,537 | `ranges/` rows 23–33 (archived detail) |
| 34–42 | `0307`–`0394` | `0x14069bb80`–`0x1408493b0` | 3,639 | `ranges/0x14069bb80-…` … `0x14081d520-0x1408493b0.md` |
| 43–44 | `0395`–`0410` | `0x140849a10`–`0x1408a6750` | 1,098 | `ranges/0x140849a10-0x140874660.md`, `ranges/0x140875440-0x1408a6750.md` |
| 45–46 | `0411`–`0426` | `0x1408a6970`–`0x1408f95b0` | 664 | `ranges/0x1408a6970-…`, `ranges/0x1408d27b0-0x1408f95b0.md` |
| **total** | **427 indices, `0000`–`0426`** | `0x140001000`–`0x1408f95b0` | **24,470** | machine-verified (`state.json`) |

Machine-verified (`state.json` after pass 46): files 24,470 (20.43 %), Σ `size=` 7,013,048
(16.36 %); classes reg 7,956 / wrapper 1,954 / builder 1,717 / sorted 280 / atexit 261 /
record 326 / other **11,976**; 7,956 registration calls = 7,952 ciphertext + 4 plaintext
(7,955 distinct; one plaintext hash ×2 — Corrections 16); `d4f30` 1,188 / `d4f70` 1,350 / `d4fb0` 4,492 / `c2d70`
4,212 / `c2d50` 326 / `c7880` 261 / `atexit` 315; records 326. Passes 27–46 = consumer only.

## Corrections ledger (machine-derived; supersedes prose in older records)
5. **`--update` is forward-only; `--init` wipes the pass list** — `--update` over a counted range double-counts and rewinds `next_chunk`; repair is `--init`. 7. **No `ciphertext band:` line** — the `CTXT` regex needs `DAT_1438` + 6 hex digits; the band is now `0x1439a…`–`0x143b…`; extremes read from the text. 8. **`zones:` filter** prints only `reg`/`record` runs with `cnt>=3`.
13. **Allocator symbol ≠ allocator** — key on the shape; allocator `func_0x141c23490(&PTR_PTR_143a01d18,size[,align])` + free `func_0x000140578190`. 15. **Minimum registered size is 3** (`FUN_1404aad50`); span 3–0x3bc0. 20. **Decompiler fabrications:** `0x826eb8xx`, `0xca334801`, `0x38046856305b946b`, `0x0a13cb7c…`, `0x09e1c148…`, `func_0x000102d05da9`/`func_0x00010161e575` — never add to a band table.
22. **2-entry vtables at `0x140556eb3`/`FUN_14057ad20/57b2c0/57e220`; both arms known.** 23. **`files=` counts functions, not chunks.** 24. **The corpus is missing functions** (pass 29: 113 gaps / 81,067 B) — record gaps, never assume padding. 27. **`0x14384b7b0–b7bc` are plaintext floats on an XOR-8 page** — pages are not homogeneous. 30. **`sum_size` is not coverage** — quote the address range and count gaps from headers. 31. **Pass 30: 332 alignment + 142 under-reported + 12 × >1 KiB = 48,640 B un-decompiled.**
32. **Hash families:** D double-mix `-0xae502812aa7333/-0x3b314601e57a13ad`; E descending buckets; D variants `FUN_1407da2d0/1407da500/1407da6c0` (40); open-addressing `(x*0x200000+~x)*0x109*0x15` (45, kill-cam ladder).
33. **Match-queue error enum 0–12** = `UserRequest … Invalid` (`FUN_1405ddb40`). 34. **Event-name table `0x143851c90` is `.data`, pointer-shaped/encoded** — not inline names.
36. **Masked chains coexist** (component `0x4d79452d…`; per-session type table `(x+0x3fa981c8e7192fa6) ror31 ^ 0x8784b4333a580288 → ror23 + 0x37a9e6a2eedd5214 + type*8`; per-frame handle `(p^0x73cc01350b9bc072)+0x704e4dbd364c5bd3 >> 0x26|×0x4000000` + `0x18317a531d116c…` bucket table; store row `0xba397115a070ffa9+0x4094aaa9c7911a89`; entity root `0x1e2421a4798a328…`; service roots `0x622b95327b2e6d1e ^ 0xd6c0ac78d0e44481`; later chains in the records; the type table is the dominant resolve, ~90 sites/pass).
39. **Overlapping decompilation windows** (pass 33/35/47/49 class); treat giant duplicates as one cascade each. 41. **Per-frame handle rows 16 B `{u32 handle,u32 pad,u64 entity_ptr}`.** 43. **Gap totals are hand-computed as distances** — always re-run `gap_report.py` before quoting. 44. **Pass 34: 4 real holes / 11,844 B.** 45. **`FUN_1406232f0` is the replay/demo frame reader too** — replay format IS the bitstream. 46. **`FUN_1406b7500` ×211** canonical open-chaining table grow + twin `FUN_140727340`.
47. **Window chunks: `size=` can be ~50× smaller than chunk text** (`chunk_bytes/size= > 20` ⇒ window chunk); far-window stamps are unread-region pointers, never coverage. 48. **Corpus maxima were range maxima** — `--maxscan` ranks `FUN_142b567b0` 571,552 B first; a NEW max is a claim until `max refs:` shows no second namer.
49. **Pass 35's 223,308-B `FUN_1407174e0` is one decompilation window**; its 24 >1 KiB "gaps" are real bodies; 6 corpus holes / 18,531 B. 50. **Second JSON parser** (rapidjson-style `FUN_140612090` + DOM verify `FUN_1422ee440`; errors 1–0x11 in `FUN_140734260`, second site `FUN_140778120`) — distinct from the pass-32 text engine.
51. **`FUN_14099xxxx` is the store's platform/purchase API** (confirmed 35; consumers to 46; bodies unread). 52. **Resume range and measurement provenance are generated** — `NEXT.txt` from `pass_next.py`, `--json` digest for records; `max refs:` auto-crossrefs. 53. **Window chunks + `window reach:`** — see 47; pass-37/38 window-cache giant set treated as one cascade each. 54. **UI-window cache** `_DAT_143b795a0/a8/b0` + `0x2d1d7705`-family hash, binary-searched by giants (prologue) and walked by dtors (`0xfd749dd6ef1fd0d4` tail) — treat namers as the same construct. 55. **XOR-8 carries ASCII code constants** (Battle.net band `0x14385c898`–`0x14385c9b4`; ruleset/result enums to `0x14385d180`).
56. **Retyping a measure block is a transcription hazard — and so is anchoring on the previous record's block** — paste from a saved run, diff before committing (pass-40 story in the archive).
57. **Window families grow by cascade** — pass 41's `FUN_14080c740` set and pass 42's name-window family (`FUN_1408314b0`…`FUN_1408493b0`, ratios to ~755) are the two largest; `size=` there is meaningless (ledgers 39/49).
58. **The `0x1421exxx` family is the UI row model** (~60 members; `FUN_1421e5100`
×536 record 45 → ×279 pass 46); the pass-42 144-stamp "ground" is one overlapping
window (ledgers 39/47/49); fields `0x3ff3/0x6003`, `0x229a`, `0x2d95`; nodes minted
as `0xa88000000000xxx` GUIDs.
59. **The pass-43 "hero count 0x13e = 62" is an arithmetic slip.** 0x13e is 318; chunk 0402 writes and compares 0x13e as the hero-select "none" sentinel. The roster/hero-table size remains open (T43-7); never quote 62 as measured.
60. **Census `cd360` counts `func_0x0001421cd360` (registration)** — the `FUN_141fcd360`/
`FUN_141fcd900` widget show/hide pair (chunk 0404) is a *different* function; `cd360 x0`
is correct despite the latter being called (pass 44; hex-collision class of ledger 7).

61. **Twin-test upgrade (pass 45)** — for large claimed twins, `diff` the bodies
modulo address/local renaming (pass 45's vote-screen giants: 51/1030 lines differ, all
local-name spellings) — canonical twin evidence, stronger than the ledger-47 ratio.
62. **Fifth hash family + twin-triple (pass 46)** — open-addressing ladder
`(x*0x1001+0x7ed55d16 → (h>>0x13^h^0xc761c23c)*0x21 → (y+0x165667b1)*0x200^
y+0xe9f8cc1d → *9+0xfd7046c5 → (z>>0x10^0x355a4f09^z)&cap-1` over 0xc-stride
{hash,next,key} rows (`FUN_1408f4fb0` rehash; channel-member + scoreboard-slot
tables); the friends set is a TWIN PAIR + shared reconciler
(`FUN_1408eaf20/1408eb720` → `FUN_1408eaf40` ×2 each) — unequal `size=` (27/5058)
makes the ledger-61 diff inapplicable across the pair; evidence = identical
prologue/chains/call-shape + `max refs:` naming only the twins.

**Closed/superseded (archive):** items 1–4, 6, 9–12, 14, 17–19, 21, 25, 28, 29, 35, 37, 38, 40, 42 — full text in `CODE_MAP_ARCHIVE.md` §Corrections archive.

## What the code is — cumulative synthesis (46 passes; evidence unless marked [inference])

`.text` is catalogued in entry-address order. After 427 chunk indices (`0000`–`0426`) the
cursor is at `0x1408f95b0` (20.43 % of functions, 16.36 % of `.text`). Names printed
`func_0x…` have **no decompiled body in this dump** — registrar/decryptors/writer/helpers,
the `0x140543xx0`/`0x1405674xx` decoders, settings accessors, component getters, hotfix
HTTP, CSV, pass-32 cipher, render tier, time/random, slot maps, `0x140f49xxx`/
`0x140f1exxx`/`0x140d2xxxx`/`0x140d5xxxx`, `tls_callback_0`.
**Six layers, in address order:**

1. **Library preamble** `0x140001000`–`0x140039fc0`: ISA-L/igzip inflate, NVAPI bootstrap + 53 wrappers.
2. **NVIDIA driver-loading shim** `0x14003a230`–`0x14003d330`: replacement `LoadLibrary` for `nv*.dll`.
3. **CRT/C++ static-init sea** `0x14003ffe0`–`0x1400fa760`: five generator templates (181-B magic-static ×2,451; 209-B locale ×354; 58-B event thunks ×284; 134-B XOR-40 ×61; 37-B `_onexit`).
4. **Typed registry machine** `0x1400fbcb0`–`0x14054ea50` (CLOSED): nine constructs (name buffers, registration, builder, copy wrapper, sorted-insert, `{id,hash}` ×326, nested-atexit, settings registrar, CompilerIDFilter).
5. **Runtime bootstrap + obfuscated dispatchers** `0x14053f6b0`–`0x14058200x`: PE entry, sig scanner, anti-tamper, masked-pointer layer.
6. **Engine runtime** `0x14054fea0`→ (passes 28–46, **OPEN**). Cumulative halves, newest first:
   **(46) post-round social & group-management stack** — award-detail
   screens (tier ladder `FUN_1408d4f80`, POTG nominees `FUN_1408d6740`,
   shuffle template ×3); the achievement-unlock belt (`FUN_140913/915/
   916xxx` families + apply transaction `FUN_140610980/140610c60`);
   hero-focus switch `FUN_1408dd7f0` (handle/component chains live);
   social quick-menu (hero table `DAT_14304c240` ×13) + voice-channel
   engine (**fifth hash family**, ledger 62; `FUN_1408e2e10` ×202);
   endorsement cards (levels 1–5, gate `+0x119/+0xc0/+0x124`);
   introsort ×2; profile tabs + filter enums; K/M/B/T + K/D
   formatters; async profile-view request blocks; **friends giants
   `FUN_1408eaf20/1408eb720` + shared 66-K `FUN_1408eaf40`** (ledger
   62); group management (6-entry LRU cache, observer pair, slot
   registry, 5-hero-slot picker); group browser (contribution graph,
   LFG roster, map-detail switch); scoreboard master `FUN_1408f62a0`
   (role switch `+0x2d` 0/1/2/3/5/6), 5-state async loader, and the
   battle-tag validator `FUN_1408f9340` (`vt+0x238("0x3FC88BB5",
   "0x4755E040",0x9d)` telemetry tags);
   **(45) hero-record engine + match-end award ceremony** — hero-info
   data layer + dispatchers `FUN_1408aca30/1408b8900`; RTTI master
   `FUN_1408b3780`; `0x1408bfxxx` row API (T44-5 closed); 15-member
   reconcile family (row key `0x41cb`); observer ladder; kill-cam;
   vote-screen twins `FUN_1408c8960/1408cb770` (ledger 61,
   round-state `0x7f2`); post-round summary `FUN_1408cef90` + redraw
   walker `FUN_1408d20e0`;
   **(44) in-match presentation stack** — hero-select tail, elim-feed/kill-cam,
   scoreboard (0x328-B rows, `0x9b<field>` sorts), ~40-screen ctor belt, HUD +
   team-composition giant `FUN_140897dc0`, hero-info/career screen (zero-gap);
   **(43) settings/menu/social/BattlePass/hero-select UI tier** — settings trio
   + interdependency engine, kill-feed giant `FUN_1408551d0`, BattlePass system,
   social tier (two compiled regexes), hero-select assembly engine (sentinel
   0x13e=318, Correction 59);
   **(42) lobby rules tier + voice client + name-window family + hero-actor** —
   5-slot HUD binding, 'VoiceClient' + 18-id cvars, ~200-fn rules over seven
   0xd0-stride banks, name-window family (one window, ledger 58);
   (41) hero ability/weapon/stat system + widget-factory belt + entity-view/HUD
   tier — 0x2a10-B hero entity, ~2000-case stat getter `FUN_1408038e0`, the
   **114-K window family** `FUN_14080c740`-set, factory registrar
   `FUN_141c4b050`; (40) match/join + hero-select + media; (39) party/voice/chat
   client; (38) UI-window engine; (37) map/scene + live-ops; (36) store/VC,
   telemetry, SAPI/Steam; (35) social + monetization; (34) replay/cinematic;
   (33) presentation; (32) gameplay loop; (31) match receive; (28–30) infra
   (~150-subsystem composition, containers, cvars, workers, bitstream, CSV).
   [inference: `0x14054fea0` marks the end of data registration and the start of behaviour.]

**Layer 6 construct index (per-pass detail + addresses in the records):** *infra* (28–30),
*match receive* (31: bitstream ×341/×248, dispatcher, saved-match, JSON serializer), *gameplay
loop* (32: event bus, entity runtime, master tick, JSON text engine), *presentation/social*
(33: VFX engine, 0x18a0-B record), *replay/cinematic* (34: demo system, chat/Markdown),
*store/social* (35: StoreSystem_C, ruleset ids, stat layer), *store completion* (36:
`__PlaceOrderWithVirtualCurrency`, SAPI), *map/live-ops* (37: 12-state load machine,
patch-note client), *UI engine* (38: window cache, springs, `FUN_140798f80`), *party
*match/media tier* (40: hero-select `FUN_1407e1e40`, match-history `FUN_1407ed2e0`,
result/media builders, generational handles `FUN_1407dd910/9c0/a70`, roster, kill
feed), *hero-ability tier* (41: hero entity `FUN_140802620/2660`, stat getter
`FUN_1408038e0/ed0`, window family `FUN_14080c740`-set, screens, entity-view),
*lobby/rules tier* (42: HUD `FUN_14081dfe0`, voice `FUN_140837fa0`, rules
`FUN_140827790`-set, name windows, summary `FUN_1408493b0`); *UI/menu tier*
(43: settings `FUN_14084b060/b750/bfb0`, kill-feed `FUN_1408551d0`, BattlePass
`FUN_14085c850`-set + pages `FUN_14085f600`, invite/groups/chat/stats, hero-select
`FUN_1408722a0/872b90`); *presentation stack* (44: hero-select tail, elim-feed,
scoreboard `FUN_140882470/1408831d0/1408845b0`, HUD `FUN_1408935a0/140897dc0`,
hero-info screen `FUN_14089efe0–1408a6750`); *hero-record/award tier* (45: data
layer `FUN_1408a6970–1408aadc0`, dispatchers `FUN_1408aca30/1408b8900`, RTTI
master `FUN_1408b3780`, row API `FUN_1408bf070–1408bf5c0`, reconcile family
`FUN_1408bc150–1408beb50`, vote twins `FUN_1408c8960/1408cb770`, summary
`FUN_1408cef90`, redraw walker `FUN_1408d20e0`); *post-round social/group tier*
(46: unlock belt `FUN_1408d8490–1408d9250`, hero-focus `FUN_1408dd7f0`,
quick-menu `FUN_1408dfe70`, channel engine `FUN_1408e1b90/1408e2e10`,
endorsement `FUN_1408e43e0`, sorts `FUN_1408e6b00/1408f0420`, friends giants
`FUN_1408eaf20/1408eb720/1408eaf40`, groups `FUN_1408ee060/1408eeac0`, LFG
`FUN_1408f11f0`, scoreboard `FUN_1408f62a0/1408f6d50`, battle-tag
`FUN_1408f9340`).

**Where the data lives** (full table in the archive; live additions):

| band | content |
|---|---|
| `0x143848d40`–`0x143861200` | XOR-8 name/payload ciphertext, extending pass by pass (settings/UI/party/store/map/widget names ≤ 41; 'Unknown' belt `0x14385d1a0`–`ddf0` 41; voice/device `0x14385f158`–`f348` 42; BattlePass pages `0x14385f9e8`–`fc24` + chat-regex `0x1438604d0/4e8` + 12 log pages 43; hero-info pagination `0x1438606c8`–`09f4` + settings-error pair `0x143861180/1200` 44; account-banner `0x143860a00`–`0b14` + highlight page `0x1438608f8/904` 45; **in-place pairs `0x143860ba0/bac` + `0x143860be0/bec` 46**; lobby-loc config `0x143860d98`–`e20` next) |
| `0x1438b8e50`–`0x1439fa330` | registry ciphertext; triplet-stub page |
| `0x143a155xx`–`0x143b81a0x` | XOR-40 keys, settings names, runtime block (~250 feature flags `0x143b945b8–0x143b9c5c0`), **pass 40: settings/observer block `0x143b90c30–0x143b90ea8`** |
| `0x143cf0000`+ | RTTI, reg outputs, settings descriptors, config globals; pass-40 null-match GUID `0x143b83da0–dc` |
| `0x1441e18f0`+ | plaintext reg outputs, struct schemas, record pools; TLS RNG base `0x144180fa0`, time scale `0x14415f7c8/f7f8` |

**What it is for.** Layers 1–2 are a vendored NVIDIA/igzip preamble; layer 3 compiled-in C++
static init; layer 4 registers ~8 k encrypted type names; layers 5–6 are the client —
infra (28–30), match receive (31), gameplay loop (32), presentation (33), replay (34),
social/store (35–36), map/UI engine (37–38), party/voice (39), match/media (40), hero
stats (41), lobby rules (42), menu/UI (43), presentation (44), hero-record/awards (45),
and the post-round social & group-management stack (46). No plaintext game protocol
(entity traffic is the bitstream; replays reuse it); the render device is
`FUN_141ff40f0` (lifecycle mapped). Confidence: counts/shapes/bands measured;
construct labels are shape-based inference; obfuscated bodies read structurally only.

**Known limits.** (a) `func_0x…` bodies absent (synthesis list; offcuts: `0x14068xxxx`,
`FUN_141da/141db`, `FUN_14099xxxx` store API (consumers to 46), `FUN_140d1xxxx` sound,
render tier, `0x140f49xxx`/`0x140f1exxx`, `0x140d2xxxx`/`0x140d5xxxx` (consumed 44),
`0x140a6xxxx` (consumed 44/45), `0x140912xxx–0x140916xxx` + `0x14091axxx` defs ahead
(T44-1/2, next pass)). (b) XOR-8 keys are per-record salts. (c) `0x142f0…`–`0x142f2b…`
thunks absent. (d) Corpus gaps: pass 30's
12 × >1 KiB; pass 34: 4 holes / 11,844 B; pass 35: 6 / 18,531 B; pass 36: 2 / 6,068 B;
pass 37–39: 0 holes; pass 40: 1 hole / 1,033 B (`0x1407efae0→0x1407eff20`, T40-6);
pass 41: 0 holes; pass 42: 1 hole / 8,015 B (`0x14083d280→0x14083f2c0`, T42-1 —
`--offcuts` pending); pass 43: 1 hole / 1,601 B (`0x14084b750→0x14084bfb0`, T43-1);
pass 44: 0 holes (98.1 % span); pass 45: 0 holes / 1 giant-window /
1 offcut-in-body (97.6 % span); **pass 46: 1 hole / 1,527 B
(`0x1408e0be0→0x1408e1260`, window-tail inference — T46-1) + 1 giant+offcut
(`FUN_1408df2d0`'s own window; 96.5 % span)**.
(e) Window chunks per ledgers 39/47/49/53/57/61: the pass-37/38 window-cache set, the
pass-41 `FUN_14080c740` set, and the pass-42 name-window family
(`FUN_1408314b0`…`FUN_1408493b0`, ratios to ~755) are the large cascades — `size=`
meaningless there; pass 43's three giants are real bodies; pass 44's giants have
direct callers; pass 45's largest bodies are the vote-screen verbatim twins
`FUN_1408c8960`/`FUN_1408cb770` (57.8 KB, diff 51/1030 lines modulo rename —
ledger 61); **pass 46's largest bodies are the friends-screen set — twin giants
`FUN_1408eaf20/1408eb720` + shared 66-K `FUN_1408eaf40` (ledger 62; `FUN_1408eaf20`
size=27 vs 49.6-K body) plus the highlight controller `FUN_1408df2d0` (window,
offcut call into itself)**.

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
| **Event post (40)** | `func_0x000140c28eb0(_DAT_143b7f410)` or group svc `(svc+0x3c3b9d672a4416a4)^0xf9798462dc0addd7` → `(**vt+0x18)(svc,id)`, ids 0x22–0x54; the app-service event bus | `0x1407d06a0` |
| **Retire idiom (34→41)** | `0x20000`-flag guard + `(**vt+0x158)/200/0x160` + `FUN_1421522e0/14214eb70/14214d400` + `+0x914` sentinel; inlined in obfuscated giants | `0x1406xxxx` |
| **Widget factory (41)** | create-stub pair + XOR-8 name page (0x18-stride name+key, 'Unknown' belt) + `FUN_141c4b050(&desc,&name,0x14,size,0,id)` — 62 calls pass 41 | `0x1407fd0a0` |
| **Entity-root chain (41)** | `(x+0x1e2421a4798a328>>0x22|x*0x40000000)^0xe1379e3cb308170d` → `>>0x2b|<<0x15` root — sibling of `0x4d79452d486f9431` | `0x140801400` |
| **Name-window triple-mix (42)** | `((x^0xeb)+0x2d1d7705)>>0xb|x*0x200000 ^ [0x143b79598+0xb5] ^ 0x998fae39` → `>>0x15|x<<0xb +0xd2e288fb ^ DAT_143847f0a` + `0x4d79452d486f9431` root — the player-name window family's hash | `0x14082f100` |
| **List API `0x1421exxx` (42→46)** | the **UI row model** (~60 members, ledger 58): `40c0/3c20/3330/3420` child-list get, `5100` begin, `52c0` node-at, `3de0…3920` getters, `41d0…4170` setters, `52a0/5370/5310` list ops, `51d0…5230` row ctors, `4140` type test, `4af0` node-by-type; fields `0x3ff3/0x6003` child lists, `0x229a` value GUID, `0x2d95` row key; `FUN_1421e5100` ×536 record 45 → ×279 pass 46 | `0x1408493b0` |
| **Player-list lock (42)** | `DAT_143b945b0` 0x400-spinlock (`FUN_141c5c3d0` escalate) + `DAT_143b945b4` disable flag over the three global arrays `PTR_DAT_14385f3b0/3f480/3f4f0` — the scoreboard's data source (T9's flag block, protocol read) | `0x140842fe0` |
| **JSON DOM + writers (43)** | node ctors/readers fully mapped consumer-side: `FUN_141940c00/ea0/e00` + `141940ef0` property set + `141941360/141941440` array + `14193e0d0/93e940/93ef80/93f510/93f560/93e5c0` readers + `FUN_140693130/1406935f0/1406934c0` writers + `func_0x00014213ee60` compact writer (0x14213f7df siblings) + posters `FUN_140840db0/140840e90` + pools `DAT_144137230/250` | `0x14084f530` |
| **UI screen tier (43–46)** | ctor = base + vtable + `0xa88000000000xxx` guid; node mint `__RegisterWaitForSingleObject(list,type,0)`/`FUN_140726800`; widget chain `FUN_1422544f0`→`1421f1780/1610`→`142255180/330`→`1421ee370/7d0`→`FUN_14224eec0/14224f390`; **reconcile template** = child-list match by node type + row key (`0x41cb` int or string `0x621f`), stale retire `FUN_1405651e0`, mint (45 ×15; 46 +10 node types incl. string-keyed); sorts `FUN_140856550/1408666c0/140871270` + locale pair + **introsort `FUN_1408e6b00`/`FUN_1408f0420` (46)**; hash-set `(x*0x40000+~x)*0x15*0x41` (`FUN_1408e2e10` ×202, 46); scoreboard `0x9b<field>` ids + `0x926036` sentinel, map GUID `|0x2e…`/`|0xb3…`/`|0x1f6…`, handle `(h&~0x3f)` decode, round-state `0x7f2`; map-detail switch `FUN_1408f2820`, LRU group cache, 5-state async loader, slot registry `DAT_1441b8130` (46) | `0x140849a10` |

## Open threads (cheapest next query each; check/update every pass)

2/5. **Entity transport framing** (client found 32, socket ahead) + **command ids** — base `0x48/0x53/0x7c/0x7d/0xa5/0xb2/0x3a`; grown 32–41 (pass 41: audio 0x8d, ability ids 0x6b/0x655/0xf5/0x580/0x1e; **pass 43: queue events 0x631b/0x6334, hero events 0x664e/0x66b7/0x6521, claim events 0x12e58–0x13223**).
7/9. `FUN_141c295b0`/`FUN_141c58170`/`FUN_142d2cf30` bodies unread (~chunk `15xx`); the `0x143b945b8`–`0x143b9c5c0` flags' writers pending (lock protocol read pass 42).
11–12. Channel-list renderer (writer found 32, renderer unfound); hotfix record dump `_DAT_1439d98c0`.
13. **Gaps** — pass 45: 0 holes / 1 giant (twin's own window) / 1 offcut (inside the giants' bodies); pass 44: 0 holes; pass 43: 1 hole / 1,601 B (T43-1); pass 42: 1 hole / 8,015 B (T42-1); `0x14059a007–0x14059c350` (9,033 B), `0x1401a4e02–0x1401abad0` (27,854 B) open.
15–16. Event-name table `0x143851c90` still encoded; pass-32–34 machinery bodies (cipher, emitters, samplers).
17–19. Handle-table writers (`grep 0x18317a531d116c`); `FUN_14099xxxx` store API (consumers 35/40–45); 'Unknown' belt `0x14385d1a0`–`ddf0` decode (122 pages).
21–23. Store endpoint labels (`0x1438595b0–0x1438597c8`); `FUN_140d1xxxx` sound (`crossref.py 140d1bcc0`); audio-channel id table (partial 41).
24–25. `0x8784b4333a5802xx` masked chain (`strlookup --band 0x1439dc5c0 0x1439dc630`); component-message ids (`0xd8…`/`0x5800…`/`0xde…`/`0x46…` families).
26–30. Widget names / UI-cache tables / render tier bodies `FUN_141ff40f0`-family (lifecycle closed 40) / live-ops flags (trail rows closed 38).
31–35. Material family (`crossref.py 142cb4c20`); `FUN_140c6xxxx` input; `FUN_1409bxxxx` appliers; `0xbd` input rows.
36–40. `0x142f2df90` fn-ptr table / `FUN_1407b0e90` stat fold / 18-key channel ladder / toast table `0x143059b80` / far-window regions `0x14213f7df`/`0x142045667`/`0x141c4b29c` — sweep when `window reach:` names a defining chunk.
41–55. T40/T41 items — serializer (`crossref.py 1407f2a00`) + twin (`142388ab0`);
time/random `FUN_141d11f60/141c4efa0`; observer blocks `0x143b90c30–ea8`;
pass-40 hole `0x1407efae0→0x1407eff20`; c740 window boundary; `FUN_142044820`
banks; factory screens' update bodies (`PTR_FUN_142fe6328/142fea6b0`).
56–63. T42-x — the 8,015-B hole `0x14083d280→0x14083f2c0`; list-API defs
`0x1421e0000+`; name-window boundary (`140adcec0`); map/mode enum table
(`142d37920`); player-array writers; `0x141bba761` region.
64. T43-1 the 1,601-B hole `0x14084b750→0x14084bfb0` — `--offcuts` when neighbours gain mentions.
65. T43-3 → T44-1: the settings-field defs `0x1409124b0+` (~20 categories / ~100 field GUIDs; **def region inside the next pass**).
66–69. T43-4 fn-ptrs `PTR_FUN_142f7d730/740`; T43-5 regex match side (`141b39f70`); T43-6 locale (`140c71110`); T43-7 sentinel 0x13e=318.
70. T43-8 → T44-2: the party-row widget defs ~`0x14091a000` (**def region inside the next pass**).
71–78. T44-3…T44-8 — `0x140d5xxx` ability-config (`crossref.py 140d56bf0`); `0x140a6xxxx`
hero-info state (`140a63a00`); `0xca…` RTTI family (`142d402d0`); `FUN_142d26xxx/142d29xxx`
writers (`142d26880`); new hashes `142697480`/`142159220`.
79–84. T45-1…T45-6 — vote-screen twin class slots (`crossref.py 1408cb4e0`); the
`0x7f2` round-state enum (writers `FUN_1408cfee0`); `_DAT_143b975a0` post-round
singleton (`143b975a0`); award-pool `0x580000000000d70` siblings (`142149490`); the
`0x129b0`/`+0x251` dirty flush (`140564e60`); the `0x18317a531d116c` bucket table.
85–91. T46-1…T46-7 — the `0x1408e0be0→0x1408e1260` hole (1,527 B, window-tail
inference); the friends-twin class's remaining slots + the `0x1408ff4c0` row family
(defs next pass); the fifth hash family's builder (`crossref.py 1408f4fb0`); the
`DAT_1441b8130` slot registry (`crossref.py 141fd41d0`); the 13-entry hero table
(`crossref.py 14304c240`); the `vt+0x238` telemetry tags (`crossref.py 14214dc60`);
`FUN_1408f6d50`'s 5-state machine (`crossref.py 141fd3970`).

CLOSED (machine): fd9670 recount; provenance; `0x1411b8070`; thread 43; T20; JSON
writer/parser/CSV; XOR-8 salt keys; presence events; closed ledgers in the archive.
Closings by pass: 36→T35-1/3; 37→T36-3; 38→T37-4; 39→T38-1; 40→render lifecycle;
41→T23 audio + belt; 42→T9 flags + voice client + field-id set; 43→T42-2 + row model
+ page table/regexes/JSON DOM; 44→T43-3/T43-8 consumer ground + zero-gap;
45→T44-5 row-API ground; **46→T44-1/T44-2/T44-6 consumer ground (defs ahead)**.

## Next pass

Resume range: **`NEXT.txt`** — written by `pass_next.py` from `state.json` + `--max`;
regenerate after every `--update`, never hand-edit. Pass 46 ends at `FUN_1408f95b0`
(the battle-tag close tail); stratum `0x14054fea0` OPEN; next = chunks `0427`–`0438`,
`.text` `0x1408f95e0`–`0x140934260`. Watch for: (a) **the lobby-location config
loader at the boundary** (`FUN_1408f95e0` decodes `showmodeLobbyLocations.json` +
the pod->lobby lookup error — the strscan look-ahead pages); (b) **the
`0x140912xxx` settings-field def region — T44-1 closes here**: `FUN_1409124b0`
and the whole `0x140913/915/916xxx` belt lie inside this range; (c) the
`0x14091axxx` party-row defs (T44-2: `FUN_14091a170/14091a480/14091a200/
14091b6a0/14091d9e0`); (d) the `0x1408ff4c0` friends-row family defs (T46-2);
(e) the `0x140a98xxx`/`0x140a99xxx` group-service ground. Do not re-run a counted
range through `--update` (ledger 5); never treat `0x826e…`/`0xca334801`/
`0x4343ffa4`-family or offcut-call addresses as data (ledger 20); ledgers
24/31/39/43/44/47/49/53/57/58/60/61/62 for gaps, windows, twins and the hash
families; `size=` is not coverage (ledger 30) — **paste, never re-type, the
measure block (ledger 56)**, and check the zone counts sum to `files=`.
