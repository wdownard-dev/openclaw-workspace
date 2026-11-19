"""Spoken slates for the round-2 reels: River (premade), same flat settings as round 1. Files in _work/slates/ (keyed by name)."""
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from cfg import *
import plan
SET={"stability":0.75,"similarity_boost":0.75,"style":0.0,"use_speaker_boost":True,"speed":1.0}
def slate_list():
    s={"intro_d":"Daniel, narrator variants.","intro_c":"Characters, round two."}
    for r in plan.rows():
        if r["role"]=="NARR": s[f"n{r['num']}"]=plan.words(r["num"]).capitalize()+("." if r["id"] not in("D4","D5") else (", control." if r["id"]=="D4" else ", bonus."))
    for role,items in plan.reel_chars():
        s[f"role_{role}"]=plan.ROLE_NAME[role]+"."
        for r in items: s[f"n{r['num']}"]=plan.slate_text(r)
    for role,items in plan.reel_extra():
        for r in items: s[f"n{r['num']}"]=plan.slate_text(r)
    s["intro_x"]="Extra candidates."
    return s
def run(tts):
    os.makedirs(f"{OUT}/_work/slates",exist_ok=True)
    for k,t in slate_list().items():
        tts("slate-"+k,RIVER[0],RIVER[1],t,SET,f"{OUT}/_work/slates/{k}.mp3","reel slate")
if __name__=="__main__":
    s=slate_list(); print(len(s),sum(len(v) for v in s.values())); [print(k,v) for k,v in s.items()]
