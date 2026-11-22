#!/usr/bin/env python3
"""GTA 6 guide scout: finds existing YouTube guides, groups them by TOPIC, proposes topics for William to approve.

  guide_scout.py scan [--offline] [--no-cache] [--max-queries N] [--only "query"] [--rebuild]
                                  run queries, filter, score, cluster into topics, update state, write
                                  out/guide_scout/YYYY-MM-DD.json + out/guide_scout/latest.md. No downloads, no LLM.
  guide_scout.py digest [--top N] [--dry] [--min-score S]
                                  print one `TGSEND {json}` line per proposed topic (value-only buttons
                                  guide_ok_<id> / guide_no_<id>). Marks them as sent unless --dry. Sends nothing itself.
  guide_scout.py callback VALUE   handle guide_ok_<id> / guide_no_<id> (sets approved / rejected, prints one line)
  guide_scout.py next [N] [--json]  approved, unbuilt topics in priority order: primary source, cross-check sources, flags
  guide_scout.py show [TOPICID]   topic table, or one topic in full
  guide_scout.py built TOPICID VIDEO_ID   mark a topic built
  guide_scout.py add-topic "name" --query "..." [--no-search]   William hands us a topic (approved), seeds a targeted search
  guide_scout.py status           counts per status, queue depth, days of queue, last scan, errors

State: guide_topics.json (statuses proposed/approved/rejected/built/stale). Tuning: guide_scout_config.json.
Cache: work/guide_scout_cache/. Every yt-dlp call goes through the local CONNECT proxy (cut_moment.start_proxy) and a shared
rate limiter with 429 backoff. Nothing is posted, sent or scheduled from here; stdout only.
"""
import argparse, csv, fcntl, glob, hashlib, json, math, os, re, subprocess, sys, threading, time, unicodedata
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CFG_PATH = os.path.join(HERE, "guide_scout_config.json")
STATE_PATH = os.environ.get("GUIDE_SCOUT_STATE", os.path.join(HERE, "guide_topics.json"))
CACHE = os.path.join(HERE, "work", "guide_scout_cache")
OUT = os.path.join(HERE, "out", "guide_scout")
LOG = os.path.join(OUT, "scan.log")
LOCK = STATE_PATH + ".lock"
NOW = lambda: time.time()


# ---------------------------------------------------------------- small utils
def load_cfg():
    return json.load(open(CFG_PATH))


def log(msg, err=False):
    os.makedirs(OUT, exist_ok=True)
    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {'ERROR ' if err else ''}{msg}"
    with open(LOG, "a") as f:
        f.write(line + "\n")
    if err:
        print(line, file=sys.stderr)


def atomic_write(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(text)
    os.replace(tmp, path)


def empty_state():
    return {"version": 1, "topics": {}, "videos": {}, "meta": {"last_scan": None, "errors": [], "last_stats": {}}}


def read_state():
    if not os.path.exists(STATE_PATH):
        return empty_state()
    try:
        st = json.load(open(STATE_PATH))
    except Exception as e:
        raise SystemExit(f"state unreadable ({e}); fix or restore {STATE_PATH}")
    for k, v in empty_state().items():
        st.setdefault(k, v)
    return st


@contextmanager
def locked_state():
    os.makedirs(os.path.dirname(LOCK) or ".", exist_ok=True)
    with open(LOCK, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        st = read_state()
        yield st
        atomic_write(STATE_PATH, json.dumps(st, indent=1, ensure_ascii=False))


def fmt_dur(s):
    s = int(s or 0)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def fmt_age(h):
    return f"{int(h)} h" if h < 48 else f"{h / 24:.1f} d"


def fmt_n(n):
    n = n or 0
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.0f}k" if n >= 1e4 else f"{n / 1e3:.1f}k" if n >= 1e3 else str(int(n))


# ---------------------------------------------------------------- yt-dlp access (proxy, rate limit, 429 backoff)
class Abort(Exception):
    pass


class Yt:
    def __init__(self, cfg):
        import cut_moment as cm
        self.cm = cm
        self.port = cm.start_proxy()
        self.net = cfg["net"]
        self.lock = threading.Lock()
        self.next_start = 0.0
        self.n429 = 0
        self.consec429 = 0
        self.calls = 0

    def run(self, args, timeout):
        n = self.net
        for attempt in range(n["retries"] + 1):
            with self.lock:
                wait = self.next_start - NOW()
                if wait > 0:
                    time.sleep(wait)
                self.next_start = NOW() + n["min_gap_s"]
            self.calls += 1
            try:
                r = subprocess.run([self.cm.YTDLP, "--proxy", f"http://127.0.0.1:{self.port}", "--no-warnings", *args],
                                   capture_output=True, text=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                log(f"timeout: {' '.join(args)[-90:]}", err=True)
                continue
            if "429" in r.stderr or "Too Many Requests" in r.stderr:
                self.n429 += 1
                self.consec429 += 1
                delay = n["backoff_s"] * (2 ** attempt)
                log(f"429, backing off {delay}s (consecutive {self.consec429})", err=True)
                if self.consec429 >= n["max_consecutive_429"]:
                    raise Abort("too many consecutive 429s")
                with self.lock:
                    self.next_start = max(self.next_start, NOW() + delay)
                continue
            self.consec429 = 0
            return r
        return None

    def search(self, query, order, cfg):
        sp = cfg["search_sp"].get(order, "")
        url = "https://www.youtube.com/results?search_query=" + quote_plus(query) + ("&sp=" + sp if sp else "")
        r = self.run(["--flat-playlist", "-j", "--playlist-end", str(cfg["per_query_results"]), url], self.net["search_timeout_s"])
        if r is None:
            raise RuntimeError("search failed after retries")
        out = []
        for line in r.stdout.splitlines():
            try:
                j = json.loads(line)
            except Exception:
                continue
            if j.get("id") and j.get("title"):
                out.append({"id": j["id"], "title": j["title"], "duration": j.get("duration"), "views": j.get("view_count")})
        if not out and r.returncode != 0:
            raise RuntimeError("search error: " + r.stderr.strip()[-160:])
        return out

    def detail(self, vid):
        r = self.run(["--skip-download", "-j", "https://www.youtube.com/watch?v=" + vid], self.net["detail_timeout_s"])
        if r is None or not r.stdout.strip():
            raise RuntimeError("detail failed: " + ((r.stderr.strip()[-160:]) if r else "retries"))
        return slim(json.loads(r.stdout.splitlines()[0]))


def slim(j):
    ac = j.get("automatic_captions") or {}
    sc = j.get("subtitles") or {}
    orig = [k for k in ac if k.endswith("-orig")]
    en_orig = any(k.startswith("en") for k in orig)
    en_sub = any(k.startswith("en") for k in sc)
    en_auto_plain = ("en" in ac) and not orig  # no other source-language track: 'en' is the spoken language
    ts = j.get("timestamp") or j.get("release_timestamp")
    if not ts and j.get("upload_date"):
        try:
            ts = datetime.strptime(j["upload_date"], "%Y%m%d").replace(tzinfo=timezone.utc).timestamp()
        except Exception:
            ts = None
    chapters = [{"start": c.get("start_time"), "end": c.get("end_time"), "title": c.get("title")} for c in (j.get("chapters") or [])]
    desc = (j.get("description") or "")
    return {"id": j["id"], "title": j.get("title"), "channel": j.get("channel") or j.get("uploader"), "duration": j.get("duration"),
            "views": j.get("view_count"), "likes": j.get("like_count"), "followers": j.get("channel_follower_count"),
            "ts": ts, "live": j.get("live_status") or ("is_live" if j.get("is_live") else None), "caps": bool(en_orig or en_sub or en_auto_plain),
            "caps_kind": "manual" if en_sub else "auto" if (en_orig or en_auto_plain) else "none",
            "w": j.get("width"), "h": j.get("height"), "chapters": chapters, "desc": desc[:2500], "age_limit": j.get("age_limit"),
            "availability": j.get("availability"), "fetched": NOW()}


# ---------------------------------------------------------------- caches
def cpath(kind, key):
    os.makedirs(CACHE, exist_ok=True)
    return os.path.join(CACHE, f"{kind}_{hashlib.md5(key.encode()).hexdigest()[:16] if kind == 'search' else key}.json")


def cache_get(kind, key, ttl_h, offline=False):
    p = cpath(kind, key)
    if not os.path.exists(p):
        return None
    try:
        d = json.load(open(p))
    except Exception:
        return None
    if offline or NOW() - d["ts"] <= ttl_h * 3600:
        return d["data"]
    return None


def cache_put(kind, key, data):
    atomic_write(cpath(kind, key), json.dumps({"ts": NOW(), "key": key, "data": data}))


# ---------------------------------------------------------------- text analysis
class Text:
    def __init__(self, cfg):
        self.cfg = cfg
        self.gta = re.compile(cfg["gta6_regex"], re.I)
        self.excl = re.compile(r"\b(" + "|".join(cfg["exclude_title"]) + r")\b", re.I)
        self.types = [(t, re.compile(rx, re.I)) for t, rx in cfg["types"]]
        self.round_rx = re.compile(cfg["roundup_title_regex"], re.I)
        self.glitch = re.compile(cfg["risk_glitch_regex"], re.I)
        self.spoil = re.compile(cfg["risk_spoiler_regex"], re.I)
        self.skipch = re.compile(cfg["skip_chapter_title_regex"], re.I)
        self.stop = set(cfg["stop_words"]) | set(cfg["brand_words"])
        self.mods = set(cfg["modifier_words"])
        self.alias = []
        self.ent_names = {}
        for e in cfg["entities"]:
            tok = "zz" + re.sub(r"[^a-z0-9]", "", e["name"].lower())[:24]
            self.ent_names[tok] = e["name"]
            for a in sorted(e["aliases"], key=len, reverse=True):
                self.alias.append((re.compile(r"(?<![a-z0-9])" + re.escape(a.lower()).replace("\\ ", r"\s+") + r"(?![a-z0-9])"), tok))

    def norm(self, s):
        s = unicodedata.normalize("NFKC", s or "").lower().replace("’", "'").replace("‘", "'")
        return self.gta.sub(" ", s)

    def words(self, s):
        s = self.norm(s)
        for rx, tok in self.alias:
            s = rx.sub(" " + tok + " ", s)
        out = []
        for w in re.findall(r"[a-z0-9]+(?:'[a-z]+)?", s):
            w = re.sub(r"'s?$", "", w)
            if w:
                out.append(w)
        return out

    @staticmethod
    def stem(w):
        return w[:-1] if len(w) > 4 and w.endswith("s") and not w.endswith("ss") else w

    def content(self, s):
        res = []
        for w in self.words(s):
            if w.startswith("zz") and w in self.ent_names:
                res.append(w)
                continue
            if w in self.stop or w.isdigit() or len(w) < 3 or self.stem(w) in self.stop:
                continue
            res.append(self.stem(w))
        return res

    def gta6(self, title):
        return bool(self.gta.search(title or ""))

    def vtype(self, text):
        t = self.norm(text)
        for name, rx in self.types:
            if rx.search(t):
                return name
        return None

    def family(self, vtype):
        return self.cfg["families"].get(vtype or "", "other")

    def is_roundup(self, title, dur):
        t = self.norm(title)
        return bool(self.round_rx.search(t)) or (dur or 0) >= self.cfg["roundup_min_duration_s"]

    def clean_title(self, title):
        t = unicodedata.normalize("NFKC", title or "")
        t = self.gta.sub(" ", t)
        t = re.sub(r"[^\x00-\x7f’]", " ", t)

        def brk(m):
            inner = m.group(1)
            toks = [w for w in self.words(inner) if w not in self.stop and not w.isdigit()]
            return f" ({inner.strip()})" if toks else " "
        t = re.sub(r"[\(\[]([^\)\]]*)[\)\]]", brk, t)
        t = re.sub(r"[*!?|~]+|\.{2,}", " ", t)
        t = re.sub(r"\s+", " ", t).strip(" -:,.&")
        t = re.sub(r"\b(in|on|at|from|of|for|to)\s*$", "", t, flags=re.I).strip(" -:,.")
        letters = [c for c in t if c.isalpha()]
        if letters and sum(c.isupper() for c in letters) / len(letters) > 0.6:
            t = re.sub(r"[A-Za-z']+", lambda m: m.group(0).capitalize(), t)
        return (t[:80] if t else title[:80]).strip()


# ---------------------------------------------------------------- video evaluation
def vid_metrics(rec, cfg):
    ts = rec.get("ts")
    age_h = (NOW() - ts) / 3600 if ts else None
    views = rec.get("views") or 0
    vph = views / max(age_h, cfg["vph_floor_hours"]) if age_h is not None else 0
    return age_h, vph


def stage1(tx, cfg, title, dur):
    if not tx.gta6(title):
        return "not_gta6"
    if dur is None:
        return "live_or_upcoming"
    if dur < cfg["min_duration_s"]:
        return "too_short"
    m = tx.excl.search(tx.norm(title) + " " + title.lower())
    if m:
        return "excluded_word:" + m.group(0).lower()
    if cfg["require_english"]:
        a = sum(c.isascii() for c in title) / max(1, len(title))
        if a < cfg["min_ascii_ratio"]:
            return "non_english"
    return None


def stage2(tx, cfg, rec):
    if rec.get("live") in ("is_live", "was_live", "is_upcoming", "post_live"):
        return "live"
    if rec.get("availability") not in (None, "public", "unlisted"):
        return "not_public"
    if rec.get("age_limit"):
        return "age_gated"
    age_h, vph = vid_metrics(rec, cfg)
    if age_h is None:
        return "no_age"
    if age_h > cfg["max_age_days"] * 24:
        return "too_old"
    views = rec.get("views") or 0
    if age_h < cfg["new_age_hours"]:
        ok = views >= cfg["min_views_new"]
    else:
        ok = views >= cfg["min_views"] or vph >= cfg["min_vph"]
    if not ok:
        return "low_views"
    t = tx.norm(rec["title"]) + " " + (rec["title"] or "").lower()
    if tx.excl.search(t):
        return "excluded_word"
    return None


# ---------------------------------------------------------------- scan: network phase
def run_scan_network(cfg, args, prior_videos):
    t0 = NOW()
    tx = Text(cfg)
    stats = {"queries_run": 0, "queries_cached": 0, "queries_failed": 0, "raw_hits": 0, "unique_hits": 0, "stage1_pass": 0,
             "detail_fetched": 0, "detail_cached": 0, "detail_failed": 0, "deferred": 0, "n429": 0, "dropped": {}}
    qlist = [(q["q"], q["hint"]) for q in cfg["queries"]]
    if args.only:
        qlist = [(args.only, "")]
    if args.max_queries:
        qlist = qlist[: args.max_queries]
    extra = getattr(args, "extra_queries", None) or []
    qlist += [(q, "") for q in extra]
    jobs = [(q, h, o) for q, h in qlist for o in cfg["orders"]]
    net = cfg["net"]
    yt = None if args.offline else Yt(cfg)
    hits = {}

    def do_search(job):
        q, h, o = job
        key = f"{q}|{o}|{cfg['per_query_results']}"
        ttl = net["cache_ttl_h"]
        d = None if args.no_cache else cache_get("search", key, ttl, offline=args.offline)
        if d is not None:
            return job, d, "cached"
        if args.offline:
            return job, [], "miss"
        if NOW() - t0 > net["scan_budget_s"] * 0.6:
            return job, None, "budget"
        try:
            d = yt.search(q, o, cfg)
            cache_put("search", key, d)
            return job, d, "run"
        except Abort:
            raise
        except Exception as e:
            log(f"query failed [{q} / {o}]: {e}", err=True)
            return job, None, "failed"

    aborted = False
    try:
        with ThreadPoolExecutor(max_workers=net["workers"] if not args.offline else 1) as ex:
            results = list(ex.map(do_search, jobs))
    except Abort as e:
        log(f"scan aborted during search: {e}", err=True)
        results, aborted = [], True
    for job, d, how in results:
        q, h, o = job
        if how == "cached":
            stats["queries_cached"] += 1
        elif how == "run":
            stats["queries_run"] += 1
        elif how in ("failed", "budget"):
            stats["queries_failed"] += 1
        for rank, e in enumerate(d or []):
            stats["raw_hits"] += 1
            h_ = hits.setdefault(e["id"], {"id": e["id"], "title": e["title"], "duration": e["duration"], "views": None, "appear": 0,
                                           "queries": set(), "best_rank": 999})
            h_["appear"] += 1
            h_["queries"].add(q)
            h_["best_rank"] = min(h_["best_rank"], rank)
            if e.get("views") is not None:
                h_["views"] = e["views"]
            if e.get("duration") is not None:
                h_["duration"] = e["duration"]
    stats["unique_hits"] = len(hits)

    # stage 1 on titles
    cand = []
    for h_ in hits.values():
        r = stage1(tx, cfg, h_["title"], h_["duration"])
        if r:
            stats["dropped"][r.split(":")[0]] = stats["dropped"].get(r.split(":")[0], 0) + 1
            continue
        cand.append(h_)
    stats["stage1_pass"] = len(cand)

    # detail fetch for the best candidates
    cand.sort(key=lambda h_: -(h_["appear"] * 10 + (6 if h_["best_rank"] < 10 else 0) + math.log10(1 + (h_["views"] or 0))))
    records = {}
    todo = []
    for h_ in cand:
        d = None if args.no_cache else cache_get("detail", h_["id"], net["detail_ttl_h"], offline=args.offline)
        if d is None and h_["id"] in prior_videos and not args.no_cache and not args.offline:
            pv = prior_videos[h_["id"]]
            if NOW() - pv.get("fetched", 0) <= net["detail_ttl_h"] * 3600:
                d = pv
        if d is not None:
            records[h_["id"]] = d
            stats["detail_cached"] += 1
        else:
            todo.append(h_)
    if args.offline:
        stats["deferred"] = len(todo)
        todo = []
    todo_run = todo[: net["max_detail"]]
    stats["deferred"] += len(todo) - len(todo_run)

    def do_detail(h_):
        if aborted or NOW() - t0 > net["scan_budget_s"]:
            return h_, None, "budget"
        try:
            d = yt.detail(h_["id"])
            cache_put("detail", h_["id"], d)
            return h_, d, "run"
        except Abort as e:
            log(f"scan aborted during detail: {e}", err=True)
            return h_, None, "abort"
        except Exception as e:
            log(f"detail failed [{h_['id']}]: {e}", err=True)
            return h_, None, "failed"

    if todo_run and yt:
        with ThreadPoolExecutor(max_workers=net["workers"]) as ex:
            for h_, d, how in ex.map(do_detail, todo_run):
                if how == "run":
                    records[h_["id"]] = d
                    stats["detail_fetched"] += 1
                elif how == "failed":
                    stats["detail_failed"] += 1
                else:
                    stats["deferred"] += 1
    for vid, rec in records.items():
        h_ = hits.get(vid)
        if h_:
            rec["appear"] = h_["appear"]
            rec["queries"] = sorted(h_["queries"])[:6]
            if h_["views"] and (rec.get("views") is None or (NOW() - rec.get("fetched", 0)) > 3600):
                rec["views"] = max(rec.get("views") or 0, h_["views"])
    stats["n429"] = yt.n429 if yt else 0
    stats["yt_calls"] = yt.calls if yt else 0
    stats["aborted"] = aborted
    stats["runtime_s"] = round(NOW() - t0)
    return records, stats


# ---------------------------------------------------------------- clustering and scoring
def source_score(src, cfg):
    s = cfg["source"]
    sc = s["cap_ok"] if src["captions"] else s["cap_none"]
    d = src["duration"] or 0
    if src["kind"] == "chapter":
        d = src["chap_len"]
        sc += 6 if 40 <= d <= 240 else 2 if 20 <= d < 40 else 0
    else:
        sc += 10 if s["good_min_s"] <= d <= s["good_max_s"] else 4 if d <= s["ok_max_s"] else -6 if d >= 30 else -8
    sc += 8 * math.log10(1 + (src["views"] or 0))
    sc += 6 * max(0, 1 - (src["age_h"] or 0) / 168)
    sc += s["hint"] if src["hint"] else 0
    sc += s["vertical"] if src.get("vertical") else 0
    sc += s["chapter_penalty"] if src["kind"] == "chapter" else 0
    return round(sc, 1)


class UF:
    def __init__(self):
        self.p = {}

    def f(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def u(self, a, b):
        self.p[self.f(a)] = self.f(b)


def build_items(tx, cfg, vids):
    """Videos -> items. Roundups with chapters become chapter items (children) and stay as pool sources."""
    items, roundups = {}, {}
    for vid, v in vids.items():
        age_h, vph = vid_metrics(v, cfg)
        title = v["title"]
        rt = tx.is_roundup(title, v.get("duration"))
        vt = tx.vtype(title) or tx.vtype(v.get("desc", "")[:200]) or None
        base = {"vid": vid, "channel": v.get("channel") or "?", "age_h": age_h or 0, "views": v.get("views") or 0, "vph": vph,
                "captions": v.get("caps", False), "caps_kind": v.get("caps_kind"), "duration": v.get("duration") or 0,
                "followers": v.get("followers") or 0, "vertical": bool(v.get("w") and v.get("h") and v["h"] > v["w"]),
                "title": title, "ts": v.get("ts")}
        chapters = [c for c in (v.get("chapters") or []) if c.get("title") and c.get("start") is not None]
        if not chapters and rt and v.get("desc"):
            lines = []
            for ln in v["desc"].splitlines():
                m = re.match(r"^\W*((?:\d{1,2}:)?\d{1,2}:\d{2})\W+\s*(.{3,80})$", ln.strip())
                if m:
                    parts = [int(x) for x in m.group(1).split(":")]
                    sec = parts[0] * 60 + parts[1] if len(parts) == 2 else parts[0] * 3600 + parts[1] * 60 + parts[2]
                    lines.append({"start": sec, "title": m.group(2).strip()})
            if len(lines) >= 3 and lines[0]["start"] <= 5:
                for i, c in enumerate(lines):
                    c["end"] = lines[i + 1]["start"] if i + 1 < len(lines) else (v.get("duration") or c["start"] + 60)
                chapters = lines
        if rt:
            roundups[vid] = dict(base, type=vt, text=tx.norm(title + " " + (v.get("desc") or "")[:1500]), chapters=len(chapters))
        if rt and chapters:
            n_ch = max(1, len(chapters))
            for c in chapters:
                clen = (c.get("end") or 0) - c["start"]
                ct = c["title"]
                ct = re.sub(r"^\W*(?:number|no\.?|tip|mistake|item|stop|part|step|secret)\s*#?\d+\s*[:.\-)]*\s*", "", ct.strip(), flags=re.I) or ct
                if tx.skipch.search(ct.strip().lower()) or clen < cfg["chapter_min_s"] or clen > cfg["chapter_max_s"]:
                    continue
                toks = tx.content(ct)
                if not toks:
                    continue
                ptoks_ = set(tx.content(title))
                if ptoks_ and len(set(toks) & ptoks_) / len(set(toks)) >= 0.6 and c["start"] <= 5:
                    continue  # chapter 0:00 that just repeats the video title (intro)
                own = tx.vtype(ct)
                typ = own or vt
                iid = f"{vid}@{int(c['start'])}"
                items[iid] = dict(base, id=iid, kind="chapter", title=ct, parent=vid, parent_title=title, type=typ, toks=toks, type_inherited=own is None,
                                  chap_start=int(c["start"]), chap_end=int(c.get("end") or c["start"] + clen), chap_len=clen,
                                  vph=vph * cfg["chapter_weight"] / math.sqrt(n_ch), views=base["views"], hint=False, risk_glitch=bool(tx.glitch.search(ct + " " + title)),
                                  risk_spoiler=bool(tx.spoil.search(ct)))
            continue
        if rt:
            continue  # roundup without chapters: pool source only (attached by mention)
        toks = tx.content(title)
        hint = any(h in tx.norm(title) for h in cfg["hint_words"])
        items[vid] = dict(base, id=vid, kind="single", type=vt, toks=toks, hint=hint, risk_glitch=bool(tx.glitch.search(title)),
                          risk_spoiler=bool(tx.spoil.search(title)), chap_len=0)
    return items, roundups


def cluster(tx, cfg, items):
    """Each item joins exactly ONE cluster: its most specific shared token (alias first, then lowest document frequency).
    No transitive merging, so a generic word cannot chain unrelated topics together."""
    n_items = max(1, len(items))
    max_df = max(cfg["df_max_abs"], int(n_items * cfg["df_max_frac"]))
    tok_items = {}
    for iid, it in items.items():
        for t in set(it["toks"]):
            tok_items.setdefault(t, set()).add(iid)
    spec = {}
    for t, ids in tok_items.items():
        chans = {items[i]["channel"] for i in ids}
        if t in tx.ent_names or (2 <= len(ids) <= max_df and len(chans) >= 2):
            spec[t] = ids
    groups = {}
    for iid, it in items.items():
        cands = [t for t in set(it["toks"]) if t in spec]
        if cands:
            order = list(tx.ent_names)
            best = sorted(cands, key=lambda t: (order.index(t) if t in tx.ent_names else 999, len(spec[t]), -len(t), t))[0]
            groups.setdefault(("e", best), []).append(iid)
        elif it["toks"]:
            groups.setdefault(("s", iid), []).append(iid)
        else:
            groups.setdefault(("g", tx.family(it["type"]), it["type"] or "tips"), []).append(iid)
    return groups, spec


def cluster_key_and_name(tx, cfg, members, items, spec):
    cnt = {}
    for m in members:
        for t in set(items[m]["toks"]):
            if t in spec:
                cnt[t] = cnt.get(t, 0) + 1
    ent_tokens = sorted(cnt, key=lambda t: (-(t in tx.ent_names), -cnt[t], -len(t), t))
    return ent_tokens, cnt


def build_topics(tx, cfg, items, roundups, built_index):
    groups, spec = cluster(tx, cfg, items)
    topics = []
    for gk, members in groups.items():
        mitems = [items[m] for m in members]
        if gk[0] == "e":
            _, cnt = cluster_key_and_name(tx, cfg, members, items, spec)
            ent = [gk[1]] + [t for t in sorted(cnt, key=lambda t: (-cnt[t], t)) if t != gk[1]][:2]
            key = "e:" + gk[1]
        elif gk[0] == "s":
            toks = sorted(set(mitems[0]["toks"]), key=lambda t: (-len(t), t))
            key = "s:" + "-".join(toks[:3])
            ent = toks[:3]
        else:
            ent, key = [], f"g:{gk[2]}:" + "-".join(sorted(_gen_mods(tx, mitems))[:1])
        # type vote
        tv = {}
        own_any = any(not it.get("type_inherited") and it["type"] for it in mitems)
        for it in mitems:
            if it["type"] and (not own_any or not it.get("type_inherited")):
                tv[it["type"]] = tv.get(it["type"], 0) + 1
        ttype = max(tv, key=lambda t: (tv[t], t)) if tv else (gk[2] if gk[0] == "g" else "tips")
        sources = []
        for it in mitems:
            s = {"id": it["id"], "vid": it["vid"], "kind": it["kind"], "title": it["title"], "channel": it["channel"], "duration": it["duration"],
                 "views": it["views"], "vph": round(it["vph"], 1), "age_h": round(it["age_h"], 1), "captions": it["captions"],
                 "caps_kind": it["caps_kind"], "hint": it["hint"], "vertical": it["vertical"], "chap_len": it["chap_len"],
                 "followers": it["followers"]}
            if it["kind"] == "chapter":
                s.update({"chap_start": it["chap_start"], "chap_end": it["chap_end"], "parent_title": it["parent_title"], "chapter_title": it["title"]})
            s["score"] = source_score(s, cfg)
            sources.append(s)
        # roundup mention (no chapter match): attach pool roundups whose text contains all entity tokens
        if gk[0] == "e" and ent:
            need = [t for t in ent[:2]]
            nment = 0
            for rid, r in roundups.items():
                if any(x["vid"] == rid for x in sources) or r["chapters"] or nment >= 3:
                    continue
                rtoks = set(tx.content(r["title"]))  # topic name must appear in the roundup TITLE
                if all(t in rtoks for t in need[:1]) and r["captions"] is not None:
                    nment += 1
                    s = {"id": rid, "vid": rid, "kind": "roundup", "title": r["title"], "channel": r["channel"], "duration": r["duration"],
                         "views": r["views"], "vph": round(r["vph"] * 0.1, 1), "age_h": round(r["age_h"], 1), "captions": r["captions"],
                         "caps_kind": r["caps_kind"], "hint": False, "vertical": r["vertical"], "chap_len": 0, "followers": r["followers"]}
                    s["score"] = source_score(s, cfg) - 8
                    sources.append(s)
        sources.sort(key=lambda s: -s["score"])
        # channel diversity: penalise repeats
        seen = {}
        for s in sources:
            c = s["channel"]
            if seen.get(c):
                s["score"] = round(s["score"] + cfg["source"]["dup_channel"], 1)
            seen[c] = seen.get(c, 0) + 1
        sources.sort(key=lambda s: -s["score"])
        topics.append({"key": key, "type": ttype, "entity": ent[:3], "members": sorted(members), "sources": sources,
                       "generic": gk[0] == "g", "own_type": own_any, "weak_type": all(i.get("type_inherited") for i in mitems)})
    return topics


def _gen_mods(tx, mitems):
    c = {}
    for it in mitems:
        for w in tx.words(it["title"]):
            if w in tx.mods:
                c[w] = c.get(w, 0) + 1
    return [w for w in sorted(c, key=lambda w: (-c[w], w))[:1]] or ["general"]


def name_topic(tx, cfg, t):
    label = cfg["type_labels"].get(t["type"], "guide")
    singles = [s for s in t["sources"] if s["kind"] == "single"]
    chaps = [s for s in t["sources"] if s["kind"] == "chapter"]
    # configured entity name wins
    for tok in t["entity"]:
        if tok in tx.ent_names:
            return tx.ent_names[tok]
    if t["generic"]:
        mods = _gen_mods(tx, [{"title": s["title"]} for s in t["sources"]])
        mod = "" if mods == ["general"] else mods[0].capitalize() + " "
        return f"{mod}{label} guides (general)".replace("  ", " ")
    pool = sorted(singles + chaps, key=lambda s: -s["score"])[:4]
    if pool:
        names = [(tx.clean_title(s["title"] if s["kind"] == "single" else s["chapter_title"]), s) for s in pool]
        full = [n for n, s in names if len(n.split()) >= 3]
        return (full or [names[0][0]])[0]
    return "Topic " + t["key"]


def score_topic(tx, cfg, t, items):
    sc = cfg["score"]
    srcs = t["sources"]
    mem = [items[m] for m in t["members"]]
    sum_vph = sum(i["vph"] for i in mem)
    chans = {i["channel"] for i in mem}
    newest_h = min((i["age_h"] for i in mem), default=999)
    comp = {}
    comp["demand"] = round(min(sc["demand_cap"], sc["demand_mult"] * math.log10(1 + sum_vph)), 1)
    comp["consensus"] = sc["consensus_per_channel"] * min(max(len(chans) - 1, 0), sc["consensus_cap"])
    comp["recency"] = round(sc["recency_max"] * max(0, 1 - newest_h / (cfg["stale_days"] * 24)), 1)
    comp["specific"] = 0 if t["generic"] else sc["specific_bonus"]
    comp["guideable"] = sc["hint_bonus"] if any(s["hint"] for s in srcs) or any(h in " ".join(s["title"].lower() for s in srcs) for h in ("location", "how to get", "where to find")) else 0
    ok = [s for s in srcs if s["captions"] and (s["kind"] == "chapter" or 20 <= (s["duration"] or 0) <= 1800)]
    comp["availability"] = sc["avail_ok"] if ok else sc["avail_none"]
    frac = lambda k: sum(1 for i in mem if i[k]) / max(1, len(mem))
    comp["weak_type"] = sc["weak_type"] if (t.get("weak_type") or not t.get("own_type")) and not t["generic"] else 0
    comp["risk_glitch"] = sc["risk_glitch"] if frac("risk_glitch") >= 0.34 else 0
    comp["risk_spoiler"] = sc["risk_spoiler"] if frac("risk_spoiler") >= 0.34 else 0
    comp["risk_single_unknown"] = sc["risk_single_unknown"] if len(chans) == 1 and max((i["followers"] for i in mem), default=0) < sc["min_followers_unknown"] else 0
    comp["type_bonus"] = sc.get("type_bonus", {}).get(t["type"], 0) if (t.get("own_type") or t["generic"]) else 0
    comp["generic_penalty"] = sc["roundup_only_generic"] if t["generic"] else 0
    flags = []
    if comp["risk_glitch"]:
        flags.append("glitch/exploit risk")
    if comp["risk_spoiler"]:
        flags.append("spoiler adjacency (check)")
    if comp["risk_single_unknown"]:
        flags.append("single unknown channel")
    if comp["availability"] < 0:
        flags.append("no_captions")
    return round(sum(comp.values()), 1), comp, flags, round(sum_vph, 1), len(chans), newest_h


# ---------------------------------------------------------------- built / posted detection
def posted_titles():
    titles = []
    for f in glob.glob(os.path.join(HERE, "out", "*.guide.json")):
        try:
            d = json.load(open(f))
            for k in ("yt_title", "title"):
                if d.get(k):
                    titles.append((d[k], os.path.basename(f)))
            if d.get("title_lines"):
                titles.append((" ".join(d["title_lines"]), os.path.basename(f)))
        except Exception:
            pass
    p = os.path.join(HERE, "out", "lane_tracker.csv")
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            if r.get("title"):
                titles.append((r["title"], "lane_tracker"))
    p = os.path.join(HERE, "..", "opusclip", "experiment-log.csv")
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            if (r.get("title") or "") and re.search(r"gta|grand theft", (r.get("title") or "") + (r.get("niche") or ""), re.I):
                titles.append((r["title"], "experiment-log"))
    return titles


def posted_match(tx, cfg, t, ptoks):
    """Match a topic against what we already built/posted: configured name regexes, or >=2 specific shared tokens
    (generic words like safe/code/store are ignored), or a shared alias entity."""
    for rx in cfg.get("built_name_regex", []):
        if re.search(rx, t["name"], re.I):
            return f"name matches built_name_regex '{rx}'"
    if t["generic"]:
        return None
    weak = set(cfg.get("posted_weak_tokens", []))
    ntoks = set(tx.content(t["name"])) | {e for e in t["entity"] if e in tx.ent_names}
    ntoks = {x for x in ntoks if x not in weak}
    if not ntoks:
        return None
    for title, src, toks in ptoks:
        common = ntoks & {x for x in toks if x not in weak}
        if len(common) >= 2:
            return f"{title} [{src}]"
    return None


# ---------------------------------------------------------------- scan: merge phase
def merge_and_cluster(cfg, records, stats, st, rebuild):
    tx = Text(cfg)
    stats["dropped2"] = {}
    kept = {}
    for vid, rec in records.items():
        r = stage2(tx, cfg, rec)
        if r:
            stats["dropped2"][r] = stats["dropped2"].get(r, 0) + 1
            continue
        kept[vid] = rec
    stats["kept"] = len(kept)
    vids = {} if rebuild else {k: v for k, v in st["videos"].items() if stage2(tx, cfg, v) is None}
    vids.update(kept)
    st["videos"] = vids
    for v in vids.values():
        v["last_seen"] = v.get("last_seen") or datetime.now().isoformat(timespec="minutes")
    for v in kept.values():
        v["last_seen"] = datetime.now().isoformat(timespec="minutes")
    items, roundups = build_items(tx, cfg, vids)
    topics = build_topics(tx, cfg, items, roundups, None)
    ptoks = [(t, s, set(tx.content(t))) for t, s in posted_titles()]
    now_iso = datetime.now().isoformat(timespec="minutes")
    old = st["topics"]
    used = set()
    result = {}
    manual = {k: v for k, v in old.items() if v.get("manual")}
    for t in topics:
        t["name"] = name_topic(tx, cfg, t)
        t["score"], t["components"], t["flags"], t["sum_vph"], t["n_channels"], t["newest_h"] = score_topic(tx, cfg, t, items)
        # match to existing topic: by key, then by member overlap
        tid = next((k for k, v in old.items() if v.get("key") == t["key"] and k not in used), None)
        if not tid:
            best, bo = None, 0
            ms = set(t["members"])
            for k, v in old.items():
                if k in used:
                    continue
                ov = len(ms & set(v.get("members", []))) / max(1, min(len(ms), len(v.get("members", [1]))))
                if ov > bo:
                    best, bo = k, ov
            if bo >= 0.5:
                tid = best
        if not tid:
            tid = "t" + hashlib.md5(t["key"].encode()).hexdigest()[:7]
        used.add(tid)
        prev = old.get(tid, {})
        status = prev.get("status", "proposed")
        if prev.get("auto_built"):
            status = "proposed"  # re-evaluate heuristic matches every scan
        t.update({"id": tid, "status": status, "first_seen": prev.get("first_seen", now_iso), "last_seen": now_iso,
                  "approved_at": prev.get("approved_at"), "auto_built": False, "built_video": prev.get("built_video"), "digested_at": prev.get("digested_at"),
                  "note": prev.get("note"), "manual": prev.get("manual", False)})
        if prev.get("status") in ("approved", "built", "rejected") and prev.get("name") and prev["status"] != "proposed":
            t["name"] = prev["name"] if prev.get("name_locked") else t["name"]
        pm = posted_match(tx, cfg, t, ptoks) if status in ("proposed", "stale") else None
        if pm:
            t["status"], t["note"], t["auto_built"] = "built", "already posted/built, matched: " + pm, True
        elif status == "proposed" and t["newest_h"] > cfg["stale_days"] * 24:
            t["status"] = "stale"
        elif status == "stale" and t["newest_h"] <= cfg["stale_days"] * 24:
            t["status"] = "proposed"
        result[tid] = t
    # carry over topics that no longer cluster (approved/built/rejected/manual stay; others age out)
    for k, v in old.items():
        if k in result:
            continue
        if v.get("status") in ("approved", "built", "rejected") or v.get("manual"):
            result[k] = v
        elif v.get("status") == "proposed":
            v["status"] = "stale"
            result[k] = v if v.get("score", 0) >= cfg["store_min_score"] else None
            if result[k] is None:
                del result[k]
    # store only worthwhile topics
    out = {}
    for k, v in result.items():
        if v.get("status") in ("approved", "built", "rejected") or v.get("manual") or v.get("score", 0) >= cfg["store_min_score"]:
            v.pop("generic_flag", None)
            out[k] = {kk: vv for kk, vv in v.items()}
    st["topics"] = out
    return out, tx


def ensure_seed_built(st, cfg):
    """First built topic: Paul Walker's Eclipse (source 0KkxxY3iJjQ)."""
    tx = Text(cfg)
    tok = next((t for t, n in tx.ent_names.items() if n.startswith("Paul Walker")), None)
    if not tok:
        return
    key = "e:" + tok
    for v in st["topics"].values():
        if v.get("key") == key:
            if v.get("status") == "proposed":
                v.update(status="built", built_video="0KkxxY3iJjQ", note="built 2026-11-21 (Rodwenn source 0KkxxY3iJjQ, out/0KkxxY3iJjQ.guide.json)")
            return
    tid = "t" + hashlib.md5(key.encode()).hexdigest()[:7]
    st["topics"][tid] = {"id": tid, "key": key, "name": tx.ent_names[tok], "type": "car", "entity": [tok], "status": "built", "score": 0,
                         "components": {}, "flags": [], "members": ["0KkxxY3iJjQ"], "built_video": "0KkxxY3iJjQ",
                         "built_at": "2026-11-21", "first_seen": "2026-11-21", "last_seen": "2026-11-21", "name_locked": True,
                         "note": "built 2026-11-21 (Rodwenn source 0KkxxY3iJjQ, out/0KkxxY3iJjQ.guide.json)",
                         "sources": [{"id": "0KkxxY3iJjQ", "vid": "0KkxxY3iJjQ", "kind": "single", "title": "Where To Find PAUL WALKER'S ECLIPSE In GTA 6 (Secret Car)",
                                      "channel": "Rodwenn", "duration": 90, "views": 643, "vph": 0, "age_h": 0, "captions": True, "score": 0, "hint": True}]}


# ---------------------------------------------------------------- output
def src_line(s):
    base = f"{s['channel']}, {fmt_dur(s['duration'])}, {fmt_n(s['views'])} views, {fmt_age(s['age_h'])} old"
    if s["kind"] == "chapter":
        return f"{s['channel']}: chapter '{s.get('chapter_title', '')[:40]}' {fmt_dur(s['chap_start'])}-{fmt_dur(s['chap_end'])} of a {fmt_dur(s['duration'])} roundup, {fmt_n(s['views'])} views, {fmt_age(s['age_h'])} old"
    if s["kind"] == "roundup":
        return f"{s['channel']} roundup ({fmt_dur(s['duration'])}, {fmt_n(s['views'])} views, mentions it, no chapter)"
    return base


def url(vid, start=None):
    return f"https://youtu.be/{vid}" + (f"?t={int(start)}" if start else "")


def digest_message(cfg, t):
    label = cfg["type_labels"].get(t["type"], t["type"])
    c = t["components"]
    srcs = t["sources"][:2]
    lines = [f"GTA 6 guide topic: {t['name']}", f"Type: {label} | score {t['score']} (demand {c.get('demand')}, consensus {c.get('consensus')}, recency {c.get('recency')})",
             f"Demand: {t['sum_vph']:.0f} views/hour across {len(t['members'])} item(s), {t['n_channels']} independent channel(s)", "Best sources:"]
    for s in srcs:
        lines.append(f"- {src_line(s)}" + ("" if s["captions"] else " [NO CAPTIONS]"))
    if srcs:
        lines.append("Link: " + url(srcs[0]["vid"], srcs[0].get("chap_start")))
    lines.append("Would cover: " + cfg["covers"].get(t["type"], cfg["covers"]["tips"]))
    if t.get("flags"):
        lines.append("Flags: " + "; ".join(t["flags"]))
    return {"text": "\n".join(lines), "buttons": [[{"label": "Approve topic", "value": f"guide_ok_{t['id']}"}, {"label": "Skip", "value": f"guide_no_{t['id']}"}]]}


def write_outputs(cfg, st, stats, topics):
    os.makedirs(OUT, exist_ok=True)
    day = datetime.now().strftime("%Y-%m-%d")
    ranked = sorted(topics.values(), key=lambda t: -t.get("score", 0))
    brief = []
    for t in ranked:
        brief.append({k: t.get(k) for k in ("id", "name", "status", "type", "score", "components", "flags", "n_channels", "sum_vph", "key")} |
                     {"sources": [{k: s.get(k) for k in ("id", "kind", "channel", "title", "duration", "views", "age_h", "captions", "score", "chap_start", "chap_end")} for s in t.get("sources", [])[:5]]})
    atomic_write(os.path.join(OUT, f"{day}.json"), json.dumps({"date": day, "stats": stats, "topics": brief}, indent=1, ensure_ascii=False))
    md = [f"# GTA 6 guide scout digest {datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
          f"Scan: {stats.get('queries_run', 0)} queries run ({stats.get('queries_cached', 0)} cached), {stats.get('unique_hits', 0)} unique hits, "
          f"{stats.get('stage1_pass', 0)} passed title filter, {stats.get('kept', 0)} kept, {len(topics)} topics, {stats.get('n429', 0)} 429s, {stats.get('runtime_s', 0)} s", ""]
    for status in ("proposed", "approved", "built", "stale", "rejected"):
        lst = [t for t in ranked if t.get("status") == status]
        if not lst:
            continue
        md.append(f"## {status} ({len(lst)})")
        for t in lst[:25]:
            c = t.get("components", {})
            top = t["sources"][0] if t.get("sources") else None
            md.append(f"- `{t['id']}` **{t['name']}** [{cfg['type_labels'].get(t.get('type'), t.get('type'))}] score {t.get('score')} "
                      f"(dem {c.get('demand')}, cons {c.get('consensus')}, rec {c.get('recency')}, spec {c.get('specific')}, hint {c.get('guideable')}, "
                      f"avail {c.get('availability')}, risk {sum(v for k, v in c.items() if k.startswith('risk') or k == 'generic_penalty')}) "
                      f"{t.get('n_channels', '?')} ch, {t.get('sum_vph', 0):.0f} vph" + (f" | flags: {'; '.join(t['flags'])}" if t.get("flags") else ""))
            if top:
                md.append(f"  - top source: {src_line(top)} {url(top['vid'], top.get('chap_start'))}")
        md.append("")
    atomic_write(os.path.join(OUT, "latest.md"), "\n".join(md))


# ---------------------------------------------------------------- commands
def cmd_scan(args):
    cfg = load_cfg()
    os.makedirs(OUT, exist_ok=True)
    st0 = read_state()
    log("scan start" + (" (offline)" if args.offline else ""))
    records, stats = run_scan_network(cfg, args, st0["videos"])
    with locked_state() as st:
        topics, tx = merge_and_cluster(cfg, records, stats, st, args.rebuild or args.offline)
        ensure_seed_built(st, cfg)
        topics = st["topics"]
        st["meta"]["last_scan"] = datetime.now().isoformat(timespec="seconds")
        st["meta"]["last_stats"] = stats
        errs = []
        if os.path.exists(LOG):
            errs = [l.strip() for l in open(LOG).read().splitlines()[-400:] if " ERROR " in l][-8:]
        st["meta"]["errors"] = errs
        write_outputs(cfg, st, stats, topics)
    log(f"scan done: {json.dumps({k: v for k, v in stats.items() if k not in ('dropped', 'dropped2')})}")
    print(f"scan done in {stats['runtime_s']}s: queries run {stats['queries_run']} (+{stats['queries_cached']} cached, {stats['queries_failed']} failed), "
          f"unique hits {stats['unique_hits']}, title-filter pass {stats['stage1_pass']}, detail fetched {stats['detail_fetched']} (+{stats['detail_cached']} cached, "
          f"{stats['deferred']} deferred), kept {stats['kept']}, topics stored {len(topics)}, 429s {stats['n429']}")
    print("dropped stage1:", stats["dropped"], "| stage2:", stats["dropped2"])
    print(f"digest: {os.path.join(OUT, 'latest.md')}")


def prop_list(st, cfg, min_score=None, include_sent=False):
    ms = cfg["propose_min_score"] if min_score is None else min_score
    out = []
    for t in st["topics"].values():
        if t.get("status") != "proposed" or t.get("score", 0) < ms:
            continue
        d = t.get("digested_at")
        if d and not include_sent and (datetime.now() - datetime.fromisoformat(d)).days < cfg["resend_days"]:
            continue
        out.append(t)
    out.sort(key=lambda t: -t["score"])
    return out


def cmd_digest(args):
    cfg = load_cfg()
    if args.dry:
        st = read_state()
        lst = prop_list(st, cfg, args.min_score, include_sent=args.all)[: args.top]
        for t in lst:
            print("TGSEND " + json.dumps(digest_message(cfg, t), ensure_ascii=False))
        return
    with locked_state() as st:
        lst = prop_list(st, cfg, args.min_score, include_sent=args.all)[: args.top]
        for t in lst:
            print("TGSEND " + json.dumps(digest_message(cfg, t), ensure_ascii=False))
            st["topics"][t["id"]]["digested_at"] = datetime.now().isoformat(timespec="seconds")


def find_topic(st, tid):
    if tid in st["topics"]:
        return tid
    c = [k for k in st["topics"] if k.startswith(tid)]
    return c[0] if len(c) == 1 else None


def queue_stats(st, cfg):
    depth = sum(1 for t in st["topics"].values() if t.get("status") == "approved")
    lo, hi = cfg["queue_per_day"]
    return depth, depth / hi, depth / lo


def cmd_callback(args):
    cfg = load_cfg()
    m = re.match(r"^(?:callback_data:\s*)?guide_(ok|no)_(\w+)$", args.value.strip())
    if not m:
        print(f"unrecognized callback value: {args.value}")
        sys.exit(1)
    with locked_state() as st:
        tid = find_topic(st, m.group(2))
        if not tid:
            print(f"unknown topic id {m.group(2)}")
            sys.exit(1)
        t = st["topics"][tid]
        if t["status"] == "built":
            print(f"topic {tid} '{t['name']}' is already built; no change")
            return
        if m.group(1) == "ok":
            t["status"], t["approved_at"] = "approved", datetime.now().isoformat(timespec="seconds")
            depth, dlo, dhi = queue_stats(st, cfg)
            p = t["sources"][0] if t.get("sources") else None
            print(f"APPROVED {tid} '{t['name']}'" + (f", primary source {p['channel']} {p['vid']}" if p else "") + f". Approved queue: {depth} guide(s), about {dlo:.1f}-{dhi:.1f} days at {cfg['queue_per_day'][0]}-{cfg['queue_per_day'][1]}/day.")
        else:
            t["status"] = "rejected"
            print(f"REJECTED {tid} '{t['name']}'. It will not be proposed again.")


def flags_for(s):
    f = ["check frames: facecam, watermark, clean first 7 s"]
    if not s["captions"]:
        f.append("NO CAPTIONS (no script source; need another source or manual transcription)")
    if s.get("vertical"):
        f.append("vertical source (letterbox look needs 16:9)")
    if s["kind"] == "chapter":
        f.append(f"use chapter {fmt_dur(s['chap_start'])}-{fmt_dur(s['chap_end'])} of the roundup")
    if s["kind"] == "roundup":
        f.append("roundup without chapters: find the item in the video")
    return f


def cmd_next(args):
    cfg = load_cfg()
    st = read_state()
    lst = sorted([t for t in st["topics"].values() if t.get("status") == "approved"], key=lambda t: (not t.get("manual"), -t.get("score", 0)))[: args.n]
    if not lst:
        print("no approved, unbuilt topics")
        return
    out = []
    for i, t in enumerate(lst, 1):
        srcs = t.get("sources", [])
        prim = srcs[0] if srcs else None
        cross = []
        seen = {prim["channel"]} if prim else set()
        for s in srcs[1:]:
            if s["channel"] in seen and len(cross) >= 1:
                continue
            seen.add(s["channel"])
            cross.append(s)
            if len(cross) == 3:
                break
        rec = {"n": i, "id": t["id"], "name": t["name"], "score": t.get("score"), "type": t.get("type"),
               "primary": prim and {"video_id": prim["vid"], "channel": prim["channel"], "kind": prim["kind"], "url": url(prim["vid"], prim.get("chap_start")), "captions": prim["captions"],
                                    "duration": prim["duration"], "views": prim["views"], "flags": flags_for(prim)},
               "cross_check": [{"video_id": s["vid"], "channel": s["channel"], "kind": s["kind"], "captions": s["captions"], "url": url(s["vid"], s.get("chap_start"))} for s in cross]}
        out.append(rec)
    if args.json:
        print(json.dumps(out, indent=1))
        return
    for r in out:
        print(f"{r['n']}. [{r['id']}] {r['name']} (score {r['score']}, {cfg['type_labels'].get(r['type'], r['type'])})")
        p = r["primary"]
        if p:
            print(f"   PRIMARY {p['video_id']} {p['channel']} {fmt_dur(p['duration'])} {fmt_n(p['views'])} views, captions: {'yes' if p['captions'] else 'NO'}  {p['url']}")
            for f in p["flags"]:
                print(f"     - {f}")
        print("   CROSS-CHECK: " + (", ".join(f"{c['video_id']} ({c['channel']}{', ' + c['kind'] if c['kind'] != 'single' else ''}, captions {'yes' if c['captions'] else 'no'})" for c in r["cross_check"]) or "none yet (single source: soften unverifiable claims)"))


def cmd_show(args):
    cfg = load_cfg()
    st = read_state()
    if not args.id:
        rows = sorted(st["topics"].values(), key=lambda t: -t.get("score", 0))[:40]
        for t in rows:
            print(f"{t['id']:9} {t.get('status', '?'):9} {t.get('score', 0):6} {t['name'][:60]}")
        return
    tid = find_topic(st, args.id)
    if not tid:
        print("unknown topic")
        sys.exit(1)
    t = st["topics"][tid]
    print(f"{tid} '{t['name']}' status={t['status']} type={t.get('type')} score={t.get('score')} key={t.get('key')}")
    print("components:", json.dumps(t.get("components")), "flags:", t.get("flags"), "note:", t.get("note"))
    for s in t.get("sources", []):
        print(f" - {s['score']:6} {s['kind']:8} {s['vid']} {src_line(s)} captions={s['captions']} | {s['title'][:70]}")


def cmd_built(args):
    with locked_state() as st:
        tid = find_topic(st, args.id)
        if not tid:
            print("unknown topic")
            sys.exit(1)
        t = st["topics"][tid]
        t["status"], t["built_video"], t["built_at"] = "built", args.video_id, datetime.now().isoformat(timespec="minutes")
        print(f"built {tid} '{t['name']}' with {args.video_id}")


def cmd_add_topic(args):
    cfg = load_cfg()
    tx = Text(cfg)
    toks = tx.content(args.name)
    key = "m:" + "-".join(sorted(toks)[:4])
    tid = "m" + hashlib.md5(key.encode()).hexdigest()[:7]
    ex = None
    if not args.no_search:
        class A:  # run the targeted search and merge into the pool
            offline = False; no_cache = False; max_queries = None; only = None; rebuild = False
            extra_queries = [args.query]
        a = A()
        a.only = args.query
        st0 = read_state()
        records, stats = run_scan_network(cfg, a, st0["videos"])
        print(f"seed search: {stats['unique_hits']} hits, {stats['stage1_pass']} pass title filter, {stats['detail_fetched']} fetched")
    else:
        records = {}
    with locked_state() as st:
        # merge the new videos into state (stage 2 filter), then attach to the manual topic by token overlap
        kept = {k: v for k, v in records.items() if stage2(tx, cfg, v) is None}
        for v in kept.values():
            v["last_seen"] = datetime.now().isoformat(timespec="minutes")
        st["videos"].update(kept)
        want = set(toks)
        items, roundups = build_items(tx, cfg, st["videos"])
        members = [i for i, it in items.items() if want and len(want & set(it["toks"])) / len(want) >= 0.6]
        srcs = []
        for m in members:
            it = items[m]
            s = {"id": m, "vid": it["vid"], "kind": it["kind"], "title": it["title"], "channel": it["channel"], "duration": it["duration"], "views": it["views"],
                 "vph": round(it["vph"], 1), "age_h": round(it["age_h"], 1), "captions": it["captions"], "caps_kind": it["caps_kind"], "hint": it["hint"],
                 "vertical": it["vertical"], "chap_len": it["chap_len"], "followers": it["followers"]}
            if it["kind"] == "chapter":
                s.update({"chap_start": it["chap_start"], "chap_end": it["chap_end"], "parent_title": it["parent_title"], "chapter_title": it["title"]})
            s["score"] = source_score(s, cfg)
            srcs.append(s)
        srcs.sort(key=lambda s: -s["score"])
        prev = st["topics"].get(tid, {})
        st["topics"][tid] = {"id": tid, "key": key, "name": args.name, "name_locked": True, "type": tx.vtype(args.name) or "tips", "entity": toks, "status": prev.get("status", "approved"),
                             "approved_at": prev.get("approved_at") or datetime.now().isoformat(timespec="seconds"), "manual": True, "query": args.query,
                             "score": 100, "components": {"manual": 100}, "flags": [], "members": members, "sources": srcs, "first_seen": prev.get("first_seen", datetime.now().isoformat(timespec="minutes")),
                             "last_seen": datetime.now().isoformat(timespec="minutes"), "n_channels": len({s['channel'] for s in srcs}), "sum_vph": round(sum(s["vph"] for s in srcs), 1)}
        print(f"topic {tid} '{args.name}' added as APPROVED (William's request), {len(srcs)} candidate source(s)")


def cmd_status(args):
    cfg = load_cfg()
    st = read_state()
    cnt = {}
    for t in st["topics"].values():
        cnt[t.get("status", "?")] = cnt.get(t.get("status", "?"), 0) + 1
    depth, dlo, dhi = queue_stats(st, cfg)
    m = st["meta"]
    print("topics by status:", json.dumps(cnt))
    print(f"queue depth: {depth} approved unbuilt guide(s) = {dlo:.1f}-{dhi:.1f} days at {cfg['queue_per_day'][0]}-{cfg['queue_per_day'][1]} guides/day (target {cfg['queue_per_day'][0]}-{cfg['queue_per_day'][1]}/day)")
    print(f"proposed and awaiting a digest: {len(prop_list(st, cfg))} (min score {cfg['propose_min_score']})")
    print("last scan:", m.get("last_scan"), "| videos tracked:", len(st["videos"]))
    ls = m.get("last_stats") or {}
    if ls:
        print("last scan stats:", json.dumps({k: v for k, v in ls.items() if k not in ('dropped', 'dropped2')}))
    errs = m.get("errors") or []
    print(f"recent errors ({len(errs)}):")
    for e in errs:
        print("  " + e[:200])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("scan")
    a.add_argument("--offline", action="store_true", help="use caches only, no network (for tuning)")
    a.add_argument("--no-cache", action="store_true")
    a.add_argument("--max-queries", type=int)
    a.add_argument("--only")
    a.add_argument("--rebuild", action="store_true", help="drop tracked videos first (topic statuses are kept)")
    a.set_defaults(f=cmd_scan)
    a = sp.add_parser("digest")
    a.add_argument("--top", type=int, default=8)
    a.add_argument("--dry", action="store_true", help="do not mark topics as sent")
    a.add_argument("--all", action="store_true", help="include topics already sent in the last resend_days")
    a.add_argument("--min-score", type=float)
    a.set_defaults(f=cmd_digest)
    a = sp.add_parser("callback")
    a.add_argument("value")
    a.set_defaults(f=cmd_callback)
    a = sp.add_parser("next")
    a.add_argument("n", nargs="?", type=int, default=5)
    a.add_argument("--json", action="store_true")
    a.set_defaults(f=cmd_next)
    a = sp.add_parser("show")
    a.add_argument("id", nargs="?")
    a.set_defaults(f=cmd_show)
    a = sp.add_parser("built")
    a.add_argument("id")
    a.add_argument("video_id")
    a.set_defaults(f=cmd_built)
    a = sp.add_parser("add-topic")
    a.add_argument("name")
    a.add_argument("--query", required=True)
    a.add_argument("--no-search", action="store_true")
    a.set_defaults(f=cmd_add_topic)
    a = sp.add_parser("status")
    a.set_defaults(f=cmd_status)
    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
