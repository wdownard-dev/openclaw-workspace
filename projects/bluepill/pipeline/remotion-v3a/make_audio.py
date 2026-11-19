"""Narration for the v2 upgrade test. One ElevenLabs TTS call per paragraph (same voice/settings as the proof),
paragraphs placed on a timeline with explicit gaps. '|' marks a shot cut inside a paragraph.
Writes public/vo/vo_N.mp3 and data/timing.json (global word times, paragraph offsets, shot boundaries)."""
import os, json, base64, subprocess
VOICE="JBFqnCBsd6RMkjVDRZzb"
# (text, gap_after_seconds)
PARAS=[
 ("Twelve men walk into this cave. | Six never walk out.", 0.25),
 ("Ten years after Troy, Odysseus is still sailing home. | His crew is starving, so they walk into a huge cave full of cheese and sheep. | Nobody is home. That is their first mistake.", 0.35),
 ("Then the owner returns. He is Polyphemus, a Cyclops, | and he rolls a boulder across the entrance that twenty-two wagons could not move.", 0.35),
 ("Odysseus cannot win a fight. So he offers the giant a cup of strong wine. | The Cyclops loves it, and asks for his name.", 0.3),
 ("Odysseus says his name is Nobody. | The giant promises to eat Nobody last, and falls asleep. | That night, the crew sharpens a wooden stake.", 0.35),
 ("Now the giant is blind. But the boulder is still there, and he is waiting at the door.", 0.35),
 ("At dawn, the blinded Cyclops feels the back of every sheep as it leaves. | Odysseus and his men are hiding underneath.", 0.35),
 ("The plan works. | But as the ship pulls away, Odysseus cannot resist shouting his real name, | and that one moment of pride will haunt him for the rest of the journey home.", 0.6),
 ("Next: the god who heard that name, and what he did to the sea.", 0.0),
]
TITLE_GAP=2.4   # silent chapter-card gap inserted after paragraph 0
FPS=30
os.makedirs("public/vo",exist_ok=True)
plain=[" ".join(x.strip() for x in p.split("|")) for p,_ in PARAS]
timeline=0.0; words=[]; shots=[]; paras=[]
for i,(raw,gap) in enumerate(PARAS):
    text=plain[i]
    cache=f"data/vo_{i}.json"
    if not os.path.exists(cache):
        body=json.dumps({"text":text,"model_id":"eleven_multilingual_v2",
            "voice_settings":{"stability":0.5,"similarity_boost":0.75,"style":0.2},
            **({"previous_text":plain[i-1]} if i>0 else {}),**({"next_text":plain[i+1]} if i<len(PARAS)-1 else {})})
        r=subprocess.run(["curl","-s","-X","POST",f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
            "-H","xi-api-key: "+os.environ["ELEVENLABS_API_KEY"],"-H","Content-Type: application/json","-d",body],capture_output=True,text=True)
        d=json.loads(r.stdout)
        if "audio_base64" not in d: raise SystemExit(str(d)[:300])
        open(f"public/vo/vo_{i}.mp3","wb").write(base64.b64decode(d["audio_base64"]))
        json.dump(d["alignment"],open(cache,"w"))
    al=json.load(open(cache)); ch=al["characters"]; st=al["character_start_times_seconds"]; en=al["character_end_times_seconds"]
    # cut positions: char index in the plain text where each '|' segment starts
    segs=[x.strip() for x in raw.split("|")]
    cuts=[]; k=0
    for sg in segs[:-1]:
        k+=len(sg)+1; cuts.append(k)
    # words with char offsets
    pw=[];cur="";ws=None;wi=None;pe=0
    for idx,(c,s,e) in enumerate(zip(ch,st,en)):
        if c.isspace():
            if cur: pw.append({"text":cur,"start":ws+timeline,"end":pe+timeline,"ci":wi}); cur=""
        else:
            if not cur: ws=s; wi=idx
            cur+=c; pe=e
    if cur: pw.append({"text":cur,"start":ws+timeline,"end":pe+timeline,"ci":wi})
    # shot starts: first word whose char index >= cut index (cut index points at the space before the next word)
    starts=[pw[0]["start"]]
    for cidx in cuts:
        nxt=[w for w in pw if w["ci"]>=cidx][0]; starts.append(nxt["start"])
    for w in pw: w.pop("ci")
    for j,s in enumerate(starts): shots.append({"para":i,"seg":j,"start":s})
    words+=pw
    dur=en[-1]
    paras.append({"i":i,"offset":timeline,"dur":dur,"start":pw[0]["start"],"end":pw[-1]["end"]})
    timeline+=dur+gap
    if i==0:
        shots.append({"para":-1,"seg":0,"start":timeline,"kind":"title"})   # chapter card in silent gap
        timeline+=TITLE_GAP
        # the audio offsets of subsequent paragraphs already include the gap via timeline
# end card starts when last paragraph starts; tail after narration
last=paras[-1]; TAIL=3.0
total=last["end"]+TAIL
# the first shot of the para after title card must start after the title card; shot ends computed here
shots.sort(key=lambda s:s["start"])
for a,b in zip(shots,shots[1:]): a["end"]=b["start"]
shots[-1]["end"]=total
# stretch each paragraph's last shot to absorb its trailing gap (handled by next start); first shot starts at 0
shots[0]["start"]=0.0
json.dump({"fps":FPS,"duration":total,"paras":paras,"shots":shots,"words":words},open("data/timing.json","w"),indent=1)
print("duration",round(total,1),"words",len(words),"shots",len(shots))
for s in shots: print(s["para"],s["seg"],round(s["start"],2),round(s["end"],2),round(s["end"]-s["start"],2))
