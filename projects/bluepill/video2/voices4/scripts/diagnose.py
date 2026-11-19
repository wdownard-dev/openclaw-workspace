"""Step 1: measurement-based diagnosis of the round-2 proof scene (voices3). Writes _work/diagnosis.json. No API calls."""
import os,sys,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
P3=f"{V3}/proof_lines"; A=json.load(open(f"{V3}/_work/assemble.json")); B=parse_script()
SET3={"NARR":1.0,"ODY":1.0,"POLY":0.8,"CYC2":0.85,"CREW":0.9}
def spec(x,sr=SR):
    """spectral centroid and share of energy above 4 kHz / 8 kHz over speech frames (2048 FFT)."""
    n=2048; fr=[x[i:i+n]*np.hanning(n) for i in range(0,len(x)-n,1024)]
    rd=np.array([db(np.sqrt((f**2).mean())) for f in fr]); keep=rd>(rd.max()-30)
    S=np.mean([np.abs(np.fft.rfft(f))**2 for f,k in zip(fr,keep) if k],axis=0); fq=np.fft.rfftfreq(n,1/sr)
    return float((fq*S).sum()/S.sum()),float(S[fq>4000].sum()/S.sum()),float(S[fq>8000].sum()/S.sum())
def edges(x,sr=SR):
    """lead/trail silence under -50 dB (20 ms frames); onset rise = time from -40 dB-rel-peak to -10 dB-rel-peak in 5 ms RMS windows; noise floor = 5th pct frame level."""
    r,H=rms_db_frames(x,20); act=np.where(r>-50)[0]; lead=act[0]*0.02; trail=(len(r)-1-act[-1])*0.02
    r5,H5=rms_db_frames(x,5); pk=r5.max(); a=np.where(r5>pk-40)[0][0]; b=a+np.where(r5[a:]>pk-10)[0][0]
    c=np.where(r5>pk-40)[0][-1]; d=c-np.where(r5[:c+1][::-1]>pk-10)[0][0]
    return dict(lead_s=round(lead,3),trail_s=round(trail,3),onset_rise_ms=round((b-a)*5),offset_fall_ms=round((c-d)*5),noise_floor_db=round(float(np.percentile(r,5)),1),
                first_sample_db=round(db(abs(x[0])),1),last_sample_db=round(db(abs(x[-1])),1),first5ms_db=round(db(np.sqrt((x[:220]**2).mean())),1),last5ms_db=round(db(np.sqrt((x[-220:]**2).mean())),1))
def jitter(x):
    """share of voiced-frame pairs whose F0 jumps by more than 2 semitones (tracker or artefact jumps), 40-400 Hz wide tracker at 16 kHz."""
    import metrics
    x16=load_16(x); fr=metrics2.f0_frames(x16,lambda s:True,1024,160,int(16000/400),int(16000/40),True,True)
    if len(fr)<10: return None
    v=12*np.log2(np.array([f for _,f in fr])/100); return round(float((np.abs(np.diff(v))>2).mean()*100),1)
def load_16(x):
    write_wav(f"{W}/_j.wav",x); return metrics.load(f"{W}/_j.wav")
res={"lines":{},"roles":{},"joins":[],"scene":{}}
raw={}
for b in BEATS:
    s=B[b][0]; x=load(f"{P3}/beat{b:02d}_{s}.mp3"); raw[b]=x
    c,h4,h8=spec(x); e=edges(x)
    res["lines"][b]=dict(spk=s,speed=SET3[s],dur_s=round(len(x)/SR,2),lufs=lufs(x),centroid_hz=round(c),hf4k_pct=round(100*h4,2),hf8k_pct=round(100*h8,3),f0_jump_pct=jitter(x),**e)
# per speaker aggregates
for s in SET3:
    L=[v for v in res["lines"].values() if v["spk"]==s]
    res["roles"][s]={k:round(float(np.mean([l[k] for l in L if l[k] is not None])),2) for k in ("lufs","centroid_hz","hf4k_pct","hf8k_pct","f0_jump_pct","onset_rise_ms","offset_fall_ms","noise_floor_db","lead_s","trail_s")}
# scene joins: decode the final proof scene and look at each join
sc=load(f"{V3}/proof_scene.mp3"); tl=A["timeline"]; med_d=float(np.median(np.abs(np.diff(sc))[np.abs(sc[1:])>0.01]))
for i in range(len(tl)-1):
    b0,s0,t0,e0=tl[i]; b1,s1,t1,e1=tl[i+1]; ge=int(e0*SR); gs=int(t1*SR)
    pre=sc[ge-int(0.4*SR):ge]; post=sc[gs:gs+int(0.4*SR)]; gap=sc[ge+int(0.03*SR):gs-int(0.03*SR)]
    # step at the cut: amplitude within last/first 2 ms of the speech (what the gate cut off) and max sample-to-sample diff within +-3 ms of both boundaries
    w=int(0.003*SR); d_out=np.abs(np.diff(sc[ge-w:ge+w])).max(); d_in=np.abs(np.diff(sc[gs-w:gs+w])).max()
    res["joins"].append(dict(a=f"{b0}{s0}",b=f"{b1}{s1}",gap_s=round(t1-e0,2),end_amp_db=round(db(np.abs(sc[ge-int(0.002*SR):ge]).max()),1),start_amp_db=round(db(np.abs(sc[gs:gs+int(0.002*SR)]).max()),1),
        max_step_out_x_med=round(float(d_out/med_d),1),max_step_in_x_med=round(float(d_in/med_d),1),gap_rms_db=round(db(np.sqrt((gap**2).mean())),1),
        last400ms_db=round(db(np.sqrt((pre**2).mean())),1),first400ms_db=round(db(np.sqrt((post**2).mean())),1),level_step_db=round(db(np.sqrt((post**2).mean()))-db(np.sqrt((pre**2).mean())),1),
        spk_change=s0!=s1))
J=res["joins"]; res["scene"]=dict(n_joins=len(J),gap_rms_db_mean=round(float(np.mean([j["gap_rms_db"] for j in J])),1),
    abs_level_step_db_mean=round(float(np.mean([abs(j["level_step_db"]) for j in J])),1),abs_level_step_db_max=round(float(max(abs(j["level_step_db"]) for j in J)),1),
    abs_level_step_speaker_changes_mean=round(float(np.mean([abs(j["level_step_db"]) for j in J if j["spk_change"]])),1),
    end_amp_db_mean=round(float(np.mean([j["end_amp_db"] for j in J])),1),start_amp_db_mean=round(float(np.mean([j["start_amp_db"] for j in J])),1),
    gaps_s=sorted({j["gap_s"] for j in J}),med_sample_diff=round(med_d,4))
# in-line pause lengths (what natural pace looks like) for POLY/CYC2 vs fixed gaps
def inline_pauses(x):
    r,H=rms_db_frames(x,25); on=np.where(r>-50)[0]; r=r[on[0]:on[-1]+1]; med=np.median(r[r>-50]); runs=[];n=0
    for v in r:
        if v<med-18: n+=1
        else:
            if n: runs.append(n*0.025)
            n=0
    return [p for p in runs if p>=0.2]
res["inline_pauses"]={s:[round(p,2) for b in BEATS if B[b][0]==s for p in inline_pauses(raw[b])] for s in SET3}
json.dump(res,open(f"{W}/diagnosis.json","w"),indent=1); 
print(json.dumps(res["roles"],indent=0)); print(json.dumps(res["scene"])); 
for j in J: print(j)
for b,v in res["lines"].items(): print(b,v["spk"],v["speed"],v["dur_s"],"LUFS",v["lufs"],"cent",v["centroid_hz"],"hf4k",v["hf4k_pct"],"lead",v["lead_s"],"trail",v["trail_s"],"on",v["onset_rise_ms"],"off",v["offset_fall_ms"],"nf",v["noise_floor_db"],"fs",v["first_sample_db"],"ls",v["last_sample_db"])
print(res["inline_pauses"])
