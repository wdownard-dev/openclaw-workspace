import json,sys,os,subprocess,time
B="/home/williamdownard/.openclaw/workspace/projects/gaming"
sys.path.insert(0,B)
import cut_moment as c
def get(vid):
    d=f"{B}/work/g1119/{vid}"; os.makedirs(d,exist_ok=True)
    out=f"{d}/transcript.txt"
    if os.path.exists(out): return out
    j=f"{B}/out/{vid}.en.json3"
    if not os.path.exists(j):
        port=c.start_proxy()
        px=["--proxy",f"http://127.0.0.1:{port}","--no-warnings"]
        for _ in range(3):
            subprocess.run([c.YTDLP,*px,"--skip-download","--write-auto-subs","--write-subs","--sub-langs","en-orig,en","--sub-format","json3","-o",d+"/tr","https://www.youtube.com/watch?v="+vid],capture_output=True,text=True)
            fs=sorted(f for f in os.listdir(d) if f.startswith("tr.") and f.endswith(".json3"))
            if fs: j=f"{d}/{fs[0]}"; break
            time.sleep(8)
        else:
            print("NO SUBS",vid); return None
    ev=json.load(open(j))["events"]
    lines=[];ct=None;cur=[]
    for e in ev:
        tx="".join(s.get("utf8","") for s in e.get("segs",[])).replace("\n"," ").strip()
        if not tx: continue
        t=e["tStartMs"]/1000
        if ct is None: ct=t
        if t-ct>8 and cur:
            lines.append(f"[{int(ct)}] "+" ".join(cur)); ct,cur=t,[]
        cur.append(tx)
    if cur: lines.append(f"[{int(ct)}] "+" ".join(cur))
    open(out,"w").write("\n".join(lines)+"\n"); return out
if __name__=="__main__":
    for v in sys.argv[1:]: print(v,get(v))
