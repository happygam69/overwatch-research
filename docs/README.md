# Findings

This folder is the reader-facing account of what the Overwatch `.text` sweep has found.
It exists because the working files are not written for newcomers: `CODE_MAP.md` is a
300-line index and the pass records under `ranges/` are dense evidence logs, both built to
carry read state from one pass to the next.

These pages are different. They are plain prose, they state conclusions first, they give
the addresses where the conclusion is visible, and they point into the records for the
evidence. They have no line budget because they are not part of the pass loop.

## Read this way

1. [`registry-machine.md`](registry-machine.md) — the startup type/object registry
   (`0x1400fbcb0`–`0x14054ea50`), the first half of the client that was read.
2. [`engine-runtime.md`](engine-runtime.md) — the engine and runtime below the UI
   (`0x14054fea0` onward): app composition, services, containers, match receive, gameplay,
   replay, store, live-ops, and the common idioms that tie them together.
3. [`ui-windows.md`](ui-windows.md) — the UI window engine, the typed row model, the
   screen builder belt, the settings/menu/BattlePass/social screens.
4. [`hero-tier.md`](hero-tier.md) — the hero entity, abilities, stats, hero records,
   hero-select, and team assembly.
5. [`provider-belt.md`](provider-belt.md) — the HUD/UI data-provider belt
   (`0x140ac1e70`–`0x140b478f0`, passes 60–63): the ~560-provider binding layer, its
   services and emit masters, the refresh cascade, and the overhead-UI row engine.
6. [`recorder-tier.md`](recorder-tier.md) — the killcam/highlight video recorder
   control tier (`0x140b47d80`+, pass 64): create/poll/finalize, the job wrapper, the
   playlist arms, and the playback hook; the encoder device band is the open tail.
7. [`auth-tier.md`](auth-tier.md) — the Battle.net authentication tower
   (`0x140bc86f0`–`0x140bda720`, pass 67): one 0x768-byte object with a **33-state**
   machine, the per-state timeout table, the web session (headers, cookie, JSON DOM,
   nine parsers), the 8-request HTTP cap, and the LogonComplete error ladder; plus the
   client view/render belt that sits in front of it.
8. [`entity-view-runtime.md`](entity-view-runtime.md) — the entity-view tier
   (`0x140c7e540`–`0x140cc20c0`, passes 72–74): the 0x1b70-byte per-entity view
   object, the bit-exact 0x124-B record schema with its width ladders, the 13-slot ×
   6-op modifier machine, the pose rings and interpolator, and the two-sided entity
   fingerprint checksum.

## Evidence and confidence

- **Evidence** means visible in the decompiled text or measured by a repo script.
- **Inference** means a shape-based reading of the evidence. Inferences are labelled and
  should not be used as premises without checking the cited record.
- The per-pass records are the evidence base. Every page links the records that support
  its statements. `CODE_MAP.md` is the cumulative index; `state.json` is the machine
  ledger behind every cumulative number. The corrections ledger in `SYNTHESIS.md`
  supersedes prose in older records when they disagree (same milestone-only contract as
  these pages).
- Pass records quote `scripts/pass_measure.py` output or its `--json` digest. Do not
  re-type those blocks. If a number is needed, quote the record or `state.json`.

## Scope of this snapshot

These pages were generated after pass 43, which ends at `0x140874660` in chunk `0402`
(chunks `0000`–`0402` inclusive — 403 chunk indices, `0000`–`013` of them read as
passes 1–2 pre-protocol — 23,415 functions, 6,486,312 B of declared `size=`, or 15.13 % of
`.text`); [`provider-belt.md`](provider-belt.md) was added at pass 63, which ends at
`0x140b478f0` in chunk `0579` (30,327 functions, 25.32 %); [`recorder-tier.md`](recorder-tier.md)
was added at pass 64, which ends at `0x140b7aa80` in chunk `0587` (31,024 functions,
25.91 %). [`entity-view-runtime.md`](entity-view-runtime.md) was added at pass 74, which
ends at `0x140cc20c0` in chunk `0667` (33,838 functions, 28.25 %). The engine-runtime
stratum is still open; the registry machine is closed.

## When these pages are updated

This is not a per-pass file. It is updated at **milestone passes**:

- when a named subsystem closes (for example, the registry machine at pass 27);
- when a named tier ends (for example, the UI-window engine at pass 38, or the
  settings/menu/social tier at pass 43);
- or when the user asks for a findings update.

At a milestone, fold the new conclusions into the relevant page, add a new page when a
subsystem has no home, and leave the pass narrative in `ranges/`. Do not copy measure
blocks, and do not recompute totals by hand. `PROTOCOL.md` carries the same rule.

Pages may be long. That is deliberate: this is the place where a reader can learn the
system without reconstructing it from abbreviation-heavy records.
