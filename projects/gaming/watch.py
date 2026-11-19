#!/usr/bin/env python3
"""GTA 6 streamer/YouTuber watcher for wrdgamingclipz. Detect only: it never submits to OpusClip and never posts.
Needs no API key (free feeds and yt-dlp only), like projects/opusclip/radar_loop.py. Prints one line per NEW item:

  GAMEWATCH_VIDEO  a GTA 6 video (<=24 h) on an approved channel: ready to screen/clip. States source minutes, credit
                   cost and whether the budget guard allows auto-submit (<=40 min) or it needs an ffmpeg cut / William.
  GAMEWATCH_LIVE   an approved channel is live now (GTA 6 title, or a GTA-RP streamer in the launch window)
  GAMEWATCH_CANDIDATE  same, on a channel that is not "approved": information only, tagged UNAPPROVED, never an alert
  GAMEWATCH_ERROR  a scan failed (throttled to once per 2 hours)

Only candidates.json entries with "approved": true produce VIDEO/LIVE alerts.

  watch.py                 loop forever (every 12 min, 7 AM-11 PM ET)
  watch.py --once          one scan now (testing); respects the window unless --anytime
  watch.py --ignore-state  do not read or write the dedupe state
  watch.py --demo          print one clearly labelled test alert (end-to-end test)
  watch.py --anytime       ignore the 7 AM-11 PM window (testing)
  watch.py --only NAME     scan just the candidate whose name contains NAME
Health: watch_status.json (last scan time, counts, errors), watch.log.
"""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gaming_budget  # noqa: E402

YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"
CANDS = os.path.join(HERE, "candidates.json")
STATE = os.path.join(HERE, "watch_state.json")
STATUS = os.path.join(HERE, "watch_status.json")
LOG = os.path.join(HERE, "watch.log")
ET = ZoneInfo("America/New_York")
INTERVAL_MIN = int(os.environ.get("GAMEWATCH_INTERVAL_MIN", "12"))
WINDOW = (7, 23)
MAX_AGE_H = float(os.environ.get("GAMEWATCH_MAX_AGE_H", "24"))
MIN_DUR_S = 60
LAUNCH = datetime(2026, 11, 19, tzinfo=ET)
REALERT_H = 48
GTA = re.compile(r"\bgta\s*(6|vi|6:)|\bgta\s*vi\b|grand theft auto\s*(6|vi)\b|\bgta6\b|vice city|\bleonida\b|jason duval|lucia caminos|grand theft auto", re.I)


def run(cmd, timeout=240):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def fetch(cand, tab, n):
    """Newest n items from a channel tab via yt-dlp. Returns rows or raises."""
    url = f"https://www.youtube.com/channel/{cand['channel_id']}/{tab}"
    fmt = "%(id)s\x1f%(live_status)s\x1f%(timestamp)s\x1f%(release_timestamp)s\x1f%(duration)s\x1f%(title)s\x1f%(description).400s\x1e"
    r = run([YTDLP, "--no-warnings", "--ignore-errors", "--skip-download", "--playlist-end", str(n), "--print", fmt, url])
    if r.returncode != 0 and not r.stdout.strip():
        err = (r.stderr or "no output").strip()
        if "does not have a" in err or "Sign in to confirm your age" in err:
            return []          # no such tab, or only age-gated items (needs cookies): not a scan failure
        raise RuntimeError(err[-160:])
    rows = []
    for rec in r.stdout.split("\x1e"):
        p = rec.strip("\n").split("\x1f")
        if len(p) < 7:
            continue
        num = lambda s: float(s) if s not in ("NA", "None", "") else None
        rows.append({"id": p[0], "status": p[1], "ts": num(p[2]) or num(p[3]), "dur": num(p[4]), "title": p[5], "desc": p[6]})
    return rows


def in_launch_window(now):
    return now >= LAUNCH


def relevant(cand, title, desc, now):
    if GTA.search(title) or GTA.search(desc or ""):
        return "title/description mentions GTA"
    if cand.get("gta_rp") and in_launch_window(now):
        return "GTA-RP streamer in launch window"
    return None


def window_open(now):
    return WINDOW[0] <= now.hour < WINDOW[1]


def budget_note(dur_s):
    mins = max(1, int(round((dur_s or 0) / 60)))
    v = gaming_budget.can_spend(mins)
    if v["allowed"]:
        return f"{mins} min source, ~{v['cost']} credits, AUTO-SUBMIT OK by budget (still needs the channel's approval + screening)"
    return f"{mins} min source, ~{v['cost']} credits, NOT auto: {'; '.join(v['reasons'])}"


def scan_channel(cand, now):
    out = []
    ts_now = time.time()
    try:
        vids = fetch(cand, "videos", 5)
        lives = fetch(cand, "streams", 3)
    except Exception as e:  # noqa: BLE001
        return [("error", cand["name"], str(e), None)]
    seen = set()
    for r in vids + lives:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        why = relevant(cand, r["title"], r["desc"], now)
        if not why:
            continue
        if r["status"] in ("is_live", "is_upcoming"):
            if r["status"] == "is_live":
                out.append(("live", cand["name"], r, why))
            continue
        if r["status"] == "post_live":
            continue
        if r["ts"] is None or (ts_now - r["ts"]) / 3600 > MAX_AGE_H:
            continue
        if not r["dur"] or r["dur"] < MIN_DUR_S:
            continue
        out.append(("video", cand["name"], r, why))
    return out


def fmt_item(kind, cand, r, why):
    approved = cand.get("approved")
    tag = "" if approved else " UNAPPROVED"
    url = f"https://www.youtube.com/watch?v={r['id']}"
    age = f"{(time.time() - r['ts']) / 3600:.1f}h old" if r.get("ts") else "age ?"
    if kind == "live":
        name = "GAMEWATCH_LIVE" if approved else "GAMEWATCH_CANDIDATE"
        return f"{name}{tag} {cand['name']} LIVE | {r['title'][:90]} | {url} | {why}"
    name = "GAMEWATCH_VIDEO" if approved else "GAMEWATCH_CANDIDATE"
    return f"{name}{tag} {cand['name']} | {r['title'][:90]} | {url} | {age}, {budget_note(r['dur'])} | {why}"


def scan(ignore_state=False, only=None):
    cands = json.load(open(CANDS))["candidates"]
    cands = [c for c in cands if c.get("channel_id") and c.get("verdict") != "skip" and (not only or only.lower() in c["name"].lower())]
    state = {} if ignore_state or not os.path.exists(STATE) else json.load(open(STATE))
    nowt = time.time()
    state = {k: t for k, t in state.items() if nowt - t < 7 * 86400}
    now = datetime.now(ET)
    with ThreadPoolExecutor(4) as ex:
        results = list(ex.map(lambda c: (c, scan_channel(c, now)), cands))
    lines, errors = [], []
    for c, items in results:
        for kind, name, r, why in items:
            if kind == "error":
                errors.append(f"{name}: {r}")
                continue
            key = f"{kind}:{r['id']}"
            if nowt - state.get(key, 0) < REALERT_H * 3600:
                continue
            state[key] = nowt
            lines.append(fmt_item(kind, c, r, why))
    if not ignore_state:
        json.dump(state, open(STATE, "w"))
    return lines, errors, len(cands)


def write_status(n, printed, errors):
    json.dump({"last_scan": datetime.now(ET).isoformat(timespec="seconds"), "channels": n, "printed": printed, "errors": errors[:10]},
              open(STATUS, "w"), indent=1)


def say(line):
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(f"{datetime.now(ET).isoformat(timespec='seconds')} {line}\n")


def demo():
    say("GAMEWATCH_VIDEO DEMO (test alert, not real) Adin Ross | GTA 6 FIRST HOUR LIVE REACTION | https://www.youtube.com/watch?v=DEMO0000000 | "
        "3.0h old, 25 min source, ~25 credits, AUTO-SUBMIT OK by budget (still needs approval + screening) | title/description mentions GTA")


def main():
    a = sys.argv[1:]
    if "--demo" in a:
        return demo()
    only = a[a.index("--only") + 1] if "--only" in a else None
    ign = "--ignore-state" in a
    if "--once" in a:
        if not window_open(datetime.now(ET)) and "--anytime" not in a:
            print("outside 7 AM-11 PM ET window; use --anytime to test")
            return
        lines, errors, n = scan(ign, only)
        write_status(n, len(lines), errors)
        for l in lines:
            say(l)
        for e in errors:
            say(f"GAMEWATCH_ERROR {e}")
        if not lines and not errors:
            print(f"scan ok: {n} channels, nothing new")
        return
    last_err = 0
    while True:
        now = datetime.now(ET)
        if window_open(now):
            try:
                lines, errors, n = scan(ign, only)
                write_status(n, len(lines), errors)
                for l in lines:
                    say(l)
                if errors and time.time() - last_err > 7200:
                    say(f"GAMEWATCH_ERROR {len(errors)} channel(s) failed: {errors[0]}")
                    last_err = time.time()
            except Exception as e:  # noqa: BLE001
                if time.time() - last_err > 7200:
                    say(f"GAMEWATCH_ERROR scan failed: {e}")
                    last_err = time.time()
        time.sleep(INTERVAL_MIN * 60)


if __name__ == "__main__":
    main()
