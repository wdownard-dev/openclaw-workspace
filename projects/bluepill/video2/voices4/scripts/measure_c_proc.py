"""Method C processing check: per role, the raw Daniel character lines vs the processed ones (same lines): F0, spectral centroid, share above 4 / 8 kHz, F0 jump rate (artefact indicator), abrupt edges."""
import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tools import *; from asm import *; from assemble_all import rubber,PROC,ST; from scene_texts import B
def jump(x):
    write_wav(f"{W}/_j2.wav",x); x16=metrics.load(f"{W}/_j2.wav"); fr=metrics2.f0_frames(x16,lambda s:True,1024,160,int(16000/400),int(16000/40),True,True)
    v=12*np.log2(np.array([f for _,f in fr])/100); return round(float((np.abs(np.diff(v))>2).mean()*100),1)
def hf8(x):
    n=2048; S=np.mean([np.abs(np.fft.rfft(x[i:i+n]*np.hanning(n)))**2 for i in range(0,len(x)-n,1024)],axis=0); fq=np.fft.rfftfreq(n,1/SR); return round(100*float(S[fq>8000].sum()/S.sum()),3)
out={}
for s in ("ODY","POLY","CYC2","CREW"):
    raw=[];pro=[]
    for b in BEATS:
        if B[b][0]!=s: continue
        x=trim_soft(load(f"{OUT}/lines/C_beat{b:02d}_{s}.mp3"),-55,0.03,0.15); raw.append(x); st,tp,ch=PROC[s]; pro.append(trim_soft(rubber(x,ST(st),tp,ch,"cm"),-55,0.03,0.15))
    text=" ".join(respell(B[b][1]) for b in BEATS if B[b][0]==s)
    r=role_measure(raw,text,"raw"+s); p=role_measure(pro,text,"pro"+s); xr=np.concatenate(raw); xp=np.concatenate(pro)
    out[s]={"raw":r,"processed":p,"settings":dict(semitones=PROC[s][0],tempo=PROC[s][1],chain=PROC[s][2]),"f0_jump_pct":(jump(xr),jump(xp)),"hf8k_pct":(hf8(xr),hf8(xp)),"dur_ratio":round(len(xp)/len(xr),2),
          "edge_abrupt_after_fade":artefact_stats(np.concatenate([fade(a) for a in pro]))["abrupt_events"]}
    print(s,json.dumps(out[s]))
json.dump(out,open(f"{W}/c_processing.json","w"),indent=1)
