"""Method A: Daniel does everything, one continuous call per passage. mode v4 = eleven_v4 with delivery tags; mode v2 = multilingual_v2 (no tags, set up by attribution; only run if v4 shifts the narrator timbre)."""
import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from scene_texts import passage,B
mode=sys.argv[1]
if mode=="v4":
    ST={"stability":0.5,"similarity_boost":0.75}
    for i in range(2):
        t=passage(i,"v4tags"); extra={}
        if i==1: extra["previous_text"]=respell(B[40][1])
        el_tts(f"A_v4_passage{i+1}",*DANIEL,t,ST,f"{OUT}/lines/A_v4_passage{i+1}.mp3","eleven_v4","Method A v4: Daniel + tags, one call",extra)
if mode=="v2":
    for i in range(2):
        t=passage(i,"v2attr"); extra={}
        if i==1: extra["previous_text"]=respell(B[40][1])
        el_tts(f"A_v2_passage{i+1}",*DANIEL,t,S_DANIEL,f"{OUT}/lines/A_v2_passage{i+1}.mp3","eleven_multilingual_v2","Method A v2: Daniel, attribution, no tags, one call",extra)
