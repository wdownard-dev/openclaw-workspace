import sys,subprocess,json,os,time
sys.path.insert(0,"/home/williamdownard/.openclaw/workspace/projects/gaming")
import cut_moment as c
B="/home/williamdownard/.openclaw/workspace/projects/gaming/work/g1120"
port=c.start_proxy()
px=["--proxy",f"http://127.0.0.1:{port}","--no-warnings"]
def tr(vid,d):
    out=f"{d}/transcript.txt"
    fs=sorted(f for f in os.listdir(d) if f.startswith("tr.") and f.endswith(".json3"))
    if not fs:
        subprocess.run([c.YTDLP,*px,"--skip-download","--write-auto-subs","--write-subs","--sub-langs","en-orig,en","--sub-format","json3","-o",d+"/tr","https://www.youtube.com/watch?v="+vid],capture_output=True,text=True,timeout=120)
        fs=sorted(f for f in os.listdir(d) if f.startswith("tr.") and f.endswith(".json3"))
    if not fs: return False
    ev=json.load(open(f"{d}/{fs[0]}"))["events"]
    lines=[];ct=None;cur=[]
    for e in ev:
        tx="".join(s.get("utf8","") for s in e.get("segs",[])).replace("\n"," ").strip()
        if not tx: continue
        t=e["tStartMs"]/1000
        if ct is None: ct=t
        if t-ct>6 and cur:
            lines.append(f"[{int(ct)}] "+" ".join(cur)); ct,cur=t,[]
        cur.append(tx)
    if cur: lines.append(f"[{int(ct)}] "+" ".join(cur))
    open(out,"w").write("\n".join(lines)+"\n"); return True
for vid in sys.argv[1:]:
    d=f"{B}/{vid}"; os.makedirs(d,exist_ok=True)
    mf=f"{d}/meta.json"
    if not os.path.exists(mf):
        try:
            r=subprocess.run([c.YTDLP,*px,"-j","--skip-download",f"https://www.youtube.com/watch?v={vid}"],capture_output=True,text=True,timeout=120)
            j=json.loads(r.stdout); m={k:j.get(k) for k in("id","title","channel","upload_date","duration","view_count","timestamp")}
            json.dump(m,open(mf,"w"))
        except Exception as e: m={"err":str(e)[:100]}
    else: m=json.load(open(mf))
    ok=False
    try: ok=tr(vid,d)
    except Exception as e: pass
    print(vid,m.get("channel"),"|",(m.get("title") or "")[:60],"|",m.get("upload_date"),m.get("duration"),m.get("view_count"),"| tr=",ok,flush=True)
