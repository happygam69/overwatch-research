# CODE_MAP — cumulative map of the systematic `.text` read

**Read in full before every pass; update after every pass. Hard budget: ≤300 lines**
(raised 250→300→350, re-tightened to 300 at pass 40 — Corrections 56).
Per-pass narrative lives ONLY in `ranges/`; cumulative numbers come from `state.json` —
never hand-add. Long-form archive: `CODE_MAP_ARCHIVE.md`.

## Files

| file | role |
|---|---|
| `chunks/chunk_NNNN.txt` | corpus, address order; unreachable-block warnings stripped 2026-11-21 (counts in `index.json`) |
| `index.json` / `state.json` | per-chunk bytes/first/last (coverage truth) / machine ledger: next_chunk, passes, totals, reg hashes, 326 `{id,hash}` rows |
| `scripts/pass_next.py` / `NEXT.txt` | resume range from `state.json.next_chunk` + the `--max` cap; `NEXT.txt` is its generated output — never hand-edit |
| `scripts/pass_measure.py` / `ranges/*.md` | canonical per-pass measurement (quoted verbatim or `--json` digest; `max refs:` = auto-crossref of the range max) / per-pass records — the evidence base |
| `scripts/gap_report.py` | per-range gap classes (`giant`/`offcut`/`hole`; `--offcuts` = corpus sweep) + `window reach:` far-window watch list (ledger 53) |
| `rdata_names.tsv`/`scripts/rdata_names.py` | plaintext `.rdata` strings (16,832 rows) / regenerator; query via `strlookup.py --pool rdata_names.tsv` |
| `docs/*.md` | reader-facing findings: plain-prose subsystem pages; no line budget, milestone-only; conclusions cite records |

## Coverage

Corpus: 2,228 chunks, 119,757 functions, 42,864,695 B `.text`. Passes 1–22 archived; `state.json` is the truth; pending range is `NEXT.txt`.

| pass | chunks | `.text` range | functions | record |
|---|---|---|---|---|
| 23–33 | `0193`–`0306` | `0x1404192e0`–`0x14069b460` | 5,537 | `ranges/` rows 23–33 (archived detail) |
| 34–42 | `0307`–`0394` | `0x14069bb80`–`0x1408493b0` | 3,639 | `ranges/0x14069bb80-…` … `0x14081d520-0x1408493b0.md` |
| 43–47 | `0395`–`0435` | `0x140849a10`–`0x1409237a0` | 2,192 | `ranges/0x140849a10-0x140874660.md` … `ranges/0x1408f95e0-0x1409237a0.md` |
| 48–49 | `0436`–`0452` | `0x140923c20`–`0x14097f6b0` | 774 | `ranges/0x140923c20-0x14094f5c0.md`, `ranges/0x14094f840-0x14097f6b0.md` |
| **50** | `0453`–`0460` | `0x14097f810`–`0x1409ab600` | 528 | `ranges/0x14097f810-0x1409ab600.md` |
| **51** | `0461`–`0470` | `0x1409ab8e0`–`0x1409d0cd0` | 410 | `ranges/0x1409ab8e0-0x1409d0cd0.md` |
| **52** | `0471`–`0483` | `0x1409d1050`–`0x1409f4b30` | 295 | `ranges/0x1409d1050-0x1409f4b30.md` |
| **53** | `0484`–`0494` | `0x1409f4bc0`–`0x140a0da80` | 289 | `ranges/0x1409f4bc0-0x140a0da80.md` |
| **total** | **495 indices, `0000`–`0494`** | `0x140001000`–`0x140a0da80` | **27,196** | machine-verified (`state.json`) |

Machine-verified (`state.json` after pass 53): files 27,196 (22.71 %), Σ `size=`
8,009,886 (18.69 %); classes reg 7,956 / wrapper 1,954 / builder 1,717 / sorted 280 /
atexit 261 / record 326 / other **14,702**; 7,956 registration calls = 7,952 ciphertext
+ 4 plaintext (7,955 distinct; one plaintext hash ×2 — Corrections 16); `d4f30` 1,188
/ `d4f70` 1,350 / `d4fb0` 4,492 / `c2d70` 4,212 / `c2d50` 326 / `c7880` 261 / `atexit` 316; records 326. Passes 27–53 = consumer only.

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
58. **The `0x1421exxx` family is the UI row model** (~60 members, ledger 58; counts tracked in the conventions row); nodes minted as `0xa88000000000xxx` GUIDs.
59. **The pass-43 "hero count 0x13e = 62" is an arithmetic slip** — 0x13e is 318, the hero-select "none" sentinel (T43-7 open); never quote 62 as measured.
60. **Census `cd360` counts `func_0x0001421cd360` (registration)** — the `FUN_141fcd360`/`FUN_141fcd900` widget pair (chunk 0404) is a *different* function; `cd360 x0` is correct (hex-collision class of ledger 7).

61. **Twin-test upgrade (45)** — for large claimed twins, `diff` the bodies modulo address/local renaming — canonical twin evidence, stronger than the ledger-47 ratio.
62. **Fifth hash family (46)** — open-addressing ladder `(x*0x1001+0x7ed55d16 → (h>>0x13^h^0xc761c23c)*0x21 → (y+0x165667b1)*0x200^y+0xe9f8cc1d → *9+0xfd7046c5 → (z>>0x10^0x355a4f09^z)&cap-1` over 0xc-stride {hash,next,key} rows (49: the audio-command table `FUN_140971460`); friends set = twin pair + reconciler.
63. **`FUN_1409054a0` (47, size=8 vs 5050-B body) leaves its own four sub-entries inside its span** — treat the following decompiled set as the window's arms. 64. **A hole whose predecessor's reach lands inside the next entry's giant is one span, not two gaps** (48's `0x1409487d0→0x140949130` midsection); 49's three giants are all this class.
65. **Pass 50's three giants are one cascade** — `FUN_14099c9f0` (48.1 K) + `FUN_14099d190` + `FUN_14099d330` (47.2 K) share the `0x1409baxxx–0x1409bbxxx` window (halting fabrications from `0x1409bb09a`); `crossref.py` on the range max shows no second namer. **Plaintext names exist inside the stratum** — `StoreSystem_C::{LoadProductCatalog,FinishRequestingExternalProducts,RequestDynamicBundlePrice,RequestGenericProductSetRefresh,RequestNewGenericProductSet}` and vendored MFC `CVSToolsListBox`/`CMFCToolBarsToolsPropertyPage` (chunk 0459).
66/67. **Far-window stamps are fabrication artifacts, not unread code (51)** — `0x141c4b29c` = a vt+0x58 jumptable (giant `FUN_1409ce9f0`, 0469), `0x1421ad73b` = the spinlock helper `FUN_141c5c3d0` (0467), `0x140a46a19` = the shared PIC-fabrication zone of the pass-51 giants. **Roster-window ctor collision (51)** — the fabricated ctor block inside `FUN_1409b1470`'s window is the named `FUN_1409c8040` (0x1b40-B; +0x210 = 0x13e sentinel, 64×0x40 rows at +0xa38, `PTR_FUN_142f7d730/740`, `func_0x000141c4aea0(+0x1a98,0x40)/(+0x1ab8,0x18)`, `func_0x000141bb8e80(+0x1b10)`); treat the giant's ctor half as that body.
68. **Pass 52: the replay/highlight file layer has its own error text and status codes** — `FUN_1409ea7d0` writes `{u16 code, u64 detail, char text[0x100]}` with **0x202** (manifest deserialize) / **0x203** (manifest read) and the 5 XOR-8 format strings `0x143865E48-0x143865F30`; the share code is `prefix + base64(payload 0x30/0x50/0x58) + base64(hash 0x20)` (`FUN_1409e8e00/1409e9430`), and `FUN_1409f4b10`/`FUN_1409f4b30` are the **same body twice** (896 normalised lines, ratio 0.9967, 3 differing lines) — ledger-61 twin evidence, cheapest diff yet. Also: the pass-51 "custom-game predicate" `FUN_1409d2480` is a **self-identity test** (local-player id pair at session-table `+0x1b0/+0x1b8`), not a mode test — T51-1 closed.
69. **`0x140a0xxxx` is REAL CODE, not a fabrication host (53)** — `0x1409fc290`–`0x140a0da80` is 289 clean entries (chunks 0488/0489: 167 with zero `halt_baddata`/PIC warnings); the pass-52 "window host" label covered it wrongly. Real far-window reach below `0x140a0da80` = a real call; above it check for an entry first (T53-1: `0x140a1b770` is a real body with no decompiled entry). Also: **`0x1426c…` is the CRT math band** — `1426c40f0` sincos (packed 2 floats), `1426ce1e4` atan2, `1426cdfc8` asin/acos, `1426c3d40` stack-cookie check (29 epilogues in pass 53).
70. **Pass 53's widget class band is `0x1430636e0`–`0x14306be9x`** — 158 refs, 44 ctors install `PTR_FUN_14306…` with MI thunks through `param_1[1]` (vtable-offset table) and `PTR_FUN_143048228` as the universal no-op sibling; child draw pass classifies 5 RTTI tags `0x143fde030/190/2f0/460/720` and calls `FUN_141d01100/1400/15b0`. The 3×4 transform constants are `0x14328cdc0..cdec` (r0/up/forward) with white at `0x14328cd40..cd4c`; `0x143a1a9f0..aa3c` is the quaternion→matrix XOR-float table.
**Closed/superseded (archive):** items 1–4, 6, 9–12, 14, 17–19, 21, 25, 28, 29, 35, 37, 38, 40, 42 — full text in `CODE_MAP_ARCHIVE.md` §Corrections archive.

## What the code is — cumulative synthesis (53 passes; evidence unless marked [inference])

`.text` is catalogued in entry-address order. After 495 chunk indices (`0000`–`0494`) the
cursor is at `0x140a0da80` (22.71 % of functions, 18.69 % of `.text`). Names printed
`func_0x…` have **no decompiled body in this dump** — registrar/decryptors/writer/helpers,
the `0x140543xx0`/`0x1405674xx` decoders, settings accessors, component getters, hotfix
HTTP, CSV, pass-32 cipher, render tier, time/random, slot maps, `0x140f49xxx`/`0x140f1exxx`/`0x140d2xxxx`/`0x140d5xxxx`, `tls_callback_0`.
**Six layers, in address order:**

1. **Library preamble** `0x140001000`–`0x140039fc0`: ISA-L/igzip inflate, NVAPI bootstrap + 53 wrappers.
2. **NVIDIA driver-loading shim** `0x14003a230`–`0x14003d330`: replacement `LoadLibrary` for `nv*.dll`.
3. **CRT/C++ static-init sea** `0x14003ffe0`–`0x1400fa760`: five generator templates (181-B magic-static ×2,451; 209-B locale ×354; 58-B event thunks ×284; 134-B XOR-40 ×61; 37-B `_onexit`).
4. **Typed registry machine** `0x1400fbcb0`–`0x14054ea50` (CLOSED): nine constructs (name buffers, registration, builder, copy wrapper, sorted-insert, `{id,hash}` ×326, nested-atexit, settings registrar, CompilerIDFilter).
5. **Runtime bootstrap + obfuscated dispatchers** `0x14053f6b0`–`0x14058200x`: PE entry, sig scanner, anti-tamper, masked-pointer layer.
6. **Engine runtime** `0x14054fea0`→ (passes 28–53, **OPEN**). Cumulative halves, newest first:
   **(53) UI widget class library of the `0x140a0…` band** — 44 widget-class ctors
   (vtable band `0x1430636e0`–`0x14306be9x`, MI thunks through a `param_1[1]`
   offset table, `PTR_FUN_143048228` no-op sibling) + dtor belt + 12 draw
   trampolines (`vt+0x1c0` visible → `vt+0x160` draw context → slot
   `+0x28/30/40/48/50/78/80`) + `FUN_140a05990` property→vec4 getter (83 callers)
   + child draw pass over 5 RTTI tags + attribute-observer lists on the ledger-36
   type table + **replay/camera playback controller** (cmd `{+0x18 tick,+0x30 op
   1=seek/2=duration/3=window}`, progress `+0x33c`, entity `+0x1350..135c`) + **timeline
   API `0x140da/0x140db`** (`dbcf70` obj, `daf8f0` find, `da44e0` insert, `db0470` sample,
   `dbcba0/aa0/cb00` min/max/scalar) + 3×4 transform widgets (sincos `1426c40f0`) +
   0x500-B marker ring buffer, per-tick `(elapsed+rem)/period`; **(52) marker/
   spectator-overlay + replay-highlight tier** — roster TTL cache
   (0x328 rows, 60 s) + game-mode belt 1..0xf; world-space marker motion + draw-call
   builder (tags `0x10a1`/`0x11a1`, sub `0x30e0`); HUD element builder (props
   `0xdc…050a–050f`, texts `0xde…4533–453a`); 5-series graph overlay; 0x178-B roster
   rows + introsort; gate bitmask (18 flags); **highlight share code** (base64 +
   seeded hash, layouts 0x30/0x50/0x58) + bit-packed serializer + **`manifest.json`
   loader** (0x202/0x203, 0xf0-B chunks) + 5-slot streaming client; nameplate widgets;
   **(51) cosmetic/aim/roster/spectate/voice/role tier** — cosmetic-attach svc
   (0xe0 rows TTL 600, 0x220 states, 0x10 refs cap 700); area-effect proximity grid;
   aim-assist (DualZone/LinearRamp/ExponentialRamp); roster UI (0x178 rows, '%s (%s)');
   spectator stack (world→screen, camera `entity+0x250→+0x820→+0x1c10`); voice
   channels (188-entry mute bitmap); 8-slot role registry over `0x1421exxx`;
   **(50) store engine + weapon/loadout tier** — JSON-DOM event-handler tier
   (573/239/146/128 resolvers, reward/challenge fills, replay-bookmark ingest);
   **group-roster engine** (`FUN_140987890`, 0x328 rows, two introsorts, 108-stub
   interface belt); hero-weapon VFX float engine (recoil springs, TLS-RNG);
   **`StoreSystem_C`** catalog/purchase (T49-1 closed: 76-member Battle.net error enum);
   store UI model + CRC32 image cache + loot boxes; render-object/weapon-transform
   cascade (one window, ledger 65); **weapon-loadout engine** (`DAT_143b8d290`,
   highlight magic `0x56c6870`); loadout-apply tier (2nd XOR-float table
   `0x143a1aa10-aa3c`); vendored MFC `CVSToolsListBox`; **(49) settings-backend /
   platform-services tier** — video/graphics engine (enum belt 0x191/0x1b9/0x1f0/
   0x1f2/0x22b); **web-view/JS-bridge** (FNV-1a registry, modal router); camera
   controller; VO resolver; highlight-save media; file streaming;
   (48) social/party/lobby + custom-game settings engine (lobby rows, party
   carousel, settings state engine `0x1409484c0`–`0x14094f5c0`); (47) summary/
   awards + def belts; (46) post-round social & group stack (fifth hash family);
   (45)–(43) hero-record/awards + in-match presentation + settings/menu/
   BattlePass/hero-select screen tier; (42) lobby rules + voice client +
   name-window family; (41) hero ability/weapon/stat system + widget-factory belt;
   (40) match/join; (39) party/voice/chat; (38) UI-window engine; (37) map/scene
   + live-ops; (36) store/VC, telemetry, SAPI/Steam; (35) social + monetization;
   (34) replay/cinematic; (33) presentation; (32) gameplay loop; (31) match
   receive; (28–30) infra (composition, containers, cvars, workers, bitstream, CSV).
   [inference: `0x14054fea0` marks the end of data registration and the start of behaviour.]

**Layer 6 construct index (detail + addresses in the records):** *infra* (28–30);
*match receive* (31: bitstream ×341/×248, dispatcher, saved-match); *gameplay loop*
(32: event bus, entity runtime, master tick, JSON text engine); *presentation* (33:
VFX engine, 0x18a0-B record); *replay/cinematic* (34: demo system, chat/Markdown);
*store/social* (35–36: StoreSystem_C, ruleset ids, `__PlaceOrderWithVirtualCurrency`, SAPI); *map/live-ops* (37: 12-state load machine); *UI engine* (38: window cache, springs, `FUN_140798f80`); *party client* (39: spawn solver `FUN_1407a8a70`, slot engine `FUN_1407c9480`);
*match/media tier* (40: hero-select `FUN_1407e1e40`, match-history `FUN_1407ed2e0`, generational handles `FUN_1407dd910/9c0/a70`, roster); *hero-ability tier* (41: hero entity `FUN_140802620/2660`, stat getter `FUN_1408038e0/ed0`, window family `FUN_14080c740`-set, entity-view); *lobby/rules tier* (42: HUD `FUN_14081dfe0`, voice `FUN_140837fa0`, rules `FUN_140827790`-set, summary `FUN_1408493b0`); *UI/menu tier* (43: settings `FUN_14084b060/b750/bfb0`, kill-feed `FUN_1408551d0`, BattlePass `FUN_14085c850`-set, hero-select `FUN_1408722a0/872b90`); *presentation stack* (44: scoreboard `FUN_140882470/1408831d0/1408845b0`, HUD `FUN_1408935a0/140897dc0`, hero-info screen `FUN_14089efe0–1408a6750`); *hero-record/award tier* (45: data layer `FUN_1408a6970–1408aadc0`, RTTI `FUN_1408b3780`, row API `FUN_1408bf070–1408bf5c0`, vote twins `FUN_1408c8960/1408cb770`); *post-round social/group tier* (46: unlock belt `FUN_1408d8490–1408d9250`, channel engine `FUN_1408e1b90/1408e2e10`, friends giants `FUN_1408eaf20/1408eb720/1408eaf40`, groups `FUN_1408ee060`, scoreboard `FUN_1408f62a0/1408f6d50`); *post-round summary/data tier* (47: map-stat master `FUN_1408fba90`, summary engine `FUN_140905280–140909e10`, **settings def belt `FUN_1409124b0–140917120`**, **party dispatcher `FUN_14091a4c0`**, award belt `FUN_1409207b0–1409237a0`); *social/party/lobby tier* (48: hero-filter `FUN_1409262b0`, lobby-browser `FUN_140929cb0`, roster build `FUN_14092c130`, lobby-player rows `FUN_14092f020–140930130`, team-player router `FUN_1409366e0`, roster shuffle `FUN_140939030`, team-member card `FUN_14093c8c0`, party carousel `FUN_140941d80`, **party roster walk `FUN_140945f40` (range max)**, settings engine `FUN_1409487d0–14094f5c0`); *settings-backend/platform tier* (49: audio router `FUN_1409507e0`, video engine `FUN_140958580/14095bd80/14095cee0`, web-view master `FUN_140965f80` + JS dispatcher `FUN_140969640` + modal router `FUN_140968b80`, camera cvars `FUN_14096c290` + master `FUN_14096cb30` + 8-thread spawner `FUN_14096e240`, VO filter `FUN_140971780/140973d80`, highlight master `FUN_140977cd0/140979010`, chunk engine `FUN_14097a660/97ab40` + canary `FUN_14097b830`, Steam listeners to `FUN_14097f6b0`);
*store/loadout tier* (50: DOM resolvers `FUN_14098def0-14098dc40`, roster master
`FUN_140987890`, VFX float engine `FUN_140990550/1409910a0/140991950`, store
core `FUN_140993c80/140995520/1409957f0/140993710/140996880`, UI model
`FUN_14099a9e0`, transform cascade `FUN_14099c9f0/14099d190/14099d330/1409a9e30`,
loadout engine `FUN_14099f4d0/14099fc60/1409a1570/1409aaea0/1409ab600`, highlight
writer/validator `FUN_1409a3bf0/1409a0330` — full lists in the pass-50 record);
*cosmetic/aim/roster/spectate/voice/role tier* (51: attach svc `FUN_1409b0de0/1409b0bf0/1409b2560`, grid `FUN_1409b2ba0/1409b39e0/1409b4b40`, cache probe `FUN_1409b3040`, aim `FUN_1409ba390/1409ba800/1409bb350/1409bcd50`, roster `FUN_1409b6d30/1409b7af0/1409b84e0/1409b9a50/1409b6090`, spectate `FUN_1409c15d0/1409c27c0/1409c29c0/1409cc9b0/1409cc100/1409cf210`, voice `FUN_1409cb130/1409cd4c0/1409c1000`, role registry `FUN_1409cfa70/1409d02f0/1409d0950/1409d0cd0`).
*marker/spectator-overlay + replay-highlight tier* (52: TTL cache `FUN_1409d1ae0/1409d1c60/1409d1de0`,
mode belt + doc writers `FUN_1409d2f00/1409d3630`, marker motion + draw-call builder
`FUN_1409d7110/1409d5270`, element builder `FUN_1409da570`, graph overlay `FUN_1409de040/1409de740`,
roster rows/sort `FUN_1409e5040/1409e5810/1409e5cb0`, gate bitmask `FUN_1409df470`, **share code
`FUN_1409e8e00/1409e9430`, record serializer `FUN_1409e95e0/1409e9b50`, manifest
`FUN_1409ea7d0/1409ec2f0`**, chunk client `FUN_1409ed4c0/1409ed8a0`, clip index `FUN_1409ee4d0/1409ef270`,
widget subclasses `FUN_1409f3520/1409f3ff0`, twin windows `FUN_1409f4b10`/`FUN_1409f4b30`).

**Where the data lives** (full table in the archive; live additions):

| band | content |
|---|---|
| `0x143848d40`–`0x143865F30` | XOR-8 name/payload ciphertext, extending pass by pass. Belt digest: names + 'Unknown' (≤41), voice/device (42), BattlePass/chat-regex/log (43), hero-info pagination + settings-error pair (44), account-banner/highlight (45), in-place pairs (46), lobby-loc + `'steamid'` (47), the 7-page enum-name error belt `0x143861DA0–`0x143862208 (48), graphics-enum/web-view/modal/camera-cvar/streaming `0x143862320–0x1438631A0` (49), the store belt `0x143863e58–0x1438650xx` incl. the 76-member Battle.net purchase-error enum `0x143864110–C38` (50), aim-debug belt `0x143865208–468` + camera/voice strings (51), game-mode belt `0x143865878–A08` + `':'` separators `0x143865DD8/DE8` + 5 manifest formats `0x143865E48–F30` (52). **Pass 53 adds no page: this tier is stringless.** |
| `0x1430636e0`–`0x14306be9x` | **UI widget class band (53)**: 158 refs — class vtables `PTR_FUN_14306…`, vtable-offset tables `DAT_14306…` (adjacent pairs 12 B apart), thunks `PTR_LAB_14306…`; plus the tuning block `0x14306be14–be2c` read by the eased-interpolation body |
| `0x143fde030`–`0x143fde720` | **UI child-class RTTI tags (53)** — 11 tag objects passed to `(**(vt+0x10))(obj,&tag)`; 5 of them (`de030/190/2f0/460/720`) select the layout entry in `FUN_140a030c0` |
| `0x1438b8e50`–`0x1439fa330` | registry ciphertext; triplet-stub page |
| `0x143a155xx`–`0x143b81a0x` | XOR-40 keys, settings names, runtime block (~250 feature flags `0x143b945b8–0x143b9c5c0`), **pass 40: settings/observer block `0x143b90c30–0x143b90ea8`** |
| `0x143cf0000`+ / `0x1441e18f0`+ | RTTI, reg outputs, settings descriptors, config globals; plaintext reg outputs, struct schemas, record pools; TLS RNG base `0x144180fa0`, time scale `0x14415f7c8/f7f8` |

**What it is for.** Layers 1–2 are a vendored NVIDIA/igzip preamble; layer 3 compiled-in C++
static init; layer 4 registers ~8 k encrypted type names; layers 5–6 are the client —
infra (28–30), match receive (31), gameplay loop (32), presentation (33), replay (34),
social/store (35–36), map/UI engine (37–38), party/voice (39), match/media (40), hero
stats (41), lobby rules (42), menu/UI (43), presentation (44), hero-record/awards (45),
post-round social (46), summary/awards + def belts (47), social/party/lobby + settings
(48), settings-backend/platform-services (49), store engine + weapon/loadout (50),
cosmetic/aim/roster/spectate/voice/role (51), marker/spectator overlay + replay/highlight
files (52), UI widget class library + replay playback/timeline (53). No plaintext game
traffic exists (entity traffic is the bitstream; replays reuse it); the render device is `FUN_141ff40f0` (lifecycle mapped).
shape-based inference; obfuscated bodies read structurally only.

**Known limits.** (a) `func_0x…` bodies absent (synthesis list; offcuts: `0x14068xxxx`, `FUN_141da/141db`,
`FUN_14099xxxx` store API (**READ 50** — T49-1; far callers `0x140c7xxxx/0x140c8xxxx`), `FUN_140d1xxxx` sound,
render tier, `0x140f49xxx`/`0x140f1exxx`, `0x140d2xxxx`/`0x140d5xxxx` (44), `0x140a6xxxx` (44/45),
`0x140912xxx–0x140916xxx`/`0x14091axxx` (47), **`0x140d23cc0–0x140d2716a` (52)**. (b) XOR-8 keys are per-record salts. (c) `0x142f0…`–`0x142f2b…` thunks absent. (d) Corpus gaps: pass 30: 12 × >1 KiB; 34: 4/11,844 B; 35: 6/18,531 B; 36: 2/6,068 B;
37–39: 0; 40: 1/1,033 B (T40-6); 41: 0; 42: 1/8,015 B (T42-1, `--offcuts` pending);
43: 1/1,601 B (T43-1); 44: 0 (98.1 % span); 45: 0/1 giant-window (97.6 %); 46: 1/1,527 B
(T46-1) + 1 giant+offcut (96.5 %); 47: 1 hole / 1,080 B (T47-1) + 3 giants;
48: 1 hole / 1,052 B + 1 giant (T48-1; 98.5 % span); **49: 0 holes (89.7 % span;
93 `size=` gaps = window midsections)**; **50: 1 hole / 1,757 B (T50-1) + 3
window-giant midsections (89.6 % span)**; **51: 0 holes / 0 offcuts (79.7 % span;
all 8 >1-KiB gaps are window midsections)**; **52: 0 holes / 0 offcuts (85.9 % span;
all 7 >1-KiB gaps are window midsections, 2 of them offcut calls of the same giant)**; **53: 0 holes / 0 offcuts
(78.4 % span; all 4 >1-KiB gaps are window midsections, 1 offcut mention)**.
(e) Window chunks per ledgers 39/47/49/53/57/61/65/68: pass-37/38 window-cache
set, pass-41 `FUN_14080c740` set, pass-42 name-window family, 45 vote twins,
46 friends-screen set, 47 `FUN_1409006d0`/`FUN_14091c3e0`, 48 `FUN_140945f40`
(50.4-K real)/`FUN_14092c130`/`FUN_140949e00`, 49 `FUN_1409527a0` (51.1-K real)/
`FUN_14096cb30`/`FUN_14096e240`, 50 `FUN_14099c9f0`+`14099d190`+`14099d330`
(one cascade)/`FUN_14098a0d0`/`FUN_1409a9e30`/`FUN_140997970`, 51 `FUN_1409bb350`/
`1409ce9f0`/`1409d0cd0`/`1409cc100` (shared fabrication zone)/`FUN_1409ac830`+
`1409b1470`+`1409b1950` (ctor half = `FUN_1409c8040`), **52 `FUN_1409d5ab0`/
`1409d5ae0`/`1409d56f0` (real host `0x140d23cc0-0x140d2716a`)/`FUN_1409da570`/
`1409df470`/`1409e3490`/`1409e3d50`/`1409e6c60`/`1409e7580` + the twin pair
`FUN_1409f4b10`/`1409f4b30` (0.9967, ledger 68), **53 `FUN_1409f6250`/`1409f7df0`/
`1409fb6f0`/`1409faeb0`/`140a05be0`/`140a06fb0`/`140a06fe0`/`140a0ae10`/`140a0da80`
(8 halt windows, all in chunks 0484/0486/0490–0494; 0488+0489 are clean)**.

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
| Entity/VFX/widgets + replay (33–34) | record 0x18a0 B; VFX `FUN_140681360`; JSON→widget `FUN_141940ef0`; demo magic `0x7495174655b5d763`; Markdown escaper; hash-grow ×211 | `0x140687fe0` |
| Party/store + telemetry/voice (35–36) | member rows; ruleset ids; `__PlaceOrderWithVirtualCurrency`; hosts us/eu/kr; FNV change-hash; perf-counter schema; SAPI; screenshots | `0x1406c7b50` |
| Map/live-ops/UI + party client (37–39) | 12-state load machine; Mongo feed queries; window-cache giants; spring `FUN_140784fd0`; session 0x14f8 B; spawn solver `FUN_1407a8a70`; slot engine `FUN_1407c9480` | `0x1407691f0` |
| **Event post (40)** | `func_0x000140c28eb0(_DAT_143b7f410)` or group svc `(svc+0x3c3b9d672a4416a4)^0xf9798462dc0addd7` → `(**vt+0x18)(svc,id)`, ids 0x22–0x54; the app-service event bus | `0x1407d06a0` |
| **Retire idiom + widget factory + entity root (41)** | `0x20000`-flag guard + `(**vt+0x158)/200/0x160` + `FUN_1421522e0/14214eb70/14214d400` + `+0x914` sentinel; create-stub pair + XOR-8 name page + `FUN_141c4b050(&desc,&name,0x14,size,0,id)`; entity root `(x+0x1e2421a4798a328>>0x22|x*0x40000000)^0xe1379e3cb308170d → >>0x2b|<<0x15` | `0x1407fd0a0` |
| **Name-window triple-mix + player-list lock (42)** | `((x^0xeb)+0x2d1d7705)>>0xb|x*0x200000 ^ [0x143b79598+0xb5] ^ 0x998fae39` → `>>0x15|x<<0xb +0xd2e288fb ^ DAT_143847f0a` + `0x4d79452d486f9431` root; `DAT_143b945b0` 0x400-spinlock + disable flag over the three global arrays `PTR_DAT_14385f3b0/3f480/3f4f0` | `0x14082f100` |
| **List API `0x1421exxx` (42→49)** | the **UI row model** (~60 members, ledger 58): `40c0/3c20/3330/3420` child-list get, `5100` begin, `52c0` node-at, `3de0…3920` getters, `41d0…4170` setters, `52a0/5370/5310` list ops, `51d0…5230` row ctors, `4140` type test, `4af0` node-by-type; fields `0x3ff3/0x6003` child lists, `0x229a` value GUID, `0x2d95` row key; `FUN_1421e5100` ×536 record 45 → ×279 pass 46 → ×316 pass 47 → ×315 pass 48 → **×72 pass 49 (displaced from #1 by `FUN_141bb8d40` ×134 — engine/protocol tier, not row-model code)** | `0x1408493b0` |
| **JSON DOM + writers (43)** | node ctors/readers fully mapped consumer-side: `FUN_141940c00/ea0/e00` + `141940ef0` property set + `141941360/141941440` array + `14193e0d0/93e940/93ef80/93f510/93f560/93e5c0` readers + `FUN_140693130/1406935f0/1406934c0` writers + `func_0x00014213ee60` compact writer (0x14213f7df siblings) + posters `FUN_140840db0/140840e90` + pools `DAT_144137230/250` | `0x14084f530` |
| **UI screen tier (43–48)** | ctor = base + vtable + `0xa88000000000xxx` guid; node mint `__RegisterWaitForSingleObject(list,type,0)`/`FUN_140726800`; widget chain `FUN_1422544f0`→`1421f1780/1610`→`142255180/330`→`1421ee370/7d0`→`FUN_14224eec0/14224f390`; **reconcile template** = child-list match by node type + row key (`0x41cb` int or string `0x621f`), stale retire `FUN_1405651e0`; sorts + locale pair + introsort ×2 (46); hash-set `(x*0x40000+~x)*0x15*0x41` (46); scoreboard `0x9b<field>` ids, map GUID `|0x2e…`/`|0xb3…`/`|0x1f6…`/pack form (47), handle `(h&~0x3f)` decode; LRU group cache, 5-state async loader, slot registry `DAT_1441b8130`; **(47) settings def belt (resolver ×58, typed setters `0x203/0x201/0x8a8/0x204`, fields `0x6896/0x6161/0x4de8/0x540a`); party dispatcher `FUN_14091a4c0` (steamid arm); widget-interest registrar `FUN_14213f870`; four per-row RB-trees; **(48) carousel roll `(idx+first)%count` `FUN_140941d80`; roster shuffle via TLS RNG `FUN_140939030`; 6-name lobby set `PTR_s_Overview_143050fd0`; settings enum decode belt `0x18/0x66/0x98/0xe5/0xf9/0x9a/0x1df/0x134/0x228` over `0xc8800000000 0xxx`; store-gate `0x1439aeff0`-chain `+0xb2485ad1cf871d2c` ×3 gates** | `0x140849a10` |
| **Settings backend / JS bridge (49)** | video settings four-generation state `FUN_140958580` + enum belt (0x191/0x1b9/0x1f0/0x1f2/0x22b) + apply/read masters `FUN_14095bd80/14095cee0`; **web view**: 16-method JS registry (plaintext names) + FNV-1a 64 dispatch `FUN_140969640` + modal router `FUN_140968b80` + hash-D method store `FUN_142693a50`; **camera**: entity chain `(DAT_14384879b^x)+0xb3a098e02bc0db2a^0x2bb16a93aa826dcc→(>>0x11|<<0x2f)+0x6494b1884caf70ee^*(_DAT_143b79598+0x97)`, cvar chain `…^DAT_1438489d0)+0xf841a90ed52dbd7d`, XOR-float table `0x143a1a9f0–0x143a1aa3c`, 8-thread pool `FUN_14096e240`; VO filter `FUN_140971780` + hash-C line table `FUN_140973b40` + fifth-family audio table `FUN_140971460`; streaming canary/chunk engine `FUN_14097a660/97ab40/97b830`; store-gate chain now **six gates** (`0x1439aef08/28/50/88`, `0x1439aeff0`, `0x1439af028`) | `0x14094f840` |
| **Store/loadout tier (50)** | DOM resolver template `(DOM+8 → vt+0x20)(app,event,&out)` + typed `FUN_14193f510/ef80/e5c0/e940/e8e0` + pool disposal 5/0xb→`DAT_144137230`, 0xc/0xd→`250`; **`StoreSystem_C`** states `+0x98 {0,0xd,9}` / `+0x108 {0,4}` via `vt+8(state,"Name")`, product resolve `FUN_1407caee0(store,id)` behind `func_0x000142d3afd0()`, clock `FUN_1409957f0` (seconds, deadlines ×1000), hash-D bundle tables +0x488/0x490, purchase post `0xe0871b`; **loadout engine**: `DAT_143b8d290` svc + `DAT_143872788` .rdata template, 0x158 view / 0x118 weapon rows / 0x78 inventory / 0xb0 request rows, 16-subtype async family over 3 queue slots, request counter `_DAT_143ba4480`, highlight format magic `0x56c6870` ('hlp' read) with branch `func_0x000141c6b880()` / build `_DAT_144159380` / account gates + seeded hash `FUN_1409a29e0(DAT_143059ad8)`, rate limiter hash-set `(x*0x40000+~x)*0x15*0x41`; second XOR-float table `_DAT_143a1aa10-aa3c`; render svc `func_0x000140c857c0` (+0x3748 name map, +0x3948 flag) | `0x14097f810` |
| **Widget tier + gate-service map (51)** | widget observers: base `FUN_14214b540/14214b670/14216fbd0` + factory `FUN_141baff30(size,0)` + dtors `FUN_14214b800/14214ba10/142150aa0`; DOM accessors `FUN_1409caba0/cacc0/cadb0` + **value classes `DAT_143df6510` float / `143df6670` vec2 / `143df67d0` vec4 / `143df6d50` string / `143df6eb0` u64**; screen-stack push/pop (+0x300/318 lists, `+0x914` retire, `+0x1b4` flags); **gate svc `(_DAT_1439aef88/aeff0/af010/af028 + 0xb2485ad1cf871d2c ^ 0x89d3e0b8c0994abf) + 0x820b88e340ab6eb0`**: name/card +0x478/0x480/0x488/0x490/0x498/0x4a0, camera +0x320/0x328 + config `FUN_142034400/142034110/142033840/142035ce0`, debug draw +0x730/0x760, registry `FUN_1421e0ce0/1421e16d0` + `func_0x0001421e2b40` (8 role slots, ids `0xe07f6f/70`/`0xe0b947/48`/`0xe0bc6d–70` `|0xb3…`; names `0xd8…43f8/4ba7c/4bc88`) | `0x1409ab8e0` |
| **Widget class library + playback (53)** | ctor = `p[1]=&DAT_14306…` offset table + base vtable chain + `PTR_FUN_143048228` MI no-op; 44 classes, `0x80000004`/`0x80000032`/`0x800000c8` dynamic-array tags; draw trampoline = `vt+0x1c0` visible → `vt+0x160` ctx → slot `+0x28/30/40/48/50/78/80`; property kinds `0/4/5/6/8/9/10/0xb/0xc/0xd` with pools `DAT_144137230/250`; node-kind `10` = float via `vt+0xf0`; playback cmd `{+0x18 tick,+0x20 u16,+0x30 op,+0x34 u16}` (1 seek / 2 duration / 3 window); marker slot 0x500 B | `0x1409fc290` |

## Open threads (cheapest next query each; check/update every pass)

2/5. **Entity transport framing + command ids** — base `0x48/0x53/0x7c/0x7d/0xa5/0xb2/0x3a`; grown 32–43 (audio 0x8d, ability 0x6b/0x655/0xf5/0x580/0x1e; queue 0x631b/0x6334, hero 0x664e/0x66b7/0x6521, claim 0x12e58–0x13223). `FUN_141c295b0`/`FUN_141c58170`/`FUN_142d2cf30` bodies unread (~chunk `15xx`).
11–19. Channel-list renderer unfound; hotfix dump `_DAT_1439d98c0`; **gaps** —
T42-1 8,015 B, T43-1 1,601 B, T47-1 1,080 B open; event-name table `0x143851c90`
still encoded; pass-32–34 machinery bodies; handle-table writers; 'Unknown' belt `0x14385d1a0`–`ddf0`.
21–25. Store endpoint labels (`0x1438595b0–0x1438597c8`); `FUN_140d1xxxx` sound (`crossref.py 140d1bcc0`);
audio-channel ids; `0x8784b4333a5802xx` masked chain; component-message ids (`0xd8…`/`0x5800…`/`0xde…`).
26–40. Widget names / UI-cache tables / render tier bodies (lifecycle closed 40); material family
(`crossref.py 142cb4c20`); `FUN_140c6xxxx` input; `FUN_1409bxxxx` appliers; `0x142f2df90` fn-ptr table /
`FUN_1407b0e90` stat fold / **toast table `0x143059b80` = the notification string table `FUN_1409a4fc0`
reads (50)** / far-window `0x14213f7df`/`0x142045667`/`0x141c4b29c`.
41–55. T40/T41 — serializer (`crossref.py 1407f2a00`) + twin (`142388ab0`);
time/random `FUN_141d11f60/141c4efa0`; observer blocks `0x143b90c30–ea8`; c740
window boundary; `FUN_142044820` banks; factory update bodies.
56–69. T42-x/T43 — 8,015-B hole; list-API defs `0x1421e0000+`; name-window boundary;
map/mode enum table (`142d37920`); player-array writers; `0x141bba761` region;
T43-1 hole (`--offcuts` when neighbours gain mentions); T43-4 fn-ptrs;
T43-5 regex side; T43-6 locale; T43-7 sentinel 0x13e.
71–84. T44-3…8 / T45-1…6 — ability-config (`140d56bf0`); hero-info state
(`140a63a00`); `0xca…` RTTI (`142d402d0`); `FUN_142d26xxx/142d29xxx` writers;
hashes `142697480`/`142159220`; vote twin slots (`1408cb4e0`); `0x7f2` enum
writers; `_DAT_143b975a0` singleton; award-pool siblings (`142149490`);
`0x129b0`/`+0x251` flush; `0x18317a531d116c` bucket table.
85–91. T46-x minus T46-2 — the `0x1408e0be0→0x1408e1260` hole (1,527 B); fifth
hash family builder (`1408f4fb0`); `DAT_1441b8130` slot registry (consumer seen 50); 13-entry hero
table (`14304c240`); `vt+0x238` tags; `FUN_1408f6d50` 5-state machine.
92–103. T47-x/T48-x — the `0x1409054a0→0x1409058e0` hole (1,080 B, ledger 63); `FUN_1409006d0`
window boundary; endorsement cascade join (`140917b70`); steamid service def (`1422ec0e0`); the
`0x1409487d0→0x140949130` hole (1,052 B) + settings-master giant (T48-1); enum-ladder member
tables (`crossref.py 141b328f0`); store-gate defining region (store side read 50); 6-name row
set's other names; `FUN_140941bf0` callers.
**T53-x (pass 53).** T53-1 `0x140a1b770` real trig helper with **no decompiled entry** (2 callers, 0 defs; between `0x140a14a60` and 0497) — `gap_report.py 495 498`; T53-2 widget→renderer slot names (`crossref.py 14214f540`); T53-3 0x500-B marker slot + `+0x4b0..+0x4f8` bundle (`crossref.py 140a02b10`); T53-4 the 5 RTTI tags’ names (`crossref.py 141d01100`); T53-5 `0x1426c…` CRT math band named (sincos/atan2/asin/acos/security-cookie) — stop chasing; T53-6 `0x140a0c724` offcut (`crossref.py 140a0c724`); T53-7 `0x140d9430c` far reach = fabrication (only real namer `FUN_140d93cf0`, chunk 0725); T53-8 `FUN_140a030c0` child-draw consumer.
110–13x. T50-x/T51-x/T52-x — T50-1 hole `0x14098e520→0x14098ec80`; render-math `0x142069a20-
0x142069bc4` + 0x1420d0xxx (`crossref.py 1420d0e80`); render-svc region `0x140c7xxxx/0x140c8xxxx`
(T50-3); CDN host `func_0x000141bbbd70`; T51-2 aim curve `FUN_140818370`; T51-3 voice monitors
`0x143ba7af8–cc8`; T51-4 role names (`0xd8…43f8/4ba7c/4bc88`); T51-5 3-char tags ('Sen'); T51-6
grid consumers (`crossref.py 1409b3780`). **T52-1** caller `FUN_140623900` reads the camera object
(`^0xad14668946be46d9`, `+…54a/…5ca/…552`) into `FUN_1409d5ae0`, then stores `entity+0x4e4`;
**T52-2** `FUN_14214ea90` vs `14214eb00` (the twins' only real difference); **T52-3** timeline API
`FUN_140dafd90`/`dbcba0`/`dbcaa0`/`dbcb00`; **T52-4** `FUN_140f76f10`/`FUN_140f74450` (manifest
schema); **T52-5** share-code layouts 0x30/0x50/0x58 + key schedule `FUN_1409e9300`; **T52-6** the
`0x140a0xxxx` / `0x140d23cc0-0x140d2716a` real host bands (not in corpus); **T52-8** the 0x1548-B
slot array (`svc+0x140+i*0x1548`). Carried: T49-2/3/5, T48-4/5, T47-x, T46-x, T45-1, T43-7,
T42-1, T43-1, T51-2…6. **Closed in 51: T50-4**; **closed in 52: T51-1 + the far-window watch
items** `0x141c4b29c`/`0x1421ad73b`/`0x140a46a19` (fabrication, ledger 66).

CLOSED (machine): fd9670 recount; provenance; `0x1411b8070`; thread 43; T20; JSON writer/parser/CSV;
XOR-8 salt keys; presence events; closed ledgers in the archive. Closings by pass: 36→T35-1/3;
37→T36-3; 38→T37-4; 39→T38-1; 40→render lifecycle; 41→T23 audio; 42→T9 flags + voice client;
43→T42-2 + row model + page table; 44→T43-3/8 + zero-gap; 45→T44-5; 46→T44-6; 47→T44-1 + def belts;
48→T47-6 + party-row belt; 49→none; 50→T49-1 + T49-4; 51→T50-4 + far-window items; **52→T51-1 +
share-code/manifest error model**; **53→T52-3 (timeline API) + T52-6 (the 0x140a0 band is real code)**.

## Next pass

Resume range: **`NEXT.txt`** — written by `pass_next.py` from `state.json` + `--max`;
regenerate after every `--update`, never hand-edit. Pass 53 ends at `FUN_140a0da80` (a
236-K window); stratum `0x14054fea0` OPEN and the widget-library tier continues; next
per `NEXT.txt` = chunks `0495`–`0508`, `.text` `0x140a0e700`–`0x140a34200` (14 chunks,
1,425,167 B). Watch for: (a) **T53-1** `0x140a1b770` — a real trig helper with no
decompiled entry, inside this range; (b) the `0x140a1xxxx` host bodies the pass-53 giants
stamp into (`func_0x000140a1d220`, `140a1e*`, `0x140a25*`, `0x140a2802e`) — real or
fabricated, decide per entry; (c) `FUN_140a195e0`/`140a19430` (called from pass 53) and
`FUN_140a10160`/`140a110a0`/`140a11760` (already visible in chunk 0495); (d) **T52-1**
`entity+0x4e4`, and the `0x140d…` bodies the timeline API needs. Do not re-run a counted
range through `--update` (ledger 5); never treat `0x826e…`/`0xca334801`/`0x4343ffa4`-family
or offcut-call addresses as data (ledger 20); ledgers 24/31/39/43/44/47/49/53/57/58/60/61/
62/63/66/67/68/69 for gaps, windows, twins, hash families and fabrication; `size=` is not
coverage (ledger 30) — **paste the measure block (ledger 56)**; check zone counts sum to `files=`.
