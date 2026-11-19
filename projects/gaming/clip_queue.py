#!/usr/bin/env python3
"""GTA 6 finished-clip queue (wrdgamingclipz). Builds on gta6_discovery.py. William sees only FINISHED clips in Telegram
(Post / Skip). Nothing is posted without his Post tap. State: clip_queue.json. Config: clip_queue_config.json.

Stages: discovered -> routed -> made -> screened -> awaiting_approval -> approved (waiting for 7 AM-11 PM ET) -> posted | skipped
  clip_queue.py cycle [--dry-run]   discovery scan (enqueues) + risk/route/make/screen + flush approved posts; prints TGSEND lines
  clip_queue.py run [--dry-run]     pipeline only (no discovery scan)
  clip_queue.py add URL [--route own_cut|guide|opus] [--dry-run]   enqueue one source by hand (test / manual)
  clip_queue.py callback VALUE      gta6post_<id> | gta6skip_<id> | gta6chok_<cid> | gta6chno_<cid>  (a Telegram tap)
  clip_queue.py payload ID          print the TGSEND line for a finished clip again
  clip_queue.py show [ID]           status table / one item
  clip_queue.py gate [ID...|all] [--force]  run the real-footage SOURCE gate (source_gate.py, cached per video id) on queued items
  clip_queue.py pending             clips held for Morpheus review: contact sheets + gate verdicts; sources needing his own look
  clip_queue.py release ID|all      send held clips to William
Output protocol: each line `TGSEND {json}` = one Telegram message: {"text","media"(optional mp4 path),"buttons"(optional rows of
{"label","value"})}. Buttons are value-only. Empty stdout = nothing to send.
Routing: walkthrough -> own_cut (moment_pick + cut_moment + original text line); guide -> guide_make (needs a reviewed
out/ID.guide.json script; a WORKORDER is written until it exists); streams / long gameplay <= 40 min -> OpusClip (budget guard);
anything else -> own_cut. Gates: every source passes source_gate.py (storyboard contact sheet + vision model; only real_gameplay without prominent
watermark/heavy overlay passes) BEFORE any make/OpusClip credit; the finished clip's contact sheet is gated again. No vision verdict
= item marked needs_my_review (nothing auto-passes). Risk: low auto-clips; medium/high hold the channel for ONE question; spoiler-risk never queues.
"""
import fcntl, json, math, os, re, subprocess, sys, time
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "opusclip"))
STATE = os.path.join(HERE, "clip_queue.json")
CFG = os.path.join(HERE, "clip_queue_config.json")
OUTQ = os.path.join(HERE, "out", "queue")
CANDS = os.path.join(HERE, "candidates.json")
YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"
FFMPEG = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")
ET = ZoneInfo("America/New_York")
DEFAULT_CFG = {"daily_cap": 8, "launch_week": {"start": "2026-11-19", "end": "2026-11-25", "cap": 14}, "skips_to_ignore": 3,
               "opus_max_min": 40, "opus_min_min": 20, "max_make_per_run": 1, "posting_window_et": [7, 23], "clip_seconds": 40,
               "accounts": {"yt_opus": "6aee359f69f72aca6cb4207e", "tiktok": "6afa5abf5a226aba99eb2d09"}}
BLOCK = re.compile(r"cutscene|cut-scene|ending|spoiler|leak|final mission|full movie|credits|concept|fan[- ]?made|fake|"
                   r"story mission|all cutscenes|prologue|opening mission", re.I)
STREAMISH = re.compile(r"\blive\b|stream|\bvod\b|marathon|24/7|24 hour|reaction|first look", re.I)
SPONSOR = re.compile(r"sponsor|#ad\b|paid promotion|use code|affiliate", re.I)
SENSITIVE = re.compile(r"\b(child sex|child porn\w*|sexual abuse|csam|rape[ds]?|sexual assault|suicide|molest\w*)\b|"
                       r"\b(blood|bleeding|dead body|corpse|gunshot wound|gore)\b", re.I)
GUIDE_RE = re.compile(r"guide|how to|tips|tutorial|explained|everything you need|things to do|best way|unlock|cheats|codes|easter egg|secret|collectible|locations?", re.I)


def now_et():
    return datetime.now(ET)


def jload(p, default):
    try:
        return json.load(open(p))
    except Exception:  # noqa: BLE001
        return default


def cfg():
    c = dict(DEFAULT_CFG)
    c.update(jload(CFG, {}))
    try:  # launch mode (gta6_keywords.json launch_mode) widens per-run make count and the posting window
        import gta6_discovery as gd
        lm = gd.launch_mode(jload(os.path.join(HERE, "gta6_keywords.json"), {}))
        if lm:
            for key in ("max_make_per_run", "posting_window_et"):
                if key in lm:
                    c[key] = lm[key]
    except Exception:  # noqa: BLE001
        pass
    return c


def load():
    s = jload(STATE, {})
    s.setdefault("items", {}); s.setdefault("channels", {})
    return s


def save(s):
    tmp = STATE + ".tmp"
    json.dump(s, open(tmp, "w"), indent=1)
    os.replace(tmp, STATE)


def run(cmd, timeout=900, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)


def log(it, stage, note=""):
    it["stage"] = stage
    it.setdefault("history", []).append({"t": now_et().isoformat(timespec="seconds"), "stage": stage, "note": note})


# ---------------------------------------------------------------- risk
def approved_ids():
    ids = {c["channel_id"] for c in jload(CANDS, {"candidates": []})["candidates"] if c.get("approved") and c.get("channel_id")}
    return ids


def assess_risk(it, state):
    """Rights-risk from computable signals. 0-1 low, 2 medium, 3+ high. Known creator permission (approved/clip_ok) = -3."""
    pts, why = 0, []
    subs = it.get("subs") or 0
    if it.get("subs") is None:
        pts += 1; why.append("subs unknown")
    if subs >= 1_000_000:
        pts += 3; why.append(f"huge channel {int(subs):,} subs")
    elif subs >= 100_000:
        pts += 2; why.append(f"large channel {int(subs):,} subs")
    elif subs >= 5_000:
        pts += 1; why.append(f"monetized-looking channel {int(subs):,} subs")
    if it.get("age_restricted"):
        pts += 3; why.append("age-restricted")
    if BLOCK.search(it.get("title", "")) and not it.get("spoiler"):
        pts += 3; why.append("cutscene/story/ending/concept words in title")
    if SPONSOR.search(it.get("title", "")):
        pts += 1; why.append("sponsored-looking")
    perm = it["cid"] in approved_ids() or state["channels"].get(it["cid"], {}).get("clip_ok")
    if perm:
        pts = max(0, pts - 3); why.append("creator permission on file")
    return ("low" if pts <= 1 else "medium" if pts == 2 else "high"), why


def route_for(it, c):
    t, title, dur = it.get("type"), it.get("title", ""), (it.get("dur") or 0) / 60
    if t == "guide" or (GUIDE_RE.search(title) and t != "walkthrough"):
        return "guide"
    if t == "walkthrough":
        return "own_cut"
    streamish = it.get("live") or STREAMISH.search(title)
    if dur and ((streamish and dur <= c["opus_max_min"]) or (c["opus_min_min"] <= dur <= c["opus_max_min"])):
        return "opus"
    return "own_cut"


# ---------------------------------------------------------------- enqueue
def enqueue(e, dry=False, route=None):
    """e: id,title,channel,cid,subs,views,dur,type,live,spoiler,age_restricted. Returns status string; dedupes by video id."""
    s = load()
    if e["id"] in s["items"]:
        return "dup"
    ch = s["channels"].setdefault(e["cid"], {"name": e["channel"], "skips": 0, "ignored": False})
    if ch.get("ignored"):
        return "channel-ignored"
    it = {"id": e["id"], "url": f"https://www.youtube.com/watch?v={e['id']}", "title": e["title"], "channel": e["channel"], "cid": e["cid"],
          "subs": e.get("subs"), "views": e.get("views"), "dur": e.get("dur"), "type": e.get("type", "other"), "live": bool(e.get("live")),
          "spoiler": bool(e.get("spoiler")), "age_restricted": bool(e.get("age_restricted")), "vph": e.get("vph", 0),
          "history": [], "credits": 0, "made_by": None, "forced_route": route}
    log(it, "discovered")
    if dry:
        return "dry-run: would queue " + it["id"]
    s["items"][it["id"]] = it
    save(s)
    return "queued"


# ---------------------------------------------------------------- helpers
_KEEP_UP = {"GTA", "VI", "PS5", "PS4", "VR", "AI", "UK", "US", "FPS", "HD", "4K", "GTA6", "GTAVI", "NPC", "NPCS", "RP", "II", "III", "NZ",
            "RDR", "DLC", "FOV", "UFO", "FBI", "CIA", "LAPD", "NYPD", "USA", "UAE", "SUV", "ATM", "GPS", "RTX", "CPU", "GPU", "SSD", "NBA", "NFL", "CJ"}


def fix_case(t):
    """Title-case shouting text and repair mangled tokens ('It'S' -> "It's", 'Gta Vi' -> 'GTA VI'). Keeps GTA/VI/GTA6 upper."""
    letters = [ch for ch in t if ch.isalpha()]
    shouting = bool(letters) and sum(ch.isupper() for ch in letters) / len(letters) > 0.6

    def word(m):
        w = m.group(0)
        if w.upper() in _KEEP_UP:
            return w.upper()
        mm = re.match(r"^([A-Za-z0-9]+)(['\u2019])([A-Za-z]{1,2})$", w)
        if mm:  # It'S / IT'S -> It's: contraction suffix is always lowercase
            base, ap, suf = mm.groups()
            if base.upper() in _KEEP_UP:
                base = base.upper()
            elif shouting or base.isupper():
                base = base[0].upper() + base[1:].lower()
            return base + ap + suf.lower()
        if shouting or (w.isalpha() and w.isupper() and len(w) >= 3):  # no all-caps words (acronyms in _KEEP_UP excepted)
            return w[0].upper() + w[1:].lower()
        return w
    return re.sub(r"[A-Za-z0-9][A-Za-z0-9'\u2019]*", word, t)


def clean_title(t):
    t = re.split(r"\s[|•]\s", t)[0]
    t = re.sub(r"#\w+|\(GRAND THEFT AUTO VI\)|\[[^\]]*\]", "", t).strip(" -:|")
    t = fix_case(t)
    return re.sub(r"\s+", " ", t)[:70].strip()


def is_real(it):
    """True only when the source gate said real_gameplay (never claim 'gameplay' otherwise)."""
    g = it.get("gate") or {}
    return g.get("verdict") == "real_gameplay" and g.get("pass") is True


NEWS_RE = re.compile(r"news|update|leak|trailer|countdown|release|rumou?r|announce|delay|date", re.I)
PROMO_RE = re.compile(r"subscri|welcome|channel|like and|hit the|patreon|sponsor|link|description|comment|today we|guys|\bchat\b|let'?s get|"
                      r"real quick|before we|new to|follow|discord|merch|giveaway|\bkick\b|\btwitch\b|thank|\bmy\b|\bi\b", re.I)
TOPIC_RE = re.compile(r"\b(car|cars|vehicle|bike|boat|jet ?ski|helicopter|plane|gun|guns|weapon|weapons|heist|police|cops?|wanted|map|vice city|leonida|"
                      r"jason|lucia|phone|app|mission|robbery|store|shop|money|cash|cheat|trick|glitch|secret|easter egg|npc|npcs|radio|house|"
                      r"apartment|garage|shoot|chase|dog|animal|weather|swim|dive|fish|drive|steal|stolen|register|spawn|upgrade|unlock)\b", re.I)
DANGLING = {"a", "an", "the", "your", "to", "of", "and", "with", "for", "in", "on", "at", "his", "her", "their", "that", "is", "are", "or", "by", "from", "you", "it", "its", "as", "into"}
FILLER_RE = re.compile(r"^(?:(?:so|and|but|then|now|okay|ok|well|first|second|next|also|yeah|because|basically|actually|here|if|when)[,\s]+)+", re.I)
# Hashtags: max 3, #GTA6 first, never #Shorts / #GTA6Gameplay (see METADATA_RULES.md). Slots 2-3 by content type (creator tag goes in slot 2 for stream moments).
TYPE_HASH = {"Walkthrough": ["#GrandTheftAuto6", "#GTAVI"], "Guide": ["#GrandTheftAuto6", "#GTAVI"], "Gameplay": ["#GrandTheftAuto6", "#GTAVI"],
             "Stream Moment": ["#GrandTheftAuto6", "#GTAVI"], "News": ["#GrandTheftAuto6", "#RockstarGames"], "Clip": ["#GrandTheftAuto6", "#GTAVI"]}
# TikTok: #GTA6 + two content tags + #fyp
TYPE_TIKTOK = {"Walkthrough": ["#gta6walkthrough", "#gaming"], "Guide": ["#gta6tips", "#gaming"], "Gameplay": ["#grandtheftauto6", "#gaming"],
               "Stream Moment": ["#streamer", "#gaming"], "News": ["#gta6news", "#gaming"], "Clip": ["#gaming", "#videogames"]}
# (titles that already carry a number, comparison or spec pattern keep their source wording: see title_style / _hooky)
LABEL_RE = re.compile(r"^GTA\s*(?:6|VI)\s*(?:[A-Za-z']+(?:\s+[A-Za-z']+){0,2})?\s*[:\u2013\u2014|]\s*(?=\S)|^GTA\s*(?:6|VI)\s*-\s+(?=\S)", re.I)
GENERIC_NAME_WORDS = {"gaming", "reacts", "clips", "live", "highlights", "vods", "tv", "official"}


def approved_creator(it):
    """Display name of the approved streamer for this item's channel (candidates.json approved=true), else None."""
    for cd in jload(CANDS, {"candidates": []})["candidates"]:
        if cd.get("approved") and cd.get("channel_id") == it.get("cid"):
            return cd.get("name") or it.get("channel")
    return None


def creator_tag(name):
    words = [w for w in re.sub(r"\([^)]*\)", "", name).split() if w]
    while len(words) > 1 and words[-1].lower() in GENERIC_NAME_WORDS:
        words.pop()
    tag = re.sub(r"[^A-Za-z0-9]", "", "".join(words))
    return "#" + tag if tag else ""


def content_type(it):
    """Label for the clip: Walkthrough | Guide | Gameplay | Stream Moment | News | Clip (never claims gameplay unless the gate passed)."""
    if approved_creator(it) or it.get("live"):
        return "Stream Moment"
    if it["type"] == "guide":
        return "Guide"
    if it["type"] == "walkthrough":
        return "Walkthrough"
    if is_real(it):
        return "Gameplay"
    return "News" if NEWS_RE.search(it.get("title", "")) else "Clip"


def moment_phrase(it, limit):
    """Concrete moment from the moment_pick transcript window (own cuts only). Conservative: needs a GTA topic word, no channel-promo or
    first-person filler, 4-14 words. Returns '' when nothing qualifies so the caller falls back to the cleaned source title."""
    text = (it.get("moment_text") or "").replace(">>", " ")
    if not text or "[ __ ]" in text:
        return ""
    sents = [FILLER_RE.sub("", x.strip()).strip(" ,.;:!?-") for x in re.split(r"(?<=[.!?])\s+", text)]
    sents = [x for x in sents if x and not PROMO_RE.search(x) and TOPIC_RE.search(x)]
    for cut in (False, True):  # pass 1: whole sentences that fit; pass 2: cut at a natural break inside the limit
        for sent in sents:
            if len(sent) > limit:
                if not cut:
                    continue
                head = sent[:limit]
                br = max(head.rfind(", "), head.rfind(" and "), head.rfind(" then "))
                sent = (head[:br] if br >= limit * 0.3 else head.rsplit(" ", 1)[0]).rstrip(" ,;:-")
                while sent.rsplit(" ", 1)[-1].lower() in DANGLING:  # never end on 'your', 'to', 'the'...
                    sent = sent.rsplit(" ", 1)[0].rstrip(" ,;:-")
            n = len(sent.split())
            if n < 4 or (sent.endswith("?") and n > 10) or not TOPIC_RE.search(sent):
                continue
            return sent[0].upper() + sent[1:]
    return ""


def fit_title(t, n=60):
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= n:
        return t
    cut = t[:n].rsplit(" ", 1)[0].rstrip(" ,;:-(&")
    cut = re.sub(r"\([^)]*$", "", cut).rstrip(" ,;:-")
    return cut


def _norm_words(t):
    return [re.sub(r"[^a-z0-9']", "", w.lower()) for w in t.split()]


def dedupe_phrases(t):
    """No repeated phrases: 'Vice Beach: Vice Beach Got Cooked' -> 'Vice Beach Got Cooked'; a repeated 2+ word run is removed from its second spot."""
    head, sep, tail = t.partition(": ")
    if sep:
        hw, tw = _norm_words(re.sub(r"^GTA\s*\d+\s*", "", head, flags=re.I)), _norm_words(tail)
        if hw and tw[:len(hw)] == hw:
            return tail.strip()
    words = t.split()
    nw = _norm_words(t)
    for n in range(min(5, len(words) // 2), 1, -1):
        for i in range(len(words) - 2 * n + 1):
            for j in range(i + n, len(words) - n + 1):
                if nw[i:i + n] == nw[j:j + n] and all(nw[i:i + n]):
                    words = words[:j] + words[j + n:]
                    return re.sub(r"\s+", " ", " ".join(words)).strip(" ,;:-")
    return t


def _hooky(t):
    """True when the title already has a number / comparison / spec pattern (game-name digits like 'GTA 6' do not count)."""
    return title_style(t) != "hook"


def strip_label(t):
    """Drop a leading 'GTA 6:' / 'GTA 6 <Type>:' label so the title opens with the hook."""
    return LABEL_RE.sub("", t).strip()


def title_style(t):
    """number | comparison | spec | hook, for logs and tests."""
    if re.search(r"\bvs\.?\b|\bversus\b|compared|would look like|\bhow long\b|years? (?:later|apart)", t, re.I):
        return "comparison"
    if re.search(r"\bfps\b|\bps5\b|series [sx]\b|edition|preload|pre-load", t, re.I):
        return "spec"
    if re.search(r"\b\d+\b", re.sub(r"GTA\s*\d+", "GTA", t, flags=re.I)):
        return "number"
    return "hook"


def finish_title(t, n=60):
    """Final pass for every YouTube title: no hashtags, no repeats, no all-caps words, game name once, <=n chars, hook first."""
    t = re.sub(r"#\w+", "", t)
    t = re.sub(r"GTA\s*VI\b", "GTA 6", t)
    t = fix_case(re.sub(r"\s+", " ", t).strip(" -:|"))
    t = dedupe_phrases(t)
    if len(re.findall(r"GTA\s*6", t)) > 1:
        t = re.sub(r"\s+(?:in|for|of|on)\s+GTA\s*6\b", "", t, count=1)
    return fit_title(t, n)


def make_yt_title(it):
    """<=60 chars, leads with the hook or a number (never 'GTA 6 <Type>:'), game name once, no all-caps, no repeats, no hashtags.
    Sources that already carry a number / comparison / spec keep their wording; otherwise a transcript moment (own cuts) is used when it is safe.
    A streamer name is used only for an approved creator's own stream with a specific quotable moment."""
    ctype = content_type(it)
    ct0 = re.sub(r"GTA\s*VI\b", "GTA 6", clean_title(it["title"]))
    egg = bool(re.match(r"GTA\s*6\s+Easter Egg\s*[:\u2013\u2014|]", ct0, re.I))  # keep 'Easter Egg' (demand phrase) when its label is stripped
    ct = dedupe_phrases(strip_label(ct0))
    can_moment = ctype in ("Walkthrough", "Guide", "Gameplay", "Stream Moment") and not _hooky(ct)
    if can_moment:
        mp = moment_phrase(it, 46)
        if mp:
            it["title_src"] = "moment"
            cr = approved_creator(it) if ctype == "Stream Moment" else None
            if cr:
                quoted = f'{cr}: "{mp}"'
                if len(quoted) <= 60:
                    return finish_title(quoted)
            return finish_title(f"{mp} (GTA 6)")
    it["title_src"] = "source"
    if not re.search(r"GTA\s*6", ct, re.I):
        ct = f"{ct} in GTA 6" if len(ct) + 9 <= 60 else ct
    if egg and "easter egg" not in ct.lower() and len(ct) + 13 <= 60:
        ct += " (Easter Egg)"
    return finish_title(ct)


def make_hashtags(it, ctype=None):
    """Max 3: #GTA6 first, then the approved creator's tag (stream moments only) and type tags. Never #Shorts, #GTA6Gameplay or title hashtags."""
    ctype = ctype or content_type(it)
    tags = ["#GTA6"]
    cr = approved_creator(it) if ctype == "Stream Moment" else None
    if cr and creator_tag(cr):
        tags.append(creator_tag(cr))
    tags += TYPE_HASH[ctype]
    seen, out = set(), []
    for t in tags:
        if t.lower() not in seen:
            seen.add(t.lower()); out.append(t)
    return out[:3]


def make_tags(it, ctype=None, yt_title=""):
    """8-10 search phrases for yt_upload_gaming.py --tags (no commas inside a tag). Core high-use phrases, plus phrases that come from this
    video's own title/type; nothing about people, games or events that are not in the clip."""
    ctype = ctype or content_type(it)
    src = (yt_title if it.get("title_src") == "moment" else it.get("title", "")) + " " + it.get("title", "")
    core = ["gta 6", "gta6", "grand theft auto 6", "grand theft auto vi", "gta vi", "rockstar games"]
    spec = []
    cr = approved_creator(it) if ctype == "Stream Moment" else None
    if cr:
        spec.append(f"{re.sub(r'[(][^)]*[)]', '', cr).strip().lower()} gta 6")
    if re.search(r"easter egg|secret|hidden|detail", src, re.I):
        spec += ["gta 6 easter egg", "gta 6 secrets", "gta 6 details"]
    if ctype == "Walkthrough":
        spec.append("gta 6 walkthrough")
        if re.search(r"part\s*1\b|episode\s*1\b|prologue|mission\s*1\b|opening", src, re.I):
            spec.append("gta 6 walkthrough part 1")
    elif ctype == "Guide":
        spec += ["gta 6 guide", "gta 6 tips"]
    elif ctype == "Gameplay":
        spec.append("gta 6 gameplay")
    elif ctype == "News":
        spec.append("gta 6 news")
        if re.search(r"trailer", src, re.I):
            spec.append("gta 6 trailer")
        if re.search(r"release|date|countdown|delay", src, re.I):
            spec.append("gta 6 release date")
    for w in dict.fromkeys(x.lower() for x in TOPIC_RE.findall(src)):
        spec.append(f"gta 6 {w}")
    spec = list(dict.fromkeys(spec))
    return list(dict.fromkeys(core + spec[:4]))[:10]


def make_tiktok(it, ctype, yt_title):
    """TikTok: own hashtag set (#GTA6 + 2 content tags + #fyp) and the title trimmed to leave room for them."""
    tags = ["#GTA6"] + TYPE_TIKTOK[ctype][:2] + ["#fyp"]
    title = fit_title(yt_title, 70)
    return title, f"{title} " + " ".join(tags), tags


def tiktok_caption(it):
    """TikTok caption: trimmed title + its own hashtag set + the same 'Via <channel>' credit line (reused-content rule). Items made before the
    new metadata existed get theirs computed here; their stored YouTube title/description are not touched."""
    cap = it.get("tt_caption")
    if not cap:
        cap = make_tiktok(it, content_type(it), it["yt_title"])[1]
    return f"{cap}\n\nVia {it['channel'].strip()}: {it['url']}"


def make_title_desc(it, line=None):
    """Returns (yt_title, description). Also stores it['yt_tags'] (list), it['tt_title'], it['tt_caption'], it['hashtags']."""
    ctype = content_type(it)
    yt = make_yt_title(it)
    kind = {"walkthrough": "walkthrough", "guide": "guide"}.get(it["type"], "gameplay")
    if kind != "guide" and not is_real(it):
        kind = "video"
    hook = line or f"A moment from {it['channel']}'s GTA 6 {kind}, with our own take on it."
    mp = moment_phrase(it, 90) if ctype in ("Walkthrough", "Guide", "Gameplay", "Stream Moment") else ""
    what = "video moment" if ctype == "Clip" else f"{ctype.lower()} clip"
    summary = (f"GTA 6 {what}: {mp}. " if mp else f"GTA 6 {what}. ") + "Search: GTA 6 tips, news and gameplay moments."
    tags = make_hashtags(it, ctype)
    desc = f"{yt}\n\n{summary}\n\n{hook}\n\nMore GTA 6 secrets and tips: wrdgamingclipz\n\n{' '.join(tags)}\n\nVia {it['channel'].strip()}: {it['url']}"
    it["hashtags"], it["yt_tags"] = tags, make_tags(it, ctype, yt)
    it["tt_title"], it["tt_caption"], _ = make_tiktok(it, ctype, yt)
    return yt, desc


def overlay_line(it):
    kind = {"walkthrough": "GTA 6 walkthrough", "guide": "GTA 6 guide"}.get(it["type"], "GTA 6 gameplay")
    if not kind.endswith("guide") and not is_real(it):
        kind = "GTA 6"  # neutral: gate did not confirm real gameplay
    ct = clean_title(it["title"])
    ct = re.sub(r"^gta\s*(6|vi)\s*[:\-]?\s*", "", ct, flags=re.I)
    return (f"{kind}: {ct}" if ct else kind)[:64]


def add_text_line(src, dst, text):
    """Original on-screen text line (reused-content rule). PIL PNG overlay: the static ffmpeg has no drawtext."""
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) > 960 and cur:
            lines.append(cur); cur = w
        else:
            cur = trial
    lines.append(cur)
    h = 70 * len(lines) + 30
    d.rectangle([40, 150, 1040, 150 + h], fill=(0, 0, 0, 150))
    for i, ln in enumerate(lines):
        d.text((540, 170 + i * 70), ln, font=font, fill=(255, 221, 0, 255), anchor="ma")
    png = dst + ".png"
    img.save(png)
    r = run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-i", png, "-filter_complex", "[0:v][1:v]overlay=0:0[v]", "-map", "[v]", "-map", "0:a?",
             "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", dst], 600)
    os.remove(png)
    if r.returncode != 0 or not os.path.exists(dst):
        raise RuntimeError("overlay failed: " + r.stderr[-300:])


# ---------------------------------------------------------------- make
def make_own_cut(it, c):
    os.makedirs(OUTQ, exist_ok=True)
    vid = it["id"]
    start = None
    mom = os.path.join(HERE, "out", f"{vid}.moments.json")
    if not os.path.exists(mom):
        run([sys.executable, os.path.join(HERE, "moment_pick.py"), vid, "--top", "8"], 900)
    m = jload(mom, {}).get("moments", [])
    dur = it.get("dur") or 0
    if m:
        best = max(m, key=lambda x: x["score"])
        start = max(0, best["start"] - 5)
        it["moment_text"] = best.get("text", "")[:400]
        it["pick"] = f"moment_pick score {best['score']} at {int(best['start'])}s"
    else:
        start = min(20, dur * 0.15) if dur else 10
        it["pick"] = "fallback (no transcript): early window"
    clip_len = min(c["clip_seconds"], max(8, dur - start)) if dur else c["clip_seconds"]
    end = start + clip_len
    name = f"q_{vid}"
    r = run([sys.executable, os.path.join(HERE, "cut_moment.py"), vid, "--start", str(int(start)), "--end", str(int(end)), "--out", OUTQ, "--name", name], 1200)
    mp4 = os.path.join(OUTQ, f"{name}.mp4")
    if not os.path.exists(mp4):
        raise RuntimeError("cut failed: " + (r.stderr or r.stdout)[-300:])
    line = overlay_line(it)
    final = os.path.join(OUTQ, f"{vid}.final.mp4")
    add_text_line(mp4, final, line)
    it["files"] = {"mp4": final, "sheet": os.path.join(OUTQ, f"{name}.contact.jpg")}
    it["overlay_line"] = line
    it["yt_title"], it["desc"] = make_title_desc(it)
    it["made_by"], it["credits"], it["how"] = "own-stack", 0, f"moment_pick+cut_moment+text line ({it['pick']}, src {int(start)}-{int(end)}s)"


def make_guide(it, c):
    vid = it["id"]
    gj = os.path.join(HERE, "out", f"{vid}.guide.json")
    if not os.path.exists(gj):
        if not os.path.isdir(os.path.join(HERE, "work", "guides", vid)) or not os.listdir(os.path.join(HERE, "work", "guides", vid)):
            run([sys.executable, os.path.join(HERE, "guide_make.py"), it["url"], "fetch"], 1200)
        wo = os.path.join(OUTQ, f"{vid}.WORKORDER.md")
        os.makedirs(OUTQ, exist_ok=True)
        open(wo, "w").write(f"# Script needed (GUIDE-RULES.md binding)\nSource: {it['url']} ({it['channel']})\nTranscript: work/guides/{vid}/transcript.txt\n"
                            f"Write out/{vid}.guide.json (see guide_make.py docstring), then the queue builds it on the next cycle.\n")
        it["needs_script"] = wo
        return False
    r = run([sys.executable, os.path.join(HERE, "guide_make.py"), it["url"], "build"], 1800)
    mp4 = os.path.join(HERE, "out", f"{vid}.mp4")
    if not os.path.exists(mp4):
        raise RuntimeError("guide build failed: " + (r.stderr or r.stdout)[-300:])
    g = jload(gj, {})
    it["files"] = {"mp4": mp4, "sheet": os.path.join(HERE, "out", f"{vid}.contact.jpg")}
    yt = g.get("yt_title") or g.get("title") or clean_title(it["title"])
    dp = os.path.join(HERE, "out", f"{vid}.desc.txt")
    it["yt_title"], it["desc"] = yt[:95], (open(dp).read() if os.path.exists(dp) else make_title_desc(it)[1])
    it["made_by"], it["credits"], it["how"] = "own-stack", 0, "guide_make (reworked, Liam voiceover, ~$0.13 TTS)"
    it.pop("needs_script", None)
    return True


def make_opus(it, c, dry=False):
    import opus
    import gaming_budget as gb
    if not it.get("opus_project"):
        if (it.get("gate") or {}).get("pass") is not True:
            it["note"] = "no credits: source gate has not passed"  # never spend OpusClip credits before the gate
            return False
        # OpusClip only takes finished videos: reuse live_watch's end test (was_live/not_live with a real duration) before any submit
        import live_watch
        st, dur, _ch, _t = live_watch.status(it["id"])
        if not (st in ("was_live", "not_live") and dur not in ("", "NA", "None")):
            it["note"] = f"no credits: stream not ended/processed yet (status {st}); waiting"
            return False
        try:
            it["dur"] = float(dur)
        except ValueError:
            pass
        mins = (it.get("dur") or 0) / 60
        v = gb.can_spend(mins)
        if not v["allowed"]:
            it["note"] = "budget: " + "; ".join(v["reasons"])
            return False
        res = opus.call("POST", "/api/clip-projects", {"videoUrl": it["url"], "curationPref": {"clipDurations": [[15, 60]], "genre": "Auto"},
                                                        "renderPref": {"layoutAspectRatio": "portrait"}})
        it["opus_project"] = res.get("id") or res.get("projectId")
        it["credits"] = v["cost"]
        gb.record(it["id"], v["cost"], f"clip_queue opus submit {it['url']}")
        it["made_by"] = "opusclip"
        return False
    st = opus.call("GET", f"/api/clip-projects/{it['opus_project']}")
    if st.get("stage") not in ("COMPLETE", "COMPLETED"):
        it["note"] = f"opus stage {st.get('stage')}"
        if st.get("error"):
            raise RuntimeError("opus error " + str(st["error"])[:200])
        return False
    res = opus.call("GET", f"/api/exportable-clips?q=findByProjectId&projectId={it['opus_project']}")
    clips = res if isinstance(res, list) else res.get("data", [])
    if not clips:
        raise RuntimeError("opus returned no clips")
    best = max(clips, key=lambda x: x.get("score") or 0)
    it["opus_clip"] = best["id"]
    it["yt_title"], it["desc"] = make_title_desc(it)
    it["how"] = f"OpusClip auto-clip (score {best.get('score')}), {it['credits']} credits"
    return True


# ---------------------------------------------------------------- screen
def screen_file(mp4):
    """Visual screen with the existing visual_check feature extractor + a blood-red pixel test. Returns (ok, reasons, metrics)."""
    import numpy as np
    import visual_check as vc
    why, met = [], {}
    f = vc.features(vc.read_gray(mp4))
    if not f:
        return False, ["too few frames"], {}
    met.update(f)
    if f["black"] > 0.4:
        why.append(f"black {f['black']:.0%}")
    if f["static"] > 0.6 or f["motion"] < 0.003:
        why.append(f"static/no motion ({f['static']:.0%})")
    r = subprocess.run([FFMPEG, "-loglevel", "error", "-i", mp4, "-an", "-vf", "fps=2,scale=108:192,format=rgb24", "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    n = len(a) // (108 * 192 * 3)
    fr = a[: n * 108 * 192 * 3].reshape(n, 192, 108, 3).astype(np.float32)
    R, G, B = fr[..., 0], fr[..., 1], fr[..., 2]
    red = ((R > 110) & (G < 0.4 * R) & (B < 0.4 * R)).mean(axis=(1, 2))
    met["red_max"], met["red_first7s"] = round(float(red.max()), 3), round(float(red[:14].max()), 3)
    if met["red_first7s"] > 0.04:
        why.append(f"blood-red in first 7s ({met['red_first7s']:.1%})")
    if met["red_max"] > 0.10:
        why.append(f"blood-red frames ({met['red_max']:.1%})")
    return not why, why, met


def screen(it):
    mp4 = (it.get("files") or {}).get("mp4")
    why, met = [], {}
    if it.get("opus_clip") and not mp4:
        r = run([sys.executable, os.path.join(HERE, "..", "opusclip", "screen_clip.py"), it["opus_project"], it["opus_clip"]], 600)
        j = json.loads(r.stdout[r.stdout.index("{"):]) if "{" in r.stdout else {}
        tf = j.get("text_flags", {})
        for k in ("sensitive", "graphic"):
            if k in tf:
                why.append(f"transcript {k}: {', '.join(tf[k])[:60]}")
        d = os.path.dirname(j["frames"][0]) if j.get("frames") else os.path.join(HERE, "..", "opusclip", "screens", it["opus_clip"].split(".")[-1])
        mp4 = os.path.join(d, "clip.mp4")
        it["files"] = {"mp4": mp4, "sheet": (j.get("frames") or [None])[0]}
        it["yt_title"] = it.get("yt_title") or j.get("title")
    elif SENSITIVE.search(it.get("moment_text", "")):
        why.append("transcript sensitive/graphic word: " + SENSITIVE.search(it["moment_text"]).group(0))
    ok, w2, met = screen_file(mp4)
    why += w2
    it["screen"] = {"ok": not why, "reasons": why, "metrics": met}
    return not why


# ---------------------------------------------------------------- gates
def gate_source(it, force=False):
    """Source gate. Returns True (pass), False (rejected; caller logs skip) or None (no vision verdict: needs_my_review)."""
    import source_gate as sg
    r = sg.check_source(it["id"], it.get("title", ""), it.get("channel", ""), force)
    it["gate"] = {k: r.get(k) for k in ("verdict", "pass", "watermark", "overlay_text", "gore_flag", "reason", "fail", "source", "model", "sheet")}
    if r.get("pass") is None:
        it["review_state"] = "needs_my_review"
        it["note"] = "source gate unavailable: " + (r.get("reason") or "")[:140]
        return None
    it.pop("review_state", None)
    return bool(r["pass"])


def gate_clip(it, mp4):
    import source_gate as sg
    r = sg.check_clip(mp4, it["id"], True)
    it["clip_gate"] = {k: r.get(k) for k in ("verdict", "pass", "watermark", "overlay_text", "gore_flag", "reason", "fail", "source", "model", "sheet")}
    return r.get("pass")


# ---------------------------------------------------------------- payloads
def payload(it):
    risk = it.get("risk", "?")
    cred = f"{it.get('credits', 0)} credits"
    text = (f"GTA 6 clip ready\n{it['yt_title']}\n\nSource: {it['channel']} ({int(it['subs']):,} subs) | rights risk: {risk}\n"
            f"Made: {it['made_by']} | {cred}\nText line on clip: {it.get('overlay_line', 'n/a')}\nPost = YouTube wrdgamingclipz + TikTok rvclips6, Via {it['channel']}\n{it['url']}"
            if it.get("subs") else f"GTA 6 clip ready\n{it['yt_title']}\n\nSource: {it['channel']} | rights risk: {risk}\nMade: {it['made_by']} | {cred}\n{it['url']}")
    return {"text": text, "media": it["files"]["mp4"], "buttons": [[{"label": "Post", "value": f"gta6post_{it['id']}"}, {"label": "Skip", "value": f"gta6skip_{it['id']}"}]]}


def channel_question(cid, ch, it):
    text = (f"New GTA 6 channel held, no clip made: {ch['name']} ({int(it['subs'] or 0):,} subs). Rights risk {it['risk']}: {'; '.join(it['risk_why'])}.\n"
            f"Example: {it['title'][:80]} {it['url']}\nClip this channel (own-stack, credit 'Via {ch['name']}') or ignore it?")
    return {"text": text, "buttons": [[{"label": "Clip it", "value": f"gta6chok_{cid}"}, {"label": "Ignore", "value": f"gta6chno_{cid}"}]]}


def tg(msg):
    print("TGSEND " + json.dumps(msg, ensure_ascii=False))


# ---------------------------------------------------------------- pipeline
def finished_today(s):
    today = now_et().strftime("%Y-%m-%d")
    return sum(1 for it in s["items"].values() if (it.get("made_at") or "")[:10] == today)


def cap_today(c):
    lw = c["launch_week"]
    d = now_et().strftime("%Y-%m-%d")
    return lw["cap"] if lw["start"] <= d <= lw["end"] else c["daily_cap"]


def pipeline(dry=False):
    c = cfg()
    s = load()
    items = s["items"]
    # 1. discovered -> risk/route
    for it in sorted([i for i in items.values() if i["stage"] == "discovered"], key=lambda i: -i.get("vph", 0)):
        ch = s["channels"].setdefault(it["cid"], {"name": it["channel"], "skips": 0})
        if it["spoiler"] or (BLOCK.search(it["title"]) and re.search(r"ending|spoiler|leak|cutscene|final mission|full movie|credits", it["title"], re.I)):
            log(it, "skipped", "auto: spoiler-risk / cutscene-ending title, never queued"); continue
        if ch.get("ignored"):
            log(it, "skipped", "auto: channel ignored"); continue
        it["risk"], it["risk_why"] = assess_risk(it, s)
        it["route"] = it.get("forced_route") or route_for(it, c)
        if it["risk"] != "low" and not ch.get("clip_ok"):
            it["hold"] = "channel_question"
            if not ch.get("question_sent"):
                if dry:
                    print(f"[dry-run] would ask channel question for {ch['name']} ({it['risk']}: {'; '.join(it['risk_why'])})")
                else:
                    ch["question_sent"] = True; ch["question_item"] = it["id"]
                    if cfg().get("channel_questions", False):
                        tg(channel_question(it["cid"], ch, it))
                    else:
                        ch["held_silent"] = True  # William only wants finished clips; held channels are listed on request
            continue
        it.pop("hold", None)
        if dry:
            print(f"[dry-run] {it['id']} {it['channel']} type={it['type']} risk={it['risk']} -> route {it['route']}"); continue
        log(it, "routed", f"{it['route']} risk={it['risk']} ({'; '.join(it['risk_why']) or 'no flags'})")
    # held items whose channel got clip_ok -> back to discovered handled in callback
    # 2. routed -> made -> screened -> awaiting_approval
    made_now = gated_now = 0
    cap = cap_today(c)
    for it in sorted([i for i in items.values() if i["stage"] == "routed"], key=lambda i: -i.get("vph", 0)):
        if made_now >= c["max_make_per_run"] and not it.get("opus_project"):
            continue
        if not it.get("opus_project") and finished_today(s) >= cap:
            continue
        if dry:
            g = it.get("gate")
            print(f"[dry-run] would make {it['id']} via {it['route']} (cap {finished_today(s)}/{cap}) source gate: "
                  + (f"{g['verdict']} pass={g['pass']}" if g else "not run yet (runs before any make/credit)")); continue
        if (it.get("gate") or {}).get("pass") is not True:
            if gated_now >= c.get("gate_max_per_run", 8):
                continue
            gated_now += 1
            gv = gate_source(it)
            if gv is None:
                save(s); continue  # needs_my_review: no vision verdict, nothing is made or spent
            if not gv:
                log(it, "skipped", f"source gate: {it['gate']['fail']} | {it['gate'].get('reason', '')}"); save(s); continue
        try:
            done = False
            if it["route"] == "own_cut":
                make_own_cut(it, c); done = True; made_now += 1
            elif it["route"] == "guide":
                done = make_guide(it, c); made_now += 1 if done else 0
            else:
                done = make_opus(it, c)
            if not done:
                save(s); continue
            it["made_at"] = now_et().isoformat(timespec="seconds")
            log(it, "made", it["how"])
            ok = screen(it)
            if not ok:
                log(it, "skipped", "auto-screen reject: " + "; ".join(it["screen"]["reasons"])); save(s); continue
            cg = gate_clip(it, it["files"]["mp4"])
            if cg is False:
                log(it, "skipped", f"clip gate: {it['clip_gate']['fail']} | {it['clip_gate'].get('reason', '')}"); save(s); continue
            log(it, "screened", json.dumps(it["screen"]["metrics"]))
            log(it, "awaiting_approval", "finished clip ready")
            held = sum(1 for x in s["items"].values() if x.get("review") in ("pending", "released"))
            if held < cfg().get("review_hold", 0) or cg is None:
                it["review"] = "pending"  # Morpheus reviews first batch; not sent to William until `release`
                log(it, "review_hold", "first-batch review, not sent to William yet" if cg is not None else "clip gate had no vision verdict: Morpheus must view the sheet")
            else:
                tg(payload(it)); it["sent_at"] = now_et().isoformat(timespec="seconds")
        except Exception as ex:  # noqa: BLE001
            it["fails"] = it.get("fails", 0) + 1
            it["last_error"] = str(ex)[:300]
            if it["fails"] >= 2:
                log(it, "skipped", "auto: make failed twice: " + it["last_error"])
        save(s)
    # 3. approved -> post when inside the window
    if not dry:
        for it in [i for i in items.values() if i["stage"] == "approved"]:
            lo, hi = c["posting_window_et"]
            if lo <= now_et().hour < hi:
                post_item(s, it, c)
                save(s)
    if not dry:
        save(s)


# ---------------------------------------------------------------- posting
def post_item(s, it, c, dry=False):
    """Publish via the existing direct paths. YouTube: yt_upload_gaming.py (own clips) or opus.py post (OpusClip clips).
    TikTok rvclips6: opus.py post (own clips are first uploaded as a no-clip OpusClip project via opus_upload.py, 1 credit)."""
    acc = c["accounts"]
    done = it.setdefault("posted", {})
    mp4 = it["files"]["mp4"]
    desc_f = os.path.join(OUTQ, f"{it['id']}.desc.txt")
    open(desc_f, "w").write(it["desc"])
    errs = []
    if dry:
        print(f"[dry-run] would post {it['id']} to YouTube + TikTok"); return
    if "yt" not in done:
        if it.get("opus_clip"):
            r = run([sys.executable, os.path.join(HERE, "..", "opusclip", "opus.py"), "post", it["opus_project"], it["opus_clip"], "--account", acc["yt_opus"],
                     "--title", it["yt_title"], "--desc", it["desc"], "--yes"], 300)
            ok = r.returncode == 0
        else:
            r = run([sys.executable, os.path.join(HERE, "yt_upload_gaming.py"), mp4, "--title", it["yt_title"], "--desc-file", desc_f, "--privacy", "public",
                     "--tags", ",".join(it.get("yt_tags") or make_tags(it, content_type(it), it["yt_title"]))], 900)
            ok = r.returncode == 0
        if ok:
            done["yt"] = (r.stdout.strip().splitlines() or ["ok"])[-1][:200]
        else:
            errs.append("YouTube: " + (r.stderr or r.stdout)[-200:])
    if "tiktok" not in done:
        try:
            proj, clip = it.get("opus_project"), it.get("opus_clip")
            if not proj:
                import opus
                import gaming_budget as gb
                r = run([sys.executable, os.path.join(HERE, "opus_upload.py"), mp4, "--title", it["yt_title"]], 900)
                m = re.search(r'"(?:id|projectId)":\s*"([^"]+)"', r.stdout)
                if not m:
                    raise RuntimeError("opus_upload: " + (r.stderr or r.stdout)[-200:])
                proj = m.group(1); it["tiktok_project"] = proj
                gb.record(it["id"], 1, "clip_queue tiktok no-clip upload")
                it["credits"] = (it.get("credits") or 0) + 1
                for _ in range(40):
                    if opus.call("GET", f"/api/clip-projects/{proj}").get("stage") == "COMPLETED":
                        break
                    time.sleep(15)
                res = opus.call("GET", f"/api/exportable-clips?q=findByProjectId&projectId={proj}")
                cl = res if isinstance(res, list) else res.get("data", [])
                if not cl:
                    raise RuntimeError("no clip in tiktok project yet")
                clip = cl[0]["id"]
            r = run([sys.executable, os.path.join(HERE, "..", "opusclip", "opus.py"), "post", proj, clip, "--account", acc["tiktok"],
                     "--title", it.get("tt_title") or fit_title(it["yt_title"], 70), "--desc", tiktok_caption(it), "--yes"], 300)
            if r.returncode != 0:
                raise RuntimeError((r.stderr or r.stdout)[-200:])
            done["tiktok"] = "ok"
        except Exception as ex:  # noqa: BLE001
            errs.append("TikTok: " + str(ex)[:200])
    if len(done) == 2:
        log(it, "posted", json.dumps(done))
        s["channels"][it["cid"]]["skips"] = 0
        tg({"text": f"Posted: {it['yt_title']}\nYouTube: {done['yt']}\nTikTok rvclips6: ok"})
    else:
        it["post_errors"] = errs
        tg({"text": f"Post partly failed for {it['yt_title']} (will retry next cycle): " + " | ".join(errs)})


# ---------------------------------------------------------------- callbacks
def callback(value):
    c = cfg()
    s = load()
    m = re.match(r"gta6(post|skip|chok|chno)_(.+)", value.strip())
    if not m:
        print("unknown callback"); return 1
    kind, key = m.groups()
    if kind in ("chok", "chno"):
        ch = s["channels"].get(key)
        if not ch:
            print("unknown channel"); return 1
        if kind == "chok":
            ch["clip_ok"] = True
            for it in s["items"].values():
                if it["cid"] == key and it["stage"] == "discovered":
                    it.pop("hold", None)
            print(f"{ch['name']}: will clip (own-stack, credited). Items re-enter routing next cycle.")
        else:
            ch["ignored"] = True
            run([sys.executable, os.path.join(HERE, "set_status.py"), key, "ignored"])
            print(f"{ch['name']}: ignored.")
        save(s); return 0
    it = s["items"].get(key)
    if not it:
        print("unknown clip id"); return 1
    if it["stage"] != "awaiting_approval":
        print(f"{it['id']} is {it['stage']}, nothing to do"); return 0
    ch = s["channels"][it["cid"]]
    if kind == "skip":
        log(it, "skipped", "william skip")
        ch["skips"] = ch.get("skips", 0) + 1
        msg = f"Skipped {it['yt_title']}."
        if ch["skips"] >= c["skips_to_ignore"]:
            ch["ignored"] = True
            run([sys.executable, os.path.join(HERE, "set_status.py"), it["cid"], "ignored"])
            msg += f" {ch['name']} skipped {ch['skips']}x: channel ignored."
        save(s); print(msg); return 0
    log(it, "approved", "william Post tap")
    lo, hi = c["posting_window_et"]
    if lo <= now_et().hour < hi:
        post_item(s, it, c)
        save(s)
    else:
        save(s)
        print(f"Approved {it['yt_title']}; outside 7 AM-11 PM ET, will post at the next window.")
    return 0


# ---------------------------------------------------------------- manual add / cli
def fetch_meta(url):
    fmt = "%(id)s\x1f%(title)s\x1f%(channel)s\x1f%(channel_id)s\x1f%(channel_follower_count)s\x1f%(duration)s\x1f%(age_limit)s\x1f%(view_count)s\x1f%(live_status)s"
    r = run([YTDLP, "--no-warnings", "--skip-download", "--print", fmt, url], 90)
    p = r.stdout.strip().split("\x1f")
    if len(p) < 9:
        raise RuntimeError("metadata failed: " + r.stderr[-200:])
    num = lambda x: float(x) if x not in ("NA", "None", "") else None
    return {"id": p[0], "title": p[1], "channel": p[2], "cid": p[3], "subs": num(p[4]), "dur": num(p[5]), "age_restricted": (num(p[6]) or 0) >= 18,
            "views": num(p[7]), "live": p[8] == "is_live", "spoiler": bool(re.search(r"ending|spoiler|leak|all cutscenes|full movie", p[1], re.I)),
            "type": "other", "vph": 0}


def show(key=None):
    s = load()
    for it in ([s["items"][key]] if key else s["items"].values()):
        print(f"{it['id']} [{it['stage']}] {it['channel']} | {it.get('route')} risk={it.get('risk')} | {it.get('made_by')} cr={it.get('credits')} | {it['title'][:60]}")
        if key:
            print(json.dumps(it, indent=1, ensure_ascii=False))


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    dry = "--dry-run" in a
    cmd = a[0]
    os.makedirs(OUTQ, exist_ok=True)
    lock = open(os.path.join(HERE, ".clip_queue.lock"), "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return 0  # previous cycle still running: stay silent
    if cmd == "cycle":
        import gta6_discovery as gd
        alerts, errors, nq, nf = gd.scan(None, False, dry)
        if dry:
            print(f"[dry-run] {nq} queries, {nf} relevant videos, {len(errors)} errors (state not written)")
        for al in alerts:
            print(al)  # only non-queue alerts (none by default)
        if errors and len(errors) >= nq:
            print(f"GTA6 DISCOVERY ERROR: {len(errors)}/{nq} queries failed: {errors[0]}")
        pipeline(dry)
    elif cmd == "run":
        pipeline(dry)
    elif cmd == "add":
        e = fetch_meta(a[1])
        e["type"] = next((t for t, pat in __import__("gta6_discovery").TYPES if re.search(pat, e["title"], re.I)), "other")
        route = a[a.index("--route") + 1] if "--route" in a else None
        print(enqueue(e, dry, route))
        pipeline(dry)
    elif cmd == "callback":
        return callback(a[1])
    elif cmd == "payload":
        s = load(); tg(payload(s["items"][a[1]]))
    elif cmd == "release":
        s = load()
        ids = [i for i, x in s["items"].items() if x.get("review") == "pending"] if a[1] == "all" else [a[1]]
        for i in ids:
            it = s["items"][i]; it["review"] = "released"; it["sent_at"] = now_et().isoformat(timespec="seconds")
            tg(payload(it))
        save(s)
    elif cmd == "gate":
        s = load()
        force = "--force" in a
        ids = [x for x in a[1:] if not x.startswith("--")]
        if not ids or ids == ["all"]:
            ids = [i for i, x in s["items"].items() if x["stage"] in ("discovered", "routed")]
        for i in ids:
            it = s["items"].get(i)
            if not it:
                print(f"{i}: not in queue"); continue
            gv = gate_source(it, force)
            if gv is False and it["stage"] in ("discovered", "routed"):
                log(it, "skipped", f"source gate: {it['gate']['fail']} | {it['gate'].get('reason', '')}")
            g = it["gate"]
            print(f"{i} | {'PASS' if gv else 'REJECT' if gv is False else 'NEEDS_MY_REVIEW'} | {g['verdict']} wm={g['watermark']} text={g['overlay_text']} gore={g['gore_flag']} | {it['title'][:40]} | {g['reason']}")
            save(s)
    elif cmd == "pending":
        s = load()
        held = [x for x in s["items"].values() if x.get("review") == "pending"]
        print(f"{len(held)} finished clip(s) held for Morpheus review (release with: clip_queue.py release ID|all)")
        for it in held:
            cg, g = it.get("clip_gate") or {}, it.get("gate") or {}
            print(f"\n{it['id']} | {it.get('yt_title')} | {it['channel']} | stage {it['stage']}\n  mp4: {(it.get('files') or {}).get('mp4')}\n  clip sheet: {cg.get('sheet')}\n  clip gate: {cg.get('verdict')} wm={cg.get('watermark')} text={cg.get('overlay_text')} gore={cg.get('gore_flag')} | {cg.get('reason')}"
                  f"\n  source sheet: {g.get('sheet')}\n  source gate: {g.get('verdict')} wm={g.get('watermark')} text={g.get('overlay_text')} | {g.get('reason')}\n  overlay line: {it.get('overlay_line')}")
        nm = [x for x in s["items"].values() if x.get("review_state") == "needs_my_review" and x["stage"] in ("discovered", "routed")]
        if nm:
            print(f"\n{len(nm)} source(s) need Morpheus' own look (no vision verdict; sheet in out/queue/review/):")
            for it in nm:
                print(f"  {it['id']} | {it['title'][:50]} | {(it.get('gate') or {}).get('sheet')} | {it.get('note')}")
    elif cmd == "show":
        show(a[1] if len(a) > 1 else None)
    else:
        sys.exit(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
