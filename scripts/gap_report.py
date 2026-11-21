#!/usr/bin/env python3
"""Classify the inter-entry gaps of a pass range. stdlib only.

usage (from work/flood/):
  python scripts/gap_report.py FIRST LAST      # chunk numbers, as pass_next.py prints them
  python scripts/gap_report.py FIRST LAST --check     # report, then assert the bookkeeping
  python scripts/gap_report.py FIRST LAST --offcuts   # + corpus sweep: offcut body or hole?

Every adjacent pair of decompiled entries leaves a gap `next_entry - (addr + size)`. Before
recording one (PROTOCOL.md; CODE_MAP ledgers 24/30/31/39) know which kind it is:

  padding  <= 16 B          alignment between two functions
  size=    17 B .. 1 KiB    the declared `size=` under-reports the body (halt_baddata etc.)
  giant    > 1 KiB, and the previous function's own decompiled text references an address
           inside the gap (`LAB_…`, `(ram,0x…)`, `&UNK_…`): the gap is its tail, `size=`
           collapsed. `reach 0x…` is the last own address inside the gap, `open` is what is
           left after it; `+offcut` marks other code that also names an address in that tail.
  offcut   > 1 KiB, no own tail, but other text in the range calls or names an address
           inside the span (`func_0x…`, `FUN_…`, a bare `0x…` literal): a body that exists
           but that Ghidra never emitted as a function. `offcut 0x…` is the first such
           address (a call target when there is one).
  hole     > 1 KiB, nothing in the range references the span. References come from this
           range's own text only, so a reference from an unread chunk would not be seen;
           --offcuts lifts that limit (below).

`--offcuts` answers the one question the range-only report cannot: is a >1 KiB span an
**offcut body** (code that exists in the binary but was never emitted as a function) or a
**hole**, when the only reference to it comes from a chunk outside the range? It sweeps all
chunks with the same three forms the range report uses (`FUN_`/`func_0x0…` call names,
`LAB_`/`ram,0x` labels, bare `0x…` literals), diffs every referenced
address against every decompiled entry in the corpus (a header scan; `index.json` carries
only each chunk's first/last), and reclassifies each big gap: `giant` (own tail), `filed`
(every reference is a decompiled entry elsewhere), `offcut` (referenced, no entry anywhere),
`hole` (referenced by nothing). Pass 34 (307-314): the range-only report calls
`0x1406c5b10->0x1406c5fd0` (1,111 B) a hole, but chunk 0535's `FUN_1406c5ba0(...)` makes it
an offcut; `0x1406ac0e0->0x1406ad5e0` stays a hole (0 references corpus-wide).

`window reach` is the far-window watch list (ledger 53). For every entry, the highest address its
own body stamps — labels, `(ram,0x…)`, literals, but not `FUN_`/`func_0x…` calls — past its
declared `size=`, minus its entry address; stamps above the corpus's highest entry (`index.json`)
are data, not `.text`, and are ignored. An entry with >= 3 such stamps is a window (one or two
stray literals are not); the three furthest are printed. A window's stamps point at unread
regions, never at this range's coverage.

A pair whose next entry starts at or below `addr + size` is an overlap, not a gap, and is
only counted. Chunk entry lists are globally address-sorted and unique, so an address
strictly inside a gap has no decompiled entry anywhere: the references above are missing
bodies, not functions filed in another chunk. Chunk boundaries are included.

Pass 30 (chunks 267-275): 520 entries, 13 gaps > 1 KiB / 195,056 B = 3 giant + 6 offcut +
4 hole. The largest, `0x1405E4210->0x140608160` (146,416 B), is giant+offcut with
`reach 0x1405E46B2`: only its first 0x4A2 B is that function's own text, and the rest is
unreferenced. Pass 33 (295-306): 198 entries, 18 gaps > 1 KiB / 53,215 B = 12 giant +
6 offcut, 0 hole; `FUN_1406815F0` reaches 0x140683A9A, matching the hand read.

Read-only, standard library only, no paths outside this repository.
"""
import bisect
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pass_measure  # noqa: E402  chunk parsing (functions) + declared sizes + headers

CHUNKS = os.path.join(os.path.dirname(HERE), 'chunks')
INDEX = os.path.join(os.path.dirname(HERE), 'index.json')

# `FUN_...` catches thunks too; the 0* prefix covers the 12-digit `func_0x0001406…` names.
RE_CALL = re.compile(r'(?:func_0x0*|thunk_FUN_|FUN_)([0-9a-f]{9,16})')
# own labels: LAB_x, `(ram,0x…)` overlap warnings, code_r0x…/switchD_…/joined_r0x…
RE_LABEL = re.compile(r'(?:LAB_|ram,0x0*|code_r0x0*|switchD_0*|joined_r0x0*)([0-9a-f]{9,16})')
RE_LIT = re.compile(r'(?<![0-9a-zA-Z_])0x0*([0-9a-f]{9,16})')


def refs(text):
    """{va: {form}} for every .text VA mentioned, form in label/call/lit."""
    out = {}
    for form, rx in (('label', RE_LABEL), ('call', RE_CALL), ('lit', RE_LIT)):
        for m in rx.finditer(text):
            v = int(m.group(1), 16)
            if 0x140000000 <= v < 0x150000000:
                out.setdefault(v, set()).add(form)
    return out


def scan(lo, hi):
    ents, own = {}, {}
    for n in range(lo, hi + 1):
        with open(os.path.join(CHUNKS, 'chunk_%04d.txt' % n), encoding='utf-8',
                  errors='replace') as fh:
            text = fh.read()
        for addr, _name, _decl, size, body in pass_measure.functions(text):
            a = int(addr, 16)
            if a not in ents:
                ents[a] = size
                own[a] = refs(body)
    return ents, own


def text_hi():
    """Highest entry address in the corpus: `.text` ends at or below it (index.json is truth)."""
    with open(INDEX) as f:
        return max(int(re.match(r'// ([0-9a-f]{16})_', c['last']).group(1), 16)
                   for c in json.load(f)['chunks'])


def report(lo, hi):
    ents, own = scan(lo, hi)
    entries = sorted(ents)
    every = {}
    for fs in own.values():
        for v, forms in fs.items():
            every.setdefault(v, set()).update(forms)

    pairs = list(zip(entries, entries[1:]))
    spans = [(a, b, b - (a + ents[a])) for a, b in pairs]
    gaps = [g for g in spans if g[2] > 0]
    overlaps = len(spans) - len(gaps)

    buckets = {'padding': [], 'size=': [], 'giant': [], 'offcut': [], 'hole': []}
    detail = []
    for a, b, d in gaps:
        first = a + ents[a]
        if d <= 1024:
            buckets['padding' if d <= 16 else 'size='].append((a, b, d))
            continue
        # a `func_0x…` name is a missing entry, not this function's own label: no 'call'
        tail = sorted(v for v in own[a] if first <= v < b and 'call' not in own[a][v])
        lost = sorted(v for v in every if first <= v < b
                      and (v not in own[a] or 'call' in own[a][v]))
        if tail:
            cls, reach = 'giant', tail[-1]
            if lost:
                cls = 'giant+offcut'
        else:
            cls, reach = ('offcut' if lost else 'hole'), None
        if lost:                       # show a call target when there is one, else a literal
            lost = [v for v in lost if 'call' in every[v]] or lost
        buckets[cls.split('+')[0]].append((a, b, d))
        detail.append((a, b, d, cls, reach, lost))

    # far-window watch list: own non-call stamps past size=, .text band only (ledger 53)
    hi_text = text_hi()
    win = []
    for a in entries:
        far = [v for v in own[a] if 'call' not in own[a][v] and a + ents[a] <= v <= hi_text]
        if len(far) >= 3:
            assert min(far) >= a + ents[a] and max(far) <= hi_text
            win.append((max(far) - a, a, max(far), len(far)))
    win.sort(reverse=True)

    span = entries[-1] - entries[0]
    size_sum = sum(ents[a] for a in entries)
    print('== gap_report chunks %04d-%04d ==' % (lo, hi))
    print('range: 0x%x-0x%x   entries=%d  span=%d  sum_size (binary)=%d (%.1f%%)'
          % (entries[0], entries[-1], len(entries), span, size_sum, 100.0 * size_sum / span))
    print('gaps: %d of %d pairs (next entry inside the previous body: %d overlaps)'
          % (len(gaps), len(pairs), overlaps))
    for name in ('padding', 'size='):
        b = buckets[name]
        print('  %-8s %5d gaps %10d B' % (name, len(b), sum(g[2] for g in b)))
    big = [g for g in gaps if g[2] > 1024]
    print('  >1 KiB   %5d gaps %10d B' % (len(big), sum(g[2] for g in big)))
    for a, b, d, cls, reach, lost in sorted(detail, key=lambda x: -x[2]):
        note = 'reach 0x%x (%d B open)' % (reach, b - reach - 1) if reach else ''
        if lost:
            note += ('  ' if note else '') + 'offcut 0x%x' % lost[0]
        print('    0x%x->0x%x %8d B  %-13s %s' % (a, b, d, cls, note))
    for cls in ('giant', 'offcut', 'hole'):   # 'giant+offcut' counts under giant
        b = buckets[cls]
        print('  %-8s %5d gaps %10d B' % (cls, len(b), sum(g[2] for g in b)))
    print('  window reach: %s' % (' | '.join(
        '0x%x +%d B -> 0x%x (%d stamps)' % (a, d, r, n) for d, a, r, n in win[:3]) or '-'))
    return ents, own, gaps, buckets, entries, detail


def chunk_count():
    with open(INDEX) as f:
        return len(json.load(f)['chunks'])


def sweep(spans):
    """One corpus pass: {va: chunk} entries, {gap_index: {va: [chunk, forms]}} refs."""
    starts = [s for s, _e in spans]
    # the bisect below needs ascending starts; offcuts() passes report()'s address order
    assert all(a < b for a, b in zip(starts, starts[1:])), 'gap spans not ascending'
    ents, hits = {}, {}
    for n in range(chunk_count()):
        with open(os.path.join(CHUNKS, 'chunk_%04d.txt' % n), encoding='utf-8',
                  errors='replace') as fh:
            text = fh.read()
        for h in pass_measure.HDR.finditer(text):
            ents[int(h.group(1), 16)] = n
        for v, forms in refs(text).items():
            i = bisect.bisect_right(starts, v) - 1
            if i >= 0 and v < spans[i][1]:
                hits.setdefault(i, {}).setdefault(v, [n, set()])[1].update(forms)
    assert all(spans[i][0] <= v < spans[i][1] for i, d in hits.items() for v in d),         'a reference landed outside its gap'
    return ents, hits


def offcuts(lo, hi):
    """Reclassify the >1 KiB gaps with a corpus-wide call-reference sweep."""
    ents, own, _gaps, _buckets, _entries, detail = report(lo, hi)
    big = detail                       # ascending by address, as report() built it
    if not big:
        print('--offcuts: no gap > 1 KiB in this range')
        return 0
    all_ents, hits = sweep([(a + ents[a], b) for a, b, _d, _c, _r, _l in big])
    print('== gap_report --offcuts: corpus sweep of %d chunks, %d entries,'
          ' %d referenced addresses =='
          % (chunk_count(), len(all_ents), sum(len(v) for v in hits.values())))
    have, verdict, ext = collections.Counter(), {}, {}
    for i, (a, b, d, cls, _reach, _lost) in enumerate(big):
        # own-body labels are the giant tail, not separate evidence (same rule as report())
        ext[i] = {v: x for v, x in hits.get(i, {}).items()
                  if 'call' in x[1] or v not in own[a]}
        if cls.startswith('giant'):
            verdict[i] = 'giant+offcut' if ext[i] else 'giant'
        elif ext[i] and all(v in all_ents for v in ext[i]):
            verdict[i] = 'filed'
        elif ext[i]:
            verdict[i] = 'offcut'
        else:
            verdict[i] = 'hole'
        have[verdict[i]] += 1
    for i, (a, b, d, cls, reach, _lost) in sorted(enumerate(big), key=lambda x: -x[1][2]):
        r = ext[i]
        note = 'reach 0x%x' % reach if reach else ''
        if r:   # a call target first, then labels/literals
            note += ('  ' if note else '') + ' '.join(
                '0x%x@%04d%s' % (v, r[v][0], '*' if v in all_ents else '')
                for v in sorted(r, key=lambda v: ('call' not in r[v][1], v))[:3])
            if len(r) > 3:
                note += ' +%d' % (len(r) - 3)
        print('    0x%x->0x%x %8d B  %-12s -> %-12s %s'
              % (a, b, d, cls, verdict[i], note))
    only = collections.Counter(c.split('+')[0] for _a, _b, _d, c, _r, _l in big)
    print('  range-only: %s'
          % ', '.join('%s %d' % (k, only[k]) for k in ('giant', 'offcut', 'hole') if only[k]))
    print('  corpus:     %s   (* = a decompiled entry at that address)'
          % ', '.join('%s %d' % (k, have[k]) for k in
                      ('giant', 'giant+offcut', 'filed', 'offcut', 'hole') if have[k]))
    return 0


def check(lo, hi):
    ents, own, gaps, buckets, entries, _detail = report(lo, hi)
    hdr = 0
    for n in range(lo, hi + 1):
        with open(os.path.join(CHUNKS, 'chunk_%04d.txt' % n), encoding='utf-8',
                  errors='replace') as fh:
            hdr += len(re.findall(r'(?m)^// [0-9a-f]{16}_', fh.read()))
    assert len(entries) == len(set(entries)), 'entry list not unique'
    assert entries == sorted(entries), 'entry list not sorted'
    assert len(entries) <= hdr, 'more entries than function headers'
    seen = collections.Counter()
    for cls, b in buckets.items():
        for a, bb, d in b:
            seen[a] += 1
            assert d == bb - (a + ents[a]) and d > 0, (cls, hex(a))
            assert (cls == 'padding') == (d <= 16), (cls, hex(a), d)
            assert (cls == 'size=') == (16 < d <= 1024), (cls, hex(a), d)
            if cls == 'giant':
                first = a + ents[a]
                assert any(first <= v < bb and 'call' not in own[a][v] for v in own[a]), hex(a)
    assert set(seen) == {a for a, _b, _d in gaps} and max(seen.values()) == 1
    total = sum(g[2] for g in gaps)
    assert sum(sum(g[2] for g in b) for b in buckets.values()) == total
    print('check: OK  (%d entries, %d gaps, %d B)' % (len(entries), len(gaps), total))
    return 0


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    if len(args) < 2 or '--help' in argv or '-h' in argv:
        print(__doc__.strip())
        return 2
    lo, hi = int(args[0]), int(args[1])
    if '--check' in argv:
        return check(lo, hi)
    if '--offcuts' in argv:
        return offcuts(lo, hi)
    report(lo, hi)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
