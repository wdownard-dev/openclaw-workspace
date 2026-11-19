"""Method B: ElevenLabs Text to Dialogue (/v1/text-to-dialogue), one call per passage. set=bp -> William's saved BP voices (also the DIAGNOSTIC clip); set=lib -> library audition voices chosen by metadata.
Narrator = Daniel in both. Tags only on character turns (scene_texts 'dlg' mode)."""
import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from scene_texts import line,B
sel=sys.argv[1]; model=sys.argv[2] if len(sys.argv)>2 else "eleven_v4"; V=BP if sel=="bp" else LIB; ST={"stability":0.5,"similarity":0.75}
rid_prev=None
for i in range(2):
    inputs=[]
    for b in SCENES[i]:
        s=B[b][0]; vid=DANIEL[1] if s=="NARR" else V[s][1]; inputs.append({"text":line(b,"dlg"),"voice_id":vid})
    extra={}
    if i==1 and rid_prev: extra["previous_request_ids"]=[rid_prev]
    path=f"{OUT}/lines/B_{sel}_{model}_passage{i+1}.mp3"
    el_dialogue(f"B_{sel}_{model}_passage{i+1}",inputs,path,model,ST,f"Method B ({sel} voices) text-to-dialogue, one call",extra)
    if os.path.exists(path+".rid"): rid_prev=open(path+".rid").read().strip()
