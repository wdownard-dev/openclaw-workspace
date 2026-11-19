import json
from common import *
from places import *
jobs=[]
for k,d in M.items():
    p=wp('pl_'+k,STYLE+" Painted scene: "+d+"."+PLACE_STYLE_NOTE)
    jobs.append(dict(id='pl_'+k,out=f'places/{k}/master.png',prompt_file=p,size='1536x1024',refs=[]))
for k,d in PROPS.items():
    bg='' if k=='oak_mistletoe' else ' Plain flat cream background.'
    p=wp('pr_'+k,STYLE+" "+d+"."+bg+" No people, no text, no labels. Thick dark ink outline, flat warm shading.")
    jobs.append(dict(id='pr_'+k,out=f'props/{k}/prop.png',prompt_file=p,size='1536x1024',refs=[]))
json.dump(jobs,open('jobs_places1.json','w'),indent=1); print(len(jobs))
