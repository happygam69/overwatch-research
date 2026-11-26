# The entity-view runtime (passes 72–74)

This page closes the **entity-view tier**, the band `0x140c7e540`–`0x140cc20c0`
(chunks 0640–0667). It is the layer that turns the server's entity bitstream into the
client's live per-entity view: what the camera shows, where health bars sit, which
modifier (speed boost, slow, damage amp) is active on which entity, and the
quantized-pose state that keeps all of that in sync between server and client.

Three records carry the evidence, in read order:

1. `ranges/0x140c52970-0x140c6fc20.md` (pass 71) — the front: window/slot objects.
2. `ranges/0x140c70370-0x140c7e540.md` (pass 72) — the **packer**: a 0x1440-B object
   that reads the DOM (the game's UI data tree) and emits 0x124-B view records.
3. `ranges/0x140c7f1e0-0x140ca03c0.md` (pass 73) — the **service belt**: foreign-key
   lookups, quaternion tooling, the CRC-32 integrity layer.
4. `ranges/0x140ca1f80-0x140cc20c0.md` (pass 74) — the **live runtime** itself.

## The object

The runtime's owner is a **0x1b70-byte view object** (`FUN_140ca37d0`, chunk 0660),
one per viewed entity. Its layout is now almost fully mapped (see the pass-74 record's
offset table). The important parts:

- a **0x124-byte current view record** at `+0x21a`, guarded by a flags word whose bits
  select which fields are present;
- four **keyed row arrays** — 0x30-B keys at `+0xd2`, 0x38-B modifier rows at `+0x10e`,
  0x40-B vector-modifier rows at `+0x12c`, and 0x188-B rig/attachment rows at `+0x14e`;
- two **pose rings**: a 0x10-B `{time, tick}` ring at `+0x400` and a 0x470-B pose
  snapshot ring at `+0x420` (the pass-72 "frame-quantised draw" reads these back);
- a **0x50-byte cached camera basis** at `+0x1ae0` with a compare-and-skip block;
- observer sets that the update master fans out through (see below).

## How a frame flows

1. **Decode.** The bitstream readers (`FUN_140cab000` and siblings, chunk 0662) read
   each field through small width-ladder tables at `0x143872ac0`–`0x143872ce0` —
   2- or 3-entry arrays of bit widths, one per field class. `FUN_140ca28c0` applies
   fifteen flag bits of the record's header to pick fields; the write-side twins
   (`FUN_140cadd80`, `FUN_140cade80`) emit the same bits, so the record schema is
   bit-exact in both directions.
2. **Apply modifiers.** `FUN_140cbcbe0` (chunk 0666, 10.3 K real body) unrolls
   **13 modifier slots × 6 ops** (add, multiply, set, min, max, clamp-to-range) over the
   object's camera and hull fields. This is the same op enum the scalar resolver
   `FUN_140cb3990` and vector resolver `FUN_140cb3b10` use on their row arrays, and it
   answers a pass-70 question: the `0x11`–`0x26` modifier ids of the HUD tier are
   applied by these inline ladders, not by a name table.
3. **Interpolate.** The pose rings hold keyframes; `FUN_140cab5f0` inserts them,
   `FUN_140cab870`/`FUN_140cabbb0`/`FUN_140cabd40` find the bracketing pair by time,
   and the pass-73 interpolator `FUN_140ca03c0` blends the two 0x124-B records.
4. **Update the world list.** The 8-phase master `FUN_140cbb260` (chunk 0665) sweeps
   the world (`FUN_140de3940`, `FUN_140ce96b0`), broadcasts each entity through
   `FUN_140cb11d0` into the pass-72 packer's 0x20-row list, then fans the observers
   out through their vtables (slots `+0x38` through `+0x68`).
5. **Resolve the camera.** `FUN_140cb86c0` (chunk 0665, 6.6 K real body) runs a
   5-sample orbit/shoulder search with collision queries (`FUN_1420328c0`), caching
   the winning basis in the `+0x1ae0` block. `FUN_140cc0700` clamps FOV;
   `FUN_140cc0dc0` is a spring-damper zoom.

## Integrity

Both sides of the entity fingerprint are now read: the pass-73 belt folds a 1024-B
table at `0x14310fa40`, and this pass reads the write side folding a 256-entry table
at `0x143110360` over the same quantized position dwords (`FUN_140cacd60`,
`FUN_140cace90`, `FUN_140cad060`). The subject is the 0x124-B record's position block —
the net-view fingerprint the client checks against the server's.

## What is still open

- the far-window helper band `0x140cc2…`–`0x140cf4…` that this tier's window hosts
  point into (the next passes' front);
- the 0x84-stride sub-object family (`FUN_140cb0640`);
- whether the two checksum tables are one polynomial in two sizes;
- the render-material band `0x142cb…` this tier consumes but whose bodies live far
  away (`FUN_142cbd1b0` and siblings).

The vtable band for this object family extends `0x14310ef40`–`0x143110858` (the
`0x1431107e0..0x14311080c` block is the sixth Newton/rsqrt constant row catalogued),
with `0x143110810` as the shared zero-handle sentinel.
