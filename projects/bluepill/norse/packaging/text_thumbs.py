from PIL import Image,ImageDraw,ImageFont
F='/home/williamdownard/.openclaw/workspace/projects/bluepill/video2/remotion-v3/public/fonts/PermanentMarker-Regular.ttf'
W,H=1280,720
Y=(255,214,64); WH=(255,255,255); INK=(15,15,25)
cfg={'A':('raw_A2.png',"THE SKY\nIS A SKULL"),'B':('raw_B2.png',"RAGNAROK")}
def draw(d,xy,t,sz,col,anchor,sw):
    d.text(xy,t,font=ImageFont.truetype(F,sz),fill=col,anchor=anchor,stroke_width=sw,stroke_fill=INK,spacing=0)
for k,(raw,t) in cfg.items():
    im=Image.open('raw/'+raw).convert('RGB').resize((W,H),Image.LANCZOS); d=ImageDraw.Draw(im)
    sz=150 if k=='A' else 175
    ImageDraw.ImageDraw.multiline_text(d,(40,25),t,font=ImageFont.truetype(F,sz),fill=Y,stroke_width=10,stroke_fill=INK,spacing=-10)
    draw(d,(W-30,H-25),"in 10 minutes",78,WH,"rs",8)
    im.save(f'thumb_{k}.jpg',quality=92)
s=Image.new('RGB',(W+30,H//2*1+20),(20,20,20))
for i,k in enumerate('AB'): s.paste(Image.open(f'thumb_{k}.jpg').resize((W//2,H//2)),(10+i*(W//2+10),10))
s.save('thumbs_2up.jpg',quality=92)
s=Image.new('RGB',(660,190),(20,20,20))
for i,k in enumerate('AB'): s.paste(Image.open(f'thumb_{k}.jpg').resize((320,180)),(10+i*330,5))
s.save('raw/small_check.jpg')
