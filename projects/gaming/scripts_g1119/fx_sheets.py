import sys
from PIL import Image, ImageDraw, ImageFont
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
d="/home/williamdownard/.openclaw/workspace/projects/gaming/work/fluxx_1119/fr"
for s in range(5):
    im=Image.new("RGB",(4*360,3*640))
    for i in range(12):
        n=s*12+i+1
        im.paste(Image.open(f"{d}/f_{n:02d}.png"),((i%4)*360,(i//4)*640))
        ImageDraw.Draw(im).text(((i%4)*360+4,(i//4)*640+2),f"{n-1}s",fill="yellow",font=ImageFont.truetype(F,26))
    im.save(f"{d}/sheet{s}.jpg",quality=85)
