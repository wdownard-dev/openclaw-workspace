#!/usr/bin/env python3
"""GTA 6 keyword/channel discovery watcher. Qualifying videos ENTER THE FINISHED-CLIP QUEUE (clip_queue.py) instead of producing alert text; nothing
is posted or sent from here. Prints nothing when there is nothing new (only scan-failure errors).
Uses yt-dlp YouTube search sorted by upload date (no API key/quota), like watch.py. Keywords: gta6_keywords.json.

  gta6_discovery.py             one rotating batch of queries (cursor in discovery_state.json)
  gta6_discovery.py --dry-run   run + print alerts but do not write state
  gta6_discovery.py --digest    weekly top-10 channel ranking (output + velocity)
  gta6_discovery.py --batch N   override batch size    --all  run every query (slow)
Status CLI: set_status.py <channel_id> approved|info_only|ignored   Statuses: new/candidate_alerted/approved/info_only/ignored
"""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"
KW = os.path.join(HERE, "gta6_keywords.json")
STATE = os.path.join(HERE, "discovery_state.json")
CANDS = os.path.join(HERE, "candidates.json")
ET = ZoneInfo("America/New_York")
MAX_CHANNEL_ALERTS = 5
GTA = re.compile(r"\bgta\s*(6|vi)\b|\bgta6\b|grand theft auto\s*(6|vi)\b|\bgtavi\b", re.I)
GTA_ADIN = re.compile(GTA.pattern + r"|\bgta\s*rp\b|\bgta\s*5?\s*rp\b|\bnopixel\b|\brp\b", re.I)
SPOILER = re.compile(r"\bending\b|spoiler|leak|all cutscenes|full movie|final mission|\bcredits\b", re.I)
TYPES = [("walkthrough", r"walkthrough|part \d+|episode|no commentary|full game|100%|completion|playthrough|let'?s play"),
         ("guide", r"guide|how to|tips|tutorial|explained|everything you need|things to do|best way|unlock|cheats|codes|easter egg|secret|collectible|locations?|best (weapon|car|settings)"),
         ("gameplay", r"gameplay|first (hour|\d+ hours?)|opening|prologue|mission|heist|story mode|free roam|vs\b|comparison")]


def run(cmd, timeout=90):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def load_json(p, default):
    try:
        return json.load(open(p))
    except Exception:  # noqa: BLE001
        return default


def approved_ids(state):
    ids = {c["channel_id"] for c in load_json(CANDS, {"candidates": []})["candidates"] if c.get("approved") and c.get("channel_id")}
    ids |= {k for k, v in state["channels"].items() if v.get("status") == "approved"}
    return ids


def launch_mode(cfg):
    """Launch-window settings (config launch_mode) when now is inside start..end, else None."""
    from datetime import datetime
    lm = cfg.get("launch_mode")
    if not lm:
        return None
    try:
        if datetime.fromisoformat(lm["start"]).timestamp() <= time.time() <= datetime.fromisoformat(lm["end"]).timestamp():
            return lm
    except Exception:  # noqa: BLE001
        pass
    return None


def build_queries(cfg):
    qs = []
    for g, spec in cfg["groups"].items():
        for kw in spec["keywords"]:
            qs.append((g, f"GTA 6 {kw}"))
            if spec.get("also_vi"):
                qs.append((g, f"GTA VI {kw}"))
    return qs


def search(q, n=12):
    """Newest-first YouTube search (sp=CAI%3D). Flat entries: id, title, channel, views, duration. Raises on failure."""
    url = "https://www.youtube.com/results?search_query=" + q.replace(" ", "+").replace("'", "%27").replace("%", "%25") + "&sp=CAI%253D"
    last = None
    for attempt in range(3):
        r = run([YTDLP, "--no-warnings", "--flat-playlist", "-J", "--playlist-end", str(n), url])
        if r.returncode == 0 and r.stdout.strip():
            return [e for e in json.loads(r.stdout).get("entries", []) if e and e.get("id") and e.get("channel_id")]
        last = (r.stderr or "no output").strip()[-160:]
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(last)


def enrich(vid):
    """Upload timestamp, live status, views, subs for one video."""
    fmt = "%(timestamp)s\x1f%(release_timestamp)s\x1f%(live_status)s\x1f%(view_count)s\x1f%(channel_follower_count)s\x1f%(duration)s\x1f%(age_limit)s"
    r = run([YTDLP, "--no-warnings", "--skip-download", "--print", fmt, f"https://www.youtube.com/watch?v={vid}"], 60)
    p = r.stdout.strip().split("\x1f")
    if len(p) < 7:
        return None
    num = lambda s: float(s) if s not in ("NA", "None", "") else None
    return {"ts": num(p[0]) or num(p[1]), "live": p[2] == "is_live", "views": num(p[3]), "subs": num(p[4]), "dur": num(p[5]), "age": (num(p[6]) or 0) >= 18}


def ctype(title):
    for name, pat in TYPES:
        if re.search(pat, title, re.I):
            return name
    return "other"


def fmt_dur(s):
    if not s:
        return "?"
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def adin_scan(cfg, state, now, dry=False):
    """Alert on any @adinross GTA 6/VI/RP upload inside the configured window (alert-only)."""
    a = cfg["adin"]
    if not (a["from"] <= datetime.now(ET).strftime("%Y-%m-%d") <= a["to"]):
        return []
    out = []
    for tab in ("videos", "streams"):
        r = run([YTDLP, "--no-warnings", "--ignore-errors", "--skip-download", "--playlist-end", "5", "--print",
                 "%(id)s\x1f%(live_status)s\x1f%(timestamp)s\x1f%(duration)s\x1f%(title)s",
                 f"https://www.youtube.com/channel/{a['channel_id']}/{tab}"])
        for line in r.stdout.splitlines():
            p = line.split("\x1f")
            if len(p) < 5 or not GTA_ADIN.search(p[4]) or p[1] in ("is_upcoming",):
                continue
            ts = float(p[2]) if p[2] not in ("NA", "None") else None
            if p[1] != "is_live" and (ts is None or (now - ts) / 3600 > 72):
                continue
            key = f"adin:{p[0]}"
            if key in state["alerted"]:
                continue
            state["alerted"][key] = now
            _enqueue({"id": p[0], "title": p[4], "channel": "Adin Ross", "cid": a["channel_id"], "subs": a.get("subs", 4000000), "views": None,
                      "dur": float(p[3]) if p[3] not in ("NA", "None") else None, "type": ctype(p[4]), "live": p[1] == "is_live",
                      "spoiler": bool(SPOILER.search(p[4])), "vph": 0}, dry)
    return out


def qualifies(ch, cfg, now):
    t = cfg["thresholds"]
    vids = [v for v in ch["videos"].values() if v["ts"] and now - v["ts"] <= 7 * 86400]
    reasons = []
    if len(vids) >= t["cand_videos_7d"]:
        reasons.append(f"{len(vids)} GTA 6 videos in 7d")
    top = max(vids, key=lambda v: v["views"] or 0, default=None)
    if top and (top["views"] or 0) > t["cand_views"]:
        reasons.append(f"{int(top['views']):,} views on one video")
    fast = max(vids, key=lambda v: v.get("vph", 0), default=None)
    if fast and fast.get("vph", 0) > t["cand_vph"]:
        reasons.append(f"{int(fast['vph']):,} views/hour")
    return reasons, sorted(vids, key=lambda v: -v["ts"])


def alert_text(cid, ch, reasons, vids, info=False):
    types = sorted({v["type"] for v in vids})
    spoil = any(v.get("spoiler") for v in vids)
    subs = f"{int(ch['subs']):,} subs" if ch.get("subs") else "subs ?"
    best = max(v["vph"] for v in vids)
    lines = [f"{'INFO-ONLY ' if info else ''}GTA6 CANDIDATE CHANNEL: {ch['name']} ({subs}) | {'; '.join(reasons)}",
             f"  type: {'/'.join(types)} | best {int(best):,} vph | {len(vids)} vids/7d"]
    for v in vids[:3]:
        lines.append(f"  - {v['title'][:80]} ({v['type']}, {fmt_dur(v['dur'])}, {int(v['views'] or 0):,} views, {v['vph']:.0f}/h) https://youtu.be/{v['id']}")
    note = "SPOILER RISK in titles; " if spoil else ""
    lines.append(f"  risk: {note}unapproved third-party footage, check rights/reuse before any clipping" + (" | info_only: never clip" if info else ""))
    lines.append(f"  channel: https://www.youtube.com/channel/{cid} | set: python3 projects/gaming/set_status.py {cid} approved|info_only|ignored")
    return "\n".join(lines)


def _enqueue(entry, dry):
    import clip_queue
    return clip_queue.enqueue(entry, dry)


def scan(batch_size, run_all, dry):
    cfg = load_json(KW, None)
    state = load_json(STATE, {})
    state.setdefault("channels", {}); state.setdefault("alerted", {}); state.setdefault("cursor", 0); state.setdefault("video_cache", {})
    now = time.time()
    t = cfg["thresholds"]
    lm = launch_mode(cfg)
    if lm and lm.get("groups"):
        cfg = dict(cfg); cfg["groups"] = {g: v for g, v in cfg["groups"].items() if g in lm["groups"] or v.get("spoiler")}
    queries = build_queries(cfg)
    spoiler_groups = {g for g, s in cfg["groups"].items() if s.get("spoiler")}
    n = len(queries) if run_all else (batch_size or (lm or {}).get("batch_size") or cfg["batch_size"])
    cur = state["cursor"] % len(queries)
    batch = [queries[(cur + i) % len(queries)] for i in range(min(n, len(queries)))]
    state["cursor"] = (cur + len(batch)) % len(queries)
    batch_q = [(None, q) for q in cfg["always_queries"]] + batch
    approved = approved_ids(state)
    alerts, errors = [], []
    found = {}
    for g, q in batch_q:
        try:
            for e in search(q):
                if GTA.search(e["title"]) or (g is None and re.search(r"adin", e["title"], re.I)):
                    found.setdefault(e["id"], (e, g))
        except Exception as ex:  # noqa: BLE001
            errors.append(f"{q}: {ex}")
        time.sleep(1.2)
    # enrich only unseen videos (cache keeps rate low)
    need = [vid for vid in found if vid not in state["video_cache"] or now - state["video_cache"][vid].get("at", 0) > 6 * 3600]
    with ThreadPoolExecutor(3) as ex:
        for vid, info in zip(need, ex.map(enrich, need)):
            if info:
                info["at"] = now
                state["video_cache"][vid] = info
    adin_id = cfg["adin"]["channel_id"]
    for vid, (e, g) in found.items():
        info = state["video_cache"].get(vid)
        if not info:
            continue
        cid = e["channel_id"]
        views = e.get("view_count") or info["views"] or 0
        age_h = (now - info["ts"]) / 3600 if info["ts"] else None
        if not info["live"] and (age_h is None or age_h > t["max_age_h"]):
            continue
        if re.search(r"adin\s*ross", e["title"], re.I) and cid != adin_id and views > t["adin_third_party_views"]:
            key = f"adin3p:{vid}"
            if key not in state["alerted"]:
                state["alerted"][key] = now
                _enqueue({"id": vid, "title": e["title"], "channel": e["channel"], "cid": cid, "subs": info["subs"], "views": views, "dur": e.get("duration") or info["dur"],
                          "type": ctype(e["title"]), "live": info["live"], "spoiler": bool(SPOILER.search(e["title"])), "age_restricted": info.get("age", False),
                          "vph": views / max(age_h or 1, 1)}, dry)
        if cid in approved or cid == adin_id:
            continue
        ch = state["channels"].setdefault(cid, {"name": e["channel"], "subs": None, "status": "new", "videos": {}})
        if ch["status"] == "ignored":
            continue
        ch["name"] = e["channel"]
        ch["subs"] = info["subs"] or ch["subs"]
        title = e["title"]
        ch["videos"][vid] = {"id": vid, "title": title, "ts": info["ts"] or now, "views": views, "dur": e.get("duration") or info["dur"],
                             "vph": views / max(age_h or 1, 1), "type": ctype(title), "live": info["live"],
                             "spoiler": bool(SPOILER.search(title)) or g in spoiler_groups, "age": info.get("age", False)}
    for cid, ch in state["channels"].items():
        if ch["status"] in ("ignored", "approved"):
            continue
        reasons, vids = qualifies(ch, cfg, now)
        if not reasons:
            continue
        if ch["status"] in ("new", "candidate_alerted"):
            if ch["status"] == "new":
                ch["status"] = "candidate_alerted"
            for v in vids:   # qualifying videos enter the finished-clip queue (no alert text)
                _enqueue({"id": v["id"], "title": v["title"], "channel": ch["name"], "cid": cid, "subs": ch.get("subs"), "views": v["views"], "dur": v["dur"],
                          "type": v["type"], "live": v["live"], "spoiler": v.get("spoiler", False), "age_restricted": v.get("age", False), "vph": v["vph"]}, dry)
        elif ch["status"] == "info_only":
            for v in vids:
                key = f"info:{v['id']}"
                if key not in state["alerted"] and ((v["views"] or 0) > t["cand_views"] or v["vph"] > t["cand_vph"]):
                    state["alerted"][key] = now
                    pass   # info_only channels: marked seen, never clipped, no alert (William: finished clips only)
    adin_scan(cfg, state, now, dry)
    # prune
    state["channels"] = {k: v for k, v in state["channels"].items() if v["status"] != "new" or any(now - x["ts"] < 7 * 86400 for x in v["videos"].values())}
    state["video_cache"] = {k: v for k, v in state["video_cache"].items() if now - v.get("at", 0) < 3 * 86400}
    if not dry:
        json.dump(state, open(STATE, "w"), indent=1)
    return alerts, errors, len(batch_q), len(found)


def digest():
    cfg = load_json(KW, None)
    state = load_json(STATE, {"channels": {}})
    now = time.time()
    rows = []
    for cid, ch in state["channels"].items():
        vids = [v for v in ch["videos"].values() if now - v["ts"] <= 7 * 86400]
        if vids:
            rows.append((cid, ch, len(vids), max(v["vph"] for v in vids), sum(v["views"] or 0 for v in vids)))
    rows.sort(key=lambda r: (-(r[2] + r[3] / 1000), r[1]["name"]))
    print(f"GTA6 DISCOVERY WEEKLY DIGEST ({datetime.now(ET):%Y-%m-%d}): {len(rows)} channels seen in 7d")
    for i, (cid, ch, n, vph, views) in enumerate(rows[:10], 1):
        subs = f"{int(ch['subs']):,}" if ch.get("subs") else "?"
        print(f"{i}. {ch['name']} [{ch['status']}] {n} vids, {views:,} views, peak {vph:,.0f}/h, {subs} subs | https://www.youtube.com/channel/{cid}")
    if not rows:
        print("no channels tracked yet")


def main():
    a = sys.argv[1:]
    if "--digest" in a:
        return digest()
    bs = int(a[a.index("--batch") + 1]) if "--batch" in a else None
    alerts, errors, nq, nf = scan(bs, "--all" in a, "--dry-run" in a)
    if "--dry-run" in a:
        print(f"[dry-run] {nq} queries, {nf} relevant videos found, {len(alerts)} alerts, {len(errors)} errors (state not written)")
    for al in alerts:
        print(al)
    if errors and (len(errors) >= nq or "--dry-run" in a):
        print(f"GTA6 DISCOVERY ERROR: {len(errors)}/{nq} queries failed: {errors[0]}")


if __name__ == "__main__":
    main()
