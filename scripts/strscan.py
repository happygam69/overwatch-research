#!/usr/bin/env python3
"""Resolve every data address mentioned in a chunk through the shipped pool.

usage: python scripts/strscan.py chunks/chunk_0267.txt [window] [--all]
       python scripts/strscan.py --x8 295 306       # per-pass XOR-8 page name list

Prints one line per distinct address that has a pool page nearby, so `DAT_`/`uRam_`
name pages become readable while reading a chunk. Stripped pages carry their recovered
identity (class / field / enum value / owner) — see `../strlookup.py` for the row shape.

`--x8 FIRST LAST` (chunk numbers, the range `pass_next.py` prints) is the pass-level mode:
the dense UI-name bands — e.g. `0x143853c10`-`0x143855944` — are many small XOR-8 pages
(`(&DAT_<base+0xc>)[i] ^= key[i & 7]`), and nearest-address lookup in a band that dense
attributes a page to its neighbour's text. The mode instead reads the page base out of
each decrypt loop and resolves `base + 8`, the record header `strpool.tsv` is keyed by
(the pool already carries `poolmap.tsv`'s kind/hash/name columns), so one line per page is
exact. Pages whose text is not printable have no row and print `(no pool row)`.

One chunk past `last` is scanned when it exists: a band is shared across chunks, so a page
the last chunk's functions reference can first decode in the next chunk's loop. Those rows
keep their own `chunk_` number and the header says `+ look-ahead`.

The trailing summary says why the rest did not resolve. Most addresses in a chunk are
never strings: `.text` mentions are code, and `.data BSS` is the section's virtual tail
(virtual size 0xCC43BC against 0x333600 file-backed bytes) holding zero-initialised
runtime globals, so no file bytes exist to decode. `--all` lists those too.

Across all 2,228 chunks: 213,042 of 227,104 file-backed `.data` mentions resolve (93.8%);
`.rdata` is only 1.7% because vtables and float tables dominate it, not name pages.

Read-only, standard library only, no paths outside this repository.
"""
import bisect
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from strlookup import load, region, show  # noqa: E402

RX = re.compile(r"(?<![0-9a-fA-F])(14[0-9a-fA-F]{7})(?![0-9a-fA-F])")
# XOR-8 page key base in the inlined decrypt loop: `... & 7) + 0x143853c10)`.
X8 = re.compile(r"& 7\) \+ (0x[0-9a-f]{7,9})")
HDR = re.compile(r"(?m)^// ([0-9a-f]{16})_")


def page_base(arg):
    """VA of an XOR-8 page from its literal, or None if it cannot be one."""
    v = int(arg, 16)
    if v < 0x140000000:
        v += 0x140000000     # 32-bit immediate in the decompiled text: 0x3855eb8 -> 0x143855eb8
    return v if v & 7 == 0 and region(v) in (".data", ".rdata") else None


def x8_report(lo, hi):
    """One line per XOR-8 page referenced in chunks lo..hi (+1 look-ahead); first sighting wins."""
    rows = {r[0]: r[1:] for r in load()}
    chunks = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chunks")
    stop = hi + 1 if os.path.exists(os.path.join(chunks, "chunk_%04d.txt" % (hi + 1))) else hi
    seen = {}
    for n in range(lo, stop + 1):
        with open(os.path.join(chunks, "chunk_%04d.txt" % n), encoding="utf-8",
                  errors="replace") as fh:
            body = fh.read()
        heads = [(m.start(), int(m.group(1), 16)) for m in HDR.finditer(body)]
        pos = [h[0] for h in heads]
        for m in X8.finditer(body):
            base = page_base(m.group(1))
            if base is None:
                continue
            i = bisect.bisect_right(pos, m.start()) - 1
            seen.setdefault(base, (n, heads[i][1] if i >= 0 else 0))

    named = sum(1 for base in seen if base + 8 in rows)
    print("== XOR-8 pages, chunks %04d-%04d%s =="
          % (lo, hi, " + look-ahead" if stop > hi else ""))
    for base in sorted(seen):
        n, func = seen[base]
        row = rows.get(base + 8)
        print("0x%X  %-48s  chunk_%04d  FUN_%x"
              % (base, show(*row) if row else "(no pool row)", n, func))
    print("%d pages, %d named, %d without a pool row"
          % (len(seen), named, len(seen) - named), file=sys.stderr)
    return 0


def main(path, window=0x60, show_all=False):
    rows = load()
    keys = [r[0] for r in rows]
    with open(path, encoding="utf-8", errors="replace") as fh:
        body = fh.read()
    seen = {int(m.group(1), 16) for m in RX.finditer(body)}

    tally = collections.Counter()
    resolved = collections.Counter()
    for addr in sorted(seen):
        reg = region(addr)
        tally[reg] += 1
        i = bisect.bisect_right(keys, addr) - 1
        hit = None
        if 0 <= i < len(rows) and addr - keys[i] <= window:
            hit = (rows[i], addr - keys[i])
        elif 0 <= i + 1 < len(rows) and keys[i + 1] - addr <= window:
            hit = (rows[i + 1], keys[i + 1] - addr)
        if hit:
            r, delta = hit
            resolved[reg] += 1
            sign = "+" if delta >= 0 else "-"
            print("0x%X (%s0x%X) %s" % (addr, sign, abs(delta), show(*r[1:])))
        elif show_all:
            print("0x%X %s" % (addr, "-- no pool page (%s)" % reg))

    n = len(seen)
    print("%d of %d addresses resolved" % (sum(resolved.values()), n), file=sys.stderr)
    for reg, cnt in tally.most_common():
        if not resolved[reg]:
            print("  %-10s %6d  no pool page" % (reg, cnt), file=sys.stderr)
        else:
            print("  %-10s %6d  %6d resolved (%.1f%%)"
                  % (reg, cnt, resolved[reg], 100.0 * resolved[reg] / cnt), file=sys.stderr)
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--x8":
        rest = sys.argv[2:]
        if not rest or not rest[0].isdigit():
            print(__doc__)
            raise SystemExit(2)
        lo = int(rest[0])
        raise SystemExit(x8_report(lo, int(rest[1]) if len(rest) > 1 else lo))
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)
    args = sys.argv[1:]
    every = "--all" in args
    args = [a for a in args if a != "--all"]
    raise SystemExit(main(args[0], int(args[1], 0) if len(args) > 1 else 0x60, every))
