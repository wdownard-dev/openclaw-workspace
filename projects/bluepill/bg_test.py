import os, json, base64, time, urllib.request, concurrent.futures as cf, sys
KEY = os.environ["OPENAI_API_KEY"]
OUT = "tests/round1"
STYLE = ("Flat-shaded illustrated concept art for a 2D animated history explainer: simplified shapes, soft painterly gradients, "
         "limited muted palette with one warm accent, subtle paper texture, clean readable composition, wide 3:2 frame, "
         "no people, no characters, no text, no letters, no logos.")
SCENES = {
 "cyclops_cave": "the dark cave of the Cyclops Polyphemus, huge boulder at the entrance, sheep pens, a dying fire, bones on the floor",
 "storm_ship": "an ancient Greek wooden ship tossed on a stormy night sea, huge waves, lightning, torn sail",
 "olympus": "the peak of Mount Olympus above the clouds with a grand marble temple of the gods at golden sunset",
 "underworld": "the underworld river Styx, a ferry boat, pale mist, dark cavern with a distant gate guarded by shadow",
 "egypt_temple": "an ancient Egyptian temple hall with giant painted columns, hieroglyph walls, shafts of sunlight and drifting dust",
 "norse_hall": "a Viking longhall interior with a central fire pit, carved wooden beams, shields on the walls, snow visible through the door",
 "map_table": "a top-down ancient parchment map table of the Mediterranean with ink coastlines, a compass, and small ship tokens, plenty of empty space",
 "troy_walls": "the massive stone walls and gates of ancient Troy at dawn, a large empty plain in front, smoke on the horizon",
}
JOBS = []
for s in ["cyclops_cave","storm_ship","olympus","underworld","egypt_temple","norse_hall"]:
    for m in ["gpt-image-2","gpt-image-2.6-flare","gpt-image-2.6-sunburst"]:
        JOBS.append((s,m))
JOBS += [("map_table","gpt-image-2"),("troy_walls","gpt-image-2")]
def run(job):
    s,m = job
    body = json.dumps({"model":m,"size":"1536x1024","quality":"medium","n":1,"prompt":f"{SCENES[s]}. {STYLE}"}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", body,
        {"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
    t=time.time()
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
        fn=f"{OUT}/{s}__{m}.png"
        open(fn,"wb").write(base64.b64decode(d["data"][0]["b64_json"]))
        return {"scene":s,"model":m,"secs":round(time.time()-t),"usage":d.get("usage",{}).get("output_tokens"),"file":fn}
    except urllib.error.HTTPError as e:
        return {"scene":s,"model":m,"error":e.read().decode()[:300]}
    except Exception as e:
        return {"scene":s,"model":m,"error":str(e)[:300]}
with cf.ThreadPoolExecutor(4) as ex:
    res = list(ex.map(run, JOBS))
json.dump(res, open(f"{OUT}/results.json","w"), indent=1)
for r in res: print(r)
