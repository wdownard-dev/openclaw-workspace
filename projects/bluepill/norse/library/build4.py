# phase 2: faces (FULL, ref own turnaround) + derived character cards + thor_disguise; run in batch via gen, then derives via derive_n
import json,sys
from concurrent.futures import ThreadPoolExecutor
from common import *
from data import *
import derive_n
def one(k):
    t,parent,change,tells,sc=D[k]
    out=f'characters/{k}/'+('front.png' if k=='loki_salmon' else 'turnaround.png')
    return k,derive_n.derive('d_'+k,f'characters/{parent}/turnaround.png',out,change,'1536x1024',tries=1,kind='char')
if __name__=='__main__':
    ids=sys.argv[1:] or list(D)
    with ThreadPoolExecutor(3) as ex: res=list(ex.map(one,ids))
    json.dump(dict(res),open('derive_chars.json','w'),indent=1)
