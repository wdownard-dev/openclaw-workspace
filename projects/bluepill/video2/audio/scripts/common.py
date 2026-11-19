"""Shared helpers for voices4 (round 3 of voice work, video 1 / Project Blue Pill). Key via ELEVENLABS_API_KEY env only.
Run with /home/williamdownard/openclaw-sites/clips-venv/bin/python -I (numpy only; no scipy)."""
import os, sys, json, csv, time, subprocess, re, wave
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(HERE); W=os.path.join(OUT,"_work"); VID2=os.path.dirname(OUT)
V3=os.path.join(VID2,"voices3"); V2=os.path.join(VID2,"voices2"); V1=os.path.join(VID2,"voices")
FF="/home/williamdownard/openclaw-sites/bin/ffmpeg"; FMT="mp3_44100_128"
sys.path.insert(0,os.path.join(V2,"scripts")); sys.path.insert(0,os.path.join(V1,"scripts"))
import numpy as np
import metrics, metrics2
SR=44100; TARGET=-19.0
LOG=os.path.join(OUT,"voice_log.csv")
COLS=["time","clip","file","endpoint","voice_id","voice_name","characters","model_id","settings","duration_s","api_seconds","quota_before","quota_after","note"]
DANIEL=("Daniel","onwK4e9ZLuTAKqWW03F9"); RIVER=("River","SAz9YHcvj6GT2YYXdXww")
S_DANIEL={"stability":0.5,"similarity_boost":0.75,"style":0.2,"use_speaker_boost":True,"speed":1.0}
SAVED=json.load(open(f"{V3}/_work/saved_voices.json"))
BP={k:(v["name"],v["voice_id"]) for k,v in SAVED.items()}   # ODY POLY CYC2 CREW
LIB={"ODY":("BP Justin (audition)","NyBVtlh1XAem9yCxNuWk"),"POLY":("BP Philip (audition)","exurTFaGNF2gnRcPNH8I"),
     "CYC2":("BP Drew (audition)","lCfIptVKzlPoj4vLmTLz"),"CREW":("BP Lukas (audition)","wSqOdjeNqDrHcoK0zorF")}
KEY=lambda: os.environ["ELEVENLABS_API_KEY"]
def duration(path):
    r=subprocess.run([FF,"-hide_banner","-i",path,"-f","null","-"],capture_output=True,text=True)
    m=re.findall(r"time=(\d+):(\d+):([\d.]+)",r.stderr)[-1]; return int(m[0])*3600+int(m[1])*60+float(m[2])
def quota():
    for k in range(4):
        r=subprocess.run(["curl","-s","-m","30","https://api.elevenlabs.io/v1/user/subscription","-H","xi-api-key: "+KEY()],capture_output=True,text=True)
        try: return json.loads(r.stdout)["character_count"]
        except Exception: time.sleep(3)
    return -1
def log(clip,path,endpoint,vid,vname,chars,model,sp,dur,api,q0,q1,note):
    new=not os.path.exists(LOG)
    with open(LOG,"a",newline="") as f:
        w=csv.writer(f)
        if new: w.writerow(COLS)
        w.writerow([time.strftime("%Y-%m-%dT%H:%M:%S"),clip,os.path.relpath(path,OUT),endpoint,vid,vname,chars,model,json.dumps(sp),round(dur,2),api,q0,q1,note])
def post(clip,url,body,path,label,vid,vname,chars,model,sp,note,timeout=300):
    """POST a JSON body, save audio to path, log with quota before/after. Stops loudly on any non-200."""
    if os.path.exists(path): print("cached",os.path.basename(path)); return
    os.makedirs(os.path.dirname(path),exist_ok=True); q0=quota(); t0=time.time()
    bp=f"{W}/_body_{os.getpid()}.json"; open(bp,"w").write(json.dumps(body))
    r=subprocess.run(["curl","-s","-m",str(timeout),"-D",path+".hdr","-o",path,"-w","%{http_code} %{content_type}","-X","POST",url,"-H","xi-api-key: "+KEY(),"-H","Content-Type: application/json","-d","@"+bp],capture_output=True,text=True)
    code,ctype=(r.stdout.strip().split(" ",1)+[""])[:2]
    if code!="200" or "audio" not in ctype:
        err=open(path,errors="replace").read()[:600] if os.path.exists(path) else r.stderr
        if os.path.exists(path): os.remove(path)
        raise SystemExit(f"STOP: API error {code} on {clip}: {err}")
    hdr=open(path+".hdr").read(); m=re.search(r"request-id:\s*(\S+)",hdr,re.I); rid=m.group(1) if m else ""
    if rid: open(path+".rid","w").write(rid)
    api=round(time.time()-t0,1); d=duration(path); time.sleep(1.0); q1=quota()
    log(clip,path,label,vid,vname,chars,model,sp,d,api,q0,q1,note); print(clip,"chars",chars,"billed",q1-q0,"dur",round(d,2)); time.sleep(0.3)
def el_tts(clip,vname,vid,text,settings,path,model,note="",extra=None):
    body=dict({"text":text,"model_id":model},**(extra or {}))
    if settings is not None: body["voice_settings"]=settings
    post(clip,f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format={FMT}",body,path,"text-to-speech",vid,vname,len(text),model,settings,note)
def el_dialogue(clip,inputs,path,model,settings,note="",extra=None):
    body=dict({"inputs":inputs,"model_id":model},**(extra or {}))
    if settings is not None: body["settings"]=settings
    chars=sum(len(i["text"]) for i in inputs)
    post(clip,f"https://api.elevenlabs.io/v1/text-to-dialogue?output_format={FMT}",body,path,"text-to-dialogue",",".join(sorted({i['voice_id'] for i in inputs})),"multi",chars,model,settings,note)
# audio helpers
def load(path,sr=SR):
    r=subprocess.run([FF,"-v","error","-i",path,"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True); return np.frombuffer(r.stdout,dtype=np.float32).copy()
def write_wav(path,x,sr=SR):
    with wave.open(path,"wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes())
def lufs(x,tmp=None):
    tmp=tmp or f"{W}/_l_{os.getpid()}.wav"; write_wav(tmp,x); return metrics.ebur(tmp)[0]
def db(v): return 20*np.log10(max(float(v),1e-9))
def rms_db_frames(x,ms=20,sr=SR):
    H=int(sr*ms/1000); n=len(x)//H; return 20*np.log10(np.maximum(np.sqrt((x[:n*H].reshape(n,H)**2).mean(1)),1e-9)),H
SCRIPT="SCRIPT-V4.md"   # V4 = V3 with William's approved cuts (77, 78, 79, 89, 91) and the shorter beat 04, 2026-11-13
def parse_script():
    d={}
    for m in re.finditer(r"^\*\*(\d+) · (\w+)\*\* (.+)$",open(os.path.join(VID2,SCRIPT)).read(),re.M): d[int(m.group(1))]=(m.group(2),m.group(3).strip())
    return d
def respell(t): return re.sub(r"\bPolyphemus\b","Pollifeemus",t)
BEATS=[27,28,29,30,31,32,33,34,35,36,37,38,39,40,63,64,65,66,67,68,69]
SCENES=[[27,28,29,30,31,32,33,34,35,36,37,38,39,40],[63,64,65,66,67,68,69]]   # two continuous passages per method
