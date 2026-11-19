import json, os, glob, shutil
from PIL import Image, ImageDraw, ImageFont
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(s):
    try: return ImageFont.truetype(FB,s)
    except: return ImageFont.load_default()
BG=(250,238,215)
def fit(path,w,h):
    im=Image.open(path).convert('RGB'); im.thumbnail((w,h)); c=Image.new('RGB',(w,h),BG); c.paste(im,((w-im.width)//2,(h-im.height)//2)); return c
def sheet(folder,title,items,cols_w,out='sheet.jpg'):
    pass
CH={
 'odysseus':("ODYSSEUS",[('turnaround','TURNAROUND  front / three-quarter / back'),('expressions','EXPRESSIONS'),('wardrobe','WARDROBE')],[('face','FACE'),('silhouette','SILHOUETTE')]),
 'polyphemus':("POLYPHEMUS",[('turnaround','TURNAROUND  front / three-quarter / back'),('expressions','EXPRESSIONS'),('wardrobe','WARDROBE')],[('face','FACE'),('silhouette','SILHOUETTE')]),
 'polyphemus_blinded':("POLYPHEMUS (BLINDED)",[('turnaround','TURNAROUND  scarred hollow'),('turnaround_band','TURNAROUND  cloth band variant'),('expressions','EXPRESSIONS')],[('face','FACE'),('silhouette','SILHOUETTE')]),
 'crewman':("CREWMAN",[('turnaround','TURNAROUND  crewman A'),('expressions','EXPRESSIONS'),('wardrobe','WARDROBE')],[('face','FACE'),('silhouette','SILHOUETTE'),('turnaround_b','VARIANT B  curly hair, stubble'),('turnaround_c','VARIANT C  older, grey beard')]),
}
for k,(title,left,right) in CH.items():
    d=f'characters/{k}/'; LW,LH,RW=1500,1000,900
    pad=20; head=110; lab=44
    H=head+max(len(left)*(LH+lab+pad), sum((RW if n in('face','silhouette') else 600)+lab+pad for n,_ in right))+pad
    S=Image.new('RGB',(LW+RW+3*pad,H),BG); dr=ImageDraw.Draw(S)
    dr.text((pad,20),title+'  -  model sheet',fill=(31,58,95),font=font(64))
    y=head
    for n,l in left:
        dr.text((pad,y),l,fill=(60,40,20),font=font(32)); S.paste(fit(d+n+'.png',LW,LH),(pad,y+lab)); y+=LH+lab+pad
    y=head
    for n,l in right:
        h=RW if n in('face','silhouette') else 600
        dr.text((LW+2*pad,y),l,fill=(60,40,20),font=font(32)); S.paste(fit(d+n+'.png',RW,h),(LW+2*pad,y+lab)); y+=h+lab+pad
    S.save(d+'sheet.jpg',quality=88); print(k,S.size)
PL={'cave_exterior':['day_wide','dusk_wide','night_wide','boulder_sealing_mouth'],
 'cave_interior':['day_shaft_of_light','night_firelight','sealed_boulder_from_inside','cheese_racks_and_pens'],
 'beach_and_ship':['morning','ship_at_sea_wide'],'hillside_pasture':['dusk']}
for k,ns in PL.items():
    d=f'places/{k}/'; w,h=1200,800; cols=2 if len(ns)>1 else 1; rows=(len(ns)+cols-1)//cols
    S=Image.new('RGB',(cols*w+(cols+1)*20,110+rows*(h+44+20)),BG); dr=ImageDraw.Draw(S)
    dr.text((20,20),k.replace('_',' ').upper()+'  -  place sheet',fill=(31,58,95),font=font(60))
    for i,n in enumerate(ns):
        x=20+(i%cols)*(w+20); y=110+(i//cols)*(h+64)
        dr.text((x,y),n.replace('_',' ').upper(),fill=(60,40,20),font=font(30)); S.paste(fit(d+n+'.png',w,h),(x,y+44))
    S.save(d+'sheet.jpg',quality=88); print(k,S.size)
