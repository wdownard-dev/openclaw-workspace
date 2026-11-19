#!/usr/bin/env python3
"""Upload a video to wrdgamingclipz (NOT wrdclipz, NOT The Myth Ledger). Always sets privacyStatus explicitly.

Usage: yt_upload_gaming.py FILE --title T [--desc D | --desc-file F] [--privacy private|unlisted|public]
                       [--thumb IMAGE] [--tags a,b] [--category 20]
Default privacy is private. Needs GOOGLE_OAUTH_CLIENT_ID/SECRET and GOOGLE_OAUTH_REFRESH_TOKEN_GAMING
in the environment (protected store). Prints the video id and Studio URL.
The granted scopes cannot delete videos; delete in Studio.
"""
import argparse, json, os, sys, urllib.error, urllib.request

p = argparse.ArgumentParser()
p.add_argument("file")
p.add_argument("--title", required=True)
p.add_argument("--desc", default="")
p.add_argument("--desc-file")
p.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
p.add_argument("--thumb")
p.add_argument("--tags", default="")
p.add_argument("--category", default="20")  # 20 = Gaming
p.add_argument("--publish-at", help="ISO 8601 time to go public; requires private (YouTube status.publishAt)")
a = p.parse_args()

for k in ("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_OAUTH_REFRESH_TOKEN_GAMING"):
    if k not in os.environ:
        sys.exit("MISSING ENV " + k)

def http(req, timeout=300):
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:600]}")

body = ("client_id=" + os.environ["GOOGLE_OAUTH_CLIENT_ID"]
        + "&client_secret=" + os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]
        + "&refresh_token=" + os.environ["GOOGLE_OAUTH_REFRESH_TOKEN_GAMING"]
        + "&grant_type=refresh_token").encode()
tok = json.load(http(urllib.request.Request("https://oauth2.googleapis.com/token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"}), 30))["access_token"]
auth = {"Authorization": "Bearer " + tok}

# Confirm we are on the right channel before uploading anything.
ch = json.load(http(urllib.request.Request(
    "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true", headers=auth), 30))["items"][0]
if ch["id"] != "UCIbJfNm2nJKUCItsO0XGhiw":
    sys.exit("WRONG CHANNEL: " + ch["snippet"]["title"])

desc = open(a.desc_file).read() if a.desc_file else a.desc
meta = {"snippet": {"title": a.title, "description": desc, "categoryId": a.category,
                    "tags": [t for t in a.tags.split(",") if t]},
        "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False}}
if a.publish_at:
    if a.privacy != "private":
        sys.exit("--publish-at requires --privacy private")
    import datetime
    t = datetime.datetime.fromisoformat(a.publish_at.replace("Z", "+00:00"))
    if t.tzinfo is None:
        sys.exit("--publish-at needs a timezone offset, e.g. 2026-11-18T09:00:00-05:00")
    meta["status"]["publishAt"] = t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
size = os.path.getsize(a.file)
init = urllib.request.Request(
    "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
    data=json.dumps(meta).encode(), method="POST",
    headers={**auth, "Content-Type": "application/json; charset=UTF-8",
             "X-Upload-Content-Length": str(size), "X-Upload-Content-Type": "video/mp4"})
loc = http(init, 60).headers["Location"]
with open(a.file, "rb") as f:
    put = urllib.request.Request(loc, data=f.read(), method="PUT",
                                 headers={**auth, "Content-Type": "video/mp4", "Content-Length": str(size)})
res = json.load(http(put, 900))
vid = res["id"]
print("video id:", vid, "| privacy:", res["status"]["privacyStatus"], "| uploadStatus:", res["status"].get("uploadStatus"))
print("Studio: https://studio.youtube.com/video/%s/edit" % vid)

if a.thumb:
    ct = "image/png" if a.thumb.lower().endswith(".png") else "image/jpeg"
    t = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=" + vid,
        data=open(a.thumb, "rb").read(), method="POST", headers={**auth, "Content-Type": ct})
    print("thumbnail set:", bool(http(t, 120).read()))
