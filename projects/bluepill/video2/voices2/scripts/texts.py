"""Writes _work/texts.json: basename -> spoken text (audio tags removed) for wpm."""
import sys,os,json,re,glob
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from cfg import *
t={}
strip=lambda s:re.sub(r"\[[^\]]*\]\s*","",s)
for c,stem,model,text,st,label,note in NARR: t[stem+".mp3"]=strip(text)
for r,l in LIB.items():
    for c,n,v in l:
        for k in ROLE_TEXTS[r]: t[f"{c}_{n}_{k}_v4.mp3"]=T[k]
for r,l in OA.items():
    for v,i in l:
        for k in ROLE_TEXTS[r]: t[f"{v}_{k}.mp3"]=T[k]
for r in DESIGN:
    for n,p in DESIGN[r]:
        for i in (1,2,3): t[f"{r}_design{n}_p{i}.mp3"]=DESIGN_TEXT[r]
json.dump(t,open(f"{OUT}/_work/texts.json","w"),indent=1)
