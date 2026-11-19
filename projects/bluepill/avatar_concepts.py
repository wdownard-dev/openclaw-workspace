import os, json, base64, urllib.request, concurrent.futures as cf
KEY=os.environ["OPENAI_API_KEY"]
BASE=" Flat vector-style channel avatar icon, bold simple shapes, strong silhouette, centred with generous margin on a solid flat background, readable at 98 pixels, clean thick outlines, limited palette. No other text, no watermark."
C={
"01_monogram_seal":"A round gold seal medallion with the two capital letters 'ML' in an elegant serif, a thin laurel wreath around the edge, on a deep navy background.",
"02_open_ledger":"An open ancient ledger book seen from the front with cream pages and a small gold laurel wreath floating above it, deep navy background.",
"03_scroll_quill":"An unrolled papyrus scroll with a gold quill pen resting across it, tiny tally marks on the scroll, deep teal background.",
"04_column_book":"A single white Greek column capital standing on an open book, gold highlights, warm terracotta background.",
"05_m_columns":"A bold capital letter 'M' whose strokes are built from two Greek columns joined by an arch, cream and gold on a deep navy background.",
"06_wax_seal":"A red wax seal stamped with a laurel branch and a small lightning bolt, on a cream parchment-coloured background.",
"07_stone_tablet":"A carved stone tablet with rows of tally marks and a small laurel sprig at the top, gold and stone grey on deep green background.",
"08_vase_emblem":"A circular emblem in the style of Greek black-figure pottery: a black silhouette of a tall amphora vase with a meander pattern ring, on an orange terracotta background.",
}
def run(k):
    body=json.dumps({"model":"gpt-image-2.6-sunburst","size":"1024x1024","quality":"medium","n":1,"prompt":C[k]+BASE}).encode()
    req=urllib.request.Request("https://api.openai.com/v1/images/generations",body,{"Authorization":"Bearer "+KEY,"Content-Type":"application/json"})
    try:
        d=json.load(urllib.request.urlopen(req,timeout=300)); open(f"brand/avatars/{k}.png","wb").write(base64.b64decode(d["data"][0]["b64_json"])); return k,"ok"
    except Exception as e: return k,"ERR "+str(getattr(e,'read',lambda:b'')()[:200] or e)
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(run,C): print(*r)
