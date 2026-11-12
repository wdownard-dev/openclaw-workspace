import json,re,statistics as st
a=json.load(open('data2.json')); old=json.load(open('data.json'))
seen={r['id'] for r in a}
for r in old:
    if r['id'] not in seen:
        r.update(likes=0,comments=0,chan_videos=0,country='',lang='',chid=''); a.append(r)
def mins(x):
    m=re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',x); h,mi,s=[int(g or 0) for g in m.groups()]; return h*60+mi+s/60
def ascii_title(t): return sum(ord(c)<128 for c in t)/max(len(t),1)>0.95
for r in a:
    r['min']=mins(r['dur']); r['ratio']=r['views']/max(r['subs'],1)
    r['en']= (r['lang'].startswith('en') or r['lang']=='') and ascii_title(r['title'])
d=[r for r in a if r['en'] and 3<=r['min']<=60]
print("total",len(a),"english-looking 3-60min",len(d))
def stats(rs):
    v=[r['views'] for r in rs]; 
    if not v: return "n=0"
    big=sum(x>=100000 for x in v); sm=sum(1 for r in rs if r['views']>=100000 and r['subs']<30000)
    return f"n={len(v):3} med={int(st.median(v)):>8,} >=100k:{big:3} ({100*big//len(v)}%) >=100k&<30kSubs:{sm}"
print("\n== Length buckets (English)")
for lo,hi in [(3,8),(8,12),(12,16),(16,20),(20,30),(30,60)]:
    print(f"{lo:>2}-{hi:<2} min:", stats([r for r in d if lo<=r['min']<hi]))
print("\n== Title patterns")
pats={"every ___ explained":r"\bevery\b","turned out (to be) true/real":r"turned out|actually (real|true|exist)|were real|really existed","how ___ died / death":r"\bdied\b|\bdeath\b|\bkilled\b","explained":r"explain","who was / who is":r"\bwho (was|is|were)\b","real story / truth":r"real story|the truth|really happened|actually","top N / ranked":r"\btop \d+|\bbest\b|\bstrongest\b|\bmost powerful|ranked","no AI":r"no ai"}
for k,p in pats.items():
    rs=[r for r in d if re.search(p,r['title'],re.I)]
    print(f"{k:30}", stats(rs))
print("\n== By mythology/subject keyword")
for k,p in {"greek":r"greek|zeus|hades|poseidon|athena|titan|olymp|medusa|troy|odysseus|hercules|heracles","norse":r"norse|odin|thor\b|loki|viking|ragnar","egyptian":r"egypt|pharaoh|anubis|osiris|ra\b|isis","mesopotamian":r"mesopotam|sumer|babylon|gilgamesh|tiamat","slavic":r"slavic|baba yaga|perun","japanese":r"japan|shinto|yokai|amaterasu","celtic":r"celtic|irish myth|druid|arthur","aztec/maya":r"aztec|maya|inca","hindu":r"hindu|vishnu|shiva|ramayana|mahabharata"}.items():
    print(f"{k:14}", stats([r for r in d if re.search(p,r['title'],re.I)]))
print("\n== Small-channel outliers (<30k subs, >=150k views), English")
sm=[r for r in d if r['subs']<30000 and r['views']>=150000]
for r in sorted(sm,key=lambda r:-r['ratio'])[:30]:
    print(f"{r['views']:>9,} | {r['subs']:>6,} subs x{r['ratio']:.0f} | {r['min']:.0f}m | pub {r['pub']} | ch since {r['chan_created']} ({r['chan_videos']} vids) | {r['ch'][:22]} | {r['title'][:70]}")
print("\n== Channels with 2+ videos >=150k (English), by count")
from collections import defaultdict
g=defaultdict(list)
for r in d:
    if r['views']>=150000: g[(r['ch'],r['subs'],r['chan_created'],r['chan_videos'])].append(r)
for k,v in sorted(g.items(), key=lambda kv:-len(kv[1]))[:14]:
    if len(v)>=2: print(len(v),"vids |",k[0][:26],"|",f"{k[1]:,} subs | since {k[2]} | {k[3]} vids | best {max(x['views'] for x in v):,}")
print("\n== Animated / stick-figure style titles or channels")
rs=[r for r in d if re.search(r"animat|stick|cartoon",r['title']+r['ch'],re.I)]
print(stats(rs))
for r in sorted(rs,key=lambda r:-r['views'])[:8]: print(f"{r['views']:>9,} | {r['subs']:>8,} subs | {r['min']:.0f}m | {r['ch'][:22]} | {r['title'][:70]}")
print("\n== Engagement (likes/views, comments/views) among >=100k English", )
e=[r for r in d if r['views']>=100000 and r['likes']]
print(f"median like rate {100*st.median(r['likes']/r['views'] for r in e):.1f}%  comments {100*st.median(r['comments']/r['views'] for r in e):.2f}%  n={len(e)}")
print("\n== Non-English share of raw pool", f"{100*sum(1 for r in a if not r['en'])//len(a)}%")
