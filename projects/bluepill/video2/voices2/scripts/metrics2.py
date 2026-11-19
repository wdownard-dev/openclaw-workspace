"""Round-2 measures (self-contained; loudness helper imported from round 1, unchanged).
Differences from round 1 metrics.py, needed because Voice Design previews carry seconds of digital silence between lines and at the end:
 - speech span = first to last 50 ms frame above -50 dBFS (wpm = words / span; wpm_raw uses the file length);
 - level reference = median of frames above -50 dBFS inside the span (round 1 used the median of all frames; identical for continuous speech);
 - pauses >= 0.3 s = runs of frames more than 18 dB under that median (same rule as the reference audio.js), per minute of span, and as % of span;
 - pitch spread = std of voiced F0 in semitones (reference definition: autocorrelation, lags 53-230 at 16 kHz = 70-300 Hz, corr > 0.5, frame 512, hop 320,
   voiced = frame within 6 dB of the median); computed with an FFT autocorrelation (same numbers as the direct sum);
 - wide F0 (40-400 Hz, Hann window 1024, lowest local peak within 90% of the maximum to avoid octave errors): mean/median in Hz and semitones re 100 Hz, for very deep or high voices;
 - short segments (voiced runs split at gaps >= 0.25 s) of <= 0.9 s: F0 p10-p90 range in semitones (robust to octave errors) as a flatness check for one-word lines.
Usage: python -I metrics2.py <out.json> <text-json> file ...   (text-json: basename -> spoken text with audio tags removed)"""
import sys, os, json, re
sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),"voices","scripts"))
import numpy as np, metrics
SR=16000
def acf(seg):
    n=len(seg); F=np.fft.rfft(seg,2*n); return np.fft.irfft(F*np.conj(F))[:n]
def f0_frames(x,mask_fn,FL,HP,lo,hi,window,wide):
    out=[]
    for s in range(0,len(x)-FL,HP):
        if not mask_fn(s): continue
        seg=x[s:s+FL]*(np.hanning(FL) if window else 1); e=float((seg*seg).sum())
        if e<1e-6: continue
        ac=acf(seg)/e; c=ac[lo:hi+1]
        if not wide:
            lag=lo+int(np.argmax(c)); 
            if c.max()>0.5: out.append((s,SR/lag))
        else:
            if c.max()<0.5: continue
            thr=0.9*c.max(); idx=next((i for i in range(1,len(c)-1) if c[i]>=thr and c[i]>=c[i-1] and c[i]>=c[i+1]),None)
            if idx is not None: out.append((s,SR/(lo+idx)))
    return out
def measure2(path,text):
    x=metrics.load(path); n=len(x); HF=800; nf=n//HF
    rdb=20*np.log10(np.maximum(np.sqrt((x[:nf*HF].reshape(nf,HF)**2).mean(1)),1e-9))
    act=np.where(rdb>-50)[0]; a0,a1=act[0],act[-1]; span=(a1-a0+1)*0.05
    med=float(np.median(rdb[a0:a1+1][rdb[a0:a1+1]>-50])); thr=med-18
    runs=[];run=0
    for f in range(a0,a1+1):
        if rdb[f]<thr: run+=1
        else:
            if run: runs.append(run*0.05)
            run=0
    pauses=[p for p in runs if p>=0.3]
    mask=lambda s:(s//HF)<nf and rdb[s//HF]>=med-6
    ref=f0_frames(x,mask,512,320,53,230,False,False)
    st=12*np.log2(np.array([f for _,f in ref])/100) if ref else np.array([])
    wide=f0_frames(x,mask,1024,320,int(SR/400),int(SR/40),True,True)
    ws=12*np.log2(np.array([f for _,f in wide])/100) if wide else np.array([])
    words=len(re.findall(r"[A-Za-z0-9']+",text)); lufs,lra,peak=metrics.ebur(path)
    m=dict(duration_s=round(n/SR,2),span_s=round(float(span),2),words=words,wpm=round(words/span*60),wpm_raw=round(words/(n/SR)*60),
        pauses_ge_0_3s=len(pauses),pause_total_s=round(float(sum(pauses)),2),pauses_per_min=round(len(pauses)/(span/60),1),pause_pct=round(100*sum(pauses)/span,1),
        pitch_spread_st=round(float(st.std()),2) if len(st) else None,f0_voiced_frames=len(st),
        f0w_mean_st=round(float(ws.mean()),2) if len(ws) else None,f0w_median_st=round(float(np.median(ws)),2) if len(ws) else None,
        f0w_mean_hz=round(float(100*2**(ws.mean()/12))) if len(ws) else None,f0w_median_hz=round(float(100*2**(np.median(ws)/12))) if len(ws) else None,
        lufs=lufs,lra_lu=lra,true_peak_db=peak)
    # short segments
    H=int(SR*0.025); nh=n//H; r2=20*np.log10(np.maximum(np.sqrt((x[:nh*H].reshape(nh,H)**2).mean(1)),1e-9)); on=r2>med-18; gap=int(0.25/0.025)
    segs=[];i=0
    while i<nh:
        if on[i]:
            j=i
            while j<nh and (on[j] or on[j:j+gap].any()): j+=1
            segs.append((i*0.025,j*0.025)); i=j
        else: i+=1
    short=[]
    for a,b in segs:
        if 0.15<=b-a<=0.9:
            s0,s1=int(a*SR),int(b*SR); fr=f0_frames(x[s0:s1],lambda s:True,1024,160,int(SR/400),int(SR/40),True,True)
            v=12*np.log2(np.array([f for _,f in fr])/100) if fr else np.array([])
            short.append(dict(start=round(a,2),dur=round(b-a,2),voiced_frames=len(v),f0_p10_p90_st=round(float(np.percentile(v,90)-np.percentile(v,10)),2) if len(v)>=8 else None,f0_median_hz=round(float(100*2**(np.median(v)/12))) if len(v) else None))
    m["n_segments"]=len(segs); m["short_segments"]=short
    return m
if __name__=="__main__":
    out,tj,*files=sys.argv[1:]; texts=json.load(open(tj)); res=json.load(open(out)) if os.path.exists(out) else {}
    for f in files:
        b=os.path.basename(f)
        if b in res: continue
        res[b]=measure2(f,texts.get(b,"")); print(b,{k:res[b][k] for k in ("span_s","wpm","pitch_spread_st","f0w_median_hz","lra_lu","pauses_per_min","pause_pct")}); json.dump(res,open(out,"w"),indent=1)
