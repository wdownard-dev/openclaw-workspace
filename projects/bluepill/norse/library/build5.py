import json,sys,os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from places import *
import derive_n
def crops():
    for k,(m,(x0,y0,x1,y1)) in CR.items():
        im=Image.open(f'places/{m}/master.png'); W,H=im.size
        c=im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H))).resize((1536,1024),Image.LANCZOS)
        os.makedirs(f'places/{k}',exist_ok=True); c.save(f'places/{k}/variant.png')
def one(k):
    m,change,extra=V[k]
    return k,derive_n.derive('v_'+k,f'places/{m}/master.png',f'places/{k}/variant.png',change,'1536x1024',extra=extra,tries=1,thr=0.6)
if __name__=='__main__':
    crops()
    ids=sys.argv[1:] or list(V)
    with ThreadPoolExecutor(3) as ex: res=list(ex.map(one,ids))
    json.dump(dict(res),open('derive_places.json','w'),indent=1)
