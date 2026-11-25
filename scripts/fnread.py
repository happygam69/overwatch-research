#!/usr/bin/env python3
"""Show one decompiled corpus body by entry address. stdlib only.

usage (from work/flood/):
    python scripts/fnread.py 0x14064f2d0            # header + first 80 lines
    python scripts/fnread.py 14064f2d0 -n 400       # more lines
    python scripts/fnread.py 0x14064f2d0 --addr      # header + address stamps only
    python scripts/fnread.py 0x14064f2d0 --stats     # header + line/byte counts

The corpus is `../../corpus/b<NNNN>/0000000<addr>_<name>.c`; a missing file means
Ghidra produced no body for that entry (or the address is not an entry).
Read-only, standard library only.
"""
import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "..", "..", "corpus")


def find(addr):
    a = re.sub(r"(?i)^0x", "", addr).lower().lstrip("0") or "0"
    return sorted(glob.glob(os.path.join(CORPUS, "b*", "*_FUN_%s.c" % a)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("addr")
    ap.add_argument("-n", "--lines", type=int, default=80)
    ap.add_argument("--stamps", action="store_true")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args(argv)
    hits = find(a.addr)
    if not hits:
        print("no corpus body for %s" % a.addr, file=sys.stderr)
        return 1
    if len(hits) > 1:
        print("ambiguous: %s" % ", ".join(hits), file=sys.stderr)
        return 1
    path = hits[0]
    text = open(path, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    print(lines[0])
    print("-- %s  %d lines  %d bytes" % (os.path.basename(path), len(lines), len(text)))
    if a.stats:
        return 0
    body = lines[1:]
    if a.stamps:
        pat = re.compile(r"(?i)0x14[0-9a-f]{7}")
        for ln in body:
            if pat.search(ln):
                print(ln.rstrip())
        return 0
    for ln in body[:a.lines]:
        print(ln.rstrip())
    if len(body) > a.lines:
        print("-- ... %d more lines (-n %d)" % (len(body) - a.lines, len(body)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
