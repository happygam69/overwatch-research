# CODE_MAP — cumulative map of the systematic `.text` read

**Read in full before every pass; update after every pass. Hard budget: ≤300 lines.** Per-pass
narrative lives ONLY in `ranges/`; cumulative numbers come from `state.json` (via
`scripts/pass_measure.py`) — never hand-add. Long-form archive: `CODE_MAP_ARCHIVE.md`.

## Files

| file | role |
|---|---|
| `chunks/chunk_NNNN.txt` | corpus, address order; unreachable-block warnings stripped 2026-11-21 (per-chunk counts in `index.json`, pre-strip `index.pre_strip.json`) |
| `index.json` / `state.json` | per-chunk bytes / first / last (coverage truth) / machine ledger: next_chunk, per-pass entries, cumulative totals, all registration hashes, all 326 `{id,hash}` rows with match flags |
| `scripts/pass_next.py` / `NEXT.txt` | resume range (chunk range, `.text` range, commands) from `state.json.next_chunk` + the `--max` cap; `NEXT.txt` is its generated output — read it, never hand-edit |
| `scripts/pass_measure.py` / `ranges/*.md` | canonical per-pass measurement (block quoted verbatim in records or `--json` digest cited; `max refs:` = automatic crossref of the range max; `largest (text)` vs `sum_size (binary)` — text exceeds binary on stripped window bodies) / per-pass records — the evidence base |
| `scripts/gap_report.py` | per-range gap classes (`giant`/`offcut`/`hole`; `--offcuts` = corpus sweep) + `window reach:` far-window watch list (ledger 53) |
| `rdata_names.tsv` / `scripts/rdata_names.py` | plaintext `.rdata` strings (16,832 rows) / regenerator; query via `strlookup.py --pool rdata_names.tsv` |

## Coverage

Corpus: 2,228 chunks, 119,757 functions, 42,864,695 B `.text`. Passes 1–22 archived in
`CODE_MAP_ARCHIVE.md`; `state.json` is the truth for cumulative numbers; pending range is `NEXT.txt`.

| pass | chunks | `.text` range | functions | record |
|---|---|---|---|---|
| 23–33 | `0193`–`0306` | `0x1404192e0`–`0x14069b460` | 5,537 | `ranges/` rows 23–33 (archived detail) |
| 34–35 | `0307`–`0323` | `0x14069bb80`–`0x140738b30` | 733 | `ranges/0x14069bb80-…`/`0x1406c7b50-…` |
| 36 (13-chunk) | `0324`–`0336` | `0x140738d00`–`0x140760880` | 247 | `ranges/0x140738d00-0x140760880.md` |
| 37 (12-chunk) | `0337`–`0348` | `0x140760c30`–`0x140784fd0` | 308 | `ranges/0x140760c30-0x140784fd0.md` |
| 38 (11-chunk) | `0349`–`0359` | `0x140785e30`–`0x1407a2800` | 238 | `ranges/0x140785e30-0x1407a2800.md` |
| **total** | **359, contiguous** | `0x140001000`–`0x1407a2800` | **20,923** | machine-verified (`state.json`) |

Machine-verified (`state.json` after pass 38): files 20,923 (17.47 %), Σ `size=` 5,729,023
(13.37 %); classes reg 7,956 / wrapper 1,954 / builder 1,717 / sorted 280 / atexit 261 /
record 326 / other **8,429**; 7,956 distinct ciphertext registrations + 4 plaintext rows
(one hash ×2 — Corrections 16); `d4f30` 1,188 / `d4f70` 1,350 / `d4fb0` 4,492 / `c2d70`
4,212 / `c2d50` 326 / `c7880` 261 / `atexit` 315; records 326. Passes 27–38 = consumer
only, zero registration (twelve consecutive).

## Corrections ledger (machine-derived; supersedes prose in older records)
5. **`--update` is forward-only; `--init` wipes the pass list.** `--update` over a counted range double-counts and rewinds `next_chunk`; repair is `--init` (why `state.json`'s pass list covers only 16–37 while totals cover 1–37).
7. **`pass_measure.py` prints no `ciphertext band:` line** — its `CTXT` regex needs `DAT_1438` + 6 hex digits; the band is now `0x1439a…`–`0x143b…`. Ciphertext extremes in records are read from the text, both addresses cited.
8. **`pass_measure.py` `zones:` filter** prints only class `reg`/`record` runs with `cnt>=3`; 1–2-function builder/wrapper runs are absent from the skeleton (they exist in the text).
13. **Allocator symbol ≠ allocator.** Per-TU one-arg symbols (`141367110`, `1412b5440`, `1418e82e0`, `1413676c0`, `141901b40/170/180`, `140f7b550`, `140f7ade0`, `14190df80`, `14191bd90`, `1419254a0`, `14192a730`; older `140f80f80`, `14114d8a0`) — key on the shape. The **container allocator** is `func_0x141c23490(&PTR_PTR_143a01d18,size[,align])` + free `func_0x140578190`, 500+ sites.
15. **Minimum registered size is 3, not 8** (`FUN_1404aad50`, size 3, align 1); span 3–0x3bc0.
20. **Decompiler fabrications:** `0x826eb8xx`, `0xca334801`, `0x38046856305b946b`, `0x0a13cb7c…`, `0x09e1c148…`, and `func_0x000102d05da9`/`func_0x00010161e575` are not code or data — they appear only after bad-instruction truncation. Never add them to a band table.
22. **Jump-table warnings** at `0x140556eb3`/`FUN_14057ad20/57b2c0/57e220` are 2-entry vtables; both arms known. **23. `files=` counts functions, not chunks.**
24. **The corpus itself is missing functions.** Pass 29's range has 113 address gaps totalling **81,067 B (~7.7 %)** with no decompiled body (largest `0x14059a007→0x14059c350`, 9,033 B). Record gaps, never assume padding.
26. **`canary x69` (pass 29) is not a builder canary** (cookies + hotfix literal; class of 21). **27. `0x14384b7b0–b7bc` are plaintext floats** on an XOR-8 page — pages are not homogeneous.
30. **`sum_size` is not coverage** — `size=` collapses at `halt_baddata`/overlap truncation; always quote the address range and count gaps from headers. **31. Alignment vs missing code** — pass 30's 486 gaps: 332 × ≤16 B (alignment), 142 × 17 B–1 KiB (under-reported `size=`), 12 × >1 KiB = 48,640 B un-decompiled.
32. **Two more hash families.** D: `(k0+k1)`/`(k0+2*k1)`, each `(x>>0x21^x)*-0xae502812aa7333 *-0x3b314601e57a13ad`, summed, `&(cap-1)`, `-1` sentinel (`0x1405d15c0`); E: descending-ordered bucket chains (`0x1405d8710`); D reappears in the store tier (`FUN_14072adf0`, pass 35). **33. Match-queue error enum 0–12** = `UserRequest, QueuePopped, QueueNotReserved, InvalidRulesetGUID, ServerError, ServerDraining, ReadyCheckTimeout, PartyNotFound, PartyAlreadyExistsInDifferentQueue, PartyFailedToJoinMatch, RulesetGUIDNotEnabled, CrossPlayChanged, MatchInputPoolChanged`, else `Invalid` (`FUN_1405ddb40`).
34. **Event names are not a plain `.rdata` table.** `rdata_names.tsv` (16,832 rows; `strlookup.py --pool`) names telemetry/protocol fields, but the pass-32 "event-name table" `0x143851c90` is in **`.data`**, pointer-shaped/encoded, not inline names (`.data` event strings `PlatformEvent`/`event-store` are decoded in `strpool.tsv`).
36. **Masked chains coexist**: component decode `0x4d79452d…` (heaviest); per-session type table (`(x+0x3fa981c8e7192fa6) ror31 ^ 0x8784b4333a580288 → ror23 + 0x37a9e6a2eedd5214 + type*8`); per-frame handle table (`(p^0x73cc01350b9bc072)+0x704e4dbd364c5bd3 >> 0x26 | 0x4000000`); store row-decode `0xba397115a070ffa9`+`0x4094aaa9c7911a89`; service root `0x622b95327b2e6d1e ^ 0xd6c0ac78d0e44481`; **pass 37 adds** the `0x309bbf8525c62fd2` slot chain, the `0x60e93ab59bc621f8` self-key chain, the `0x4c1c315c09b449e` key seed, the `(x+0xb441a9797379a3c4)^0x4d06fcd25c0c008e` slot-row chain, the `0x2d1d7705`-family return-address hash and the object-key scrambler `FUN_14077fef0` (`0xa6c156b0120b4011` chain).
39. **The pass-33 entity update is ONE cascade seen through overlapping decompilation windows** — `FUN_140678850`/`140689930`/`14068ae00` share stamps and calls; pass 33's 18 >1 KiB gaps (53,215 B) are these spans. **41. Per-frame handle-table rows are 16 B `{u32 handle, u32 pad, u64 entity_ptr}`** (`FUN_14067d8b0`/`140691400`); count/rows at `+0x18317a531d116c14/c0c`.
43. **Gap totals were hand-computed as distances, not gaps.** `gap_report.py <first> <last>` measures `next_entry − (addr + size)` and classes every >1 KiB gap (giant tail / offcut body / hole). Re-run it for any range before quoting gap numbers; a referenced entry inside a neighbour's declared `size=` is not a gap and stays invisible to it.
44. **Pass 34 has 4 real holes (11,844 B)** — first since ledger 24: `0x1406a2aa0→0x1406a3ca0` (4,467 B), `0x1406ac0e0→0x1406ad5e0` (4,342 B), `0x1406bb060→0x1406bbe20` (1,924 B), `0x1406c5b10→0x1406c5fd0` (1,111 B), all inside obfuscated replay-capture functions; plus 4 offcut bodies. Corpus sweep (`--offcuts`): 6 offcut / 2 hole.
45. **`FUN_1406232f0` is the replay/demo frame reader too** (0x20-B variant `FUN_1406b1270`): the replay file format IS the entity bitstream; frame apply re-checks the pass-28 anti-tamper constants. **46. `FUN_1406b7500` ×211** is the canonical open-chaining table grow (16-B rows `{u32 next, u64 key, u64 val}`) + twin `FUN_140727340`.
47. **`FUN_1406b3220` (41,249-B text) is not a corpus maximum** — one region seen through overlapping windows (as are the `FUN_1406c2cf0`-family chat cascade and `FUN_1407174e0`). **48. Corpus maxima were range maxima.** `--maxscan` ranks the real top: `FUN_142b567b0` **571,552 B** (unread chunk `2056`) > `FUN_1423add80` 414,426 > `FUN_142b4e520` 398,819 > `FUN_140a17da0` 345,153; `state.json.max_text` holds the maximum; the `max refs:` line crossrefs the range max automatically, so a NEW max is a claim until no second entry names it (47).
49. **Pass 35's 223,308-B `FUN_1407174e0` is one decompilation window over the whole store tier** — its stamps reach `0x140737d24`, past 30 later entries (class of 39/47); it is the range max (39.1 % of corpus max), NOT a corpus-max candidate. `sum_size` 23.3 % of the span is the ledger-30 effect at its most extreme: the two 111–161-KB "offcut" gaps are `FUN_1406d3ff0`/`1406efb90`'s real bodies. Corpus sweep keeps **6 holes / 18,531 B** (`0x1406ccb30`, `0x1406d2e50`, `0x1406cf520`, `0x14071af50`, `0x140728290`, `0x1406ce1a0` spans), all inside obfuscated bodies. **50. A second JSON parser exists** — the store tier parses HTTP responses with a rapidjson-style reader (`FUN_140612090` + DOM verify `FUN_1422ee440`); its verbatim error strings (codes 1–0x11) sit in `FUN_140734260` (+ pass-37 second site `FUN_140778120`); distinct from the pass-32 text engine — do not merge the two constructs. **51. Thread 18's `FUN_14099xxxx` family is the store's platform/purchase API** (confirmed pass 35): `FUN_140992cf0/993c80/9957f0/9964f0/996720/9937a0` are called from `StoreSystem_C`; bodies still unread.
52. **Resume range and measurement provenance are generated.** `pass_next.py` writes the resume block to `NEXT.txt` (from `state.json.next_chunk` + `--max`), and `pass_measure.py --json` prints the range facts plus a 16-hex `digest` (state-derived `corpus_max` excluded) a record can cite instead of pasting the block; the block's `max refs:` line auto-crossrefs the range max. First use closes thread 20: `FUN_1407174e0` is defined once (chunk `0316`) and no other function names it.
53. **"Window chunks" — `size=` can be ~50× smaller than the chunk text.** Pass 36 has six entries like `FUN_14074d1e0` (size=3,144 vs 139,652-B chunk text), `FUN_140749e20` (1,076 vs 89,260), `FUN_14075c310` (76 vs 82,176), `FUN_14075a8a0` (231 vs 119,897), `FUN_14075d060` (294 vs 74,582), `FUN_14075fe40` (31 vs 7,617) — one decompilation window spanning many real functions (ledger-39 class made extreme; pass 37 has fifteen more, record §headline). The named small entries around them are the real bodies; treat any chunk with `chunk_bytes / size= > 20` as a window chunk. **Far reaches.** Those windows also stamp far outside the range (`FUN_14074b240` → `0x1421e243d` +27.9 MB; pass 37: `FUN_14077fd10`/`FUN_1407803f0` → `0x141c4b29c`, `FUN_140765e50` → `0x140785b27`) — pointers into unread regions, never this range's coverage. `gap_report.py` prints the top three as its `window reach:` line, so the watch list is generated, not hand-collected.
54. **The UI-window cache is machine-visible.** Five pass-37 giants (`FUN_14077d100/d230`, `FUN_140782390/2d70`, `FUN_140784720`) share an identical `0x2d1d7705`-family return-address hash + binary search against `_DAT_143b795a0/a8/b0` — a return-address → UI-window cache; treat any body naming `_DAT_143b795a0` as a window-cache giant (ledger-53 class; would have predicted 4/6 of pass 37's giant gaps). `0x4343ffa4`-family branches there are decompiler fabrications (ledger-20 class).
**Closed/superseded (moved to archive 2026-11-21, pass 35):** items 1–4, 6, 9–12, 14, 17–19, 21, 25, 28, 29, 35, 37, 38, 40, 42 — record-hash match rule (1, 9, 11), sorted/atexit counts (2, 3), provenance (4), no shutdown table (6), roots regime (12), sorted-insert middle call (14), RTTI band (17), XOR pad table (18), name-page layout (19), non-builder canaries (21, 25, 26), plaintext floats (27), MSVC concurrency (28), strpool naming (29, supersedes 19), event-bus registrar (35), range maxima 100,672/101,443 B (37, 38, superseded by 48), thread-6 closure (40), per-frame rows (41→kept), match-queue enum (33 kept). Full text in `CODE_MAP_ARCHIVE.md` §Corrections archive.

## What the code is — cumulative synthesis (37 passes; evidence unless marked [inference])

`.text` is catalogued in entry-address order. After 348 chunks the cursor is at `0x140784fd0`
(17.28 % of functions, 13.17 % of `.text`). Names printed `func_0x…` have **no decompiled body
in this dump** — registrar, decryptors `d4f30`/`d4f70`, writer `c2d50`, helpers `c2d70`/`c7880`,
the `0x140543xx0`/`0x1405674xx` decoder family, settings accessors, component getters, the hotfix
HTTP client, the CSV parse iterator and the pass-32 cipher family `FUN_142454xxx` — as does
`tls_callback_0` (generic list insert/update). **Six layers, in address order:**

1. **Library preamble** `0x140001000`–`0x140039fc0`: ISA-L/igzip DEFLATE inflate (12 fns),
   `nvapi_QueryInterface` bootstrap, 53 NVAPI entry wrappers, `Initialize`/`Unload`.
2. **NVIDIA driver-loading shim** `0x14003a230`–`0x14003d330`: replacement `LoadLibrary` for
   `nv*.dll` (D3DKMT, SetupAPI, service paths, Khronos keys).
3. **CRT/C++ static-init sea** `0x14003ffe0`–`0x1400fa760`: five generator templates — 181-B
   magic-static descriptor (×2,451), 209-B locale/facet statics (×354), 58-B event thunks
   (×284), 134-B XOR-40 + cipher registrations (×61), 37-B `_onexit` stubs.
4. **Typed registry machine** `0x1400fbcb0`–`0x14054ea50` (CLOSED): nine constructs;
   families CompilerIDFilter, physics/serialization schemas (`dm*`/`bc*`), telemetry
   (`circuitbreaker.*`, `gameruleset.gameoptions.*`), catch descriptors, component
   id→handler registry, dispatch rows, plaintext struct schemas.
5. **Runtime bootstrap + obfuscated dispatchers** `0x14053f6b0`–`0x14058200x`: PE `entry`
   trampoline, signature scanner `FUN_140541200` (patch record `0x143b79640`), anti-tamper
   (CPUID FPU gate, `"0x811C9DC5"`), masked-pointer layer with 16–47 KB obfuscated bodies.
6. **Engine runtime** `0x14054fea0`→ (passes 28–38, **OPEN**). The game client's own
   runtime — cumulative halves, newest first; per-pass detail in `ranges/`:
   (38) **UI-window engine room** — the window-cache giant family doubles to ~24
   prologue-bearing bodies (11 full giants incl. range max `FUN_140786360`); three
   `0xd8…`-descriptor apply twins (~80 ids total); the 3-phase spring init/eval +
   per-entity 0x650-B / camera 0x600-B trail rows with the ring reader; the
   quaternion→basis and camera yaw/pitch math; the 0x22d0-B per-window manager,
   0x1928-B sub-objects, 0x368-B 9-ring + 0x268-B widget-manager objects; the
   u32 + 0x20-B-row introsorts; the 24-field descriptor unpack (3 qwords → row);
   the state-gated viewport getter tier + shutdown gate; the 109-caller
   per-frame handle lease;
   (37) **map/scene lifecycle + live-ops feed + UI-window tier** — 12-state map-load
   machine ('SHUTDOWN'…'WORLD_RUNNING') with hotfix stall/mismatch telemetry;
   patch-note/news/esports/web-event web-feed client (Mongo `{"$and":[platform,
   country]}` filters, URL-encoded JSON type filters, the full patch-note schema:
   generic/hero/map-comparison sections with abilities, images, allowed-URL regex);
   capability manager (0x75/0xc5/0x77 trio, six states); 0x18a0-B hero/entity record;
   masked UI-window manager (return-address window cache, widget clone-classes,
   6-op modifier applier, 3-phase spring interpolator);
   (36) store purchase/VC completion, client telemetry + platform diagnostics
   (Battle.net hosts, purchase-status enum, perf-counter schema, SAPI voice,
   Steam screenshots/overlay/controller + 16-device hot-plug), and the
   `0x622b95327b2e6d1e`-rooted effect/impulse engine (parallel jobs, quaternion
   emitters, row pools, session close with the `"hotfix"` report);
   (35) social + monetization (party/social client, player-stat layer with weighted
   scoreboard + sabotage detection, sound/visibility weights, `StoreSystem_C` with
   OAuth/Steam mtx/catalog/VC and the rapidjson HTTP parser);
   (34) replay/highlight/cinematic (progression + CSV, demo/replay over the pass-31
   bitstream, sequence recorder, spectator, chat/Markdown, presence);
   (33) presentation (visual actors, VFX keyframe engine `FUN_140681360`,
   animation rings, widget binding, party-lobby UI);
   (32) live gameplay loop (event bus, entity replay/interpolation,
   NetworkEventSystem_C, match flow, master tick/visibility/world-to-screen, JSON
   text engine); (31) match-lifecycle receive side;
   (28–30) infra: ~150-subsystem app composition/teardown, container/hash library,
   cvars, chat/voice (Vivox), hotfix downloader, worker pool, HUD/markers, event
   bridge, spatial/entity runtime, bitstream reader, CSV, Steam/XInput.
   [inference: `0x14054fea0` marks the end of data registration and the start of
   behaviour.]

**Layer 6 constructs (passes 28–37; per-pass detail + addresses in the records):**
*infra* (28–30): handle table ×494; hash A/B/C + allocator; vector library ×983; per-site
logger; named-service registry; hotfix verifier/HTTP; worker pool ×20; component access;
spatial raycast/LOS; frame loop; event bridge; bitstream reader; debug-UI table API; CSV
iterator; HUD quad; tracked-entity; spawn queue; presence; Steam stats; XInput; JSON tags.
*match receive side* (31): bitstream codec reader ×341 / writer ×248 + entity
header/field/baseline/component-apply + 67-KB dispatcher; introsort; saved-match tables;
JSON serializer; JamMessage dispatch; event-bus subscribe; telemetry HTTP #2.
*live gameplay loop* (32): event-bus + mass wiring `FUN_14064d2a0`;
`ClientLobbyMessageSystem_C`; connection state machine + toast router; entity runtime
(component decoders, 0x468-B state copy, frame replay, interpolation); scoreboard +
end-of-round report; NetworkEventSystem_C; match-flow handlers `0x4f4c–0x4f6a`; kill
feed; time sync; master tick + watchdog; ability bitsets + hero HUD; world-to-screen;
FNV-1a; JSON text engine + `"--name {json}"` pipeline. *presentation + social* (33):
visual actors; VFX keyframe engine `FUN_140681360`; 0x18a0-B entity record + 0x470-B
animation rings; entity state machine; JSON→widget binding; party/lobby debug screens.
*replay/cinematic/chat* (34): progression reports (loot-box sim + CSV, leaderboards,
skill-rating, XP); social-actor manager; async file-I/O (5 drainers); demo/replay
system (fragment pump, header, CLI keys, magic `0x7495174655b5d763`); sequence
cinematic machine; spectator view; hash-table grow ×211; chat/Markdown UI; presence
pump. *party + stats + store* (35): party/social client (0x1d8-B member rows,
Steam-group sync); player-stat layer (ruleset enum, weighted scoreboard,
sabotage detector); sound-importance cvars; spatial visibility weights; 64-slot
registry service; **StoreSystem_C** (catalog cache, request queue, OAuth, Steam mtx,
product sets, bundle price, `__GetProducts`, personalized shop, VC grants, URL picker,
watchdog, "Content-Encoding"); hash C/D maps; wait-handle registry ×78.
(37) **map lifecycle + live-ops + UI windows (37)**: 12-state map/scene load machine
   (`FUN_1407691f0`/`FUN_14076d0a0`, name table `FUN_14076a210`, hotfix stall watcher
   `FUN_14076a6b0`); 0x18a0-B hero/entity record (`FUN_140782e30`: 3×0x90 anim tables,
   masked key `+0x286`); patch-note schema (`FUN_140773900`: generic/hero/map-comparison
   sections); feed query builders ×4 (news/esports/game-update/web-event, Mongo
   `{"$and":…}` + URL-encoded JSON filters); capability manager (`0x75/0xc5/0x77` trio,
   six-state table); rapidjson error formatter `FUN_140778120` (ledger 50 second site);
   UI-window cache giants ×5 (ledger 54); widget clone-classes ×7; sorted mod rows (key
   float,u32,u64); 6-op modifier applier `FUN_140784310`; 3-phase spring `FUN_140784fd0`
   (pass-37 range max). *UI-window engine room (38)*: window-cache giants `FUN_140786360`
   (range max, ~50 `0xd8…` applies) + `FUN_140786760` (transform interpolator) /
   `FUN_140786b60` (trail-ring reader, ring `+0x1440` 0x10-stride) / `FUN_1407880b0`
   (0x18-stride input-state apply) / `FUN_140789970`/`FUN_1407911d0` (apply twins 2–3,
   +`0xde…2370/2371/2372`); spring init `FUN_140788f90` + random pop `FUN_14078a100`;
   trail appenders `FUN_14078ba00` (0x600-B camera) / `FUN_14078bbe0` (0x650-B entity);
   quat→basis `FUN_1407884b0` + camera pack `FUN_140789720` + yaw/pitch/dist
   `FUN_14078c220`; anim-value getter `FUN_14078b230` (17 ids); 0x22d0-B manager
   `FUN_140795a40` + 0x1928-B sub-object `FUN_140796390` + 0x368-B 9-ring
   `FUN_14078dd50` + 0x268-B `FUN_14078a160`; introsorts `FUN_140790c00` (u32) /
   `FUN_1407951c0` (0x20-B rows); descriptor unpack `FUN_140798f80` (3 qwords → 24
   fields, `0x14385bfa0` 0x13-entry table); shutdown gate `FUN_14079ecf0` + viewport
   getters `FUN_1407999c0`-family; material walker `FUN_140792560`; widget tree
   `FUN_14079ff00` (27,978-B clean body); event send `FUN_1407a2340`
   (`FUN_140623720` + 5/0xb vs 0xc/0xd tags); handle lease `FUN_1407a2610` (109
   callers).

**The registry machine — nine constructs/variants (layer 4, closed):** name buffers (XOR-8,
24-bit len); **registration** `func_0x1421cd360(…,18 args)` — 7,956 ciphertext + 4 plaintext
rows, `base = out − 0xa0`; identity mapped for 44,360 name pages in `../../poolmap.tsv`;
**builder** (allocator → XOR-8 → `d4f30/d4f70` → `d4fb0` → row `{+0x20 root, +0x28 inst,
+0x30 0, +0x98 1, +0x9c 0}`); **copy wrapper** (`c2d70`+`d4fb0`); **sorted-insert** (2×56-B
keyed at +8); **`{id,hash,alias}`** (326 rows); **nested-atexit** (261); **settings/variable
registrar** (`FUN_141c58170` + `_onexit`); + 15 CompilerIDFilter shells. Builders/sorted/
atexit carry stack cookies; registrations, wrappers and settings functions do not.

**Where the data lives** (shutdown slots moved to Corrections archive item 6):

| band | content |
|---|---|
| `0x143848d40`–`0x14384ad54`, `0x143864e80`–`0x143864ed8` | XOR-8 name/payload ciphertext: runtime bootstrap, settings, logger, hotfix/log format strings, ~50 console-var names (3 copies), UI/event strings (key@+0, len@+8, latch-0x48). `0x14384b7b0–b7bc` on the same page are **plaintext** floats (Corrections 27). Pass 33 adds UI/dialogue pages `0x143853c10`–`0x143855944` + fn-ptr tables `0x143854720`/`0x143856720`; pass 34 extends to `0x143857d44` (replay/sequence/chat strings); **pass 35 extends to `0x143859f58`** (party/member status, ruleset enum, stat/sabotage, store/OAuth/grant pages) + new store fn-ptr tables (`PTR_FUN_142f8a3c0…4f0`, `142f8a728/7a0`, `142f8ac68…d58`, `142f8b108/b148/b250`, `PTR_FUN_1438493b0`, `PTR_FUN_143859178`); **pass 36 extends to `0x14385a6a4`** (Battle.net API/OAuth host tables + HTTP header pairs `0x143859328`–`0x143859560`, purchase-status enum `0x143859a18`–`b90`, the performance-counter schema `0x14385a058`–`0x14385a338`, match/tournament debug formats `0x14385a3a8`–`478`, session-summary tags to `0x14385a6a4`) + fn-ptr tables `PTR_FUN_142f8bc18/c50/c30`, `PTR_LAB_142f8bc88`, `PTR_FUN_142f8c7f0`, `PTR_LAB_142f8c508`, `PTR_FUN_142f8cbb8` (0x3f0-B channel), `PTR_LAB_142f8c950`, `PTR_FUN_142f8cc10`, `PTR_FUN_14385a580` (screenshot sink), `PTR_FUN_14384d9a0`; **pass 37 extends to `0x14385bb4c`** (map/scene state table `0x14385a9f0`–`0x14385ab64`; hotfix formats `0x14385acd8`–`0x14385af30`; deserializer errors `0x14385af88`–`0x14385b2d0` + `0x14385b478`–`0x14385b8bc`; query keys `0x14385af3c`–`0x14385b428`; capability states `0x14385b930`–`0x14385b9b4`) + widget vtables `PTR_FUN_142f8d4a0/d4b8/d4b0/d4c0/d4c8/d4a8/d970/88d10`, `PTR_FUN_142f93d48/93ce8/93d18/91c58/8fac8/8da18/8d9e8/88c90/88cd0/88cf0/88d00`, `PTR_DAT_142f8d850`, `PTR_FUN_142f8fa88/8fa50/91b38/93ca0/8a180/88b20/869e8`;  **pass 38 extends to `0x14385beb0`** (widget-clone ctor name pages `0x14385bb48`–`0x14385beb0`, 24 pages, decode inline in each ctor; the 0x13×0x10-B select table `0x14385bfa0`; the `0x142fac3f0` (10) / `0x142fac440` (6) qword tables + `0x142fac4ac..504` float scales; `0x14385c0d0` sub-object name page; `0x14385be14` 2-float format; `DAT_142f8902c` `0xde…` string-set default) + new vtables `PTR_FUN_142f95e58/e20/df0/eb0/ee0/9f90` (0x268-B), `PTR_FUN_142f97f58/142f9c040/142f9c080/142f9e0b0/142fa00e0/142fa0120/142fa2150/142fa41d8/142fa4208/142fa62a8/142fa6278`, `PTR_FUN_142f95df0`, `PTR_FUN_142f9bfd0` (0x368-B), `PTR_FUN_142f7d730/740/720` (0x1928-B), `PTR_FUN_142fac490/470/480/510/540/550` (0x22d0-B/0x48-B), `PTR_FUN_142f81740`, `PTR_FUN_142fa2190`; new globals `DAT_143b8ecd0/143b8ecd8` (0xbd input rows), `_DAT_143b8eb24`, `_DAT_1441880e8`, `_DAT_14418a278..298`, `_DAT_142fa6270/276`, `_DAT_143b796a8`, `DAT_1441b8130` |
| `0x1438b8e50`–`0x1439a9b2c`, `0x143a16e38–2e7b` | registry name/payload ciphertext; `PTR_s_CompilerIDFilter_*`; triplet-stub object page `0x1439b0000`–`0x1439fa330` |
| `0x143a155xx`–`0x143aa36xx`, `0x143b0c…`–`0x143b77…` | XOR-40 key tables, settings names, locale/ciphertext, catch keys, `0x143a19b50–0x143a19b88` (camera/volume float block), `0x143a19938–44` (render defaults) |
| `0x143b7a428`–`0x143b7af00`, `0x143b7f410`, `0x143b808xx–0x143b81a0x` | passes 28–29 runtime block: logger objects, worker-pool state, object-id counter `0x143b91f50`, ~250 feature flags `0x143b945b8–0x143b9c5c0`; the app object; per-HUD-object flags |
| `0x143cf0000`–`0x143d05000`, `0x143f8…`–`0x143f94…`, `0x143e99d90`–`0x14413b7a0` | RTTI type_info (17); registration outputs / instance slots; settings descriptors; config globals |
| `0x1441e18f0`–`0x1441e67c8`, `0x1442a1920`–`0x1442a1bd8` | plaintext reg outputs + registry-list head; struct-schema rows (`dmWorld`, `bcMtx44`, …); record pools `0x1442e37xx–0x1442f14d2` |
| `0x144226c70/80`, `0x1441d05xx`, `0x144180ed0`/`f20`, `0x1441b3bb8`, `0x1441880e8`, `0x1441b8170–8198` | named-service registry; voice levels/mic; settings-slot objects; id-intern table |

**What it is for.** Layers 1–2 are a vendored NVIDIA/igzip preamble; layer 3 is compiled-in C++
static init; layer 4 registers ~8 k encrypted type names with sizes/alignment/category and builds
instances, tables and id rows from them; layers 5–6 are the client that consumes that data —
settings, telemetry, schemas, chat/voice, hotfix patching, HUD markers, the spatial/entity
runtime, and then, pass by pass, its halves: match-lifecycle receive (31), live gameplay loop
(32), presentation (33), replay/cinematic (34), social + monetization (35), client diagnostics +
audio effects (36), and map lifecycle + live-ops feed + UI windows (37: the 12-state map-load
machine, the patch-note/news/esports/web-event client, the capability manager, the 0x18a0-B
hero/entity record, the UI-window manager).
No plaintext game
protocol (entity traffic is the `FUN_1406232f0`/`FUN_1406264c0` bitstream over an unframed
transport — and the replay files reuse the same reader), the render device is one opaque
`FUN_141ff40f0` call (2 sightings), and no gameplay *rules* are
in the read range — but the HUD, scoreboard, kill feed, match-state builders, the
social/party UI, the replay/highlight/cinematic pipeline, the store/monetization and
player-stat-integrity layers, the named telemetry/audio subsystems, and the map-load
state machine + live-ops feed/patch-note client are.
Confidence: counts/shapes/bands measured; construct labels are shape-based inference;
obfuscated bodies read structurally only.

**Known limits.** (a) `func_0x…` bodies absent (registrar, decryptors, `0x140543xx0`
family, settings accessors, component getters, HTTP client, CSV iterator, event-bus ctors
`FUN_142e0xxxx`, cipher `FUN_142454xxx`; offcut families: `0x14068xxxx` helpers (33),
`FUN_141da/141db` emitters (33), `FUN_14099xxxx` store API (35), `FUN_140d1xxxx` sound
assets (36), render-object tier `FUN_141ff40f0/141ffed40/142042cc0/142043170` + query
helpers `FUN_142d37xxx/142d38040` (37)). (b) XOR-8 keys are
per-record salts; only pool text exists (ledger 29). (c) `0x142f0…`–`0x142f2b…` labelled
thunks absent. (d) Corpus gaps: pass 30's 12 × >1 KiB (ledger 31); passes 31–33 offcut/
under-reporting spans (ledger 39); pass 35's 24 × >1 KiB = 327,786 B (ledger 49: 6 corpus
holes / 18,531 B, the rest `FUN_1407174e0` window + offcut bodies); pass 36's 11 × >1 KiB =
22,122 B (2 holes / 6,068 B inside the obfuscated telemetry/sound bodies, 8 giant tails +
1 offcut); **pass 37's 6 × >1 KiB = 9,871 B with 0 holes** (5 giant tails + 1 offcut —
first zero-hole pass since ledger 24). (e) Obfuscated bodies
resist decompilation: pass 32's giants (`FUN_140669ee0` 100,672-B text …) carry offcut stamps
to `0x1406a1703`; pass 33's `FUN_140681360` (101,443); pass 35's `FUN_1407174e0` (223,308,
range max, one window — ledger 49); pass 36's window chunks per **ledger 53**
(`FUN_14074d1e0` 139,652, `FUN_1407528b0` 136,865, `FUN_14075a8a0` 119,897, …);
pass 37's per ledger 53/54 (nineteen window chunks, topped by `FUN_140784fd0` 75,833,
`FUN_140765e50` 73,532, `FUN_140784b50` 68,881 — full list in the record).
## Cross-cutting conventions (one line each; per-pass deltas in the records)

| convention | rule | first seen |
|---|---|---|
| TLS guard + 181-B descriptor | `*(TLS+0x50) < epoch` → `FUN_1426c3bcc(&epoch)` → `_Init_thread_footer`; descriptor `{+0x20=1\|2, +0x40=ctor, +0x48=vtable/FUN, +0x50=third, +0x58=payload, +0x60=shared}` ×2,451 | `0x140001000` |
| **Registry primitives** | XOR-40/XOR-8 decryptors 8-byte key 24-bit len (`d4f30/d4f70(&out,&buf,hash,0)`); `{id,hash,alias}` 326 rows (two TLS guards + `c2d50`); builder row `{+0x20 root, +0x28 ptr, +0x30 0, +0x98 1, +0x9c 0}`; stack canary `_DAT_143ac5f40 ^ stack` → `FUN_1426c3d40` (builders/sorted/atexit only); nested-atexit 261 | `0x1400fbf70` |
| Registration + sorted + settings | registration 18 args, zero hash reuse, `arg18 = out − 0xa0`; no-output form 242–257-B (arg17 = arg18 = 0); sorted registry: min-to-slot-0 pre-swap + insertion sort of 2×56-B records keyed `+8` (280); settings registrar 209–399-B: 1–3 XOR-8 → `FUN_141c58170(&desc,0,&config,&name,&default)` → `_onexit` | `0x1400fbcb0` |
| Layer-4 row shapes | catch descriptor 181-B (×272); triplet stub 66-B; "Unknown" error row ×87; component registry `{u16 id,handler,u64}` ids 1–0x19; dispatch-slot row (8 fn-ptrs + bit flip); registry list push (LIFO `_DAT_1441e1c70`); struct schema `{&name,off,size}` `0x1442a1920+`; metric `func_0x000141d23660(&DAT,type,"name","tag,k=v;…")` | `0x1404f8720` |
| **Masked ptr + obfuscation + sig scan** | masked pointer `local = 0x<const>; func_0x140543xx0(&local)`, result `^ *(u64*)(_DAT_143b79598+n)`, fail gate `0x4c208ebc71408a54`; dispatcher: overlapping instructions, `halt_baddata`, `rdtsc`, POPCOUNT parity, nibble tables `0x142f7aa08/aa18/d158`; sig scan `FUN_140541200` (VirtualProtect + memcmp, `0x90`/`0xcc`) → patch record 0x58 B at `0x143b79640` | `0x14053f9a0` |
| **App object + settings accessor** | app `_DAT_143b7f410`, vtable `PTR_LAB_14328c990`, ≥0x420 B, ~150 children (attach `FUN_141c52d10`/`1405721d0`/`140572140`/`140bc7590`); settings: XOR-8 name → `FUN_141c295b0(int)`/`280b0`/`2bfd0`/`29b00`/`28b30`/`29060(min,max)`/`2ca50`, numeric `FUN_142d2cf30` | `0x140554220` |
| **Logger + handle table + hash maps** | per-site logger: TLS-guarded 0x28-B static via `func_0x141c48370`, `FUN_141c48450` gate → `FUN_141c48330`; handle table 0xfff buckets `{u32 handle,u64 value}`, lease `FUN_140567590`; hash A int64 `(~k+k*0x40000)>>31^…`, B u32 `k*0x1001+0x7ed55d16…`, tombstone `-1` | `0x1405601c0` |
| **Container allocator / worker pool** | alloc `func_0x141c23490(&PTR_PTR_143a01d18,size[,align])` / free `func_0x140578190` (capacity word `sign|count`); pool `FUN_141bb7520(0x20000,FUN_140573d40,ctx,name,0x14)`, enqueue `FUN_140573f10`, stop `FUN_140573fc0` | `0x140558120` |
| **Hotfix + component + spatial + events** | hotfix 0x30-B record `{hash,idx,verified,handle,ts}` → SHA-256 memcmp, tags `"hotfix"`/`"canary"`; component access `func_0x140c503d0/140c506f0(entity,id[,default])`; spatial ray `FUN_14206b500/14206a660` + rsqrtss/Newton; event payload `FUN_140583fb0` 0x18-B `{ptr,ptr,u32,2}` filled by `FUN_141940x0/141941x0`, send `FUN_1405ae0e0` or app vt `+0x140/+0x150`; 0x19c message `FUN_141c23430(buf,0x19c)` + `FUN_14200dee0` | `0x14056cd40` |
| **Cvar + HUD + tracked entity + debug UI** | cvar registrar XOR-8 name pair → `FUN_141c29b00`/`141c2a030`(float)/`141c2bfd0`/`141c285e0`, 3 copies under latch `DAT_143b80a9c`; HUD marker 0x90-B quad (verts `+0x540..0x578`, occlusion `FUN_142032690`); tracked-entity rows 0x58/0x60/0x68-B (key `+0`, prio `+0x38`, flags `+0x50`); table API `FUN_141c64c10` begin → cells → `…651a0` end | `0x140596b00` |
| **Hash C + command dispatcher** | hash C `h=(k*0x200000+~k); (h>>0x18^h)*0x109; (h>>0xe^h)*0x15; (h>>0x1c^h)*-0x7fffffff & (cap-1)` (chained or range; byte-keyed registries `FUN_140621990/aa0`); dispatcher `(**(code**)(*disp+0x10))(disp,fn,id,0)` (+`0x30`), ~50 dispatchers, default `FUN_140548d00` ×97 | `0x140599970` |
| **CSV / presence / JSON value** | CSV iterator `func_0x1423887b0`-family (0x20-B rows); presence `{bnet_dbid,title_id,group,field,unique_id}` via `FUN_141c63bc0`; JSON value 0x10-B `{data, u16 tag @ +0xe}` (3 obj, 4 arr, 9/0xa bool, `0x?96/0x?d6` ints, `0xc05` heap / `0x1c05` inline string, `len = 0xd - low byte`); writer `FUN_1406331b0` | `0x1405afc60` |
| **Bitstream codec + event bus + session tables** | reader `FUN_1406232f0` / writer `FUN_1406264c0`; entity header `FUN_140622f00` (0xc-bit flags → 6 widths); field/baseline/component-apply `FUN_140623120/1406251a0/140625950`; dispatcher `FUN_140623900`; event-bus map `FUN_14064cdd0(bus+0x48,id)` → 0xb0 descriptor, dispatch `FUN_14064d0d0/140`, registrar 3-variant, ids hash-obfuscated (`FUN_14053bd90`); session masked table `(row+0x160+0x3fa981c8e7192fa6) ror31 ^ 0x8784b4333a580288 → ror23 + 0x37a9e6a2eedd5214 + type*8` | `0x1406232f0` |
| **Net frame + cipher + JSON text + command string (32)** | incoming 0x22-bit header, ping ring 128; outgoing `FUN_140654c50` 16-bit time + 8-bit seq, `FUN_140657580` presence-bit + 32-bit length, cipher `FUN_142454xxx`; JSON parser `FUN_140673120` (number `FUN_140672500`, string `FUN_140672c80` SIMD, writer `FUN_14066b5d0`); `"--%s %s"`+`{json}` builder `FUN_140673be0/140675580` → executor `FUN_140676370` (7-field lookup → hero-GUID check) | `0x140654c50` |
| **Entity record + VFX + widget binding (33)** | entity record 0x18a0 B (move `FUN_140687fe0`, transforms ×8 `+0x1300-139c`, bone rows 0x1c `+0xe50`, sub-records 0x470, anim snapshot rings); VFX keyframe engine `FUN_140681360` (rows 0x650 B, ~21 tracks, binsearch+lerp); JSON→widget binding `FUN_141940ef0` (value ctors `FUN_141940x0/141941x0`, widget ids `0xd8000000000…`) | `0x140687fe0` |
| **File I/O + replay/cinematic (34)** | 5 drainers (flag `+0x128`, refcount `+0x129`); demo record 0x1d0 B (`FUN_1406a99c0`, state `+0xf8` 0–3), fragment pump `FUN_1406b06e0`, frame apply = `FUN_1406232f0(state,0x20)`, magic `0x7495174655b5d763`, CLI keys; sequence machine `FUN_1406b81d0` (state 0–10, capture `FUN_14206b2d0/afb0/b480/b460`) | `0x1406a7b40` |
| **Chat + social actors (34)** | Markdown pipeline (escaper `FUN_1406c24f0` → sort/merge/redact); submit `FUN_1406c36c0` (channels 0–6); id tables `DAT_142f89a30/142f89e70`; social-actor record 0x240 B `FUN_1406a4e90` + 0x220-B mirror `FUN_1406a6060`; recent-players top-5 (`FUN_1406a7910`, 1-day gate) | `0x1406a4e90` |
| **Hash-table grow (34)** | `FUN_1406b7500` ×211: power-of-2 buckets, 16-B rows `{u32 next, u64 key, u64 val}`, fill −1, re-chain `(cap−1)&hash`; probe `FUN_1406b5a30` | `0x1406b7500` |
| **Party/social + stats (35)** | member rows 0x1d8 B; Steam-group sync `FUN_1406caa00`; SeasonLobbyState dumps; ruleset enum 16 names; weighted-stat scoreboard `FUN_14071dce0`; sabotage detector `FUN_14071d290`; GUID→name `FUN_14071ea70` | `0x1406c7b50` |
| **StoreSystem_C (35)** | object 0x390 B (ctor `FUN_14072c560`); product rows 0x1b8 B; catalog cache `FUN_14072e230`; pending-request queue 0x110-B, states 0/4/5/9/0xc/0xd; OAuth `FUN_140734af0/260`; Steam mtx; URL picker `FUN_140738790`; auth-error gate `{0x191,0,0x1ad,5xx}`; "Content-Encoding" `FUN_140738b30`; grant pipeline `_tier_`/"BattlePass: … - Tier …" | `0x14072c560` |
| **Store completion + hosts (36)** | async sinks `FUN_140738d00/8e60`; header builders `FUN_140738f80` (json)/`FUN_1407398c0` (form); region→host `FUN_1407393a0` (us/eu/kr.api.blizzard.com) + OAuth `FUN_140739a90`; `__PlaceOrderWithVirtualCurrency` (`FUN_14073a190`→`14073a600`, retry ×7); `__ProductsComplete` `FUN_14073ad30`; VC balance `FUN_14073e850`; purchase-status enum 16 values `FUN_14073bc80`; event pump `FUN_14073c6c0`; submit funnel `FUN_14073ba80` | `0x140738d00` |
| **Telemetry report (36)** | change hash FNV-1a `FUN_140741960/140742ef0` vs latch `_DAT_143b8bb68`; report builder `FUN_140743c50` (+ send twin `FUN_140745880`): 0x58 root / 0x68 system / 0xd8 + 0x60 / 0x48 local-player sections, `|1|2|4…` presence flags; **named perf-counter schema** ('System.PeakWorkingSet'…'SingleFrame', 0x40-entry counter walk) `0x14385a058`–`0x14385a338` | `0x140743c50` |
| **SAPI voice + Steam overlay/input (36)** | SAPI enum `FUN_14073fe50` (HKLM `SOFTWARE\Microsoft\Speech\Voices`), speak `FUN_140740370`, pump `FUN_140740930`; screenshots `STEAMSCREENSHOTS_INTERFACE_VERSION003` (`FUN_14074b210`, RGBA→RGB `FUN_14074a990`); overlay frame `FUN_14074b240` (10 hotkey rows); input gate `FUN_14074ba20` (ids 0x113–0x138); hot-plug tail `0x1421e1e4c` (4-state, `_DAT_143aa88c8[0x40]`) | `0x14073fe50` |
| **Sound-effect service (36)** | masked root `0x622b95327b2e6d1e^0xd6c0ac78d0e44481`; effect rows 0x100 B + 0x80/0x58/0x28 pools; importer `FUN_140752d10`; dispatcher `FUN_14074d1e0` (parallel split `FUN_14075ce50`); emitter math `FUN_1407517a0`/`FUN_14075f180` (quaternion basis, Newton rsqrt); channel records 0x3f0 B (`FUN_14075b430`); audio flags `FUN_142044960(0x100/0x585/0x7b7/0x172/0x171)`; session close `FUN_14075d060` (900-ms stall, `"hotfix"` path); assets `FUN_140d1xxxx` (offcut) | `0x14074dbd0` |
| **JSON parser #2 (35)** | rapidjson-style reader `FUN_140612090` + DOM verify `FUN_1422ee440`; verbatim error table 1–0x11 ("The document is empty."…"Unknown error.") in `FUN_140734260`; **second site `FUN_140778120`** (pass 37, "JSON parse error: %s (%u)"); distinct from pass-32 engine | `0x140734260` |
| **Map/scene load machine (37)** | state byte `+0x28` 2→…→0xb (forward `FUN_1407691f0`/`FUN_14076d410`, reverse `FUN_14076d0a0`, poll `FUN_140769950`); 12-name table `FUN_14076a210`; app shutdown machine `FUN_14076d6f0`; record 0x138 B + compare `FUN_1407650b0` | `0x1407691f0` |
| **Live-ops feed (37)** | Mongo queries `FUN_142d38040/142d37f70` (`{"$and":[%s,%s]}`, URL-encoded `{"type":"%s",…}`); types news_item/game_update/esports_event/web_event; patch-note schema `FUN_140773900` (sections generic_update/hero_update/map_comparison; members title/description/dev_comment/metadata.asset_guid/icon_guid); HTTP poll `FUN_140774b40` + funnel `FUN_1407792d0`; news cache invalidate on 12 feature flags (`FUN_140771e70`) | `0x1407702b0` |
| **Capability manager (37)** | trio `0x75/0xc5/0x77` at `+0x88/+0x90/+0x98`, gate `FUN_14077b480`, hash-C id maps (`FUN_14077c4f0`), six-state table `FUN_14077b210`, device probes `FUN_14077b5e0` (`0x6e…065/f8/118/f9/fa/fb/fc/17`) | `0x14077b210` |
| **UI-window tier (37)** | object-key scrambler `FUN_14077fef0`; window-cache giants (ledger 54); widget clone-classes ×7 (slot ids 0x2a–0x42); sorted mod rows 0x30 B key (float,u32,u64) `FUN_1407837a0`; 6-op modifier enum `FUN_140784310` (add/set/mul/min/max/clamp); 3-phase spring `FUN_140784fd0`; 0x18a0-B record `FUN_140782e30` (`0x60e93ab59bc621f8` key chain) | `0x14077fef0` |
| **UI-window engine room (38)** | window-cache prologue `0x2d1d7705` → `_DAT_143b795a0` search + `_DAT_143b795a8` write `[(n&0xfff)+1]` (×~24 bodies); `0xd8…`-descriptor apply `func_0x140d32840(ctx,0xd8000000000XXXX)` cascades (~80 ids; `0xce13/ce14` 3-state; `0xcde0–cde5` mirrors); spring init `FUN_140788f90` + eval `FUN_140786b60` (trail ring `+0x1440`, 0x10-stride, head `+0x1650`); trail rows 0x600-B (camera) / 0x650-B (entity) via `FUN_1405a8410`, key `+0x8`/id `+0x630`; descriptor unpack `FUN_140798f80` (bools + `0x142fac3f0`/`0x142fac440`/`0x14385bfa0` selects + `0x142fac4ac..504` scales); shutdown gate `FUN_14079ecf0` (`vt+0x270`); state-gated getters `(*masked_svc+0x160/0x168/0x1f8/0x328)` selectors 2/3/5/6; u32/0x20-B introsorts (`0x1e` cutoff, explicit stack); handle lease `FUN_1407a2610` (`(n&0xfffff000)+0x1000+tls_id`, backoff ≤16); event send `FUN_1407a2340` → `FUN_140623720`, JSON-text ids `0xe0ec9c/9d/9e/a9/aa` + `0x100e01d56/57`; widget clone-ctor family (~12, slot ids 0x46–0x95, XOR-8 name pages `0x14385bb48`–`0x14385beb0`) | `0x140785e30` |

## Open threads (cheapest next query each; check/update every pass)

2. **0x19c-B / entity-state transport framing** — client framing found pass 32 (`FUN_140654c50`/`FUN_140657580`); remaining: the socket/UDP layer carrying the finalized buffer — grep forward for `FUN_142454xxx` cipher outputs. Pass 35 added the store's HTTP transport; entity transport still ahead.
5. **Command ids** — base set `0x48/0x53/0x7c/0x7d/0xa5/0xb2/0x3a`; grep later chunks for `+0x10))(…,0x`/`+0x30))(…,0x`. Grown since: gated blocks `0x4f4c–0x4f6a`, `0x64c8–0x64d4`, `0x6b6c/d`, `0xa794–0xa79a` (32); plain ids 0x33/0x3a/0x37/0x72 (33), 0x24/0x2d/0x2e/0x38/0x39/0x41/0x51 + `0xde…` toasts (34), `0x47` + `0x58661fbe` family (35); pass 37 adds JamMessage posts `0x56/0x57/0x59/0x5f/0x6e`.
6. CLOSED (pass 33, ledger 40) — `FUN_141c2a030` negative min found.
7. **`FUN_141c295b0`/`FUN_141c58170`/`FUN_142d2cf30` bodies** — `FUN_`-named, unread corpus (~chunk `15xx`). **8. `func_0x140543xx0` family** — absent; test the masked-pointer chain against a known `.data` address.
9. **`0x143b945b8`–`0x143b9c5c0` (~250 flags)** — grep forward for `143b94`/`143b95`/`143b9c` readers; pass 37 names 12 concrete members in `FUN_140771e70` (thread 30). **10. `_DAT_143b7f410` field map** — merge `FUN_140554220/5559c0/585220` for ~150 offsets.
11. **Channel list `_DAT_143c00680`** — writer found (pass 32: `FUN_140663de0`); the renderer that walks it is still unfound. **12. Hotfix file identity** — dump one 0x30-B record (`_DAT_1439d98c0`); backoff table `_DAT_1439d9890`.
13. **Gaps** — pass 38: 8 × >1 KiB = 14,438 B, **0 holes** (second consecutive; 6 giant tails + 2 offcuts); pass 37: 6 × >1 KiB = 9,871 B, **0 holes** (first since ledger 24); pass 35: 6 holes / 18,531 B (ledger 49); pass 34: 4 holes / 11,844 B (ledger 44); pass 30: 12 × >1 KiB (ledger 31); `0x14059a007–0x14059c350` (9,033 B) and `0x1401a4e02–0x1401abad0` (27,854 B) still open. **14. CompilerIDFilter** — unchanged (pass 21); payloads are regs.
15. **Event-bus / gameplay names — table still open.** the 68-entry `.data` table `0x143851c90` remains encoded (ledger 34); chat id tables `DAT_142f89a30[id]`/`DAT_142f89e70[id]` and arg-spec table `0x143857998` still need raw dumps. Next: decode `0x143851c90`.
16. **Pass-32/33/34 machinery bodies** — cipher `FUN_142454xxx`; event-hash resolver `FUN_14053bd90`; offcut `0x14068xxxx` helpers; emitters `FUN_141da/141db`; anim samplers; camera-capture `FUN_14206b2d0/afb0/b480/b460`. **17. Handle-table writers** — row shape known; writer unfound — grep forward for `0x18317a531d116c`.
18. **Party/lobby `FUN_14099xxxx` family** — pass 35 confirms it is the **store/platform purchase API** (`FUN_140992cf0` request post, `FUN_140993c80` scope/region, `FUN_1409957f0` time source, `FUN_1409964f0` per-row test, `FUN_140996720` license check, `FUN_1409937a0` region/enum, `FUN_140993710/140997520` product lookups) — called constantly by `StoreSystem_C`; **bodies at `0x14099xxxx` remain unread**; grep forward when the read reaches them.
19. **Widget/party enum pages** — XOR-8 names `0x143854b30–0x143854cb0`, party-screen columns `0x1438556b0–0x143855790`; band now extends to `0x143859f58` (pass 35), `0x14385bb4c` (pass 37) and `0x14385beb0` (pass 38, all 'Unknown' — thread 31).
20. **`FUN_1407174e0` window split (T35-1)** — CLOSED: `crossref.py` = defined once (chunk `0316`), no other namer; its 223,308-B text is a single window over bodies Ghidra never filed as entries (ledger 52).
21. **Store endpoint labels (T35-2)** — decode XOR-8 pages `0x1438595b0–0x1438597c8` to name the six 2,495-B response-handler twins ('StorefrontService/v1/GetCurrentPages' + '/ProductCatalogService/v1/GetProductsByStoreId' already visible); request side decoded pass 36, response twins unnamed.
22. **Sound-effect asset family `FUN_140d1xxxx` (T36-2)** — 16+ functions called throughout the `0x622b95327b2e6d1e` effect service; bodies offcut, unread. Query: `python scripts/crossref.py 140d1bcc0`.
23. **Audio-channel id semantics (T36-4)** — `FUN_142044960(chan,0x100/0x585/0x7b7/0x172/0x171,…)`. Query: `python scripts/crossref.py 142044960`.
24. **`0x8784b4333a5802xx` masked string chain (T36-3)** — `FUN_14075fe40`/`FUN_140771f60` copy `_DAT_1439dc5c8/5f8/628`; decode the band or extend the ledger-36 chain. Query: `python scripts/strlookup.py --pool rdata_names.tsv --band 0x1439dc5c0 0x1439dc630`.
25. **Component-message id enums (T36-5)** — grow the pass-32 tables: `0x5800000000000dc/41b/3bd8` poster family, `0xd80000000000…` query family (`734`,`4aa`,`18cb`,`20a7`,`1c8d/4d2/8e3/522/a0d/1df3`), toast `0xde000000001b12b`. Query: grep forward for `0x580000000000` / `0xd80000000000`. **Pass 37 adds** `0x5800000000000dc` reprise + `0xd8000000001022f/1dee/1e36/1e38`, `0x6e…` ids `0x65/f7/f8/f9/fa/fb/fc/101/118/029/0ca/12a/0da/0e6/079`, `0x46…` id `0x46000000000011b`, `0xa6` family, and JamMessage posts `0x56/0x57/0x59/0x5f/0x6e` (feed/status). **Pass 38 adds ~30 `0xd8…` ids** (full list in the record; incl. `0xcde0–0xcde5` mirrors, `0xce13/ce14` 3-state, `01dec/020df/02901/01ded/0e0eb/041c1/01ec2/01f6f/021f0/02e64/0b364/11c9a/1236e`), `0xde0000000002370/2371/2372`, `0x460000000000068` (entity list), and JSON-text event ids `0xe0ec9c/0xe0ec9d/0xe0ec9e/0xe0eca9/0xe0ecaa` + `0x100e01d56/0x100e01d57`.
26. **Widget clone-class names (T37-1, widened pass 38 → thread 31)** — the pass-37 seven ctors (slot ids 0x2a–0x42) plus ~12 pass-38 ctors (`FUN_14078ac30/14078cd80/14078d870/14078fbe0/1407907c0/140790a80/140790f00/140791fc0/1407923b0/140793c60/1407945f0/140794b90`, slot ids 0x46–0x95) decode name pages from the `0x14385b9f0`–`0x14385beb0` band; all 'Unknown' in the pool — needs a pool-side decode (thread 31).
27. **UI-window cache tables (T37-2)** — `_DAT_143b795a0/a8/b0` + the `0x2d1d7705`-family return-address hash, binary-searched by five giants (ledger 54). Query: grep chunks for `143b795a0` to size the cache.
28. **Render-object tier (T37-3)** — `FUN_141ff40f0` (2 sightings), `FUN_141ffed40`, `FUN_142042cc0`, `FUN_142043170` called from the 0x18a0-B object but not defined in range. Query: `python scripts/crossref.py 141ff40f0`.
29. **0x650-B trail rows (T37-4)** — CLOSED (pass 38): `FUN_14078bbe0` appends 0x650-B per-entity animation/scale trail rows (key `+0x8`, id `+0x630`, sums `+0x630..+0x640`); `FUN_14078ba00` the 0x600-B camera-trail twin; reader = `FUN_140786b60`'s ring walk.
30. **Live-ops feature-flag set (T37-5)** — the 12 `_DAT_1439xxxxxx` globals whose writes invalidate the news cache (`FUN_140771e70`): `0x1439b63e8/0x1439dc6b0/0x1439de690/0x1439de9c0/0x1439decf0/0x1439df020/0x1439de360/0x1439dd040/0x1439dd370/0x1439dd6a0/0x1439dd9d0/0x1439dcd10`. Query: grep forward for readers.
31. **Widget-name band (T38-1)** — the ~24 XOR-8 pages `0x14385bb48`–`0x14385beb0` (all 'Unknown' in the pool) are widget-clone ctor names, decode loop inline in each ctor; also `0x14385bfa0` (0x13×0x10 B selects), `0x142fac3f0` (10 qwords), `0x142fac440` (6 qwords). Query: pool-side decode of the band (strscan only names the headers).
32. **Material family `FUN_142cb…`/`FUN_142cc…` (T38-2)** — ~14 functions walked by `FUN_140792560` (`142cb4c20/3e80/3e00/3d00/4140/46b0/4920/49a0/9d60/a2a0/a180`, `142cc5730/57e0`). Query: `python scripts/crossref.py 142cb4c20`.
33. **`FUN_140c6xxxx` input family (T38-3)** — the 5.1-MB far-window stamp targets `0x140c6fba0`/`0x140c6b3db` (window reach, pass 38). Query: `python scripts/crossref.py 140c6b3db`.
34. **Widget value appliers `FUN_1409bxxxx` (T38-4)** — `FUN_1409bcab0/1409bca70` (value apply), `FUN_1409ba800/1409ba390/1409b93c0` (player records). Query: `python scripts/crossref.py 1409bcab0`.
35. **The 0xbd input rows (T38-5)** — `DAT_143b8ecd0/143b8ecd8` (0xbd × 0x10 B) drive the window-manager ctors and `FUN_1407880b0`'s per-frame state test. Query: dump `0x143b8ecd0`; grep forward for `143b8ecd8` readers.

CLOSED (machine): fd9670 recount; provenance; `0x1411b8070`; thread 43; thread 20 (`max refs:`); JSON writer/parser/CSV consumer (31/32); XOR-8 salt keys; presence-failure events; ledgers 1–4, 6, 9–12, 14, 17–21, 25, 28–29, 35, 37–38, 40 (archive). Pass 36 closes T35-1 (window split) + T35-3 (no socket layer in range). **Pass 37 closes T36-3 partially** (masked chains `0x309bbf8525c62fd2` + `0x60e93ab59bc621f8` now mapped) and the pass-36 watch item (a): the `FUN_140760130` forwards `FUN_140760c30/140761230/1407615c0` are read. **Pass 38 closes T37-4** (0x650-B = per-entity trail rows, 0x600-B = camera trail rows, reader `FUN_140786b60`) and the pass-37 watch item (a): the `FUN_140786760/1407880b0/14078dd90/14078e4e0` offcut family is read in full.

## Next pass

Resume range: **`NEXT.txt`** — written by `python scripts/pass_next.py` from
`state.json` + `--max`; regenerate it after every `--update`, never hand-edit.
Pass 38 ends at `FUN_1407a2800` (the string-intern hash-table dtor), engine-runtime
stratum `0x14054fea0` OPEN. Run `pass_measure.py <start> <end>`, quote the block or
cite its `--json` digest, run `--update`, refresh `NEXT.txt` and this file. Watch
for: (a) **window-cache continuation** — the resume range starts at `0x1407a28c0`,
just past the 0x48-B player-record family; the `0x2d1d7705` prologue signature and
the `FUN_1407a2610` handle lease (109 callers) should keep appearing; (b) the
**`FUN_140c6xxxx` input family** (thread 33) — the pass-38 far-window stamps point
there; (c) the **render-object tier** `FUN_141ff40f0/141ffed40/142042cc0/142043170`
(thread 28) — `FUN_141ffab90` also called, still undefined; (d) the **material
family `FUN_142cb…`/`FUN_142cc…`** (thread 32) — `FUN_140792560` walks it, bodies
ahead; (e) whether the UI-window tier gives way to a new subsystem past
`0x1407cc6a0`. Do not re-run a counted range through `--update` (ledger 5); no
ciphertext script line (ledger 7); leave the stale flags (ledgers 11/16) alone;
never treat `0x826e…`/`0xca334801`/`0x4343ffa4`-family or offcut-call addresses
as data (ledger 20); ledgers 24/31/39/44/49/53/54 for gaps; `size=` is not coverage
(ledger 30); overlapping windows per ledgers 39/47/49 — treat the pass-37/38
window-cache giant set (`FUN_14077d100/d230`, `FUN_140782390/2910/2d70/2e30`,
`FUN_1407839b0`, `FUN_140784720/b50/fd0`, `FUN_140786360/786760/786b60/7871b0/
7875e0/787b50/7880b0/788710/788b60/788f90/789970/78d450/78e600/78ee30/7911d0/
792560/7951c0/7980c0/7984f0/798950/79a5b0/79a9d0/79af50/79bc50/79c080/79c500`)-shaped
duplicates as one cascade each.
