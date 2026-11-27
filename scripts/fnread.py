#!/usr/bin/env python3
"""Show one decompiled corpus body by entry address. stdlib only.

usage (from work/flood/):
    python scripts/fnread.py 0x14064f2d0            # header + first 80 lines
    python scripts/fnread.py 14064f2d0 -n 400       # more lines
    python scripts/fnread.py 0x14064f2d0 --addr      # header + address stamps only
    python scripts/fnread.py 0x14064f2d0 --stats     # header + line/byte counts

Bodies come from the committed `chunks/` corpus (located through `index.json`), so this
reads nothing outside the repository. A missing body means Ghidra produced no entry at
that address (or the address is not an entry).
Read-only, standard library only.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
INDEX = os.path.join(ROOT, "index.json")
HDR = re.compile(r"(?m)^// 0*([0-9a-f]{9,16})_")


def heads(text):
    return [(m.start(), int(m.group(1), 16)) for m in HDR.finditer(text)]


def bodies(addr):
    """[(path, header_line, body_text)] for an entry address across the chunk corpus."""
    out = []
    idx = json.load(open(INDEX, encoding="utf-8"))
    for c in idx["chunks"]:
        lo, hi = HDR.match(c["first"]), HDR.match(c["last"])
        if not lo or not hi or not (int(lo.group(1), 16) <= addr <= int(hi.group(1), 16)):
            continue
        path = os.path.join(ROOT, c["path"])
        text = open(path, encoding="utf-8", errors="replace").read()
        hs = heads(text)
        for j, (p, ad) in enumerate(hs):
            if ad == addr:
                end = hs[j + 1][0] if j + 1 < len(hs) else len(text)
                line, _, rest = text[p:end].partition("\n")
                out.append((path, line, rest))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("addr")
    ap.add_argument("-n", "--lines", type=int, default=80)
    ap.add_argument("--stamps", action="store_true")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args(argv)
    addr = int(re.sub(r"(?i)^0x", "", a.addr), 16)
    hits = bodies(addr)
    if not hits:
        print("no corpus body for %s" % a.addr, file=sys.stderr)
        return 1
    if len(hits) > 1:
        print("ambiguous: %s" % ", ".join(os.path.relpath(h[0], ROOT) for h in hits), file=sys.stderr)
        return 1
    path, header, body = hits[0]
    lines = body.splitlines()
    print(header)
    print("-- %s  %d lines  %d bytes" % (os.path.basename(path), len(lines), len(body)))
    if a.stats:
        return 0
    if a.stamps:
        pat = re.compile(r"(?i)0x14[0-9a-f]{7}")
        for ln in lines:
            if pat.search(ln):
                print(ln.rstrip())
        return 0
    for ln in lines[:a.lines]:
        print(ln.rstrip())
    if len(lines) > a.lines:
        print("... %d more lines (use -n)" % (len(lines) - a.lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
