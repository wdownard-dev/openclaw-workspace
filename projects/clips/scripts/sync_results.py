#!/usr/bin/env python3
"""Snapshot public YouTube stats for every clip in results.csv (needs YOUTUBE_API_KEY).

Usage:
  sync_results.py            take a snapshot (appends to results-snapshots.csv), print alerts
  sync_results.py --report   print a table: views now, change since ~24h ago, % of 5,000 threshold

Only PUBLIC videos are visible to the key; private/scheduled ones show as 'not public'.
Never writes results.csv (other jobs edit it); results-snapshots.csv is the time series Editor learns from.
State for one-time alerts: results-alerts.json. Threshold per post is THRESHOLD views (Vyro campaign rule).
"""
import csv, json, os, re, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RESULTS, SNAP, ALERTS = f"{ROOT}/results.csv", f"{ROOT}/results-snapshots.csv", f"{ROOT}/results-alerts.json"
THRESHOLD = 5000
FIELDS = ["ts_utc", "clip_id", "views", "likes", "comments", "privacy", "age_h"]


def clips():
    out = []
    for r in csv.DictReader(open(RESULTS, encoding="utf-8")):
        m = re.search(r"shorts/([A-Za-z0-9_-]{11})", r.get("post_url", ""))
        if m:
            out.append((r["clip_id"], m.group(1), r.get("hook", "")))
    return out


def fetch(ids):
    url = ("https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,status&id=" + ",".join(ids)
           + "&key=" + os.environ["YOUTUBE_API_KEY"])
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return {i["id"]: i for i in json.loads(r.read()).get("items", [])}
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:200]}")


def read_snaps():
    return list(csv.DictReader(open(SNAP))) if os.path.exists(SNAP) else []


def main():
    cl = clips()
    if not cl:
        print("no clips with a post_url in results.csv")
        return
    items = fetch([v for _, v, _ in cl])
    now = datetime.now(timezone.utc)
    snaps = read_snaps()

    if "--report" in sys.argv:
        print(f"{'clip':8} {'views':>7} {'+24h':>6} {'% of 5k':>8}  status / hook")
        for cid, vid, hook in cl:
            it = items.get(vid)
            if not it:
                print(f"{cid:8} {'-':>7} {'-':>6} {'-':>8}  not public yet  | {hook}")
                continue
            views = int(it["statistics"].get("viewCount", 0))
            prev = [s for s in snaps if s["clip_id"] == cid and s["views"] != ""]
            old = None
            for s in prev:
                age = (now - datetime.fromisoformat(s["ts_utc"])).total_seconds() / 3600
                if age >= 20:
                    old = int(s["views"])
            delta = f"{views - old:+d}" if old is not None else "n/a"
            print(f"{cid:8} {views:>7} {delta:>6} {views / THRESHOLD * 100:>7.0f}%  public, {it['statistics'].get('likeCount', '?')} likes, "
                  f"{it['statistics'].get('commentCount', '?')} comments | {hook}")
        return

    new_file = not os.path.exists(SNAP)
    alerts = json.load(open(ALERTS)) if os.path.exists(ALERTS) else {}
    crossed = []
    with open(SNAP, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            w.writeheader()
        for cid, vid, hook in cl:
            it = items.get(vid)
            if not it:
                w.writerow({"ts_utc": now.isoformat(timespec="seconds"), "clip_id": cid, "views": "", "likes": "",
                            "comments": "", "privacy": "not public", "age_h": ""})
                continue
            st = it["statistics"]
            age = (now - datetime.fromisoformat(it["snippet"]["publishedAt"].replace("Z", "+00:00"))).total_seconds() / 3600
            views = int(st.get("viewCount", 0))
            w.writerow({"ts_utc": now.isoformat(timespec="seconds"), "clip_id": cid, "views": views,
                        "likes": st.get("likeCount", ""), "comments": st.get("commentCount", ""),
                        "privacy": it["status"]["privacyStatus"], "age_h": round(age, 1)})
            if views >= THRESHOLD and not alerts.get(cid):
                alerts[cid] = now.isoformat(timespec="seconds")
                crossed.append((cid, views, hook))
    json.dump(alerts, open(ALERTS, "w"), indent=1)
    live = sum(1 for _, v, _ in cl if v in items)
    print(f"snapshot ok: {live}/{len(cl)} clips public")
    for cid, views, hook in crossed:
        print(f"CROSSED 5,000: {cid} ({views} views) {hook}")
    if not crossed:
        print("no new threshold crossings")


if __name__ == "__main__":
    main()
