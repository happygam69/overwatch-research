#!/usr/bin/env python3
"""Dump plaintext NUL-terminated strings from Overwatch_clean.exe .rdata.

Kinds: ascii (printable), cstring (contains \\t/\\n/\\r), utf16 (UTF-16LE).
Row shape matches strpool.tsv, so the shipped lookup works:

    python scripts/strlookup.py --pool rdata_names.tsv 0x143600000

usage:
    python scripts/rdata_names.py [image] [-o rdata_names.tsv]

The default image is `OW_IMAGE` or the path in `scripts/img.py`; this regenerates the
shipped table, so it needs the whole `.rdata` and cannot run from the `image/` slices.
Read-only, standard library only.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img  # noqa: E402

DEFAULT_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rdata_names.tsv")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", nargs="?", default=None,
                    help="default: OW_IMAGE or %s" % img.IMAGE)
    ap.add_argument("-o", "--out", default=DEFAULT_OUT)
    a = ap.parse_args(argv)

    if a.image:
        img.IMAGE = a.image
    s = img.section(".rdata")
    blob = img.read(s[0], s[2]) if s else None
    if blob is None:
        print("no .rdata bytes -- set OW_IMAGE (or pass the image path); this command "
              "regenerates the shipped table and needs the whole section", file=sys.stderr)
        return 1
    va = s[0]

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
