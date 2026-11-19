import json
from common import *
from data import *
jobs=[]
def add(cid,out,pf,size,refs=()):
    jobs.append(dict(id=cid,out=out,prompt_file=pf,size=size,refs=list(refs)))
for k,(t,tier,d,tells,sc) in C.items():
    b=f'characters/{k}/'
    if k=='odin_one_eye': continue
    if tier=='FULL':
        add(k+'_turn',b+'turnaround.png',wp(k+'_turn',P(TURN,d)),'1536x1024')
    else:
        size='1024x1536' if k=='eagle_nidhogg_ratatosk' else '1024x1024'
        add(k+'_card',b+'front.png',wp(k+'_card',P(SIMPLE,d)),size)
json.dump(jobs,open('jobs_chars1.json','w'),indent=1); print(len(jobs))
