#!/usr/bin/env python3
"""Dump plaintext NUL-terminated strings from Overwatch_clean.exe .rdata.

Kinds: ascii (printable), cstring (contains \\t/\\n/\\r), utf16 (UTF-16LE).
Row shape matches strpool.tsv, so the shipped lookup works:

    python scripts/strlookup.py --pool rdata_names.tsv 0x143600000

usage:
    python scripts/rdata_names.py [image] [-o rdata_names.tsv]

Read-only, standard library only.
"""
import argparse
import os
import re
import struct
import sys

DEFAULT_IMAGE = r"E:\Overwatch\_retail_\Overwatch_clean.exe"
DEFAULT_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rdata_names.tsv")


def pe_sections(data):
    """(name, va, virtual_size, raw_ptr) for each section; PE32/PE32+."""
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    nsec = struct.unpack_from("<H", data, pe + 6)[0]
    optsz = struct.unpack_from("<H", data, pe + 20)[0]
    magic = struct.unpack_from("<H", data, pe + 24)[0]
    image_base = struct.unpack_from("<Q" if magic == 0x20B else "<I",
                                    data, pe + 24 + (0x18 if magic == 0x20B else 0x1C))[0]
    off = pe + 24 + optsz
    for _ in range(nsec):
        name = data[off:off + 8].rstrip(b"\0").decode("ascii", "replace")
        vsize, va, rawsize, rawptr = struct.unpack_from("<IIII", data, off + 8)
        yield name, image_base + va, min(vsize or rawsize, rawsize), rawptr
        off += 40


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", nargs="?", default=DEFAULT_IMAGE)
    ap.add_argument("-o", "--out", default=DEFAULT_OUT)
    a = ap.parse_args(argv)

    with open(a.image, "rb") as fh:
        data = fh.read()
    section = next((s for s in pe_sections(data) if s[0] == ".rdata"), None)
    if section is None:
        print("no .rdata section in %s" % a.image, file=sys.stderr)
        return 1
    _, va, size, raw = section
    blob = data[raw:raw + size]

    rows = []
    for m in re.finditer(rb"[\x09\x0a\x0d\x20-\x7e]{4,}\x00", blob):
        raw = m.group()[:-1]
        if sum(1 for b in raw if 0x20 <= b <= 0x7E) < 4:
            continue
        kind = "ascii" if all(0x20 <= b <= 0x7E for b in raw) else "cstring"
        rows.append((va + m.start(), raw.decode("latin1"), kind))
    for m in re.finditer(rb"(?:[\x09\x0a\x0d\x20-\x7e]\x00){4,}\x00\x00", blob):
        raw = m.group()[:-2]
        s = raw.decode("utf-16le")
        if sum(1 for c in s if 0x20 <= ord(c) <= 0x7E) < 4:
            continue
        rows.append((va + m.start(), s, "utf16"))
    rows.sort(key=lambda r: r[0])

    def esc(s):
        return (s.replace("\\", "\\\\").replace("\t", "\\t")
                 .replace("\r", "\\r").replace("\n", "\\n"))

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as out:
        out.write("# addr\ttext\tkind — plaintext NUL-terminated strings in .rdata\n")
        out.write("# kind: ascii | cstring (has \\t/\\n/\\r) | utf16 (UTF-16LE);\n")
        out.write("# >=4 printable chars; backslash and controls escaped; use scripts/strlookup.py --pool\n")
        for addr, s, kind in rows:
            out.write("0x%X\t%s\t%s\n" % (addr, esc(s), kind))
    print("%d strings -> %s" % (len(rows), a.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
