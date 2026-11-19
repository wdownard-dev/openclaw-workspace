import os,sys,json
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import words as Wd
P=Wd.plan()["passages"]; bg=[];ig=[]; tot=0
for p in P:
    ws=Wd.words_of(p); tot+=ws[-1]["end"]-ws[0]["start"]
    for a,b in zip(ws,ws[1:]):
        g=b["start"]-a["end"]; (bg if a["beat"]!=b["beat"] else ig).append(g)
import statistics as S
print("speech span total",round(tot,1),"s")
print("beat gaps n",len(bg),"mean",round(S.mean(bg),2),"median",round(S.median(bg),2),"max",round(max(bg),2),"sum",round(sum(bg),1))
print("intra gaps n",len(ig),"sum",round(sum(ig),1),">0.3:",sum(1 for g in ig if g>0.3),"sum of >0.3:",round(sum(g for g in ig if g>0.3),1),">0.6:",sum(1 for g in ig if g>0.6))
for cap in (0.3,0.35,0.4,0.5):
    print("cap",cap,"beat gaps ->",round(sum(min(g,cap) for g in bg),1))
for cap in (0.35,0.45,0.55):
    print("intra cap",cap,"saves",round(sum(max(0,g-cap) for g in ig),1))
print("word-only speech (no gaps >0.12):",round(sum(min(0.12,x) for x in bg+ig)+0,1))
