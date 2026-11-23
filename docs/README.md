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

## Evidence and confidence

- **Evidence** means visible in the decompiled text or measured by a repo script.
- **Inference** means a shape-based reading of the evidence. Inferences are labelled and
  should not be used as premises without checking the cited record.
- The per-pass records are the evidence base. Every page links the records that support
  its statements. `CODE_MAP.md` is the cumulative index; `state.json` is the machine
  ledger behind every cumulative number. The corrections ledger in `CODE_MAP.md`
  supersedes prose in older records when they disagree.
- Pass records quote `scripts/pass_measure.py` output or its `--json` digest. Do not
  re-type those blocks. If a number is needed, quote the record or `state.json`.

## Scope of this snapshot

These pages were generated after pass 43, which ends at `0x140874660` in chunk `0402`
(chunks `0000`–`0402` inclusive — 403 chunk indices, `0000`–`013` of them read as
passes 1–2 pre-protocol — 23,415 functions, 6,486,312 B of declared `size=`, or 15.13 % of
`.text`). The engine-runtime stratum is still open; the registry machine is closed.

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
