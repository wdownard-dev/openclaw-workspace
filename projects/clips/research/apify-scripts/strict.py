import csv, json, os
DATA = "/home/williamdownard/.openclaw/workspace/projects/clips/research/apify-data"
rows = json.load(open(os.path.join(DATA, "combined_posts.json")))
STRICT = {
  "mw4": ["mrbeast", "mw4partner"],
  "tdr": ["total drama", "totaldrama", "totalrobloxdrama", "#trd", " trd", "tdi"],
  "ff": ["family guy", "familyguy", "hulupartner"],
  "hs": ["hardscope", "unpacked"],
}
def bucket(r):
    t = (r["caption"] + " " + r["hashtags"]).lower()
    if any(k in t for k in STRICT["mw4"]): return "mrbeast_mw4"
    if any(k in t for k in STRICT["tdr"]): return "total_drama_roblox"
    if any(k in t for k in STRICT["ff"]) and ("hell" in t or "halloween" in t or "hulupartner" in t): return "family_guy_hell"
    if any(k in t for k in STRICT["hs"]): return "unpacked_hardscope"
    if r["query_or_tag"] and r["query_or_tag"].lower().startswith("mw4"): return "generic_cod_mw4_game"
    if r["query_or_tag"] and r["query_or_tag"].lower().startswith("unpacked"): return "generic_unpacking_game"
    return "other"
for r in rows: r["bucket"] = bucket(r)
from collections import Counter
print(Counter(r["bucket"] for r in rows))
for b in ["mrbeast_mw4","total_drama_roblox","family_guy_hell","unpacked_hardscope"]:
    sub = sorted([r for r in rows if r["bucket"]==b], key=lambda r:-r["views"])
    print(f"\n== {b}: {len(sub)} posts; median views {sorted(r['views'] for r in sub)[len(sub)//2] if sub else 0}")
    for r in sub[:8]:
        print(r["views"], r["likes"], r["comments"], r["shares"], r["saves"], "|", r["author"], r["author_followers"], "|", r["duration_s"], f'{r["width"]}x{r["height"]}', "|", r["posted_utc"][:10], "|", r["url"].split('/video/')[1][:8] if r["url"] else "")
        print("    ", r["caption"][:140], "|", r["hashtags"][:100])
# save with bucket
import csv
with open(os.path.join(DATA, "combined_posts.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(rows, open(os.path.join(DATA, "combined_posts.json"), "w"), ensure_ascii=False, indent=1)
