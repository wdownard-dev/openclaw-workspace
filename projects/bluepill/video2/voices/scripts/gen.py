"""Audition clip generator. Usage (python3 -I gen.py <stage> [args]):
  narr1              first-pass narrator clips (short excerpt) for all narrators
  narr2 N04 N07 ...  longer script for the named narrators
  alt   N04          the named narrator with the two alternate setting sets (V1 and 0.4/0.3)
  chars              character role clips (3 candidates per role)
  slates             spoken slate clips (River) for the reels
Skips clips that already exist. Stops on the first API error (no loops). Key via ELEVENLABS_API_KEY env, same as video1/voice.py."""
import os, sys, json, csv, time, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(HERE)
sys.path.insert(0,HERE)
from catalog import *
FMT="mp3_44100_128"
LOG=os.path.join(OUT,"voice_log.csv")
FFMPEG="/home/williamdownard/openclaw-sites/bin/ffmpeg"
def duration(path):
    r=subprocess.run([FFMPEG,"-hide_banner","-i",path,"-f","null","-"],capture_output=True,text=True)
    import re
    m=re.findall(r"time=(\d+):(\d+):([\d.]+)",r.stderr)[-1]
    return int(m[0])*3600+int(m[1])*60+float(m[2])
def tts(clip,vname,vid,text,settings,path,note="",model=MODEL):
    if os.path.exists(path): print("cached",os.path.basename(path)); return
    body={"text":text,"model_id":model,"voice_settings":settings}
    bp=os.path.join(OUT,"_work","_body.json"); open(bp,"w").write(json.dumps(body))
    t0=time.time()
    r=subprocess.run(["curl","-s","-m","180","-o",path,"-w","%{http_code} %{content_type}","-X","POST",
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format={FMT}",
        "-H","xi-api-key: "+os.environ["ELEVENLABS_API_KEY"],"-H","Content-Type: application/json","-d","@"+bp],capture_output=True,text=True)
    code,ctype=(r.stdout.split(" ",1)+[""])[:2]
    if code!="200" or "audio" not in ctype:
        err=open(path,errors="replace").read()[:400] if os.path.exists(path) else r.stderr
        if os.path.exists(path): os.remove(path)
        raise SystemExit(f"STOP: API error {code} on {clip} {vname}: {err}")
    api=round(time.time()-t0,1); dur=round(duration(path),2)
    new=not os.path.exists(LOG)
    with open(LOG,"a",newline="") as f:
        w=csv.writer(f)
        if new: w.writerow(["time","clip","file","voice_id","voice_name","characters","model_id","settings","output_format","duration_s","api_seconds","note"])
        w.writerow([time.strftime("%Y-%m-%dT%H:%M:%S"),clip,os.path.relpath(path,OUT),vid,vname,len(text),model,json.dumps(settings),FMT,dur,api,note])
    print(clip,vname,"chars",len(text),"dur",dur); time.sleep(0.3)
def narr1():
    for c,n,v,s,note in NARRATORS:
        tts(c,n,v,N_SHORT,SET_PERF_N,f"{OUT}/narrators/{c}_{n}.mp3","narrator first pass, short excerpt")
def narr2(ids):
    for c,n,v,s,note in NARRATORS:
        if c in ids: tts(c+"L",n,v,N_LONG,SET_PERF_N,f"{OUT}/narrators/{c}L_{n}.mp3","narrator long script, perf 0.5/0.2")
def alt(cid):
    for c,n,v,s,note in NARRATORS:
        if c==cid:
            tts(c+"-V1",n,v,N_LONG,SET_V1,f"{OUT}/narrators/{c}L_{n}_set-V1-0.75-0.05.mp3","setting set: V1 0.75/0.05")
            tts(c+"-ACT",n,v,N_LONG,SET_ACT,f"{OUT}/narrators/{c}L_{n}_set-act-0.4-0.3.mp3","setting set: acting 0.4/0.3")
def chars():
    for role,lst in CHARS.items():
        for c,n,v,s,note in lst:
            tts(c,n,v,C_TEXT[role],SET_CHAR,f"{OUT}/characters/{c}_{role}_{n}.mp3",f"role {role}, Nobody exchange lines")
def slates():
    import slates as S
    S.run(tts)
def v4():
    T="[dry, deadpan, amused documentary narrator] Twelve men follow Odysseus into a cave. Six of them get out. [pause] The cleverest man in the poem is waiting for a gift basket from a stranger's cave."
    for c,n,v,s,note in NARRATORS:
        if c in("N01","N09"):
            tts(c+"-v4",n,v,T,{"stability":0.5,"similarity_boost":0.75,"style":0.2,"use_speaker_boost":True,"speed":1.0},f"{OUT}/narrators/{c}_{n}_model-eleven_v4-tag.mp3","Eleven v4 with audio tag",model="eleven_v4")
if __name__=="__main__":
    if sys.argv[1]=="v4": v4(); sys.exit()
    a=sys.argv[1:]
    {"narr1":narr1,"chars":chars,"slates":slates}.get(a[0],lambda:None)() if a[0] in("narr1","chars","slates") else (narr2(set(a[1:])) if a[0]=="narr2" else alt(a[1]))
