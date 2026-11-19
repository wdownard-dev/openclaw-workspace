"""One-word-line flatness check. faster-whisper small.en (cached model, local) gives word timings; F0 inside the target word is measured with the
wide-range tracker (3-point median filter), reporting voiced frames, median Hz and the p10-p90 F0 range in semitones. FLAT = range < 2.0 st with >= 6 voiced frames;
too few voiced frames = UNRELIABLE. Usage: python -I words.py <out.json> <text-json> file ... ; targets come from cfg.ONEWORDS by clip role key (guessed from the file name)."""
import sys, os, json, re, difflib
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(HERE)),"voices","scripts"))
import numpy as np, metrics, metrics2
from cfg import *
os.environ.setdefault("HF_HOME","/home/williamdownard/openclaw-sites/models")
from faster_whisper import WhisperModel
def key_of(name):
    if name.startswith("POLY_design"): return "POLY_NOBODY"
    for k in ("POLY_NOBODY","POLY_RAM","POLY_PRAYER"):
        if k in name: return k
    for r in ("CYC2","CREW","ODY"):
        if name.startswith(r+"_") or f"_{r}" in name: return r
    return None
def norm(w): return re.sub(r"[^a-z0-9']","",w.lower())
if __name__=="__main__":
    out,tj,*files=sys.argv[1:]; texts=json.load(open(tj)); res=json.load(open(out)) if os.path.exists(out) else {}
    model=WhisperModel("small.en",device="cpu",compute_type="int8",download_root="/home/williamdownard/openclaw-sites/models")
    for f in files:
        b=os.path.basename(f)
        if b in res: continue
        k=key_of(b); tg=ONEWORDS.get(k,[])
        segs,_=model.transcribe(f,word_timestamps=True,beam_size=1,language="en",condition_on_previous_text=False)
        W=[w for s in segs for w in s.words]; heard=" ".join(w.word.strip() for w in W)
        x=metrics.load(f); H=800; nf=len(x)//H; rdb=20*np.log10(np.maximum(np.sqrt((x[:nf*H].reshape(nf,H)**2).mean(1)),1e-9)); act=rdb[rdb>-50]; med=float(np.median(act))
        ours=[norm(w) for w in re.findall(r"\S+",texts[b])]; hw=[norm(w.word) for w in W]
        sm=difflib.SequenceMatcher(None,ours,hw,autojunk=False); mp={}
        for a,b2,n in sm.get_matching_blocks():
            for i in range(n): mp[a+i]=b2+i
        entry=dict(heard=heard,words=[])
        raw=re.findall(r"\S+",texts[b])
        for t in tg:
            idx=[i for i,w in enumerate(raw) if norm(w)==norm(t)]
            if not idx: continue
            i=idx[-1] if k in("CYC2",) else idx[0]
            if i not in mp: entry["words"].append(dict(word=t,status="NOT FOUND by aligner")); continue
            w=W[mp[i]]; s0,s1=int(w.start*16000),int(w.end*16000); seg=x[s0:s1]
            fr=metrics2.f0_frames(seg,lambda s:True,1024,160,int(16000/400),int(16000/40),True,True)
            v=12*np.log2(np.array([f for _,f in fr])/100) if fr else np.array([])
            if len(v)>=3: v=np.array([np.median(v[max(0,j-1):j+2]) for j in range(len(v))])
            rng=float(np.percentile(v,90)-np.percentile(v,10)) if len(v)>=6 else None
            lvl=float(20*np.log10(max(np.sqrt((seg**2).mean()),1e-9)))-med
            status="UNRELIABLE (few voiced frames)" if rng is None else ("FLAT" if rng<2.0 else "ok")
            entry["words"].append(dict(word=t,start=round(w.start,2),end=round(w.end,2),dur=round(w.end-w.start,2),voiced_frames=len(v),f0_median_hz=round(float(100*2**(np.median(v)/12))) if len(v) else None,f0_p10_p90_st=round(rng,2) if rng is not None else None,level_vs_clip_median_db=round(lvl,1),status=status))
        res[b]=entry; print(b,entry["words"]); json.dump(res,open(out,"w"),indent=1)
