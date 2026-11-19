import os, json, shutil, sys
import numpy as np
from PIL import Image, ImageFilter
import gen
def _edges(im):
    g=np.asarray(im.convert('L').resize((768,512)).filter(ImageFilter.GaussianBlur(1.5)),float)
    gy,gx=np.gradient(g); m=np.hypot(gx,gy); h,w=m.shape
    box=np.asarray(Image.fromarray(m.astype('float32'),mode='F').resize((w//8,h//8),Image.BOX).resize((w,h),Image.BILINEAR))
    return m/(box+1e-3)
def edge_corr(a,b):
    A=Image.open(a).convert('RGB'); B=Image.open(b).convert('RGB').resize(A.size)
    return round(float(np.corrcoef(_edges(A).ravel(),_edges(B).ravel())[0,1]),3)
def derive(cid,master,out,change,size,extra=(),tries=1,thr=0.6,kind='scene'):
    if kind=='scene':
        prompt=f"Edit image 1: keep the same scene, same layout, same geometry, same drawing style and every object in the same place. Change ONLY: {change}. No people."
    else:
        prompt=f"Edit image 1: keep the same character, same face, same drawing style, line weight, colours and the same plain cream background and layout. Change ONLY: {change}."
    if extra: prompt+=" Image 2 is only a reference for the added object."
    pf=gen.HERE+f'/prompts/{cid}.txt'; open(pf,'w').write(prompt)
    best=None; log=[]
    for t in range(1,tries+1):
        tmp=out+f'.try{t}.png'
        os.makedirs(os.path.dirname(out),exist_ok=True)
        r=gen.run(f'{cid}_t{t}',tmp,pf,[master,*extra],size)
        if r!='ok': break
        c=edge_corr(master,tmp); log.append(c); print(cid,t,c,flush=True)
        if best is None or c>best[0]: best=(c,tmp)
        if c>=thr: break
    if best: shutil.copy(best[1],out)
    for t in range(1,tries+1):
        p=out+f'.try{t}.png'
        if os.path.exists(p): os.remove(p)
    json.dump(dict(id=cid,master=master,change=change,edge_corr=log),open(out+'.check.json','w'))
    return log
