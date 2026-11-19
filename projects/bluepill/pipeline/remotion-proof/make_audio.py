import os, json, base64, subprocess, re
SHOTS=[
 ("s1_arrive.png","Odysseus and his crew are starving, so they walk into a huge cave full of cheese and sheep. Nobody is home. That is their first mistake."),
 ("s2_trapped.png","Then the owner returns. He is Polyphemus, a Cyclops, and he rolls a boulder across the entrance that twenty-two wagons could not move."),
 ("s3_wine.png","Odysseus cannot win a fight. So he offers the giant a cup of strong wine. The Cyclops loves it, and asks for his name."),
 ("s4_asleep.png","Odysseus says his name is Nobody. The giant promises to eat Nobody last, and falls asleep. That night, the crew sharpens a wooden stake."),
 ("s5b_escape_blinded.png","At dawn, the blinded Cyclops feels the back of every sheep as it leaves. Odysseus and his men are hiding underneath."),
 ("s6_sail.png","The plan works. But as the ship pulls away, Odysseus cannot resist shouting his real name, and that one moment of pride will haunt him for the rest of the journey home."),
]
text=" ".join(t for _,t in SHOTS)
body=json.dumps({"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.5,"similarity_boost":0.75,"style":0.2}})
r=subprocess.run(["curl","-s","-X","POST","https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb/with-timestamps?output_format=mp3_44100_128","-H","xi-api-key: "+os.environ["ELEVENLABS_API_KEY"],"-H","Content-Type: application/json","-d",body],capture_output=True,text=True)
d=json.loads(r.stdout)
if "audio_base64" not in d: raise SystemExit(str(d)[:300])
open("public/narration.mp3","wb").write(base64.b64decode(d["audio_base64"]))
al=d["alignment"]; ch=al["characters"]; st=al["character_start_times_seconds"]; en=al["character_end_times_seconds"]
# words
words=[];cur="";ws=None
for c,s,e in zip(ch,st,en):
    if c.isspace():
        if cur: words.append({"text":cur,"start":ws,"end":pe}); cur=""
    else:
        if not cur: ws=s
        cur+=c; pe=e
if cur: words.append({"text":cur,"start":ws,"end":pe})
# shot boundaries by char offset
shots=[];pos=0
for img,t in SHOTS:
    a=pos; b=pos+len(t); pos=b+1
    shots.append({"image":img,"start":st[a],"end":en[min(b,len(en))-1]})
for i in range(len(shots)-1): shots[i]["end"]=shots[i+1]["start"]
total=en[-1]+0.8; shots[-1]["end"]=total
json.dump({"fps":30,"duration":total,"shots":shots,"words":words},open("data/timing.json","w"),indent=1)
print("chars",len(text),"duration",round(total,1),"words",len(words)); print([ (s["image"],round(s["start"],1),round(s["end"],1)) for s in shots])
