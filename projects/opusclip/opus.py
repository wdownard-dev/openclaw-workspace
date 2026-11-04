#!/usr/bin/env python3
"""Thin OpusClip API helper for the wrdclipz pipeline.

Key comes from OPUSCLIP_API_KEY (injected by the OpenClaw secrets store).
Nothing is posted unless `post` or `schedule` is run with --yes.

  opus.py accounts
  opus.py submit URL [--min 15] [--max 60] [--keywords a,b] [--ratio portrait]
  opus.py status PROJECT_ID
  opus.py clips PROJECT_ID
  opus.py post PROJECT_ID CLIP_ID --account ID --title T --desc D [--yes]
  opus.py schedule PROJECT_ID CLIP_ID --account ID --title T --desc D --at ISO_UTC [--yes]
  opus.py cancel SCHEDULE_ID --yes
"""
import argparse, json, os, sys, urllib.request, urllib.error

BASE = "https://api.opus.pro"


def call(method, path, body=None):
    key = os.environ.get("OPUSCLIP_API_KEY")
    if not key:
        sys.exit("OPUSCLIP_API_KEY not set")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    org = os.environ.get("OPUS_ORG_ID")
    if org:
        headers["x-opus-org-id"] = org
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:500]}")


def bare(clip_id):
    # exportable-clips returns {projectId}.{clipId}; posting wants the part after the dot
    return clip_id.split(".", 1)[-1]


def post_body(a, with_time):
    body = {
        "projectId": a.project,
        "clipId": bare(a.clip),
        "postAccountId": a.account,
        "postDetail": {
            "title": a.title,
            "mediaType": "video",
            "custom": {"description": a.desc, "privacy": a.privacy},
        },
    }
    if with_time:
        body["publishAt"] = a.at
    return body


def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    s.add_parser("accounts")
    sub = s.add_parser("submit")
    sub.add_argument("url")
    sub.add_argument("--min", type=int, default=15)
    sub.add_argument("--max", type=int, default=60)
    sub.add_argument("--keywords", default="")
    sub.add_argument("--ratio", default="portrait")
    c = s.add_parser("clips")
    c.add_argument("project")
    st = s.add_parser("status")
    st.add_argument("project")
    for name in ("post", "schedule"):
        x = s.add_parser(name)
        x.add_argument("project")
        x.add_argument("clip")
        x.add_argument("--account", required=True)
        x.add_argument("--title", required=True)
        x.add_argument("--desc", default="")
        x.add_argument("--privacy", default="public")
        x.add_argument("--yes", action="store_true")
        if name == "schedule":
            x.add_argument("--at", required=True)
    cx = s.add_parser("cancel")
    cx.add_argument("schedule_id")
    cx.add_argument("--yes", action="store_true")
    a = p.parse_args()

    if a.cmd == "accounts":
        for acc in call("GET", "/api/social-accounts?q=mine")["data"]:
            print(acc["platform"], acc["extUserName"], acc["postAccountId"])
    elif a.cmd == "submit":
        pref = {"clipDurations": [[a.min, a.max]], "genre": "Auto"}
        if a.keywords:
            pref["topicKeywords"] = a.keywords.split(",")
        body = {"videoUrl": a.url, "curationPref": pref,
                "renderPref": {"layoutAspectRatio": a.ratio}}
        print(json.dumps(call("POST", "/api/clip-projects", body), indent=2))
    elif a.cmd == "status":
        r = call("GET", f"/api/clip-projects/{a.project}")
        print(r.get("stage"), r.get("error") or "")
    elif a.cmd == "clips":
        res = call("GET", f"/api/exportable-clips?q=findByProjectId&projectId={a.project}")
        for cl in (res if isinstance(res, list) else res.get("data", [])):
            scores = {k: v for k, v in cl.items()
                      if any(t in k.lower() for t in ("score", "viral", "rating")) and not isinstance(v, (dict, list))}
            print(cl["id"], round(cl["durationMs"] / 1000), "s |", cl.get("title"), "|", scores or "no score field")
    elif a.cmd in ("post", "schedule"):
        sched = a.cmd == "schedule"
        body = post_body(a, sched)
        if not a.yes:
            print("DRY RUN (add --yes to send):")
            print(json.dumps(body, indent=2))
            return
        path = "/api/publish-schedules" if sched else "/api/post-tasks"
        print(json.dumps(call("POST", path, body), indent=2))
    elif a.cmd == "cancel":
        if not a.yes:
            sys.exit("add --yes to cancel")
        print(json.dumps(call("DELETE", f"/api/publish-schedules/{a.schedule_id}"), indent=2))


if __name__ == "__main__":
    main()
