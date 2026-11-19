import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tools import *; from scene_texts import B
tag=sys.argv[1]; res={}
for i in range(2):
    p=f"{OUT}/lines/{tag}_passage{i+1}.mp3"; bt=[(b,respell(B[b][1])) for b in SCENES[i]]
    t,cov,heard=align(p,bt); res[i]={"times":{b:t.get(b) for b in SCENES[i]},"coverage":round(cov,3)}
    print(i,"coverage",round(cov,3),"dur",round(duration(p),1)); 
    for b in SCENES[i]: print(b,B[b][0],t.get(b))
json.dump(res,open(f"{W}/align_{tag}.json","w"),indent=1)
