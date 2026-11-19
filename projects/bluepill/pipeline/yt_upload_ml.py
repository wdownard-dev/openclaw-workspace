#!/usr/bin/env python3
"""Upload a video to The Myth Ledger (NOT wrdclipz). Always sets privacyStatus explicitly.

Usage: yt_upload_ml.py FILE --title T [--desc D | --desc-file F] [--privacy private|unlisted|public]
                       [--thumb IMAGE] [--tags a,b] [--category 27]
Default privacy is private. Needs GOOGLE_OAUTH_CLIENT_ID/SECRET and GOOGLE_OAUTH_REFRESH_TOKEN_MYTHLEDGER
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
p.add_argument("--category", default="27")  # 27 = Education
a = p.parse_args()

for k in ("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_OAUTH_REFRESH_TOKEN_MYTHLEDGER"):
    if k not in os.environ:
        sys.exit("MISSING ENV " + k)

def http(req, timeout=300):
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:600]}")

body = ("client_id=" + os.environ["GOOGLE_OAUTH_CLIENT_ID"]
        + "&client_secret=" + os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]
        + "&refresh_token=" + os.environ["GOOGLE_OAUTH_REFRESH_TOKEN_MYTHLEDGER"]
        + "&grant_type=refresh_token").encode()
tok = json.load(http(urllib.request.Request("https://oauth2.googleapis.com/token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"}), 30))["access_token"]
auth = {"Authorization": "Bearer " + tok}

# Confirm we are on the right channel before uploading anything.
ch = json.load(http(urllib.request.Request(
    "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true", headers=auth), 30))["items"][0]
if ch["id"] != "UCNSflpCKmwHr4bLpNTCbBqQ":
    sys.exit("WRONG CHANNEL: " + ch["snippet"]["title"])

desc = open(a.desc_file).read() if a.desc_file else a.desc
meta = {"snippet": {"title": a.title, "description": desc, "categoryId": a.category,
                    "tags": [t for t in a.tags.split(",") if t]},
        "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False}}
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
