#!/usr/bin/env python3
"""Guardrails for automatic follow-ups on priority stories (William, 2026-11-06: "auto, but methodical").

The radar loop only detects. These commands keep the follow-up agent methodical and stop double posts:

  followup.py status                         active priority stories with spacing, daily posts and credits used
  followup.py can-post STORY [--urgent]      may we auto-post a follow-up for STORY right now? (JSON); --urgent skips the 3 h spacing
                                             (for a brand-new official briefing) but not the daily cap
  followup.py can-spend STORY CREDITS        may we auto-submit CREDITS to OpusClip for STORY? (JSON)
  followup.py record-post STORY CLIP_ID      count an auto follow-up post
  followup.py record-credits STORY CREDITS   count credits spent on STORY
  followup.py reject STORY CLIP_ID REASON    a clip failed screening; never offer it again
  followup.py exhausted STORY                no screenable banked clips left; stop BANKED_DUE prompts
  followup.py seen-add STORY VIDEO_ID        mark a video as already handled (for example the source we already clipped)
  followup.py pending-add PROJECT STORY      we submitted PROJECT to OpusClip for STORY; the loop will remind us to finish it
  followup.py pending-add-live VIDEO_ID STORY  an official stream is live for STORY; the loop will tell us when it ends
  followup.py pending-done ID                finished (posted, rejected or abandoned): stop the reminders
  followup.py pending-list                   open pending items
  followup.py log-post STORY CLIP_ID --title T --source S --score N --signal TEXT [--source-age-h H]
                                             append a news-lane row to experiment-log.csv (YouTube, posted now)

Rules (edit here to tune): at most 3 auto posts per story per 24 h, at least 3 h between posts, posting window 7 AM to
11 PM ET, at most 60 credits per story and 120 credits a day for automatic submissions. Anything outside these
limits goes to William instead of happening automatically.
"""
import csv, json, os, sys, time
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TRACK = os.environ.get("RADAR_TRACK_FILE", os.path.join(HERE, "radar_track.json"))
LOG = os.path.join(HERE, "experiment-log.csv")
ET = ZoneInfo("America/New_York")
MAX_POSTS_24H = 3
MIN_SPACING_H = 3
WINDOW = (7, 23)
STORY_CREDITS = 60
DAY_CREDITS = 120


def load():
    t = json.load(open(TRACK)) if os.path.exists(TRACK) else {"videos": {}, "priority": {}, "hot_alerted": {}}
    t.setdefault("credits_log", [])
    return t


def save(t):
    json.dump(t, open(TRACK, "w"), indent=1)


def find(t, story):
    ks = [k for k in t["priority"] if story.lower() in k.lower() or k.lower() in story.lower()]
    if not ks:
        sys.exit(json.dumps({"error": f"no active priority matches '{story}'", "active": list(t["priority"])}))
    return ks[0], t["priority"][ks[0]]


def project_last_post(project):
    """Latest post time (epoch) of any logged clip from this OpusClip project, so spacing survives renames and manual priorities."""
    best = 0
    if project and os.path.exists(LOG):
        for r in csv.DictReader(open(LOG)):
            if (r.get("clip_id") or "").startswith(project + ".") and (r.get("status") or "").startswith(("posted", "live")):
                try:
                    best = max(best, int(datetime.strptime(r["post_et"][:16], "%Y-%m-%d %H:%M").replace(tzinfo=ET).timestamp()))
                except ValueError:
                    pass
    return best


def last_post_ts(t, pr):
    v = t["videos"].get(pr.get("video_id", ""), {})
    return max([p[0] for p in pr.get("auto_posts", [])] + [v.get("ts", 0), project_last_post(pr.get("project", ""))])


def can_post(t, key, pr, urgent=False):
    now = time.time()
    h = datetime.now(ET).hour
    recent = [p for p in pr.get("auto_posts", []) if now - p[0] < 86400]
    if now > pr["expires"]:
        return False, "priority expired", None
    if not (WINDOW[0] <= h < WINDOW[1]):
        return False, f"outside the posting window ({WINDOW[0]} AM to {WINDOW[1] - 12} PM ET)", None
    if len(recent) >= MAX_POSTS_24H:
        return False, f"already {len(recent)} auto posts in 24 h (max {MAX_POSTS_24H})", None
    nxt = last_post_ts(t, pr) + MIN_SPACING_H * 3600
    if now < nxt and not urgent:
        return False, f"spacing: wait until {datetime.fromtimestamp(nxt, ET).strftime('%H:%M ET')}", nxt
    return True, "ok", None


def spent(t, key=None, window=None):
    now = time.time()
    return sum(n for ts, n, s in t["credits_log"] if (key is None or s == key) and (window is None or now - ts < window))


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    t = load()
    cmd = a[0]
    if cmd == "status":
        for k, pr in t["priority"].items():
            ok, why, _ = can_post(t, k, pr)
            print(json.dumps({"story": k, "project": pr.get("project"), "hours_left": round((pr["expires"] - time.time()) / 3600, 1),
                              "auto_posts_24h": len([p for p in pr.get("auto_posts", []) if time.time() - p[0] < 86400]),
                              "can_post_now": ok, "why": why, "credits_story": spent(t, k), "credits_24h_all": spent(t, None, 86400),
                              "rejected": pr.get("rejected", []), "banked_exhausted": pr.get("exhausted", False)}))
        return
    if cmd == "can-post":
        k, pr = find(t, a[1])
        ok, why, nxt = can_post(t, k, pr, urgent="--urgent" in a)
        print(json.dumps({"story": k, "allowed": ok, "reason": why}))
    elif cmd == "can-spend":
        k, pr = find(t, a[1])
        n = int(a[2])
        ok = spent(t, k) + n <= STORY_CREDITS and spent(t, None, 86400) + n <= DAY_CREDITS
        print(json.dumps({"story": k, "allowed": ok, "story_credits_so_far": spent(t, k), "day_credits_so_far": spent(t, None, 86400),
                          "limits": {"story": STORY_CREDITS, "day": DAY_CREDITS},
                          "reason": "ok" if ok else "over the automatic credit limit: ask William"}))
    elif cmd == "record-post":
        k, pr = find(t, a[1])
        pr.setdefault("auto_posts", []).append([int(time.time()), a[2]])
        save(t)
        print("recorded")
    elif cmd == "record-credits":
        k, pr = find(t, a[1])
        t["credits_log"].append([int(time.time()), int(a[2]), k])
        save(t)
        print("recorded")
    elif cmd == "reject":
        k, pr = find(t, a[1])
        pr.setdefault("rejected", []).append({"clip": a[2], "why": " ".join(a[3:])})
        save(t)
        print("recorded")
    elif cmd == "exhausted":
        k, pr = find(t, a[1])
        pr["exhausted"] = True
        save(t)
        print("recorded")
    elif cmd == "seen-add":
        k, pr = find(t, a[1])
        for vid in a[2:]:
            for tag in (vid, "live:" + vid):
                if tag not in pr.setdefault("seen", []):
                    pr["seen"].append(tag)
        save(t)
        print("recorded")
    elif cmd == "pending-add" or cmd == "pending-add-live":
        t.setdefault("pending", []).append({"id": a[1], "story": " ".join(a[2:]), "kind": "live" if cmd.endswith("live") else "project",
                                            "added": int(time.time()), "last_emit": 0})
        save(t)
        print("recorded")
    elif cmd == "pending-done":
        t["pending"] = [x for x in t.get("pending", []) if x["id"] != a[1]]
        save(t)
        print("done")
    elif cmd == "pending-list":
        print(json.dumps(t.get("pending", []), indent=1))
    elif cmd == "log-post":
        k, pr = find(t, a[1])
        clip = a[2]
        opt = {a[i][2:]: a[i + 1] for i in range(3, len(a) - 1, 2) if a[i].startswith("--")}
        rows = list(csv.reader(open(LOG)))
        h = rows[0]
        row = [""] * len(h)
        now = datetime.now(ET)

        def put(col, val):
            if col in h:
                row[h.index(col)] = val
        put("post_et", now.strftime("%Y-%m-%d %H:%M"))
        put("platform", "YouTube")
        put("source", opt.get("source", ""))
        put("niche", "news (breaking)")
        put("content_type", "priority-story follow-up")
        put("clip_id", clip)
        put("title", opt.get("title", ""))
        put("opus_curved", opt.get("score", ""))
        put("group", "news priority follow-up")
        put("status", f"posted {now.strftime('%m/%d %H:%M')} ET (post task accepted; live URL not yet confirmed)")
        put("why_it_did_or_didnt_work", f"Auto follow-up on priority story '{k}'.")
        put("lane", "news")
        put("radar_signal", opt.get("signal", "priority follow-up"))
        put("source_age_h_at_post", opt.get("source-age-h", ""))
        rows.append(row)
        csv.writer(open(LOG, "w", newline="")).writerows(rows)
        print("logged")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
