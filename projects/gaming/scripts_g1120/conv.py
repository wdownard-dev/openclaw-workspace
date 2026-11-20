import json,sys,os
B="/home/williamdownard/.openclaw/workspace/projects/gaming"
for vid in sys.argv[1:]:
    j=f"{B}/out/{vid}.en.json3"; d=f"{B}/work/g1120/{vid}"; os.makedirs(d,exist_ok=True)
    ev=json.load(open(j))["events"]; lines=[];ct=None;cur=[]
    for e in ev:
        tx="".join(s.get("utf8","") for s in e.get("segs",[])).replace("\n"," ").strip()
        if not tx: continue
        t=e["tStartMs"]/1000
        if ct is None: ct=t
        if t-ct>6 and cur: lines.append(f"[{int(ct)}] "+" ".join(cur)); ct,cur=t,[]
        cur.append(tx)
    if cur: lines.append(f"[{int(ct)}] "+" ".join(cur))
    open(d+"/transcript.txt","w").write("\n".join(lines)+"\n"); print(vid,len(lines))
