import os, json, base64, urllib.request, concurrent.futures as cf
KEY=os.environ["OPENAI_API_KEY"]
P=("Wide flat vector banner in the style of Greek black-figure pottery, thick dark outlines, limited palette of warm orange terracotta, cream, black and small gold accents. "
"Orange terracotta background. Dead centre, a horizontal dark charcoal band with thin gold lines top and bottom holding the title 'THE MYTH LEDGER' in bold cream serif capitals, with the smaller italic cream tagline 'Every myth, accounted for.' beneath it. "
"STRICT LAYOUT: the dark band and all text together occupy only the middle 48 percent of the image width, perfectly centred, with a wide empty terracotta gap on both sides of the band. "
"At the far left edge, a black silhouette hoplite warrior with crested helmet and spear, standing on a thin black ground line, fully inside the left 22 percent of the image and not touching the band. "
"At the far right edge, a black silhouette Greek column with a gold laurel sprig, fully inside the right 22 percent of the image and not touching the band. "
"A few small tally-mark groups scattered subtly in the gaps. No other text, no watermark.")
def run(k):
    body=json.dumps({"model":"gpt-image-2.6-sunburst","size":"1536x1024","quality":"medium","n":1,"prompt":P}).encode()
    req=urllib.request.Request("https://api.openai.com/v1/images/generations",body,{"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
    try:
        d=json.load(urllib.request.urlopen(req,timeout=300)); open(f"brand/banner_r2/{k}.png","wb").write(base64.b64decode(d["data"][0]["b64_json"])); return k,"ok"
    except Exception as e: return k,"ERR "+str(getattr(e,'read',lambda:b'')()[:200] or e)
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(run,["a","b","c","d"]): print(*r)
