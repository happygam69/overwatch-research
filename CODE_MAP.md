# CODE_MAP — cumulative map of the systematic `.text` read

**Read in full before every pass; update after every pass. Hard budget: ≤300 lines.** Per-pass
narrative lives ONLY in `ranges/`; cumulative numbers come from `state.json` (via
`scripts/pass_measure.py`) — never hand-add. Long-form archive: `CODE_MAP_ARCHIVE.md`.

## Files

| file | role |
|---|---|
| `chunks/chunk_NNNN.txt` | corpus, address order; unreachable-block warnings stripped 2026-11-21 (668,998 lines / 42.1 MB; per-chunk counts in `index.json`, pre-strip `index.pre_strip.json`) |
| `index.json` / `state.json` | per-chunk bytes / first / last (coverage truth) / machine ledger: next_chunk, per-pass entries, cumulative totals, all registration hashes, all 326 `{id,hash}` rows with match flags |
| `scripts/pass_next.py` / `NEXT.txt` | resume range (chunk range, `.text` range, commands) from `state.json.next_chunk` + the `--max` cap; `NEXT.txt` is its generated output — read it, never hand-edit |
| `scripts/pass_measure.py` / `ranges/*.md` | canonical per-pass measurement (block quoted verbatim in records or its `--json` digest cited; `max refs:` = automatic crossref of the range max; 1,204 Ghidra-named functions in chunks ≥235 are not `FUN_`-named) / per-pass records — the evidence base |
| `rdata_names.tsv` / `scripts/rdata_names.py` | plaintext `.rdata` strings (16,832 addr→text→kind rows: 15,365 ascii / 658 cstring / 809 utf16; ≥4 printable chars, controls escaped) / regenerator; query via `strlookup.py --pool rdata_names.tsv` |

## Coverage

Corpus: 2,228 chunks, 119,757 functions, 42,864,695 B `.text`. Passes 1–22 are archived in
`CODE_MAP_ARCHIVE.md` (its Coverage table covers 1–15 and 16–22); `state.json` is the truth for
per-pass `Σ size=` and every other cumulative number; the pending range is `NEXT.txt`.

| pass | chunks | `.text` range | functions | record |
|---|---|---|---|---|
| 23–24 | `0193`–`0213` | `0x1404192e0`–`0x140473f50` | 1,195 | `ranges/0x1404192e0-…`/`0x140451160-…` |
| 25–27 | `0214`–`0238` | `0x1404740d0`–`0x14054ea50` | 2,269 | `ranges/` rows 25–27 |
| 28–30 | `0239`–`0275` | `0x14054fea0`–`0x140610980` | 1,257 | `ranges/` rows 28–30 |
| 31–33 | `0276`–`0306` | `0x140610c60`–`0x14069b460` | 1,016 | `ranges/` rows 31–33 |
| 34 | `0307`–`0314` | `0x14069bb80`–`0x1406c7080` | 351 | `ranges/0x14069bb80-0x1406c7080.md` |
| 35 (9-chunk) | `0315`–`0323` | `0x1406c7b50`–`0x140738b30` | 382 | `ranges/0x1406c7b50-0x140738b30.md` |
| **total** | **323, contiguous** | `0x140001000`–`0x140738b30` | **20,130** | machine-verified (`state.json`) |

Machine-verified cumulative (`state.json` after pass 35): files 20,130 (16.81 %), Σ `size=`
5,381,142 (12.55 % of `.text`); classes reg 7,956 / wrapper 1,954 / builder 1,717 / sorted 280 /
atexit 261 / record 326 / other **7,636**; registrations 7,956 ciphertext rows all distinct (+4
plaintext rows, one hash ×2 — Corrections 16); `d4f30` 1,188 / `d4f70` 1,350 / `d4fb0` 4,492 /
`c2d70` 4,212 / `c2d50` 326 / `c7880` 261 / `atexit` 315; records 326. Passes 27–35 = consumer
only, zero registration (nine consecutive).## Corrections ledger (machine-derived; supersedes prose in older records)
5. **`--update` is forward-only; `--init` wipes the pass list.** `--update` over a counted range double-counts and rewinds `next_chunk`; repair is `--init` — why `state.json`'s pass list covers only 16–35 (totals cover 1–35).
7. **`pass_measure.py` prints no `ciphertext band:` line** — its `CTXT` regex needs `DAT_1438` + 6 hex digits; the band is now `0x1439a…`–`0x143b…`. Ciphertext extremes in records are read from the text, both addresses cited.
8. **`pass_measure.py` `zones:` filter** prints only class `reg`/`record` runs with `cnt>=3`; 1–2-function builder/wrapper runs are absent from the skeleton (they exist in the text).
13. **Allocator symbol ≠ allocator.** Per-TU one-arg symbols (`141367110`, `1412b5440`, `1418e82e0`, `1413676c0`, `141901b40/170/180`, `140f7b550`, `140f7ade0`, `14190df80`, `14191bd90`, `1419254a0`, `14192a730`; older `140f80f80`, `14114d8a0`) — key on the shape. Pass 28 adds the **container allocator** `func_0x141c23490(&PTR_PTR_143a01d18,size[,align])` + free `func_0x140578190`, 500+ sites; pass 30 uses it with a 1-byte element size throughout.
15. **Minimum registered size is 3, not 8** (`FUN_1404aad50`, size 3, align 1); span 3–0x3bc0.
20. **Decompiler fabrications:** `0x826eb8xx`, `0xca334801`, `0x38046856305b946b`, `0x0a13cb7c…`, `0x09e1c148…`, and `func_0x000102d05da9`/`func_0x00010161e575` are not code or data — they appear only after bad-instruction truncation. Never add them to a band table.
22. **Jump-table warnings** at `0x140556eb3`/`FUN_14057ad20/57b2c0/57e220` are 2-entry vtables; both arms known. **23. `pass_measure.py` `files=` counts functions, not chunks.**
24. **The corpus itself is missing functions.** Pass 29's range has 113 address gaps totalling **81,067 B (~7.7 %)** with no decompiled body — largest `0x14059a007→0x14059c350` (9,033 B), `0x1405818be→0x1405838c0` (8,194 B). Record gaps, never assume padding.
26. **`canary x69` (pass 29) is not a builder canary** (cookies + hotfix literal; class of 21). **27. `0x14384b7b0–b7bc` are plaintext floats** on an XOR-8 page — pages are not homogeneous.
30. **`sum_size` is not coverage.** In pass 30 it is 42.0 % of the span: `size=` collapses at `halt_baddata`/overlap truncation (`FUN_1405d0c40 size=1`). Always quote the address range; count gaps from headers. **31. Alignment vs missing code.** Pass 30's 486 gaps = 332 × ≤16 B (alignment), 142 × 17 B–1 KiB (under-reported `size=`), 12 × >1 KiB = 48,640 B un-decompiled.
32. **Two more hash families.** D: `(k0+k1)`/`(k0+2*k1)`, each `(x>>0x21^x)*-0xae502812aa7333 *-0x3b314601e57a13ad`, summed, `&(cap-1)`, `-1` sentinel (`0x1405d15c0`); E: descending-ordered bucket chains (`0x1405d8710`); D reappears in the store tier (`FUN_14072adf0`, pass 35). **33. Match-queue error enum 0–12** = `UserRequest, QueuePopped, QueueNotReserved, InvalidRulesetGUID, ServerError, ServerDraining, ReadyCheckTimeout, PartyNotFound, PartyAlreadyExistsInDifferentQueue, PartyFailedToJoinMatch, RulesetGUIDNotEnabled, CrossPlayChanged, MatchInputPoolChanged`, else `Invalid` (`FUN_1405ddb40`).
34. **Event names are not a plain `.rdata` table.** `rdata_names.tsv` (16,832 rows; `strlookup.py --pool`) names telemetry/protocol fields, but the pass-32 "event-name table" `0x143851c90` is in **`.data`**, pointer-shaped/encoded, not inline names (`.data` event strings `PlatformEvent`/`event-store` are decoded in `strpool.tsv`).
36. **Three masked chains coexist**: component decode `0x4d79452d…` (heaviest); per-session type table (`(x+0x3fa981c8e7192fa6) ror31 ^ 0x8784b4333a580288 → ror23 + 0x37a9e6a2eedd5214 + type*8`); per-frame handle table (`(p^0x73cc01350b9bc072)+0x704e4dbd364c5bd3 >> 0x26 | 0x4000000`); pass 35 adds the store's `0xba397115a070ffa9`+`0x4094aaa9c7911a89` row-decode chain and the `0x622b95327b2e6d1e ^ 0xd6c0ac78d0e44481` service root.
39. **The pass-33 entity update is ONE cascade seen through overlapping decompilation windows** — `FUN_140678850`/`140689930`/`14068ae00` share stamps and calls; the `0x14068xxxx` helpers have no decompiled entries; pass 33's 18 >1 KiB gaps (53,215 B) are these spans (ledger 43). **41. Per-frame handle-table rows are 16 B `{u32 handle, u32 pad, u64 entity_ptr}`** (`FUN_14067d8b0`/`140691400`); count/rows at `+0x18317a531d116c14/c0c`.
43. **Gap totals were hand-computed as distances, not gaps.** Pass 33's "41 gaps / 148,944 B" was distance-count + whole span; `gap_report.py <first> <last>` measures `next_entry − (addr + size)` and classes every >1 KiB gap (giant tail / offcut body / hole); pass 33 = **18 gaps / 53,215 B**. Re-run it for any range before quoting gap numbers; a referenced entry inside a neighbour's declared `size=` is not a gap and stays invisible to it.
44. **Pass 34 has 4 real holes (11,844 B)** — first since ledger 24: `0x1406a2aa0→0x1406a3ca0` (4,467 B), `0x1406ac0e0→0x1406ad5e0` (4,342 B), `0x1406bb060→0x1406bbe20` (1,924 B), `0x1406c5b10→0x1406c5fd0` (1,111 B), all inside obfuscated replay-capture functions; plus 4 offcut bodies (`0x1406bab10`, `0x1406b9000`, `0x1406bd560`, `0x1406c6550`). `gap_report.py 307 314` = 8 gaps / 18,144 B, 0 giant tails. `gap_report.py 307 314 --offcuts` (corpus sweep) keeps `0x1406ac0e0`/`0x1406bb060` as true holes (no reference in any chunk) and shows `0x1406a2aa0`/`0x1406c5b10` are offcut bodies referenced only from unread chunks (`0x1406a2cdb`@`0291`, `0x1406c5ba0`@`0535`): 6 offcut / 2 hole.
45. **`FUN_1406232f0` is the replay/demo frame reader too** (0x20-B variant `FUN_1406b1270`): the replay file format IS the entity bitstream; frame apply re-checks the pass-28 anti-tamper constants. **46. `FUN_1406b7500` ×211** is the canonical open-chaining table grow (16-B rows `{u32 next, u64 key, u64 val}`); pass 35 adds twin `FUN_140727340`.
47. **`FUN_1406b3220` (41,249-B text) is not a corpus maximum** — one region seen through overlapping windows (as are the `FUN_1406c2cf0`-family chat cascade and, pass 35, `FUN_1407174e0`). **48. Corpus maxima were range maxima.** `pass_measure.py --maxscan` ranks the real top: `FUN_142b567b0` **571,552 B** (chunk `2056`) > `FUN_1423add80` 414,426 > `FUN_142b4e520` 398,819 > `FUN_140a17da0` 345,153; `state.json.max_text` holds the maximum and every `pass_measure.py` block compares its range against it; the block's `max refs:` line crossrefs the range max automatically, so a NEW max is a claim until no second entry names it (47); the 571,552-B body is in an **unread** chunk (`2056`).
49. **Pass 35's 223,308-B `FUN_1407174e0` is one decompilation window over the whole store tier** — its stamps reach `0x140737d24`, past 30 later entries (class of 39/47); it is the range max (39.1 % of corpus max), NOT a corpus-max candidate. `sum_size` 23.3 % of the span is the ledger-30 effect at its most extreme: the two 111–161-KB "offcut" gaps are `FUN_1406d3ff0`/`1406efb90`'s real bodies. Corpus sweep keeps **6 holes / 18,531 B** (`0x1406ccb30`, `0x1406d2e50`, `0x1406cf520`, `0x14071af50`, `0x140728290`, `0x1406ce1a0` spans), all inside obfuscated bodies. **50. A second JSON parser exists** — the store tier parses HTTP responses with a rapidjson-style reader (`FUN_140612090` + DOM verify `FUN_1422ee440`); its verbatim error strings (codes 1–0x11, "The document is empty."…"Unknown error.") sit in `FUN_140734260`; distinct from the pass-32 text engine — do not merge the two constructs. **51. Thread 18's `FUN_14099xxxx` family is the store's platform/purchase API** (confirmed pass 35): `FUN_140992cf0/993c80/9957f0/9964f0/996720/9937a0` are called from `StoreSystem_C`; bodies still unread.
52. **Resume range and measurement provenance are generated.** `pass_next.py` writes the resume block to `NEXT.txt` (from `state.json.next_chunk` + `--max`), and `pass_measure.py --json` prints the range facts plus a 16-hex `digest` (state-derived `corpus_max` excluded) a record can cite instead of pasting the block; the block's `max refs:` line auto-crossrefs the range max. First use closes thread 20: `FUN_1407174e0` is defined once (chunk `0316`) and no other function names it.
**Closed/superseded (moved to archive 2026-11-21, pass 35):** items 1–4, 6, 9–12, 14, 17–19, 21, 25, 28, 29, 35, 37, 38, 40, 42 — record-hash match rule (1, 9, 11), sorted/atexit counts (2, 3), provenance (4), no shutdown table (6), roots regime (12), sorted-insert middle call (14), RTTI band (17), XOR pad table (18), name-page layout (19), non-builder canaries (21, 25, 26), plaintext floats (27), MSVC concurrency (28), strpool naming (29, supersedes 19), event-bus registrar (35), range maxima 100,672/101,443 B (37, 38, superseded by 48), thread-6 closure (40), per-frame rows (41→kept), match-queue enum (33 kept). Full text in `CODE_MAP_ARCHIVE.md` §Corrections archive.

## What the code is — cumulative synthesis (35 passes; evidence unless marked [inference])

`.text` is catalogued in entry-address order. After 323 chunks the cursor is at `0x140738b30`
(16.81 % of functions, 12.55 % of `.text`). Names printed `func_0x…` have **no decompiled body
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
6. **Engine runtime** `0x14054fea0`→ (passes 28–35, **OPEN**). The game client's own
   runtime: ~150-subsystem app composition/teardown, container/hash library, cvar
   registration/reading, chat/voice (Vivox), hotfix downloader, worker pool, HUD/markers,
   event bridge, spatial/entity runtime — then (31) the match-lifecycle receive side;
   (32) the **live gameplay loop** (event bus, entity replay/interpolation,
   NetworkEventSystem_C, match flow, master tick/visibility/world-to-screen, JSON text
   engine); (33) its **presentation half** (visual actors, VFX keyframe engine
   `FUN_140681360`, animation rings, widget binding, social/party-lobby layer);
   (34) its **replay/highlight/cinematic half** (progression reports + CSV export,
   demo/replay system, sequence recorder/player, spectator camera, chat/Markdown text
   UI, presence pump); and (35) its **social + monetization half** — the party/social
   service client, the obfuscated player-stat layer (weighted scoreboard,
   gameplay-sabotage detection), sound-importance cvars + spatial visibility weights,
   and the full in-game store `StoreSystem_C` (OAuth, Steam microtransactions, product
   catalog with persisted cache, virtual currency and grant reports, personalized shop,
   HTTP transport with a second rapidjson-style JSON parser).
   [inference: `0x14054fea0` marks the end of data registration and the start of
   behaviour.]

**Layer 6 constructs (passes 28–35; per-pass detail + addresses in the records):**
*infra* (28–30): handle table ×494; hash A/B/C + allocator; vector library ×983; per-site
logger; named-service registry; hotfix verifier/HTTP; worker pool ×20; component access;
spatial raycast/LOS; frame loop; event bridge; bitstream reader; debug-UI table API; CSV
iterator; HUD quad; tracked-entity; spawn queue; presence; Steam stats; XInput; JSON value
tags. *match receive side* (31): bitstream codec reader ×341 / writer ×248 + entity
header/field/baseline/component-apply + 67-KB dispatcher; restore walkers; introsort;
saved-match name tables; JSON serializer; JamMessage dispatch; event-bus subscribe;
telemetry HTTP #2. *live gameplay loop* (32): event-bus machinery + mass wiring
`FUN_14064d2a0`; `ClientLobbyMessageSystem_C`; connection state machine + toast router;
client entity runtime (component decoders, 0x468-B state copy, frame replay, interpolated
transform); scoreboard + end-of-round report; NetworkEventSystem_C (ping ring 128,
encryptor); match-flow handlers `0x4f4c–0x4f6a`; kill-feed decoder; time sync; master tick +
watchdog; telemetry JSON; ability bitsets + hero HUD; world-to-screen; FNV-1a + name
tables; JSON text engine + `"--name {json}"` pipeline. *presentation + social* (33): visual
actors; VFX keyframe engine `FUN_140681360` (corpus max) + emitters; 0x18a0-B entity
record + 0x470-B animation rings; entity state machine; u32 hash map; JSON→widget
binding; party/lobby records + debug screens. *replay/cinematic/chat* (34): progression
reports (loot-box sim + CSV export, Drive tables, leaderboards, skill-rating, XP/level-up,
match forgiveness); social-actor manager (0x240-B + 0x220-B mirror, recent-players top-5);
async file-I/O state machine (5 drainers); demo/replay system (fragment pump over the
pass-31 bitstream reader, header tables, fast-forward, CLI keys); sequence cinematic
machine (10-state, capture API); spectator view-target + view matrix; hash-table grow
×211; chat/text UI (Markdown pipeline, channel registration, command dispatcher +
arg-spec table); presence pump; new `0xde…` toasts; MSVC concurrency dtors.
*party + stats + store* (35): party/social service client (member rows 0x1d8 B, Steam-group
sync, SeasonLobbyState dumps); obfuscated player-stat layer (ruleset enum, per-hero time,
shots counters, weighted-stat scoreboard, gameplay-sabotage detector); sound-importance
cvars; spatial visibility weights (annular/obstruction/distance); 64-slot registry service
(0x228b0-B object); **StoreSystem_C** — catalog cache loader (CSV schema + 2 JSON blobs),
request state machine + pending-request queue, OAuth pair, Steam purchases + mtx
authorization + licenses, generic product sets, dynamic bundle price, `__GetProducts`
orchestrator (12 GUID sets), personalized shop, account currency, virtual-currency grant
reports, URL picker, watchdog, "Content-Encoding" header parser; hash C/D id maps; MSVC
wait-handle registry ×78.

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
| `0x143848d40`–`0x14384ad54`, `0x143864e80`–`0x143864ed8` | XOR-8 name/payload ciphertext: runtime bootstrap, settings, logger, hotfix/log format strings, ~50 console-var names (3 copies), UI/event strings (key@+0, len@+8, latch-0x48). `0x14384b7b0–b7bc` on the same page are **plaintext** floats (Corrections 27). Pass 33 adds UI/dialogue pages `0x143853c10`–`0x143855944` + fn-ptr tables `0x143854720`/`0x143856720`; pass 34 extends to `0x143857d44` (replay/sequence/chat strings); **pass 35 extends to `0x143859f58`** (party/member status, ruleset enum, stat/sabotage, store/OAuth/grant pages) + new store fn-ptr tables (`PTR_FUN_142f8a3c0…4f0`, `142f8a728/7a0`, `142f8ac68…d58`, `142f8b108/b148/b250`, `PTR_FUN_1438493b0`, `PTR_FUN_143859178`); JSON-value pools `.data 0x144137230/248/250/268` |
| `0x1438b8e50`–`0x1439a9b2c`, `0x143a16e38–2e7b` | registry name/payload ciphertext; `PTR_s_CompilerIDFilter_*`; triplet-stub object page `0x1439b0000`–`0x1439fa330` |
| `0x143a155xx`–`0x143aa36xx`, `0x143b0c…`–`0x143b77…` | XOR-40 key tables, settings names, locale/ciphertext, catch keys, `0x143a19b50–0x143a19b88` (camera/volume float block), `0x143a19938–44` (render defaults) |
| `0x143b7a428`–`0x143b7af00`, `0x143b7f410`, `0x143b808xx–0x143b81a0x` | passes 28–29 runtime block: logger objects, worker-pool state, object-id counter `0x143b91f50`, ~250 feature flags `0x143b945b8–0x143b9c5c0`; the app object; per-HUD-object flags |
| `0x143cf0000`–`0x143d05000` + far `0x143f8…`–`0x143f94…` | RTTI type_info descriptors (Corrections 17) || `0x143e99d90`–`0x14413b7a0` | registration outputs / instance slots; settings descriptors; config globals `0x144140740/758/…` |
| `0x1441e18f0`–`0x1441e67c8` | plaintext reg outputs, registry-list head `_DAT_1441e1c70`, dispatch-slot columns + readiness bitfield |
| `0x1442a1920`–`0x1442a1bd8` | plaintext struct-schema rows (`dmWorld`, `bcMtx44`, …); record pools `0x1442e37xx–0x1442f14d2` |
| `0x144226c70/80`, `0x1441d05xx` | named-service registry (lock + node list); voice levels/mic |
| `0x144180ed0`/`f20`, `0x1441b3bb8`, `0x1441880e8`, `0x1441b8170–8198` | settings-slot objects; id-intern table (buckets/counts/latch) |

**What it is for.** Layers 1–2 are a vendored NVIDIA/igzip preamble; layer 3 is compiled-in C++
static init; layer 4 registers ~8 k encrypted type names with sizes/alignment/category and builds
instances, tables and id rows from them; layers 5–6 are the client that consumes that data —
settings, telemetry, schemas, chat/voice, hotfix patching, HUD markers, the spatial/entity
runtime, the match-lifecycle receive side (pass 31), the (pass 32) **live gameplay loop**
(entity replay/interpolation, ciphered network connection, match flow, tick/visibility/
world-to-screen, JSON command pipeline), (pass 33) its **presentation half** (visual
actors, VFX keyframe engine, animation rings, widget binding, social/party-lobby layer),
(pass 34) its **replay/cinematic half** (progression reports with CSV export, the demo
replay system, the sequence recorder/player, spectator camera, chat/Markdown text UI and
the social presence pump), and (pass 35) its **social and monetization half** (the
party/social service client, the obfuscated player-stat layer with weighted scoreboard
and gameplay-sabotage detection, and the full `StoreSystem_C` in-game store: OAuth,
Steam microtransactions, product catalog with persisted cache, virtual currency and
grant reports).
No plaintext game
protocol (entity traffic is the `FUN_1406232f0`/`FUN_1406264c0` bitstream over an unframed
transport — and the replay files reuse the same reader), the render device is one opaque
`FUN_141ff40f0` call, and no gameplay *rules* are
in the read range — but the HUD, scoreboard, kill feed, match-state builders, the
social/party UI, the replay/highlight/cinematic pipeline, and now the store/monetization
and player-stat-integrity layers are.
Confidence: counts/shapes/bands measured; construct labels are shape-based inference;
obfuscated bodies read structurally only.

**Known limits.** (a) `func_0x…` bodies absent (registrar, decryptors, `0x140543xx0`
family, settings accessors, component getters, HTTP client, CSV iterator, event-bus ctors
`FUN_142e0xxxx`, cipher `FUN_142454xxx`; pass 33 adds the `0x14068xxxx` offcut helpers,
emitters `FUN_141da/141db`, anim samplers; pass 35 adds the store platform API
`FUN_14099xxxx` subset + obfuscation helpers `func_0x00014073/74xxxx`). (b) XOR-8 keys are
per-record salts; only pool text exists (ledger 29). (c) `0x142f0…`–`0x142f2b…` labelled
thunks absent. (d) Corpus gaps: pass 30's 12 × >1 KiB (ledger 31); passes 31–33 offcut/
under-reporting spans (ledger 39); pass 35's 24 × >1 KiB = 327,786 B (ledger 49: 6 corpus
holes / 18,531 B, the rest `FUN_1407174e0` window + offcut bodies). (e) Obfuscated bodies
resist decompilation: pass 32's giants (`FUN_140669ee0` 100,672-B text …) carry offcut stamps
to `0x1406a1703`; pass 33's `FUN_140681360` (101,443); pass 35's `FUN_1407174e0` (223,308,
range max, one window — ledger 49).
## Cross-cutting conventions (one line each; per-pass deltas in the records)

| convention | rule | first seen |
|---|---|---|
| TLS init guard | `*(TLS+0x50) < epoch` → `FUN_1426c3bcc(&epoch)` → `_Init_thread_footer` | `0x140001000` |
| 181-B descriptor | `{+0x20=1\|2, +0x40=ctor, +0x48=vtable/FUN, +0x50=third, +0x58=payload, +0x60=shared}` ×2,451 | `0x14003ffe0` |
| XOR-40 / XOR-8 decryptors | 8-byte key, 24-bit length; `d4f30/d4f70(&out,&buf,hash,0)` | `0x1400fbf70` |
| `{id,hash,alias}` record | two TLS guards + `c2d50(&dst,&src)`; 326 rows; ids `0x1`–`0x18b` | `0x1400fbeb0` |
| Builder | guards + `c2d70`/decrypt + `d4fb0` + row `{+0x20 root, +0x28 ptr, +0x30 0, +0x98 1, +0x9c 0}` | `0x1400fbf70` |
| Stack canary | `_DAT_143ac5f40 ^ stack` → `FUN_1426c3d40`; builders/sorted/atexit only | `0x1400fbf70` |
| Nested-atexit | guards + per-object global slot + `atexit(&LAB_142f0…)` + `c7880(&slot)`; 261 | `0x1401003f0` |
| Registration schema | 18 args; zero hash reuse; `arg18 = out − 0xa0`; flags 0 default | `0x1400fbcb0` |
| No-output registration | 242/246/252/257-B; arg17 = arg18 = 0 | `0x140341b30` |
| Sorted registry | min-to-slot-0 pre-swap + insertion sort of 2×56-B records keyed at `+8`; 280 | `0x1400ff280` |
| Settings/variable registrar | 209–399-B: 1–3 XOR-8 decrypts → `FUN_141c58170(&desc,0,&config,&name,&default)` → `_onexit(&LAB_142f16xxx)` | `0x1404b94e0` |
| Layer-4 row shapes | catch descriptor 181-B (`func_0x00014213e3d0` + handler + type_info, 272); triplet stub 66-B (`func_0x000141c712f0` ×3 + `_onexit`); "Unknown" error row ×87; component registry `{u16 id,handler,u64}` ids 1–0x19; dispatch-slot row (8 fn-ptrs + bit flip `func_0x00014224ebe0`); registry list push (LIFO `_DAT_1441e1c70`); struct schema `{&name,off,size}` at `0x1442a1920+`; metric `func_0x000141d23660(&DAT,type,"name","tag,k=v;…")` | `0x1404f8720` |
| Masked pointer | `local = 0x<const>; func_0x140543xx0(&local)` decodes it; result `^ *(u64*)(_DAT_143b79598+n)`; fail gate `0x4c208ebc71408a54` | `0x14053f9a0` |
| Obfuscated dispatcher | overlapping instructions, `halt_baddata`, `rdtsc`, POPCOUNT parity, LOCK copies, nibble tables `0x142f7aa08/aa18/d158` | `0x140541450` |
| Signature scan / patch record | `FUN_140541200`: VirtualProtect (`*_DAT_142f2d5a0`) + memcmp patterns, bytes `0x90`/`0xcc`; `FUN_140541000` writes 0x58-B record to `0x143b79640` | `0x140541000` |
| **App object** | `_DAT_143b7f410`, vtable `PTR_LAB_14328c990`, ≥0x420 B; child attach via `FUN_141c52d10` / `FUN_1405721d0` / `FUN_140572140` / `FUN_140bc7590`; ~150 children | `0x140554220` |
| **Settings accessor** | XOR-8 name buffer → `FUN_141c295b0(int)`/`280b0`/`2bfd0`/`29b00`/`28b30`/`29060(min,max)`/`2ca50`; numeric form `FUN_142d2cf30` | `0x140554220` |
| **Per-site logger** | TLS-guarded 0x28-B static via `func_0x141c48370`; `FUN_141c48450` gate → `FUN_141c48330(obj,&name,…)` | `0x1405601c0` |
| **Handle table** | 0xfff buckets, entry `{u32 handle,u64 value}`; lease `FUN_140567590` | `0x140567590` |
| **Hash maps** | A: int64 keys `(~k + k*0x40000)>>31^ …`; B: u32 keys `k*0x1001+0x7ed55d16 …`; tombstone `-1` | `0x140564ca0` |
| **Container allocator / worker pool** | alloc `func_0x141c23490(&PTR_PTR_143a01d18,size[,align])` / free `func_0x140578190` (capacity word `sign|count`); pool `FUN_141bb7520(0x20000,FUN_140573d40,ctx,name,0x14)`, enqueue `FUN_140573f10`, stop `FUN_140573fc0` | `0x140558120` |
| **Hotfix/integrity** | 0x30-B record `{hash,idx,verified,handle,ts}` → SHA-256 memcmp; tags `"hotfix"`/`"canary"`; traps `"0x811C9DC5"` etc. | `0x14056cd40` |
| **Component access** | `func_0x140c503d0(entity,id)` has / `func_0x140c506f0(entity,id,default)` get; ids `0xd80000000007a7b` etc. | `0x14057a870` |
| **Spatial query** | 4-float ray → `FUN_14206b500/14206a660` → `rsqrtss`+Newton normal | `0x140579010` |
| **Event tag / payload** | `FUN_140583fb0` pushes 0x18-B `{ptr,ptr,u32,2}`; fill with `FUN_141940c00/0db0/0e00/1360`; ids `0xa4…`/`0x2400…`/`0xde0…`/`0xd8…`; send `FUN_1405ae0e0` or app vtable `+0x140/+0x150` | `0x140584450` |
| **0x19c message** | `FUN_141c23430(buf,0x19c)` + `func_0x141b39150` + `FUN_14200dee0(dst,buf,0)`; `0/0xffffffff` slot pairs | `0x140594cd0` |
| **Console-var registrar** | XOR-8 name pair → `FUN_141c29b00` \| `FUN_141c2a030` (float) \| `FUN_141c2bfd0` \| `FUN_141c285e0`; defaults 100.0f/5.0f/1/0; 3 duplicated copies under latch `DAT_143b80a9c` | `0x140596b00` |
| **HUD marker** | 0x90-B quad record (verts `+0x540..0x578`); occlusion `FUN_142032690`; projection `FUN_14059d730` | `0x14059dad0` |
| **Tracked-entity row** | 0x58/0x60/0x68-B rows: key `+0`, prio `+0x38`, flags `+0x50`, slot `+0x58`, state `+0x5c`; expiry `+0x10/+0x18` | `0x140588370` |
| **Table/debug UI** | `FUN_141c64c10` begin → `…64c30("col",0)` → `…64cd0` row → `…64df0/64e30/650c0/65050` cells → `…651a0` end | `0x1405a2ba0` |
| **Hash family C** | `h=(k*0x200000+~k); (h>>0x18^h)*0x109; (h>>0xe^h)*0x15; (h>>0x1c^h)*-0x7fffffff & (cap-1)`; chained `{next,key,val}` or range layout; byte-keyed handler registries `FUN_140621990/aa0` (pass 31) | `0x140599970` |
| **Command dispatcher / JamMessage** | `(**(code**)(*disp+0x10))(disp,fn,id,0)` (and `+0x30`); ids `0x48,0x53,0x7c,0x7d,0xa5,0xb2`; ~50 dispatchers map contiguous id blocks to handlers; default `FUN_140548d00` ×97 | `0x1405ac510` |
| **CSV / presence (28–30)** | CSV iterator `func_0x1423887b0/388a00/388ab0/388af0/3887e0` (0x20-B rows); presence `{bnet_dbid,title_id,group,field,unique_id}` via `FUN_141c63bc0` (row 0x58 B) | `0x1405afc60` |
| **JSON value** | 0x10-B `{data, u16 tag @ +0xe}`: `3` obj, `4` arr, `9/0xa` true/false, `0x?96/0x?d6` ints (0x20=signed, 0x40=32-bit, 0x100=wide), `0xc05` heap string, `0x1c05` inline (`len = 0xd - low byte`); **writer** `FUN_1406331b0` (tags 0–5/num; double `FUN_140635480`, u64/u32 `FUN_140637450/371f0`, pair table `DAT_142f86ee0`) | `0x14060fc90` |
| **Bitstream codec / entity delta** | reader `FUN_1406232f0` (≤64-bit spans, `{words,cur,idx@+0x1c}`) / writer `FUN_1406264c0`; entity header `FUN_140622f00` (0xc-bit flags → 6 field widths, out 0x38-B); field `FUN_140623120`; baseline/delta `FUN_1406251a0`; component apply `FUN_140625950`; dispatcher `FUN_140623900`; event-bus subscribe `0x14063ddf0`+ | `0x1406232f0` |
| **Event-bus (32)** | map `FUN_14064cdd0(bus+0x48,id)` → 0xb0 descriptor; dispatch `FUN_14064d0d0/140`; registrar 3-variant (listen `mask\|2` / announce `mask\|1` / `FUN_142e04e00`); event ids hash-obfuscated (`FUN_14053bd90`) | `0x140644930` |
| **Session masked table** | `(row+0x160 + 0x3fa981c8e7192fa6) ror31 ^ 0x8784b4333a580288 → ror23 + 0x37a9e6a2eedd5214 + type*8`; per-frame handle table rows 16-B @ `+0x18317a531d116c0c/c14` | `0x14064efa0` |
| **Net frame + cipher (32)** | incoming: 0x22-bit header, type nibble `buf+0xc`, ping ring 128; outgoing: `FUN_140654c50` 16-bit time + 8-bit seq, `FUN_140657580` presence-bit + 32-bit length, then cipher `FUN_142454xxx` + bit-splice `FUN_14065aaa0` | `0x140654c50` |
| **JSON text engine (32)** | recursive parser `FUN_140673120` (errors 3–7/0x10); number `FUN_140672500`; string `FUN_140672c80` (SIMD tables `0x142f888c0…88ef`, `\u`+surrogates); writer = `FUN_14066b5d0` + serializer `FUN_1406331b0` | `0x140672500` |
| **Command string (32)** | build `"--%s %s"` + `{json}` (`FUN_140673be0/140675580`) → submit `PTR_FUN_143849970` vt+0x188; queue (12-s TTL) → executor `FUN_140676370` (7-field lookup → hero-GUID check) | `0x140673be0` |
| **Entity record 0x18a0 B (33)** | move `FUN_140687fe0`, dtor `FUN_1406895d0`; transforms ×8 `+0x1300-139c`, net id `+0x1390/94`, bone rows 0x1c `+0xe50`, sub-records 0x470 `+0x70/4f0/970`; animation snapshot rings (controller `comp+0x18`, snapshots 0x470-B, rows 0x30-B `+0x12040`) | `0x140687fe0` |
| **VFX keyframe engine (33)** | rows 0x650 B, ~21 toggle tracks, keyframe binsearch+lerp, time remap `×_DAT_142f80ff8`; emitters `FUN_141da/141db` | `0x140681360` |
| **JSON→widget binding (33)** | `FUN_141940ef0(widget, 0xd8…id, &value)`; value ctors `FUN_141940ea0/1419413b0/141940c50/141941360/141940c00`; widget ids `0xd8000000000 88a6/8d70/618e/2e4a/aa7c…aba3`; result pools `.data 0x144137230/250` | `0x14068b890` |
| **File I/O state machine (34)** | 5 drainers on 0x10-B rows (delete/size/open/save/rename): flag `+0x128`, refcount `+0x129`, done `+0x12a`; retry `FUN_1407ce8d0` | `0x1406a7b40` |
| **Demo/replay system (34)** | record 0x1d0 B (`FUN_1406a99c0`, state `+0xf8` 0–3, event 0x39); fragment pump `FUN_1406b06e0` ≤0x1e/tick; frame apply = `FUN_1406232f0(state,0x20)` + anti-tamper; header 0x120 B; CLI keys format/fastforward/commandframe/target/loop/live; magic `0x7495174655b5d763` | `0x1406a99c0` |
| **Sequence cinematic machine (34)** | `FUN_1406b81d0`: state `+0x148` 0–10, type `+0xc4` 1–5; capture API `FUN_14206b2d0/afb0/b480/b460`; resolution 0x80–0x800, fps 8 | `0x1406b81d0` |
| **Hash-table grow (34)** | `FUN_1406b7500` ×211: power-of-2 buckets, 16-B rows `{u32 next, u64 key, u64 val}`, `FUN_142efe950` fill −1, re-chain `(cap−1)&hash`; probe `FUN_1406b5a30` | `0x1406b7500` |
| **Chat/text UI (34)** | Markdown pipeline: escaper `FUN_1406c24f0` (0x3fc cap) → span sort `FUN_1406c02f0` → merge `FUN_1406c1520` → redact `FUN_1406c2080`; submit `FUN_1406c36c0` (channels 0–6); register `FUN_14055e790`; id tables `DAT_142f89a30/142f89e70`; arg-spec table `0x143857998` | `0x1406c21d0` |
| **Social-actor manager (34)** | record 0x240 B `FUN_1406a4e90` (GUID blocks +0x18/+0x50/+0x70/+0xa8, bucket inits `FUN_142c95xx0`); 0x220-B net-state mirror `FUN_1406a6060`; hash lookup `FUN_1406a4be0` (0x10-B key); recent-players top-5 (`FUN_1406a7910`, 1-day gate 0x15181) | `0x1406a4e90` |
| **Party/social + stats (35)** | member rows 0x1d8 B (dtor `FUN_1406c8230`); Steam-group sync `FUN_1406caa00`; SeasonLobbyState dumps `FUN_1406cc030/1406cbc50`; ruleset enum 16 names (pages `0x1438586c0`+); weighted-stat scoreboard `FUN_14071dce0`; gameplay-sabotage detector `FUN_14071d290`; GUID→name `FUN_14071ea70` | `0x1406c7b50` |
| **StoreSystem_C (35)** | object 0x390 B (ctor `FUN_14072c560`); product rows 0x1b8 B; catalog cache loader `FUN_14072e230` (CSV schema + 2 JSON blobs); pending-request queue 0x110-B `{id,next}`, states 0/4/5/9/0xc/0xd; OAuth `FUN_140734af0/260`; Steam mtx (`STEAMINVENTORY_INTERFACE_V003`); URL picker `FUN_140738790`; auth-error gate `{0x191,0,0x1ad,5xx}`; "Content-Encoding" parser `FUN_140738b30`; grant pipeline `_tier_`/"BattlePass: … - Tier …" | `0x14072c560` |
| **JSON parser #2 (35)** | rapidjson-style reader `FUN_140612090` + DOM verify `FUN_1422ee440`; verbatim error table 1–0x11 ("The document is empty."…"Unknown error.") in `FUN_140734260`; distinct from pass-32 engine | `0x140734260` |

## Open threads (cheapest next query each; check/update every pass)

2. **0x19c-B / entity-state transport framing** — pass 32 found the client framing (`FUN_140654c50` 16-bit time + 8-bit seq; `FUN_140657580` presence-bit + 32-bit length); remaining: the socket/UDP layer carrying the finalized buffer — grep forward for `FUN_142454xxx` cipher outputs. Pass 35 adds the store's HTTP transport (header parser `FUN_140738b30`, watchdog `FUN_1407388d0` writes diagnostics) — entity transport still ahead.
5. **Command ids `0x48/0x53/0x7c/0x7d/0xa5/0xb2/0x3a`** — grep later chunks for `+0x10))(…,0x`/`+0x30))(…,0x`; pass 32 adds gated blocks `0x4f4c–0x4f6a`, `0x64c8–0x64d4`, `0x6b6c/d`, `0xa794–0xa79a`; pass 33 adds plain ids 0x33/0x3a/0x37/0x72; pass 34 adds plain ids 0x24/0x2d/0x2e/0x38/0x39/0x41/0x51 + the `0xde…` toast set; pass 35 adds `0x24`/`0x47` (stat JamMessage subscription), `0x58661fbe`-family handler ids, and `0xde…` toasts 43c/43b/45e0/17438/8c77/8f5d/1a50/4070/433.
6. CLOSED (pass 33, ledger 40) — `FUN_141c2a030` negative min found.
7. **`FUN_141c295b0`/`FUN_141c58170`/`FUN_142d2cf30` bodies** — `FUN_`-named, unread corpus (~chunk `15xx`). **8. `func_0x140543xx0` family** — absent; test the masked-pointer chain against a known `.data` address.
9. **`0x143b945b8`–`0x143b9c5c0` (~250 flags)** — grep forward for `143b94`/`143b95`/`143b9c` readers. **10. `_DAT_143b7f410` field map** — merge `FUN_140554220/5559c0/585220` for ~150 offsets.
11. **Channel list `_DAT_143c00680`** — writer found (pass 32: `FUN_140663de0`); the renderer that walks it is still unfound. **12. Hotfix file identity** — dump one 0x30-B record (`_DAT_1439d98c0`); backoff table `_DAT_1439d9890`.
13. **Gaps** — pass 35: 24 × >1 KiB = 327,786 B (ledger 49: 6 corpus holes / 18,531 B at `0x1406ccb30`, `0x1406d2e50`, `0x1406cf520`, `0x14071af50`, `0x140728290`, `0x1406ce1a0` spans; the rest is the `FUN_1407174e0` window + offcut bodies); pass 34's 4 holes / 11,844 B (ledger 44); pass 30's 12 × >1 KiB (ledger 31); `0x14059a007–0x14059c350` (9,033 B) and `0x1401a4e02–0x1401abad0` (27,854 B) still open. **14. CompilerIDFilter** — unchanged (pass 21); payloads are regs.
15. **Event-bus / gameplay names — table still open.** the 68-entry `.data` table `0x143851c90` remains encoded (ledger 34); chat id tables `DAT_142f89a30[id]`/`DAT_142f89e70[id]` and arg-spec table `0x143857998` still need raw dumps. Next: decode `0x143851c90`.
16. **Pass-32/33/34 machinery bodies** — cipher family `FUN_142454xxx`; event-hash resolver `FUN_14053bd90`; session type-code getters; offcut `0x14068xxxx` helpers; emitters `FUN_141da/141db`; anim samplers; camera-capture API `FUN_14206b2d0/afb0/b480/b460`; state-5/6 handlers `FUN_1406bd560`/`1406b9000` (offcut). **17. Handle-table writers** — row shape known; writer unfound — grep forward for `0x18317a531d116c`.
18. **Party/lobby `FUN_14099xxxx` family** — pass 35 confirms it is the **store/platform purchase API** (`FUN_140992cf0` request post, `FUN_140993c80` scope/region, `FUN_1409957f0` time source, `FUN_1409964f0` per-row test, `FUN_140996720` license check, `FUN_1409937a0` region/enum, `FUN_140993710/140997520` product lookups) — called constantly by `StoreSystem_C`; **bodies at `0x14099xxxx` remain unread** (cursor at `0x140738b30`); grep forward when the read reaches them.
19. **Widget/party enum pages** — XOR-8 names `0x143854b30–0x143854cb0` and the party-screen columns `0x1438556b0–0x143855790`; decode via `strpool.tsv`/`poolmap`. Pass 34 extends the XOR-8 band to `0x143857d44` (replay/chat log strings); **pass 35 extends it to `0x143859f58`** (party/member status, ruleset enum, stat/sabotage, store/OAuth/grant pages).
20. **`FUN_1407174e0` window split (T35-1)** — CLOSED by the standing `max refs:` check: `python scripts/crossref.py 1407174e0` = defined once (chunk `0316`), no other function names it, so its 223,308-B text is a single window over bodies Ghidra never filed as entries — there is no second entry set to split off (ledger 52).
21. **Store endpoint labels (T35-2)** — decode XOR-8 pages `0x1438595b0–0x1438597c8` (`python scripts/strlookup.py --band 0x1438595b0 0x1438597c8`) to name the six 2,495-B response-handler twins; 'StorefrontService/v1/GetCurrentPages' and '/ProductCatalogService/v1/GetProductsByStoreId' are already visible.

CLOSED (machine): fd9670 recount; provenance; `0x1411b8070`; thread 43; thread 20 (`max refs:`); JSON writer/parser/CSV consumer (31/32); XOR-8 salt keys; presence-failure events; ledgers 1–4, 6, 9–12, 14, 17–21, 25, 28–29, 35, 37–38, 40 (see Corrections archive).

## Next pass

Resume range: **`NEXT.txt`** — written by `python scripts/pass_next.py` from
`state.json.next_chunk` + `--max`; regenerate it after every `--update`, never hand-edit.
Pass 35 ends at `FUN_140738b30`, engine-runtime stratum `0x14054fea0` OPEN. Run
`pass_measure.py <start> <end>`, quote the block or cite its `--json` digest, run `--update`,
refresh `NEXT.txt` and this file. Watch for: (a) the **store/monetization continuation** — the
`StoreSystem_C` tier (chunks 0319–0323) references platform bodies just ahead:
`FUN_1407398c0/14073a020` (session store), `FUN_140736160/1407366b0/140736790`
(gate/URL helpers), `FUN_140739cf0`, plus the six 2,495-B response-handler twins'
endpoints (thread 21); (b) the **`FUN_14099xxxx` platform/purchase API** (thread 18,
now the store's confirmed dependency) — bodies at `0x14099xxxx`, still far ahead;
(c) the **socket/transport layer** under the cipher `FUN_142454xxx` (threads 2/17) —
the store's HTTP transport (`FUN_140738b30` header parse, `FUN_1407388d0` watchdog)
suggests the socket layer is nearby (thread T35-3); (d) whether the store stratum
gives way to new gameplay systems or more client services; (e) the 223-KB
`FUN_1407174e0` window is one emission (thread 20 closed, ledger 52), so the next
chunks should be ordinary store/service bodies. Do not re-run a
counted range through `--update` (ledger 5); no ciphertext script line (ledger 7);
leave the stale flags (ledgers 11/16) alone; never treat `0x826e…`/`0xca334801` or
offcut-call addresses as data (ledger 20); ledgers 24/31/39/44/49 for gaps; `size=`
is not coverage (ledger 30); overlapping windows per ledgers 39/47/49 — treat
`FUN_140678850`/`140689930`/`14068ae00`-, `FUN_1406c2cf0`/`1406c3ec0`/`1406c44c0`/
`1406c4b20`/`1406c50b0`-, and `FUN_1407174e0`-shaped duplicates as one cascade
each.
