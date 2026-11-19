"""Step 3/4 assembly. Trim edges, match loudness per speaker (all of a speaker's lines get the same gain so that speaker's integrated loudness = -19 LUFS),
join with 0.25-0.4 s gaps, then 2-pass loudnorm to -19 LUFS integrated, true peak <= -1.5 dBFS. Also builds the neighbours A/B (CYC2 pitch shifted with rubberband).
Run with clips-venv python -I."""
import os,sys,json,subprocess,re,wave
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np, metrics
from proof_gen import BEATS, parse
SR=44100; TARGET=-19.0
def load(path):
    r=subprocess.run([FF,"-v","error","-i",path,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True); return np.frombuffer(r.stdout,dtype=np.float32).copy()
def trim(x,thr_db=-50):
    H=441; n=len(x)//H; r=20*np.log10(np.maximum(np.sqrt((x[:n*H].reshape(n,H)**2).mean(1)),1e-9)); idx=np.where(r>thr_db)[0]
    return x[max(0,idx[0]*H-int(0.02*SR)):min(len(x),(idx[-1]+1)*H+int(0.04*SR))]
def write_wav(path,x):
    with wave.open(path,"wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes())
def lufs(x,tmp):
    write_wav(tmp,x); return metrics.ebur(tmp)
def shift(x,semi,tmp):
    write_wav(tmp+"_in.wav",x); f=2**(semi/12)
    subprocess.run([FF,"-y","-v","error","-i",tmp+"_in.wav","-af",f"rubberband=pitch={f:.5f}:formant=shifted:transients=smooth","-ar",str(SR),tmp+"_out.wav"],check=True)
    return load(tmp+"_out.wav")
def final_mp3(x,dst,tmp):
    write_wav(tmp,x)
    r=subprocess.run([FF,"-hide_banner","-nostats","-i",tmp,"-af",f"loudnorm=I={TARGET}:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True)
    j=json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}")+1])
    af=(f"loudnorm=I={TARGET}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,"
        "alimiter=limit=0.89:level=false")
    subprocess.run([FF,"-y","-v","error","-i",tmp,"-af",af,"-ar","44100","-ac","1","-c:a","libmp3lame","-b:a","192k",dst],check=True)
    return metrics.ebur(dst)
def gap_after(spk,nxt): return 0.25 if spk!="NARR" and nxt!="NARR" else (0.4 if spk=="NARR" and nxt=="NARR" else 0.32)
if __name__=="__main__":
    B=parse(); lines=[(b,B[b][0]) for b in BEATS]; X={}
    for b,s in lines: X[b]=trim(load(f"{OUT}/proof_lines/beat{b:02d}_{s}.mp3"))
    # per-speaker gain
    gain={}; meas={}
    for spk in ("NARR","ODY","POLY","CYC2","CREW"):
        cat=np.concatenate([np.concatenate([X[b],np.zeros(int(0.3*SR),np.float32)]) for b,s in lines if s==spk]); I,lra,tp=lufs(cat,f"{W}/_tmp.wav")
        gain[spk]=TARGET-I; meas[spk]={"raw_lufs":I,"gain_db":round(gain[spk],2),"n_lines":sum(1 for b,s in lines if s==spk)}
        print(spk,meas[spk])
    G={b:X[b]*10**(gain[s]/20) for b,s in lines}
    def build(shift_semi=0,subset=None,tag=""):
        parts=[];gaps=[];L=[(b,s) for b,s in lines if subset is None or b in subset]; t=0.0; timeline=[]
        for i,(b,s) in enumerate(L):
            x=G[b]
            if shift_semi and s=="CYC2": x=shift(x,shift_semi,f"{W}/_sh")
            timeline.append((b,s,round(t,2),round(t+len(x)/SR,2))); parts.append(x); t+=len(x)/SR
            if i+1<len(L): g=gap_after(s,L[i+1][1]); parts.append(np.zeros(int(g*SR),np.float32)); t+=g
        return np.concatenate(parts),timeline
    scene,tl=build(); I=final_mp3(scene,f"{OUT}/proof_scene.mp3",f"{W}/_scene.wav"); print("proof_scene",I)
    json.dump({"gain":meas,"timeline":tl,"final_lufs_lra_tp":I},open(f"{W}/assemble.json","w"),indent=1)
    # chorus-shifted variant of the full scene
    sc2,_=build(3); I2=final_mp3(sc2,f"{OUT}/proof_scene_chorus_plus3st.mp3",f"{W}/_scene2.wav"); print("proof_scene_chorus_plus3st",I2)
    # A/B neighbours 37-39 (+ nothing else), narrator-free; A unshifted, B +2 st, C +3 st
    os.makedirs(f"{OUT}/ab",exist_ok=True); sub={37,38,39}; outs=[]
    for tag,semi in (("A_unshifted",0),("B_chorus_plus2st",2),("C_chorus_plus3st",3)):
        x,_=build(semi,sub); Ii=final_mp3(x,f"{OUT}/ab/neighbours_{tag}.mp3",f"{W}/_ab.wav"); print(tag,Ii); outs.append(x)
    sil=np.zeros(int(1.5*SR),np.float32); combo=np.concatenate([outs[0],sil,outs[1],sil,outs[2]]); I3=final_mp3(combo,f"{OUT}/ab/neighbours_ABC.mp3",f"{W}/_ab.wav"); print("ABC",I3)
