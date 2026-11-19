"""Scores clips per role against explicit measurement targets and builds the selection + F0 distinctness matrix. Writes _work/selection.json. Run: python -I select2.py
Targets are my reading of the brief (William's words), not facts about taste; lower score = closer. All numbers come from _work/metrics_*.json and _work/words.json."""
import sys, os, json, re, math, itertools
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from cfg import *
W=f"{OUT}/_work"; M=json.load(open(f"{W}/metrics_chars.json")); MD=json.load(open(f"{W}/metrics_daniel.json")); WD=json.load(open(f"{W}/words.json"))
def st(hz): return 12*math.log2(hz/100)
def out_of(v,lo,hi): return 0 if lo<=v<=hi else (lo-v if v<lo else v-hi)
def art(m):
    """articulation pace: words per minute of speaking time (pauses >= 0.3 s removed), so long line gaps in design previews do not look like slow speech"""
    return round(m["words"]/max(m["span_s"]-m["pause_total_s"],1)*60)
def score(role,m,wd):
    f=m["f0w_median_hz"]; s=m["pitch_spread_st"]; w=art(m); l=m["lra_lu"]; parts={}
    if role=="ODY":   # warm dry mid-baritone, wry, controlled, a little expressive, conversational pace
        parts=dict(f0=out_of(st(f),st(90),st(125))/2,spread=abs(s-4.5)/1.5,wpm=abs(w-185)/25,lra=abs(l-3.6)/2)
    elif role=="POLY":  # enormous, very deep, slow, sincere, not flat
        parts=dict(f0=out_of(st(f),st(60),st(95))/2,spread=abs(s-3.5)/1.5,wpm=abs(w-150)/20,lra=max(0,l-4)/2)
    elif role=="CYC2":  # bored, flat, tired, mid-low, slowish
        parts=dict(f0=out_of(st(f),st(105),st(150))/2,spread=abs(s-3.0)/1.2,wpm=abs(w-150)/20,lra=max(0,l-3)/2)
    elif role=="CREW":  # young, mid-high, breathless, expressive
        parts=dict(f0=out_of(st(f),st(150),st(240))/2,spread=abs(s-4.5)/1.2,wpm=abs(w-175)/20,lra=abs(l-3.5)/3)
    pen=0
    for x in wd or []:
        if role=="CREW" and x.get("status")=="FLAT": pen+=0.75     # 'Nope.' / 'Hello?' must not be flat
    parts["flat_oneword"]=pen
    return round(sum(parts.values()),2),parts
def inventory():
    """list of dict(role, engine, label, file, key(metrics), words)"""
    inv=[]
    for role,l in DESIGN.items():
        for n,p in l:
            for i in (1,2,3):
                b=f"{role}_design{n}_p{i}.mp3"; inv.append(dict(role=role,engine="design",voice=f"design {role} {n}",prompt=n,preview=i,file=f"characters/{role}/design/{b}",base=b,line=DESIGN_TEXT and ("POLY_NOBODY" if role=="POLY" else role)))
    for role,vs in LIB.items():
        for c,nm,vid in vs:
            for k in ROLE_TEXTS[role]:
                b=f"{c}_{nm}_{k}_v4.mp3"; inv.append(dict(role=role,engine="eleven_lib",voice=nm,preview=None,file=f"characters/{role}/eleven_lib/{b}",base=b,line=k))
    for role,vs in OA.items():
        for v,ins in vs:
            for k in ROLE_TEXTS[role]:
                b=f"{v}_{k}.mp3"; inv.append(dict(role=role,engine="openai",voice=v,preview=None,file=f"characters/{role}/openai/{b}",base=b,line=k))
    return inv
def build():
    inv=inventory(); 
    for r in inv:
        r["m"]=M[r["base"]]; r["words"]=(WD.get(r["base"]) or {}).get("words",[])
        r["score"],r["parts"]=score(r["role"],r["m"],r["words"])
    # per role: best preview per prompt for designs; per voice for lib/openai the primary clip (NOBODY for POLY)
    sel={}
    for role in ROLE_TEXTS:
        prim="POLY_NOBODY" if role=="POLY" else role
        rows=[r for r in inv if r["role"]==role and (r["engine"]=="design" or r["line"]==prim)]
        best={}
        for r in rows:
            key=(r["engine"],r["voice"])
            if key not in best or r["score"]<best[key]["score"]: best[key]=r
        sel[role]=sorted(best.values(),key=lambda r:r["score"])
    return inv,sel
def d_ref(): 
    # Daniel reference: closest to 174 wpm, 4.7 st, 3.6 LU
    out=[]
    for k,m in MD.items():
        sc=abs(m["wpm"]-174)/10+abs(m["pitch_spread_st"]-4.7)/1.0+abs(m["lra_lu"]-3.6)/1.0
        out.append((round(sc,2),k,m["wpm"],m["pitch_spread_st"],m["lra_lu"],m["f0w_median_hz"]))
    return sorted(out)
if __name__=="__main__":
    inv,sel=build()
    print("DANIEL ranking (score, file, wpm, st, LRA, F0 median):")
    for x in d_ref(): print(" ",x)
    for role,rows in sel.items():
        print("\n",role)
        for r in rows: print("  %-22s %-12s p%s score %.2f  wpm %s st %s lra %s f0 %s  %s"%(r["voice"][:22],r["engine"],r["preview"],r["score"],r["m"]["wpm"],r["m"]["pitch_spread_st"],r["m"]["lra_lu"],r["m"]["f0w_median_hz"],{k:round(v,1) for k,v in r["parts"].items() if v}))
    pools={"design only":lambda r:r["engine"]=="design","any engine":lambda r:True}
    D2=MD["D2a_v4_tagA_speed1.0.mp3"]; combos={}
    for pn,fn in pools.items():
        cand={role:[r for r in rows if fn(r)][:6] for role,rows in sel.items()}
        best=None
        for combo in itertools.product(*[cand[r] for r in ("ODY","POLY","CYC2","CREW")]):
            pts=[("Daniel",D2["f0w_mean_st"])]+[(r["role"],r["m"]["f0w_mean_st"]) for r in combo]
            mn=min(abs(a[1]-b[1]) for a,b in itertools.combinations(pts,2)); tot=sum(r["score"] for r in combo)
            key=(0 if mn>=2 else 1, tot if mn>=2 else -mn)
            if best is None or key<best[0]: best=(key,combo,mn,tot,pts)
        combos[pn]=best
        print("\nPOOL",pn,"min pairwise F0-mean gap %.2f st, total score %.2f"%(best[2],best[3]))
        for r in best[1]: print("  ",r["role"],r["voice"],r["engine"],"p%s"%r["preview"],"score",r["score"],"f0 mean st",r["m"]["f0w_mean_st"])
    json.dump({pn:dict(min_gap=b[2],total=b[3],picks=[r["file"] for r in b[1]]) for pn,b in combos.items()},open(f"{W}/combos.json","w"),indent=1)
    json.dump({k:[dict(voice=r["voice"],engine=r["engine"],file=r["file"],preview=r["preview"],score=r["score"]) for r in v] for k,v in sel.items()},open(f"{W}/selection.json","w"),indent=1)
