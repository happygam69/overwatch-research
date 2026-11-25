#!/usr/bin/env python3
"""Dump raw image bytes at a virtual address (data tables, pointer arrays). stdlib only.

usage (from work/flood/):
    python scripts/dumpva.py 0x143851c90          # 16 qwords, resolved
    python scripts/dumpva.py 0x143851c90 64       # 64 qwords
    python scripts/dumpva.py 0x143851c90 -n 64    # same
    python scripts/dumpva.py --bytes 0x143851c90 128

Each row: address, raw hex, u64, then a resolution -- `FUN_<addr>` for .text,
`"text"` for a NUL-terminated printable string in the same section, else nothing.
Read-only, no paths outside this repository except the shipped image.
"""
import argparse
import os
import struct
import sys

IMAGE = r"E:\Overwatch\_retail_\Overwatch_clean.exe"


def sections(data):
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    nsec = struct.unpack_from("<H", data, pe + 6)[0]
    optsz = struct.unpack_from("<H", data, pe + 20)[0]
    magic = struct.unpack_from("<H", data, pe + 24)[0]
    base = struct.unpack_from("<Q" if magic == 0x20B else "<I", data,
                              pe + 24 + (0x18 if magic == 0x20B else 0x1C))[0]
    off = pe + 24 + optsz
    for _ in range(nsec):
        name = data[off:off + 8].rstrip(b"\0").decode("ascii", "replace")
        vsz, va, rsz, raw = struct.unpack_from("<IIII", data, off + 8)
        yield name, base + va, min(vsz or rsz, rsz), raw, rsz
        off += 40


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
    with open(IMAGE, "rb") as fh:
        data = fh.read()
    secs = list(sections(data))

    def sec_of(va):
        for name, sva, size, raw, rsz in secs:
            if sva <= va < sva + max(size, rsz):
                return name, sva, size, raw
        return None

    def off_of(va):
        s = sec_of(va)
        if s is None:
            return None
        name, sva, size, raw = s
        if va - sva >= size:
            return None
        return raw + (va - sva)

    def cstr(va, limit=96):
        o = off_of(va)
        if o is None:
            return None
        end = data.find(b"\0", o, o + limit)
        if end < 0:
            return None
        raw = data[o:end]
        if raw and all(9 <= b <= 0x7E for b in raw):
            return raw.decode("ascii")
        return None

    try:
        va = int(a.addr, 16)
    except ValueError:
        print("address must be hex", file=sys.stderr)
        return 1
    o = off_of(va)
    if o is None:
        print("0x%x is not file-backed" % va, file=sys.stderr)
        return 1

    if a.bytes:
        blob = data[o:o + a.count]
        for i in range(0, len(blob), 16):
            chunk = blob[i:i + 16]
            print("0x%x  %-47s  %s" % (va + i, chunk.hex(" "),
                                       "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)))
        return 0

    ten = prog = 0
    for i in range(a.count):
        qva = va + i * 8
        qo = off_of(qva)
        if qo is None or qo + 8 > len(data):
            break
        q = struct.unpack_from("<Q", data, qo)[0]
        note = ""
        s = sec_of(q)
        if s is not None:
            name = s[0]
            if name == ".text":
                note = "-> FUN_%x" % q
                prog += 1
            else:
                t = cstr(q)
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
