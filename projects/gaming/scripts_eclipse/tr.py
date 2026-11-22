import sys,os,json,subprocess,time
sys.path.insert(0,"/home/williamdownard/.openclaw/workspace/projects/gaming")
import cut_moment as c
port=c.start_proxy()
px=["--proxy",f"http://127.0.0.1:{port}","--ffmpeg-location",c.FFMPEG,"--no-warnings"]
base="/home/williamdownard/.openclaw/workspace/projects/gaming/work/eclipse_tr"
for vid in sys.argv[1:]:
    d=f"{base}/{vid}"; os.makedirs(d,exist_ok=True)
    if os.path.exists(d+"/transcript.txt"): continue
    subprocess.run([c.YTDLP,*px,"--skip-download","--write-auto-subs","--write-subs","--sub-langs","en-orig,en","--sub-format","json3","--write-info-json","-o",d+"/tr","https://www.youtube.com/watch?v="+vid],capture_output=True,text=True)
    fs=sorted(f for f in os.listdir(d) if f.endswith(".json3"))
    if not fs: print(vid,"NO CAPS"); time.sleep(5); continue
    ev=json.load(open(f"{d}/{fs[0]}"))["events"]
    lines=[];ct=None;cur=[]
    for e in ev:
        tx="".join(s.get("utf8","") for s in e.get("segs",[])).replace("\n"," ").strip()
        if not tx: continue
        t=e["tStartMs"]/1000
        if ct is None: ct=t
        if t-ct>6 and cur:
            lines.append(f"[{int(ct)}s] "+" ".join(cur)); ct,cur=t,[]
        cur.append(tx)
    if cur: lines.append(f"[{int(ct)}s] "+" ".join(cur))
    open(d+"/transcript.txt","w").write("\n".join(lines)+"\n")
    print(vid,"ok",len(lines),"lines"); time.sleep(4)
