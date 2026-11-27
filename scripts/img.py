#!/usr/bin/env python3
"""Raw image bytes without the image. stdlib only.

The client image (65 MB) is not in this repo, but records quote raw bytes at VAs:
XOR-8 pages, pointer/float tables, the `.pdata` unwind table. Those bytes live in
`image/` -- `pe.json` (section table + image identity) and zlib slices keyed by VA
(`slices.json` index + `slices.bin`) -- and every script reads through `read()`:
the image itself when reachable (`OW_IMAGE`, else `IMAGE` below), else the slices.
A bare clone can therefore re-derive every byte the records quote.

usage (from work/flood/):
    python scripts/img.py stats                      # what the store holds
    python scripts/img.py init                       # write image/pe.json from the image
    python scripts/img.py export 0x143872f70 108     # copy a range into the store
    python scripts/img.py export --pdata             # the whole .pdata (1.1 MB zlib)
    python scripts/img.py export --cited ranges/*.md # every data VA a record quotes
    python scripts/img.py selftest                   # read the store with no image

`export`/`init` need the image once; everything else works from the repo alone.
Read-only unless a subcommand says otherwise, standard library only.
"""
import bisect
import hashlib
import json
import os
import re
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
STORE = os.path.join(ROOT, "image")
IMAGE = os.environ.get("OW_IMAGE", r"E:\Overwatch\_retail_\Overwatch_clean.exe")

# The two artifacts of this build. They are byte-identical everywhere except `.text`: in
# the retail exe `.text` is encrypted (7.98 bits/byte), .rdata/.data/.pdata are plaintext.
# So the retail exe can serve every data-section read; code bytes must come from the clean
# (unpacked memory) image.
CLEAN_SHA = "e02f89fd1df5512b329498780db9f99164f6bb676ea9ecdf1feffa74d63e5037"
SHIPPED_SHA = "e4472f75a11f035c5854f8eed41c1388878b517ec4f64258316bdcc132e49cd5"

_pe = None
_slices = None
_keys = None
_blob = b""
_image = False          # False = not loaded yet, None = absent
_sha = False
_warned = False
_force_store = False    # selftest: ignore the image even when it is there


def pe():
    """{'base', 'size', 'sha256', 'sections': [[name, va, vsize, rawsize, rawoff], ...]}"""
    global _pe
    if _pe is None:
        with open(os.path.join(STORE, "pe.json"), encoding="utf-8") as fh:
            _pe = json.load(fh)
    return _pe


def sections():
    return [tuple(s) for s in pe()["sections"]]


def section_at(va):
    for s in sections():
        if s[1] <= va < s[1] + max(s[2], s[3]):
            return s
    return None


def section(name):
    """(va, virtual_size, file_size, raw_offset) or None."""
    for s in sections():
        if s[0] == name:
            return s[1:]
    return None


def image():
    """Whole image bytes if reachable, else None."""
    global _image
    if _image is False:
        try:
            with open(IMAGE, "rb") as fh:
                _image = fh.read()
        except OSError:
            _image = None
    return _image


def load_store():
    global _slices, _keys, _blob
    if _slices is None:
        try:
            with open(os.path.join(STORE, "slices.json"), encoding="utf-8") as fh:
                _slices = json.load(fh)["slices"]
            with open(os.path.join(STORE, "slices.bin"), "rb") as fh:
                _blob = fh.read()
        except FileNotFoundError:
            _slices, _blob = [], b""
        _keys = [r[0] for r in _slices]
    return _slices


def sha():
    """sha256 of the reachable image, or None."""
    global _sha
    if _sha is False:
        d = image()
        _sha = hashlib.sha256(d).hexdigest() if d else None
    return _sha


def build():
    """'clean' (full image), 'shipped' (retail exe: data sections only), or None."""
    s = sha()
    if s is None:
        return None
    if s == SHIPPED_SHA:
        return "shipped"
    if s == CLEAN_SHA or s == pe()["sha256"]:
        return "clean"
    return None


def _warn_shipped():
    global _warned
    if not _warned:
        _warned = True
        sys.stderr.write("img: image is the retail Overwatch.exe -- .text is encrypted there, "
                         "data sections only (use the clean image for code bytes)\n")


def read(va, n):
    """n file-backed bytes at va -- image first, else the slice store; None if absent."""
    if n <= 0:
        return b""
    d = None if _force_store else image()
    if d is not None:
        b = build()
        if b is None:
            raise SystemExit("image at %s is sha256 %s..., neither Overwatch_clean.exe (%s...) "
                             "nor Overwatch.exe (%s...) -- point OW_IMAGE at the right build"
                             % (IMAGE, (sha() or "")[:16], CLEAN_SHA[:16], SHIPPED_SHA[:16]))
        s = section_at(va)
        if s is None or va - s[1] + n > s[3]:
            return None
        if b == "shipped" and s[0] == ".text":
            _warn_shipped()
            return None
        o = s[4] + va - s[1]
        return d[o:o + n]
    slices = load_store()
    i = bisect.bisect_right(_keys, va) - 1
    if i >= 0:
        va0, ln, off, zln = slices[i]
        if va0 <= va and va + n <= va0 + ln:
            return zlib.decompress(_blob[off:off + zln])[va - va0:va - va0 + n]
    return None


def cstring(va, limit=96):
    """NUL-terminated printable ASCII at va, or None."""
    raw = read(va, limit)
    if raw is None:
        return None
    end = raw.find(b"\0")
    if end < 0:
        return None
    raw = raw[:end]
    return raw.decode("ascii") if raw and all(9 <= b <= 0x7E for b in raw) else None


def need(va, span=0x40):
    """Cache ranges worth keeping for a cited address: 16-aligned, XOR-8 page extended."""
    s = section_at(va)
    if s is None or s[0] == ".text":
        return []
    start = va & ~15
    ln = read(va + 8, 8)
    if ln:
        k = struct.unpack("<Q", ln)[0] & 0xFFFFFF      # {key[8], len24, data} triple
        if 0 < k <= 0x4000 and section_at(va + 0xC + k):
            span = max(span, va + 0xC + k - start)
    return [(start, span)]


def _from_image(d, va, n):
    s = section_at(va)
    if s is None or va - s[1] + n > s[3]:
        return b""
    o = s[4] + va - s[1]
    return d[o:o + n]


def save(parts):
    """parts: [(va, bytes)] -> merged, zlib, written to `image/`."""
    parts = sorted((p, b) for p, b in parts if b)
    merged = []
    for start, b in parts:
        if merged and start <= merged[-1][0] + len(merged[-1][1]) + 16:
            p, pb = merged[-1]
            end = max(p + len(pb), start + len(b))
            buf = bytearray(end - p)
            buf[:len(pb)] = pb
            buf[start - p:start - p + len(b)] = b
            merged[-1] = (p, bytes(buf))
        else:
            merged.append((start, b))
    os.makedirs(STORE, exist_ok=True)
    rows, out = [], bytearray()
    for start, b in merged:
        z = zlib.compress(b, 9)
        rows.append([start, len(b), len(out), len(z)])
        out += z
    with open(os.path.join(STORE, "slices.bin"), "wb") as fh:
        fh.write(out)
    meta = {"image": {k: pe()[k] for k in ("size", "sha256")}, "slices": rows}
    with open(os.path.join(STORE, "slices.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(meta, fh, indent=0)
        fh.write("\n")
    return len(rows), len(out)


def write_pe():
    """Write `image/pe.json` from the image (run once, where the image exists)."""
    d = image()
    if d is None:
        raise SystemExit("no image at %s -- set OW_IMAGE" % IMAGE)
    if hashlib.sha256(d).hexdigest() == SHIPPED_SHA:
        raise SystemExit("that is the retail Overwatch.exe (.text encrypted); init from the "
                         "clean/unpacked image -- the section tables are identical, but the "
                         "build identity must name the clean one")
    peoff = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, peoff + 6)[0]
    optsz = struct.unpack_from("<H", d, peoff + 20)[0]
    magic = struct.unpack_from("<H", d, peoff + 24)[0]
    base = struct.unpack_from("<Q" if magic == 0x20B else "<I", d,
                              peoff + 24 + (0x18 if magic == 0x20B else 0x1C))[0]
    off = peoff + 24 + optsz
    out = []
    for _ in range(nsec):
        name = d[off:off + 8].rstrip(b"\0").decode("ascii", "replace")
        vsz, va, rsz, raw = struct.unpack_from("<IIII", d, off + 8)
        out.append([name, base + va, vsz, min(rsz, vsz or rsz), raw])
        off += 40
    os.makedirs(STORE, exist_ok=True)
    with open(os.path.join(STORE, "pe.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"name": os.path.basename(IMAGE), "base": base, "size": len(d),
                   "sha256": hashlib.sha256(d).hexdigest(), "sections": out}, fh, indent=0)
        fh.write("\n")
    print("%d sections -> image/pe.json (size %d, sha256 %s…)"
          % (len(out), len(d), hashlib.sha256(d).hexdigest()[:16]))


RX = re.compile(r"(?<![0-9a-fA-F])(14[0-9a-fA-F]{7,8})(?![0-9a-fA-F])")


def cited(paths, span=0x40):
    """Cache windows for every data-section VA mentioned in the given records/docs."""
    want, seen = [], set()
    for p in paths:
        with open(p, encoding="utf-8", errors="replace") as fh:
            for m in RX.finditer(fh.read()):
                va = int(m.group(1), 16)
                if va in seen:
                    continue
                seen.add(va)
                want.extend(need(va, span))
    return want


def cmd_export(argv):
    d = image()
    if d is None:
        raise SystemExit("no image at %s -- set OW_IMAGE" % IMAGE)
    want = []
    if argv.pdata:
        s = section(".pdata")
        want.append((s[0], s[2]))
    if argv.cited:
        want.extend(cited(argv.cited))
    if len(argv.addr_len) % 2:
        raise SystemExit("export wants ADDR LEN pairs")
    for va, n in zip(argv.addr_len[::2], argv.addr_len[1::2]):
        want.append((int(va, 16), int(n, 0)))
    cur = list(zip([r[0] for r in load_store()],
                   [zlib.decompress(_blob[r[2]:r[2] + r[3]]) for r in load_store()]))
    for va, n in want:
        cur.append((va, _from_image(d, va, n)))
    rows, size = save(cur)
    print("%d range(s) requested -> %d slice(s), %d B zlib in image/slices.bin"
          % (len(want), rows, size))


def cmd_stats(argv):
    slices = load_store()
    tot = sum(r[1] for r in slices)
    raw = sum(r[3] for r in slices)
    print("image/pe.json      %s  size %d  %s"
          % ("present" if os.path.exists(os.path.join(STORE, "pe.json")) else "MISSING",
             pe()["size"], pe()["sha256"][:16]))
    print("image/slices.bin   %d slices  %d B raw  %d B zlib" % (len(slices), tot, raw))
    print("image reachable    %s" % (("%s (%s)" % (build(), IMAGE)) if image() is not None
                                    else "no (%s)" % IMAGE))
    for name, va, vsz, rsz, _raw in sections():
        if va:
            cover = sum(1 for r in slices if va <= r[0] < va + max(vsz, rsz))
            print("  %-8s 0x%x  %d slice(s)" % (name, va, cover))


SELFTEST = [(0x143872f70, "This console command is configured incorrectly"),
            (0x143872fe0, "This console command does not take arguments"),
            (0x143873020, "Values for entity %s, instance %d"),
            (0x143873060, "[%d]: (No output variable)"),
            (0x143873088, "[%d]: %s"),
            (0x1438730a0, "Expected at least %d argument%s")]


def cmd_selftest(argv):
    """The store alone (no image) must still yield the pages pass 77 quoted."""
    global _force_store
    _force_store = True
    bad = 0
    for va, want in SELFTEST:
        raw = read(va, 0x10)
        if raw is None:
            print("MISSING page 0x%x -- run: python scripts/img.py export 0x%x 0x40" % (va, va))
            bad += 1
            continue
        key = raw[:8]
        n = struct.unpack_from("<Q", raw, 8)[0] & 0xFFFFFF
        ct = read(va + 0xC, n)
        text = bytes(b ^ key[i & 7] for i, b in enumerate(ct or b"")) if ct else b""
        ok = text.startswith(want.encode()) and len(text) == n
        print("%s 0x%x  %r" % ("ok  " if ok else "FAIL", va, text[:60]))
        bad += not ok
    pd = section(".pdata")
    print("%s .pdata table %d records"
          % ("ok  " if read(pd[0], 12) else "FAIL",
             (pd[2] // 12) if read(pd[0], 12) else 0))
    print("-- selftest %s" % ("passed" if not bad else "%d failure(s)" % bad))
    return 1 if bad else 0


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("init")
    sub.add_parser("stats")
    sub.add_parser("selftest")
    e = sub.add_parser("export")
    e.add_argument("addr_len", nargs="*", metavar="ADDR LEN")
    e.add_argument("--pdata", action="store_true")
    e.add_argument("--cited", nargs="+", metavar="PATH")
    a = ap.parse_args(argv)
    if a.cmd == "init":
        write_pe()
        return 0
    if a.cmd == "export":
        cmd_export(a)
        return 0
    if a.cmd == "selftest":
        return cmd_selftest(a)
    cmd_stats(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
