"""Per-role F0 from the proof lines, shifted-chorus F0, pitch distances, one-word flatness. Writes _work/analysis.json. clips-venv python -I."""
import os,sys,json,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np, metrics, metrics2
from assemble import load,trim,write_wav,shift,SR
from proof_gen import BEATS,parse,respell
os.environ.setdefault("HF_HOME","/home/williamdownard/openclaw-sites/models")
from faster_whisper import WhisperModel
B=parse(); lines=[(b,B[b][0]) for b in BEATS]; res={"roles":{}}
def role_audio(spk,semi=0):
    xs=[trim(load(f"{OUT}/proof_lines/beat{b:02d}_{s}.mp3")) for b,s in lines if s==spk]
    if semi: xs=[shift(x,semi,f"{W}/_sh") for x in xs]
    return np.concatenate([np.concatenate([x,np.zeros(int(0.3*SR),np.float32)]) for x in xs])
def measure_role(spk,semi=0):
    x=role_audio(spk,semi); p=f"{W}/_role.wav"; write_wav(p,x)
    text=" ".join(B[b][1] for b,s in lines if s==spk); m=metrics2.measure2(p,text)
    return {k:m[k] for k in ("f0w_mean_hz","f0w_median_hz","pitch_spread_st","wpm","span_s","pauses_per_min","lufs","lra_lu")}
for spk in ("NARR","ODY","POLY","CYC2","CREW"): res["roles"][spk]=measure_role(spk); print(spk,res["roles"][spk])
for semi in (2,3): res["roles"][f"CYC2+{semi}st"]=measure_role("CYC2",semi); print("CYC2 +",semi,res["roles"][f"CYC2+{semi}st"])
st=lambda a,b:round(12*np.log2(a/b),2)
R=res["roles"]; pairs={}
for a,b in (("ODY","POLY"),("ODY","CYC2"),("POLY","CYC2"),("POLY","CREW"),("NARR","ODY"),("NARR","POLY"),("NARR","CYC2"),("CYC2+2st","POLY"),("CYC2+3st","POLY"),("CYC2+2st","ODY"),("CYC2+3st","ODY"),("CYC2+3st","CREW"),("CYC2+3st","NARR")):
    pairs[f"{a} vs {b}"]={"mean_st":st(R[a]["f0w_mean_hz"],R[b]["f0w_mean_hz"]),"median_st":st(R[a]["f0w_median_hz"],R[b]["f0w_median_hz"])}
res["pairs_st"]=pairs; print(json.dumps(pairs,indent=0))
# one-word flatness
model=WhisperModel("small.en",device="cpu",compute_type="int8",download_root="/home/williamdownard/openclaw-sites/models")
def norm(w): return re.sub(r"[^a-z0-9']","",w.lower())
def flat(path,word,mode):
    x=metrics.load(path); n=len(x)
    if mode=="whole": w0,w1=0,n/16000
    else:
        segs,_=model.transcribe(path,word_timestamps=True,beam_size=1,language="en",condition_on_previous_text=False)
        W_=[w for s in segs for w in s.words]; c=[w for w in W_ if norm(w.word)==norm(word)]
        if not c: return {"word":word,"file":os.path.basename(path),"status":"NOT FOUND","heard":" ".join(w.word.strip() for w in W_)}
        w=c[0] if mode=="first" else c[-1]; w0,w1=w.start,w.end
    seg=trim(x_:=x[int(w0*16000):int(w1*16000)]) if False else x[int(w0*16000):int(w1*16000)]
    fr=metrics2.f0_frames(seg,lambda s:True,1024,160,int(16000/400),int(16000/40),True,True)
    v=12*np.log2(np.array([f for _,f in fr])/100) if fr else np.array([])
    if len(v)>=3: v=np.array([np.median(v[max(0,j-1):j+2]) for j in range(len(v))])
    rng=float(np.percentile(v,90)-np.percentile(v,10)) if len(v)>=6 else None
    return {"word":word,"file":os.path.basename(path),"dur":round(w1-w0,2),"voiced_frames":len(v),"f0_median_hz":round(float(100*2**(np.median(v)/12))) if len(v) else None,
            "f0_p10_p90_st":round(rng,2) if rng is not None else None,"status":"UNRELIABLE (few voiced frames)" if rng is None else ("FLAT" if rng<2.0 else "ok")}
P=f"{OUT}/proof_lines/"
checks=[(P+"beat66_CREW.mp3","Nope.","whole"),(P+"beat64_CREW.mp3","Hello?","whole"),(P+"extra_CYC2_Sheep.mp3","Sheep.","whole"),(P+"extra_ODY_Ah_ctx.mp3","Ah","last"),
        (P+"beat31_ODY.mp3","Nobody","last"),(P+"beat32_POLY.mp3","Nobody","first"),(P+"beat33_ODY.mp3","honoured","last")]
res["oneword"]=[flat(*c) for c in checks]
for o in res["oneword"]: print(o)
json.dump(res,open(f"{W}/analysis.json","w"),indent=1)
