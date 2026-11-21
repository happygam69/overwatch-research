#!/usr/bin/env python3
"""Read the decoded XOR string pool that ships with this repo.

Nearly every "name page" in the client is an obfuscated record decoded in place on
first use, so a plain string search finds nothing. `strpool.tsv` (beside this
directory, two levels up from `scripts/`) already carries the plaintext for all of
them, so a `DAT_<addr>` symbol in decompiled code resolves without the image.

Row shape — `addr <TAB> text <TAB> kind <TAB> hash <TAB> name`:

    addr   pool header VA; the corpus names it `DAT_<addr>`
    text   the decoded plaintext
    kind   class / field / enumval / enumtype / owner / other (empty if unknown)
    hash   the 32-bit class / field / enum hash (empty if unknown)
    name   OWLib name, else a synthetic STU_<HASH> / field_<HASH> / enumval_<HASH>

A row whose text is `Unknown` is a name page the build stripped; columns 3-5 carry
the identity recovered from the registrar call that consumes it. Those are the only
rows that are not literal text — everything else in `text` is readable as-is.

usage:
    python scripts/strlookup.py 0x143884d660 [0x143884d763 ...]   # exact / nearest
    python scripts/strlookup.py --band 0x143849000 0x14384a000    # a whole page range
    python scripts/strlookup.py --grep 'MODEL|TXTR|MAPDATA'       # search the text
    python scripts/strlookup.py --grep '^m_' --ignore-case
    python scripts/strlookup.py --count                            # what is in the file

Read-only, standard library only, no paths outside this repository.
"""
import argparse
import bisect
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
POOL = os.path.join(HERE, "..", "strpool.tsv")

# PE sections of Overwatch_clean.exe as VA ranges, using VirtualSize (not raw size), so
# that an address that only exists at runtime is still classified. `.data` is 13.4 MB
# virtually but only 3.36 MB is file-backed; the rest is BSS with no bytes to decode.
REGIONS = [
    (".text", 0x140001000, 0x142F2C3D3),
    (".rdata", 0x142F2D000, 0x143845F58),
    (".data", 0x143846000, 0x143B79600),
    (".data BSS", 0x143B79600, 0x14450A3BC),
    (".pdata", 0x14450B000, 0x144758968),
    ("_RDATA", 0x144759000, 0x1447792E0),
    (".rodata", 0x14477A000, 0x14477B260),
    (".rsrc", 0x14477C000, 0x1447890B0),
    (".reloc", 0x14478A000, 0x14483718C),
]


def region(addr):
    """Section name for a VA; only .rdata/_RDATA/.data carry decoded pool pages."""
    for name, lo, hi in REGIONS:
        if lo <= addr < hi:
            return name
    return "unmapped"


def unescape(s):
    esc = {"t": "\t", "n": "\n", "r": "\r"}
    return re.sub(r"\\(.)", lambda m: esc.get(m.group(1), m.group(1)), s)


def load(path=None):
    """Rows sorted by address as (addr, text, kind, hash, name)."""
    path = path or POOL
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 2:
                continue
            try:
                addr = int(p[0], 16)
            except ValueError:
                continue
            p += [""] * (5 - len(p))
            rows.append((addr, unescape(p[1]), p[2], p[3], p[4]))
    rows.sort()
    return rows


def show(text, kind, hashv, name):
    if name:
        bits = " ".join(x for x in (kind, hashv, name) if x)
        return "%r [%s]" % (text, bits)
    return repr(text)


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("addrs", nargs="*", help="pool addresses, 0x-prefixed")
    ap.add_argument("--band", nargs=2, metavar=("START", "END"), help="list a range")
    ap.add_argument("--grep", metavar="REGEX", help="search the plaintext")
    ap.add_argument("-i", "--ignore-case", action="store_true")
    ap.add_argument("--window", type=lambda s: int(s, 0), default=0x100,
                    help="nearest-match tolerance in bytes (default 0x100)")
    ap.add_argument("--count", action="store_true", help="summarise the file")
    ap.add_argument("--pool", help="alternate strpool.tsv")
    a = ap.parse_args(argv)

    rows = load(a.pool)
    if a.count:
        unknown = sum(1 for r in rows if r[1] == "Unknown")
        named = sum(1 for r in rows if r[4])
        uniq = len({r[1] for r in rows})
        print("%d rows, %d unique strings, %d identified" % (len(rows), uniq, named))
        print("literal 'Unknown' placeholders: %d (%.1f %% of rows, %d of %d unique)"
              % (unknown, 100.0 * unknown / len(rows),
                 int(unknown > 0), uniq))
        print("readable non-placeholder rows: %d" % (len(rows) - unknown))
        return 0

    if a.band:
        lo, hi = (int(x, 16) for x in a.band)
        hits = [r for r in rows if lo <= r[0] < hi]
        for addr, text, kind, hashv, name in hits:
            print("0x%X %s" % (addr, show(text, kind, hashv, name)))
        print("%d rows in 0x%X..0x%X" % (len(hits), lo, hi), file=sys.stderr)
        return 0

    if a.grep:
        flags = re.IGNORECASE if a.ignore_case else 0
        rx = re.compile(a.grep, flags)
        hits = 0
        for addr, text, kind, hashv, name in rows:
            if rx.search(text) or (name and rx.search(name)):
                print("0x%X %s" % (addr, show(text, kind, hashv, name)))
                hits += 1
        print("%d of %d rows match %r" % (hits, len(rows), a.grep), file=sys.stderr)
        return 0 if hits else 1

    if not a.addrs:
        ap.print_help()
        return 2

    keys = [r[0] for r in rows]
    for arg in a.addrs:
        addr = int(arg, 16)
        i = bisect.bisect_right(keys, addr) - 1
        if i >= 0 and addr - keys[i] <= a.window:
            r = rows[i]
            print("0x%X -> +0x%X %s" % (addr, addr - r[0], show(r[1], r[2], r[3], r[4])))
        elif i + 1 < len(rows) and keys[i + 1] - addr <= a.window:
            r = rows[i + 1]
            print("0x%X -> -0x%X %s" % (addr, r[0] - addr, show(r[1], r[2], r[3], r[4])))
        else:
            print("0x%X -> (no pool string within 0x%X bytes)" % (addr, a.window))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
