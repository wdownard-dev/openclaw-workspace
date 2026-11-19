"""Synthesise the five chapter-card stings for video 1 (pure Python, no third-party audio, no samples).
Each sting: 2.0 s mono 44.1 kHz. Slow-attack low pad (two detuned sines per partial + soft octave + fifth/third) plus a
low-passed noise swell, slow raised-cosine attack (~0.8 s), gentle decay to silence by 1.75 s, then 0.25 s of true silence so
it ends well before the next narration starts. Calibrated to about -29 LUFS integrated (measured with ffmpeg loudnorm).
Run: python3 make_stings.py   -> audio/stings/sting_*.wav"""
import os, math, random, wave, array, subprocess, json, re
HERE=os.path.dirname(os.path.abspath(__file__)); PROJ=os.path.dirname(HERE)
FF=os.path.join(PROJ,"pipeline/remotion-proof/node_modules/@remotion/compositor-linux-x64-gnu/ffmpeg")
OUT=os.path.join(HERE,"audio","stings"); os.makedirs(OUT,exist_ok=True)
SR=44100; DUR=2.0; FADE_END=1.75; PEAK_T=0.8; TARGET=-29.0
# chapter index (as in beats.py CHAPTERS), name, root Hz, third/fifth ratio, noise seed
SPEC=[(2,"poem",73.42,1.5,11),        # D2 + fifth: open, plain
      (3,"skull",65.41,1.189,22),     # C2 + minor third: darker, for the bones
      (4,"cyclopes",82.41,1.5,33),    # E2 + fifth
      (5,"limits",55.00,1.189,44),    # A1 + minor third: sober
      (6,"verdict",73.42,1.26,55)]    # D2 + major third: slightly resolved
def env(t):
    if t<PEAK_T: return math.sin(0.5*math.pi*t/PEAK_T)**2
    if t<FADE_END: return 0.5*(1+math.cos(math.pi*(t-PEAK_T)/(FADE_END-PEAK_T)))
    return 0.0
def render(root,ratio,seed):
    rnd=random.Random(seed); n=int(SR*DUR); lp1=lp2=0.0; a=1-math.exp(-2*math.pi*350/SR); out=[0.0]*n
    ph=[rnd.random()*6.283 for _ in range(8)]
    for i in range(n):
        t=i/SR; e=env(t)
        trem=1+0.06*math.sin(2*math.pi*0.45*t+ph[7])
        x=0.0
        for k,(f,amp) in enumerate([(root,1.0),(root*1.0045,0.8),(root*2,0.28),(root*2.007,0.2),(root*ratio,0.34*trem),(root*ratio*1.005,0.26*trem)]):
            x+=amp*math.sin(2*math.pi*f*t+ph[k])
        w=rnd.uniform(-1,1); lp1+=a*(w-lp1); lp2+=a*(lp1-lp2)          # two-pole low-passed noise (~350 Hz)
        nz=lp2*7.0*(0.5*(1-math.cos(2*math.pi*min(t/FADE_END,1.0))))  # noise swell peaks mid-sting
        out[i]=(x*0.25+nz*0.12)*e
    for i in range(int(0.005*SR)): out[i]*=i/(0.005*SR)
    return out
def write(path,s,gain):
    arr=array.array('h',(max(-32768,min(32767,int(round(v*gain*32767)))) for v in s))
    with wave.open(path,'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(arr.tobytes())
def measure(path):
    p=subprocess.run([FF,"-hide_banner","-nostats","-i",path,"-af","loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True)
    j=json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}',p.stderr).group(0)); return float(j['input_i']),float(j['input_tp'])
if __name__=="__main__":
    rep=[]
    for ch,name,root,ratio,seed in SPEC:
        s=render(root,ratio,seed); pk=max(abs(v) for v in s); g=0.2/pk; path=f"{OUT}/sting_ch{ch}_{name}.wav"
        for _ in range(3):
            write(path,s,g); L,TP=measure(path); g*=10**((TARGET-L)/20)
        write(path,s,g); L,TP=measure(path); rep.append((ch,name,root,round(L,2),round(TP,2)))
        print(path,"LUFS",round(L,2),"TP",round(TP,2))
    json.dump(rep,open(f"{OUT}/levels.json","w"))
