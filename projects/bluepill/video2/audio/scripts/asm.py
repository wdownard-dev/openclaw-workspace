"""Smooth-join assembly shared by all methods. No hard trims: 10-20 ms fades on every segment, a continuous room-tone bed under the whole scene (so no gap is digital silence),
equal-power crossfades (40 ms) wherever two renders are butted together, per-line loudness match toward -19 LUFS, two-pass loudnorm for the final mp3.
Also artefact_stats(): the same kind of join indicators used in the round-2 diagnosis."""
import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import json
def fade(x,fi=0.015,fo=0.02):
    x=x.copy(); a=int(fi*SR); b=int(fo*SR)
    if a: x[:a]*=np.sin(np.linspace(0,np.pi/2,a))**2
    if b: x[-b:]*=np.cos(np.linspace(0,np.pi/2,b))**2
    return x
def trim_soft(x,thr_db=-55,pre=0.03,post=0.12):
    """cut to speech with generous margins (post margin keeps natural decay), then the caller fades the edges."""
    r,H=rms_db_frames(x,10); idx=np.where(r>thr_db)[0]
    if not len(idx): return x
    return x[max(0,int(idx[0]*H-pre*SR)):min(len(x),int((idx[-1]+1)*H+post*SR))]
def line_lufs(x):
    try:
        v=lufs(x if len(x)>int(0.6*SR) else np.concatenate([x,np.zeros(int(0.6*SR)-len(x),np.float32)]))
        if v is not None and v>-60: return v
    except Exception: pass
    r,H=rms_db_frames(x,50); a=r[r>r.max()-25]; return float(a.mean())-3
def room_tone(seconds,level_db=-62,seed=7):
    """pink-ish noise, band-limited 70 Hz-5 kHz, level_db RMS, with a slow 0.15 Hz level drift of +-1 dB so it never sounds like a loop."""
    n=int(seconds*SR); rng=np.random.default_rng(seed); X=np.fft.rfft(rng.standard_normal(n)); f=np.fft.rfftfreq(n,1/SR); f[0]=1
    g=1/np.sqrt(f); g[(f<70)|(f>5000)]*=0.05; y=np.fft.irfft(X*g,n).astype(np.float32); y/=np.sqrt((y**2).mean())
    y*=10**(level_db/20)*(1+0.12*np.sin(2*np.pi*0.15*np.arange(n)/SR)); return y.astype(np.float32)
def xfade(a,b,ms=40):
    """equal-power crossfade of the tail of a into the head of b (overlap of ms)."""
    n=int(ms/1000*SR); n=min(n,len(a),len(b)); t=np.linspace(0,np.pi/2,n)
    return np.concatenate([a[:-n],a[-n:]*np.cos(t)+b[:n]*np.sin(t),b[n:]])
def build_timeline(segs,gap_fn):
    """segs: list of (role,audio). Lines are placed on a timeline with gap_fn(prev_role,next_role) seconds between them; returns bus (speech only), timeline [(role,t0,t1)]."""
    t=0.0; tl=[]; parts=[]
    for i,(r,x) in enumerate(segs):
        x=fade(x); tl.append((r,round(t,3),round(t+len(x)/SR,3))); parts.append((int(t*SR),x)); t+=len(x)/SR
        if i+1<len(segs): t+=gap_fn(r,segs[i+1][0])
    bus=np.zeros(int(t*SR)+SR//2,np.float32)
    for s,x in parts: bus[s:s+len(x)]+=x
    return bus,tl
def final_mp3(x,dst,tone_db=-62):
    """add room tone under the whole thing, two-pass loudnorm to -19 LUFS (TP -1.5), 192 kbps mono mp3. Returns (I,LRA,TP)."""
    x=x+room_tone(len(x)/SR,tone_db)[:len(x)]; tmp=f"{W}/_fin.wav"; write_wav(tmp,x)
    r=subprocess.run([FF,"-hide_banner","-nostats","-i",tmp,"-af",f"loudnorm=I={TARGET}:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True)
    j=json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}")+1])
    af=(f"loudnorm=I={TARGET}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,alimiter=limit=0.89:level=false")
    subprocess.run([FF,"-y","-v","error","-i",tmp,"-af",af,"-ar","44100","-ac","1","-c:a","libmp3lame","-b:a","192k",dst],check=True)
    return metrics.ebur(dst)
def artefact_stats(x):
    """Join/edge indicators on a finished scene (44.1 kHz mono float).
    abrupt = adjacent 5 ms RMS frames differing by > 35 dB where the louder one is above -45 dBFS (a cut into/out of silence or a splice);
    click = sample-to-sample step > 8x the median speech step at such an event; floor = quietest 100 ms window RMS (digital silence reads about -120 or lower; a room tone reads about -60)."""
    r,H=rms_db_frames(x,5); d=np.diff(r); hi=np.maximum(r[:-1],r[1:]); ab=np.where((np.abs(d)>35)&(hi>-45))[0]
    dx=np.abs(np.diff(x)); med=float(np.median(dx[np.abs(x[1:])>0.01])); clicks=0
    for k in ab:
        s=k*H; w=dx[max(0,s-H):s+2*H]; clicks+= int(len(w) and w.max()>8*med)
    n=int(0.1*SR); mins=min(db(np.sqrt((x[i:i+n]**2).mean())) for i in range(0,max(1,len(x)-n),n//2))
    return dict(abrupt_events=int(len(ab)),click_events=clicks,abrupt_per_min=round(len(ab)/(len(x)/SR/60),1),quietest_100ms_db=round(float(mins),1))
