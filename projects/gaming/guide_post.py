#!/usr/bin/env python3
"""Post an APPROVED guide Short to YouTube wrdgamingclipz (William tapped Approve). Never run without his approval.

  guide_post.py ID [--dry-run] [--now]     ID = guide id (out/ID.guide.json, .mp4, .desc.txt, .thumb.jpg)

Picks the next free slot from the channel's real upload list (public + scheduled), so guides, wow-moment posts and Opus posts all count:
  - daily cap: post_caps.json ("default" and per-date overrides); window 7 AM-11 PM ET; posts at least GAP_H hours apart;
  - if the next slot is within 10 minutes (or --now) it publishes immediately (public); otherwise it uploads PRIVATE with
    status.publishAt, and YouTube publishes it at that time.
Uploads with the custom thumbnail (guide_thumb.py), marks the scout topic built, appends to out/lane_tracker.csv, prints ONE summary line.
YouTube only; TikTok (rvclips6) is a separate step.
"""
import argparse, csv, datetime, json, os, re, subprocess, sys, urllib.request
from zoneinfo import ZoneInfo

B = os.path.dirname(os.path.abspath(__file__))
OUT = B + "/out"
ET = ZoneInfo("America/New_York")
CHANNEL = "UCIbJfNm2nJKUCItsO0XGhiw"
GAP_H = 2.0
WINDOW = (7, 23)
CORE_TAGS = ["gta 6", "gta6", "grand theft auto 6", "grand theft auto vi", "gta vi", "rockstar games"]


def api(url, tok):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": "Bearer " + tok}), timeout=40))


def token():
    body = ("client_id=" + os.environ["GOOGLE_OAUTH_CLIENT_ID"] + "&client_secret=" + os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]
            + "&refresh_token=" + os.environ["GOOGLE_OAUTH_REFRESH_TOKEN_GAMING"] + "&grant_type=refresh_token").encode()
    return json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=body), timeout=30))["access_token"]


def channel_times(tok):
    """Datetimes (ET) of the channel's published + scheduled videos, newest 50."""
    pl = "UU" + CHANNEL[2:]
    ids = [i["contentDetails"]["videoId"] for i in api(f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={pl}", tok)["items"]]
    times = []
    for v in api("https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=" + ",".join(ids), tok)["items"]:
        st = v["status"]
        if st["privacyStatus"] == "private" and not st.get("publishAt"):
            continue  # unscheduled private draft
        t = st.get("publishAt") or v["snippet"]["publishedAt"]
        times.append(datetime.datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(ET))
    return times


def cap_for(day):
    c = json.load(open(B + "/post_caps.json"))
    return int(c.get(day.isoformat(), c["default"]))


def next_slot(times, now):
    """Earliest free slot: today from now (+2 min), later days from 9 AM; respects the daily cap, the 7 AM-11 PM window and the gap."""
    for n in range(14):
        day = now.date() + datetime.timedelta(days=n)
        same = sorted(t for t in times if t.date() == day)
        if len(same) >= cap_for(day):
            continue
        if n == 0:
            earliest = max(datetime.datetime.combine(day, datetime.time(WINDOW[0], 0), ET), now + datetime.timedelta(minutes=2))
        else:
            earliest = datetime.datetime.combine(day, datetime.time(9, 0), ET)
        if same:
            earliest = max(earliest, same[-1] + datetime.timedelta(hours=GAP_H))
        latest = datetime.datetime.combine(day, datetime.time(WINDOW[1], 0), ET) - datetime.timedelta(minutes=30)
        if earliest <= latest:
            return earliest, len(same), cap_for(day)
    sys.exit("no free slot in the next 14 days")


def tags_for(g):
    t = list(CORE_TAGS)
    title = re.sub(r"\s+in GTA 6.*$", "", g["yt_title"], flags=re.I)
    title = re.sub(r"^(how to|where to find|where to get|free)\s+", "", title, flags=re.I).strip().lower()
    for extra in ("gta 6 secrets", "gta 6 guide", "gta 6 " + title, title):
        if extra and extra not in t and len(t) < 10:
            t.append(extra)
    return ",".join(t[:10])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("id"); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--now", action="store_true")
    a = ap.parse_args(); gid = a.id
    g = json.load(open(f"{OUT}/{gid}.guide.json"))
    mp4, desc, thumb = f"{OUT}/{gid}.mp4", f"{OUT}/{gid}.desc.txt", f"{OUT}/{gid}.thumb.jpg"
    for f in (mp4, desc):
        if not os.path.exists(f):
            sys.exit("missing " + f)
    if not os.path.exists(thumb) and g.get("thumb"):
        subprocess.run([sys.executable, B + "/guide_thumb.py", gid], check=True)
    now = datetime.datetime.now(ET)
    tok = token(); times = channel_times(tok)
    slot, used, cap = next_slot(times, now)
    immediate = a.now or (slot - now) <= datetime.timedelta(minutes=10)
    when = "now" if immediate else slot.strftime("%a %b %-d %-I:%M %p ET")
    if a.dry_run:
        print(f"DRY RUN {gid}: slot {when} (that day has {used}/{cap}); title {g['yt_title']!r}; tags {tags_for(g)}")
        return
    cmd = [sys.executable, B + "/yt_upload_gaming.py", mp4, "--title", g["yt_title"], "--desc-file", desc, "--category", "20", "--tags", tags_for(g)]
    if os.path.exists(thumb):
        cmd += ["--thumb", thumb]
    cmd += ["--privacy", "public"] if immediate else ["--privacy", "private", "--publish-at", slot.isoformat()]
    r = subprocess.run(cmd, capture_output=True, text=True)
    open(f"{OUT}/{gid}.post.txt", "w").write(r.stdout + r.stderr)
    m = re.search(r"video id: (\S+)", r.stdout)
    if r.returncode or not m:
        sys.exit("UPLOAD FAILED: " + (r.stdout + r.stderr)[-400:])
    vid = m.group(1)
    if g.get("topic_id"):
        subprocess.run([sys.executable, B + "/guide_scout.py", "built", g["topic_id"], vid], capture_output=True, text=True)
    with open(f"{OUT}/lane_tracker.csv", "a", newline="") as f:
        csv.writer(f).writerow([vid, g["yt_title"], "guide", g.get("creator", ""), 0, (now if immediate else slot).strftime("%Y-%m-%dT%H:%M"),
                                f"guide {gid}; template v2; thumbnail set; {'published' if immediate else 'scheduled'} on William's Approve tap"])
    print(f"{'POSTED' if immediate else 'SCHEDULED'} {g['yt_title']} | {when} | https://youtube.com/shorts/{vid} | day {used + 1}/{cap}")


if __name__ == "__main__":
    main()
