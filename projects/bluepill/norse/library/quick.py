import sys
from PIL import Image,ImageDraw,ImageFont
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def sheet(items,out,cols=3,w=800,h=560):
    f=ImageFont.truetype(FB,26); rows=(len(items)+cols-1)//cols
    S=Image.new('RGB',(cols*w,rows*(h+34)),(250,238,215)); d=ImageDraw.Draw(S)
    for i,(lab,p) in enumerate(items):
        im=Image.open(p).convert('RGB'); im.thumbnail((w-8,h)); x=(i%cols)*w; y=(i//cols)*(h+34)
        d.text((x+6,y+3),lab,fill=(31,58,95),font=f); S.paste(im,(x+(w-im.width)//2,y+34))
    S.save(out,quality=85)
if __name__=='__main__':
    items=[(a.split('=')[0],a.split('=')[1]) for a in sys.argv[2:]]
    sheet(items,sys.argv[1])
