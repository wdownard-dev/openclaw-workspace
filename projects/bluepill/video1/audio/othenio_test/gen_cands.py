import os,sys,json,base64,subprocess,re
sys.path.insert(0,'/home/williamdownard/.openclaw/workspace/projects/bluepill/video1')
import voice
OUT=os.path.dirname(os.path.abspath(__file__))
PREV="During the Ice Age, dwarf elephants lived on islands across the Mediterranean."
PH='<phoneme alphabet="ipa" ph="oˈteːnjo">Othenio</phoneme> <phoneme alphabet="ipa" ph="ˈaːbl̩">Abel</phoneme>'
C=[(1,"Othenio Abel",voice.MODEL),(2,"Oh-tay-nyo Ah-bel",voice.MODEL),(3,"Otenyo Ahbel",voice.MODEL),(4,"Oh-TAY-nee-oh AH-bull",voice.MODEL),
(5,"Ottaynio Abel",voice.MODEL),(6,"Oh-teh-nee-oh Ah-bel",voice.MODEL),(7,PH,"eleven_turbo_v2_5")]
S=dict(voice.SETTINGS); S["speed"]=1.0
log=[]
for n,name,model in C:
    text=f"In 1914, the palaeontologist {name} thought there might be."
    s=dict(S)
    if model!=voice.MODEL: s.pop("speed",None); s["speed"]=1.0
    body={"text":text,"model_id":model,"voice_settings":s,"previous_text":PREV}
    d=voice.call(body)
    if "audio_base64" not in d:
        print(n,"ERROR",str(d)[:400]); log.append(dict(n=n,text=text,model=model,error=str(d)[:400])); continue
    open(f"{OUT}/cand_{n}.mp3","wb").write(base64.b64decode(d["audio_base64"]))
    al=d["alignment"]; ch=al["characters"]; st=al["character_start_times_seconds"]; en=al["character_end_times_seconds"]
    t=''.join(ch); a=t.find(name) if n!=7 else t.find("Othenio")
    # name span: from name start to end of 'Abel' (just before ' thought')
    b=t.find(" thought")
    nd=en[b-1]-st[a]
    print(n,model,"chars",len(text),"name",round(st[a],2),"->",round(en[b-1],2),"dur",round(nd,2),"total",round(en[-1],2))
    log.append(dict(n=n,text=text,model=model,chars=len(text),name_start=st[a],name_end=en[b-1],name_dur=nd,total=en[-1],spoken_text_alignment=t))
json.dump(log,open(f"{OUT}/results.json","w"),ensure_ascii=False,indent=1)
