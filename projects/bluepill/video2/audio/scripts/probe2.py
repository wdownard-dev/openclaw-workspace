import os,sys,json,difflib
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from common import *; import tools, words as Wd
for pid in sys.argv[1:]:
    p=next(q for q in Wd.plan()["passages"] if q["id"]==pid); ws=Wd.words_of(p)
    segs,_=tools.model().transcribe(os.path.join(OUT,"passages",pid+".mp3"),word_timestamps=True,beam_size=5,language="en",condition_on_previous_text=False)
    W=[w for s in segs for w in s.words if tools.norm(w.word)]
    want=[tools.norm(w["word"]) for w in ws]; heard=[tools.norm(w.word) for w in W]
    sm=difflib.SequenceMatcher(None,want,heard,autojunk=False)
    for tag,a0,a1,b0,b1 in sm.get_opcodes():
        if tag=="insert": print(pid,"INSERT heard",[(W[i].word,round(W[i].start,2)) for i in range(b0,b1)],"after script words",[ws[i]["word"] for i in range(max(0,a0-4),a0)],"before",[ws[i]["word"] for i in range(a0,min(len(ws),a0+3))],"script t",round(ws[a0-1]["end"],2))
