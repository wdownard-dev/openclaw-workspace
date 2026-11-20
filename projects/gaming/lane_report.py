#!/usr/bin/env python3
"""Views by lane for wrdgamingclipz. Reads lane_tracker.csv, pulls live stats via YouTube API, prints a table."""
import csv, json, os, urllib.request, datetime
D = os.path.dirname(os.path.abspath(__file__))
b = ("client_id=" + os.environ["GOOGLE_OAUTH_CLIENT_ID"] + "&client_secret=" + os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]
     + "&refresh_token=" + os.environ["GOOGLE_OAUTH_REFRESH_TOKEN_GAMING"] + "&grant_type=refresh_token").encode()
t = json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=b), timeout=30))["access_token"]
rows = list(csv.DictReader(open(D + "/out/lane_tracker.csv")))
ids = ",".join(r["video_id"] for r in rows)
r = json.load(urllib.request.urlopen(urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?part=statistics,status&id=" + ids, headers={"Authorization": "Bearer " + t}), timeout=60))
st = {v["id"]: v for v in r["items"]}
now = datetime.datetime.now(datetime.timezone.utc)
out = []
for x in rows:
    v = st.get(x["video_id"])
    if not v or v["status"]["privacyStatus"] != "public": continue
    views = int(v["statistics"].get("viewCount", 0)); likes = int(v["statistics"].get("likeCount", 0))
    age = (now - datetime.datetime.fromisoformat(x["posted_utc"]).replace(tzinfo=datetime.timezone.utc)).total_seconds() / 3600
    out.append((x["lane"], x["title"][:48], x["source_views_when_picked"] or "-", views, round(views / max(age, 1)), round(100 * likes / max(views, 1), 1), round(age)))
out.sort(key=lambda o: -o[4])
print("lane | title | source views | our views | views/h | like % | age h")
for o in out: print(" | ".join(map(str, o)))
for lane in ("moment", "guide"):
    L = [o for o in out if o[0] == lane]
    if L: print(f"{lane}: n={len(L)} median views/h={sorted(o[4] for o in L)[len(L)//2]}")
