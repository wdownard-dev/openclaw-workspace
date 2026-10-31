import json, os, statistics as st
DATA = "/home/williamdownard/.openclaw/workspace/projects/clips/research/apify-data"
rows = json.load(open(os.path.join(DATA, "combined_posts.json")))
seen = {}
for r in rows:
    seen.setdefault(r["video_id"], r)  # dedupe across hashtag/search
uniq = list(seen.values())
camp = [r for r in uniq if r["bucket"] in ("mrbeast_mw4","total_drama_roblox","family_guy_hell","unpacked_hardscope")]
print("unique posts", len(uniq), "campaign-matched unique", len(camp))
def summ(name, sub):
    if not sub: print(name, "none"); return
    fol = [r["author_followers"] or 0 for r in sub]
    dur = [r["duration_s"] or 0 for r in sub]
    eng = [((r["likes"]+r["comments"]+r["shares"]+r["saves"])/r["views"]) for r in sub if r["views"]>0]
    print(f'{name}: n={len(sub)} median_views={int(st.median([r["views"] for r in sub]))} '
          f'median_followers={int(st.median(fol))} share<1k_followers={sum(f<1000 for f in fol)/len(fol):.0%} '
          f'median_dur_s={st.median(dur):.0f} share_dur_<=30s={sum(d<=30 for d in dur)/len(dur):.0%} '
          f'median_engagement={st.median(eng):.2%} share_original_sound={sum(bool(r["music_original"]) for r in sub)/len(sub):.0%} '
          f'share_ad_flag={sum(bool(r["is_ad"]) for r in sub)/len(sub):.0%} '
          f'share_portrait={sum((r["height"] or 0)>(r["width"] or 0) for r in sub)/len(sub):.0%}')
summ("ALL campaign-matched", camp)
for b in ["mrbeast_mw4","total_drama_roblox","family_guy_hell","unpacked_hardscope"]:
    summ(b, [r for r in camp if r["bucket"]==b])
top10 = sorted(camp, key=lambda r:-r["views"])[:10]
summ("TOP10 campaign-matched by views", top10)
small = [r for r in camp if (r["author_followers"] or 0) < 1000 and r["views"]>=5000]
print("small(<1k) & >=5k views:", len(small), [ (r["author"], r["views"]) for r in small])
print("top10 hashtags sample:"); [print("  ", r["author"], r["hashtags"][:110]) for r in top10]
print("campaign-tag usage in campaign-matched:", {t: sum(t in (r["hashtags"]+" "+r["caption"]).lower() for r in camp) for t in ["#mw4partner","#mw4 ","#paidpartnership","#hulupartner","#totaldramaroblox","#mrbeast","#familyguy","#halloween"]})
print("duration quartiles all campaign-matched:", [round(x) for x in st.quantiles([r["duration_s"] or 0 for r in camp], n=4)])
print("caption length median chars:", int(st.median([len(r["caption"]) for r in camp])))
print("share with 3+ hashtags:", f'{sum(len(r["hashtags"].split())>=3 for r in camp)/len(camp):.0%}')
print("share posted in last 14 days (since 2026-10-16):", f'{sum((r["posted_utc"] or "")>="2026-10-16" for r in camp)/len(camp):.0%}')
json.dump(camp, open(os.path.join(DATA, "campaign_matched_unique.json"), "w"), ensure_ascii=False, indent=1)
