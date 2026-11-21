"""Pick the next pass's chunk range from post-strip sizes. stdlib only.

usage (from work/flood/):
  python scripts/pass_next.py                    # start = state.json next_chunk, max 1200 KiB
  python scripts/pass_next.py 230                # explicit start chunk
  python scripts/pass_next.py chunk_0230.txt     # same
  python scripts/pass_next.py 230 --max 900      # cap in KiB, post-strip

Fills chunks in entry order while they fit under the cap, so the pass is size-targeted, not
a fixed count: post-strip chunks run 9-580 KB, not 140 KB. The printed range never exceeds
--max KiB: the chunk that would cross the cap is left for the next pass. Read-only —
state.json is read for next_chunk, never written; --update advances it.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FLOOD = os.path.dirname(HERE)
DEFAULT_MAX = 1200             # KiB, post-strip
ADDR = re.compile(r'// ([0-9a-f]{16})_')


def die(msg):
    sys.exit('pass_next: ' + msg)


def parse_start(arg, chunks):
    name = os.path.basename(arg)
    if name.endswith('.txt'):
        name = name[:-4]
    if name.startswith('chunk_'):
        name = name[6:]
    if not name.isdigit():
        die('cannot read start chunk %r (want 230, chunk_0230 or chunk_0230.txt)' % arg)
    n = int(name)
    if n >= len(chunks):
        die('chunk %d does not exist (corpus has 0..%d)' % (n, len(chunks) - 1))
    return n


def chunk_addr(entry, key):
    m = ADDR.search(entry[key])
    if not m:
        die('no function header in index.json %s for chunk %d' % (key, entry['chunk']))
    return '0x%x' % int(m.group(1), 16)


def main():
    argv = sys.argv[1:]
    max_kb, start_arg, i = DEFAULT_MAX, None, 0
    while i < len(argv):
        a = argv[i]
        if a in ('-m', '--max'):
            if i + 1 >= len(argv):
                die('--max needs a value in KiB')
            a = '--max=' + argv[i + 1]
            i += 1
        if a.startswith('--max='):
            try:
                max_kb = int(a.split('=', 1)[1])
            except ValueError:
                die('--max needs a whole number of KiB, got %r' % a.split('=', 1)[1])
            if max_kb < 1:
                die('--max must be at least 1 KiB')
            i += 1
        elif a in ('-h', '--help'):
            print(__doc__.strip())
            return
        elif a.startswith('-'):
            die('unknown option %r' % a)
        else:
            if start_arg is not None:
                die('more than one start chunk given (%r, %r)' % (start_arg, a))
            start_arg = a
            i += 1

    with open(os.path.join(FLOOD, 'index.json'), encoding='utf-8') as f:
        chunks = json.load(f)['chunks']
    with open(os.path.join(FLOOD, 'state.json'), encoding='utf-8') as f:
        next_chunk = json.load(f)['next_chunk']

    lo = parse_start(start_arg, chunks) if start_arg is not None else next_chunk
    if not 0 <= lo < len(chunks):
        die('state.json next_chunk %d is outside 0..%d' % (lo, len(chunks) - 1))

    max_bytes = max_kb * 1024
    total, hi = chunks[lo]['bytes'], lo
    while hi + 1 < len(chunks) and total + chunks[hi + 1]['bytes'] <= max_bytes:
        hi += 1
        total += chunks[hi]['bytes']

    first, last = chunk_addr(chunks[lo], 'first'), chunk_addr(chunks[hi], 'last')
    if total > max_bytes:
        tail = 'chunk_{:04d} alone is over the cap; kept (a pass needs one chunk)'.format(lo)
    elif hi + 1 < len(chunks):
        tail = '+{:,} B headroom; chunk_{:04d} (+{:,} B) would cross'.format(
            max_bytes - total, hi + 1, chunks[hi + 1]['bytes'])
    else:
        tail = 'corpus ends here'
    print('== next pass ==')
    print('chunks  %04d..%04d (%d)  chunks/chunk_%04d.txt .. chunks/chunk_%04d.txt'
          % (lo, hi, hi - lo + 1, lo, hi))
    print('bytes   {:,} post-strip (max {:,} KiB = {:,} B; {})'
          .format(total, max_kb, max_bytes, tail))
    print('text    %s-%s' % (first, last))
    print('measure python scripts/pass_measure.py %d %d' % (lo, hi))
    print('gaps    python scripts/gap_report.py %d %d' % (lo, hi))
    print('record  ranges/%s-%s.md' % (first, last))
    print('next    state.json.next_chunk becomes %d after --update' % (hi + 1))

    if lo != next_chunk:
        if lo < next_chunk:
            print('note    start %d is BEFORE state.json.next_chunk %d: %d chunk(s) already '
                  'counted (do not --update them again)' % (lo, next_chunk, next_chunk - lo))
        else:
            print('note    start %d is AFTER state.json.next_chunk %d: %d chunk(s) between them '
                  'not counted yet' % (lo, next_chunk, lo - next_chunk))
    else:
        print('note    start %d agrees with state.json.next_chunk' % lo)

    bad = ['chunk_%04d' % i for i in range(lo, hi + 1)
           if chunks[i]['bytes'] != os.path.getsize(os.path.join(FLOOD, 'chunks',
                                                                 'chunk_%04d.txt' % i))]
    if bad:
        print('warning index.json size mismatch on %d chunk(s), first %s; rerun the strip/index '
              'build before trusting these bytes' % (len(bad), bad[0]))


if __name__ == '__main__':
    main()
