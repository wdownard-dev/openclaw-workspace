import csv, json, os
DATA = "/home/williamdownard/.openclaw/workspace/projects/clips/research/apify-data"
items = json.load(open(os.path.join(DATA, "hashtag_raw_items.json")))
rows, seen = [], {}
for x in items:
    vm = x.get("videoMeta") or {}
    am = x.get("authorMeta") or {}
    mm = x.get("musicMeta") or {}
    tags = [h.get("name") if isinstance(h, dict) else h for h in (x.get("hashtags") or [])]
    row = {
        "video_id": x.get("id"),
        "search_tag": x.get("searchHashtag", {}).get("name") if isinstance(x.get("searchHashtag"), dict) else x.get("searchHashtag"),
        "author": am.get("name"),
        "author_followers": am.get("fans"),
        "author_verified": am.get("verified"),
        "author_total_likes": am.get("heart"),
        "author_video_count": am.get("video"),
        "url": x.get("webVideoUrl"),
        "posted_utc": x.get("createTimeISO"),
        "duration_s": vm.get("duration"),
        "width": vm.get("width"), "height": vm.get("height"),
        "views": x.get("playCount"), "likes": x.get("diggCount"),
        "comments": x.get("commentCount"), "shares": x.get("shareCount"),
        "saves": x.get("collectCount"), "reposts": x.get("repostCount"),
        "caption": (x.get("text") or "").replace("\n", " "),
        "hashtags": " ".join("#" + t for t in tags if t),
        "music_name": mm.get("musicName"), "music_original": mm.get("musicOriginal"),
        "is_ad": x.get("isAd"), "is_sponsored": x.get("isSponsored"),
        "is_slideshow": x.get("isSlideshow"), "is_pinned": x.get("isPinned"),
        "cover_url": vm.get("coverUrl") or vm.get("originalCoverUrl"),
        "language": x.get("textLanguage"),
    }
    if row["video_id"] in seen:
        seen[row["video_id"]]["search_tag"] += "; " + str(row["search_tag"])
        continue
    seen[row["video_id"]] = row
    rows.append(row)
rows.sort(key=lambda r: -(r["views"] or 0))
with open(os.path.join(DATA, "hashtag_posts_flat.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(rows, open(os.path.join(DATA, "hashtag_posts_flat.json"), "w"), ensure_ascii=False, indent=1)
print("unique posts", len(rows), "dupes collapsed", len(items)-len(rows))
print("sample videoMeta keys:", sorted((items[0].get("videoMeta") or {}).keys()))
print("tag counts:", {t: sum(1 for r in rows if r["search_tag"] and t in r["search_tag"]) for t in ["unpacked","TotalDramaRoblox","MW4","MW4partner","FamilyGuy"]})
print("duplicates across tags:", len(items)-len(rows))
print()
print("TOP 15 BY VIEWS")
for r in rows[:15]:
    print(r["views"], r["likes"], r["comments"], r["shares"], r["saves"], "|", r["author"], r["author_followers"], "|", r["duration_s"], f'{r["width"]}x{r["height"]}', "|", r["search_tag"], "|", r["posted_utc"], "|", r["url"])
    print("   ", r["caption"][:160], "|", r["hashtags"][:120], "| music:", r["music_name"], "orig" if r["music_original"] else "")
