# thirds contact sheets + stills for the v1 cut. usage: python full_sheets3.py (needs out/norse_full_frames from render.sh full)
import json,textwrap,subprocess
from PIL import Image,ImageDraw,ImageFont
FF='/home/williamdownard/openclaw-sites/bin/ffmpeg'
TL=json.load(open('src/slice_timeline.json')); cuts=TL['cuts']; D='out/norse_full_frames'
Fm=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',15); Ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
W=400;IH=225;H=IH+62;COLS=6;per=60
for k,n in enumerate('abc'):
    part=cuts[k*per:(k+1)*per]; rows=(len(part)+COLS-1)//COLS
    S=Image.new('RGB',(COLS*W,rows*H),(17,17,17)); d=ImageDraw.Draw(S)
    for i,c in enumerate(part):
        x,y=(i%COLS)*W,(i//COLS)*H
        S.paste(Image.open(f"{D}/{c['beat']}.jpg").resize((W-4,IH-2)),(x+2,y+2))
        d.text((x+4,y+IH),f"{c['beat']} {c['move']} {c['image'][:-4]}",font=Fm,fill=(201,162,39))
        for j,l in enumerate(textwrap.wrap(c['text'],52)[:3]): d.text((x+4,y+IH+17+j*15),l,font=Ft,fill=(235,235,235))
    S.save(f'out/norse_v1_sheet_{n}.jpg',quality=82); print(n,S.size,len(part))
dur=TL['total']/TL['fps']; N=24; fr=[]
for i in range(N):
    t=(i+0.5)*dur/N
    p=f'/tmp/still{i}.jpg'; subprocess.run([FF,'-y','-loglevel','error','-ss',f'{t:.2f}','-i','out/norse_v1_540p.mp4','-frames:v','1','-q:v','3',p],check=True); fr.append((t,p))
w,h=320,180; S=Image.new('RGB',(6*w,4*h)); d=ImageDraw.Draw(S)
for i,(t,p) in enumerate(fr):
    S.paste(Image.open(p).resize((w,h)),((i%6)*w,(i//6)*h)); d.text(((i%6)*w+3,(i//6)*h+3),f'{int(t//60)}:{t%60:04.1f}',font=Fm,fill=(255,255,0))
S.save('out/norse_v1_stills.jpg',quality=85)
