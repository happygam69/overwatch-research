"""Canonical per-pass measurement over flood chunks. stdlib only.

usage (from work/flood/):
  python scripts/pass_measure.py START END           # measure only, prints the block
  python scripts/pass_measure.py START END --json    # read-only: the same facts as JSON + digest
  python scripts/pass_measure.py START END --update  # measure + merge into state.json
  python scripts/pass_measure.py --init A B          # rebuild state.json from chunks A..B
  python scripts/pass_measure.py --maxscan           # rank the whole corpus by text size, seed state.json

Output is the reproducible 'headline numbers' block for the pass record: quote it
verbatim; hand-typed numbers in records are not acceptable (PROTOCOL.md). `--json` prints
those facts as one object plus a `digest` (16 hex) a record may cite instead of pasting the
block; the digest covers the range facts only, so it does not move when state.json's
`max_text` does (`corpus_max` is printed alongside but excluded from the hash).

The block's `largest (text):` / `corpus max:` lines rank functions by the declared `(NNNN B)`
decompiled-text size and compare the range's biggest against the corpus maximum kept in
state.json (`--maxscan` seeds/refreshes it; `--init` wipes it, so re-run `--maxscan` after
a rebuild), so "is this the corpus maximum" is read, not hand-grepped (ledgers 37/38/47).
`sum_size (binary)` sums the binary `size=` header field instead; on stripped window bodies
text exceeds binary, so the two are not comparable.
A NEW max is a claim to verify against overlapping windows, not a result:
`scripts/crossref.py <addr>` lists every chunk that names the same body. The block prints
that check for the range max as a `max refs:` line (thread 20, ledgers 47/49), so every
pass carries it without a separate command.

Classification per function (first match wins):
  reg      calls func_0x1421cd360 (registration)
  record   calls func_0x1421c2d50 ({id,hash} row)
  atexit   calls func_0x1421c7880 (nested-atexit builder)
  sorted   >=2 inline decryptor calls (sorted-insert builder)
  builder  exactly 1 inline decryptor call
  wrapper  c2d70 + d4fb0, no decryptor
  other    everything else
"""
import collections
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FLOOD = os.path.dirname(HERE)
STATE = os.path.join(FLOOD, 'state.json')

HDR = re.compile(r'^// ([0-9a-f]{16})_(\S+)\s+\((\d+) B\)', re.M)
META = re.compile(r'^// ([0-9a-f]+) \S+ size=(\d+) callers', re.M)
REG = re.compile(r'func_0x0001421cd360\((.*?)\);', re.S)
DEC = re.compile(r'func_0x0001421(d4f30|d4f70)\((.*?)\);', re.S)
C2D50 = re.compile(r'func_0x0001421c2d50\((.*?)\);', re.S)
STORE = re.compile(r'^\s*(_?DAT_[0-9a-f]+) = (.+);', re.M)
CTXT = re.compile(r'\bDAT_1438[0-9a-f]{6}\b')
FUNREF = re.compile(r'\bFUN_[0-9a-f]{9,12}\b')


def chunk_path(n):
    return os.path.join(FLOOD, 'chunks', 'chunk_%04d.txt' % n)


def functions(text):
    """Yield (addr, name, declared_bytes, size, body) per function."""
    parts = re.split(r'(?m)^(?=// [0-9a-f]{16}_)', text)
    for p in parts:
        m = HDR.match(p)
        if not m:
            continue
        mm = META.search(p)
        yield ('0x%x' % int(m.group(1), 16), m.group(2), int(m.group(3)),
               int(mm.group(2)) if mm else 0, p)


def classify(body):
    if 'func_0x0001421cd360' in body:
        return 'reg'
    if 'func_0x0001421c2d50' in body:
        return 'record'
    if 'func_0x0001421c7880' in body:
        return 'atexit'
    n = len(DEC.findall(body))
    if n >= 2:
        return 'sorted'
    if n == 1:
        return 'builder'
    if 'func_0x0001421c2d70' in body and 'func_0x0001421d4fb0' in body:
        return 'wrapper'
    return 'other'


def arg_list(s):
    return [a.strip() for a in s.split(',')]


def measure(lo, hi):
    m = {
        'chunks': hi - lo + 1, 'files': 0, 'sum_size': 0, 'disk': 0,
        'classes': collections.Counter(), 'sizes': collections.Counter(),
        'calls': collections.Counter(),
        'reg_hashes': [], 'reg_flags': collections.Counter(), 'reg_align': collections.Counter(),
        'reg_sizes': collections.Counter(), 'reg_tokens': collections.Counter(),
        'reg_outs': [], 'reg_argc_bad': 0,
        'dec_hashes': collections.defaultdict(collections.Counter),
        'records': [], 'roots': collections.Counter(), 'ctxt': [],
        'first': None, 'last': None, 'runs': [], 'targets': collections.Counter(),
        'big': [],
    }
    prev_class = None
    for n in range(lo, hi + 1):
        with open(chunk_path(n), encoding='utf-8', errors='replace') as f:
            text = f.read()
        m['disk'] += len(text)
        for addr, name, decl, size, body in functions(text):
            m['big'].append((decl, addr, name, n))
            m['files'] += 1
            m['sum_size'] += size
            m['first'] = m['first'] or addr
            m['last'] = addr
            cls = classify(body)
            m['classes'][cls] += 1
            m['sizes'][size] += 1
            if cls != prev_class:
                m['runs'].append([addr, addr, cls, 1])
                prev_class = cls
            else:
                m['runs'][-1][1] = addr
                m['runs'][-1][3] += 1
            for kw in ('1426c3bcc', '1426c3d40', '140f80f80', '140548d00', '14053a070',
                      '140548f80', '_Init_thread_footer'):
                m['calls'][kw] += body.count('FUN_' + kw if kw[0].isdigit() else kw)
            for fn in FUNREF.findall(body):
                m['targets'][fn] += 1
            for t in CTXT.findall(body):
                m['ctxt'].append(t)
            # registrations
            for call in REG.finditer(body):
                args = arg_list(call.group(1))
                if len(args) != 18:
                    m['reg_argc_bad'] += 1
                    continue
                h = '0x%x' % int(args[2], 16)
                m['reg_hashes'].append(h)
                m['reg_flags'][args[6]] += 1
                m['reg_align'][args[5]] += 1
                m['reg_sizes'][args[4]] += 1
                if args[8] != '0':
                    m['reg_tokens'][args[8]] += 1
                out = re.match(r'&DAT_([0-9a-f]+)', args[0])
                if out:
                    m['reg_outs'].append(int(out.group(1), 16))
            # inline decryptor calls + hashes
            for dec in DEC.finditer(body):
                args = arg_list(dec.group(2))
                m['dec_hashes'][dec.group(1)][args[2].lower() if len(args) > 2 else '?'] += 1
            # {id,hash} records: literal stores feeding c2d50
            for rec in C2D50.finditer(body):
                args = arg_list(rec.group(1))
                src = re.match(r'&DAT_([0-9a-f]+)', args[1] if len(args) > 1 else '')
                if not src:
                    continue
                s = int(src.group(1), 16)
                vals = {}
                for st in STORE.finditer(body):
                    t = st.group(1).lstrip('_')
                    if t.startswith('DAT_'):
                        a = int(t[4:], 16)
                        if a - s in (0, 4, 8):
                            try:
                                vals[a - s] = int(st.group(2).rstrip(';').strip(), 0)
                            except ValueError:
                                pass
                if 0 in vals and 4 in vals:
                    m['records'].append({'id': vals[0], 'hash': '0x%x' % vals[4],
                                         'third': vals.get(8, 0)})
            # class-root census: first store whose RHS is a &-pointer, non-reg/record fns
            if cls in ('wrapper', 'builder', 'atexit', 'sorted'):
                for st in STORE.finditer(body):
                    if st.group(2).startswith('&'):
                        m['roots'][st.group(2)] += 1
                        break
            for call, name in (('func_0x0001421c2d70', 'c2d70'),
                               ('func_0x0001421d4fb0', 'd4fb0'),
                               ('func_0x0001421c2d50', 'c2d50'),
                               ('func_0x0001421c7880', 'c7880')):
                m['calls'][name] += body.count(call)
            m['calls']['atexit'] += body.count('atexit(')
        prev_class = None  # runs do not span chunk boundaries
    m['big'].sort(reverse=True)
    m['maxrefs'] = max_refs(m)
    return m


def max_refs(m):
    """Corpus-wide mentions of the range max: a second entry naming it is a window/cascade signal."""
    if not m['big']:
        return {'name': None, 'def': [], 'others': [], 'other_count': 0}
    _d, addr, name, _n = m['big'][0]
    import crossref                       # imports this module; safe only after it is loaded
    found, defs = crossref.scan(crossref.pattern('0x' + addr[2:]), range(crossref.n_chunks()))
    others = sorted([n, '0x%x' % a, nm, c]
                    for n, rows in found.items() for a, nm, c in rows
                    if '0x%x' % a != addr)
    return {'name': name, 'def': sorted({n for n, _a, _nm in defs}),
            'others': others[:10], 'other_count': len(others)}


def largest(lo, hi, top):
    """[(declared_bytes, addr, name, chunk)] ranked by declared text size."""
    out = []
    for n in range(lo, hi + 1):
        with open(chunk_path(n), encoding='utf-8', errors='replace') as f:
            for h in HDR.finditer(f.read()):
                out.append((int(h.group(3)), '0x%x' % int(h.group(1), 16), h.group(2), n))
    out.sort(reverse=True)
    return out[:top]


def fmt_max(m, corpus):
    """The corpus-max line: stored maximum + this range's biggest against it."""
    top = m['big'][0] if m['big'] else None
    if not corpus:
        return 'corpus max: unknown - seed it: python scripts/pass_measure.py --maxscan'
    if top and top[0] > corpus['bytes']:
        return ('corpus max: NEW %s %d B (chunk %04d); was %s %d B (chunk %04d) -'
                ' rule out an overlapping window (ledger 47) via the max refs line below'
                % (top[2], top[0], top[3], corpus['name'], corpus['bytes'], corpus['chunk']))
    return ('corpus max: %s %d B (chunk %04d)%s'
            % (corpus['name'], corpus['bytes'], corpus['chunk'],
               '  [range max = %.1f%% of it]' % (100.0 * top[0] / corpus['bytes'])
               if top else ''))


def fmt_refs(m):
    """The range max's corpus-wide references: its own entries vs other functions naming it."""
    r = m['maxrefs']
    if not r['name']:
        return 'max refs: -'
    head = 'max refs: %s def chunk %s, ' % (
        r['name'], ','.join('%04d' % n for n in r['def']) or '-')
    if not r['other_count']:
        return head + 'no other fn names it'
    rows = ', '.join('%04d %s %s x%d' % tuple(o) for o in r['others'][:3])
    more = '' if r['other_count'] <= 3 else ' +%d' % (r['other_count'] - 3)
    return head + '%d other fn(s) name it: %s%s' % (r['other_count'], rows, more)


def facts(m, lo, hi):
    """Everything a record cites, canonical for hashing (no state-derived fields)."""
    return {
        'chunks': [lo, hi],
        'range': [m['first'], m['last']],
        'files': m['files'], 'sum_size': m['sum_size'], 'disk': m['disk'],
        'largest': [[name, d, n] for d, _a, name, n in m['big'][:3]],
        'max_refs': m['maxrefs'],
        'classes': dict(m['classes']),
        'sizes': [[k, v] for k, v in m['sizes'].most_common(24)],
        'calls': dict(m['calls']),
        'registrations': {
            'calls': len(m['reg_hashes']), 'distinct': len(set(m['reg_hashes'])),
            'argc_bad': m['reg_argc_bad'],
            'flags': dict(m['reg_flags']), 'align': dict(m['reg_align']),
            'sizes': dict(m['reg_sizes']), 'tokens': dict(m['reg_tokens'].most_common(6)),
            'outputs': [min(m['reg_outs']), max(m['reg_outs'])] if m['reg_outs'] else None},
        'decryptors': {d: {'uses': sum(m['dec_hashes'][d].values()),
                           'top': dict(m['dec_hashes'][d].most_common(8))}
                       for d in ('d4f30', 'd4f70')},
        'records': m['records'],
        'roots': dict(m['roots'].most_common(12)),
        'ciphertext_band': [min(m['ctxt']), max(m['ctxt'])] if m['ctxt'] else None,
        'targets': dict(m['targets'].most_common(12)),
        'runs': m['runs'],
    }


def mdigest(f):
    """16-hex provenance hash over the citable facts (corpus_max excluded: it moves with state)."""
    blob = json.dumps(f, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def census(counter, top=10, fmt=str):
    return ' '.join('%s x%d' % (fmt(k), v) for k, v in counter.most_common(top))


def fmt_out(m, corpus=None):
    L = []
    A = L.append
    A('== pass_measure chunks %04d-%04d ==' % (lo, hi))
    A('range: %s-%s   files=%d  sum_size (binary)=%d  disk=%d (post-strip)'
      % (m['first'], m['last'], m['files'], m['sum_size'], m['disk']))
    A('largest (text): %s' % (' | '.join('%s %d B (chunk %04d)' % (name, d, n)
                                 for d, _a, name, n in m['big'][:3]) or '-'))
    A(fmt_max(m, corpus))
    A(fmt_refs(m))
    A('classes: %s' % ' '.join('%s=%d' % (k, v) for k, v in m['classes'].most_common()))
    A('size census: %s' % ' '.join('%dx%d' % (k, v) for k, v in m['sizes'].most_common(24)))
    A('calls: cd360 x%d  1426c3bcc x%d  canary x%d  d4f30 x%d  d4f70 x%d  d4fb0 x%d  '
      'c2d70 x%d  c2d50 x%d  c7880 x%d  atexit x%d  140f80f80 x%d'
      % (len(m['reg_hashes']), m['calls']['1426c3bcc'], m['calls']['1426c3d40'],
         sum(m['dec_hashes']['d4f30'].values()), sum(m['dec_hashes']['d4f70'].values()),
         m['calls']['d4fb0'], m['calls']['c2d70'], m['calls']['c2d50'], m['calls']['c7880'],
         m['calls']['atexit'], m['calls']['140f80f80']))
    if m['reg_argc_bad']:
        A('WARNING: %d cd360 calls did not have 18 args — census incomplete' % m['reg_argc_bad'])
    A('registrations: %d calls, %d distinct hashes (zero-reuse: %s)'
      % (len(m['reg_hashes']), len(set(m['reg_hashes'])),
         'OK' if len(set(m['reg_hashes'])) == len(m['reg_hashes']) else 'VIOLATED'))
    A('  flags: %s | align: %s' % (census(m['reg_flags']), census(m['reg_align'])))
    A('  sizes: %s' % ' '.join('%sx%d' % (k, v) for k, v in m['reg_sizes'].most_common(12)))
    toks = m['reg_tokens']
    A('  nonzero tokens: %d uses / %d distinct; top: %s'
      % (sum(toks.values()), len(toks), census(toks, 6)))
    if m['reg_outs']:
        A('  outputs: 0x%x..0x%x' % (min(m['reg_outs']), max(m['reg_outs'])))
    for d in ('d4f30', 'd4f70'):
        c = m['dec_hashes'][d]
        A('  %s hashes: %d uses / %d distinct; top: %s'
          % (d, sum(c.values()), len(c), census(c, 8)))
    A('records: %d  %s' % (len(m['records']),
                           ' '.join('{0x%x,0x%s%s}' % (r['id'], r['hash'],
                                                      ',0x%x' % r['third'] if r['third'] else '')
                                    for r in m['records'])))
    A('roots (first &-store in builder/wrapper/atexit/sorted): %s' % census(m['roots'], 12))
    if m['ctxt']:
        A('ciphertext band: 0x%s..0x%s (%d refs)'
          % (min(m['ctxt'])[4:], max(m['ctxt'])[4:], len(m['ctxt'])))
    A('top call targets: %s' % census(m['targets'], 12))
    A('zones:')
    for a0, a1, cls, cnt in m['runs']:
        if cnt >= 3 or cls in ('reg', 'record'):
            A('  %s-%s  %s x%d' % (a0, a1, cls, cnt))
    return '\n'.join(L)


def load_state():
    with open(STATE) as f:
        return json.load(f)


def write_state(state):
    with open(STATE, 'w', newline='\n') as f:
        json.dump(state, f, indent=1)


def maxscan():
    """Rank the whole corpus by declared text size and store the maximum."""
    if not os.path.exists(STATE):
        print('max_text: %s missing - run --init or --update first' % STATE)
        return 1
    idx = json.load(open(os.path.join(FLOOD, 'index.json')))
    last = len(idx['chunks']) - 1
    top = largest(0, last, 12)
    print('== pass_measure --maxscan: largest declared text bodies, all %d chunks =='
          % (last + 1))
    print('corpus max: %s %d B (chunk %04d)' % (top[0][2], top[0][0], top[0][3]))
    for i, (d, _a, name, n) in enumerate(top, 1):
        print('%2d. %-24s %7d B  chunk %04d' % (i, name, d, n))
    state = load_state()
    old = state.get('max_text') or {}
    state['max_text'] = {'bytes': top[0][0], 'addr': top[0][1], 'name': top[0][2],
                         'chunk': top[0][3]}
    write_state(state)
    print('[state.json] max_text = %s %d B (chunk %04d; was %s %s B)'
          % (top[0][2], top[0][0], top[0][3], old.get('name', '-'), old.get('bytes', '-')))
    return 0


def main():
    global lo, hi
    argv = sys.argv[1:]
    if '--maxscan' in argv:
        return maxscan()
    rest = [a for a in argv if not a.startswith('--')]
    lo, hi = int(rest[0]), int(rest[1])
    if '--init' in argv:
        mode = 'init'
    else:
        mode = 'update' if '--update' in argv else 'measure'
    if '--json' in argv and mode != 'measure':
        sys.exit('pass_measure: --json is read-only; run --update/--init as a separate call')

    m = measure(lo, hi)
    if '--json' in argv:
        f = facts(m, lo, hi)
        assert mdigest(f) == mdigest(json.loads(json.dumps(f))), 'facts are not canonical'
        state = load_state() if os.path.exists(STATE) else {}
        out = dict(f, digest=mdigest(f), corpus_max=state.get('max_text'))
        print(json.dumps(out, indent=1, sort_keys=True))
        return
    state = {'passes': [], 'totals': collections.Counter(), 'reg_hashes': set(),
             'max_text': None}
    if os.path.exists(STATE) and mode != 'init':
        s = load_state()
        state['reg_hashes'] = set(s.get('reg_hashes', []))
        state['passes'] = s.get('passes', [])
        state['totals'] = collections.Counter(s.get('totals', {}))
        state['max_text'] = s.get('max_text')

    # record-hash match against all known registration hashes (cross-pass)
    known = state['reg_hashes'] | set(m['reg_hashes'])
    unmatched = [r for r in m['records'] if r['hash'] not in known]
    print(fmt_out(m, state['max_text']))
    print('record-hash match vs all known reg hashes: %d/%d%s'
          % (len(m['records']) - len(unmatched), len(m['records']),
             '; unmatched: ' + ', '.join('id 0x%x -> %s' % (r['id'], r['hash'])
                                         for r in unmatched) if unmatched else ''))

    if mode == 'measure':
        return

    # merge into state
    state['reg_hashes'] = sorted(set(state['reg_hashes']) | set(m['reg_hashes']))
    if mode == 'update':
        state['passes'].append({
            'chunks': [lo, hi], 'range': '%s-%s' % (m['first'], m['last']),
            'files': m['files'], 'sum_size': m['sum_size'],
            'classes': dict(m['classes']),
            'regs': len(m['reg_hashes']), 'reg_distinct': len(set(m['reg_hashes'])),
            'records': len(m['records']), 'record_unmatched': len(unmatched),
        })
    t = state['totals']
    t['files'] += m['files']
    t['sum_size'] += m['sum_size']
    for k, v in m['classes'].items():
        t['class_' + k] += v
    t['registrations'] += len(m['reg_hashes'])
    t['records'] += len(m['records'])
    for k in ('c2d70', 'd4fb0', 'c2d50', 'c7880', 'atexit'):
        t[k] += m['calls'][k]
    for d in ('d4f30', 'd4f70'):
        t['d4_' + d[2:]] += sum(m['dec_hashes'][d].values())
    state['next_chunk'] = hi + 1
    top = m['big'][0] if m['big'] else None
    if mode == 'update' and top and (not state['max_text']
                                     or top[0] > state['max_text']['bytes']):
        print('[state.json] max_text: %s %d B (chunk %04d)' % (top[2], top[0], top[3]))
        state['max_text'] = {'bytes': top[0], 'addr': top[1], 'name': top[2], 'chunk': top[3]}
    write_state({'next_chunk': state['next_chunk'], 'passes': state['passes'],
                 'totals': dict(state['totals']), 'reg_hashes': state['reg_hashes'],
                 'max_text': state['max_text']})
    print('[state.json] next_chunk=%d  totals: %s' % (state['next_chunk'], dict(state['totals'])))


if __name__ == '__main__':
    main()
