"""Blue Pill video 1 narration: chunk beats into paragraphs, call ElevenLabs /with-timestamps once per chunk.
Usage: python3 voice.py gen <chunk_ids...|all>   (cached: skips chunks that already have audio/chunks/cNN.json unless --force)
Text sent to TTS = beat text with phonetic respellings of names (1 token -> 1 token, so words map back 1:1).
The saved script / beats.py are never altered."""
import os, sys, json, re, base64, subprocess, csv, time, importlib.util
HERE=os.path.dirname(os.path.abspath(__file__))
AUD=os.path.join(HERE,"audio"); CH=os.path.join(AUD,"chunks"); os.makedirs(CH,exist_ok=True)
VOICE="JBFqnCBsd6RMkjVDRZzb"   # George, same as v2 test (confirmed in TOOLS.md voice decision)
MODEL="eleven_multilingual_v2"
SETTINGS={"stability":0.75,"similarity_boost":0.75,"style":0.05,"use_speaker_boost":True,"speed":float(os.environ.get("VSPEED","0.90"))}
FORMAT="mp3_44100_192"
# respellings (one token each, stress via syllable spelling). Othenio Abel is Austrian/German: first take "Oh-tenny-oh Ah-bel" was heard as
# "oh-ten-e-o" (wrong); now "Oh-TAY-nee-oh AH-bel" (2026-11-12, stressed syllable capitalised for the name only; alt "Oh-TAY-nyo").
# Chunks already generated keep the text they were sent (saved in cNN.json "text"); only chunk 6 was redone with the new spelling.
RESPELL=[("Polyphemus","Pollifeemus"),("Othenio",os.environ.get("OTHENIO_RESP","Oh-TAY-nee-oh")),("Abel",os.environ.get("ABEL_RESP","AH-bel")),("Empedocles","Em-peddokleez"),
 ("Theocritus","Thee-ockritus"),("Thucydides","Thoo-sididdeez"),("Tiryns","Tie-rinz"),("Pausanias","Paw-sayneeus"),
 ("Brontes","Bron-teez"),("Steropes","Stair-oh-peez"),("Arges","Ar-geez"),("Aci","Ah-chee"),("Trezza","Tret-sah"),
 ("Aguirre","Ah-gheereh"),("Burkert","Boor-kert")]
def tts_text(t):
    for a,b in RESPELL: t=re.sub(r'\b'+a+r'\b',b,t)
    return t
def load_beats():
    spec=importlib.util.spec_from_file_location('beats',os.path.join(HERE,'beats.py')); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.R,m.CHAPTERS
def chunks():
    R,_=load_beats(); out=[]
    for i,r in enumerate(R):
        if r['para'] or not out: out.append([])
        out[-1].append(i)
    res=[]
    for k,c in enumerate(out):
        orig=' '.join(R[i]['text'] for i in c); sent=tts_text(orig)
        assert len(orig.split())==len(sent.split()),k
        res.append(dict(id=k,beats=c,ch=R[c[0]]['ch'],orig=orig,sent=sent))
    return res
def call(body):
    path=os.path.join(AUD,"_body.json"); open(path,"w").write(json.dumps(body))
    r=subprocess.run(["curl","-s","-m","180","-X","POST",f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format={FORMAT}",
        "-H","xi-api-key: "+os.environ["ELEVENLABS_API_KEY"],"-H","Content-Type: application/json","-d","@"+path],capture_output=True,text=True)
    try: d=json.loads(r.stdout)
    except Exception: raise SystemExit("non-json response: "+r.stdout[:300]+r.stderr[:200])
    return d
def gen(ids,force=False):
    cs=chunks()
    for c in cs:
        if c['id'] not in ids: continue
        jp=os.path.join(CH,f"c{c['id']:02d}.json")
        if os.path.exists(jp) and not force: print("cached",c['id']); continue
        body={"text":c['sent'],"model_id":MODEL,"voice_settings":SETTINGS}
        if c['id']>0: body["previous_text"]=cs[c['id']-1]['sent'][-300:]
        if c['id']<len(cs)-1: body["next_text"]=cs[c['id']+1]['sent'][:300]
        t0=time.time(); d=call(body)
        if "audio_base64" not in d:
            raise SystemExit(f"STOP: API error on chunk {c['id']}: {str(d)[:400]}")   # auth/quota: stop, do not loop
        open(os.path.join(CH,f"c{c['id']:02d}.mp3"),"wb").write(base64.b64decode(d["audio_base64"]))
        json.dump({"alignment":d["alignment"],"normalized_alignment":d.get("normalized_alignment"),"text":c['sent'],"orig":c['orig']},open(jp,"w"))
        dur=d["alignment"]["character_end_times_seconds"][-1]
        row=[time.strftime("%Y-%m-%dT%H:%M:%S"),c['id'],len(c['sent']),MODEL,VOICE,json.dumps(SETTINGS),FORMAT,round(dur,2),round(time.time()-t0,1),os.environ.get("VNOTE","")]
        lp=os.path.join(AUD,"voice_log.csv"); new=not os.path.exists(lp)
        with open(lp,"a",newline="") as f:
            w=csv.writer(f)
            if new: w.writerow(["time","chunk_id","characters","model_id","voice_id","settings","output_format","alignment_end_s","api_seconds","note"])
            w.writerow(row)
        print("chunk",c['id'],"chars",len(c['sent']),"dur",round(dur,2),"wpm",round(len(c['orig'].split())/dur*60))
if __name__=="__main__":
    a=sys.argv[1:]; force="--force" in a; a=[x for x in a if x!="--force"]
    if a[0]=="gen":
        n=len(chunks()); ids=set(range(n)) if a[1]=="all" else {int(x) for x in a[1:]}
        gen(ids,force)
    elif a[0]=="show":
        for c in chunks(): print(c['id'],c['ch'],len(c['sent']),c['sent'][:90])
