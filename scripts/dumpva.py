#!/usr/bin/env python3
"""Dump raw image bytes at a virtual address (data tables, pointer arrays). stdlib only.

usage (from work/flood/):
    python scripts/dumpva.py 0x143851c90          # 16 qwords, resolved
    python scripts/dumpva.py 0x143851c90 64       # 64 qwords
    python scripts/dumpva.py 0x143851c90 -n 64    # same
    python scripts/dumpva.py --bytes 0x143851c90 128

Each row: address, raw hex, u64, then a resolution -- `FUN_<addr>` for .text,
`"text"` for a NUL-terminated printable string in the same section, else nothing.
Bytes come from `scripts/img.py`: the client image when reachable (`OW_IMAGE`), else
the committed `image/` slices. A range in neither prints the `img.py export` command
that would add it. Read-only, standard library only.
"""
import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("addr")
    ap.add_argument("count", nargs="?", type=lambda s: int(s, 0), default=16)
    ap.add_argument("-n", "--qwords", type=lambda s: int(s, 0))
    ap.add_argument("--bytes", action="store_true")
    a = ap.parse_args(argv)
    if a.qwords is not None:
        a.count = a.qwords
    try:
        va = int(a.addr, 16)
    except ValueError:
        print("address must be hex", file=sys.stderr)
        return 1
    if img.read(va, 1) is None:
        print("0x%x is not file-backed (or not in image/) -- python scripts/img.py export 0x%x 16"
              % (va, va), file=sys.stderr)
        return 1

    if a.bytes:
        blob = img.read(va, a.count) or b""
        for i in range(0, len(blob), 16):
            chunk = blob[i:i + 16]
            print("0x%x  %-47s  %s" % (va + i, chunk.hex(" "),
                                       "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)))
        return 0

    ten = prog = 0
    for i in range(a.count):
        qva = va + i * 8
        raw = img.read(qva, 8)
        if raw is None:
            print("0x%x  (absent)  -- python scripts/img.py export 0x%x %d" % (qva, qva, 8 * a.count))
            break
        q = struct.unpack("<Q", raw)[0]
        note = ""
        s = img.section_at(q)
        if s is not None:
            name = s[0]
            if name == ".text":
                note = "-> FUN_%x" % q
                prog += 1
            else:
                t = img.cstring(q)
                if t is not None:
                    note = '"%s"' % t[:64]
                elif name in (".data", ".rdata"):
                    ten += 1
        if q:
            print("0x%x  %016x  %20u  %s" % (qva, q, q, note))
        else:
            print("0x%x  %016x  %20u  (0)" % (qva, q, q))
    print("-- %d qwords; %d .text targets; %d unmapped nonzero" % (a.count, prog, ten))
    return 0


if __name__ == "__main__":
    sys.exit(main())
