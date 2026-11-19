"""Table numbering and reel contents shared by slates2.py, reel2.py and build_audition2.py."""
import sys, os, json
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from cfg import *
import select2
NUMW=["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
TENS={2:"twenty",3:"thirty",4:"forty",5:"fifty",6:"sixty",7:"seventy",8:"eighty",9:"ninety"}
def words(n):
    if n<20: return NUMW[n]
    t,o=divmod(n,10); return TENS[t]+("-"+NUMW[o] if o else "")
ROLE_NAME={"ODY":"Odysseus","POLY":"Polyphemus","CYC2":"The Cyclopes","CREW":"The crew"}
def rows():
    """all clips in table order: list of dict(num, section, role, engine, base, file, kind)"""
    out=[]; n=0
    for c,stem,model,text,st,label,note in sorted(NARR,key=lambda x:{"D1":1,"D2a":2,"D2b":3,"D3":4,"D4":5,"D5":6}[x[0]]):
        n+=1; out.append(dict(num=n,role="NARR",engine="elevenlabs",base=stem+".mp3",file=f"narrator_daniel/{stem}.mp3",id=c,desc=label,note=note))
    for role in ("ODY","POLY","CYC2","CREW"):
        for p,_ in DESIGN[role]:
            for i in (1,2,3):
                n+=1; b=f"{role}_design{p}_p{i}.mp3"; out.append(dict(num=n,role=role,engine="design",base=b,file=f"characters/{role}/design/{b}",id=f"{role}-D{p}{i}",design=p,preview=i))
        if role=="POLY":
            n+=1; b="POLY_designA_p2_pitchdown4st.mp3"; out.append(dict(num=n,role=role,engine="post",base=b,file=f"characters/POLY/post/{b}",id="POLY-DA2-shift"))
        for c,nm,vid in LIB[role]:
            for k in ROLE_TEXTS[role]:
                n+=1; b=f"{c}_{nm}_{k}_v4.mp3"; out.append(dict(num=n,role=role,engine="eleven_lib",base=b,file=f"characters/{role}/eleven_lib/{b}",id=f"{c}-{k}",voice=nm,line=k,vid=vid))
        for v,ins in OA[role]:
            for k in ROLE_TEXTS[role]:
                n+=1; b=f"{v}_{k}.mp3"; out.append(dict(num=n,role=role,engine="openai",base=b,file=f"characters/{role}/openai/{b}",id=f"OA-{v}-{k}",voice=v,line=k,ins=ins))
    return out
def _sel():
    inv,sel=select2.build(); R={r["file"]:r for r in rows()}; return sel,R
def reel_chars():
    """main reel: best preview per design prompt (3) + the best-scoring non-design clip per role"""
    sel,R=_sel(); plan=[]
    for role in ("ODY","POLY","CYC2","CREW"):
        rs=sel[role]; ds=sorted([r for r in rs if r["engine"]=="design"],key=lambda r:r["prompt"])
        items=[R[r["file"]] for r in ds]
        nd=[r for r in rs if r["engine"]!="design"][0]; items.append(R[nd["file"]])
        plan.append((role,items))
    return plan
def reel_extra():
    """extra reel: next two non-design voices per role, POLY pitch-shift option, ram and prayer clips for the library and OpenAI picks"""
    sel,R=_sel(); main={r["file"] for _,its in reel_chars() for r in its}; plan=[]
    for role in ("ODY","POLY","CYC2","CREW"):
        nd=[r for r in sel[role] if r["engine"]!="design"]; items=[]
        if role=="POLY": items.append(R["characters/POLY/post/POLY_designA_p2_pitchdown4st.mp3"])
        for r in nd[:3]:
            if r["file"] in main: continue
            if len([i for i in items if i["engine"]!="post"])>=2: break
            items.append(R[r["file"]])
            if role=="POLY":
                for k in ("POLY_RAM","POLY_PRAYER"):
                    if r["engine"]=="eleven_lib" and r["voice"]=="PhilipQuietAuthority" or r["voice"]=="ash":
                        items.append(R[r["file"].replace("POLY_NOBODY",k)])
        if role=="POLY":   # the main-reel pick (ash) also gets its ram and prayer here
            for k in ("POLY_RAM","POLY_PRAYER"):
                f=f"characters/POLY/openai/ash_{k}.mp3"
                if R[f] not in items: items.append(R[f])
        plan.append((role,items))
    return plan
def slate_text(r):
    e={"design":"designed","post":"designed, pitched down","eleven_lib":"library","openai":"open A I"}.get(r["engine"],"")
    extra={"POLY_RAM":", the ram","POLY_PRAYER":", the prayer"}.get(r.get("line"),"")
    return f"{words(r['num']).capitalize().replace('-',' ')}, {e}{extra}."
if __name__=="__main__":
    for role,items in reel_chars()+[("--extra--",[])]+reel_extra():
        print(role); [print("  ",r["num"],r["file"],"|",slate_text(r)) for r in items]
