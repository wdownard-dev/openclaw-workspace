#!/usr/bin/env python3
"""Real-footage gate for the GTA 6 clip queue: vision-classify a contact sheet of the SOURCE video (before a clip is made or any
OpusClip credit is spent) and of the FINISHED clip. Posts/uploads/spends nothing except one tiny Gemini call per new source.

  source_gate.py ID_OR_URL [--force] [--title T --channel C]    gate one source (cached per video id)
  source_gate.py --clip MP4 [--name NAME] [--force]             gate a finished clip (contact sheet from the mp4)

Source sheet: yt-dlp storyboard sb0 (320x180 thumbnails, a few small image fragments, NO video download, ~5 s), 10 frames spread
over 5-95% of the video, 5x2 grid. Clip sheet: 8 frames from the mp4, 4x2 grid. Classifier: Gemini (GEMINI_API_KEY from env, the
same key the bluepill pipeline uses; flash-lite class model, ~2k tokens/call, well under $0.01). If no vision API is usable the
verdict is 'unavailable' (pass=None): the sheet is still written to out/queue/review/ and the queue marks the item
'needs_my_review' for Morpheus. Nothing passes without a real_gameplay verdict.

Returns/stores: {verdict, has_burned_in_watermark, watermark ('none'|'small'|'prominent'), has_overlay_text, overlay_text
('none'|'light'|'heavy'), gore_flag, reason, pass, source ('gemini'|'unavailable'), model, sheet, kind}. Cache: out/queue/gate/<id>.<kind>.json
"""
import base64, email, io, json, math, os, re, shutil, subprocess, sys, tempfile, urllib.request
from email import policy

HERE = os.path.dirname(os.path.abspath(__file__))
OUTQ = os.path.join(HERE, "out", "queue")
GATE_DIR = os.path.join(OUTQ, "gate")
REVIEW_DIR = os.path.join(OUTQ, "review")
YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"
FFMPEG = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")
MODELS = ["gemini-3.1-pro-preview", "gemini-3.1-flash-lite"]
MODELS_STRONG = ["gemini-3.1-pro-preview", "gemini-3.1-flash-lite"]  # finished clips get the stronger model first
VERDICTS = ["real_gameplay", "concept_or_trailer", "explainer_or_graphics", "news_or_talking_head", "other_game",
            "watermarked_third_party", "unclear"]

PROMPT_COMMON = """You are screening video for a GTA 6 clips channel that may only post REAL GTA 6 in-game footage (actual gameplay or
the game's own rendered footage, third-person/driving/free-roam). The image is a contact sheet of frames sampled evenly across the
video (left to right, top to bottom). {extra}
Classify the WHOLE video with exactly one verdict:
- real_gameplay: most frames are real in-engine game footage of GTA 6 (characters Jason/Lucia, Vice City, HUD, driving, on foot).
- concept_or_trailer: official trailer cuts, cinematic/CGI, fan concept or fan-made renders, AI-generated footage, key art.
- explainer_or_graphics: illustrations, slides, maps, infographics, thumbnails-as-frames, branded explainer graphics, stock/AI images.
- news_or_talking_head: news roundups, tweet/article/screenshot overlays, commentators, facecam, studio, reaction, real-world footage.
- other_game: footage of a different game (GTA V/Online, RDR2, Fortnite, etc).
- watermarked_third_party: gameplay but a big third-party watermark/logo/banner/frame dominates it.
- unclear: cannot tell.
Also report: watermark = none | small | prominent (a burned-in channel/brand/logo/handle on frames: 'small' = tiny corner bug,
'prominent' = large, repeated on every frame, or banner); overlay_text = none | light | heavy (burned-in captions, tweet cards,
headlines, lower-thirds; 'heavy' = on many frames or covering a large area); gore_flag = true only for visible blood or graphic injury.
mixed_footage = true if ANY frame (even one or two) shows something other than real in-engine GTA 6 footage: GTA V/other-game frames, key art,
promo/ad art, stock or real-world footage, a facecam, an app/UI mock-up, or a tweet/article card. Look at EVERY frame individually.
Be strict: when in doubt between real_gameplay and anything else, do not choose real_gameplay.
Reply with ONLY JSON: {{"verdict": "...", "watermark": "none|small|prominent", "overlay_text": "none|light|heavy", "gore_flag": false, "mixed_footage": false, "reason": "one short line"}}"""

EXTRA_SOURCE = "Context: this is the source video the clip would be cut from."
EXTRA_CLIP = ("Context: this is a FINISHED vertical clip. Ignore the clip's own yellow-on-dark caption bar near the top (we add it); "
              "also ignore plain word-by-word subtitle captions (white/green/yellow text near the bottom or centre); do NOT count those as overlay text. Judge the underlying footage: classify by what the frames show, and flag watermarks, tweet/article cards, facecams and any non-GTA 6 frames.")


def sh(cmd, timeout=120):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def vid_of(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", s)
    return m.group(1) if m else s


# ------------------------------------------------------------------ sheets
def source_sheet(vid, n=10):
    """10 frames across the video from the sb0 storyboard (320x180 tiles, 3x3 per fragment jpg; no video download)."""
    import concurrent.futures as cf
    from PIL import Image
    os.makedirs(REVIEW_DIR, exist_ok=True)
    r = sh([YTDLP, "--no-warnings", "-j", f"https://www.youtube.com/watch?v={vid}"], 120)
    try:
        j = json.loads(r.stdout)
    except Exception:  # noqa: BLE001
        j = None
    if j is None or "sb0" not in {x.get("format_id") for x in j.get("formats", [])}:
        if j is None:
            raise RuntimeError("no metadata (unavailable?): " + (r.stderr or "")[-120:].replace("\n", " "))
        return stream_sheet(vid, j, n)  # live / just-ended stream with no storyboard: sample the stream directly
    f = next(x for x in j["formats"] if x["format_id"] == "sb0")
    frags = f["fragments"]
    cols, rows = f.get("columns") or 3, f.get("rows") or 3
    per = cols * rows
    step = frags[0]["duration"] / per
    total = min(len(frags) * per, max(4, math.ceil((j.get("duration") or len(frags) * frags[0]["duration"]) / step)))
    want = sorted({min(total - 1, int(total * (0.05 + 0.90 * i / (n - 1)))) for i in range(n)})
    need = sorted({i // per for i in want})
    get = lambda k: (k, urllib.request.urlopen(frags[k]["url"], timeout=30).read())
    with cf.ThreadPoolExecutor(4) as ex:
        imgs = {k: Image.open(io.BytesIO(d)).convert("RGB") for k, d in ex.map(get, need)}
    tw, th = f.get("width") or 320, f.get("height") or 180
    sheet = Image.new("RGB", (tw * 5, th * math.ceil(len(want) / 5)), (0, 0, 0))
    for k, i in enumerate(want):
        im, t = imgs[i // per], i % per
        sheet.paste(im.crop(((t % cols) * tw, (t // cols) * th, (t % cols) * tw + tw, (t // cols) * th + th)), ((k % 5) * tw, (k // 5) * th))
    path = os.path.join(REVIEW_DIR, f"{vid}.source.jpg")
    sheet.save(path, quality=82)
    return path


def stream_sheet(vid, j, n=10, budget=55):
    """No storyboard (live or just-ended stream): resolve a <=360p HLS playlist with yt-dlp, pick n segments spread across it (live: the
    whole DVR window, newest 10 s excluded; ended: 5-95%), download ONLY those ~2 s segments with urllib, and pull one frame from each with
    the static ffmpeg (it segfaults on network URLs, so it only ever reads local files). Builds the same 5x2 sheet of 320x180 tiles as the
    storyboard path. Never downloads the whole video; temp dir is removed. Raises on failure (caller -> needs_my_review)."""
    import concurrent.futures as cf, time
    from PIL import Image
    t0 = time.time()
    fmts = [x for x in j.get("formats", []) if x.get("vcodec") not in (None, "none") and x.get("url") and (x.get("height") or 0) <= 360
            and str(x.get("protocol", "")).startswith("m3u8")]
    if not fmts:
        raise RuntimeError("no <=360p HLS format to sample (live_status=%s)" % j.get("live_status"))
    fmts.sort(key=lambda x: ((x.get("height") or 0), x.get("tbr") or 0), reverse=True)
    pl = urllib.request.urlopen(urllib.request.Request(fmts[0]["url"], headers={"User-Agent": "Mozilla/5.0"}), timeout=20).read().decode()
    segs, init = [], None
    for ln in pl.splitlines():
        if ln.startswith("#EXT-X-MAP:"):
            m = re.search(r'URI="([^"]+)"', ln)
            init = m.group(1) if m else None
        elif ln and not ln.startswith("#"):
            segs.append(ln.strip())
    if len(segs) < n:
        raise RuntimeError(f"playlist has only {len(segs)} segments")
    usable = len(segs) - (5 if j.get("live_status") == "is_live" else 0)  # skip the live edge (not yet reliably cached)
    idx = sorted({min(usable - 1, int(usable * (0.05 + 0.90 * i / (n - 1)))) for i in range(n)})
    tw, th = 320, 180
    td = tempfile.mkdtemp(prefix="gate_stream_")
    try:
        initb = urllib.request.urlopen(init, timeout=20).read() if init else b""

        def grab(k):
            i = idx[k]
            if time.time() - t0 > budget:
                return k, None
            try:
                data = urllib.request.urlopen(urllib.request.Request(segs[i], headers={"User-Agent": "Mozilla/5.0"}), timeout=20).read()
                seg = os.path.join(td, f"{k}.seg")
                open(seg, "wb").write(initb + data)
                out = os.path.join(td, f"{k}.jpg")
                sh([FFMPEG, "-y", "-loglevel", "error", "-i", seg, "-ss", "0.7", "-frames:v", "1", "-vf",
                    f"scale={tw}:{th}:force_original_aspect_ratio=decrease,pad={tw}:{th}:(ow-iw)/2:(oh-ih)/2", out], 20)
                if not (os.path.exists(out) and os.path.getsize(out) > 500):  # segment shorter than 0.7 s: first frame
                    sh([FFMPEG, "-y", "-loglevel", "error", "-i", seg, "-frames:v", "1", "-vf",
                        f"scale={tw}:{th}:force_original_aspect_ratio=decrease,pad={tw}:{th}:(ow-iw)/2:(oh-ih)/2", out], 20)
                return k, out if os.path.exists(out) and os.path.getsize(out) > 500 else None
            except Exception:  # noqa: BLE001
                return k, None
        with cf.ThreadPoolExecutor(5) as ex:
            got = dict(ex.map(grab, range(len(idx))))
        frames = [got[k] for k in range(len(idx)) if got.get(k)]
        if len(frames) < 4:
            raise RuntimeError(f"stream sampling got only {len(frames)}/{len(idx)} frames")
        sheet = Image.new("RGB", (tw * 5, th * math.ceil(len(frames) / 5)), (0, 0, 0))
        for k, fp in enumerate(frames):
            sheet.paste(Image.open(fp).convert("RGB"), ((k % 5) * tw, (k // 5) * th))
        os.makedirs(REVIEW_DIR, exist_ok=True)
        path = os.path.join(REVIEW_DIR, f"{vid}.source.jpg")
        sheet.save(path, quality=82)
        return path
    finally:
        shutil.rmtree(td, ignore_errors=True)


def clip_sheet(mp4, name, n=8):
    """8 frames from the finished clip, 4x2 grid of 216x384."""
    from PIL import Image
    os.makedirs(REVIEW_DIR, exist_ok=True)
    r = sh([FFMPEG, "-i", mp4], 30)  # static ffmpeg has no ffprobe; parse Duration from stderr
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", (r.stderr or "") + (r.stdout or ""))
    dur = (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))) if m else 30.0
    sheet = Image.new("RGB", (216 * 4, 384 * 2), (0, 0, 0))
    with tempfile.TemporaryDirectory() as td:
        for i in range(n):
            f = os.path.join(td, f"{i}.jpg")
            sh([FFMPEG, "-y", "-loglevel", "error", "-ss", f"{dur * (i + 0.5) / n:.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=216:384", f], 60)
            if os.path.exists(f):
                sheet.paste(Image.open(f).convert("RGB"), ((i % 4) * 216, (i // 4) * 384))
    path = os.path.join(REVIEW_DIR, f"{name}.clip.jpg")
    sheet.save(path, quality=85)
    return path


# ------------------------------------------------------------------ classifier
def gemini(sheet, extra, title="", channel=""):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not in env")
    prompt = PROMPT_COMMON.format(extra=extra)
    if title:
        prompt += f"\nVideo title (claimed, do not trust): {title[:120]} | channel: {channel[:60]}"
    body = {"contents": [{"parts": [{"text": prompt}, {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(open(sheet, "rb").read()).decode()}}]}],
            "generationConfig": {"temperature": 0, "responseMimeType": "application/json", "maxOutputTokens": 2500}}
    err = None
    for model in (MODELS_STRONG if "FINISHED vertical clip" in extra else MODELS):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        for attempt in range(2):
            try:
                req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json"})
                resp = json.load(urllib.request.urlopen(req, timeout=60))
                txt = resp["candidates"][0]["content"]["parts"][0]["text"]
                j = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
                j["model"] = model
                return j
            except Exception as ex:  # noqa: BLE001
                err = f"{model}: {str(ex)[:120]}"
                if "429" in str(ex) or "503" in str(ex):
                    import time; time.sleep(8)
                    continue
                break
    raise RuntimeError(err or "gemini failed")


def judge(j):
    """Normalise model JSON and apply the pass rule. Only real_gameplay without prominent watermark / heavy overlay / gore passes."""
    v = j.get("verdict") if j.get("verdict") in VERDICTS else "unclear"
    wm = j.get("watermark") if j.get("watermark") in ("none", "small", "prominent") else "none"
    ot = j.get("overlay_text") if j.get("overlay_text") in ("none", "light", "heavy") else "none"
    out = {"verdict": v, "watermark": wm, "has_burned_in_watermark": wm != "none", "overlay_text": ot, "has_overlay_text": ot != "none",
           "gore_flag": bool(j.get("gore_flag")), "mixed_footage": bool(j.get("mixed_footage")), "reason": str(j.get("reason", ""))[:200], "source": "gemini", "model": j.get("model")}
    why = []
    if v != "real_gameplay":
        why.append(v)
    if wm == "prominent":
        why.append("prominent watermark")
    if ot == "heavy":
        why.append("heavy overlay text")
    if out["gore_flag"]:
        why.append("gore")
    if out["mixed_footage"]:
        why.append("mixed footage (non-GTA6 or promo frames)")
    out["pass"] = not why
    out["fail"] = ", ".join(why)
    return out


def _run(kind, key, sheet_fn, extra, force, title="", channel=""):
    os.makedirs(GATE_DIR, exist_ok=True)
    cache = os.path.join(GATE_DIR, f"{key}.{kind}.json")
    if not force and os.path.exists(cache):
        r = json.load(open(cache)); r["cached"] = True
        return r
    try:
        sheet = sheet_fn()
    except Exception as ex:  # noqa: BLE001
        return {"verdict": "unclear", "pass": None, "source": "unavailable", "kind": kind, "reason": "sheet failed: " + str(ex)[:160],
                "fail": "sheet failed", "sheet": None}
    try:
        r = judge(gemini(sheet, extra, title, channel))
    except Exception as ex:  # noqa: BLE001
        # conservative fallback: no verdict. Morpheus reviews the sheet; nothing passes automatically.
        return {"verdict": "unclear", "pass": None, "source": "unavailable", "kind": kind, "sheet": sheet,
                "reason": "vision API unusable: " + str(ex)[:140], "fail": "no vision verdict"}
    r["kind"], r["sheet"] = kind, sheet
    json.dump(r, open(cache, "w"), indent=1)
    return r


def check_source(vid, title="", channel="", force=False):
    return _run("source", vid, lambda: source_sheet(vid), EXTRA_SOURCE, force, title, channel)


def check_clip(mp4, name, force=False):
    return _run("clip", name, lambda: clip_sheet(mp4, name), EXTRA_CLIP, force)


def summary(r):
    return (f"{r['verdict']} wm={r.get('watermark', '?')} text={r.get('overlay_text', '?')} gore={r.get('gore_flag', '?')} | {r.get('reason', '')}")[:230]


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    force = "--force" in a
    arg = lambda f: a[a.index(f) + 1] if f in a else ""
    if a[0] == "--clip":
        r = check_clip(a[1], arg("--name") or os.path.splitext(os.path.basename(a[1]))[0], force)
    else:
        r = check_source(vid_of(a[0]), arg("--title"), arg("--channel"), force)
    print(json.dumps(r, indent=1, ensure_ascii=False))
