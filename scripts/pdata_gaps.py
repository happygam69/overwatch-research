#!/usr/bin/env python3
"""Is a >1 KiB inter-entry gap missing code, or a Ghidra entry artifact? stdlib only.

usage (from work/flood/):
  python scripts/pdata_gaps.py 0x14083d280 0x14083f2c0     # one explicit gap pair
  python scripts/pdata_gaps.py --range 0x140800000 0x140900000

`gap_report.py` classifies a gap from the corpus text alone (padding / size= /
giant / offcut / hole). A "hole" only means *no decompiled entry* -- it does not
mean no code. This script reads the shipped image: it decodes the gap bytes and
matches them against `.pdata` (the PE unwind table, one RUNTIME_FUNCTION per real
function/fragment), then prints one verdict per >1 KiB gap:

  inside pdata span FUN_x   gap is the body tail of a function we already have
                            (its decompiled text stopped at a `ret`/jump table)
  N pdata records           unwind records start in the gap: funclets/cold code,
                            usually still inside the same function body
  no pdata                  leaf code without unwind: stubs/thunks or asm
  stub table                >=8 `ret` in 512 B + int3 padding: generated thunks

So "hole" totals are re-checked against the binary instead of assumed. Read-only,
standard library only; bytes come from `scripts/img.py` -- the image when it is
reachable (`OW_IMAGE`), else the committed `image/` slices (`.pdata` ships whole, so
the pdata verdicts always run; the byte-composition columns need gap bytes in the store).
"""
import argparse
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CHUNKS = os.path.join(HERE, "..", "chunks")
HDR = re.compile(r"^// ([0-9a-f]{9,16}) \S+ size=(0x[0-9a-f]+|\d+)", re.M)


def pdata_table():
    """[(start, end)] from the .pdata RUNTIME_FUNCTION rows."""
    pva, _vsz, psz, _raw = img.section(".pdata")
    blob = img.read(pva, psz)
    if blob is None:
        raise SystemExit("no .pdata bytes -- run `python scripts/img.py export --pdata` "
                         "where the image is, or set OW_IMAGE")
    base = img.pe()["base"]
    return [(base + b, base + e) for b, e, _u in struct.iter_unpack("<III", blob)]


def entries(lo, hi):
    out = []
    for name in sorted(os.listdir(CHUNKS)):
        if not re.match(r"chunk_\d{4}\.txt$", name):
            continue
        with open(os.path.join(CHUNKS, name), encoding="utf-8", errors="replace") as fh:
            for m in HDR.finditer(fh.read()):
                a = int(m.group(1), 16)
                if lo <= a < hi:
                    out.append((a, a + int(m.group(2), 0)))
    return sorted(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pair", nargs="*", metavar="ADDR")
    ap.add_argument("--range", nargs=2, metavar=("LO", "HI"))
    a = ap.parse_args(argv)
    tva, tsz = img.section(".text")[:2]
    pdata = pdata_table()

    if a.range:
        lo, hi = (int(x, 16) for x in a.range)
        ents = entries(lo, hi)
        pairs = [(ents[i][1], ents[i + 1][0]) for i in range(len(ents) - 1)]
    else:
        if len(a.pair) != 2:
            ap.error("give ADDR ADDR or --range LO HI")
        pairs = [(int(a.pair[0], 16), int(a.pair[1], 16))]

    shown = 0
    for start, end in pairs:
        if end - start <= 1024 or start < tva or end > tva + tsz:
            continue
        blob = img.read(start, end - start)
        cover = [(b, e) for b, e in pdata if b < end and e > start]
        ahead = [(b, e) for b, e in cover if b <= start]
        inside = [(b, e) for b, e in cover if start < b < end]
        if blob is None:
            print("gap 0x%x-0x%x  %d B | text bytes not in image/ | .pdata %d"
                  % (start, end, end - start, len(cover)))
        else:
            int3 = blob.count(0xCC)
            nop = blob.count(0x90)
            zero = blob.count(0x00)
            print("gap 0x%x-0x%x  %d B | int3 %d%% nop %d%% zero %d%% | .pdata %d"
                  % (start, end, end - start, 100 * int3 // len(blob),
                     100 * nop // len(blob), 100 * zero // len(blob), len(cover)))
        for b, e in ahead:
            print("   inside pdata span FUN_%x (%x-%x, %d B)" % (b, b, e, e - b))
        if inside:
            print("   %d pdata record(s) start in gap: %s"
                  % (len(inside), ", ".join("0x%x/%dB" % (b, e - b) for b, e in inside)))
        if not cover:
            print("   no pdata (leaf/no-unwind code)")
        if blob is not None and blob[:512].count(0xC3) >= 8 and int3:
            print("   stub table (>=8 ret in 512 B + int3 padding)")
        shown += 1
    print("-- %d gap(s) over 1 KiB" % shown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
