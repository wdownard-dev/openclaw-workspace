"""Step 2 compare: first-line segment of each chosen clip (cut at whisper word times; local, free) vs the same line rendered through the saved voice (two models).
Writes _work/verify_metrics.json. Run with the clips-venv python -I."""
import os,sys,json,subprocess,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np, metrics2, metrics
os.environ.setdefault("HF_HOME","/home/williamdownard/openclaw-sites/models")
from faster_whisper import WhisperModel
from verify_gen import LINES
CH={"ODY":"characters/ODY/design/ODY_designA_p3.mp3","POLY":"characters/POLY/design/POLY_designB_p2.mp3","CYC2":"characters/CYC2/design/CYC2_designB_p2.mp3","CREW":"characters/CREW/design/CREW_designB_p1.mp3"}
NW={r:len(re.findall(r"[A-Za-z0-9']+",t)) for r,t in LINES.items()}
model=WhisperModel("small.en",device="cpu",compute_type="int8",download_root="/home/williamdownard/openclaw-sites/models")
def cut(src,dst,role):
    segs,_=model.transcribe(src,word_timestamps=True,beam_size=1,language="en",condition_on_previous_text=False)
    ws=[w for s in segs for w in s.words]; n=NW[role]; print(role,"heard first:"," ".join(w.word.strip() for w in ws[:n]))
    a=max(0,ws[0].start-0.05); b=ws[n-1].end+0.1
    subprocess.run([FF,"-y","-v","error","-i",src,"-ss",str(a),"-to",str(b),dst],check=True)
res={}
for role,text in LINES.items():
    seg=f"{W}/chosen_{role}_first.wav"; cut(f"{V2}/{CH[role]}",seg,role)
    res[role]={"chosen_first_line":metrics2.measure2(seg,text)}
    for m in ("eleven_multilingual_v2","eleven_v3"): res[role][m]=metrics2.measure2(f"{OUT}/verify/{role}_{m}.mp3",text)
json.dump(res,open(f"{W}/verify_metrics.json","w"),indent=1)
print(f"{'role':5} {'clip':26} {'dur':>5} {'span':>5} {'F0mean':>6} {'F0med':>5} {'spread':>6} {'LUFS':>6}")
for role,d in res.items():
    for k,m in d.items(): print(f"{role:5} {k:26} {m['duration_s']:5} {m['span_s']:5} {m['f0w_mean_hz']:6} {m['f0w_median_hz']:5} {m['pitch_spread_st']:6} {m['lufs']:6}")
