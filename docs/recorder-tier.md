# The killcam/highlight recorder tier

**Bottom line.** At the start of the `0x140b47` band (pass 64,
[`0x140b47d80-0x140b7aa80.md`](../ranges/0x140b47d80-0x140b7aa80.md), chunk 0580) the
sweep read the complete client-side lifecycle of the killcam/highlight video
recorder: three functions that create, poll, and finalize a recording, plus the
strings, the job wrapper, the playlist arms, and the playback hook that tie them into
the rest of the client. The recorder object itself, the encoder, and the media output
remain `func_0x…` bodies — what closed at pass 64 is the *control* tier: every call the
UI and the party state machine make into it is now mapped.

The evidence is all in the pass-64 record
([`0x140b47d80-0x140b7aa80.md`](../ranges/0x140b47d80-0x140b7aa80.md)); the strings
were decoded at pass 63 and the share-code machinery was built at pass 52.

## The lifecycle

**Create — `FUN_140b4a190`** (`0x140b4a190`, size 2810, 26 callees). Gated by the
session-type chain (`FUN_1409a9d50(param_1, param_2[0x20], 0)` + `FUN_1407cf0d0` name
resolve), it reads the video configuration from the render service (capture width at
`+0x198`, clamped to 4320; a scale/aspect factor at `+0x19c`; frame rate at `+0x1a0`;
quality at `+0x1a4`), scales the height and clamps it to 7680, then creates the
recorder through the factory `FUN_141b25490(_DAT_14413bfa4, 0)` and stores it at
`param_1+0x1c0`. The vtable calls are: `+0x88` init(w, h, w*fps, h*fps), `+0x90`
set-metadata, `+0x98` begin, `+0xa0` set-output(path, fps), `+0xa8` stop(reason),
`+0xb0` set-quality, `+0x108` get-id.

Every failure arm posts `FUN_1407ce8d0(svc, {tag 0x206, u64 detail, char text[0x100]})`
— the pass-52 `FUN_1409ea7d0` toast shape — and sets the party-machine state to `0xc`:

| detail | string (XOR-8 page) |
|---|---|
| 1 | 'Failed to create recorder.' (0x14386a670 / 0x698 / 0x6c0) |
| 3 | 'Failed to build metadata.' (0x14386a6e8) |
| 4 | 'Failed to create encoder.' (0x14386a710) |

The metadata arm is the interesting one: it calls
`FUN_1409e9300(_DAT_144159380)` and `FUN_1409e9430(&meta, buf)` — the **same keyed
SHA-256 / share-code serializer the highlight-share tier built at pass 52**. The
recorder tier is the fourth consumer of that machinery; the payload is the
highlight/session id set (ids from `FUN_1409a0e90(param_1+0x1e8)` plus a sub-object at
`+0x3a`, the quality byte, and two flag bits). On success the encoder gets the buffer
(vt+0x90), the output path (vt+0xa0), and begins (`FUN_1409a3b40`, vt+0x98), with
`param_1+0x201` set as the recording flag.

**Auto-stop.** While recording, elapsed time (`(now − +0x1e0) * _DAT_142f7aadc`) is
compared against a max duration read from the DOM (`FUN_14098dd30(param_1,
param_2[0x1e])`). When it expires, the client builds the **highlight playback viewer**:
`FUN_1406b77e0(_DAT_143b7f410)` creates a 0x30-B viewer (`+0x30 = 60.0/fps` playback
speed, `+0x34` the share id, `FUN_1407dddd0(viewer, recorder)` binds the recorder), and
mints a row-model node with the GUID `0xa88000000000544` (`FUN_1421e1040`). The
recorder is stopped with reason 6 and the party state goes to 5.

**Poll — `FUN_140b49bd0`** (`0x140b49bd0`, size 1427). Called on the tick: it walks
the 0x38-B pending-awaitable array at `+0x1c8` (count `+0x1d0`, live slot `+0x30`),
asks the gate service `+0x498` per row, computes progress as `(done/total) * 100` plus
the current recording length, and writes it as a float property. If the recorder has
reached state 3 it runs the same finalize job as below; on all-rows-done it stops the
recorder, sets state 4, and snapshots a frame counter.

**Finalize — `FUN_140b49430`** (`0x140b49430`, size 925). Reads the recorder's state
byte at `+0x44`. State 3 wraps the recorder in a **0x150-B refcounted job**
(`func_0x000141b1ab00(0x150)`, vtable `PTR_FUN_142f840f8`, dual `+4/+0xc` refcounts,
`FUN_140976f90(job+0x10, recorder)`) and runs `FUN_140573f10(&job)`; on failure it
posts event `{0x206, 0, 5}` with 'Finalize job failed.'. States above 3 map to event
codes (4→2, 5→6, else 0) with 'Encoding failed.' and state 0xc. The recorder is then
released with `FUN_141b251d0()`.

## Where it plugs in

* The 15-state party member machine `FUN_140b45640` (pass 63, chunk 0579) names
  `FUN_140b49bd0` and `FUN_140b4a190` as its case-3/4 callees — recording is a party
  state, not a standalone screen.
* The playlist arms sit around the trio: `FUN_140b47e30` teardown, `FUN_140b498c0`
  enter, `FUN_140b4ace0` refresh (0x158-B playlist rows via `FUN_1406626f0/1406624a0`),
  and the clip-info reader `FUN_140b484d0` (`FUN_142c8aa20(out+0x38, row+0x48)` over the
  six-field clip block) — the metadata the summary screen renders.
* The playback viewer GUID `0xa88000000000544` is the same `0xa88000000000xxx` family
  the screen tier has used for row-model nodes since pass 43.
* The error strings live on the XOR-8 belt at `0x14386a5a0–0x14386a738`
  ('Finalize job failed.' ×2, 'Encoding failed.' ×2, 'Failed to create recorder.' ×3,
  'Failed to build metadata.', 'Failed to create encoder.'), decoded in place with the
  standard key-page-at−8 scheme.
* A second hotfix batch walker, `FUN_140b487a0` (same chunk, 22,143 B text), sits in
  the same state flow: it walks 0x78-B hotfix descriptor rows with three id-array pairs
  (`|0x250000000000000` guids) and one `|0x350000000000000` tag, and applies them through
  `FUN_1407a9c00` / `FUN_14081c9c0` — the session-scoped sibling of pass 63's
  `FUN_140b387a0`.

## What is still open

The encoder itself — the body behind the `+0x88/+0x90/+0x98/+0xa0/+0xa8/+0xb0` vtable
arms and the `FUN_140573f10` finalize-job implementation — has no decompiled body in
the corpus (`func_0x…` class, `0x142f84xxx` device band). The recorded-file format, the
muxer, and the 'Finalize job' worker are therefore conclusions-in-waiting; the control
flow that drives them is complete. Pass 64's record carries this as **T64-1**
(`crossref.py 142f840f8` is the cheapest next query).
