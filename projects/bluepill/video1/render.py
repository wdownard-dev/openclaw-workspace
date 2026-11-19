import importlib.util, re, math, collections
spec=importlib.util.spec_from_file_location('beats','beats.py'); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
R=b.R; CH=b.CHAPTERS
WPS=2.5
def dur(t): return max(3.2, len(t.split())/WPS)
def fmt(s): s=int(round(s)); return f"{s//60}:{s%60:02d}"
def split_text(t):
    w=t.split(); n=len(w); mid=n/2
    best=None
    for i,x in enumerate(w[:-1]):
        if x[-1] in ',:;.' and 3<=i+1<=n-3:
            d=abs(i+1-mid)
            if best is None or d<best[0]: best=(d,i+1)
    k=best[1] if best else n//2
    return ' '.join(w[:k]),' '.join(w[k:])
shots=[]; t=0.0; last_ch=-1
for ri,r in enumerate(R):
    if r['ch']!=last_ch:
        last_ch=r['ch']; card=CH[r['ch']][1]
        if card:
            shots.append(dict(card=True,text="",kind="title card",chars="none",light="flat parchment, calm",cam="hold",asset="CODE:chapter-card",note=f"'{card}', silent, 2.5 s",start=t,d=2.5,ch=r['ch'],words=0,para=False,beat=ri)); t+=2.5
    d=dur(r['text'])
    if d>6.2:
        a,bb=split_text(r['text']); parts=[(a,r['asset'],r['note'],r['kind']),(bb,("X:"+re.sub(r'^X:','',r['asset'].split(' + ')[0])) if r['kind']!='card' and not r['asset'].startswith('CODE') else r['asset'],"B shot: second crop or state of the same image, hard cut at the phrase break" if r['kind']!='card' else "B shot: next state of the same card",r['kind'])]
        for pi,(tx,asset,note,kind) in enumerate(parts):
            s=dict(r); s.update(text=tx,asset=asset,note=note if pi==0 else note,kind=kind if pi==0 else (r['kind'] if r['kind'] in('card','map','diagram','white') else ('bakedX' if r['kind'] in ('baked','bakedX','bakedR') else r['kind'])),start=t,d=dur(tx),words=len(tx.split()),card=False,para=r['para'] if pi==0 else False,beat=ri)
            shots.append(s); t+=s['d']
    else:
        s=dict(r); s.update(start=t,d=d,words=len(r['text'].split()),card=False,beat=ri); shots.append(s); t+=d
total=t
for i,s in enumerate(shots,1): s['n']=i
words=sum(len(r['text'].split()) for r in R)
ch_start={}
for s in shots: ch_start.setdefault(s['ch'],s['start'])
kc=collections.Counter()
for s in shots:
    k=s['kind']
    if k in('baked','bakedX','bakedR'): kc['baked']+=1
    elif k=='cutout': kc['cutout']+=1
    else: kc['card']+=1
N=len(shots)
# assets
ids=collections.defaultdict(list)
first={}
for s in shots:
    for m in re.findall(r'\b(NBG\d+|NB\d+|NP\d+)\b',s['asset']):
        if s['n'] not in ids[m]: ids[m].append(s['n'])
        first.setdefault(m,s)
reuse=collections.defaultdict(list)
for s in shots:
    for m in re.findall(r'\b(RS\d+|RC\d+)\b',s['asset']):
        reuse[m].append(s['n'])
RISK={'NB01':'M','NB02':'H','NB03':'L','NB04':'L','NB05':'H','NB06':'M','NB07':'M','NB08':'M','NB09':'H','NB10':'M','NB11':'M','NB12':'H','NB13':'L','NB14':'H','NB15':'L','NB16':'H','NB17':'L','NB18':'H','NB19':'H','NB20':'L','NB21':'M','NB22':'M','NB23':'L','NB24':'M','NB25':'L',
 'NBG01':'L','NBG02':'L','NBG03':'L','NBG04':'L','NBG05':'L','NBG06':'L','NBG07':'M','NBG08':'M','NBG09':'L','NP01':'M','NP02':'L','NP03':'L','NP04':'H'}
ATT={'H':2.0,'M':1.43,'L':1.18}
allids=sorted(ids, key=lambda x:(re.match(r'[A-Z]+',x).group()!='NB', re.match(r'[A-Z]+',x).group()!='NBG', x))
nb=[i for i in allids if i.startswith('NB') and not i.startswith('NBG')]; nbg=[i for i in allids if i.startswith('NBG')]; npp=[i for i in allids if i.startswith('NP')]
new_total=len(allids)
flat_calls=math.ceil(new_total/0.7)
rw_calls=sum(ATT[RISK[i]] for i in allids)
cnt=collections.Counter(RISK[i] for i in allids)
NAMES={}
def short_spec(i):
    s=first[i]; return f"{s['chars']}; {s['light']}; {s['note']}"
pace_long=[s['n'] for s in shots if not s['card'] and s['d']>6.0]
pace_short=[s['n'] for s in shots if not s['card'] and s['d']<3.5]
if __name__=='__main__':
    print('shots',N,'narrated words',words,'runtime',fmt(total),dict(kc),'new',len(nb),len(nbg),len(npp),new_total,'flat calls',flat_calls,'risk-weighted',round(rw_calls,1),dict(cnt))
    print('long',pace_long,'short',pace_short); print({k:v for k,v in reuse.items()})
    wc=sum(1 for s in shots if 'extras' in s['chars'] or 'crew' in s['chars'].lower())
    print('crew/extras shots',wc)
