"""Rebuilds reel2_characters.mp3 (main) and reel2_extra.mp3 (extras) from the CURRENT plan.py, using existing slates only (no TTS).
Same processing as reel2.py. Writes _work/reel_manifest.json (item order, slate number, file). Run: python -I reel2b.py"""
import os, sys, json, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(HERE)),"voices","scripts"))
from cfg import *
import plan, metrics
TMP=f"{OUT}/_work/reel_tmp"; os.makedirs(TMP,exist_ok=True); TARGET=-19.0
SIL="silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08:stop_periods=-1:stop_duration=0.9:stop_threshold=-50dB:stop_silence=0.7"
def prep(src,dst,trim=True):
    t=f"{TMP}/_t.wav"
    subprocess.run([FF,"-y","-v","error","-i",src,"-af",(SIL+"," if trim else "")+"aresample=44100","-ac","1",t],check=True)
    lufs,lra,peak=metrics.ebur(t); g=TARGET-lufs
    subprocess.run([FF,"-y","-v","error","-i",t,"-af",f"volume={g:.2f}dB,alimiter=limit=0.89:level=disabled","-ar","44100","-ac","1",dst],check=True)
def silence(sec,dst): subprocess.run([FF,"-y","-v","error","-f","lavfi","-i","anullsrc=r=44100:cl=mono","-t",str(sec),dst],check=True)
def build(items,out):
    silence(0.4,f"{TMP}/s04.wav"); silence(1.0,f"{TMP}/s10.wav"); lst=[]
    for i,(slate,clip) in enumerate(items):
        sp=f"{OUT}/_work/slates/{slate}.mp3"; assert os.path.exists(sp),sp
        a=f"{TMP}/{i:02d}a.wav"; b=f"{TMP}/{i:02d}b.wav"; prep(sp,a,trim=False)
        if clip is None: lst+=[a,f"{TMP}/s10.wav"]; continue
        prep(clip,b); lst+=[a,f"{TMP}/s04.wav",b,f"{TMP}/s10.wav"]
    open(f"{TMP}/list.txt","w").write("".join(f"file '{p}'\n" for p in lst))
    subprocess.run([FF,"-y","-v","error","-f","concat","-safe","0","-i",f"{TMP}/list.txt","-c:a","libmp3lame","-b:a","128k",out],check=True)
    for f in os.listdir(TMP): os.remove(f"{TMP}/{f}")
man={}
for name,pl,intro in (("reel2_characters.mp3",plan.reel_chars(),"intro_c"),("reel2_extra.mp3",plan.reel_extra(),None)):
    items=[(intro,None)] if intro else []; m=[]
    for role,rs in pl:
        items.append((f"role_{role}",None)); m.append(dict(slate=f"role_{role}"))
        for r in rs: items.append((f"n{r['num']}",f"{OUT}/{r['file']}")); m.append(dict(slate=f"n{r['num']}",num=r["num"],file=r["file"],role=role))
    build(items,f"{OUT}/{name}"); man[name]=m; print(name,len(items))
json.dump(man,open(f"{OUT}/_work/reel_manifest.json","w"),indent=1)
