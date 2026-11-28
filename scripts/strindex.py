#!/usr/bin/env python3
"""Index every string the corpus names, and where each one is referenced.

Three sources, one address-keyed map:

  pool     the decoded XOR name pages (`strpool.tsv`), referenced from a chunk as
           `&DAT_<base>` (page key = base+8), `_DAT_<key>` (the 8-byte header) or
           any byte inside the payload.  One row per page.
  rdata    plaintext `.rdata` strings, referenced by their exact address or through a
           `PTR_s_<name>_<addr>` / `PTR_u_<name>_<addr>` pointer (one qword deref, read
           through `img.py` when the image/slices are present).  This table has no file of
           its own: it is stored as the rdata rows of `strings_index.tsv`.
  literal  C string literals the decompiler printed inline (`"..."`, `L"..."`), with
           their function, plus the `.rdata` row(s) whose text and kind match exactly.

Outputs (repo root, overwritten):

  strings_index.tsv     addr source section kind name hits ptr lit funcs first_chunk first_func text
  strings_literals.tsv  wide hits funcs first_chunk first_func rdata_addr text
  strings_refs.tsv      addr source wide chunk func hits deltas text

`hits` counts mentions, `funcs` distinct owner functions, `first_*` the first sighting in
address order, `deltas` the offsets from the string key seen in that function (`-8` = page
base literal, `0` = key/header, `+8` = payload).  A pool page's decrypt loop names its own
record ~9 times, so `funcs` is the semantic count and `hits` is not.  Window hosts re-emit
another function's body, so a string can be credited to both.  `ptr` counts `PTR_s_`/
`PTR_u_` derefs; `lit` counts inline literals that match exactly one `.rdata` row.

usage:
    python scripts/strindex.py                     # full scan + summary + three TSVs
    python scripts/strindex.py --find 'DualZone'   # regex over text / name / address
    python scripts/strindex.py --addr 0x1438734D0  # one string and every ref
    python scripts/strindex.py --func 0x140dd8320  # strings one function names
    python scripts/strindex.py --chunk 0749        # strings one chunk names
    python scripts/strindex.py --selftest

Read-only except the three TSVs; standard library only.  The one-qword pointer deref reads
through `img.py` (the image when reachable, else the committed slices), so the scan runs on
a bare clone too.
"""
import argparse
import bisect
import collections
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import strlookup  # noqa: E402

try:
    import img  # noqa: E402  (optional: only the PTR_s_ deref needs bytes)
except ImportError:  # pragma: no cover
    img = None

SRC_POOL = os.path.join(ROOT, "strpool.tsv")
OUT_INDEX = os.path.join(ROOT, "strings_index.tsv")
OUT_LITERALS = os.path.join(ROOT, "strings_literals.tsv")
OUT_REFS = os.path.join(ROOT, "strings_refs.tsv")

# 14xxxxxxx is the whole VA space of this image; the lookarounds reject a match inside
# a longer hex run (16-hex chunk-header addresses, 64-bit constants).
RX_ADDR = re.compile(r"(?<![0-9a-fA-F])(14[0-9a-fA-F]{7})(?![0-9a-fA-F])")
RX_HDR = re.compile(r"(?m)^// ([0-9a-f]{16})_")
# C literal; \\ escapes are consumed here, decoded later.  A raw newline cannot occur.
RX_LIT = re.compile(r'(L?)"((?:[^"\\\n]|\\.)*)"')
PTR_PRE = ("PTR_s_", "PTR_u_")
RX_RASC = re.compile(rb"[\x09\x0a\x0d\x20-\x7e]{4,}\x00")
RX_RU16 = re.compile(rb"(?:[\x09\x0a\x0d\x20-\x7e]\x00){4,}\x00\x00")
INDEX_HDR = ["addr", "source", "section", "kind", "name", "hits", "ptr", "lit",
             "funcs", "first_chunk", "first_func", "text"]
ESC = {"a": "\a", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t",
       "v": "\v", "0": "\0", "\\": "\\", '"': '"', "'": "'"}


def esc(s):
    """TSV-safe text: backslash-escape backslash and every control byte."""
    out = []
    for c in s:
        o = ord(c)
        if c == "\\":
            out.append("\\\\")
        elif c == "\t":
            out.append("\\t")
        elif c == "\n":
            out.append("\\n")
        elif c == "\r":
            out.append("\\r")
        elif o < 32 or o == 127:
            out.append("\\x%02x" % o)
        else:
            out.append(c)
    return "".join(out)


def cunescape(s):
    """Decode the escapes Ghidra prints inside a C string literal."""
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        i += 1
        if i >= len(s):
            out.append("\\")
            break
        d = s[i]
        i += 1
        if d == "x":
            m = re.match(r"[0-9a-fA-F]{1,2}", s[i:])
            if m:
                out.append(chr(int(m.group(), 16)))
                i += len(m.group())
            else:
                out.append("x")
        elif d in "01234567":
            j = i - 1
            while i < len(s) and i - j < 3 and s[i] in "01234567":
                i += 1
            out.append(chr(int(s[j:i], 8)))
        else:
            out.append(ESC.get(d, d))
    return "".join(out)


def page_hit(pool, keys, addr):
    """Row whose [key-8, key+8+len(text)] record covers addr, best candidate wins."""
    i = bisect.bisect_right(keys, addr) - 1
    best = None
    best_score = 9
    for j in (i, i + 1):
        if not 0 <= j < len(pool):
            continue
        key, text = keys[j], pool[j][1]
        if not key - 8 <= addr < key + 8 + len(text) + 1:
            continue
        score = 0 if addr == key else 1 if addr == key - 8 else 2
        if score < best_score:
            best, best_score = j, score
    return None if best is None else pool[best]


def deref_addr(addr):
    """Qword at addr, or None (image/slices absent or the range was never exported)."""
    if img is None:
        return None
    raw = img.read(addr, 8)
    return struct.unpack("<Q", raw)[0] if raw and len(raw) == 8 else None


def load_rdata():
    """`.rdata` plaintext rows as (addr, text, kind, "", ""), strlookup.load() shape.

    Re-read from `.rdata` when the image is reachable; the committed slices hold only the
    VAs a record cites, not the whole 5.7 MB section. On a bare clone the rows come from
    the index being rebuilt -- they are 100% of `strings_index.tsv`'s rdata rows, so the
    table survives a full rescan without a second copy on disk.
    """
    s = img.section(".rdata") if img is not None else None
    blob = img.read(s[0], s[2]) if s else None
    if blob:
        rows = []
        for m in RX_RASC.finditer(blob):
            raw = m.group()[:-1]
            if sum(1 for b in raw if 0x20 <= b <= 0x7E) < 4:
                continue
            kind = "ascii" if all(0x20 <= b <= 0x7E for b in raw) else "cstring"
            rows.append((s[0] + m.start(), raw.decode("latin1"), kind))
        for m in RX_RU16.finditer(blob):
            txt = m.group()[:-2].decode("utf-16le")
            if sum(1 for c in txt if 0x20 <= ord(c) <= 0x7E) < 4:
                continue
            rows.append((s[0] + m.start(), txt, "utf16"))
        rows.sort(key=lambda r: r[0])
        return [(a, t, k, "", "") for a, t, k in rows]
    if not os.path.exists(OUT_INDEX):
        print("no .rdata bytes and no %s -- rdata rows unavailable" % OUT_INDEX,
              file=sys.stderr)
        return []
    print(".rdata not readable -- inheriting the rdata rows of %s" % OUT_INDEX,
          file=sys.stderr)
    rows = []
    with open(OUT_INDEX, encoding="utf-8", errors="replace") as fh:
        fh.readline()
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) != len(INDEX_HDR) or p[1] != "rdata":
                continue
            # the text column only holds \\, \t, \n, \r escapes (the extraction byte class)
            rows.append((int(p[0], 16), strlookup.unescape(p[11]), p[3], "", ""))
    return rows


def scan():
    pool = strlookup.load(SRC_POOL)
    pkeys = [r[0] for r in pool]
    rdata = load_rdata()
    rmap = {r[0]: r for r in rdata}
    rtext = collections.defaultdict(list)
    rkind = {}
    for a, text, kind, _, _ in rdata:
        rtext[text].append(a)
        rkind[a] = kind

    # addr -> {source, kind, name, text, hits, ptr, funcs:set, first:(chunk,func)}
    index = {}
    for a, text, kind, _, name in pool:
        index[a] = dict(source="pool", kind=kind, name=name, text=text, hits=0, ptr=0,
                        lit=0, funcs=set(), first=None)
    for a, text, kind, _, _ in rdata:
        index[a] = dict(source="rdata", kind=kind, name="", text=text, hits=0, ptr=0,
                        lit=0, funcs=set(), first=None)

    lit = {}                     # (text, wide) -> hits, funcs, first
    refs = collections.Counter()  # (key, chunk, func) -> mentions
    deltas = collections.defaultdict(set)
    chunks = funcs = 0
    for n in range(2228):
        path = os.path.join(ROOT, "chunks", "chunk_%04d.txt" % n)
        if not os.path.exists(path):
            continue
        chunks += 1
        with open(path, encoding="utf-8", errors="replace") as fh:
            body = fh.read()
        heads = [(m.start(), int(m.group(1), 16)) for m in RX_HDR.finditer(body)]
        funcs += len(heads)
        hpos = [h[0] for h in heads]

        def owner(pos):
            i = bisect.bisect_right(hpos, pos) - 1
            return heads[i][1] if i >= 0 else 0

        def hit(key, pos, step):
            rec = index[key]
            f = owner(pos)
            rec["hits"] += 1
            rec["funcs"].add(f)
            if rec["first"] is None:
                rec["first"] = (n, f)
            refs[(key, n, f)] += 1
            deltas[(key, n, f)].add(step)
            return rec

        for m in RX_ADDR.finditer(body):
            a = int(m.group(1), 16)
            reg = strlookup.region(a)
            if reg == ".data":
                row = page_hit(pool, pkeys, a)
                if row is not None:
                    hit(row[0], m.start(), a - row[0])
            elif reg == ".rdata":
                if a in rmap:
                    hit(a, m.start(), 0)
                elif any(p in body[max(0, m.start() - 40):m.start()] for p in PTR_PRE):
                    t = deref_addr(a)
                    if t is not None and t in rmap:
                        rec = hit(t, m.start(), 0)
                        rec["ptr"] += 1

        for m in RX_LIT.finditer(body):
            text = cunescape(m.group(2))
            if not text:
                continue
            wide = 1 if m.group(1) else 0
            key = (text, wide)
            rec = lit.get(key)
            if rec is None:
                rec = lit[key] = dict(hits=0, funcs=set(), first=None)
            f = owner(m.start())
            rec["hits"] += 1
            rec["funcs"].add(f)
            if rec["first"] is None:
                rec["first"] = (n, f)
            refs[(key, n, f)] += 1

    lit_addrs = {}
    for (text, wide), rec in lit.items():
        want = ("utf16",) if wide else ("ascii", "cstring")
        cand = [a for a in rtext.get(text, ()) if rkind[a] in want]
        lit_addrs[(text, wide)] = cand
        if len(cand) == 1:
            index[cand[0]]["lit"] += rec["hits"]
    return index, lit, refs, deltas, chunks, funcs, lit_addrs


def write(index, lit, refs, deltas, lit_addrs):
    with open(OUT_INDEX, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# " + "\t".join(INDEX_HDR) + "\n")
        for a in sorted(index):
            r = index[a]
            first = r["first"] or ("", "")
            fh.write("0x%X\t%s\t%s\t%s\t%s\t%d\t%d\t%d\t%d\t%s\t%s\t%s\n" % (
                a, r["source"], strlookup.region(a), r["kind"], r["name"], r["hits"],
                r["ptr"], r["lit"], len(r["funcs"]),
                "%04d" % first[0] if first[0] != "" else "",
                "%X" % first[1] if first[1] else "", esc(r["text"])))

    with open(OUT_LITERALS, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# wide\thits\tfuncs\tfirst_chunk\tfirst_func\trdata_addr\ttext\n")
        for (text, wide), r in sorted(lit.items(), key=lambda kv: (-kv[1]["hits"], kv[0])):
            first = r["first"] or ("", "")
            addr = ",".join("0x%X" % a for a in lit_addrs[(text, wide)])
            fh.write("%d\t%d\t%d\t%s\t%s\t%s\t%s\n" % (
                wide, r["hits"], len(r["funcs"]),
                "%04d" % first[0] if first[0] != "" else "",
                "%X" % first[1] if first[1] else "", addr, esc(text)))

    rows = []
    for (k, chunk, func), hits in refs.items():
        if isinstance(k, tuple):
            text, wide = k
            rows.append((1, 0, wide, text, chunk, func, hits, "", "literal", text))
        else:
            d = sorted(deltas[(k, chunk, func)])
            rows.append((0, k, 0, "", chunk, func, hits,
                         ",".join("%+d" % x for x in d), index[k]["source"],
                         index[k]["text"]))
    with open(OUT_REFS, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# addr\tsource\twide\tchunk\tfunc\thits\tdeltas\ttext\n")
        for kind, a, wide, text, chunk, func, hits, d, source, body in sorted(
                rows, key=lambda r: (r[0], r[1], r[2], r[3], r[4], r[5])):
            fh.write("%s\t%s\t%d\t%04d\t%X\t%d\t%s\t%s\n" % (
                "0x%X" % a if kind == 0 else "", source, wide, chunk, func, hits, d,
                esc(body)))


def summary(index, lit, refs, deltas, chunks, funcs):
    pool = [r for r in index.values() if r["source"] == "pool"]
    rd = [r for r in index.values() if r["source"] == "rdata"]
    print("scan: %d chunks, %d functions" % (chunks, funcs))
    print("pool : %6d rows, %6d referenced, %7d mentions"
          % (len(pool), sum(1 for r in pool if r["hits"]), sum(r["hits"] for r in pool)))
    print("rdata: %6d rows, %6d referenced, %7d mentions (%d via PTR_s_/PTR_u_)"
          % (len(rd), sum(1 for r in rd if r["hits"]), sum(r["hits"] for r in rd),
             sum(r["ptr"] for r in rd)))
    print("       +%5d rows named only by a unique inline literal"
          % sum(1 for r in rd if r["lit"] and not r["hits"]))
    print("literal: %5d unique (%d wide), %7d mentions"
          % (len(lit), sum(1 for k in lit if k[1]), sum(r["hits"] for r in lit.values())))
    print("refs : %6d (string, function) rows" % len(refs))
    used_funcs = {f for (_, _, f) in refs}
    used_chunks = {n for (_, n, _) in refs}
    one = sum(1 for r in pool if r["hits"] and len(r["funcs"]) == 1)
    real = sum(1 for r in pool if r["hits"] and r["text"] != "Unknown")
    print("use  : %6d functions, %6d chunks name a string"
          % (len(used_funcs), len(used_chunks)))
    print("       pool: %5d referenced pages have one namer (registrar); %d carry real text"
          % (one, real))
    vocab = ({r["text"] for r in pool} | {r["text"] for r in rd}
             | {k[0] for k in lit})
    print("vocab: %6d distinct texts (%d pool + %d rdata + %d literal, overlapping)"
          % (len(vocab), len({r["text"] for r in pool}), len({r["text"] for r in rd}),
             len({k[0] for k in lit})))

    top = sorted((r for r in index.values() if r["hits"]),
                 key=lambda r: (-len(r["funcs"]), -r["hits"]))[:15]
    print("\ntop strings (by distinct functions):")
    for r in top:
        a = next(k for k, v in index.items() if v is r)
        print("  %4d funcs %6d hits  %s  %s"
              % (len(r["funcs"]), r["hits"], "0x%X" % a, esc(r["text"])[:90]))

    bands = collections.defaultdict(lambda: [0, 0])
    for a, r in index.items():
        if r["hits"]:
            b = bands[(a >> 16) << 16]
            b[0] += 1
            b[1] += r["hits"]
    print("\ntop bands (0x10000, distinct strings):")
    for lo, (rows, hits) in sorted(bands.items(), key=lambda kv: -kv[1][0])[:15]:
        best = max(((a, r) for a, r in index.items()
                    if (a >> 16) << 16 == lo and r["hits"]
                    and (r["text"] != "Unknown" or r["name"])),
                   default=None, key=lambda ar: len(ar[1]["funcs"]))
        if best is None:
            best = max(((a, r) for a, r in index.items()
                        if (a >> 16) << 16 == lo and r["hits"]),
                       key=lambda ar: len(ar[1]["funcs"]))
        label = best[1]["text"] if best[1]["text"] != "Unknown" else best[1]["name"]
        print("  0x%X %-8s %5d strings %7d hits  %s"
              % (lo, strlookup.region(best[0]), rows, hits, esc(label)[:55]))


def read_tsv(path, header):
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        head = fh.readline().lstrip("#").strip().split("\t")
        if head != header:
            raise SystemExit("%s: unexpected header %r" % (path, head))
        for line in fh:
            rows.append(line.rstrip("\n").split("\t"))
    return rows


def need_outputs():
    for p in (OUT_INDEX, OUT_LITERALS, OUT_REFS):
        if not os.path.exists(p):
            raise SystemExit("%s missing -- run python scripts/strindex.py first" % p)


def cmd_find(rx):
    need_outputs()
    idx = read_tsv(OUT_INDEX, INDEX_HDR)
    lit = read_tsv(OUT_LITERALS, ["wide", "hits", "funcs", "first_chunk", "first_func",
                                  "rdata_addr", "text"])
    pat = re.compile(rx, re.IGNORECASE)
    n = 0
    for a, src, sec, kind, name, hits, ptr, lits, funcs, ch, fn, text in idx:
        if pat.search(text) or (name and pat.search(name)) or pat.search(a):
            print("%s %s %-5s hits=%-6s funcs=%-4s first=%s/%s %s%s"
                  % (a, sec, src, hits, funcs, ch or "-", fn or "-", text,
                     " [%s %s]" % (kind, name) if kind or name else ""))
            n += 1
    for wide, hits, funcs, ch, fn, addr, text in lit:
        if pat.search(text) or (addr and pat.search(addr)):
            print("%-5s literal hits=%-6s funcs=%-4s first=%s/%s rdata=%s %s"
                  % ("wide" if wide == "1" else "", hits, funcs, ch or "-", fn or "-",
                     addr or "-", text))
            n += 1
    print("%d match(es)" % n, file=sys.stderr)


def cmd_addr(arg):
    need_outputs()
    a = int(arg, 16)
    idx = read_tsv(OUT_INDEX, INDEX_HDR)
    for row in idx:
        if int(row[0], 16) == a:
            print("\t".join(row))
            break
    else:
        print("0x%X not in %s" % (a, OUT_INDEX), file=sys.stderr)
        return 1
    refs = read_tsv(OUT_REFS, ["addr", "source", "wide", "chunk", "func", "hits",
                              "deltas", "text"])
    for row in refs:
        if row[0] and int(row[0], 16) == a:
            print("\t".join(row))
    lit = read_tsv(OUT_LITERALS, ["wide", "hits", "funcs", "first_chunk", "first_func",
                                  "rdata_addr", "text"])
    for wide, hits, funcs, ch, fn, addr, text in lit:
        if "0x%X" % a in addr.split(","):
            print("\tliteral\t%s\t%s\t%s\t%s\t\t%s" % (wide, ch, fn, hits, text))
    return 0


def cmd_refs(args):
    need_outputs()
    refs = read_tsv(OUT_REFS, ["addr", "source", "wide", "chunk", "func", "hits",
                              "deltas", "text"])
    func = int(args.func, 16) if args.func else None
    chunk = int(args.chunk.lstrip("0") or "0") if args.chunk else None
    n = 0
    for row in refs:
        if func is not None and row[4] and int(row[4], 16) != func:
            continue
        if chunk is not None and int(row[3]) != chunk:
            continue
        print("\t".join(row))
        n += 1
    print("%d row(s)" % n, file=sys.stderr)
    return 0


def selftest():
    index, lit, refs, deltas, chunks, funcs, lit_addrs = scan()
    assert chunks == 2228 and funcs == 119757, (chunks, funcs)
    assert index[0x1438734D0]["text"] == "No Failure"
    assert index[0x1438734D0]["hits"] > 0
    assert sum(1 for r in index.values() if r["source"] == "rdata") == 16832
    assert any(k[0] == 0x1438734D0 and k[1] == 749 for k in refs)
    assert index[0x143051000]["text"] == "Overview"
    assert index[0x143051000]["ptr"] > 0
    assert any(k[0] == 0x143051000 and k[1] == 437 for k in refs)
    assert ("0x75F23B41", 0) in lit
    assert any(k[0] == ("0x75F23B41", 0) and k[1] == 744 for k in refs)
    assert cunescape(r"\n\t\\\"") == '\n\t\\"'
    assert esc('a\tb\\c') == 'a\\tb\\\\c'
    assert esc("\x01") == "\\x01"
    print("selftest OK: %d strings, %d literals, %d refs" % (len(index), len(lit), len(refs)))


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--find", metavar="REGEX", help="search the generated index")
    ap.add_argument("--addr", metavar="0xADDR", help="one string and its references")
    ap.add_argument("--func", metavar="0xADDR", help="strings a function references")
    ap.add_argument("--chunk", metavar="N", help="strings a chunk references")
    ap.add_argument("--selftest", action="store_true", help="scan and check known rows")
    a = ap.parse_args(argv)
    if a.selftest:
        selftest()
        return 0
    if a.find or a.addr or a.func or a.chunk:
        if a.addr:
            return cmd_addr(a.addr)
        if a.find:
            return cmd_find(a.find)
        return cmd_refs(a)
    index, lit, refs, deltas, chunks, funcs, lit_addrs = scan()
    write(index, lit, refs, deltas, lit_addrs)
    summary(index, lit, refs, deltas, chunks, funcs)
    print("\nwrote %s\n      %s\n      %s" % (OUT_INDEX, OUT_LITERALS, OUT_REFS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
