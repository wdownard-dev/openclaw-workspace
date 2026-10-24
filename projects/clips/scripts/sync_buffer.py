#!/usr/bin/env python3
"""Snapshot Buffer status, live link and metrics for every post in buffer-posts.json (needs BUFFER_API_KEY).

Usage:
  sync_buffer.py            append a snapshot to buffer-snapshots.csv, print one line per post
  sync_buffer.py --report   print the same table without writing

buffer-posts.json maps "<clip_id>-<platform>" -> Buffer post id. Add an entry whenever a post is created.
Prints NOTICE lines for status changes (scheduled->sent, error) and when a live link first appears.
"""
import csv, json, os, sys, urllib.error, urllib.request
from datetime import datetime, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
POSTS, SNAP, STATE = f"{ROOT}/buffer-posts.json", f"{ROOT}/buffer-snapshots.csv", f"{ROOT}/buffer-state.json"
METRICS = ["views", "reach", "reactions", "comments", "shares", "totalTimeWatched", "averageTimeWatched", "engagementRate"]
FIELDS = ["ts_utc", "key", "post_id", "status", "sent_at", "link", "error"] + METRICS


def gql(q):
    req = urllib.request.Request("https://api.buffer.com", data=json.dumps({"query": q}).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + os.environ["BUFFER_API_KEY"]})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:200]}")


def main():
    posts = json.load(open(POSTS))
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = []
    for key, pid in posts.items():
        d = gql('{ post(input:{id:"%s"}){ status sentAt externalLink error { message } metrics { type value } } }' % pid)
        p = (d.get("data") or {}).get("post")
        if not p:
            print(f"{key}: lookup failed {json.dumps(d)[:150]}")
            continue
        m = {x["type"]: x["value"] for x in p.get("metrics") or []}
        row = {"ts_utc": now, "key": key, "post_id": pid, "status": p["status"], "sent_at": p.get("sentAt") or "",
               "link": p.get("externalLink") or "", "error": (p.get("error") or {}).get("message", "")}
        row.update({k: m.get(k, "") for k in METRICS})
        rows.append(row)
        old = state.get(key, {})
        if row["status"] != old.get("status"):
            print(f"NOTICE {key}: status {old.get('status', '-')} -> {row['status']}")
        if row["link"] and not old.get("link"):
            print(f"NOTICE {key}: live link {row['link']}")
        if row["error"] and row["error"] != old.get("error"):
            print(f"NOTICE {key}: ERROR {row['error']}")
        state[key] = {"status": row["status"], "link": row["link"], "error": row["error"]}
    for r in rows:
        print(f"{r['key']:20} {r['status']:10} views={r['views']} reach={r['reach']} likes={r['reactions']} "
              f"comments={r['comments']} shares={r['shares']} {r['link']}")
    if "--report" in sys.argv:
        return
    new = not os.path.exists(SNAP)
    with open(SNAP, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerows(rows)
    json.dump(state, open(STATE, "w"), indent=1)


if __name__ == "__main__":
    main()
