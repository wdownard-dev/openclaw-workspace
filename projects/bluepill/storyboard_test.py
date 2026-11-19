import os, json, base64, urllib.request, uuid, concurrent.futures as cf
KEY=os.environ["OPENAI_API_KEY"]; OUT="tests/storyboard"
HERO="tests/characters/01_round_hero.png"; CY="tests/characters3/cyclops.png"
STYLE=" Both characters must stay identical to the two reference images (image 1 = the hero with laurel wreath, image 2 = the one-eyed giant Cyclops) and keep the same flat minimal cartoon style. Flat-shaded illustrated background, muted palette, wide 3:2 frame, no text, no letters."
SHOTS=[
 ("s1_arrive","Wide shot: the small hero and two tiny companions silhouettes approach the huge cave entrance on a rocky seaside hill at dusk, a flock of sheep outside. Only the hero is a full character."+""),
 ("s2_trapped","Inside the dark cave: the Cyclops has just rolled a giant boulder across the entrance and blocks it with one arm raised, the hero stands small in the foreground looking up in alarm, firelight."),
 ("s3_wine","The hero politely offers the Cyclops a big clay cup of wine in front of a campfire inside the cave, the Cyclops is smiling happily and reaching for the cup."),
 ("s4_asleep","The Cyclops is fast asleep on his back snoring with Z-shaped dust puffs, huge, the hero tiptoes beside him with a finger to his lips, cave lit by dim embers."),
 ("s5_escape","Dawn at the cave mouth: the hero clings underneath a large fluffy sheep to sneak out past the Cyclops who sits blindly feeling the sheep's backs, golden sunrise outside."),
 ("s6_sail","The hero stands at the back of a wooden ship sailing away on a calm sea at sunrise, waving, the Cyclops tiny and angry on the distant cliff throwing a rock."),
]
def mp(fields,files):
    b=uuid.uuid4().hex; body=b""
    for k,v in fields.items(): body+=f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k,p in files: body+=f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{os.path.basename(p)}"\r\nContent-Type: image/png\r\n\r\n'.encode()+open(p,"rb").read()+b"\r\n"
    return body+f'--{b}--\r\n'.encode(), b
def run(s):
    name,desc=s
    body,b=mp({"model":"gpt-image-2.6-sunburst","size":"1536x1024","quality":"medium","prompt":desc+STYLE},[("image[]",HERO),("image[]",CY)])
    req=urllib.request.Request("https://api.openai.com/v1/images/edits",body,{"Authorization":"Bearer "+KEY,"Content-Type":f"multipart/form-data; boundary={b}"})
    try:
        d=json.load(urllib.request.urlopen(req,timeout=400)); open(f"{OUT}/{name}.png","wb").write(base64.b64decode(d["data"][0]["b64_json"])); return name,"ok",d.get("usage",{}).get("output_tokens")
    except Exception as e: return name,"ERR",str(getattr(e,"read",lambda:b"")()[:200] or e)
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(run,SHOTS): print(*r)
