"""Spoken slates for the reels, one fixed neutral voice (River, premade), flat settings. Files in _work/slates/."""
import os
from catalog import *
OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM=["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen"]
SET={"stability":0.75,"similarity_boost":0.75,"style":0.0,"use_speaker_boost":True,"speed":1.0}
def slate_list():
    s={}
    s["intro_n"]="Narrators."
    for i,(c,n,v,src,note) in enumerate(NARRATORS,1): s[c]=f"{NUM[i].capitalize()}."
    s["long"]="Longer script."
    for c in ("N03","N05","N07","N08","N09"): s[c+"L"]=f"{NUM[int(c[1:])].capitalize()}, long."
    s["N09-V1"]="Nine, steady settings."
    s["N09-ACT"]="Nine, acting settings."
    s["N01-v4"]="One, model v four, with a style tag."
    s["N09-v4"]="Nine, model v four, with a style tag."
    s["intro_c"]="Characters."
    roles={"ODY":"Odysseus","POLY":"Polyphemus","CYC2":"The Cyclopes","CREW":"The crew"}
    for r,l in CHARS.items():
        for k,(c,n,v,src,note) in enumerate(l,1): s[c]=f"{roles[r]}, {NUM[k]}."
    return s
def run(tts):
    os.makedirs(f"{OUT}/_work/slates",exist_ok=True)
    for k,t in slate_list().items():
        tts("slate-"+k,SLATE_VOICE[0],SLATE_VOICE[1],t,SET,f"{OUT}/_work/slates/{k}.mp3","reel slate")
