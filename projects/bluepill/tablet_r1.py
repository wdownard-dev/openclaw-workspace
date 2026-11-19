import os, json, base64, urllib.request, concurrent.futures as cf
KEY=os.environ["OPENAI_API_KEY"]
BASE=" Flat vector-style channel avatar icon, bold simple shapes, strong silhouette, tablet centred with generous margin on a solid flat background, readable at 98 pixels, clean thick dark outlines, limited palette. The only text is the two capital letters 'ML', spelled exactly, no other letters, no watermark."
C={
"a_navy_gold":"A carved arched stone tablet in warm sandstone beige, the large bold serif capital letters 'ML' carved deeply at the top in gold, below them three short rows of gold tally marks, a small gold laurel sprig under the letters, on a deep midnight navy background.",
"b_terracotta":"A carved arched limestone tablet in cream, the large bold serif capital letters 'ML' carved at the top in black, below them rows of black tally marks with a meander pattern border along the tablet edge, on a warm orange terracotta background.",
"c_oxblood":"A carved arched stone tablet in pale sandstone, a gold laurel wreath at the top with the capital letters 'ML' inside the wreath, below it two rows of tally marks in deep red, on a rich oxblood burgundy background.",
"d_teal_coral":"A carved arched stone tablet in light cream, the large bold capital letters 'ML' carved at the top in coral orange, below them rows of coral tally marks, on a deep teal turquoise background.",
"e_purple_gold":"A dark charcoal slate arched tablet with glowing gold engraving: the large capital letters 'ML' at top, rows of gold tally marks below and a small laurel sprig, on a deep royal purple background.",
"f_cream_black":"A dark charcoal stone arched tablet with the large capital letters 'ML' carved in cream at the top, rows of cream tally marks below with a tiny gold laurel sprig, on a warm cream parchment background with a thin gold ring border.",
}
def run(k):
    body=json.dumps({"model":"gpt-image-2.6-sunburst","size":"1024x1024","quality":"medium","n":1,"prompt":C[k]+BASE}).encode()
    req=urllib.request.Request("https://api.openai.com/v1/images/generations",body,{"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
    try:
        d=json.load(urllib.request.urlopen(req,timeout=300)); open(f"brand/tablet_r1/{k}.png","wb").write(base64.b64decode(d["data"][0]["b64_json"])); return k,"ok"
    except Exception as e: return k,"ERR "+str(getattr(e,'read',lambda:b'')()[:200] or e)
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(run,C): print(*r)
