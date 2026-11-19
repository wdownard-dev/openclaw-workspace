"""Method C: Daniel renders the character lines (multilingual_v2, narrator settings, no speed change); narrator lines are reused from voices3 (Daniel, identical settings, no new characters).
previous_text/next_text (free) give each line its neighbours. Differentiation is done afterwards by audio processing (assemble_c.py)."""
import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
B=parse_script(); tot=0
for i,b in enumerate(BEATS):
    s,t=B[b]
    if s=="NARR": continue
    prev=respell(B[BEATS[i-1]][1]) if i else None; nxt=respell(B[BEATS[i+1]][1]) if i+1<len(BEATS) else None
    extra={k:v for k,v in (("previous_text",prev),("next_text",nxt)) if v}
    el_tts(f"C_beat{b:02d}_{s}",*DANIEL,respell(t),S_DANIEL,f"{OUT}/lines/C_beat{b:02d}_{s}.mp3","eleven_multilingual_v2","Method C: Daniel character line, processed afterwards",extra); tot+=len(respell(t))
print("method C characters",tot)
