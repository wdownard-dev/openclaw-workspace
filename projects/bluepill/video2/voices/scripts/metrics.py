"""Measure clips like the reference teardown (analysis_teardown_scripts/audio.js): F0 by autocorrelation on 16 kHz mono, frame 512, hop 320,
lags 53-230 (70-300 Hz), corr>0.5, voiced = 50 ms frame above (median - 6 dB); pitch spread = std of voiced F0 in semitones (re 100 Hz).
Usage: /home/williamdownard/openclaw-sites/clips-venv/bin/python -I metrics.py <out.json> <text-json> file1.mp3 file2.mp3 ...
text-json maps file basename -> spoken text (for words per minute). Loudness via ffmpeg ebur128 (integrated LUFS, LRA)."""
import sys, json, subprocess, re, os
import numpy as np
FF="/home/williamdownard/openclaw-sites/bin/ffmpeg"
def load(path):
    r=subprocess.run([FF,"-v","error","-i",path,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True)
    return np.frombuffer(r.stdout,dtype=np.int16).astype(np.float32)/32768
def ebur(path):
    r=subprocess.run([FF,"-hide_banner","-nostats","-i",path,"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True)
    t=r.stderr.split("Summary:")[-1]
    g=lambda k: float(re.search(k+r":\s+(-?[\d.]+)",t).group(1)) if re.search(k+r":\s+(-?[\d.]+)",t) else None
    return g("I"),g("LRA"),g("Peak")
def measure(path,text):
    x=load(path); SR=16000; n=len(x); HF=800; nf=n//HF
    rms=np.sqrt((x[:nf*HF].reshape(nf,HF)**2).mean(1)); rdb=20*np.log10(np.maximum(rms,1e-9))
    med=np.percentile(rdb,50)
    active=np.where(rdb>med-18)[0]                      # speech span: first to last frame within 18 dB of the median
    span=(active[-1]-active[0]+1)*0.05 if len(active) else n/SR
    # pauses inside the span (frames more than 18 dB under the median), runs of >=0.3 s
    thr=med-18; runs=[];run=0
    for f in range(active[0] if len(active) else 0,(active[-1]+1) if len(active) else nf):
        if rdb[f]<thr: run+=1
        else:
            if run: runs.append(run*0.05)
            run=0
    pauses=[p for p in runs if p>=0.3]
    FL,HP=512,320; f0=[]
    for s in range(0,n-FL,HP):
        fi=s//HF
        if fi>=nf or rdb[fi]<med-6: continue
        seg=x[s:s+FL]; e=float((seg*seg).sum())
        if e<1e-6: continue
        # normalised autocorrelation (same normalisation as the reference: divide by frame energy)
        ac=np.correlate(seg,seg,"full")[FL-1:]/e
        lo,hi=53,230
        lag=lo+int(np.argmax([ (seg[:FL-l]*seg[l:]).sum()/e for l in range(lo,hi+1)]))
        c=(seg[:FL-lag]*seg[lag:]).sum()/e
        if c>0.5: f0.append(SR/lag)
    st=12*np.log2(np.array(f0)/100) if f0 else np.array([])
    words=len(re.findall(r"[A-Za-z0-9']+",text))
    lufs,lra,peak=ebur(path)
    return dict(duration_s=round(n/SR,2),speech_span_s=round(float(span),2),words=words,
        wpm_total=round(words/(n/SR)*60),wpm_active=round(words/span*60) if span else None,
        pauses_ge_0_3s=len(pauses),pause_total_s=round(float(sum(pauses)),2),
        f0_voiced_frames=int(len(f0)),pitch_spread_st=round(float(st.std()),2) if len(st) else None,
        f0_median_hz=round(float(100*2**(np.median(st)/12))) if len(st) else None,
        lufs=lufs,lra_lu=lra,true_peak_db=peak,frame_db_std_voiced=round(float(rdb[rdb>med].std()),2))
if __name__=="__main__":
    out,tj,*files=sys.argv[1:]
    texts=json.load(open(tj)); res={}
    if os.path.exists(out): res=json.load(open(out))
    for f in files:
        b=os.path.basename(f)
        if b in res: continue
        res[b]=measure(f,texts.get(b,"")); print(b,res[b]); json.dump(res,open(out,"w"),indent=1)
