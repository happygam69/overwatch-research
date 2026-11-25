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
standard library only; the image path is the one `rdata_names.py` already uses.
"""
import argparse
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHUNKS = os.path.join(HERE, "..", "chunks")
IMAGE = r"E:\Overwatch\_retail_\Overwatch_clean.exe"
HDR = re.compile(r"^// ([0-9a-f]{9,16}) \S+ size=(0x[0-9a-f]+|\d+)", re.M)


def sections(data):
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    nsec = struct.unpack_from("<H", data, pe + 6)[0]
    optsz = struct.unpack_from("<H", data, pe + 20)[0]
    magic = struct.unpack_from("<H", data, pe + 24)[0]
    base = struct.unpack_from("<Q" if magic == 0x20B else "<I", data,
                              pe + 24 + (0x18 if magic == 0x20B else 0x1C))[0]
    off = pe + 24 + optsz
    out = {}
    for _ in range(nsec):
        name = data[off:off + 8].rstrip(b"\0").decode("ascii", "replace")
        vsz, va, rsz, raw = struct.unpack_from("<IIII", data, off + 8)
        out[name] = (base + va, min(vsz or rsz, rsz), raw)
        off += 40
    return base, out


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
    with open(IMAGE, "rb") as fh:
        data = fh.read()
    base, sec = sections(data)
    tva, tsz, traw = sec[".text"]
    pva, psz, praw = sec[".pdata"]
    pdata = []
    for i in range(psz // 12):
        b, e, _u = struct.unpack_from("<III", data, praw + i * 12)
        pdata.append((base + b, base + e))

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
        blob = data[traw + start - tva:traw + end - tva]
        int3 = blob.count(0xCC)
        nop = blob.count(0x90)
        zero = blob.count(0x00)
        cover = [(b, e) for b, e in pdata if b < end and e > start]
        ahead = [(b, e) for b, e in cover if b <= start]
        inside = [(b, e) for b, e in cover if start < b < end]
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
        if blob[:512].count(0xC3) >= 8 and int3:
            print("   stub table (>=8 ret in 512 B + int3 padding)")
        shown += 1
    print("-- %d gap(s) over 1 KiB" % shown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
