from PIL import Image,ImageDraw,ImageFont
F='/home/williamdownard/.openclaw/workspace/projects/bluepill/video2/remotion-v3/public/fonts/PermanentMarker-Regular.ttf'
W,H=1280,720
cfg={'A':("NOBODY",(50,40),"la",190,(255,214,64)),
     'B':("THE ESCAPE",(50,40),"la",150,(255,214,64)),
     'C':("THE REAL\nCYCLOPS?",(W//2,H-40),"ms",130,(255,255,255))}
for k,(t,xy,anch,sz,col) in cfg.items():
    im=Image.open(f'raw/raw_{k}.png').convert('RGB').resize((W,H),Image.LANCZOS)
    d=ImageDraw.Draw(im); f=ImageFont.truetype(F,sz)
    if k=='C':
        lines=t.split('\n'); y=H-30
        for ln in reversed(lines):
            for dx in range(-8,9,4):
                for dy in range(-8,9,4): d.text((W//2+dx,y+dy),ln,font=f,fill=(15,15,25),anchor="ms",stroke_width=6,stroke_fill=(15,15,25))
            d.text((W//2,y),ln,font=f,fill=col,anchor="ms"); y-=sz*0.95
    else:
        d.text(xy,t,font=f,fill=col,anchor=anch,stroke_width=10,stroke_fill=(15,15,25))
    im.save(f'thumb_{k}.jpg',quality=92)
s=Image.new('RGB',(W*3//2+40,H//2+20),(20,20,20))
for i,k in enumerate('ABC'):
    s.paste(Image.open(f'thumb_{k}.jpg').resize((W//2,H//2)),(10+i*(W//2+10),10))
s.save('thumbs_3up.jpg',quality=92)
