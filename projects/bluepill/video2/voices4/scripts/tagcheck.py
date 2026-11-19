import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tools import *
TAGW={"dry","controlled","slow","enormous","gentle","bored","flat","bellowing","pain","earnest","nervous","horrified","puzzled","quietly","bellowing"}
out={}
for stem in ("A_v4","B_bp_eleven_v4","B_lib_eleven_v4"):
    hit=[]
    for i in (1,2):
        segs,_=model().transcribe(f"{OUT}/lines/{stem}_passage{i}.mp3",word_timestamps=True,beam_size=1,language="en",condition_on_previous_text=False)
        hit+=[(round(w.start,1),norm(w.word)) for s in segs for w in s.words if norm(w.word) in TAGW]
    out[stem]=hit; print(stem,hit)
json.dump(out,open(f"{W}/tagcheck.json","w"))
