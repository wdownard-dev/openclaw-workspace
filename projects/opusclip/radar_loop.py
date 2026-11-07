#!/usr/bin/env python3
"""Fast news detector for wrdclipz. Runs every 15 minutes (7 AM-11 PM ET) and prints one RADAR_* line
per NEW item. It needs no API key: the OpenClaw stream runner does not receive stored secrets, so this
loop uses only free feeds and yt-dlp search. The agent adds view-velocity numbers afterwards by running
`radar.py --query ... --no-state` (which has the YouTube key).

  RADAR_LIVE   an official channel (sheriff/police/NTSB/...) is LIVE on a big breaking event
  RADAR_ALERT  an official video (<=24 h, 2-40 min) exists for a big breaking event: ready to clip
  RADAR_EARLY  a very big event (many outlets, last 2 h) and no official video yet
  RADAR_ERROR  the scan failed (throttled to once per 2 hours)
  RADAR_HOT    one of our own news clips is gaining views: that story becomes a PRIORITY for 48 h
  RADAR_FOLLOWUP  a priority story has something new: an official live stream or video, a news surge, or a
                  BANKED_DUE reminder (time to post the next unused clip from the same source)

Health (checked by the daily tracker): radar_loop_status.json (last scan time) and radar_loop.log.
Every candidate event and the decision made about it goes to radar_loop_decisions.jsonl so the weekly
review can tune thresholds and see what the filters hid.

  radar_loop.py                 loop forever
  radar_loop.py --once          one scan now (testing)
  radar_loop.py --ignore-state  do not read or write the dedupe state (testing)
  radar_loop.py --demo          print one clearly-labelled test ALERT for the HCSO Citibank briefing (end-to-end test)
  radar_loop.py --prioritize "story words" [--hours 48] [--project OPUS_PROJECT_ID]   make a story a priority by hand
  radar_loop.py --priorities    list active priority stories and our tracked clips
  radar_loop.py --unprioritize "story words"              end a priority early
  radar_loop.py --rename "old words" "new words"          change a priority's story words, keeping its clip, project, spacing and posts

Story priority (William, 2026-11-06): when a clip we posted starts to do well, prioritize that story for a day or
two and follow its traction: watch it every 15 min for new official streams/videos and news surges, with no outlet
threshold, and use the unused clips already made from the same source.
"""
import csv, hashlib, json, os, re, subprocess, sys, time, urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import radar  # noqa: E402

STATE = os.path.join(HERE, "radar_loop_state.json")
STATUS = os.path.join(HERE, "radar_loop_status.json")
LOG = os.path.join(HERE, "radar_loop.log")
DECISIONS = os.path.join(HERE, "radar_loop_decisions.jsonl")
INTERVAL_MIN = int(os.environ.get("RADAR_INTERVAL_MIN", "15"))
ET = ZoneInfo("America/New_York")
ALERT_MIN_OUTLETS = 4
EARLY_MIN_OUTLETS = 6
ROUTINE_EARLY_MIN_OUTLETS = 8   # routine-looking road crashes still surface if the outlet count is high
MAX_EARLY = 2
REALERT_H = 24
TODAY = "&sp=EgIIAg%253D%253D"       # YouTube upload date filter: today (last 24 h)

TRACK = os.environ.get("RADAR_TRACK_FILE", os.path.join(HERE, "radar_track.json"))
TRACK_LOG = os.path.join(HERE, "radar_track.log")
EXPERIMENT_LOG = os.path.join(HERE, "experiment-log.csv")
CHANNEL_SHORTS = "https://www.youtube.com/@wrdclipz/shorts"
HOT_VIEWS = int(os.environ.get("RADAR_HOT_VIEWS", "300"))      # total views within HOT_MAX_AGE_H of posting
HOT_GAIN_1H = int(os.environ.get("RADAR_HOT_GAIN_1H", "60"))   # or a rate of this many views per hour
HOT_MAX_AGE_H = 36
PRIORITY_H = 48
PRIORITY_EXTEND_H = 24          # extended while the clip still gains >= EXTEND_GAIN_1H an hour
EXTEND_GAIN_1H = 20
PRIORITY_MAX_H = 168
FOLLOW_NEWS_MIN_OUTLETS = 3
NEWS_NEW_WORDS = re.compile(r"\b(arrest\w*|charged|charges|identified|released|footage|video|bodycam|lawsuit|funeral|report|"
                            r"update|new details|cause|investigation|sentenced|trial|hearing|suspect)\b", re.I)

ROUTINE = re.compile(r"\b(vehicles?|cars?|pickups?|trucks?|semi|motorcycl\w*|dui|rollover|interstate|highway|turnpike|lanes?|"
                     r"roads?|intersection|bicycl\w*|pedestrian|scooter|bus|driver|dragged)\b", re.I)
SPICY = re.compile(r"\b(plane|jet|aircraft|helicopter|airliner|train|derailment|gunman|shooter|mass shooting|explosion|"
                   r"hostage|manhunt|standoff|tornado|wildfire|hurricane|earthquake|collapse|officers?|deputies|"
                   r"citibank|school|hospital|mall|church|nightclub|concert|stadium|killed \d{2,})\b", re.I)


def yt_today(query):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query) + TODAY
    return radar._flat_full(url)


def official_rows(rows, live, ctx=""):
    out = []
    for r in rows:
        if not radar.is_official_name(r["channel"]):
            continue
        if ctx and not radar.relevant(r["title"], ctx):
            continue            # an official-sounding channel, but the video is not about this story
        if live and r["status"] in ("is_live", "is_upcoming"):
            out.append(r)
        elif not live and r["status"] not in ("is_live", "is_upcoming", "post_live") and r["dur"] and 120 <= r["dur"] <= radar.SOURCE_MAX_MIN * 60:
            out.append(r)
    return out


def record(decision, c, n, extra=None):
    row = {"ts": datetime.now(ET).isoformat(timespec="seconds"), "story": c["title"][:140], "outlets": n, "decision": decision}
    if extra:
        row.update(extra)
    with open(DECISIONS, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def scan(ignore_state=False):
    clusters = radar.event_clusters()
    state = {} if ignore_state or not os.path.exists(STATE) else json.load(open(STATE))
    now = time.time()
    early_tokens = [e for e in state.pop("_early_tokens", []) if now - e[0] < 2 * 86400]
    state = {k: t for k, t in state.items() if now - t < 7 * 86400}
    state["_early_tokens"] = early_tokens
    fresh = lambda k: now - state.get(k, 0) > REALERT_H * 3600
    lines, early = [], 0

    def work(c):
        short = " ".join(radar.tokens(c["title"])[:5])
        plain = yt_today(short)            # what YouTube shows for the story today (titles reveal the agency)
        titles = [{"title": t} for t in c["titles"][:8]] + [{"title": r["title"]} for r in plain[:8]]
        ag = radar.agencies({"headline": c["title"], "query": c["title"]}, titles)
        ctx = " ".join(c["titles"][:8])
        live = official_rows(radar.yt_search_live_full(short + " press conference"), True, ctx)
        for a in ag:
            live += official_rows(radar.yt_search_live_full(a + " press conference"), True, ctx)
        vids = official_rows(plain, False, ctx) + official_rows(yt_today(short + " press conference"), False, ctx)
        for a in ag:
            vids += official_rows(yt_today(a + " news conference"), False, ctx)
        return c, ag, live, vids, plain

    with ThreadPoolExecutor(max_workers=4) as ex:
        work_out = list(ex.map(work, clusters))
    for c, ag, live, vids, plain in work_out:
        n = len(c["sources"])
        text = " ".join(c["titles"])
        if radar.BLOCK.search(text):
            record("skipped: sensitive", c, n)
            continue
        if radar.POLITICAL.search(text):
            record("skipped: political (held)", c, n)
            continue
        routine = bool(ROUTINE.search(text) and not SPICY.search(text))
        flags = (["allegation: attribute only"] if radar.ALLEGATION.search(text) else []) + \
                (["routine-looking road crash: judge whether the people involved make it a story"] if routine else [])
        base = {"story": c["title"], "outlets_2h": n, "agency": ag, "flags": flags}
        if not live and not vids:
            # William 11/6: TV-network/TMZ-type video is allowed if it is good, but only with his approval first
            ctx_text = " ".join(c["titles"][:8])
            opts = sorted((r for r in plain if r["dur"] and 60 <= r["dur"] <= radar.SOURCE_MAX_MIN * 60 and r["status"] != "is_live"
                           and radar.relevant(r["title"], ctx_text)),
                          key=lambda r: -r["views"])[:2]
            if opts:
                base["non_official_options_need_william_approval"] = [
                    {"channel": r["channel"], "title": r["title"][:80], "minutes": int(r["dur"] // 60), "views": r["views"],
                     "url": f"https://www.youtube.com/watch?v={r['id']}"} for r in opts]
        if live and n >= ALERT_MIN_OUTLETS and fresh("live:" + live[0]["id"]):
            r = live[0]
            lines.append(("LIVE", "live:" + live[0]["id"],
                          {**base, "official_live": {"channel": r["channel"], "title": r["title"][:90],
                                                     "url": f"https://www.youtube.com/watch?v={r['id']}"}}))
            record("LIVE", c, n, {"url": r["id"]})
        elif vids and n >= ALERT_MIN_OUTLETS and fresh(vids[0]["id"]):
            r = vids[0]
            lines.append(("ALERT", r["id"],
                          {**base, "official_video": {"channel": r["channel"], "title": r["title"][:90],
                                                      "minutes": r["dur"] // 60, "views": r["views"],
                                                      "url": f"https://www.youtube.com/watch?v={r['id']}"}}))
            record("ALERT", c, n, {"url": r["id"]})
        elif not live and not vids and n >= (ROUTINE_EARLY_MIN_OUTLETS if routine else EARLY_MIN_OUTLETS) and early < MAX_EARLY:
            k = "early:" + hashlib.md5(" ".join(sorted(radar.tokens(c["title"]))[:5]).encode()).hexdigest()[:10]
            tk_now = set(radar.tokens(c["title"]))
            seen_before = any(now - ts_ < REALERT_H * 3600 and len(tk_now & set(tk_)) >= 3 and
                              len(tk_now & set(tk_)) / max(1, min(len(tk_now), len(tk_))) >= 0.5
                              for ts_, tk_ in state.get("_early_tokens", []))
            if fresh(k) and not seen_before:
                state.setdefault("_early_tokens", []).append([now, sorted(tk_now)])
                early += 1
                lines.append(("EARLY", k, base))
                record("EARLY", c, n, {"routine": routine})
            else:
                record("already alerted (24h)", c, n)
        else:
            why = "already alerted (24h)" if (live or vids) else \
                f"below threshold ({'routine ' if routine else ''}{n} outlets, no official source)"
            record(why, c, n, {"routine": routine, "official_found": bool(live or vids)})
    for kind, key, payload in lines:
        state[key] = now
        print(f"RADAR_{kind} " + json.dumps(payload, ensure_ascii=False), flush=True)
    if not ignore_state:
        json.dump(state, open(STATE, "w"))
    return len(clusters), len(lines)


# ---------------------------------------------------------------- story priority / traction tracking
def tload():
    return json.load(open(TRACK)) if os.path.exists(TRACK) else {"videos": {}, "priority": {}, "hot_alerted": {}}


def tsave(t):
    json.dump(t, open(TRACK, "w"), indent=1)


def tlog(msg):
    with open(TRACK_LOG, "a") as f:
        f.write(f"{datetime.now(ET).isoformat(timespec='seconds')} {msg}\n")


def yt_view_info(vid):
    """Key-less: post time and current views of one of our videos."""
    r = subprocess.run([radar.YTDLP, "--no-warnings", "--skip-download", "--print", "%(timestamp)s|%(view_count)s",
                        f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True, timeout=60)
    p = (r.stdout.strip().splitlines() or [""])[-1].split("|")
    try:
        return int(float(p[0])), (int(p[1]) if len(p) > 1 and p[1].isdigit() else 0)
    except ValueError:
        return None, 0


def our_news_rows():
    """News-lane rows from experiment-log.csv (title, clip id) used to recognise our news clips on the channel."""
    rows = []
    if not os.path.exists(EXPERIMENT_LOG):
        return rows
    for r in csv.DictReader(open(EXPERIMENT_LOG)):
        if r.get("lane") == "news" and r.get("title"):
            rows.append(r)
    return rows


def match_log(title, rows):
    tk = set(radar.tokens(title))
    best, score = None, 0.0
    for r in rows:
        rk = set(radar.tokens(r["title"]))
        j = len(tk & rk) / max(1, len(tk | rk))
        if j > score:
            best, score = r, j
    return best if score >= 0.8 else None


def story_query_from(title):
    drop = radar.GENERIC | {"per", "hcso", "likely", "prevented", "far", "greater", "loss", "life", "ran", "toward"}
    words = [w for w in radar.tokens(title) if w not in drop]
    return " ".join(words[:4])


def track_tick(now=None):
    """Snapshot our recent Shorts, flag clips that are gaining, and make their story a priority."""
    now = now or time.time()
    t = tload()
    r = subprocess.run([radar.YTDLP, "--no-warnings", "--flat-playlist", "--playlist-end", "12", "--print",
                        "%(id)s\t%(view_count)s\t%(title)s", CHANNEL_SHORTS], capture_output=True, text=True, timeout=90)
    listing = []
    for line in r.stdout.splitlines():
        p = line.split("\t", 2)
        if len(p) == 3:
            listing.append((p[0], int(p[1]) if p[1].isdigit() else 0, p[2]))
    if not listing:
        raise RuntimeError("channel Shorts listing came back empty")
    news_rows = our_news_rows()
    out = []
    for vid, views, title in listing:
        v = t["videos"].get(vid)
        if v is None:
            ts, views2 = yt_view_info(vid)
            if ts is None or now - ts > 72 * 3600:
                t["videos"][vid] = {"title": title, "ts": ts or 0, "snaps": [], "old": True}
                continue
            v = t["videos"][vid] = {"title": title, "ts": ts, "snaps": [], "old": False}
            views = max(views, views2)
        if v.get("old"):
            continue
        v["snaps"].append([int(now), views])
        v["snaps"] = v["snaps"][-300:]
        age_h = (now - v["ts"]) / 3600
        # views per hour over the longest window up to ~1 h (needs >= 10 min of history, so a fast spike is seen early)
        window = [s for s in v["snaps"] if 600 <= now - s[0] <= 3900]
        if window:
            s0 = window[0]
            gain_1h = round((views - s0[1]) * 3600 / max(now - s0[0], 600))
            if views - s0[1] < 25:
                gain_1h = min(gain_1h, 24)       # tiny absolute gains are noise
        else:
            gain_1h = None
        v["views"], v["age_h"], v["gain_1h"] = views, round(age_h, 1), gain_1h
        log_row = match_log(v["title"], news_rows)
        tlog(f"{vid} {views} views, {age_h:.1f}h old, gain_1h={gain_1h}, news={'yes' if log_row else 'no'} | {v['title'][:60]}")
        if not log_row or age_h > HOT_MAX_AGE_H or vid in t["hot_alerted"]:
            continue
        if views >= HOT_VIEWS or (gain_1h is not None and gain_1h >= HOT_GAIN_1H):
            key = story_query_from(log_row["title"]) or story_query_from(v["title"])
            t["hot_alerted"][vid] = int(now)
            clip_id = log_row.get("clip_id", "")
            project = clip_id.split(".")[0] if "." in clip_id else ""
            same = [k for k, pr in t["priority"].items() if project and pr.get("project") == project]
            if same:                      # another clip from the same source is already driving this story
                t["priority"][same[0]].setdefault("also_clips", []).append(vid)
                tlog(f"HOT {vid} joins existing priority '{same[0]}' (same project {project})")
                continue
            t["priority"][key] = {"query": key, "video_id": vid, "title": v["title"], "project": project,
                                  "started": int(now), "expires": int(now + PRIORITY_H * 3600), "seen": [], "last_news": 0,
                                  "source": "auto"}
            out.append(("HOT", {"story": key, "our_clip": v["title"], "our_clip_url": f"https://www.youtube.com/shorts/{vid}",
                                "views": views, "hours_since_post": round(age_h, 1), "views_gained_last_hour": gain_1h,
                                "priority_until_hours": PRIORITY_H, "opus_project": project,
                                "note": "unused clips from the same OpusClip project can be posted as follow-ups with no extra credits"}))
            tlog(f"HOT {vid} -> priority '{key}' for {PRIORITY_H}h")
    # keep the file small
    t["videos"] = {k: v for k, v in t["videos"].items() if now - (v.get("ts") or 0) < 14 * 86400 or not v.get("ts")}
    # extend or expire priorities
    for key, pr in list(t["priority"].items()):
        if now > pr["expires"]:
            vid = t["videos"].get(pr["video_id"], {})
            gain = vid.get("gain_1h")
            if pr.get("source") == "auto" and gain is not None and gain >= EXTEND_GAIN_1H \
                    and now + PRIORITY_EXTEND_H * 3600 - pr["started"] <= PRIORITY_MAX_H * 3600:
                pr["expires"] = int(now + PRIORITY_EXTEND_H * 3600)
                tlog(f"priority '{key}' extended {PRIORITY_EXTEND_H}h (still gaining {gain}/h)")
            else:
                tlog(f"priority '{key}' expired")
                del t["priority"][key]
    # follow each active priority story
    for key, pr in t["priority"].items():
        q = pr["query"]
        ctx = key + " " + pr.get("title", "")
        found = []
        for r_ in official_rows(radar.yt_search_live_full(q + " press conference"), True, ctx):
            if ("live:" + r_["id"]) not in pr["seen"]:
                pr["seen"].append("live:" + r_["id"])
                found.append(("LIVE", r_))
        today = yt_today(q + " news conference") + yt_today(q)
        for r_ in official_rows(today, False, ctx):
            if r_["id"] not in pr["seen"]:
                pr["seen"].append(r_["id"])
                found.append(("VIDEO", r_))
        for kind, r_ in found:
            out.append(("FOLLOWUP", {"priority_story": key, "kind": kind, "channel": r_["channel"], "title": r_["title"][:90],
                                     "minutes": int((r_["dur"] or 0) // 60), "url": f"https://www.youtube.com/watch?v={r_['id']}",
                                     "our_clip_url": f"https://www.youtube.com/shorts/{pr['video_id']}" if pr.get("video_id") else "",
                                     "opus_project": pr.get("project", "")}))
        # methodical cadence: when the spacing and daily limits allow, remind the follow-up agent to post the next banked clip
        h_now = datetime.now(ET).hour
        recent_auto = [p_ for p_ in pr.get("auto_posts", []) if now - p_[0] < 86400]
        v_ts = t["videos"].get(pr.get("video_id", ""), {}).get("ts", 0)
        import followup as _fu
        last_post = max([p_[0] for p_ in pr.get("auto_posts", [])] + [v_ts, _fu.project_last_post(pr.get("project", ""))])
        if pr.get("project") and not pr.get("exhausted") and 8 <= h_now < 22 and len(recent_auto) < 3 \
                and now - last_post >= 3 * 3600 and now - pr.get("last_due", 0) >= 3 * 3600:
            pr["last_due"] = int(now)
            out.append(("FOLLOWUP", {"priority_story": key, "kind": "BANKED_DUE", "opus_project": pr["project"],
                                     "our_clip_url": f"https://www.youtube.com/shorts/{pr['video_id']}" if pr.get("video_id") else "",
                                     "auto_posts_24h": len(recent_auto), "hours_since_last_post": round((now - last_post) / 3600, 1) if last_post else None,
                                     "rejected_clips": [r_["clip"] for r_ in pr.get("rejected", [])]}))
        # news surge: several outlets, new headlines about the story
        if now - pr.get("last_news", 0) > 3 * 3600:
            try:
                root = radar.ET.fromstring(radar.http("https://news.google.com/rss/search?" + urllib.parse.urlencode(
                    {"q": f"{q} when:2h", "hl": "en-US", "gl": "US", "ceid": "US:en"}), 30))
                items = [(radar.clean_headline(i.findtext("title") or ""), (i.findtext("source") or "?")) for i in root.iter("item")]
                fresh_heads = [h for h, _ in items if NEWS_NEW_WORDS.search(h)]
                outlets = {s_ for _, s_ in items}
                if len(outlets) >= FOLLOW_NEWS_MIN_OUTLETS and fresh_heads:
                    pr["last_news"] = int(now)
                    out.append(("FOLLOWUP", {"priority_story": key, "kind": "NEWS", "outlets_2h": len(outlets),
                                             "new_headlines": fresh_heads[:3], "our_clip_url": f"https://www.youtube.com/shorts/{pr['video_id']}",
                                             "opus_project": pr.get("project", "")}))
            except Exception as e:
                tlog(f"news check failed for '{key}': {e}")
    # pending follow-ups (the stream-triggered agent cannot schedule one-shot jobs, so the loop reminds it)
    for pend in list(t.get("pending", [])):
        age_min = (now - pend["added"]) / 60
        if age_min > 240:
            out.append(("FOLLOWUP", {"kind": "PENDING_ABANDONED", "priority_story": pend["story"], "id": pend["id"],
                                     "note": "pending for 4 h with no result; tell William and run followup.py pending-done"}))
            t["pending"].remove(pend)
            continue
        if now - pend["last_emit"] < 10 * 60:
            continue
        if pend["kind"] == "live":
            r_ = subprocess.run([radar.YTDLP, "--no-warnings", "--skip-download", "--print", "%(live_status)s|%(duration)s",
                                 f"https://www.youtube.com/watch?v={pend['id']}"], capture_output=True, text=True, timeout=60)
            st = (r_.stdout.strip().splitlines() or [""])[-1].split("|")[0]
            if st in ("was_live", "not_live"):
                pend["last_emit"] = int(now)
                out.append(("FOLLOWUP", {"kind": "PENDING_CHECK", "priority_story": pend["story"], "video_id": pend["id"],
                                         "state": "stream ended: submit it to OpusClip now (VIDEO procedure), then followup.py pending-done " + pend["id"]}))
        elif age_min >= 8:
            pend["last_emit"] = int(now)
            out.append(("FOLLOWUP", {"kind": "PENDING_CHECK", "priority_story": pend["story"], "opus_project": pend["id"],
                                     "state": "submitted " + str(int(age_min)) + " min ago: check python3 opus.py status " + pend["id"] +
                                              "; if COMPLETE run the BANKED steps (b) to (f) for it; if still processing do nothing"}))
    tsave(t)
    return out


def cli_priority():
    t = tload()
    now = time.time()
    if "--rename" in sys.argv:
        i = sys.argv.index("--rename")
        old, new = sys.argv[i + 1], sys.argv[i + 2]
        ks = [k for k in t["priority"] if old.lower() in k.lower()]
        if not ks:
            sys.exit("no priority matches " + old)
        pr = t["priority"].pop(ks[0])
        pr["query"] = new
        t["priority"][new] = pr
        tsave(t)
        print(f"renamed '{ks[0]}' -> '{new}' (clip, project, spacing and posts kept)")
        return
    if "--priorities" in sys.argv:
        print("PRIORITY STORIES:")
        for k, pr in t["priority"].items():
            print(f"  '{k}' ({pr.get('source')}), {max(0, int((pr['expires'] - now) / 3600))} h left, clip {pr['video_id']}, project {pr.get('project')}")
        print("TRACKED CLIPS (last 72 h):")
        for vid, v in t["videos"].items():
            if not v.get("old") and v.get("views") is not None:
                print(f"  {vid} {v['views']} views, {v['age_h']}h old, gain_1h={v.get('gain_1h')} | {v['title'][:60]}")
        return
    q = sys.argv[sys.argv.index("--prioritize" if "--prioritize" in sys.argv else "--unprioritize") + 1]
    if "--unprioritize" in sys.argv:
        for k in [k for k in t["priority"] if q.lower() in k.lower()]:
            del t["priority"][k]
            print("removed", k)
    else:
        hours = int(sys.argv[sys.argv.index("--hours") + 1]) if "--hours" in sys.argv else PRIORITY_H
        proj = sys.argv[sys.argv.index("--project") + 1] if "--project" in sys.argv else ""
        t["priority"][q] = {"query": q, "video_id": "", "title": q, "project": proj, "started": int(now),
                            "expires": int(now + hours * 3600), "seen": [], "last_news": 0, "source": "manual"}
        print(f"priority '{q}' for {hours} h")
    tsave(t)


def demo():
    """One test ALERT built from the real HCSO Citibank briefing, to prove the whole chain end to end."""
    rows = [r for r in yt_today("Hillsborough County Sheriff news conference Citibank") if r["id"] == "2bQt2cGNSXk"] or \
           [{"id": "2bQt2cGNSXk", "channel": "HCSOSheriff", "title": "News Conference - Citibank Shooting", "dur": 1671, "views": 0}]
    r = rows[0]
    payload = {"story": "TEST ONLY (end-to-end check, not a new story): Citibank shooting, Tampa", "outlets_2h": 4,
               "agency": ["Hillsborough County Sheriff"], "flags": [],
               "official_video": {"channel": r["channel"], "title": r["title"][:90], "minutes": int((r["dur"] or 1671) // 60),
                                  "views": r["views"], "url": f"https://www.youtube.com/watch?v={r['id']}"}}
    print("RADAR_ALERT " + json.dumps(payload, ensure_ascii=False), flush=True)


def write_status(clusters, printed, error=None):
    json.dump({"last_scan_et": datetime.now(ET).isoformat(timespec="seconds"), "last_scan_epoch": int(time.time()),
               "clusters": clusters, "printed": printed, "error": error, "pid": os.getpid()}, open(STATUS, "w"))
    with open(LOG, "a") as f:
        f.write(f"{datetime.now(ET).isoformat(timespec='seconds')} scanned {clusters} clusters, printed {printed}"
                + (f", ERROR {error}" if error else "") + "\n")


def main():
    once = "--once" in sys.argv
    ignore_state = "--ignore-state" in sys.argv
    if "--prioritize" in sys.argv or "--priorities" in sys.argv or "--unprioritize" in sys.argv or "--rename" in sys.argv:
        cli_priority()
        return
    if "--demo" in sys.argv:
        demo()
        time.sleep(3600)       # stay alive so the supervisor does not treat a quick exit as a crash loop
        return
    last_err = 0.0
    while True:
        now = datetime.now(ET)
        if once or 7 <= now.hour < 23:
            try:
                n, k = scan(ignore_state)
                try:
                    for kind, payload in track_tick():
                        print(f"RADAR_{kind} " + json.dumps(payload, ensure_ascii=False), flush=True)
                        k += 1
                except Exception as te:
                    tlog(f"track_tick failed: {type(te).__name__}: {te}")
                write_status(n, k)
                if once:
                    print(f"scanned {n} event clusters, printed {k} lines")
            except Exception as e:
                msg = f"{type(e).__name__}: {str(e)[:200]}"
                write_status(0, 0, msg)
                if once or time.time() - last_err > 2 * 3600:
                    print(f"RADAR_ERROR {msg}", flush=True)
                    last_err = time.time()
        if once:
            return
        nxt = (now.minute // INTERVAL_MIN + 1) * INTERVAL_MIN
        time.sleep(max((nxt - now.minute) * 60 - now.second, 30))


if __name__ == "__main__":
    main()
