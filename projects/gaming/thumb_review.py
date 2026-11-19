#!/usr/bin/env python3
"""Build out/thumbs/review_sheet_N.png: current auto-thumbnail (first Short frame) | new thumbnail."""
import os
from PIL import Image, ImageDraw, ImageFont
import importlib.util
D=os.path.dirname(os.path.abspath(__file__)); OUT=D+"/out/thumbs"
spec=importlib.util.spec_from_file_location("tm",D+"/thumb_make.py"); tm=importlib.util.module_from_spec(spec); spec.loader.exec_module(tm)
LIVE={"iSgpSI7KrJQ","BEtSNncs-8Q","v1331JIwRNs","W0g79Gzpw6Y","8gCNaCdIyyo","Bk3drifXNas","8L0Ix62AJlg","6AnNLkEO8Cs","fM5XtZZl2ds"}
TITLE={"iSgpSI7KrJQ":"Fortnite Pirate Shop Token (walk v4)","BEtSNncs-8Q":"Carian Regal Scepter + Rennala spell","v1331JIwRNs":"Bloodhound's Step early","W0g79Gzpw6Y":"Mimic Tear Ashes","8gCNaCdIyyo":"Mini Miku Sprite","Bk3drifXNas":"Pirate Shop Token chest route","8L0Ix62AJlg":"Frog statue two rare chests","6AnNLkEO8Cs":"Uchigatana early","fM5XtZZl2ds":"Moonveil Katana","O4-F81c2n6E":"Flask of Wondrous Physick early","pchWVunshDQ":"Jam Track container quest","6m8FUczYGHU_poster":"Sprite wanted poster chest quest","6m8FUczYGHU_fruit":"Consume a Devil Fruit quest","Oxh7-i4mXLc":"Pirate Token: Best Chest Route (Lucky Sprite)","LkSzM6mbLC8":"Sprite Chest Trick: reuse Treasure Map","WZMrijY6TzI":"Bolt of Gransax (no faith)","S65gy4AC_kI":"Gum-Gum Fruit: break every chest","AecawgyFqXg":"Messmer the Impaler route","tsK0MAnTik0":"Gum-Gum Fruit almost every match"}
ids=list(tm.V); f=ImageFont.truetype(tm.FONT,30); tw,th=300,533
per=10
for n in range(0,len(ids),per):
    part=ids[n:n+per]; cols=2; rows=(len(part)+1)//2
    cw=2*tw+30+40; ch=th+60
    s=Image.new("RGB",(cols*cw,rows*ch),(24,24,28)); d=ImageDraw.Draw(s)
    for i,k in enumerate(part):
        x=(i%cols)*cw+20; y=(i//cols)*ch
        d.text((x,y+4),f"{k}  {'LIVE/SCHEDULED' if k in LIVE else 'BUILT'}",font=ImageFont.truetype(tm.FONT,22),fill=(255,214,0))
        d.text((x,y+28),TITLE[k],font=ImageFont.truetype(tm.FONT,26),fill=(255,255,255))
        old=Image.open(f"{tm.WORK}/{k}/f01.jpg").resize((tw,th)); new=Image.open(f"{OUT}/{k}.png").convert("RGB").resize((tw,th))
        s.paste(old,(x,y+58-8)); s.paste(new,(x+tw+30,y+58-8))
    s.save(f"{OUT}/review_sheet_{n//per+1}.png"); print("sheet",n//per+1,s.size)
