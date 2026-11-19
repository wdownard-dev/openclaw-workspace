#!/usr/bin/env python3
"""Apply approved thumbnails to wrdgamingclipz videos (thumbnails.set). Channel-guarded.
Usage: apply_thumbs.py ID [ID ...]      reads out/thumbs/<ID>.png  (ID = YouTube video id)
Uploaded Shorts only; a thumbnail file named <ID>.png must exist. Needs the same env vars as yt_upload_gaming.py."""
import json, os, sys, urllib.error, urllib.request
D = os.path.dirname(os.path.abspath(__file__))
ids = sys.argv[1:]
if not ids: sys.exit(__doc__)
for k in ("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_OAUTH_REFRESH_TOKEN_GAMING"):
    if k not in os.environ: sys.exit("MISSING ENV " + k)
def http(req, timeout=120):
    try: return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e: sys.exit(f"HTTP {e.code}: {e.read().decode()[:600]}")
body = ("client_id=" + os.environ["GOOGLE_OAUTH_CLIENT_ID"] + "&client_secret=" + os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]
        + "&refresh_token=" + os.environ["GOOGLE_OAUTH_REFRESH_TOKEN_GAMING"] + "&grant_type=refresh_token").encode()
tok = json.load(http(urllib.request.Request("https://oauth2.googleapis.com/token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"}), 30))["access_token"]
auth = {"Authorization": "Bearer " + tok}
ch = json.load(http(urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true", headers=auth), 30))["items"][0]
if ch["id"] != "UCIbJfNm2nJKUCItsO0XGhiw": sys.exit("WRONG CHANNEL: " + ch["snippet"]["title"])
for vid in ids:
    p = f"{D}/out/thumbs/{vid}.png"
    if not os.path.exists(p): print("SKIP (no file):", vid); continue
    if os.path.getsize(p) > 2_000_000: print("SKIP (>2MB):", vid); continue
    req = urllib.request.Request(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
        data=open(p, "rb").read(), method="POST", headers={**auth, "Content-Type": "image/png"})
    r = json.load(http(req)); print("OK", vid, r.get("items", [{}])[0].get("default", {}).get("url", ""))
