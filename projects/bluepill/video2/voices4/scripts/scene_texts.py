"""Scene texts for the three methods (beats from SCRIPT-V3.md; Polyphemus respelled Pollifeemus in speech as in round 2)."""
import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
B=parse_script()
TAG={"ODY":"[dry, controlled]","POLY":"[slow, enormous, gentle]","CYC2":"[bored, flat]","CREW":"[earnest, nervous]"}
TAG_BEAT={38:"[enormous, bellowing in pain]",64:"[earnest, nervous, quietly]",66:"[flat, horrified]",68:"[earnest, nervous, puzzled]"}
ATTR={28:"said Odysseus, quite calmly",30:"the giant rumbled",31:"said Odysseus",37:"a Cyclops asked, bored",38:"the giant bellowed",39:"the Cyclops said flatly",64:"the sailor asked",}
def line(b,mode):
    s,t=B[b]; t=respell(t)
    if s=="NARR": return t
    if mode=="v4tags": return f'{TAG_BEAT.get(b,TAG[s])} "{t}"'
    if mode=="v2attr":
        a=ATTR.get(b); end=t[-1]
        if a: return f'"{t[:-1]}{"," if end=="." else end}" {a}.'.replace('?,','?').replace('!,','!')
        return f'"{t}"'
    if mode=="plain": return t                         # for dialogue / per-speaker calls
    if mode=="dlg": return f'{TAG_BEAT.get(b,TAG[s])} {t}'
    raise ValueError(mode)
def passage(i,mode): return "\n\n".join(line(b,mode) for b in SCENES[i])
if __name__=="__main__":
    for m in ("v2attr",):
        for i in range(2): p=passage(i,m); print(m,i,len(p)); print(p); print()
