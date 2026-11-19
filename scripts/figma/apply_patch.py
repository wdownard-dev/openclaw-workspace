#!/usr/bin/env python3
"""Apply storyboard_patch.json (from figma_pull.py) to storyboard.json.
Default is --dry-run: prints a diff, writes nothing. --write backs up the original first.
Per shot: bg replaced if patch has one; sprite events matched by src in order get new x/y/h/mirror;
patch sprites with no match become NEW sprite events (at = shot start word, flagged "previz": true);
storyboard sprite events not in the Figma frame are KEPT unless --prune-missing.
swap/none events, labels, chips, stamps, counters, sfx are never touched."""
import argparse, copy, datetime, json, os, shutil, sys

V2 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../projects/bluepill/video2'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('patch')
    ap.add_argument('--storyboard', default=os.path.join(V2, 'storyboard.json'))
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--dry-run', action='store_true', help='default')
    ap.add_argument('--prune-missing', action='store_true', help='delete sprite events whose src is absent from the Figma frame')
    ap.add_argument('--out', help='with --write: write here instead of over the storyboard (original untouched)')
    a = ap.parse_args()
    raw = open(a.storyboard).read()
    sb = json.loads(raw)
    patch = json.load(open(a.patch))
    new = copy.deepcopy(sb)
    shots = {s['id']: s for s in new['shots']}
    log, changed = [], 0
    for sid, p in patch['shots'].items():
        s = shots.get(sid)
        if not s:
            log.append('! %s not in storyboard, skipped' % sid); continue
        log.append('== %s (beat %s, frame %s)' % (sid, p['beat'], p['frame']))
        if p.get('bg') and (s['bg'].get('src') != p['bg']['src'] or s['bg'].get('type') != p['bg']['type']):
            log.append('  bg: %s -> %s' % (json.dumps(s['bg']), json.dumps(p['bg']))); s['bg'] = {**s['bg'], **p['bg']}; changed += 1
        evs = [e for e in new['events'] if e['shot'] == sid and e['kind'] == 'sprite']
        used = set()
        for ps in p['sprites']:
            match = next((e for e in evs if e['src'] == ps['src'] and id(e) not in used), None)
            if match:
                used.add(id(match))
                before = {k: match.get(k) for k in ('x', 'y', 'h', 'mirror', 'inset')}
                for k in ('x', 'y', 'h'):
                    match[k] = ps[k]
                if ps.get('mirror'): match['mirror'] = True
                else: match.pop('mirror', None)
                if ps.get('inset') and not match.get('inset'): match['inset'] = True
                after = {k: match.get(k) for k in before}
                if before != after:
                    changed += 1
                    log.append('  ~ %s  %s -> %s' % (ps['src'], json.dumps({k: v for k, v in before.items() if v is not None}), json.dumps({k: v for k, v in after.items() if v is not None})))
            else:
                at = evs[0]['at'] if evs else {'word': s['start']['word']}
                ev = {'shot': sid, 'kind': 'sprite', 'at': at, 'src': ps['src'], 'x': ps['x'], 'y': ps['y'], 'h': ps['h'], 'previz': True}
                for k in ('mirror', 'inset'):
                    if ps.get(k): ev[k] = True
                if not evs:
                    ev['t'] = s['t']
                else:
                    ev['t'] = evs[0].get('t')
                idx = max([i for i, e in enumerate(new['events']) if e['shot'] == sid] or [len(new['events']) - 1]) + 1
                new['events'].insert(idx, ev); changed += 1
                log.append('  + NEW %s x=%d y=%d h=%d (at %s; adjust timing by hand)' % (ps['src'], ps['x'], ps['y'], ps['h'], json.dumps(at)))
        missing = [e for e in evs if id(e) not in used]
        for e in missing:
            if a.prune_missing:
                new['events'].remove(e); changed += 1; log.append('  - REMOVED %s (not in Figma frame)' % e['src'])
            else:
                log.append('  . kept %s (not in Figma frame; --prune-missing to delete)' % e['src'])
        for u in p.get('unmapped', []):
            log.append('  ? unmapped: ' + u)
    print('\n'.join(log))
    print('\n%d change(s). %s' % (changed, 'WRITING' if a.write else 'dry run, nothing written (use --write)'))
    if a.write and changed:
        indent = 2 if raw.startswith('{\n  "') else (1 if raw.startswith('{\n "') else None)
        if a.out:
            dest = a.out
        else:
            dest = a.storyboard
            bak = a.storyboard + '.bak-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            shutil.copy2(a.storyboard, bak); print('backup:', bak)
        with open(dest, 'w') as f:
            json.dump(new, f, indent=indent, ensure_ascii=True)   # byte-identical style to the original (ascii-escaped, no trailing newline)
        print('wrote', dest)


if __name__ == '__main__':
    main()
