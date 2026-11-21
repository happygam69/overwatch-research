#!/usr/bin/env python3
"""Corpus-wide symbol cross-reference: which functions mention a symbol. stdlib only.

usage (from work/flood/):
  python scripts/crossref.py FUN_1406c5ba0
  python scripts/crossref.py 0x1406c5ba0 143b94 143b95
  python scripts/crossref.py DAT_143851c90 --chunks
  python scripts/crossref.py --regex 'func_0x000142454[0-9a-f]+'
  python scripts/crossref.py --check                # assert the spelling and range rules

A symbol that ends in a hex run is searched as that address, not as its spelling:
`0x1406c5ba0`, `FUN_1406c5ba0`, `func_0x0001406c5ba0`, `DAT_1406c5ba0` and a bare
`0x1406c5ba0` literal are one query. The run is a prefix (leading zeros ignored, no right
boundary), so `143b94` covers the band `0x143b945b8`-`0x143b9c5c0` and a 64-bit base
`0x18317a531d116c` finds its `+…6c0c+off` uses. Symbols without a hex run are plain substrings.

Per symbol it prints the entry that defines it (the `// <addr>_<name>` header, when the
corpus has one), one line per referencing function `chunk_NNNN 0x<addr> <name> x<hits>`,
then the referencing chunks as a compact list. `--chunks` prints only that list (no
per-function attribution); `--max N` caps the function lines (default 60, 0 = all). Exit
code 1 when a symbol matched nothing.

This is the "grep forward for X" query of CODE_MAP's open threads (2, 9, 11, 17) over all
chunks at once, so a thread update is one command, not a hand-picked range.

Read-only, standard library only, no paths outside this repository.
"""
import bisect
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pass_measure  # noqa: E402  header regex, chunk paths

HDR = pass_measure.HDR
HEXTAIL = re.compile(r'(?i)([0-9a-f]{4,16})$')
WRAPPER = re.compile(r'(?i)(?:[a-z]+_)?(?:0x)?0*')


def n_chunks():
    with open(os.path.join(pass_measure.FLOOD, 'index.json')) as f:
        return len(json.load(f)['chunks'])


def pattern(sym, regex=False):
    """Search regex for one symbol; see the module docstring for the spelling rules."""
    if regex:
        return re.compile(sym)
    m = HEXTAIL.search(sym)
    if m and WRAPPER.fullmatch(sym[:m.start()]):
        # prefix match: 143b94 -> 143b945b8, 18317a531d116c -> 18317a531d116c0c
        return re.compile(r'(?<![1-9a-f])%s' % (m.group(1).lstrip('0') or '0'), re.I)
    return re.compile(re.escape(sym))


def compact(nums):
    """[305, 308, 309, 310] -> '0305, 0308-0310'."""
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append('%04d' % nums[i] if i == j else '%04d-%04d' % (nums[i], nums[j]))
        i = j + 1
    return ', '.join(out) or '-'


def scan(rx, chunks, attribute=True):
    """({chunk: [(addr, name, hits)]}, [(chunk, addr, name)]) over the given chunks.

    With attribute=False only the referencing chunks are collected, as {chunk: []}.
    A match on a function's own header line counts as that entry's definition, not a hit.
    """
    found, defs = {}, []
    for n in chunks:
        with open(pass_measure.chunk_path(n), encoding='utf-8', errors='replace') as f:
            text = f.read()
        if not rx.search(text):
            continue
        if not attribute:
            found[n] = []
            continue
        hdrs = [(h.start(), h.end(), int(h.group(1), 16), h.group(2))
                for h in HDR.finditer(text)]
        starts = [h[0] for h in hdrs]
        counts = {}
        for m in rx.finditer(text):
            i = bisect.bisect_right(starts, m.start()) - 1
            if i < 0:
                continue
            _s0, _e0, a, name = hdrs[i]
            if text.startswith('//', text.rfind('\n', 0, m.start()) + 1):
                defs.append((n, a, name))      # header/meta line: this entry's own name
                continue
            counts[a] = counts.get(a, 0) + 1
        if counts:
            names = {a: name for _s, _e, a, name in hdrs}
            found[n] = [(a, names[a], c) for a, c in sorted(counts.items())]
    return found, defs


def check():
    """Assert the spelling rules and chunk-list compaction on known inputs."""
    assert compact([]) == '-' and compact([1, 2, 3, 5]) == '0001-0003, 0005'
    assert pattern('0x1406c5ba0').pattern == r'(?<![1-9a-f])1406c5ba0'
    assert pattern('FUN_1406c5ba0').pattern == pattern('func_0x0001406c5ba0').pattern
    assert pattern('FUN_1406c5ba0').search('call FUN_1406c5ba0(x)')
    assert not pattern('FUN_1406c5ba0').search('FUN_11406c5ba0')       # left hex boundary
    assert pattern('143b94').search('_DAT_143b945b8')                  # band prefix
    assert pattern('0x18317a531d116c').search('+ 0x18317a531d116c0c')  # 64-bit base + offset
    assert pattern('pool').search('swimming pool')
    print('check: OK')
    return 0


def main(argv):
    opts = {'regex': False, 'chunks': False, 'max': 60}
    syms = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--regex':
            opts['regex'] = True
        elif a == '--chunks':
            opts['chunks'] = True
        elif a == '--check':
            return check()
        elif a == '--max':
            i += 1
            if i == len(argv):
                print('crossref: --max needs a number')
                return 2
            opts['max'] = int(argv[i])
        elif a in ('-h', '--help'):
            print(__doc__.strip())
            return 0
        elif a.startswith('--'):
            print('crossref: unknown option %r' % a)
            return 2
        else:
            syms.append(a)
        i += 1
    if not syms:
        print(__doc__.strip())
        return 2

    chunks = range(n_chunks())
    empty = 0
    for sym in syms:
        found, defs = scan(pattern(sym, opts['regex']), chunks, not opts['chunks'])
        rows = [(n, a, name, c) for n in sorted(found) for a, name, c in found[n]]
        print('== crossref %s ==' % sym)
        for n, a, name in list(dict.fromkeys(defs))[:4]:
            print('def: chunk_%04d 0x%x %s' % (n, a, name))
        for n, a, name, c in (rows[:opts['max']] if opts['max'] else rows):
            print('  %04d 0x%x %-24s x%d' % (n, a, name, c))
        if opts['max'] and len(rows) > opts['max']:
            print('  ... +%d more functions (--max 0 for all)' % (len(rows) - opts['max']))
        print('chunks: %s   (%d chunks%s)'
              % (compact(sorted(found)), len(found),
                 ', %d functions, %d hits' % (len(rows), sum(r[3] for r in rows))
                 if rows else ''))
        empty += not found
    return 1 if empty else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
