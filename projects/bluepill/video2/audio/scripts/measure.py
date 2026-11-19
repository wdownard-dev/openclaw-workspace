import os,sys,json
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from common import *; from tools import role_measure,spec
import words as Wd
pid=sys.argv[1]; P=next(p for p in Wd.plan()["passages"] if p["id"]==pid)
x=load(os.path.join(OUT,"passages",pid+".mp3")); ws=Wd.words_of(P)
nar=[w for w in ws if w["speaker"]=="NARR" and not w["added"]]
t0,t1=ws[0]["start"],ws[-1]["end"]
seg=x[int(max(0,t0-0.05)*SR):int((t1+0.2)*SR)]
text=" ".join(w["word"] for w in ws)
m=role_measure([seg],text,"test_"+pid); print("whole passage",m)
# inter-beat gaps
gaps=[]; prev=None
for w in ws:
    if prev and w["beat"]!=prev["beat"]: gaps.append((prev["beat"],w["beat"],round(w["start"]-prev["end"],2)))
    prev=w
print("beat gaps",gaps)
iw=[round(b["start"]-a["end"],2) for a,b in zip(ws,ws[1:]) if b["beat"]==a["beat"] and b["start"]-a["end"]>0.4]
print("intra-beat gaps >0.4",iw)
