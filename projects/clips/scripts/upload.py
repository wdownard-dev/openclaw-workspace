#!/usr/bin/env python3
"""Upload one video to the authorizing creator's own YouTube channel.

Usage:
  upload.py VIDEO --title "..." [--description "..."] [--tags a,b] [--privacy private|unlisted|public] [--yes]

Flow: refresh the OAuth access token -> show the channel and video details -> ask the owner to
approve -> resumable upload via the YouTube Data API (videos.insert) -> check processing status
(videos.list). Nothing is uploaded without approval (interactive prompt, or --yes when the
approval already happened out-of-band, e.g. via the Telegram preview).

Credentials come from the environment (GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET,
GOOGLE_OAUTH_REFRESH_TOKEN). Under the OpenClaw egress proxy these are sentinels replaced on the
wire, so no secret value is ever printed or handled in plaintext by this script.
Default privacy is "private".
"""
import argparse, json, mimetypes, os, sys, time, urllib.error, urllib.parse, urllib.request


def api(req, timeout=60):
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        sys.exit(f"HTTP {e.code} from {req.full_url.split('?')[0]}: {body}")


def access_token():
    # Built by hand: the credential values may be sentinels that must not be re-encoded.
    body = "&".join([
        "client_id=" + os.environ["GOOGLE_OAUTH_CLIENT_ID"],
        "client_secret=" + os.environ["GOOGLE_OAUTH_CLIENT_SECRET"],
        "refresh_token=" + os.environ["GOOGLE_OAUTH_REFRESH_TOKEN"],
        "grant_type=refresh_token",
    ]).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=body,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    _, _, raw = api(req)
    tok = json.loads(raw).get("access_token")
    if not tok:
        sys.exit("Could not refresh access token.")
    return tok


def get_json(url, token):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    return json.loads(api(req)[2])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--title", required=True)
    ap.add_argument("--description", default="")
    ap.add_argument("--tags", default="")
    ap.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    ap.add_argument("--yes", action="store_true", help="approval already given out-of-band")
    a = ap.parse_args()

    if not os.path.isfile(a.video):
        sys.exit(f"No such file: {a.video}")
    size = os.path.getsize(a.video)
    ctype = mimetypes.guess_type(a.video)[0] or "video/mp4"

    token = access_token()
    ch = get_json("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true", token)["items"][0]
    print(f"Channel: {ch['snippet']['title']} ({ch['id']})")
    print(f"Video:   {a.video} ({size/1e6:.1f} MB)\nTitle:   {a.title}\nPrivacy: {a.privacy}")

    if not a.yes:
        if input("Approve upload? [y/N] ").strip().lower() != "y":
            sys.exit("Not approved. Nothing uploaded.")

    meta = {
        "snippet": {"title": a.title[:100], "description": a.description,
                    "tags": [t.strip() for t in a.tags.split(",") if t.strip()]},
        "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False},
    }
    init = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=json.dumps(meta).encode(), method="POST",
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Length": str(size), "X-Upload-Content-Type": ctype})
    _, hdrs, _ = api(init)
    session = next(v for k, v in hdrs.items() if k.lower() == "location")

    with open(a.video, "rb") as f:
        data = f.read()
    put = urllib.request.Request(session, data=data, method="PUT",
                                 headers={"Content-Type": ctype, "Content-Length": str(size)})
    _, _, raw = api(put, timeout=600)
    vid = json.loads(raw)["id"]
    print(f"Uploaded. Video ID: {vid}  https://youtu.be/{vid}")

    for _ in range(12):
        st = get_json(f"https://www.googleapis.com/youtube/v3/videos?part=status,processingDetails&id={vid}", token)
        item = st["items"][0]
        print("upload:", item["status"].get("uploadStatus"), "| privacy:", item["status"].get("privacyStatus"),
              "| processing:", item.get("processingDetails", {}).get("processingStatus"))
        if item["status"].get("uploadStatus") in ("processed", "failed", "rejected"):
            break
        time.sleep(5)


if __name__ == "__main__":
    main()
