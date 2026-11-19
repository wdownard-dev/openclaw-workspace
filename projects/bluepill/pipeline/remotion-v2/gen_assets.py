import os, json, base64, time, urllib.request, concurrent.futures as cf
KEY=os.environ["OPENAI_API_KEY"]; OUT="tests/v2/gen"
STYLE=("Flat-shaded illustrated concept art for a 2D animated history explainer: simplified shapes, soft painterly gradients, "
 "limited muted palette with one warm accent, subtle paper texture, clean readable composition, wide 3:2 frame, no people, no characters, no text, no letters, no logos.")
JOBS={
 "island_dusk":"a green rocky Greek island hillside at dusk with a dirt path winding up to a large dark cave mouth, flock of white sheep dots on the grass, calm sea and low orange sun in the distance, empty foreground path so characters can stand there. "+STYLE,
 "sea_sunrise":"open calm sea at sunrise, warm pink and gold sky, low sun on horizon, gentle waves with white foam, a small rocky island cliff far on the right, large empty water area in the foreground, no ship. "+STYLE,
 "cave_mouth_dawn":"view from inside the Cyclops cave looking out at a large bright cave entrance at dawn, warm golden sunrise light spilling onto a dusty cave floor, dark rocky walls framing the arch, sea and hills visible outside, empty floor foreground. "+STYLE,
}
PROPS=("Prop sprite sheet on a perfectly plain flat off-white background, 3 columns by 2 rows, generous spacing, each prop fully separate, no overlap, thick dark outline, flat colours, simple cartoon style matching a minimal round-head cartoon cast. "
 "Row 1: a fluffy white sheep seen from the side, a red clay wine cup with gold rim, a long sharpened wooden stake with glowing hot tip. "
 "Row 2: a round grey stone boulder, an ancient Greek wooden sailing ship seen from the side with cream sail and red trim, a clay wine amphora. No text, no characters.")
def run(item):
    name,prompt=item
    body=json.dumps({"model":"gpt-image-2.6-sunburst","size":"1536x1024","quality":"medium","n":1,"prompt":prompt}).encode()
    req=urllib.request.Request("https://api.openai.com/v1/images/generations",body,{"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
    t=time.time()
    try:
        d=json.load(urllib.request.urlopen(req,timeout=300))
        open(f"{OUT}/{name}.png","wb").write(base64.b64decode(d["data"][0]["b64_json"]))
        return name,round(time.time()-t),d.get("usage",{}).get("output_tokens")
    except Exception as e:
        return name,"ERR",str(getattr(e,'read',lambda:e)())[:300]
items=list(JOBS.items())+[("props_sheet",PROPS)]
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(run,items): print(r)
