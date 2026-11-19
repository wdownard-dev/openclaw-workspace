"""Round-2 generator. Usage: python3 -I gen2.py <stage>
  quota      print the ElevenLabs subscription counter
  narr       Part A: Daniel, 5 clips (D1, D2a, D2b, D3, D4)
  design X   Part B1 voice design for role X (ODY POLY CYC2 CREW): 3 prompts x 1 call, keeps all 3 previews each
  lib        Part B2 ElevenLabs library voices with eleven_v4 acting tags
  oa         Part B2 OpenAI gpt-4o-mini-tts
  slates     reel slates (River, ElevenLabs)
Skips existing files. Stops on the first API error. Key via ELEVENLABS_API_KEY / OPENAI_API_KEY env (same as round 1)."""
import os, sys, json, csv, time, subprocess, re, base64
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from cfg import *
LOG=os.path.join(OUT,"voice_log.csv"); W=os.path.join(OUT,"_work")
COLS=["time","clip","file","engine","voice_id","voice_name","characters","model_id","settings_or_prompt","duration_s","api_seconds","note"]
def duration(path):
    r=subprocess.run([FF,"-hide_banner","-i",path,"-f","null","-"],capture_output=True,text=True)
    m=re.findall(r"time=(\d+):(\d+):([\d.]+)",r.stderr)[-1]; return int(m[0])*3600+int(m[1])*60+float(m[2])
def log(clip,path,engine,vid,vname,chars,model,sp,dur,api,note):
    new=not os.path.exists(LOG)
    with open(LOG,"a",newline="") as f:
        w=csv.writer(f)
        if new: w.writerow(COLS)
        w.writerow([time.strftime("%Y-%m-%dT%H:%M:%S"),clip,os.path.relpath(path,OUT),engine,vid,vname,chars,model,sp if isinstance(sp,str) else json.dumps(sp),round(dur,2),api,note])
def quota():
    r=subprocess.run(["curl","-s","-m","30","https://api.elevenlabs.io/v1/user/subscription","-H","xi-api-key: "+os.environ["ELEVENLABS_API_KEY"]],capture_output=True,text=True)
    d=json.loads(r.stdout); return d["character_count"],d["character_limit"]
def curl_json(url,body,headers,out=None):
    bp=os.path.join(W,"_body_%d.json"%os.getpid()); open(bp,"w").write(json.dumps(body))
    cmd=["curl","-s","-m","240","-w","\n%{http_code} %{content_type}","-X","POST",url]+sum([["-H",h] for h in headers],[])+["-d","@"+bp]
    if out: cmd[1:1]=["-o",out]
    return subprocess.run(cmd,capture_output=True,text=True)
def el_tts(clip,vname,vid,text,settings,path,note="",model="eleven_multilingual_v2",engine="elevenlabs"):
    if os.path.exists(path): print("cached",os.path.basename(path)); return
    os.makedirs(os.path.dirname(path),exist_ok=True)
    t0=time.time()
    r=curl_json(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format={FMT}",{"text":text,"model_id":model,"voice_settings":settings},
        ["xi-api-key: "+os.environ["ELEVENLABS_API_KEY"],"Content-Type: application/json"],out=path)
    code,ctype=(r.stdout.strip().split("\n")[-1].split(" ",1)+[""])[:2]
    if code!="200" or "audio" not in ctype:
        err=open(path,errors="replace").read()[:400] if os.path.exists(path) else r.stderr
        if os.path.exists(path): os.remove(path)
        raise SystemExit(f"STOP: API error {code} on {clip} {vname}: {err}")
    api=round(time.time()-t0,1); d=duration(path); log(clip,path,engine,vid,vname,len(text),model,settings,d,api,note)
    print(clip,vname,"chars",len(text),"dur",round(d,2)); time.sleep(0.3)
def narr():
    for c,stem,model,text,st,label,note in NARR:
        el_tts(c,"Daniel",DANIEL[1],text,st,f"{OUT}/narrator_daniel/{stem}.mp3",note,model)
def design(role):
    for n,prompt in DESIGN[role]:
        stem=f"{role}_design{n}"; d=f"{OUT}/characters/{role}/design"; pd=f"{W}/previews/{stem}"
        if os.path.exists(f"{pd}_p1.mp3"): print("cached",stem); continue
        os.makedirs(d,exist_ok=True); os.makedirs(f"{W}/previews",exist_ok=True)
        text=DESIGN_TEXT[role]; t0=time.time()
        body={"voice_description":prompt,"model_id":"eleven_ttv_v3","text":text,"guidance_scale":4,"loudness":0.5}
        r=curl_json(f"https://api.elevenlabs.io/v1/text-to-voice/design?output_format={FMT}",body,["xi-api-key: "+os.environ["ELEVENLABS_API_KEY"],"Content-Type: application/json"])
        parts=r.stdout.rsplit("\n",1); code=parts[-1].split(" ")[0]
        if code!="200": raise SystemExit(f"STOP: design error {code} on {stem}: {parts[0][:500]}")
        j=json.loads(parts[0]); api=round(time.time()-t0,1)
        for i,p in enumerate(j["previews"],1):
            fp=f"{pd}_p{i}.mp3"; open(fp,"wb").write(base64.b64decode(p["audio_base_64"]))
            log(f"{stem}_p{i}",fp,"elevenlabs-voice-design",p["generated_voice_id"],f"design {role}{n}",len(text) if i==1 else 0,"eleven_ttv_v3","guidance 4, loudness 0.5; PROMPT: "+prompt,duration(fp),api,"preview %d of %d (credits charged once per call)"%(i,len(j["previews"])))
        print(stem,"previews",len(j["previews"])); time.sleep(0.5)
def lib():
    for role,voices in LIB.items():
        for c,n,vid in voices:
            for k in ROLE_TEXTS[role]:
                tag=TAGS[k]; el_tts(f"{c}-{k}",n,vid,tag+" "+T[k],{"stability":0.5,"similarity_boost":0.75,"style":0.3,"use_speaker_boost":True,"speed":1.0},
                    f"{OUT}/characters/{role}/eleven_lib/{c}_{n}_{k}_v4.mp3",f"eleven_v4 tag {tag}","eleven_v4")
def oa():
    for role,lst in OA.items():
        for voice,ins in lst:
            for k in ROLE_TEXTS[role]:
                path=f"{OUT}/characters/{role}/openai/{voice}_{k}.mp3"
                if os.path.exists(path): print("cached",path); continue
                os.makedirs(os.path.dirname(path),exist_ok=True); t0=time.time()
                r=curl_json("https://api.openai.com/v1/audio/speech",{"model":"gpt-4o-mini-tts","voice":voice,"input":T[k],"instructions":ins,"response_format":"mp3"},
                    ["Authorization: Bearer "+os.environ["OPENAI_API_KEY"],"Content-Type: application/json"],out=path)
                code=r.stdout.strip().split("\n")[-1].split(" ")[0]
                if code!="200":
                    err=open(path,errors="replace").read()[:300]; os.remove(path); raise SystemExit(f"STOP: openai {code} {voice} {k}: {err}")
                d=duration(path); log(f"OA-{voice}-{k}",path,"openai",voice,voice,len(T[k]),"gpt-4o-mini-tts","instructions: "+ins,d,round(time.time()-t0,1),"openai tts; approx $0.015/min")
                print(role,voice,k,round(d,2)); time.sleep(0.3)
if __name__=="__main__":
    a=sys.argv[1:]
    if a[0]=="quota": print(quota())
    elif a[0]=="narr": narr()
    elif a[0]=="design": design(a[1])
    elif a[0]=="lib": lib()
    elif a[0]=="oa": oa()
    elif a[0]=="slates":
        import slates2; slates2.run(el_tts)
