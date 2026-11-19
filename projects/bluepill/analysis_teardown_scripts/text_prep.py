import json,sys,re
root='/home/williamdownard/.openclaw/workspace/projects/bluepill/'
out='/home/williamdownard/.openclaw/workspace/projects/bluepill/analysis_teardown_out/'
import os; os.makedirs(out,exist_ok=True)
# reference words
d=json.load(open(root+'tests/ref_mJS_captions/ref.en.json3'))
words=[]
for e in d['events']:
    if 'segs' not in e: continue
    t0=e['tStartMs']
    for s in e['segs']:
        w=s['utf8']
        if w.strip()=='' : continue
        words.append({'text':w.strip(),'start':(t0+s.get('tOffsetMs',0))/1000})
# dedupe: auto-captions might repeat across rolling windows
seen=set(); uniq=[]
for w in words:
    k=(w['text'],round(w['start'],2))
    if k in seen: continue
    seen.add(k); uniq.append(w)
uniq.sort(key=lambda w:w['start'])
print(len(words),len(uniq))
json.dump(uniq,open(out+'ref_words.json','w'))
# ours
o=json.load(open(root+'video1/audio/words.json'))
print(len(o), o[-1]['end'])
