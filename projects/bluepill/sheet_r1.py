import sys,glob,os
from PIL import Image, ImageDraw
d=sys.argv[1]; out=sys.argv[2]
fs=sorted(glob.glob(d+"/*.png")); n=len(fs); cols=3; rows=(n+cols-1)//cols
S=480; P=30; H=S+110
sheet=Image.new("RGB",(cols*(S+P)+P,rows*(H+P)+P),(30,30,30))
dr=ImageDraw.Draw(sheet)
for i,f in enumerate(fs):
    im=Image.open(f).convert("RGB")
    x=P+(i%cols)*(S+P); y=P+(i//cols)*(H+P)
    m=Image.new("L",(S,S),0); ImageDraw.Draw(m).ellipse((0,0,S-1,S-1),fill=255)
    sheet.paste(im.resize((S,S),Image.LANCZOS),(x,y),m)
    sm=im.resize((98,98),Image.LANCZOS); m2=Image.new("L",(98,98),0); ImageDraw.Draw(m2).ellipse((0,0,97,97),fill=255)
    sheet.paste(sm,(x,y+S+8),m2)
    dr.text((x+115,y+S+40),os.path.basename(f)[:-4],fill=(255,255,255))
sheet.save(out,quality=88)
