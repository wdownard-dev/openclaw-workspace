#!/usr/bin/env python3
"""Clip radar for wrdclipz (news lane).

Finds stories moving right now and checks whether an official source video exists to clip, or an
official stream is live. Signals:
  * event spikes: the same event reported by several outlets in the last 2 hours (Google News)
  * YouTube view velocity (the main gate for "this is pulling views")
  * topic feeds that only supply candidates: Google Trends, Google News sections, TMZ, Page Six,
    Reddit, Bluesky, Mastodon (headlines for information, never clipped)

Outputs, most urgent first:
  LIVE    an official channel (sheriff, police, NTSB, ...) is live or has a scheduled stream on a hot story
  ALERT   an official video is up (<=48 h, 2-40 min) on a hot story: ready to clip
  EARLY   a big event (many outlets) with no official video yet: be ready
  WATCH / HELD / BLOCKED  informational, never alerted

  radar.py                 scan, print report, record alerts in radar_state.json
  radar.py --no-state      scan without recording alerts (testing)
  radar.py --json          machine-readable (live, alerts, early, watch, blocked)
  radar.py --query "text"  test a single topic

Candidate topics -> yt-dlp flat search (free) -> YouTube Data API videos.list (1 unit per 50 ids).
Key comes from YOUTUBE_API_KEY (injected by the OpenClaw secrets store).
"""
import hashlib, json, os, re, subprocess, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "radar_state.json")
YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) wrdclipz-radar"}

MAX_CANDIDATES = 48
RESULTS_PER_QUERY = 10
MAX_VIDEO_AGE_H = 72
HOT_VPH = 400
ALERT_VPH = 1000
N_HOT = 3
SOURCE_MAX_AGE_H = 48
SOURCE_MAX_MIN = 40
REALERT_AFTER_H = 24
EVENT_MIN_OUTLETS = 3       # outlets reporting one event before it becomes a candidate
LIVE_MIN_OUTLETS = 3        # official live stream + this many outlets = LIVE alert
EARLY_MIN_OUTLETS = 6       # no official video yet: only a big event gets an EARLY alert
MAX_EARLY = 2

EVENT_QUERIES = ['shooting OR shot OR gunman OR stabbing',
                 'crash OR "plane crash" OR derailment OR collapse',
                 'explosion OR "building fire" OR evacuated OR "bomb threat"',
                 'manhunt OR standoff OR hostage OR "police chase"',
                 'tornado OR wildfire OR hurricane OR earthquake OR flooding']
EVENT_WINDOW = os.environ.get("RADAR_EVENT_WINDOW", "2h")


def event_feed_url(q):
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": f"({q}) when:{EVENT_WINDOW}", "hl": "en-US", "gl": "US", "ceid": "US:en"})


NEWS_FEEDS = [
    ("gnews-top", "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", 8),
    ("gnews-nation", "https://news.google.com/rss/headlines/section/topic/NATION?hl=en-US&gl=US&ceid=US:en", 6),
    ("gnews-world", "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en", 4),
    ("gnews-entertainment", "https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=en-US&gl=US&ceid=US:en", 4),
    ("tmz", "https://www.tmz.com/rss.xml", 5),
    ("pagesix", "https://pagesix.com/feed/", 3),
]
TRENDS = "https://trends.google.com/trending/rss?geo=US"
REDDIT_RSS = [("reddit-news", "https://www.reddit.com/r/news/.rss", 6),
              ("reddit-worldnews", "https://www.reddit.com/r/worldnews/.rss", 4),
              ("reddit-publicfreakout", "https://www.reddit.com/r/PublicFreakout/.rss", 4)]
BSKY_TRENDING = "https://public.api.bsky.app/xrpc/app.bsky.unspecced.getTrendingTopics?limit=10"
MASTO_LINKS = "https://mastodon.social/api/v1/trends/links?limit=8"

BLOCK = re.compile(r"\b(child sex|child porn\w*|sexual abuse|csam|child abuse|molest|rape[ds]?|sexual assault|suicide|"
                   r"school shooting|killed (?:his|her|their) (?:child|children|son|daughter)|"
                   r"minor|teen(?:ager)? (?:killed|dies|dead))\b", re.I)
POLITICAL = re.compile(r"\b(election|ballot|trump|biden|harris|vance|congress|senate|republican|democrat|"
                       r"gop|governor race|midterm|supreme court ruling)\b", re.I)
ALLEGATION = re.compile(r"\b(arrest(?:ed)?|accused|alleged|allegations?|charged|indicted|lawsuit|sued)\b", re.I)
OFFICIAL = re.compile(r"(sheriff|police|ntsb|nasa|noaa|usgs|whitehouse|coastguard|gov$)|"
                      r"\b(pd|department|dept|office|county|city of|state of|faa|fbi|doj|dhs|fire|rescue|emergency|"
                      r"court|nws|nhc|cdc|fda|military|army|navy|air force|marines|transportation safety|"
                      r"national weather|white house)\b", re.I)
NOT_OFFICIAL = re.compile(r"\b(news|tv|media|show|podcast|network|channel \d|nbc|abc|cbs|fox|cnn|msnbc|reuters|"
                          r"associated press|ap archive|wfla|wesh|wkmg|insider|times|post|daily|body ?cam|bodycam|cops|compilation|"
                          r"true crime|audit|prank|reaction|footage|clips?|archive)\b", re.I)
STOP = set("the a an of to in on at for and or is are was were be been by with from as it its this that "
           "after over into new says say said how why what who will has have had not but about up out".split())


def http(url, timeout=20):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def tokens(s):
    return [w for w in re.findall(r"[a-z0-9']+", s.lower()) if w not in STOP and len(w) > 1]


def clean_headline(t):
    return re.sub(r"\s+[-|]\s+[^-|]{2,40}$", "", t.strip())


def event_clusters():
    """Group recent Google News items by event; keep events reported by several distinct outlets."""
    items, seen = [], set()
    for q in EVENT_QUERIES:
        try:
            root = ET.fromstring(http(event_feed_url(q), 30))
        except Exception as e:
            print(f"warn: event query failed ({q[:20]}): {e}", file=sys.stderr)
            continue
        for it in root.iter("item"):
            link = it.findtext("link") or it.findtext("title")
            if link in seen:
                continue
            seen.add(link)
            items.append(it)
    clusters = []
    for it in items:
        title = clean_headline(it.findtext("title") or "")
        src = (it.findtext("source") or "").strip() or "?"
        tk = set(tokens(title))
        if len(tk) < 3:
            continue
        for c in clusters:
            shared = len(tk & c["tk"])
            if shared >= 3 and shared / max(1, min(len(tk), len(c["tk"]))) >= 0.5:
                c["sources"].add(src)
                c["tk"] |= tk
                c["titles"].append(title)
                break
        else:
            clusters.append({"title": title, "tk": set(tk), "sources": {src}, "titles": [title]})
    clusters = [c for c in clusters if len(c["sources"]) >= EVENT_MIN_OUTLETS]
    clusters.sort(key=lambda c: -len(c["sources"]))
    return clusters[:8]


def gather_candidates():
    cands = []  # (query, origin, headline, outlets)
    try:
        for c in event_clusters():
            n = len(c["sources"])
            cands.append((" ".join(c["title"].split()[:11]), f"event({n} outlets)", c["title"], n))
    except Exception as e:
        print(f"warn: event feed failed: {e}", file=sys.stderr)
    try:
        root = ET.fromstring(http(TRENDS))
        ns = {"ht": "https://trends.google.com/trending/rss"}
        for it in list(root.iter("item"))[:10]:
            topic = it.findtext("title") or ""
            news = it.find("ht:news_item/ht:news_item_title", ns)
            traffic = it.findtext("ht:approx_traffic", namespaces=ns) or ""
            cands.append((topic, f"trends({traffic})", (news.text if news is not None else "") or topic, 0))
    except Exception as e:
        print(f"warn: trends failed: {e}", file=sys.stderr)
    for name, url, n in NEWS_FEEDS:
        try:
            root = ET.fromstring(http(url))
            for it in list(root.iter("item"))[:n]:
                t = it.findtext("title") or ""
                if t:
                    h = clean_headline(t)
                    cands.append((" ".join(h.split()[:11]), name, h, 0))
        except Exception as e:
            print(f"warn: {name} failed: {e}", file=sys.stderr)
    ATOM = "{http://www.w3.org/2005/Atom}"
    for i, (name, url, n) in enumerate(REDDIT_RSS):
        try:
            if i:
                time.sleep(3)
            root = ET.fromstring(http(url))
            for e in list(root.iter(ATOM + "entry"))[:n]:
                t = e.findtext(ATOM + "title") or ""
                if t:
                    cands.append((" ".join(t.split()[:11]), name, t, 0))
        except Exception as e:
            print(f"warn: {name} failed: {e}", file=sys.stderr)
    try:
        for t in json.loads(http(BSKY_TRENDING)).get("topics", [])[:10]:
            if t.get("topic"):
                cands.append((t["topic"], "bluesky", t["topic"], 0))
    except Exception as e:
        print(f"warn: bluesky failed: {e}", file=sys.stderr)
    try:
        for l in json.loads(http(MASTO_LINKS))[:8]:
            h = clean_headline(l.get("title", ""))
            if h:
                cands.append((" ".join(h.split()[:11]), "mastodon", h, 0))
    except Exception as e:
        print(f"warn: mastodon failed: {e}", file=sys.stderr)
    out = []
    for q, origin, head, outlets in cands:
        tk = set(tokens(q))
        if not tk:
            continue
        for o in out:
            if len(tk & o["tk"]) / max(1, len(tk | o["tk"])) >= 0.4:
                o["origins"].append(origin)
                o["outlets"] = max(o["outlets"], outlets)
                break
        else:
            out.append({"query": q, "origins": [origin], "headline": head, "tk": tk, "outlets": outlets})
    return out[:MAX_CANDIDATES]


def _flat(url_or_search):
    try:
        r = subprocess.run([YTDLP, "--no-warnings", "--flat-playlist", "--print",
                            "%(id)s\t%(duration)s\t%(channel)s\t%(view_count)s\t%(title)s", url_or_search],
                           capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return []
    rows = []
    for line in r.stdout.splitlines():
        p = line.split("\t", 4)
        if len(p) == 5:
            rows.append({"id": p[0], "channel": p[2], "title": p[4]})
    return rows


def _flat_full(url):
    """Key-less flat listing with live status, duration (seconds) and views, for the stream runner."""
    try:
        r = subprocess.run([YTDLP, "--no-warnings", "--flat-playlist", "--playlist-end", "8", "--print",
                            "%(id)s\t%(duration)s\t%(channel)s\t%(view_count)s\t%(live_status)s\t%(title)s", url],
                           capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return []
    rows = []
    for line in r.stdout.splitlines():
        p = line.split("\t", 5)
        if len(p) == 6:
            try:
                dur = float(p[1])
            except ValueError:
                dur = None
            rows.append({"id": p[0], "dur": dur, "channel": p[2], "status": p[4], "title": p[5],
                         "views": int(p[3]) if p[3].isdigit() else 0})
    return rows


def yt_search_live_full(query):
    return _flat_full("https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query) + "&sp=EgJAAQ%253D%253D")


def yt_search(query):
    return _flat(f"ytsearch{RESULTS_PER_QUERY}:{query}")


def yt_search_live(query):
    """YouTube results page filtered to live streams (sp=EgJAAQ== is the 'Live' filter)."""
    return _flat("https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query) + "&sp=EgJAAQ%253D%253D")[:RESULTS_PER_QUERY]


def iso_dur(s):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s)
    d, h, mi, se = [int(x or 0) for x in m.groups()] if m else (0, 0, 0, 0)
    return d * 86400 + h * 3600 + mi * 60 + se


def api_videos(ids):
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit("YOUTUBE_API_KEY not set")
    info = {}
    ids = list(ids)
    for i in range(0, len(ids), 50):
        qs = urllib.parse.urlencode({"part": "snippet,statistics,contentDetails,liveStreamingDetails",
                                     "id": ",".join(ids[i:i + 50]), "key": key})
        d = json.loads(http("https://www.googleapis.com/youtube/v3/videos?" + qs, 30))
        for v in d.get("items", []):
            ls = v.get("liveStreamingDetails", {})
            info[v["id"]] = {
                "published": v["snippet"]["publishedAt"],
                "views": int(v["statistics"].get("viewCount", 0)),
                "channel": v["snippet"]["channelTitle"],
                "title": v["snippet"]["title"],
                "dur": iso_dur(v["contentDetails"].get("duration", "PT0S")),
                "live": v["snippet"].get("liveBroadcastContent", "none"),   # live | upcoming | none
                "viewers": int(ls["concurrentViewers"]) if ls.get("concurrentViewers") else None,
                "sched": ls.get("scheduledStartTime"),
            }
    return info


def age_hours(iso):
    t = time.mktime(time.strptime(iso[:19], "%Y-%m-%dT%H:%M:%S")) - time.timezone
    return max((time.time() - t) / 3600, 0)


GENERIC = set("news conference press briefing update live police sheriff office department county city state "
              "video full watch breaking says say man woman killed dead after crash shooting".split())


def relevant(title, ctx_text, need=2):
    """A candidate official video must share distinctive words with the story (place, name, event)."""
    ctx = {w for w in tokens(ctx_text) if w not in GENERIC or w in ("crash", "shooting")}
    t = {w for w in tokens(title)}
    distinctive = ctx & t
    return len(distinctive) >= need


def short_q(c):
    """A tight query (first distinctive words) finds the briefing better than a whole headline."""
    return " ".join(tokens(c["query"])[:5])


AGENCY = re.compile(r"\b((?:[A-Z][a-zA-Z.']+ ){1,2}(?:County )?(?:Sheriff's Office|Sheriff|Police Department|Police|Fire Department|Fire Rescue)"
                    r"|NTSB|FAA|FBI|ATF|DEA|National Weather Service)\b")


def agencies(c, vids):
    """Agency names mentioned in the headline or the hot video titles, e.g. 'Hillsborough County Sheriff'."""
    found = []
    for text in [c["headline"], c["query"]] + [v["title"] for v in vids[:8]]:
        for m in AGENCY.finditer(text):
            name = m.group(1).strip()
            if name.lower() not in [f.lower() for f in found]:
                found.append(name)
    return found[:2]


# Case-sensitive on purpose: real agency channels use proper names ("Tampa Police Department", "HCSOSheriff",
# "NTSBgov"); fan and entertainment channels ("Minh Luyen police", "Police Activity") do not.
OFFICIAL_CS = re.compile(r"(Sheriff|Police Department|Police Dept|Police|Fire Department|Fire Rescue|Fire & Rescue|Highway Patrol|"
                         r"State Patrol|NTSB|FAA|FBI|NASA|NOAA|NWS|NHC|USGS|CDC|FDA|DHS|DOJ|ATF|DEA|Coast Guard|"
                         r"Department of|National Weather Service|White House|[A-Z]{2,6}(?:PD|SO|FD|SD)\b)")
NOT_OFFICIAL_CS = re.compile(r"(Activity|Academy|Cadet|Recruit|Memorial|Foundation|Fan|Dash ?cam|Dispatch Audio|Scanner)", re.I)


def is_official_name(name):
    return bool(OFFICIAL_CS.search(name) and not NOT_OFFICIAL.search(name) and not NOT_OFFICIAL_CS.search(name))


def main():
    use_state = "--no-state" not in sys.argv
    as_json = "--json" in sys.argv
    if "--query" in sys.argv:
        q = sys.argv[sys.argv.index("--query") + 1]
        cands = [{"query": q, "origins": ["manual"], "headline": q, "tk": set(tokens(q)), "outlets": 0}]
    else:
        cands = gather_candidates()
    with ThreadPoolExecutor(max_workers=4) as ex:
        searches = list(ex.map(lambda c: yt_search(c["query"]), cands))
    info = api_videos({r["id"] for rows in searches for r in rows})

    def to_vids(rows):
        vids = []
        for r in rows:
            v = info.get(r["id"])
            if not v or v["live"] != "none":
                continue
            age = age_hours(v["published"])
            if age > MAX_VIDEO_AGE_H:
                continue
            vids.append({**v, "id": r["id"], "age_h": round(age, 1), "vph": round(v["views"] / max(age, 1.0))})
        vids.sort(key=lambda x: -x["vph"])
        return vids

    def find_official(vids, c=None):
        for v in vids:
            if is_official_name(v["channel"]) and v["age_h"] <= SOURCE_MAX_AGE_H and 120 <= v["dur"] <= SOURCE_MAX_MIN * 60 \
                    and (c is None or relevant(v["title"], c["headline"] + " " + c["query"])):
                return v
        return None

    def find_live(rows):
        for r in rows:
            v = info.get(r["id"])
            if v and v["live"] in ("live", "upcoming") and is_official_name(v["channel"]):
                return {**v, "id": r["id"]}
        return None

    def hot(vids):
        return bool(vids) and (vids[0]["vph"] >= ALERT_VPH or sum(1 for v in vids if v["vph"] >= HOT_VPH) >= N_HOT)

    first = [to_vids(rows) for rows in searches]
    # second pass for interesting topics: look for the briefing itself and for official live streams
    interesting = [c for c, v in zip(cands, first) if hot(v) or c["outlets"] >= LIVE_MIN_OUTLETS]
    extra, live_rows = {}, {}
    if interesting:
        with ThreadPoolExecutor(max_workers=4) as ex:
            need = [c for c, v in zip(cands, first) if c in interesting and not find_official(v, c)]
            for c, rows in zip(need, ex.map(lambda c: yt_search(short_q(c) + " press conference"), need)):
                extra[c["query"]] = list(rows)
            firsts = {c["query"]: v for c, v in zip(cands, first)}
            ag = [(c, a) for c in need for a in agencies(c, firsts[c["query"]])]
            for (c, a), rows in zip(ag, ex.map(lambda ca: yt_search(ca[1] + " news conference"), ag)):
                extra[c["query"]] += rows
            for c, rows in zip(interesting, ex.map(lambda c: yt_search_live(short_q(c) + " press conference"), interesting)):
                live_rows[c["query"]] = rows
        more = {r["id"] for rows in list(extra.values()) + list(live_rows.values()) for r in rows} - set(info)
        if more:
            info.update(api_videos(more))

    results = []
    for c, rows, vids in zip(cands, searches, first):
        official = find_official(vids, c) or (find_official(to_vids(extra[c["query"]]), c) if c["query"] in extra else None)
        live = find_live(rows) or find_live(live_rows.get(c["query"], []))
        text = c["headline"] + " " + c["query"] + " " + " ".join(v["title"] for v in vids[:5])
        flags = []
        if BLOCK.search(text):
            flags.append("BLOCKED:sensitive")
        if POLITICAL.search(text):
            flags.append("HOLD:political")
        if ALLEGATION.search(text):
            flags.append("allegation: attribute only")
        results.append({"query": c["query"], "headline": c["headline"], "origins": c["origins"], "outlets": c["outlets"],
                        "vmax": vids[0]["vph"] if vids else 0,
                        "n_hot": sum(1 for v in vids if v["vph"] >= HOT_VPH), "passes_gate": hot(vids),
                        "flags": flags, "official": official, "live": live, "top": vids[:3]})

    # a story is blocked if it shares top videos with a blocked story
    blocked_ids = {v["id"] for r in results if any(f.startswith("BLOCKED") for f in r["flags"]) for v in r["top"]}
    for r in results:
        if r["top"] and not any(f.startswith("BLOCKED") for f in r["flags"]) and {v["id"] for v in r["top"]} & blocked_ids:
            r["flags"].append("BLOCKED:same story as a sensitive item")

    state = json.load(open(STATE)) if os.path.exists(STATE) else {"alerted": {}}
    now = time.time()
    state["alerted"] = {k: t for k, t in state["alerted"].items() if now - t < 7 * 86400}
    fresh = lambda k: now - state["alerted"].get(k, 0) > REALERT_AFTER_H * 3600
    live_a, alerts, early, watch, blocked = [], [], [], [], []
    for r in sorted(results, key=lambda x: (-x["outlets"], -x["vmax"])):
        flags = r["flags"]
        is_blocked = any(f.startswith("BLOCKED") for f in flags)
        is_held = any(f.startswith("HOLD") for f in flags)
        story_hot = r["passes_gate"] or r["outlets"] >= LIVE_MIN_OUTLETS
        if is_blocked:
            if story_hot:
                blocked.append(r)
            continue
        if is_held:
            if story_hot:
                watch.append(r)
            continue
        if r["live"] and story_hot:
            r["key"] = "live:" + r["live"]["id"]
            if fresh(r["key"]):
                live_a.append(r)
                continue
        if r["official"] and r["passes_gate"]:
            r["key"] = r["official"]["id"]
            if fresh(r["key"]):
                alerts.append(r)
            continue
        if r["outlets"] >= EARLY_MIN_OUTLETS and not r["official"]:
            r["key"] = "early:" + hashlib.md5(" ".join(sorted(tokens(r["query"]))[:5]).encode()).hexdigest()[:10]
            if fresh(r["key"]) and len(early) < MAX_EARLY:
                early.append(r)
            continue
        if r["passes_gate"]:
            watch.append(r)
    if use_state:
        for r in live_a + alerts + early:
            state["alerted"][r["key"]] = now
        json.dump(state, open(STATE, "w"), indent=1)

    if as_json:
        print(json.dumps({"live": live_a, "alerts": alerts, "early": early, "watch": watch, "blocked": blocked,
                          "scanned": len(cands)}, indent=1, default=str))
        return

    def show(r, tag):
        t = r["top"][0] if r["top"] else None
        print(f"[{tag}] {r['query']}  | origins: {', '.join(r['origins'])}")
        print(f"   outlets in last 2h: {r['outlets'] or 'n/a'}; velocity: best {r['vmax']}/h, {r['n_hot']} videos >= {HOT_VPH}/h"
              + (f"; flags: {'; '.join(r['flags'])}" if r["flags"] else ""))
        if t:
            print(f"   top video: {t['channel']} | {t['title'][:80]} | {t['views']} views, {t['age_h']}h old, {t['vph']}/h | https://youtu.be/{t['id']}")
        if r.get("live"):
            lv = r["live"]
            when = f"live now, {lv['viewers']} watching" if lv["live"] == "live" else f"scheduled {lv['sched']}"
            print(f"   OFFICIAL LIVE: {lv['channel']} | {lv['title'][:80]} | {when} | https://www.youtube.com/watch?v={lv['id']}")
        o = r["official"]
        if o:
            print(f"   OFFICIAL SOURCE: {o['channel']} | {o['title'][:80]} | {o['dur'] // 60} min, {o['age_h']}h old, {o['views']} views | https://www.youtube.com/watch?v={o['id']}")
        elif not r.get("live"):
            print("   no official source video found (<=48h, 2-40 min)")

    print(f"scanned {len(cands)} topics; gate: best >= {ALERT_VPH}/h or {N_HOT}+ videos >= {HOT_VPH}/h; "
          f"event spike = {EVENT_MIN_OUTLETS}+ outlets in 2h")
    print(f"LIVE: {len(live_a)}  ALERTS: {len(alerts)}  EARLY: {len(early)}")
    for r in live_a:
        show(r, "LIVE")
    for r in alerts:
        show(r, "ALERT")
    for r in early:
        show(r, "EARLY")
    held = [r for r in watch if any(f.startswith("HOLD") for f in r["flags"])]
    watch = [r for r in watch if r not in held]
    print(f"WATCH (hot, no clippable official source): {len(watch)}")
    for r in watch[:6]:
        show(r, "WATCH")
    if held:
        print(f"HELD political ({len(held)}, not clipped unless William asks): "
              + "; ".join(f"{r['query'][:45]} ({r['vmax']}/h)" for r in held[:5]))
    if blocked:
        print(f"BLOCKED (hot but never clip): {len(blocked)}")
        for r in blocked[:4]:
            print(f"[BLOCKED] {r['query']} | best {r['vmax']}/h | {'; '.join(r['flags'])}")


if __name__ == "__main__":
    main()
