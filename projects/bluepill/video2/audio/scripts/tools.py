"""Analysis helpers: whisper alignment of a rendered passage back to script beats, per-role measures (F0, spectral, loudness)."""
import os,sys,re,json,difflib; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
os.environ.setdefault("HF_HOME","/home/williamdownard/openclaw-sites/models")
_M=None
def model():
    global _M
    if _M is None:
        from faster_whisper import WhisperModel
        _M=WhisperModel("small.en",device="cpu",compute_type="int8",download_root="/home/williamdownard/openclaw-sites/models")
    return _M
def norm(w): return re.sub(r"[^a-z0-9']","",w.lower().replace("’","'"))
def align(path,beat_texts):
    """beat_texts: list of (beat,text). Returns {beat:(t0,t1)} from whisper word times matched to the script words (difflib), plus coverage."""
    segs,_=model().transcribe(path,word_timestamps=True,beam_size=1,language="en",condition_on_previous_text=False)
    W=[w for s in segs for w in s.words if norm(w.word)]
    heard=[norm(w.word) for w in W]; want=[];owner=[]
    for b,t in beat_texts:
        for w in t.split():
            if norm(w): want.append(norm(w)); owner.append(b)
    sm=difflib.SequenceMatcher(None,want,heard,autojunk=False); times={}
    for a,bb,n in sm.get_matching_blocks():
        for k in range(n):
            b=owner[a+k]; w=W[bb+k]; t0,t1=times.get(b,(1e9,-1)); times[b]=(min(t0,w.start),max(t1,w.end))
    cov=sum(n for _,_,n in sm.get_matching_blocks())/max(1,len(want))
    return times,cov,[w.word for w in W]
def spec(x,sr=SR):
    n=2048; fr=[x[i:i+n]*np.hanning(n) for i in range(0,len(x)-n,1024)]
    rd=np.array([db(np.sqrt((f**2).mean())) for f in fr]); keep=rd>(rd.max()-30)
    S=np.mean([np.abs(np.fft.rfft(f))**2 for f,k in zip(fr,keep) if k],axis=0); fq=np.fft.rfftfreq(n,1/sr)
    return float((fq*S).sum()/S.sum()),float(S[fq>4000].sum()/S.sum())
def role_measure(segments,text,tag="role"):
    """segments: list of numpy arrays (44.1k) of one role. Concatenate with 0.3 s silence, measure like round 2 (wide F0 mean/median Hz, spread st, wpm, LUFS) + centroid and >4 kHz share."""
    x=np.concatenate([np.concatenate([s,np.zeros(int(0.3*SR),np.float32)]) for s in segments]); p=f"{W}/_role_{tag}.wav"; write_wav(p,x)
    m=metrics2.measure2(p,text); c,h4=spec(x)
    return dict(f0_mean_hz=m["f0w_mean_hz"],f0_median_hz=m["f0w_median_hz"],f0_spread_st=m["pitch_spread_st"],wpm=m["wpm"],lufs=m["lufs"],centroid_hz=round(c),hf4k_pct=round(100*h4,2),seconds=round(len(x)/SR,1))
def spans_audio(x,spans,pad=0.0):
    return [x[max(0,int((a-pad)*SR)):int((b+pad)*SR)] for a,b in spans]
