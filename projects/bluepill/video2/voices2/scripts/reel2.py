"""Builds reel2_daniel.mp3 and reel2_characters.mp3: slate (River), 0.4 s, clip (edge silence trimmed, gaps over 0.9 s shortened to 0.7 s, level-matched to -19 LUFS), 1.0 s gap.
Files in narrator_daniel/ and characters/ stay raw. Run: python -I reel2.py"""
import os, sys, subprocess
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
        a=f"{TMP}/{i:02d}a.wav"; b=f"{TMP}/{i:02d}b.wav"
        prep(f"{OUT}/_work/slates/{slate}.mp3",a,trim=False)
        if clip is None: lst+=[a,f"{TMP}/s10.wav"]; continue
        prep(clip,b); lst+=[a,f"{TMP}/s04.wav",b,f"{TMP}/s10.wav"]
    open(f"{TMP}/list.txt","w").write("".join(f"file '{p}'\n" for p in lst))
    subprocess.run([FF,"-y","-v","error","-f","concat","-safe","0","-i",f"{TMP}/list.txt","-c:a","libmp3lame","-b:a","128k",out],check=True)
    r=subprocess.run([FF,"-hide_banner","-i",out,"-f","null","-"],capture_output=True,text=True); print(out,r.stderr.split("time=")[-1][:11])
def clean():
    for f in os.listdir(TMP): os.remove(f"{TMP}/{f}")
rows=[r for r in plan.rows() if r["role"]=="NARR"]
items=[("intro_d",None)]+[(f"n{r['num']}",f"{OUT}/{r['file']}") for r in rows]
build(items,f"{OUT}/reel2_daniel.mp3"); clean()
items=[("intro_c",None)]
for role,rs in plan.reel_chars():
    items.append((f"role_{role}",None))
    for r in rs: items.append((f"n{r['num']}",f"{OUT}/{r['file']}"))
build(items,f"{OUT}/reel2_characters.mp3"); clean()
