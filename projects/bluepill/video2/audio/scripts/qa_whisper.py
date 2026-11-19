import os,sys,json,difflib
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from common import *; import tools
import words as Wd
P=Wd.plan()["passages"]; res={}
for p in P:
    path=os.path.join(OUT,"passages",p["id"]+".mp3")
    segs,_=tools.model().transcribe(path,word_timestamps=True,beam_size=1,language="en",condition_on_previous_text=False)
    W=[w for s in segs for w in s.words if tools.norm(w.word)]
    heard=[tools.norm(w.word) for w in W]
    ws=Wd.words_of(p); want=[tools.norm(w["word"]) for w in ws]
    sm=difflib.SequenceMatcher(None,want,heard,autojunk=False)
    cov=sum(n for _,_,n in sm.get_matching_blocks())/len(want)
    diffs=[]
    for tag,a0,a1,b0,b1 in sm.get_opcodes():
        if tag!="equal": diffs.append(dict(op=tag,want=[(ws[i]["word"],ws[i]["beat"],round(ws[i]["start"],2)) for i in range(a0,a1)],heard=" ".join(heard[b0:b1])))
    res[p["id"]]=dict(coverage=round(cov,3),n=len(want),heard_n=len(heard),diffs=diffs)
    print(p["id"],"coverage",round(cov,3),"want",len(want),"heard",len(heard)); 
    for d in diffs: print("   ",d)
json.dump(res,open(os.path.join(OUT,"_work","qa_whisper.json"),"w"),indent=1)
