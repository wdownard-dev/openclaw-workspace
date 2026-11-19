import json
from common import *
from data import *
jobs=[]
for k,(t,tier,d,tells,sc) in C.items():
    if tier!='FULL': continue
    b=f'characters/{k}/'
    extra=" Same character as the attached reference image (show the first character only, if several)." 
    jobs.append(dict(id=k+'_face',out=b+'face.png',prompt_file=wp(k+'_face',P(FACE,d+extra)),size='1024x1024',refs=[b+'turnaround.png']))
json.dump(jobs,open('jobs_faces.json','w'),indent=1); print(len(jobs))
