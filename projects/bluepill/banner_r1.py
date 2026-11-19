import os, json, base64, urllib.request, concurrent.futures as cf
KEY=os.environ["OPENAI_API_KEY"]
BASE=" Wide flat vector banner, bold simple shapes, thick dark outlines, limited palette of warm orange terracotta, cream and black with small gold accents, in the style of Greek black-figure pottery. Layout: the middle 60 percent of the width is calm and uncluttered holding the text; all decoration sits in the left and right outer fifths and along thin top and bottom Greek-key meander borders. The only text is exactly 'THE MYTH LEDGER' in large bold serif capitals centred, and beneath it, smaller, 'Every myth, accounted for.' No other text, no watermark."
C={
"1":"Centred cream stone tablet shape behind the title with the title carved in black, flanked at the far left and right by black silhouette amphora vases and laurel sprigs, orange terracotta background.",
"2":"Orange terracotta background with the title in cream on a dark charcoal band, black silhouette figures in pottery style at the far left (a hero with spear) and far right (a column and laurel), tally marks scattered subtly.",
"3":"Orange terracotta background, the title in black serif capitals with a thin gold underline, at far left and right tall stacks of tally-mark tablets and laurel wreaths, Greek-key borders top and bottom.",
}
def run(k):
    body=json.dumps({"model":"gpt-image-2.6-sunburst","size":"1536x1024","quality":"medium","n":1,"prompt":C[k]+BASE}).encode()
    req=urllib.request.Request("https://api.openai.com/v1/images/generations",body,{"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
    try:
        d=json.load(urllib.request.urlopen(req,timeout=300)); open(f"brand/banner_r1/{k}.png","wb").write(base64.b64decode(d["data"][0]["b64_json"])); return k,"ok"
    except Exception as e: return k,"ERR "+str(getattr(e,'read',lambda:b'')()[:200] or e)
with cf.ThreadPoolExecutor(3) as ex:
    for r in ex.map(run,C): print(*r)
