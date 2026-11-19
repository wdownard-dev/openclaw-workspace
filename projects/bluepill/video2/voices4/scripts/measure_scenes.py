"""Comparison table inputs: per-role F0/spectral/loudness, gaps, join artefact indicators for every method + the round-2 baseline. Writes _work/comparison.json (no API calls)."""
import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tools import *; from asm import artefact_stats; from scene_texts import B
res={}
FILES={"R2_proof_scene":f"{V3}/proof_scene.mp3","A_v4":f"{OUT}/methodA_v4_scene.mp3","A_v2":f"{OUT}/methodA_v2_scene.mp3","B_bp":f"{OUT}/methodB_bp_scene.mp3","B_lib":f"{OUT}/methodB_scene.mp3","C":f"{OUT}/methodC_scene.mp3","diag":f"{OUT}/diag_bp_voices_smooth.mp3"}
STEM={"A_v4":"A_v4","A_v2":"A_v2","B_bp":"B_bp_eleven_v4","B_lib":"B_lib_eleven_v4"}
for k,f in FILES.items():
    x=load(f); r={"duration_s":round(len(x)/SR,1),"artefacts":artefact_stats(x),"lufs_lra_tp":metrics.ebur(f)}
    roles={}; gaps=[]
    if k in STEM:   # spans from whisper alignment of the raw render; loudness after the gain ride from assembled_*.json
        al=json.load(open(f"{W}/align_{STEM[k]}.json")); det=json.load(open(f"{W}/assembled_{k}.json"))["detail"]; spans=[]
        for i in range(2):
            raw=load(f"{OUT}/lines/{STEM[k]}_passage{i+1}.mp3"); prev_end=None
            for b in SCENES[i]:
                t=al[str(i)]["times"][str(b)]
                if not t: continue
                s=B[b][0]; roles.setdefault(s,[]).append((b,raw[max(0,int((t[0]-0.05)*SR)):int((t[1]+0.15)*SR)]))
                if prev_end is not None: gaps.append(t[0]-prev_end)
                prev_end=t[1]
        pre={};post={}
        for b,(l,g) in det.items(): s=B[int(b)][0]; pre.setdefault(s,[]).append(l); post.setdefault(s,[]).append(l+g)
        loud={s:(round(float(np.mean(pre[s])),1),round(float(np.mean(post[s])),1)) for s in pre}
    elif k=="R2_proof_scene":
        A=json.load(open(f"{V3}/_work/assemble.json"))["timeline"]; prev=None
        for b,s,t0,t1 in A:
            roles.setdefault(s,[]).append((b,x[int(t0*SR):int(t1*SR)]))
            if prev is not None: gaps.append(t0-prev)
            prev=t1
        loud=None
    else:
        tl=json.load(open(f"{W}/assembled_{k}.json"))["detail"]["timeline"]; prev=None
        for (s,t0,t1),b in zip(tl,BEATS):
            roles.setdefault(s,[]).append((b,x[int(t0*SR):int(t1*SR)]))
            if prev is not None: gaps.append(t0-prev)
            prev=t1
        loud=None
    r["roles"]={}
    for s,L in roles.items():
        text=" ".join(respell(B[b][1]) for b,_ in L); r["roles"][s]=role_measure([a for _,a in L],text,f"{k}{s}")
    if loud: r["role_loudness_pre_post_ride"]=loud
    g=np.array(gaps); r["gaps_s"]={"n":len(g),"min":round(float(g.min()),2),"median":round(float(np.median(g)),2),"max":round(float(g.max()),2)}
    res[k]=r; print(k,r["duration_s"],r["artefacts"],r["lufs_lra_tp"],r["gaps_s"]); 
    for s,v in r["roles"].items(): print("  ",s,v)
json.dump(res,open(f"{W}/comparison.json","w"),indent=1,default=str)
