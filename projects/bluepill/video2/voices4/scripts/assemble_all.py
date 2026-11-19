"""Assemble every scene with smooth joins. Usage: assemble_all.py <name>   name in: A_v4 A_v2 B_bp B_lib C diag
 - A/B (one continuous render per passage): no cuts inside a passage. A slow gain ride (linear in dB between beat midpoints, max +-4 dB) pulls each beat toward the scene's median beat loudness
   without any splice; the two passages are joined with fade-out 60 ms / fade-in 30 ms into a continuous room-tone bed.
 - C and diag (separate renders per line): per-line gain to -19 LUFS (max +-9 dB), 15 ms fade-in / 25 ms fade-out on every line, gaps 0.25-0.4 s, continuous room-tone bed (-62 dBFS) under everything.
Outputs mp3 in voices4/ and a JSON with timeline + indicators in _work/."""
import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from asm import *
from scene_texts import B
name=sys.argv[1] if len(sys.argv)>1 else ""
def gap_fn(a,b): return 0.25 if a!="NARR" and b!="NARR" else (0.4 if a=="NARR" and b=="NARR" else 0.32)
def ride(x,spans,limit=4.0):
    """spans: {beat:(t0,t1)}. gain knots at beat midpoints."""
    ks=[];g=[]
    L={b:line_lufs(x[int(max(0,t0-0.05)*SR):int((t1+0.1)*SR)]) for b,(t0,t1) in spans.items()}
    tgt=float(np.median(list(L.values())))
    for b,(t0,t1) in sorted(spans.items(),key=lambda kv:kv[1][0]): ks.append((t0+t1)/2); g.append(float(np.clip(tgt-L[b],-limit,limit)))
    gt=np.interp(np.arange(len(x))/SR,ks,g); return x*10**(gt/20).astype(np.float32),{b:(round(L[b],1),round(float(np.interp((spans[b][0]+spans[b][1])/2,ks,g)),1)) for b in spans}
def passage_scene(stem,dst):
    al=json.load(open(f"{W}/align_{stem}.json")); P=[]; info={}
    for i in range(2):
        x=load(f"{OUT}/lines/{stem}_passage{i+1}.mp3"); spans={int(b):tuple(t) for b,t in al[str(i)]["times"].items() if t}
        x,gi=ride(x,spans); info.update(gi); 
        y=trim_soft(x,-55,0.03,0.25); P.append(("P%d"%(i+1),y))
    segs=[(r,fade(y,0.030 if r=="P2" else 0.015,0.06)) for r,y in P]
    t=0.0; parts=[]
    for k,(r,y) in enumerate(segs): parts.append((int(t*SR),y)); t+=len(y)/SR+0.55
    bus=np.zeros(int(t*SR)+SR//2,np.float32)
    for s,y in parts: bus[s:s+len(y)]+=y
    I=final_mp3(bus,dst); return I,info
def rubber(x,pitch=1.0,tempo=1.0,chain="",tag="p"):
    write_wav(f"{W}/_{tag}_in.wav",x)
    af=f"rubberband=tempo={tempo:.5f}:pitch={pitch:.5f}:formant=shifted:pitchq=quality:transients=smooth:window=long:phase=laminar"+(","+chain if chain else "")
    subprocess.run([FF,"-y","-v","error","-i",f"{W}/_{tag}_in.wav","-af",af,"-ar",str(SR),f"{W}/_{tag}_out.wav"],check=True); return load(f"{W}/_{tag}_out.wav")
ST=lambda s:2**(s/12)
PROC={ # role: (semitones, tempo, extra ffmpeg chain)  -- mild by design; timbre family stays Daniel's
 "ODY":(-1.0,1.0,"equalizer=f=250:t=q:w=1:g=1.0"),
 "POLY":(-3.5,0.88,"equalizer=f=130:t=q:w=1:g=2.5,treble=g=-2.5:f=4500"),
 "CYC2":(-1.0,0.94,"highpass=f=110,lowpass=f=5200,equalizer=f=2500:t=q:w=1:g=-2,acompressor=threshold=0.063:ratio=3:attack=15:release=120:makeup=1.3"),
 "CREW":(2.5,1.04,"highpass=f=90,treble=g=2:f=4000"),
}
def lines_scene(kind,dst):
    segs=[];meta=[]
    for b in BEATS:
        s=B[b][0]
        if kind=="C":
            f=f"{V3}/proof_lines/beat{b:02d}_NARR.mp3" if s=="NARR" else f"{OUT}/lines/C_beat{b:02d}_{s}.mp3"
            x=load(f); x=trim_soft(x,-55,0.03,0.15)
            if s!="NARR": st,tp,ch=PROC[s]; x=rubber(x,ST(st),tp,ch,"c"); x=trim_soft(x,-55,0.03,0.15)
        else:   # diag: round-2 per-line renders (voices3, William's BP voices, speeds 0.8-0.9 as before), only the joins are new
            x=trim_soft(load(f"{V3}/proof_lines/beat{b:02d}_{s}.mp3"),-55,0.03,0.12)
        L=line_lufs(x); g=float(np.clip(TARGET-L,-9,9)); x=x*10**(g/20); meta.append((b,s,round(L,1),round(g,1))); segs.append((s,x))
    segs=[(s,fade(x,0.015,0.025)) for s,x in segs]
    bus,tl=build_timeline(segs,gap_fn); I=final_mp3(bus,dst); return I,{"timeline":tl,"lines":meta}
if __name__=="__main__":
    dst={"A_v4":"methodA_v4_scene.mp3","A_v2":"methodA_v2_scene.mp3","B_bp":"methodB_bp_scene.mp3","B_lib":"methodB_scene.mp3","C":"methodC_scene.mp3","diag":"diag_bp_voices_smooth.mp3"}[name]
    p=f"{OUT}/{dst}"
    if name in("A_v4","A_v2"): I,info=passage_scene(name,p)
    elif name=="B_bp": I,info=passage_scene("B_bp_eleven_v4",p)
    elif name=="B_lib": I,info=passage_scene("B_lib_eleven_v4",p)
    else: I,info=lines_scene(name,p)
    x=load(p); r={"file":dst,"loudnorm_I_LRA_TP":I,"duration_s":round(len(x)/SR,1),"artefacts":artefact_stats(x),"detail":info}; json.dump(r,open(f"{W}/assembled_{name}.json","w"),indent=1,default=str)
    print(name,dst,I,round(len(x)/SR,1),r["artefacts"])
