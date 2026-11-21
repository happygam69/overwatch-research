# CODE_MAP — cumulative map of the systematic `.text` read

**Read in full before every pass; update after every pass. Hard budget: ≤300 lines.** Per-pass
narrative lives ONLY in `ranges/<first>-<last>.md`; cumulative numbers come from `state.json`
(via `scripts/pass_measure.py`) — never hand-add. Long-form archive: `CODE_MAP_ARCHIVE.md`.

## Files

| file | role |
|---|---|
| `chunks/chunk_NNNN.txt` | corpus, address order; `Removing unreachable block` warnings stripped in place 2026-11-21 (668,998 lines / 42,145,998 B; per-chunk counts in `index.json`, pre-strip `index.pre_strip.json`); every code line present |
| `index.json` / `state.json` | per-chunk bytes / first / last (coverage truth) / machine ledger: next_chunk, per-pass entries, cumulative totals, all registration hashes, all 326 `{id,hash}` rows with match flags |
| `scripts/pass_measure.py` / `ranges/*.md` | the canonical per-pass measurement (stdout quoted verbatim in records; 1,204 Ghidra-named functions in chunks ≥235 are not `FUN_`-named) / per-pass records named by `.text` range — the evidence base |
| `rdata_names.tsv` / `scripts/rdata_names.py` | plaintext `.rdata` strings (16,832 addr→text→kind rows: 15,365 ascii / 658 cstring / 809 utf16; ≥4 printable chars, controls escaped) / regenerator; query via `strlookup.py --pool rdata_names.tsv` |

## Coverage

Total corpus: 2,228 chunks, 119,757 functions, 42,864,695 B `.text` (raw index bytes 325,787,798).

Passes 1–22 are archived in `CODE_MAP_ARCHIVE.md` (Coverage + Coverage archive); `state.json` remains the machine truth.

| pass | chunks | `.text` range | functions | Σ `size=` | record |
|---|---|---|---|---|---|
| 23 (10-chunk) | `0193`–`0202` | `0x1404192e0`–`0x140451060` | 738 | 203,154 | `ranges/0x1404192e0-0x140451060.md` |
| 24 (11-chunk) | `0203`–`0213` | `0x140451160`–`0x140473f50` | 457 | 132,700 | `ranges/0x140451160-0x140473f50.md` |
| 25 | `0214`–`0221` | `0x1404740d0`–`0x140495d90` | 453 | 126,840 | `ranges/0x1404740d0-0x140495d90.md` |
| 26 | `0222`–`0229` | `0x140495e90`–`0x1404bfd20` | 557 | 148,986 | `ranges/0x140495e90-0x1404bfd20.md` |
| 27 | `0230`–`0238` | `0x1404bfe00`–`0x14054ea50` | 1,259 | 200,071 | `ranges/0x1404bfe00-0x14054ea50.md` |
| 28 | `0239`–`0253` | `0x14054fea0`–`0x14057fe40` | 336 | 100,696 | `ranges/0x14054fea0-0x14057fe40.md` |
| 29 | `0254`–`0266` | `0x14057ff10`–`0x1405b2ee0` | 401 | 141,297 | `ranges/0x14057ff10-0x1405b2ee0.md` |
| 30 | `0267`–`0275` | `0x1405b3080`–`0x140610980` | 520 | 160,792 | `ranges/0x1405b3080-0x140610980.md` |
| 31 | `0276`–`0285` | `0x140610c60`–`0x1406446c0` | 446 | 154,182 | `ranges/0x140610c60-0x1406446c0.md` |
| 32 | `0286`–`0294` | `0x140644930`–`0x140676370` | 372 | 145,579 | `ranges/0x140644930-0x140676370.md` |
| **total** | **295, contiguous** | `0x140001000`–`0x140676370` | **19,199** | **5,029,889** | machine-verified (`state.json`) |
| pending | `0295`–`2227` | `0x140676370`→ | — | — | resume at `chunk_0295` |

Machine-verified cumulative (`state.json` after pass 32): files 19,199 (16.03 %), Σ `size=`
5,029,889 (11.73 % of `.text`); classes reg 7,956 / wrapper 1,954 / builder 1,717 / sorted 280 /
atexit 261 / record 326 / other **6,705**; registrations 7,956 ciphertext rows all distinct (+4
plaintext rows, one hash ×2 — Corrections 16); `d4f30` 1,188 / `d4f70` 1,350 / `d4fb0` 4,492 /
`c2d70` 4,212 / `c2d50` 326 / `c7880` 261 / `atexit` 313; records 326. Passes 27–32 = consumer
only, zero registration (six consecutive).## Corrections ledger (machine-derived; supersedes prose in older records)

1. **`{id,hash}` records match 75/75, not 74/75.** Pass 15's "unmatched" hash `0x3fd91271` (id `0x35`) is the registration hash of `FUN_140290c50` (chunk `0114`). Thread 43 CLOSED. Pass 16 adds 23 rows; pass 17 adds 45.
2. **Sorted-insert builders: 280 cumulative** after pass 26 (249→+31). Use `state.json`.
3. **Nested-atexit builders: 261 cumulative**; shapes 526/542/558-B; initializer families grow per pass. The `atexit` counter rose to 313 in pass 29 but that call is a settings-id static, not a builder (ledger 25).
4. **Provenance caveat:** passes 1–15 records state counts without a quoting script (their ad-hoc scripts were not kept). All passes' `files`/Σ `size=` are reproduced by `scripts/pass_measure.py`.
5. **`--update` is forward-only; `--init` wipes the pass list.** `--update` over an already-counted range double-counts and rewinds `next_chunk`; repair is `--init` — why `state.json` lists only passes 16–28.
6. **There is no shutdown table and no "move".** Shutdown rows are per-object global slots scattered by the linker (`0x1438e…`, `0x143ce7…`, `0x143e5e/6…`, `0x143c3ab20/ba40`, `0x143e92/94…`, `0x144101c90`, `0x144123ab0–af0`, `0x144126320–378`, `0x14412cd58/da0`, `0x14412e078–0b0`, `0x144136068–0a8`, `0x14398bc98–d58`); the code addresses each absolutely.
7. **`pass_measure.py` prints no `ciphertext band:` line** — its `CTXT` regex needs `DAT_1438` + 6 hex digits; the band is now `0x1439a…`–`0x143b…`. Ciphertext extremes in records are read from the text, both addresses cited.
8. **`pass_measure.py` `zones:` filter** prints only class `reg`/`record` runs with `cnt>=3`; 1–2-function builder/wrapper runs are absent from the skeleton (they exist in the text).
9. **`record-hash = registration-hash` is a rule; the two historical exceptions are resolved by direct evidence.** `FUN_14036bb60` (chunk `0156`) registers `0x39091531`, the hash of record ids `0x3e`/`xcb`. The two `state.json` rows stay `matched:false`; treat them as stale.
10. **The 178-B third field is an alias registration hash, not a flag.** Row layout = `{id, hash, alias}`; most third fields are 0.
11. **Corrections 9 is closed by direct evidence** — see item 9; keep the two stale flags untouched.
12. **Roots alternate; "static-root era over" is retired.** Pass 26 roots sit almost entirely on registration outputs; static `0x143cf/d…` roots are the minority. Regime is per-block, not a timeline.
13. **Allocator symbol ≠ allocator.** Per-TU one-arg symbols (`141367110`, `1412b5440`, `1418e82e0`, `1413676c0`, `141901b40/170/180`, `140f7b550`, `140f7ade0`, `14190df80`, `14191bd90`, `1419254a0`, `14192a730`; older `140f80f80`, `14114d8a0`) — key on the shape. Pass 28 adds the **container allocator** `func_0x141c23490(&PTR_PTR_143a01d18,size[,align])` + free `func_0x140578190`, 500+ sites; pass 30 uses it with a 1-byte element size throughout.
14. **The sorted-insert middle call is the ordinary pre-step slot.** Not a second decrypt stage.
15. **Minimum registered size is 3, not 8** (`FUN_1404aad50`, size 3, align 1); span 3–0x3bc0.
16. **Zero hash reuse is conditional.** Pass 27's 4 plaintext rows (`"teStructuredData"` ×2, `"MirrorData"`, `"TrackedData"`) trip the check legitimately. Do not "repair" `state.json`.
17. **The static `0x143cf…/0x143d…` band is RTTI type_info**, not "class roots"; the band's content label is superseded (root wording in 12 still holds for builder roots).
18. **`0x143b79598` is a XOR pad table.** Pass 27's "config block" wording is refined: `local = 0x<const>; func_0x140543xx0(&local)` decodes a *compile-time* masked pointer; the result is XORed with `*(u64*)(_DAT_143b79598 + n)`. ~40 sites in pass 28.
19. **Name ciphertext pages extended** (pass 28): `0x1438493c8–0x1438497f8`, `0x1438499a0–0x14384a3bc`, `0x14384a428–0x14384ad54`, `0x143a16e38/58/70`. Same layout as the registry (key[8] @ +0, u32 len @ +8 `&0xffffff`, done-flag = high byte `0x48`, payload @ +0xc). No name decrypted yet.
20. **Decompiler fabrications:** `0x826eb8xx`, `0xca334801`, `0x38046856305b946b`, `0x0a13cb7c…`, `0x09e1c148…`, and `func_0x000102d05da9`/`func_0x00010161e575` are not code or data — they appear only after bad-instruction truncation. Never add them to a band table.
21. **`canary x32` in pass 28 is not a builder canary.** It counts `FUN_1426c3d40` cookie calls plus the hotfix literal `"canary"` (`FUN_141bb9610(...,"canary")`). No builder exists in that range.
22. **Jump-table warnings** at `0x140556eb3` and in `FUN_14057ad20/57b2c0/57e220` are 2-entry vtables `{FUN_14057ae30, FUN_14057ae30}` / `{FUN_14057af70, FUN_14057ae80}`; both arms are known.
23. **`pass_measure.py` `files=` counts functions, not chunks** (pass 29: 401 files over 13 chunks; chunk `0258` holds 24, chunk `0259` holds 4).
24. **The corpus itself is missing functions.** Pass 29's range has 113 address gaps totalling **81,067 B (~7.7 %)** with no decompiled body — largest `0x14059a007→0x14059c350` (9,033 B), `0x1405818be→0x1405838c0` (8,194 B), `0x1405ae2fb→0x1405afaf0` (6,133 B). Record gaps, never assume padding.
25. **`atexit` 312→313 (pass 29) is not a builder.** The one call is `FUN_1405924c0`'s TLS static `{0x75,0x77}` + `atexit(&LAB_142f01c90)`. Nested-atexit builders stay 261.
26. **`canary x69` (pass 29) is not a builder canary**: `FUN_1426c3d40` cookies + the hotfix `"canary"` literal. Same class as ledger 21.
27. **`0x14384b7b0–0x14384b7bc` are plaintext floats** read without XOR by the HUD code, on the same page as XOR-8 strings. Pages are not homogeneous — check each datum.
28. **MSVC concurrency bodies are in `.text`**: `0x140586870`/`0x1405868c0` are `Concurrency::details::UMSFreeThreadProxyFactory` scalar-deleting destructors (`Library Function - Single Match`).
29. **The XOR-8 name pages are already decoded, in this repo.** `strpool.tsv` (regenerated by `../ship_strpool.py` from `../../strpool.txt` + `../../poolmap.tsv`) is anchored at **page base + 8** (the length word; key@+0, payload@+0xc). Read via `scripts/strlookup.py` (address/`--band`/`--grep`/`--count`) and `scripts/strscan.py` (chunk → `DAT_` pages); both stdlib-only. Ledger 19's "no name decrypted yet" is superseded for naming. `Unknown` rows carry their stripped identity (class/field/enum value/enum type/owner; `STRPOOL_UNKNOWN.md`); the 1,185 residual `Unknown` rows are genuine literal placeholders (full-image Ghidra xrefs, 0 new names).
30. **`sum_size` is not coverage.** In pass 30 it is 42.0 % of the 383,232-B address span: `size=` collapses at `halt_baddata`/overlapping-instruction truncation (`FUN_1405d0c40 size=1`, `FUN_1405c7710 size=1482`). Always quote the address range, and count gaps from the per-function headers.
31. **Alignment vs missing code.** 486 inter-entry gaps in pass 30 = 332 × ≤16 B (alignment), 142 × 17 B–1 KiB (mostly under-reported `size=`), **12 × >1 KiB = 48,640 B of genuinely un-decompiled code** (largest `0x1405ca0f1→0x1405cc1d0`, 8,415 B).
32. **Two more hash families.** D: `h=(k0+k1)` and `(k0+2*k1)`, each `(x>>0x21^x)*-0xae502812aa7333` then `*-0x3b314601e57a13ad`, summed, `&(cap-1)`, `-1` sentinel (`0x1405d15c0`). E: descending-hash-ordered bucket chains with reserve flags `+0x8`/`+0x9`, rehash `<0x3fdc` (`0x1405d8710`).
33. **Match-queue error enum 0–12** = `UserRequest, QueuePopped, QueueNotReserved, InvalidRulesetGUID, ServerError, ServerDraining, ReadyCheckTimeout, PartyNotFound, PartyAlreadyExistsInDifferentQueue, PartyFailedToJoinMatch, RulesetGUIDNotEnabled, CrossPlayChanged, MatchInputPoolChanged`, else `Invalid` (`FUN_1405ddb40`, pages `0x14384dad0…0x14384dc80`).
34. **Event names are not a plain `.rdata` table.** `rdata_names.tsv` (16,832 `.rdata` strings — ascii/cstring/utf16, regenerated by `scripts/rdata_names.py`; query with `strlookup.py --pool`) names telemetry/protocol fields, but `strlookup.py` on the `PTR_DAT_143b…` pointers still finds no pool row, and the pass-32 "event-name table" `0x143851c90` is in **`.data`**, not `.rdata`; its bytes are pointer-shaped/encoded, not inline names. `.data` event strings already decoded in `strpool.tsv` (`PlatformEvent`, `event-store`).
35. **The event-bus registrar is three-variant** (listen `mask|2` / announce `mask|1` / `FUN_142e04e00` pair) and **`FUN_14064cdd0` is the std::map<u32 id→0xb0 descriptor>** behind `FUN_142e029b0` (122 callers; listener list `desc+0x60`, refcount `+8`).
36. **Three masked chains coexist**: component decode `0x4d79452d…` (pass 27, heaviest); per-session type table (`(x+0x3fa981c8e7192fa6) ror31 ^ 0x8784b4333a580288 → ror23 + 0x37a9e6a2eedd5214 + type*8`); per-frame handle→entity table (`(p^0x73cc01350b9bc072)+0x704e4dbd364c5bd3 >> 0x26 | 0x4000000`).
37. **`FUN_140669ee0` (100,672-B text) is the largest function in the corpus**; its return-address stamps reach `0x1406a1703`, so chunks after `0295` begin with its `0x14068xxxx` helper family.

## What the code is — cumulative synthesis (32 passes; evidence unless marked [inference])

`.text` is catalogued in entry-address order. After 295 chunks the cursor is at `0x140676370`
(16.03 % of functions, 11.73 % of `.text`). Names printed `func_0x…` have **no decompiled body
in this dump** — registrar, decryptors `d4f30`/`d4f70`, writer `c2d50`, helpers `c2d70`/`c7880`,
the `0x140543xx0`/`0x1405674xx` decoder family, settings accessors, component getters, the hotfix
HTTP client, the CSV parse iterator and the pass-32 cipher family `FUN_142454xxx` — as does
`tls_callback_0` (generic list insert/update). **Six layers, in address order:**

1. **Library preamble** `0x140001000`–`0x140039fc0`. ISA-L/igzip DEFLATE inflate (12 fns);
   `nvapi_QueryInterface` bootstrap; 53 NVAPI entry wrappers; `Initialize`/`Unload`.
2. **NVIDIA driver-loading shim** `0x14003a230`–`0x14003d330`. Replacement `LoadLibrary` for
   `nv*.dll` (D3DKMT, SetupAPI, service paths, Khronos keys).
3. **CRT/C++ static-init sea** `0x14003ffe0`–`0x1400fa760`. Five generator templates: 181-B
   MSVC magic-static descriptor (**2,451**), 209-B locale/facet statics (354), 58-B event thunks
   (284), 134-B XOR-40 + cipher registrations (61), 37-B `_onexit` stubs; pass-1 tail: 864
   descriptors + 39 shared `PTR_DAT_14386a…` markers.
4. **Typed registry machine** `0x1400fbcb0`–`0x14054ea50` (passes 2-tail–27, CLOSED). Nine
   constructs; families: CompilerIDFilter, physics/serialization schemas (`dm*`/`bc*`),
   telemetry (`circuitbreaker.*`, `gameruleset.gameoptions.*`), catch descriptors, component
   id→handler registry, dispatch rows, plaintext struct schemas.
5. **Runtime bootstrap + obfuscated dispatchers** `0x14053f6b0`–`0x14058200x` (pass 27). PE
   `entry` trampoline `0x140540fd0`; **signature scanner** `FUN_140541200` → patch record at
   `0x143b79640`; anti-tamper (CPUID FPU gate, `"0x811C9DC5"`); masked-pointer/obfuscation
   layer with 16–47 KB bodies (`halt_baddata`, `rdtsc`, POPCOUNT parity, nibble tables).
6. **Engine runtime** `0x14054fea0`→ (passes 28–32, **OPEN**). Consumer stratum: app-object
   composition and teardown (~150 subsystems), the container/allocator/hash library,
   **console-variable registration + reading** of layer 4's registrar data, chat/voice
   (Vivox), **hotfix/patch downloader** (HTTP + SHA-256), 20-thread worker pool, parallel
   per-entity update, **HUD/marker layer**, **event bridge** (`0xa4…`/`0x2400…`/`0xde…` tags),
   debug tables, Battle.net "BGS" club plumbing, spatial/entity access by 64-bit id, the
   match-lifecycle receive side (pass 31) — and (pass 32) **the live gameplay loop**: the
   event-bus wiring + machinery, client entity replay/interpolation, NetworkEventSystem_C
   (connect/reconnect, 128-sample ping ring, outgoing cipher), match-flow JamMessage
   handlers, the per-frame tick/visibility/world-to-screen layer, and the full JSON text
   engine (recursive parser + number/string/SIMD-whitespace scanners) behind the
   `"--name {json}"` command pipeline. [inference: this is the game client's own runtime;
   `0x14054fea0` marks the end of data registration and the start of behaviour.]

**Layer 6 constructs (passes 28–32; per-pass detail in the records):** *infra* (28–30): handle
table `FUN_140567590` ×494; hash A/B + allocator pair; vector library `FUN_1405649b0` ×983;
per-site logger; named-service registry (`"VivoxSDK"`); hotfix verifier/HTTP; worker pool ×20;
component access `func_0x140c503d0/140c506f0`; spatial raycast/LOS; frame loop
`FUN_140551c40`; event bridge (`FUN_140583fb0`, app vtable `+0x140/+0x150`, sink
`FUN_1405ae0e0`); bitstream reader `FUN_140586bc0`; debug-UI `FUN_141c64c10…651a0`; CSV
iterator; hash family C `FUN_140599970`; HUD quad record; tracked-entity container; staged
spawn queue; presence component; Steam stats; XInput; JSON value tags (`0xc05`/`0x1c05`).
*match receive side* (31): bitstream codec reader ×341 / writer ×248 + entity
header/field/baseline/component-apply + 67-KB dispatcher `FUN_140623900`; restore walkers;
introsort; saved-match/match-phase name tables; JSON serializer `FUN_1406331b0`;
narrative-viewer schema; JamMessage dispatch `0x140638ca0`+ (default `FUN_140548d00` ×97);
event-bus subscribe `0x14063ddf0`+; telemetry HTTP #2. *live gameplay loop* (32,
`0x140644930`–`0x140676370`): event-bus machinery + mass wiring `FUN_14064d2a0`;
`ClientLobbyMessageSystem_C::__LobbyServerConnectionUp`; connection state machine + toast
router; **client entity runtime** (component decoders, 0x468-B state copy, frame replay,
state writer `FUN_140654c50`, snapshot serializer, interpolated transform `FUN_140655de0`);
scoreboard + end-of-round 0x19c-B report; **NetworkEventSystem_C** (connect/disconnect,
frame handler + 128-sample ping ring, encryptor `FUN_14065aaa0`, net-stats HUD); match-flow
handlers `0x4f4c`–`0x4f6a`; message queue; **kill-feed decoder `FUN_14065fe20`**; time sync;
**master tick `FUN_140669ee0`** (100,672-B text) + watchdog; telemetry JSON
(`FUN_14066b5d0/14066bdd0/14066cd30`, world upsert with 12-s TTL); ability bitsets + hero
HUD; **world-to-screen `FUN_14066fe20`**; FNV-1a lookup + "countries"/"system_notification"
tables; JSON text engine + `"--name {json}"` command pipeline (`FUN_140673120/673be0/
140675580/140676370`).

**The registry machine — nine constructs/variants (layer 4, closed):** name buffers (XOR-8,
24-bit len, bands in Corrections 19/23); **registration** `func_0x1421cd360(…,18 args)` — 7,956
ciphertext + 4 plaintext rows, `base = out − 0xa0`; identity mapped for 44,360 name pages in
`../../poolmap.tsv` (7,946 class + 23,898 field + 8,716 enum value + 651 enum type + 3,013
owner); **builder** (allocator → XOR-8 → `d4f30/d4f70` → `d4fb0` → `{+0x20 root, +0x28 inst,
+0x30 0, +0x98 1, +0x9c 0}`); **copy wrapper** (`c2d70`+`d4fb0`); **sorted-insert** (2×56-B
keyed at +8); **`{id,hash,alias}`** (326 rows); **nested-atexit** (261); **settings/variable
registrar** (`FUN_141c58170` + `_onexit`); plus 15 CompilerIDFilter shells. Builders/sorted/
atexit carry stack cookies; registrations, wrappers and settings functions do not.

**Where the data lives** (scattered shutdown slots in Corrections 6):

| band | content |
|---|---|
| `0x143848d40`–`0x14384ad54`, `0x143864e80`–`0x143864ed8` | XOR-8 name/payload ciphertext: runtime bootstrap, settings, logger strings, hotfix/log format strings, ~50 console-var names (3 copies), UI/event strings (key@+0, len@+8, latch-0x48). `0x14384b7b0–b7bc` on the same page are **plaintext** floats (Corrections 27) |
| `0x1438b8e50`–`0x1439a9b2c`, `0x143a16e38–2e7b` | registry name/payload ciphertext; `PTR_s_CompilerIDFilter_*`; page-allocator + hotfix names; triplet-stub object page `0x1439b0000`–`0x1439fa330` (`func_0x000141c712f0` ×3 + flag per 66-B stub) |
| `0x143a155xx`–`0x143aa36xx`, `0x143b0c…`–`0x143b77…` | XOR-40 key tables, settings names, locale/ciphertext, catch keys, `0x143a19b50–0x143a19b88` (camera/volume float block), `0x143a19938–44` (render defaults) |
| `0x143b7a428`–`0x143b7af00`, `0x143b7f410`/`0x143b7f1e0–238`, `0x143b808xx–0x143b81a0x` | passes 28–29 runtime block: per-site logger objects (`0x28` B), worker-pool state, object-id counter `0x143b91f50`, ~250 feature flags `0x143b945b8`–`0x143b9c5c0`; the single app object and its setters; per-HUD-object flags (`0x143b809cc/ce`, `0x143b80a90`, `0x143b8145c`, `0x143b8152c`) |
| `0x143cf0000`–`0x143d05000` + far `0x143f8…`–`0x143f94…` | RTTI type_info descriptors (Corrections 17) || `0x143e99d90`–`0x14413b7a0` | registration outputs / instance slots; settings descriptors to `0x14413b7a0`; config globals `0x144140740/758/144143410/1441d0150/14414fb48` |
| `0x1441e18f0`–`0x1441e67c8` | plaintext reg outputs, registry-list head `_DAT_1441e1c70`, dispatch-slot columns + readiness bitfield |
| `0x1442a1920`–`0x1442a1bd8` | plaintext struct-schema rows (`dmWorld`, `dmManifold`, `bcMtx44`, …) + field tables; record pools `0x1442e37xx–0x1442f14d2` |
| `0x144226c70/80`, `0x1441d05xx` | named-service registry (lock + node list); voice levels/mic (`_DAT_1441d05e8`, `_DAT_1441d0578`) |
| `0x144180ed0`/`0x144180f20`, `0x1441b3bb8`, `0x1441880e8`, `0x1441b8170–8198` | two 0x50-B settings-slot objects; "zero id" string; default 3-dword value; global refcounted id intern table (buckets `0x1441b8178`, counts `0x1441b8180/18c/198`, shutdown latch `0x1441b81cd`) |

**What it is for.** Layers 1–2 are a vendored NVIDIA/igzip preamble; layer 3 is compiled-in C++
static init; layer 4 registers ~8 k encrypted type names with sizes/alignment/category and builds
instances, tables and id rows from them; layers 5–6 are the client that consumes that data —
settings, telemetry, schemas, chat/voice, hotfix patching, HUD markers, the spatial/entity
runtime, the match-lifecycle receive side (pass 31), and (pass 32) the **live gameplay loop**:
entity replay/interpolation, the ciphered network connection, match flow, the per-frame
tick/visibility/world-to-screen layer, and the JSON command pipeline. No plaintext game
protocol (entity traffic is the `FUN_1406232f0`/`FUN_1406264c0` bitstream over an unframed
transport), the render device is one opaque `FUN_141ff40f0` call, and no gameplay *rules* are
in the read range — but the HUD, scoreboard, kill feed and match-state builders are.
Confidence: counts/shapes/bands measured; construct labels are shape-based inference;
obfuscated bodies read structurally only.

**Known limits.** (a) `func_0x…` bodies absent (registrar, decryptors, `0x140543xx0` family,
settings accessors, component getters, HTTP client, CSV iterator, event-bus bus/ctors
`FUN_142e02e00/142e029b0/142e03480/142e04e00`, `FUN_142d8xxxx` and the pass-32 cipher family
`FUN_142454xxx`). (b) XOR-8 keys are per-record random salts; only pool text exists (ledger 29);
`Unknown` identity from `../../poolmap.tsv`. (c) `0x142f0…`–`0x142f2b…` labelled thunks absent.
(d) Corpus gaps: pass 30's 12 × >1 KiB (48,640 B, ledger 31); passes 31–32's >1 KiB gaps are
giant-function `size=` under-reporting (pass 32: 34 gaps / 91,184 B, all bodies read). (e)
Obfuscated bodies resist decompilation; pass 32 adds `FUN_140669ee0` (100,672-B text),
`FUN_14066fe20` (48,690), `FUN_14066ec90` (48,466), `FUN_140672c80` (19,470) and six more
>17 KB ones; their text carries offcut-call stamps up to `0x1406a1703`.
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
| **Settings accessor** | XOR-8 name buffer → `FUN_141c295b0(int)` / `280b0` / `2bfd0` / `29b00` / `28b30` / `29060(min,max)` / `2ca50`; targets `_DAT_143b7a46x`, `_DAT_1438499ax`; numeric form `FUN_142d2cf30(0xe0xxxx)` | `0x140554220` |
| **Per-site logger** | TLS-guarded 0x28-B static via `func_0x141c48370(buf,&DAT_143b93fa0,0x28)`; `FUN_141c48450` gate → `FUN_141c48330(obj,&name,args…)` | `0x1405601c0` |
| **Handle table** | 0xfff buckets, entry `{u32 handle,u64 value}`; lease helper `FUN_140567590` (thread id in low 12 bits); resolve then vtable | `0x140567590` |
| **Hash maps** | A: int64 keys `((~k + k*0x40000)>>31^)…*0x15 …*0x41`; B: u32 keys `k*0x1001+0x7ed55d16 …*9+0xfd7046c5`; tombstone `-1` | `0x140564ca0` |
| **Container allocator / worker pool** | alloc `func_0x141c23490(&PTR_PTR_143a01d18,size[,align])` / free `func_0x140578190` (capacity word `sign|count`); pool `FUN_141bb7520(0x20000,FUN_140573d40,ctx,name,0x14)`, enqueue `FUN_140573f10`, stop `FUN_140573fc0` | `0x140558120` |
| **Hotfix/integrity** | 0x30-B record `{hash,idx,verified,handle,ts}` → SHA-256 memcmp; tags `"hotfix"`, `"canary"`; traps `"0x811C9DC5"`, `"0x2AEE6BD9"`, `"0xE430A66C"` | `0x14056cd40` |
| **Component access** | `func_0x140c503d0(entity,0xd8…id)` has / `func_0x140c506f0(entity,id,default)` get; ids `0xd80000000007a7b`, `…1cbb`, `…8016/8017`, `…ce5f`, `…4aa`, `…b141` | `0x14057a870` |
| **Spatial query** | 4-float ray → `FUN_14206b500`/`FUN_14206a660` → `rsqrtss`+Newton normal (`_DAT_142f81720/81730`) → `divps` | `0x140579010` |
| **Event tag / payload** | `FUN_140583fb0` pushes 0x18-B `{ptr,ptr,u32,2}`; fill with `FUN_141940c00`(bool)/`…0db0`/`…0e00`(4B)/`…1360`(8B)/`…93d210`(struct); ids `0xa4…`, `0x2400…`, `0xde0…`, `0xd8…`; send `FUN_1405ae0e0(chan,msg)` or app vtable `+0x140`/`+0x150` | `0x140584450` |
| **0x19c message** | `FUN_141c23430(buf,0x19c)` + `func_0x141b39150(buf,u64,u32)` + `FUN_14200dee0(dst,buf,0)`; `0/0xffffffff` slot pairs; consumers = pass-31 deserializer (thread 2) | `0x140594cd0` |
| **Console-var registrar** | XOR-8 name pair → `FUN_141c29b00` (int/bool) \| `FUN_141c2a030(name,name,&t,&min,&max)` (float) \| `FUN_141c2bfd0` \| `FUN_141c285e0(...,&min,&max)`; defaults 100.0f/5.0f/1/0; 3 duplicated copies under latch `DAT_143b80a9c` | `0x140596b00` |
| **HUD marker** | 0x90-B quad record (verts `+0x540..0x578`, `+0x530=5`), occlusion `FUN_142032690`, projection `FUN_14059d730`, draw `func_0x14206d250/2b0`, outline `func_0x14057acb0` | `0x14059dad0` |
| **Tracked-entity row** | 0x58/0x60/0x68-B rows: key `+0`, prio `u32 +0x38`, flags `u32 +0x50`, slot `u32 +0x58`, state `u8 +0x5c`; expiry `double +0x10/+0x18`; four percentage floats at `+0x6104` | `0x140588370` |
| **Table/debug UI** | `FUN_141c64c10` begin → `…64c30("col",0)` → `…64cd0` row → `…64df0`/`…64e30`/`…650c0`/`…65050` cells → `…651a0` end; plaintext `"BGS Result"`, `"Club ID"`, `"SYSTEM"`, `"%F %T"`, `"0x%016llX"` | `0x1405a2ba0` |
| **Hash family C** | `h=(k*0x200000+~k); (h>>0x18^h)*0x109; (h>>0xe^h)*0x15; (h>>0x1c^h)*-0x7fffffff & (cap-1)`; chained `{next,key,val}` or range layout; byte-keyed handler registries `FUN_140621990/aa0` (pass 31) | `0x140599970` |
| **Command dispatcher / JamMessage** | `(**(code**)(*disp+0x10))(disp,fn,id,0)` (and `+0x30`); ids `0x48,0x53,0x7c,0x7d,0xa5,0xb2`; ~50 `0x140638ca0`+ dispatchers map contiguous id blocks (`0x5014–0x5021, 0x5078–0x507e, 0x5140–0x515e, 53000/0xcf09–0xcf25, 0x8dcc–0x8de9, 0x5eec–0x5f0f, …`) to handlers via `func_0x000141c52420(app,&DAT_143bxxxxx)`; default `FUN_140548d00` ×97; `"Unhandled JamMessage, unable to dispatch"` | `0x1405ac510` |
| **CSV / presence (28–30)** | CSV iterator `func_0x1423887b0(&it)` open / `…388a00` step / `…388ab0(&i)` / `…388af0(&u64)` / `…3887e0` close (0x20-B `{int,u64,string}` rows); presence `{bnet_dbid,title_id,group,field,unique_id}` via `FUN_141c63bc0` (row 0x58 B, class `+0x18`=0x8e74, field `+0x28` ∈ {1,2,3,4,5,0xc,0x16,0x19}, value tag `+0x50` 1 bool/4 str/5 vec/6 nested) | `0x1405afc60` |
| **JSON value** | 0x10-B `{data, u16 tag @ +0xe}`: `3` obj, `4` arr, `9/0xa` true/false, `0x?96/0x?d6` ints (0x20=signed, 0x40=32-bit, 0x100=wide), `0xc05` heap string, `0x1c05` inline (`len = 0xd - low byte`); **writer** `FUN_1406331b0` (tags 0–5/num; double `FUN_140635480`, u64/u32 `FUN_140637450/371f0`, pair table `DAT_142f86ee0`) | `0x14060fc90` |
| **Bitstream codec / entity delta** | reader `FUN_1406232f0` (≤64-bit spans, `{words,cur,idx@+0x1c}`) / writer `FUN_1406264c0`; entity header `FUN_140622f00` (0xc-bit flags → 0x76/0xa6/0x30/0x20/0x40/0x14e-bit fields, out 0x38-B); field `FUN_140623120`; baseline/delta `FUN_1406251a0`; component apply `FUN_140625950` (byte key grp<<6\|slot → popcount field table at `rec+0x80/0x130` → registries `FUN_140621990/aa0`); dispatcher `FUN_140623900`; event-bus subscribe `0x14063ddf0`+ (0xb0 desc + 0x30 listener, arms 1/2) | `0x1406232f0` |
| **Event-bus (pass 32)** | map `FUN_14064cdd0(bus+0x48,id)` → 0xb0 descriptor (refcount `+8`, listener list `+0x60`); dispatch `FUN_14064d0d0/140` (`(*(l+0x18))(a,e)`, ret 2 → queue); registrar 3-variant: listen `mask\|2` / announce `mask\|1` / `FUN_142e04e00` pair; **event ids hash-obfuscated** (`FUN_14053bd90(hash,1,0)`) | `0x140644930` |
| **Session masked table** | `(row+0x160 + 0x3fa981c8e7192fa6) ror31 ^ 0x8784b4333a580288 → ror23 + 0x37a9e6a2eedd5214 + type*8`; type code from `func_0x0001407xxxxxx`; **per-frame handle table** `(p^0x73cc01350b9bc072)+0x704e4dbd364c5bd3 >> 0x26 \| 0x4000000`, rows `{u32 handle,…,ptr}` @ `+0x18317a531d116c0c/c14` | `0x14064efa0` |
| **Net frame + cipher (pass 32)** | incoming: 0x22-bit header, type nibble `buf+0xc` (1 = 16-bit seq + 8-bit count + events; 0xe last-handler; 0xf fixed slot), ping ring 128 `ent+0x3374`; outgoing: `FUN_140654c50` 16-bit time + 8-bit seq, `FUN_140657580` presence-bit + 32-bit length per entity, then cipher `FUN_142454a90/0f0/7010/6ce0` over 0xb80-B buffer + bit-splice (`FUN_14065aaa0`) | `0x140654c50` |
| **JSON text engine (pass 32)** | recursive parser `FUN_140673120` (errors 3–7, 0x10); number `FUN_140672500` (overflow guards, exp ±308, tables `0x142f853e0/5d80`); string `FUN_140672c80` (SIMD tables `0x142f888c0…88ef`, escape map `0x142f887c0`, `\u`+surrogates → UTF-8 `FUN_14060da00`); whitespace `FUN_140674f90` (tables `0x142f886c0…86ff`); writer side = pair append `FUN_14066b5d0` + serializer `FUN_1406331b0` | `0x140672500` |
| **Command string (pass 32)** | build `"--%s %s"` + `{json}` (`FUN_140673be0`/`140675580`, field names in pages `0x1438538e0…3a30`) → submit to service `PTR_FUN_143849970` vt+0x188; queue (12-s TTL rows, 900-unit respawn) → executor `FUN_140676370` (unpack → parse → 7-field lookup → hero-GUID check → `FUN_14062b4c0`) | `0x140673be0` |

## Open threads (cheapest next query each; check/update every pass)

1. CLOSED (2026-11-21) — **the XOR-8 key is a per-record random salt.** All 30,933 `Unknown`-streak keys distinct, entropy 7.999 bits; `strpool.txt` gives the text (ledger 29; `STRPOOL_UNKNOWN.md` §Evidence 5).
2. **0x19c-B / entity-state transport framing** — pass 32 found the client framing: `FUN_140654c50` writes `16-bit time + 8-bit seq` and `FUN_140657580` per-entity presence-bit + `32-bit length`; remaining: the socket/UDP layer that carries the finalized buffer — grep forward for the `FUN_142454xxx` cipher outputs.
3. CLOSED — `0xde000000000030e`/`0x30f` are pass 30's presence-failure events (`FUN_1405d54f0`).
4. CLOSED (2026-11-21) — **JSON writer + parser + CSV consumer**: writer `FUN_1406331b0` (pass 31); pass 32 adds the callers (`FUN_14066bdd0`, command builders) and the full parser `FUN_140673120`; CSV consumer `FUN_140637d10/140637f20` (pass 31, reused pass 32).
5. **Command ids `0x48/0x53/0x7c/0x7d/0xa5/0xb2/0x3a`** — grep later chunks for `+0x10))(…,0x`/`+0x30))(…,0x`; pass 32 adds gated-dispatch JamMessage blocks `0x4f4c–0x4f6a`, `0x64c8–0x64d4`, `0x6b6c/d`, `0xa794–0xa79a`.
6. **`FUN_141c2a030` min/max** — locals are `{0,5.0f}`/`{0,100.0f}`; find one site with a negative max.
7. **`FUN_141c295b0` / `FUN_141c58170` / `FUN_142d2cf30` bodies** — `FUN_`-named, unread corpus (~chunk `15xx`).
8. **`func_0x140543xx0` family** — absent; test `0x6c12bdf61cf839d6` against a known `.data` address.
9. **`0x143b945b8`–`0x143b9c5c0` (~250 flags)** — grep forward for `143b94`/`143b95`/`143b9c` readers.
10. **`_DAT_143b7f410` field map** — merge `FUN_140554220`/`5559c0`/`585220` for ~150 offsets.
11. **Channel list `_DAT_143c00680`** — writer found (pass 32: `FUN_140663de0`, id 0x4f66); the renderer that walks it is still unfound — grep forward.
12. **Hotfix file identity** — dump one 0x30-B record (`_DAT_1439d98c0`); `_DAT_1439d9890` = backoff table.
13. **Gaps** — pass 30's 12 × >1 KiB gaps (ledger 31), largest `0x1405ca0f1→0x1405cc1d0`; passes 31–32's >1 KiB gaps are giant-function `size=` under-reporting (bodies read); plus `0x14059a007–0x14059c350` (9,033 B) and `0x1401a4e02–0x1401abad0` (27,854 B) still open.
14. **CompilerIDFilter** — unchanged (last touched pass 21); payloads are regs.
15. **Event-bus / gameplay names — raw dump done, table still open.** `rdata_names.tsv` now holds all 16,832 `.rdata` strings (15,365 ascii / 658 cstring / 809 utf16; query `strlookup.py --pool`); it names the telemetry/protocol fields but **no** toast/event names. The 68-entry table `0x143851c90` is in `.data` and its bytes are pointer-shaped/encoded, not inline names (ledger 34); `.data` strings `PlatformEvent`/`event-store` are already in `strpool.tsv`. Next: decode `0x143851c90` or find its name pool. `FUN_140548d00` body still unread — verify no-op.
16. **Pass-32 machinery bodies** — cipher family `FUN_142454a90/1424540f0/142457010/142456ce0`; event-hash resolver `FUN_14053bd90` (one call in `FUN_140660420`); the ~20 session type-code getters `func_0x0001407xxxxxx`/`func_0x000140cxxxxxx` (bodies in ≤ chunk 285); the `0x14068xxxx` tick-helper family behind `FUN_140669ee0`.
17. **Handle-table writers** — the per-frame table keyed `+0x18317a531d116c0c/c14` has no writer in range; grep forward for the constant to learn the bucket-row layout.

CLOSED (machine): fd9670 recount; provenance; `0x1411b8070` unread corpus; thread 43 (`0x3fd91271`); JSON writer + CSV consumer (pass 31); ledgers 5, 6, 10, 11, 16, 17, 18, 20, 19 (naming); update/init, shutdown slots, alias field, `0x39091531`, zero-reuse, type_info band, pad table, decompiler artifacts.

## Next pass

Resume at **`chunk_0295.txt`** — pass 32 ends at `FUN_140676370` (hero-select command
interpreter), engine-runtime stratum `0x14054fea0` OPEN; `state.json.next_chunk = 295` agrees;
the pass **length comes from `python scripts/pass_next.py`** and this file names only the resume
chunk. Run `pass_measure.py <start> <end>`, quote stdout verbatim in the record, run `--update`,
refresh this file. Watch for: (a) the **`0x14068xxxx` tick-helper family** — `FUN_140669ee0`'s
stamps reach `0x1406a1703`, so the master tick's per-entity helpers (`func_0x0001406823f0/
685cc0/686560/680f70`) and the `FUN_14099xxxx` family should appear first; (b) the
**socket/transport layer** under the cipher `FUN_142454xxx` (threads 2/17) and the per-frame
handle-table writers (thread 18); (c) whether a `cd360` registration or `{id,hash}` record
returns after six passes without; (d) new plaintext names — `"countries"`,
`"system_notification"`, `"title"/"description"/"updated_at"` landed in pass 32; (e) the
`FUN_14071c/d/exxx` hero-ability handlers (dispatched at `0x64c8`–`0x64d4`, bodies ahead) and
the `0x14062b4c0` action family now reachable from `FUN_140676370`; (f) `SteamUserStats` /
`ISteamFriends`/`ISteamRemoteStorage` strings. Do not re-run a counted range through `--update`
(ledger 5); no ciphertext script line (ledger 7); leave the stale flags (ledgers 11/16) alone;
never treat `0x826e…`/`0xca334801` or offcut-call addresses (`0x1409bb0xx`,
`func_0x00012429xxxx`) as data (ledger 20); ledger 24/31 for gaps; `size=` is not coverage
(ledger 30).
