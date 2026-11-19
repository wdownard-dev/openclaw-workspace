"""reel_methods.mp3: spoken slate (River) then the scene, for A (v4 tags), A (v2, no tags), B (library voices, dialogue endpoint), C (Daniel processed). Continuous room tone between."""
import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from asm import *
items=[("A4","methodA_v4_scene.mp3"),("A2","methodA_v2_scene.mp3"),("B","methodB_scene.mp3"),("C","methodC_scene.mp3")]
t=0.0; parts=[]; marks=[]
for k,f in items:
    s=fade(trim_soft(load(f"{W}/slate_{k}.mp3"),-55,0.03,0.2),0.015,0.04); g=TARGET-line_lufs(s); s=s*10**(g/20)
    sc=load(f"{OUT}/{f}")
    parts.append((int(t*SR),s)); marks.append((k,round(t,1))); t+=len(s)/SR+1.0
    parts.append((int(t*SR),sc)); t+=len(sc)/SR+2.2
bus=np.zeros(int(t*SR),np.float32)
for st,x in parts: bus[st:st+len(x)]+=x
I=final_mp3(bus,f"{OUT}/reel_methods.mp3"); print(I,round(t,1),marks); json.dump({"marks":marks,"loudness":I,"duration_s":round(t,1)},open(f"{W}/reel.json","w"))
