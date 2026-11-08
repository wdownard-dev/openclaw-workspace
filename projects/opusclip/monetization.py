#!/usr/bin/env python3
"""YouTube Partner Program progress tracker for wrdclipz.

Run: python3 -I monetization.py   (from projects/opusclip; env supplies YOUTUBE_API_KEY and the
GOOGLE_OAUTH_* egress-proxy sentinels)

Reads
  - public: subscribers, total views, video count, public uploads in the last 90 days (Data API, API key)
  - owner-only: 12-month long-form watch hours and 90-day Shorts views (YouTube Analytics API; needs the
    yt-analytics.readonly scope on GOOGLE_OAUTH_REFRESH_TOKEN)
Writes
  - monetization-log.csv    one row per day (appended; same-day rerun replaces the row)
  - MONETIZATION-STATUS.md  latest snapshot, for Morpheus and the Strategist
Prints a short summary. Thresholds are YouTube's published YPP tiers; confirm in Studio > Earn.
"""
import csv, datetime as dt, json, os, sys, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = f"{HERE}/monetization-log.csv"
STATUS = f"{HERE}/MONETIZATION-STATUS.md"
CHANNEL = "UCxl0SIOxzXMLd6vMxtmvE3g"
UPLOADS = "UU" + CHANNEL[2:]
KEY = os.environ.get("YOUTUBE_API_KEY", "")
FIELDS = ["date", "subs", "views_total", "videos", "public_uploads_90d", "watch_hours_12m_longform",
          "shorts_views_90d", "analytics"]

# (name, subs, uploads_90d, watch_hours_12m, shorts_views_90d)
TIERS = {"Full (ads)": (1000, None, 4000, 10_000_000), "Early (fan funding)": (500, 3, 3000, 3_000_000)}


def get(url, token=None):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token} if token else {})
    return json.load(urllib.request.urlopen(req, timeout=30))


def public_stats():
    s = get("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=%s&key=%s" % (CHANNEL, KEY))
    st = s["items"][0]["statistics"]
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)
    ids, page = [], ""
    while True:
        p = get("https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50"
                "&playlistId=%s&key=%s%s" % (UPLOADS, KEY, page))
        ids += [i["contentDetails"]["videoId"] for i in p["items"]]
        if "nextPageToken" not in p or len(ids) >= 300:
            break
        page = "&pageToken=" + p["nextPageToken"]
    recent = 0
    for i in range(0, len(ids), 50):
        v = get("https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id=%s&key=%s"
                % (",".join(ids[i:i + 50]), KEY))
        for it in v["items"]:
            when = dt.datetime.fromisoformat(it["snippet"]["publishedAt"].replace("Z", "+00:00"))
            if it["status"]["privacyStatus"] == "public" and when >= cutoff:
                recent += 1
    return int(st["subscriberCount"]), int(st["viewCount"]), int(st["videoCount"]), recent


def analytics():
    """Returns (watch_hours_12m_longform, shorts_views_90d) or (None, None, reason)."""
    try:
        body = "&".join(["client_id=" + os.environ["GOOGLE_OAUTH_CLIENT_ID"],
                         "client_secret=" + os.environ["GOOGLE_OAUTH_CLIENT_SECRET"],
                         "refresh_token=" + os.environ["GOOGLE_OAUTH_REFRESH_TOKEN"],
                         "grant_type=refresh_token"]).encode()
        tok = json.load(urllib.request.urlopen(urllib.request.Request(
            "https://oauth2.googleapis.com/token", data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"}), timeout=30))["access_token"]
    except Exception as e:
        return None, None, "token refresh failed: %s" % e

    def report(days):
        end = dt.date.today()
        q = urllib.parse.urlencode({
            "ids": "channel==MINE", "startDate": str(end - dt.timedelta(days=days)), "endDate": str(end),
            "metrics": "views,estimatedMinutesWatched", "dimensions": "creatorContentType"})
        return get("https://youtubeanalytics.googleapis.com/v2/reports?" + q, tok).get("rows") or []

    try:
        long_minutes = sum(r[2] for r in report(365) if r[0].upper() != "SHORTS")
        shorts_views = sum(r[1] for r in report(90) if r[0].upper() == "SHORTS")
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:300]
        hint = ("scope missing: re-authorize with yt-analytics.readonly" if e.code in (401, 403)
                and "insufficient" in detail.lower() else
                "YouTube Analytics API not enabled in the Cloud project" if "has not been used" in detail
                or "disabled" in detail.lower() else "")
        return None, None, "analytics HTTP %s %s %s" % (e.code, hint, detail)
    return round(long_minutes / 60, 1), int(shorts_views), "ok"


def pct(v, need):
    return None if v is None else min(100.0, 100.0 * v / need)


def main():
    subs, views, videos, recent = public_stats()
    hours, shorts, note = analytics()
    today = str(dt.date.today())
    row = {"date": today, "subs": subs, "views_total": views, "videos": videos, "public_uploads_90d": recent,
           "watch_hours_12m_longform": "" if hours is None else hours,
           "shorts_views_90d": "" if shorts is None else shorts, "analytics": note[:80]}
    rows = []
    if os.path.exists(LOG):
        rows = [r for r in csv.DictReader(open(LOG)) if r["date"] != today]
    rows.append(row)
    with open(LOG, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    def rate(field, days=14):
        """Average gain per day over the trailing window of logged days."""
        pts = [(dt.date.fromisoformat(r["date"]), float(r[field])) for r in rows if r[field] != ""]
        pts = [p for p in pts if (dt.date.today() - p[0]).days <= days]
        if len(pts) < 2 or pts[-1][0] == pts[0][0]:
            return None
        return (pts[-1][1] - pts[0][1]) / (pts[-1][0] - pts[0][0]).days

    def eta(v, need, field):
        if v is None:
            return "n/a (no analytics)"
        if v >= need:
            return "reached"
        r = rate(field)
        if not r or r <= 0:
            return "no growth measured yet"
        return "~%d days at the recent pace" % ((need - v) / r)

    lines = ["# wrdclipz monetization progress (%s ET)" % today, "",
             "Subscribers %s | total views %s | videos %s | public uploads in last 90 d: %s" %
             (subs, views, videos, recent), "",
             "Analytics: %s" % note, ""]
    lines += ["| Tier | Subscribers | Public uploads (90 d) | Long-form watch hours (12 mo) | Shorts views (90 d) |",
              "|---|---|---|---|---|"]
    for name, (ns, nu, nh, nv) in TIERS.items():
        up = "n/a" if nu is None else ("%d/%d %s" % (recent, nu, "ok" if recent >= nu else "short"))
        hh = "n/a" if hours is None else "%.1f/%d (%.1f%%)" % (hours, nh, pct(hours, nh))
        sv = "n/a" if shorts is None else "%d/%d (%.2f%%)" % (shorts, nv, pct(shorts, nv))
        lines.append("| %s | %d/%d (%.1f%%) | %s | %s | %s |" % (name, subs, ns, pct(subs, ns), up, hh, sv))
    lines += ["", "Everything also needs: 2-step verification on, no active Community Guidelines strikes, an AdSense "
              "account. Qualify by subscribers AND (watch hours OR Shorts views).", "",
              "ETA to full tier (recent 14-day pace): subscribers %s; watch hours %s; Shorts views %s." %
              (eta(subs, 1000, "subs"), eta(hours, 4000, "watch_hours_12m_longform"),
               eta(shorts, 10_000_000, "shorts_views_90d"))]
    open(STATUS, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.exit("monetization.py failed: %s" % e)
