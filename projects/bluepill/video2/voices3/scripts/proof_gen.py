"""Step 4: render the proof scene line by line. Beats parsed from SCRIPT-V3.md; previous_text/next_text (free) give each line its neighbours as context.
Characters billed: sum of line lengths (+ the two extra 'Ah.' / 'Sheep.' flatness lines)."""
import os,sys,re,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
SCRIPT=os.path.join(os.path.dirname(OUT),"SCRIPT-V3.md")
BEATS=[27,28,29,30,31,32,33,34,35,36,37,38,39,40,63,64,65,66,67,68,69]
GAPS={}  # gap after beat (s); default set below
def parse():
    d={}
    for m in re.finditer(r"^\*\*(\d+) · (\w+)\*\* (.+)$",open(SCRIPT).read(),re.M): d[int(m.group(1))]=(m.group(2),m.group(3).strip())
    return d
def respell(t): return re.sub(r"\bPolyphemus\b","Pollifeemus",t)
def base(stab=0.45,speed=1.0): return {"stability":stab,"similarity_boost":0.75,"style":0.25,"use_speaker_boost":True,"speed":speed}
SETTINGS={"NARR":S_DANIEL,"ODY":base(0.45,1.0),"POLY":base(0.45,0.8),"CYC2":base(0.45,0.85),"CREW":base(0.45,0.9)}
MODEL="eleven_multilingual_v2"
def voice(spk):
    if spk=="NARR": return DANIEL
    sv=saved()[spk]; return (sv["name"],sv["voice_id"])
if __name__=="__main__":
    q0=quota(); print("quota before",q0); B=parse(); lines=[(b,)+B[b] for b in BEATS]; total=0
    for i,(b,spk,text) in enumerate(lines):
        vn,vid=voice(spk); t=respell(text)
        prev=respell(lines[i-1][2]) if i else None; nxt=respell(lines[i+1][2]) if i+1<len(lines) else None
        extra={k:v for k,v in (("previous_text",prev),("next_text",nxt)) if v}
        el_tts(f"beat{b:02d}_{spk}",vn,vid,t,SETTINGS[spk],f"{OUT}/proof_lines/beat{b:02d}_{spk}.mp3",MODEL,"proof scene line",extra); total+=len(t)
    # one-word flatness extras: Ah. in context (beats 19-20), Sheep. standalone
    sv=saved()
    el_tts("extra_ODY_Ah_ctx","BP Odysseus",sv["ODY"]["voice_id"],"And then who moves the stone? Ah.",SETTINGS["ODY"],f"{OUT}/proof_lines/extra_ODY_Ah_ctx.mp3",MODEL,"flatness check, Ah. inside beats 19-20"); total+=len("And then who moves the stone? Ah.")
    el_tts("extra_CYC2_Sheep","BP Cyclops chorus",sv["CYC2"]["voice_id"],"Sheep.",SETTINGS["CYC2"],f"{OUT}/proof_lines/extra_CYC2_Sheep.mp3",MODEL,"flatness check, Sheep. standalone",{"previous_text":"I keep sheep."}); total+=6
    print("proof characters this run (if not cached):",total); print("quota after",quota())
