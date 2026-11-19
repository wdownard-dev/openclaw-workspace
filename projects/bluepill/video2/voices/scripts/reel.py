"""Stitch audition reels: slate (River) + 0.4 s + clip level-matched to -19 LUFS + 1.0 s gap. Run: clips-venv python -I reel.py
Reel clips are gain-matched copies (the files in narrators/ and characters/ stay raw)."""
import os, sys, subprocess, glob
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(HERE); sys.path.insert(0,HERE)
from catalog import *
import metrics
FF=metrics.FF; TMP=f"{OUT}/_work/reel_tmp"; os.makedirs(TMP,exist_ok=True)
TARGET=-19.0
def norm(src,dst):
    lufs,lra,peak=metrics.ebur(src)
    g=TARGET-lufs
    subprocess.run([FF,"-y","-v","error","-i",src,"-af",f"volume={g:.2f}dB,alimiter=limit=0.89:level=disabled","-ar","44100","-ac","1",dst],check=True)
def silence(sec,dst):
    subprocess.run([FF,"-y","-v","error","-f","lavfi","-i",f"anullsrc=r=44100:cl=mono","-t",str(sec),dst],check=True)
def build(items,out):
    silence(0.4,f"{TMP}/s04.wav"); silence(1.0,f"{TMP}/s10.wav")
    lst=[]
    for i,(slate,clip) in enumerate(items):
        a=f"{TMP}/{i:02d}a.wav"; b=f"{TMP}/{i:02d}b.wav"
        if slate in("intro_n","intro_c","long"):
            norm(f"{OUT}/_work/slates/{slate}.mp3",a); lst+= [a,f"{TMP}/s10.wav"]; continue
        norm(f"{OUT}/_work/slates/{slate}.mp3",a); norm(clip,b)
        lst+= [a,f"{TMP}/s04.wav",b,f"{TMP}/s10.wav"]
    lp=f"{TMP}/list.txt"; open(lp,"w").write("".join(f"file '{p}'\n" for p in lst))
    subprocess.run([FF,"-y","-v","error","-f","concat","-safe","0","-i",lp,"-c:a","libmp3lame","-b:a","128k",out],check=True)
    r=subprocess.run([FF,"-hide_banner","-i",out,"-f","null","-"],capture_output=True,text=True)
    print(out,r.stderr.split("time=")[-1][:11])
def nfile(pattern): return glob.glob(f"{OUT}/narrators/{pattern}")[0]
items=[("intro_n",None)]
for c,n,v,s,note in NARRATORS: items.append((c,nfile(f"{c}_{n}.mp3")))
items.append(("long",None))
for c in ("N03","N05","N07","N08"): items.append((c+"L",nfile(f"{c}L_*.mp3") if False else [p for p in glob.glob(f"{OUT}/narrators/{c}L_*.mp3") if "_set-" not in p][0]))
items.append(("N09L",[p for p in glob.glob(f"{OUT}/narrators/N09L_*.mp3") if "_set-" not in p][0]))
items.append(("N09-V1",nfile("N09L_*_set-V1*.mp3"))); items.append(("N09-ACT",nfile("N09L_*_set-act*.mp3")))
items.append(("N01-v4",nfile("N01_*_model-eleven_v4-tag.mp3"))); items.append(("N09-v4",nfile("N09_*_model-eleven_v4-tag.mp3")))
build(items,f"{OUT}/reel_narrators.mp3")
for f in glob.glob(f"{TMP}/*.wav"): os.remove(f)
items=[("intro_c",None)]
for r,l in CHARS.items():
    for c,n,v,s,note in l: items.append((c,glob.glob(f"{OUT}/characters/{c}_*.mp3")[0]))
build(items,f"{OUT}/reel_characters.mp3")
