#!/usr/bin/env python3
"""Prefilter a long VOD for streamer-reaction moments. Calls no LLM, posts nothing, costs no credits.

  moment_pick.py VIDEO_ID_OR_URL [--top 14] [--window 30] [--out DIR] [--audio] [--chat] [--gap 180]

--audio merges OUT/<id>.audio.json (signals_audio.py) with the transcript score and ranks windows by AGREEMENT: flags
T (transcript reaction z>=1.5) and A (audio z>=1.5); a window flagged in both outranks one flagged in only one. --chat
merges OUT/<id>.chat.json (signals_chat.py, flag C). Merged picks are >= --gap seconds apart (default 180).

Downloads the English auto-subs (json3) with yt-dlp, builds word-timestamp windows, scores them for the streamer's own
energy (lowercase conversational talk, 'yo/bro/no way', laughter, rapid speech, repeated words) and down-weights
game-subtitle text (long ALL-CAPS runs, '>>' speaker changes). Writes OUT/<id>.moments.json with the top
non-overlapping windows (start/end/score/text) and prints a numbered list. The agent reads it and writes picks.json:
  [{"start":2850,"end":2885,"why":"...","title":"..."}]
"""
import argparse, bisect, glob, json, os, re, subprocess, sys

YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"
HERE = os.path.dirname(os.path.abspath(__file__))

REACT = re.compile(r"\b(yo+|bro+|brother|no way|did you see|did you just|what the|oh my god|omg|dude|bruh|holy|crazy|insane|"
                   r"are you kidding|i can'?t believe|let'?s go+|wait wait|look at this|look at that|they just|he just|she just|"
                   r"что|nah|hell nah|no no|oh no|what is that|what was that|that'?s (so )?(crazy|insane|wild)|my god|chat)\b", re.I)
LAUGH = re.compile(r"\[(laughter|laughing)\]|\b(ha ?ha|hehe|lmao|lol)\b", re.I)
BLEEP = "[ __ ]"


def video_id(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|live/)([\w-]{11})", s)
    return m.group(1) if m else s.strip()


def fetch_subs(vid, out):
    os.makedirs(out, exist_ok=True)
    existing = glob.glob(os.path.join(out, f"{vid}.en*.json3"))
    for langs in ([] if existing else ["en", "en-orig"]):  # some uploads only expose the original track as en-orig
        subprocess.run([YTDLP, "--no-warnings", "--ignore-no-formats-error", "--skip-download", "--write-auto-subs",
                        "--sub-langs", langs, "--sub-format", "json3", "-o", os.path.join(out, "%(id)s"),
                        f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True, timeout=300)
        existing = glob.glob(os.path.join(out, f"{vid}.en*.json3"))
        if existing:
            break
    return sorted(existing)[0] if existing else None


def words_from_json3(path):
    ws = []
    for ev in json.load(open(path)).get("events", []):
        if "segs" not in ev:
            continue
        base = ev["tStartMs"] / 1000
        for sg in ev["segs"]:
            t = sg.get("utf8", "")
            if not t.strip():
                continue
            ws.append((base + sg.get("tOffsetMs", 0) / 1000, t.strip()))
    return ws


def clean(w):
    return re.sub(r"^[>\s]+|[^\w'\[\] _-]+$", "", w)


def is_caps(w):
    c = re.sub(r"[^A-Za-z]", "", w)
    return len(c) >= 2 and c.isupper() or w in ("I", "A") and False


def tag_scripted(words):
    """Mark words that look like game subtitles: caps runs of 4+, and text following '>>' that is caps."""
    n = len(words)
    caps = [is_caps(w) for _, w in words]
    scripted = [False] * n
    i = 0
    while i < n:
        if caps[i]:
            j = i
            while j < n and (caps[j] or words[j][1] in (BLEEP, "[", "__", "]")):
                j += 1
            if j - i >= 4:
                for k in range(i, j):
                    scripted[k] = True
            i = max(j, i + 1)
        else:
            i += 1
    return scripted


def score_window(ws, sc, dur):
    toks = [w for _, w in ws]
    n = len(toks)
    if n < 8:
        return 0.0, {"scripted_frac": 0}
    text = " ".join(toks)
    scripted_frac = sum(sc) / n
    low = sum(1 for w in toks if re.sub(r"[^A-Za-z]", "", w) and re.sub(r"[^A-Za-z]", "", w).islower()) / n
    speaker = text.count(">>")
    react = len(REACT.findall(text))
    laugh = len(LAUGH.findall(text))
    bleeps = text.count(BLEEP)
    rate = n / dur
    norm = [clean(w).lower() for w in toks]
    rep = sum(1 for a, b in zip(norm, norm[1:]) if a and a == b)
    excl = text.count("!") + text.count("?")
    s = 0.0
    s += min(react, 8) * 3.0
    s += min(laugh, 4) * 3.0
    s += min(rep, 10) * 0.8
    s += max(0.0, rate - 2.0) * 4.0
    s += low * 6.0
    s += min(bleeps, 6) * 0.7
    s += min(excl, 6) * 0.3
    s -= scripted_frac * 14.0
    s -= min(speaker, 10) * 1.0
    return round(s, 2), {"scripted_frac": round(scripted_frac, 2), "react": react, "laugh": laugh, "rep": rep,
                         "wps": round(rate, 2), "speaker_changes": speaker}


def pick(words, window, top):
    sc = tag_scripted(words)
    end = words[-1][0]
    cands = []
    t = 0.0
    idx0 = 0
    while t < end:
        while idx0 < len(words) and words[idx0][0] < t:
            idx0 += 1
        idx1 = idx0
        while idx1 < len(words) and words[idx1][0] < t + window:
            idx1 += 1
        seg = words[idx0:idx1]
        if seg:
            s, f = score_window(seg, sc[idx0:idx1], window)
            cands.append((s, t, f, seg))
        t += 5.0
    cands.sort(key=lambda c: -c[0])
    chosen = []
    for s, t, f, seg in cands:
        if s <= 0:
            break
        if all(abs(t - c["start"]) >= window for c in chosen):
            txt = " ".join(w for _, w in seg).replace(BLEEP, "[bleep]")
            if len(txt) > 330:
                txt = txt[:327] + "..."
            chosen.append({"start": round(seg[0][0], 1), "end": round(t + window, 1), "score": s, "flags": f, "text": txt})
        if len(chosen) >= top:
            break
    chosen.sort(key=lambda c: -c["score"])
    return chosen, sum(sc) / len(sc)


def zs(x):
    import statistics
    med = statistics.median(x)
    mad = statistics.median([abs(v - med) for v in x]) * 1.4826
    if mad < 1e-9:
        mad = (statistics.pstdev(x) or 1e-9)
    return [(v - med) / mad for v in x]


def pick_merged(words, window, top, audio, chat, gap):
    """Rank audio-hop windows by transcript z + audio z (+ chat z) with an agreement bonus; spread picks >= gap s."""
    sc = tag_scripted(words)
    times = [w[0] for w in words]
    hop = audio["hop"]
    arows = {r[0]: r for r in audio["windows"]}
    crow = {r[0]: r for r in chat["windows"]} if chat else {}
    starts = sorted(arows)
    tsc, meta = [], []
    for t in starts:
        i0 = bisect.bisect_left(times, t)
        i1 = bisect.bisect_left(times, t + window)
        if i1 - i0 >= 8:
            s, f = score_window(words[i0:i1], sc[i0:i1], window)
        else:
            s, f = 0.0, {"scripted_frac": 0}
        tsc.append(s)
        meta.append((i0, i1, f))
    tz = zs(tsc)
    out = []
    for k, t in enumerate(starts):
        i0, i1, f = meta[k]
        az = arows[t][1]
        cz = 0.0
        if crow:
            cr = crow.get(int(t // 30 * 30))
            cz = cr[3] if cr else 0.0
        flags = ("T" if tz[k] >= 1.5 else "-") + ("A" if az >= 1.5 else "-") + (("C" if cz >= 1.5 else "-") if crow else "")
        pos = [max(tz[k], 0), max(az, 0)] + ([max(cz, 0)] if crow else [])
        agree = sorted(pos)[-2] if len(pos) > 1 else 0
        comb = tz[k] + az + (cz if crow else 0) + 2.0 * agree
        if f.get("scripted_frac", 0) > 0.5:
            comb -= 4.0
        out.append((comb, t, flags, tz[k], az, f, i0, i1))
    out.sort(key=lambda r: -r[0])
    chosen = []
    for comb, t, flags, tzv, azv, f, i0, i1 in out:
        if all(abs(t - c["start"]) >= gap for c in chosen):
            txt = " ".join(w for _, w in words[i0:i1]).replace(BLEEP, "[bleep]")
            chosen.append({"start": float(t), "end": float(t + window), "score": round(comb, 2), "flags": f, "sig": flags,
                           "tz": round(tzv, 1), "az": round(azv, 1), "text": txt[:140]})
        if len(chosen) >= top:
            break
    return chosen, sum(sc) / len(sc)


def fmt(t):
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def drop_reason(v):
    if v["black"] > 0.40:
        return f"{v['black']:.0%} black frames"
    if v["static"] > 0.60:
        return f"{v['static']:.0%} static/menu frames"
    if v["black"] + v["static"] > 0.60:
        return f"black+static {v['black'] + v['static']:.0%}"
    if v["motion"] < 0.012 and v["p90"] < 0.03:
        return "almost no motion"
    return None


def apply_visual(chosen, vid, out):
    """Merge visual features: V flag = strong motion (visual_score>=1.1); score += 8*(vs-0.9); drop black/static windows."""
    vp = os.path.join(out, f"{vid}.visual.json")
    if not os.path.exists(vp):
        print(f"VISUAL_MISSING: run visual_check.py {vid} --moments out/{vid}.moments.json first"); sys.exit(2)
    vis = {round(w["start"]): w for w in json.load(open(vp))["windows"] if "error" not in w}
    rows = []
    for c in chosen:
        v = vis.get(round(c["start"]))
        r = dict(c)
        if v is None:
            r.update(visual_score=None, dropped="no visual data", vflag="?", final=c["score"], frames=[])
        else:
            why = drop_reason(v)
            vs = v["visual_score"]
            r.update(visual_score=vs, features={k: v[k] for k in ("motion", "p90", "cuts", "black", "static", "flat", "static_run_s", "cam_ratio")},
                     frames=v["frames"], dropped=why, vflag="V" if vs >= 1.1 else "-", final=round(c["score"] + 8 * (vs - 0.9), 2))
        r["sig"] = r["sig"] + r["vflag"]
        rows.append(r)
    rows.sort(key=lambda r: (r.get("dropped") is not None, -r["final"]))
    json.dump({"video": vid, "ranked": rows}, open(os.path.join(out, f"{vid}.visual_rank.json"), "w"), separators=(",", ":"))
    n = 0
    print(f"{vid}: visual-merged ranking (T transcript, A audio, V visual; final = score + 8*(vs-0.9))")
    for r in rows:
        if r.get("dropped"):
            print(f" X  {fmt(r['start'])} [{r['start']:.0f}] {r['sig']} DROPPED ({r['dropped']}): {r['text'][:70]}")
        else:
            n += 1
            f = r["features"]
            print(f"{n:>2}. {fmt(r['start'])} [{r['start']:.0f}] {r['sig']} final={r['final']} (was {r['score']}) vs={r['visual_score']} mot={f['motion']} blk={f['black']} sta={f['static']}: {r['text'][:80]}")
    print("wrote", os.path.join(out, f"{vid}.visual_rank.json"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--top", type=int, default=14)
    ap.add_argument("--window", type=int, default=30)
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--audio", action="store_true", help="merge out/ID.audio.json")
    ap.add_argument("--chat", action="store_true", help="merge out/ID.chat.json")
    ap.add_argument("--gap", type=int, default=180, help="min seconds between merged picks")
    ap.add_argument("--visual", action="store_true", help="merge out/ID.visual.json (visual_check.py): drop black/static windows, boost motion")
    a = ap.parse_args()
    vid = video_id(a.video)
    path = fetch_subs(vid, a.out)
    if not path:
        print(f"MOMENT_PICK_NO_TRANSCRIPT {vid}: no English auto-subs; pick moments by hand or skip this VOD.")
        sys.exit(2)
    words = words_from_json3(path)
    if len(words) < 200:
        print(f"MOMENT_PICK_NO_TRANSCRIPT {vid}: only {len(words)} words in transcript.")
        sys.exit(2)
    if a.audio or a.chat:
        audio = chat = None
        if a.audio:
            ap_ = os.path.join(a.out, f"{vid}.audio.json")
            if not os.path.exists(ap_):
                print(f"AUDIO_MISSING: run signals_audio.py {vid} first"); sys.exit(2)
            audio = json.load(open(ap_))
        if a.chat:
            cp_ = os.path.join(a.out, f"{vid}.chat.json")
            if os.path.exists(cp_):
                chat = json.load(open(cp_))
            else:
                print("CHAT_UNAVAILABLE (no chat.json); continuing without chat")
        if audio is None:
            audio = {"hop": 10, "windows": [[t, 0.0, 0, 0, 0] for t in range(0, int(words[-1][0]), 10)]}
        chosen, scripted = pick_merged(words, a.window, a.top, audio, chat, a.gap)
        if a.visual:
            apply_visual(chosen, vid, a.out)
            return
        warn = f"MOSTLY_SCRIPTED: {scripted:.0%} of words look like game subtitles." if scripted > 0.35 else None
        outp = os.path.join(a.out, f"{vid}.moments.json")
        json.dump({"video": vid, "window": a.window, "merged": True, "scripted_fraction": round(scripted, 2),
                   "warning": warn, "moments": chosen}, open(outp, "w"), separators=(",", ":"))
        print(f"{vid}: {len(words)} words, {fmt(words[-1][0])} long, scripted {scripted:.0%}; flags T=transcript A=audio" + (" C=chat" if chat else "") + (f"\n{warn}" if warn else ""))
        for i, c in enumerate(chosen, 1):
            print(f"{i:>2}. {fmt(c['start'])} [{c['start']:.0f}] {c['sig']} sc={c['score']} t{c['tz']} a{c['az']} scr={c['flags']['scripted_frac']}: {c['text'][:110]}")
        print("wrote", outp)
        return
    chosen, scripted = pick(words, a.window, a.top)
    warn = None
    if scripted > 0.35:
        warn = f"MOSTLY_SCRIPTED: {scripted:.0%} of words look like game subtitles; picks are unreliable, verify with frames."
    outp = os.path.join(a.out, f"{vid}.moments.json")
    json.dump({"video": vid, "window": a.window, "scripted_fraction": round(scripted, 2), "warning": warn,
               "moments": chosen}, open(outp, "w"), separators=(",", ":"))
    print(f"{vid}: {len(words)} words, {fmt(words[-1][0])} long, scripted {scripted:.0%}" + (f"\n{warn}" if warn else ""))
    for i, c in enumerate(chosen, 1):
        f = c["flags"]
        print(f"{i:>2}. {fmt(c['start'])}-{fmt(c['end'])} [{c['start']:.0f}-{c['end']:.0f}] sc={c['score']} scr={f['scripted_frac']}: {c['text'][:200]}")
    print("wrote", outp)


if __name__ == "__main__":
    main()
