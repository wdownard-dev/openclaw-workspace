import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tools import *; from scene_texts import B
tag=sys.argv[1]; al=json.load(open(f"{W}/align_{tag}.json")); out={}
roles={}
for i in range(2):
    x=load(f"{OUT}/lines/{tag}_passage{i+1}.mp3")
    for b in SCENES[i]:
        t=al[str(i)]["times"][str(b)]
        if not t: continue
        s=B[b][0]; roles.setdefault(s,[]).append((b,x[max(0,int((t[0]-0.05)*SR)):int((t[1]+0.15)*SR)]))
for s,L in roles.items():
    text=" ".join(respell(B[b][1]) for b,_ in L); out[s]=role_measure([a for _,a in L],text,f"A{tag}{s}"); print(s,out[s])
# D4 control = voices3 narrator lines (Daniel, multilingual_v2, same settings)
ctrl=[load(f"{V3}/proof_lines/beat{b:02d}_NARR.mp3") for b in BEATS if B[b][0]=="NARR"]
out["D4_control"]=role_measure(ctrl," ".join(respell(B[b][1]) for b in BEATS if B[b][0]=="NARR"),"ctrl"); print("D4 control",out["D4_control"])
json.dump(out,open(f"{W}/measure_{tag}.json","w"),indent=1)
