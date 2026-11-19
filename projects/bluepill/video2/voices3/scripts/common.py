"""Shared helpers for voices3 (video 1, Project Blue Pill). Key via ELEVENLABS_API_KEY env only."""
import os, sys, json, csv, time, subprocess, re
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(HERE); W=os.path.join(OUT,"_work")
V2=os.path.join(os.path.dirname(OUT),"voices2")
FF="/home/williamdownard/openclaw-sites/bin/ffmpeg"; FMT="mp3_44100_128"
sys.path.insert(0,os.path.join(V2,"scripts")); sys.path.insert(0,os.path.join(os.path.dirname(OUT),"voices","scripts"))
LOG=os.path.join(OUT,"voice_log.csv")
COLS=["time","clip","file","engine","voice_id","voice_name","characters","model_id","settings","duration_s","api_seconds","note"]
DANIEL=("Daniel","onwK4e9ZLuTAKqWW03F9")
S_DANIEL={"stability":0.5,"similarity_boost":0.75,"style":0.2,"use_speaker_boost":True,"speed":1.0}
def saved(): return json.load(open(f"{W}/saved_voices.json"))
def duration(path):
    r=subprocess.run([FF,"-hide_banner","-i",path,"-f","null","-"],capture_output=True,text=True)
    m=re.findall(r"time=(\d+):(\d+):([\d.]+)",r.stderr)[-1]; return int(m[0])*3600+int(m[1])*60+float(m[2])
def quota():
    r=subprocess.run(["curl","-s","-m","30","https://api.elevenlabs.io/v1/user/subscription","-H","xi-api-key: "+os.environ["ELEVENLABS_API_KEY"]],capture_output=True,text=True)
    d=json.loads(r.stdout); return d["character_count"],d["character_limit"]
def log(clip,path,vid,vname,chars,model,sp,dur,api,note):
    new=not os.path.exists(LOG)
    with open(LOG,"a",newline="") as f:
        w=csv.writer(f)
        if new: w.writerow(COLS)
        w.writerow([time.strftime("%Y-%m-%dT%H:%M:%S"),clip,os.path.relpath(path,OUT),"elevenlabs",vid,vname,chars,model,json.dumps(sp),round(dur,2),api,note])
def el_tts(clip,vname,vid,text,settings,path,model,note="",extra=None):
    if os.path.exists(path): print("cached",os.path.basename(path)); return
    os.makedirs(os.path.dirname(path),exist_ok=True); t0=time.time()
    bp=f"{W}/_body_{os.getpid()}.json"; open(bp,"w").write(json.dumps(dict({"text":text,"model_id":model,"voice_settings":settings},**(extra or {}))))
    r=subprocess.run(["curl","-s","-m","240","-o",path,"-w","%{http_code} %{content_type}","-X","POST",f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format={FMT}",
        "-H","xi-api-key: "+os.environ["ELEVENLABS_API_KEY"],"-H","Content-Type: application/json","-d","@"+bp],capture_output=True,text=True)
    code,ctype=(r.stdout.strip().split(" ",1)+[""])[:2]
    if code!="200" or "audio" not in ctype:
        err=open(path,errors="replace").read()[:400] if os.path.exists(path) else r.stderr
        if os.path.exists(path): os.remove(path)
        raise SystemExit(f"STOP: API error {code} on {clip} {vname}: {err}")
    api=round(time.time()-t0,1); d=duration(path); log(clip,path,vid,vname,len(text),model,settings,d,api,note)
    print(clip,vname,"chars",len(text),"dur",round(d,2)); time.sleep(0.3)
