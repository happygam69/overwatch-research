# Systematic .text read — protocol

Goal: consume the entire decompiled `.text` of `Overwatch_clean.exe` in order, and
leave one detailed record per pass. Nothing skipped, nothing sampled.

## Source

All paths below are relative to this repo root (the chunk corpus, `index.json`,
`state.json`); the decompiler output and build tools sit two levels up. One exception:
the decoded string pool is copied in as `strpool.tsv`, so `scripts/strlookup.py` and
`scripts/strscan.py` need nothing outside this folder (ledger 29).

`../../corpus/b5120..b5167` — 119,757 Ghidra `.c` files, one per function, named by entry
address. `../../tools/flood_build.py` repacks them into `chunks/chunk_NNNN.txt`:
function-aligned, ~128 KiB raw each, ordered by entry address.
**The byte-identical one-line `/* WARNING: Removing unreachable block … */` comments
were stripped from the chunk bodies on 2026-11-21** (`../../tools/flood_strip.py`; 668,998
lines / 42.1 MB; per-chunk `raw_bytes`/`dropped_lines` in `index.json`; pre-strip index
kept as `index.pre_strip.json`). Chunk names, boundaries and every code line are
unchanged — no read-state was affected.

    files 119757  chunks 2228  raw bytes 325787798  post-strip bytes 283641800

`index.json` → per chunk: byte count, first/last `// <addr>_FUN_<addr>`.
That index is the source of truth for coverage; never count by eye.
`state.json` → machine ledger: `next_chunk`, per-pass entries, cumulative
totals, all registration hashes, all `{id,hash}` rows. Never hand-accumulate numbers.
`scripts/pass_next.py` → range picker: start chunk (or `state.json.next_chunk`) + `--max` KiB
cap (default 1200) → printed chunk range, `.text` range, `pass_measure.py` command, record
path. Read-only.
`scripts/gap_report.py` → gap classifier, same chunk range in: every inter-entry gap as
padding (≤16 B) / `size=` (≤1 KiB) / **giant** tail / **offcut** body / **hole**, with byte
totals, so a record quotes it instead of classifying gaps by hand. `--offcuts` sweeps all
chunks for mentions inside each >1 KiB gap and diffs them against every decompiled entry, so
a reference from an unread chunk reclassifies a range-only "hole" as an offcut body. Read-only.
`scripts/pass_measure.py` → the canonical measurement; its block carries the `largest:` /
`corpus max:` lines (declared `(NNNN B)` text size) against `state.json.max_text`, and
`--maxscan` ranks the whole corpus and seeds that field, so "is this the corpus maximum" is
quoted, never hand-grepped (ledgers 37/38/47).
`scripts/crossref.py <symbol>` → corpus-wide cross-reference: the defining entry, every
function that mentions the symbol with its chunk and hit count, and the compact chunk list;
a short bare hex run (`143b94`) matches as a prefix, so a band is one query. This is the
"grep forward for X" open-thread query (threads 2, 9, 11, 17). Read-only.

(Not to be confused with `../flood.py` — the byte-budget corpus streamer with
`../flood_cursor.txt`, a separate mechanism.)

## Pass

One pass = the chunk range printed by `python scripts/pass_next.py` (fills chunks up to a
`--max` KiB cap, default 1200; post-strip chunks run 9–580 KB, so the count varies). Trust
the script, not a remembered chunk count. You have a
1 million-token context in total for the whole session.

0. **Before the pass**, read `CODE_MAP.md` in full, plus the most recent record in
   `ranges/`. Update both after the pass.
1. Read every chunk in the printed range completely (or stop at a stated boundary and say so).
2. Run `python scripts/pass_measure.py <first> <last>` from this repo root and read its output
   alongside the chunks — it is the index to what was read (headline numbers, class and
   zone skeleton, registration/decrypt censuses, record-hash matches, the range's largest
   bodies against the corpus maximum), never a substitute for reading. For the record's gap
   caveat run `python scripts/gap_report.py <first> <last>`; add `--offcuts` when a gap could
   be an offcut body rather than a hole (it sees chunks outside the range). For the pass's
   decoded XOR-8 UI names run `python scripts/strscan.py --x8 <first> <last>`.
   A `corpus max: NEW …` line is a claim, not a result: run `scripts/crossref.py <addr>`
   first, to rule out an overlapping decompilation window (ledger 47).
3. Write one record: `ranges/<first>-<last>.md`, named by the `.text` addresses covered
   (from the script's `range:` line or `index.json`). **Quote the script output verbatim**
   in the record's headline-numbers section; do not retype its numbers.
4. Run `python scripts/pass_measure.py <first> <last> --update` to merge the pass into
   `state.json`, then update `CODE_MAP.md`: coverage row, corrections/synthesis only if
   something structural changed, open threads, "Next pass" section — in that section name
   only the resume chunk; the length comes from `pass_next.py`. Cumulative
   numbers in `CODE_MAP.md` come from `state.json` totals — never hand-added.

A pass may read ahead of the census (the script's classes are call-shape heuristics;
novel constructs will land in `other`): anything the script cannot classify must be read
raw and, if it is a new construct, given an address boundary in `CODE_MAP.md`.

## Recording rules

- Every claimed fact is either **evidence** (visible in the text / measured) or
  **inference** (shape-based guess). Label inferences inline; never build a later
  pass on an unlabelled inference.
- Zone boundaries get an address. If a zone starts at `0x1400ff620`, say so.
- Numbers must be reproducible: either quoted from `scripts/pass_measure.py` output or
  from `index.json`/`state.json`. Records may cite only scripts that exist in the repo,
  and must quote their output rather than paraphrase. No hand-computed cumulative
  arithmetic — that is what produced the earlier 931,009/116,193-class slips.
- Unresolved things are recorded as open threads with the cheapest next query,
  not omitted.

## The most important thing

It's all done to understand the underlying logic and what it does. When others read your
findings they should have a clear view of what the given range contains and what it's for.

## Context budget

Do **not** guess how much context is used — the guess is wrong, usually badly. The number
is reported externally (harness usage counter); ask for it or be told. Planning a pass on
a guessed figure is how a pass gets cut in half.

Fixed overhead per pass: `CODE_MAP.md` (≤300 lines, ~6K tokens) + one record (~5K) +
the pass's chunks (the printed range, up to the `--max` cap) + room to write the new record. When the ceiling is
reached mid-pass: stop at a chunk boundary, write the read-state table (which chunks
read, which pending), and stop. Never burn the remaining budget on a partial chunk that
leaves no room to write the record.

## Cumulative index

`CODE_MAP.md` (this directory) is the single cumulative index; it is kept to a hard
≤300-line budget: coverage, corrections ledger, synthesis, one-line conventions, open
threads, next-pass instructions. Per-pass narrative, highlights and method notes live
only in `ranges/`. `state.json` is the machine ledger behind every cumulative number.
The long-form map through pass 15 is preserved in `CODE_MAP_ARCHIVE.md`.

Corpus: 325,787,798 raw index bytes → 283,641,800 post-strip; `.text` 42,864,695 B;
119,757 functions; 2,228 chunks (`index.json`).
