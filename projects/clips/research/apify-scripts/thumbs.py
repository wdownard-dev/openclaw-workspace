import json, os, urllib.request
DATA = "/home/williamdownard/.openclaw/workspace/projects/clips/research/apify-data"
TH = os.path.join(DATA, "thumbs"); os.makedirs(TH, exist_ok=True)
rows = json.load(open(os.path.join(DATA, "combined_posts.json")))
SEL = ["royaldropp","streamermomente_","perfectclips_1","swagg","socialinfos","cloutopia",
       "trd_luvr13682","trd_uploads","campistanoaceptad0","ter1yaky","foxfamilyguy","clipsahoytvv"]
picked, seen = [], set()
for a in SEL:
    cands = [r for r in rows if r["author"] == a and r["bucket"] not in ("generic_cod_mw4_game","generic_unpacking_game","other") and r["cover_url"]]
    cands.sort(key=lambda r: -r["views"])
    for r in cands:
        if r["video_id"] in seen: continue
        seen.add(r["video_id"]); picked.append(r); break
ok = []
for r in picked:
    fn = os.path.join(TH, f'{r["author"]}_{r["video_id"]}.jpg')
    try:
        req = urllib.request.Request(r["cover_url"], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp, open(fn, "wb") as f: f.write(resp.read())
        ok.append((r["author"], r["video_id"], os.path.getsize(fn), r["url"]))
    except Exception as e:
        print("FAIL", r["author"], type(e).__name__, str(e)[:80])
for o in ok: print("OK", o[0], o[2], o[3])
json.dump([{"author":r["author"],"video_id":r["video_id"],"url":r["url"],"views":r["views"],"bucket":r["bucket"]} for r in picked],
          open(os.path.join(TH, "index.json"), "w"), indent=1)
print("saved", len(ok), "of", len(SEL))
