import csv, json, os
DATA = "/home/williamdownard/.openclaw/workspace/projects/clips/research/apify-data"
CAMPAIGN_TERMS = {
  "totaldramaroblox": ["total drama", "totaldrama", "trd", "roblox"],
  "mw4": ["mrbeast", "mw4", "mw4partner", "dmz"],
  "mw4partner": ["mrbeast", "mw4", "mw4partner", "dmz"],
  "familyguy": ["family guy", "familyguy", "hell", "halloween", "hulupartner"],
  "unpacked": ["unpack", "hardscope"],
}
def flat(x, source, label):
    vm = x.get("videoMeta") or {}; am = x.get("authorMeta") or {}; mm = x.get("musicMeta") or {}
    tags = [h.get("name") if isinstance(h, dict) else h for h in (x.get("hashtags") or [])]
    return {
        "source": source, "query_or_tag": label, "video_id": x.get("id"),
        "author": am.get("name"), "author_followers": am.get("fans"),
        "author_verified": am.get("verified"), "author_videos": am.get("video"),
        "url": x.get("webVideoUrl"), "posted_utc": x.get("createTimeISO"),
        "duration_s": vm.get("duration"), "width": vm.get("width"), "height": vm.get("height"),
        "views": x.get("playCount") or 0, "likes": x.get("diggCount") or 0,
        "comments": x.get("commentCount") or 0, "shares": x.get("shareCount") or 0,
        "saves": x.get("collectCount") or 0,
        "caption": (x.get("text") or "").replace("\n", " ").strip(),
        "hashtags": " ".join("#" + t for t in tags if t),
        "music_name": mm.get("musicName"), "music_original": mm.get("musicOriginal"),
        "is_ad": x.get("isAd"), "is_sponsored": x.get("isSponsored"),
        "is_slideshow": x.get("isSlideshow"), "cover_url": vm.get("coverUrl") or vm.get("originalCoverUrl"),
        "language": x.get("textLanguage"), "subtitles_available": bool(vm.get("subtitleLinks")),
    }
rows = []
for x in json.load(open(os.path.join(DATA, "hashtag_raw_items.json"))):
    tag = x.get("searchHashtag", {}).get("name") if isinstance(x.get("searchHashtag"), dict) else x.get("searchHashtag")
    rows.append(flat(x, "hashtag", tag))
for x in json.load(open(os.path.join(DATA, "search_raw_items.json"))):
    rows.append(flat(x, "search", x.get("searchQuery")))
# on-campaign flag: caption/hashtags mention the campaign terms for the tag/query
def on_campaign(r):
    key = (r["query_or_tag"] or "").lower()
    text = (r["caption"] + " " + r["hashtags"]).lower()
    if "unpacked" in key or "hardscope" in key: terms = CAMPAIGN_TERMS["unpacked"]
    elif "roblox" in key or "total" in key: terms = CAMPAIGN_TERMS["totaldramaroblox"]
    elif "mrbeast" in key or "mw4" in key: terms = CAMPAIGN_TERMS["mw4"]
    elif "family" in key or "hell" in key: terms = CAMPAIGN_TERMS["familyguy"]
    else: return False
    return any(t in text for t in terms)
for r in rows: r["campaign_term_match"] = on_campaign(r)
rows.sort(key=lambda r: -r["views"])
fields = list(rows[0].keys())
with open(os.path.join(DATA, "combined_posts.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
json.dump(rows, open(os.path.join(DATA, "combined_posts.json"), "w"), ensure_ascii=False, indent=1)
print("rows", len(rows), "campaign-term matches", sum(r["campaign_term_match"] for r in rows))
print("\nSMALL ACCOUNTS (<1k followers) with >=5k views:")
for r in rows:
    if (r["author_followers"] or 0) < 1000 and r["views"] >= 5000:
        print(r["views"], r["author_followers"], r["author"], r["query_or_tag"], r["duration_s"], r["url"])
print("\nTOP 12 CAMPAIGN-MATCHED BY VIEWS:")
for r in [r for r in rows if r["campaign_term_match"]][:12]:
    print(r["views"], r["likes"], r["comments"], r["shares"], r["saves"], "|", r["author"], r["author_followers"], "|", r["duration_s"], f'{r["width"]}x{r["height"]}', "|", r["query_or_tag"], "|", r["posted_utc"][:10], "|", r["url"])
    print("    ", r["caption"][:150], "|", r["hashtags"][:90])
print("\nTOP 10 OVERALL (no campaign filter):")
for r in rows[:10]:
    print(r["views"], r["author"], r["author_followers"], r["query_or_tag"], r["campaign_term_match"])
