# contact sheet: one render-time frame per beat from the muxed mp4 -> out/${NAME}_sheet.jpg (env NAME)
import json,subprocess,os,textwrap
from PIL import Image,ImageDraw,ImageFont
NAME=os.environ.get('NAME','norse_slice')
FF='/home/williamdownard/openclaw-sites/bin/ffmpeg'
TL=json.load(open('src/slice_timeline.json')); cuts=TL['cuts']; D=f'out/{NAME}_frames'; os.makedirs(D,exist_ok=True)
for c in cuts:
    t=min(c['start_s']+0.3,TL['total']/TL['fps']-0.1)
    subprocess.run([FF,'-y','-loglevel','error','-ss',f'{t:.3f}','-i',f'out/{NAME}_540p.mp4','-frames:v','1','-q:v','3',f"{D}/{c['beat']}.jpg"],check=True)
Fm=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',15); Ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
W=400;IH=225;H=IH+62;COLS=6
rows=(len(cuts)+COLS-1)//COLS; S=Image.new('RGB',(COLS*W,rows*H),(17,17,17)); d=ImageDraw.Draw(S)
for i,c in enumerate(cuts):
    x,y=(i%COLS)*W,(i//COLS)*H
    S.paste(Image.open(f"{D}/{c['beat']}.jpg").resize((W-4,IH-2)),(x+2,y+2))
    d.text((x+4,y+IH),f"{c['beat']} {c['move']} {c['image'][:-4]}",font=Fm,fill=(201,162,39))
    for k,l in enumerate(textwrap.wrap(c['text'],52)[:3]): d.text((x+4,y+IH+17+k*15),l,font=Ft,fill=(235,235,235))
S.save(f'out/{NAME}_sheet.jpg',quality=85); print(f'out/{NAME}_sheet.jpg',S.size)
