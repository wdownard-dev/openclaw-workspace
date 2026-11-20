#!/usr/bin/env python3
"""fsheet.py FILE START END STEP OUT : labelled sheet (4 cols, 400x225), label = t+offset where offset arg OFF (default 0)."""
import sys,subprocess
from PIL import Image,ImageDraw,ImageFont
FF="/home/williamdownard/openclaw-sites/bin/ffmpeg"; F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f,s,e,st,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
off=float(sys.argv[6]) if len(sys.argv)>6 else 0
ts=[];t=s
while t<=e: ts.append(t); t+=st
ts=ts[:24]; cols=4; rows=(len(ts)+3)//4
im=Image.new("RGB",(cols*400,rows*225))
for i,t in enumerate(ts):
    subprocess.run([FF,"-y","-loglevel","error","-ss",f"{t:.2f}","-i",f,"-frames:v","1","-vf","scale=400:225","/tmp/_fs.jpg"],check=True)
    x,y=(i%cols)*400,(i//cols)*225
    im.paste(Image.open("/tmp/_fs.jpg"),(x,y)); ImageDraw.Draw(im).text((x+4,y+2),f"{t+off:.0f}",fill="yellow",font=ImageFont.truetype(F,22))
im.save(out,quality=82); print(out)
