import os
from PIL import Image,ImageDraw,ImageFont
from data import C,D
from places import M,V,CR,PROPS
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(s,b=True): return ImageFont.truetype(FB if b else FR,s)
BG=(250,238,215); INK=(31,58,95); BR=(60,40,20)
def fit(path,w,h):
    im=Image.open(path).convert('RGB'); im.thumbnail((w,h)); c=Image.new('RGB',(w,h),BG); c.paste(im,((w-im.width)//2,(h-im.height)//2)); return c
def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def card(cid,title,files,tells,scale,out):
    W=1600; pad=30
    S=Image.new('RGB',(W,2000),BG); d=ImageDraw.Draw(S); y=pad
    d.text((pad,y),title,fill=INK,font=font(60)); y+=84
    line='  |  '.join(tells)
    for l in wrap(d,line,font(34),W-2*pad): d.text((pad,y),l,fill=BR,font=font(34)); y+=44
    y+=14
    main,face=files
    if face:
        S.paste(fit(main,W-2*pad,1010),(pad,y)); y+=1010+16
        S.paste(fit(face,560,560),(pad,y)); d.text((pad+590,y+10),'FACE CLOSE-UP',fill=BR,font=font(30))
        yy=y+60
        if scale:
            for l in wrap(d,'SCALE NOTE: '+scale,font(30),W-2*pad-600): d.text((pad+590,yy),l,fill=BR,font=font(30)); yy+=40
        y+=560
    else:
        S.paste(fit(main,W-2*pad,1060 if 'turnaround' in main else 1000),(pad,y)); y+=(1060 if 'turnaround' in main else 1000)
        if scale:
            y+=14
            for l in wrap(d,'SCALE NOTE: '+scale,font(30),W-2*pad): d.text((pad,y),l,fill=BR,font=font(30)); y+=40
    S=S.crop((0,0,W,y+pad)); S.save(out,quality=92); return out
def build_all():
    out=[]
    for k,(t,tier,desc,tells,sc) in C.items():
        b=f'characters/{k}/'
        if tier=='FULL': f=(b+'turnaround.png',b+'face.png')
        else: f=(b+'front.png',None)
        out.append((k,card(k,t,f,tells,sc,f'refs/{k}__card.png')))
    for k,(t,parent,ch,tells,sc) in D.items():
        b=f'characters/{k}/'
        main=b+('front.png' if k=='loki_salmon' else 'turnaround.png')
        face=b+'face.png' if os.path.exists(b+'face.png') else None
        out.append((k,card(k,t,(main,face),tells,sc,f'refs/{k}__card.png')))
    props={'chains_and_ribbon':("PROP: CHAINS AND RIBBON",["thick iron chain","very thin pale silk ribbon"],"ribbon about 1/20 the width of the chain; chain links the size of Thor's fist, second chain twice as thick"),
     'ox_head_hook':("PROP: OX HEAD, HOOK, ROPE",["huge ox head","wide curved horns","iron hook","heavy rope"],"head about 1.0 (as long as Thor is tall), horns wider than his shoulders; hook 0.6 Thor-height; rope as thick as his wrist"),
     'hymirs_boat':("PROP: HYMIR'S BOAT",["wooden rowboat","clinker planks","oars"],"hull about 4 Thor-heights long: big enough for Thor in the bow and Hymir (3.0) in the stern"),
     'oak_mistletoe':("PROP: OAK AND MISTLETOE",["oak branch","green sprig","white berries"],"the sprig is tiny (a hand-length); enlarge far beyond true scale in every close shot"),
     'naglfar':("PROP: NAGLFAR",["ship of fingernails","pale curved planks","ragged pale sail"],"hull as long as the sea shot is wide; empty deck")}
    for k,(t,tl,sc) in props.items():
        out.append((k,card(k,t,(f'props/{k}/prop.png',None),tl,sc,f'refs/{k}__card.png')))
    return out
if __name__=='__main__':
    o=build_all(); print(len(o))
