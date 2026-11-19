import re, sys, json
src = open('/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/src/beats2.txt').read().splitlines()
chs = []; cur = None; state = None; bad = []
for i, l in enumerate(src, 1):
    l = l.rstrip()
    if not l: continue
    if l.startswith('@CH '):
        cur = {'title': l[4:], 'beats': []}; chs.append(cur); continue
    if l.startswith('@S '):
        state = l[3:]; continue
    p = [x.strip() for x in l.split('||')]
    if len(p) != 3:
        bad.append((i, l[:70])); continue
    cur['beats'].append({'text': p[0], 'shot': p[1], 'state': state, 'trace': p[2]})
w = lambda t: len(re.findall(r"[A-Za-z0-9']+", t))
allt = ' '.join(b['text'] for c in chs for b in c['beats'])
sents = [s.strip() for s in re.split(r'(?<=[.?!])\s+', allt) if s.strip()]
tot = w(allt)
print('bad lines', bad)
print('words', tot, 'beats', sum(len(c['beats']) for c in chs), 'sentences', len(sents),
      'mean', round(tot/len(sents), 1), 'questions', allt.count('?'), 'min', round(tot/150, 2),
      'sent/min', round(len(sents)/(tot/150), 1))
t = 0
for c in chs:
    cw = sum(w(b['text']) for b in c['beats'])
    print(c['title'], cw, round(t/150*60), 's start')
    t += cw
json.dump(chs, open('/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/src/parsed2.json', 'w'))
