#!/usr/bin/env python3
"""wrdgamingclipz guide-Short factory (GUIDE-RULES.md is binding). Generalises work/walk4_build.py.

  guide_make.py URL_OR_ID            fetch (if needed); then build if out/ID.guide.json exists, else stop at the script step
  guide_make.py URL fetch            download video-only <=720p + English captions -> work/guides/ID/, prints transcript path
  guide_make.py URL sheet S E [step] labelled frame sheet(s) of the source, one frame per `step` s (default 1) -> work/guides/ID/sheet_*.jpg
  guide_make.py URL build            TTS (Liam) + render + description + contact sheet from out/ID.guide.json
  guide_make.py URL upload [--publish-at ISO]   upload out/ID.mp4 PRIVATE via yt_upload_gaming.py (privacy is hard-coded private;
                                     --publish-at e.g. 2026-11-18T09:00:00-05:00 schedules it: privacyStatus stays private + status.publishAt)
A clip's optional 4th element is another source video id (default: the guide's own source); fetch it first (`guide_make.py OTHER_ID fetch`).
guide.json optional "credits": [["Channel", "VIDEO_ID"], ...] adds extra "Guide via" lines after the main credit (description only).
guide.json optional "evergreen": true -> patch stamp says 'Works as of <build month year>' instead of the source date.

SCRIPT STEP (separate, reviewable): the writer reads work/guides/ID/transcript.txt, ranks every tip, and writes out/ID.guide.json:
  {"title": "HOW TO ...", "yt_title": "...", "hook": "...", "tips": ["ranked tip + transcript time", ...],
   "parts": [{"key":"hook","text":"...","label":null,"clips":[[src_s, dur_weight, zoom, optional_source_video_id], ...]},
             {"key":"s1","text":"One. ...","label":"1  Short label","clips":[...]}, ..., {"key":"end","text":"...","label":null,"clips":[...]}],
   "desc_steps": ["1. full step text, including tips cut from the Short", ...],
   "tags": ["#Fortnite", ...], "crop_top": 0.12, "crop_bottom": 0, "crop_left": 0}  (crop to hide source watermark/captions/facecam)
Build writes out/ID.script.txt (script + tip ranking), out/ID.mp4, out/ID.contact.jpg, out/ID.desc.txt, out/ID.COSTS.json.
Build lints the script: hedge words (fail), word count, and capitalised names/numbers not found in the transcript (warn).
"""
import json, os, re, subprocess, sys, time, datetime

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
FF = "/home/williamdownard/openclaw-sites/bin/ffmpeg"
OUT = B + "/out"
VOICE = "TX3LPaxmHKxFdv7VOQHJ"  # ElevenLabs Liam, the only gaming voice
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ANTON = B + "/assets/fonts/Anton-Regular.ttf"  # open-license headline font (William picked this title style 2026-11-21)
HEDGES = ["reportedly", "apparently", "supposedly", "according to", "allegedly", "rumored", "rumoured", "it seems", "might be", "i think"]
TTS_USD_PER_CHAR = 0.22 / 1000


def title_png(W, lines):
    """Headline title (guide.json "title_lines": [line1, line2?]): Anton, line 1 yellow, line 2 white, thick black stroke."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = 95
    for i, text in enumerate(lines[:2]):
        size = 112 if i == 0 else 88
        f = ImageFont.truetype(ANTON, size)
        while d.textlength(text, font=f) > 1000 and size > 50:  # shrink long lines to fit
            size -= 4; f = ImageFont.truetype(ANTON, size)
        tw = d.textlength(text, font=f)
        d.text(((1080 - tw) / 2, y), text, font=f, fill="#FFE14D" if i == 0 else "white", stroke_width=10 if i == 0 else 9, stroke_fill="black")
        y += 130
    p_ = f"{W}/title_headline.png"; im.save(p_); return p_


def vid_id(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", s)
    return m.group(1) if m else s


def wdir(vid):
    d = f"{B}/work/guides/{vid}"
    os.makedirs(d, exist_ok=True)
    return d


def dur(p):
    r = subprocess.run([FF, "-hide_banner", "-i", p, "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"time=(\d+):(\d+):([\d.]+)", r)[-1]
    return int(m[0]) * 3600 + int(m[1]) * 60 + float(m[2])


def fetch(vid):
    import cut_moment as c
    d = wdir(vid)
    url = "https://www.youtube.com/watch?v=" + vid
    port = c.start_proxy()
    px = ["--proxy", f"http://127.0.0.1:{port}", "--ffmpeg-location", c.FFMPEG, "--no-warnings"]
    if not any(f.startswith("src.") for f in os.listdir(d)):
        r = subprocess.run([c.YTDLP, *px, "-f", "bv*[height<=720]", "-o", d + "/src.%(ext)s", url], capture_output=True, text=True)
        if r.returncode:
            sys.exit("DOWNLOAD FAIL " + r.stderr[-300:])
    if not os.path.exists(d + "/transcript.txt"):
        for _ in range(3):
            subprocess.run([c.YTDLP, *px, "--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", "en-orig,en", "--sub-format", "json3", "-o", d + "/tr", url], capture_output=True, text=True)
            fs = sorted(f for f in os.listdir(d) if f.startswith("tr.") and f.endswith(".json3"))
            if fs:
                break
            time.sleep(8)
        if not fs:
            sys.exit("NO TRANSCRIPT (captions unavailable or 429)")
        ev = json.load(open(f"{d}/{fs[0]}"))["events"]
        lines, cur_t, cur = [], None, []
        for e in ev:
            tx = "".join(s.get("utf8", "") for s in e.get("segs", [])).replace("\n", " ").strip()
            if not tx:
                continue
            t = e["tStartMs"] / 1000
            if cur_t is None:
                cur_t = t
            if t - cur_t > 6 and cur:
                lines.append(f"[{int(cur_t)//60}:{int(cur_t)%60:02d} = {cur_t:.0f}s] " + " ".join(cur)); cur_t, cur = t, []
            cur.append(tx)
        if cur:
            lines.append(f"[{int(cur_t)//60}:{int(cur_t)%60:02d} = {cur_t:.0f}s] " + " ".join(cur))
        open(d + "/transcript.txt", "w").write("\n".join(lines) + "\n")
    src = [f for f in os.listdir(d) if f.startswith("src.")][0]
    print("SRC", f"{d}/{src}", "\nTRANSCRIPT", d + "/transcript.txt", len(open(d + "/transcript.txt").read()), "chars")


def src_path(vid):
    d = wdir(vid)
    return d + "/" + [f for f in os.listdir(d) if f.startswith("src.")][0]


def sheet(vid, s, e, step=1.0):
    from PIL import Image, ImageDraw, ImageFont
    d = wdir(vid); sp = src_path(vid); ts = []
    t = s
    while t <= e:
        ts.append(t); t += step
    n = 0
    for k in range(0, len(ts), 20):
        chunk = ts[k:k + 20]; im = Image.new("RGB", (4 * 400, 5 * 225))
        for i, t in enumerate(chunk):
            fp = f"{d}/_f.jpg"
            subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", sp, "-frames:v", "1", "-vf", "scale=400:225", fp], check=True)
            x, y = (i % 4) * 400, (i // 4) * 225
            im.paste(Image.open(fp), (x, y)); ImageDraw.Draw(im).text((x + 4, y + 2), f"{t:.1f}s", fill="yellow", font=ImageFont.truetype(FONT, 22))
        o = f"{d}/sheet_{int(s)}_{n}.jpg"; im.save(o, quality=80); print(o); n += 1


def lint(g, vid):
    text = " ".join(p["text"] for p in g["parts"])
    low = text.lower()
    bad = [h for h in HEDGES if h in low]
    if bad:
        sys.exit("LINT FAIL hedge words: " + str(bad))
    words = len(text.split())
    print("words", words, "(no length target: as long as the guide needs; William 2026-11-21)")
    tr = open(wdir(vid) + "/transcript.txt").read().lower()
    ordw = {"One", "Two", "Three", "Four", "Five", "Here's", "Got", "Drop", "Equip", "Expect", "Don't", "Or", "You", "It"}
    miss = []
    for w in set(re.findall(r"\b[A-Z][a-zA-Z']{2,}\b", text)) - ordw:
        if w.lower() not in tr:
            miss.append(w)
    nums = [n for n in re.findall(r"\b\d+\b", text) if n not in tr]
    if miss or nums:
        print("LINT WARN not in transcript (verify, auto-captions mishear names):", sorted(miss), nums)


def tts(g, vid):
    W = wdir(vid); chars = 0
    for p in g["parts"]:
        f = f"{W}/{p['key']}.mp3"
        if os.path.exists(f):  # build() removes mp3s whose script text changed
            continue
        open(f"{W}/b.json", "w").write(json.dumps({"text": p["text"], "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.4, "similarity_boost": 0.75, "style": 0.35, "use_speaker_boost": True, "speed": 1.1}}))
        r = subprocess.run(["curl", "-s", "-m", "120", "-o", f, "-w", "%{http_code}", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", "-H", "xi-api-key: " + os.environ["ELEVENLABS_API_KEY"], "-H", "Content-Type: application/json", "-d", f"@{W}/b.json"], capture_output=True, text=True)
        if r.stdout.strip() != "200":
            print("TTS ERR", r.stdout, open(f, errors="ignore").read()[:200]); os.remove(f); sys.exit(1)
        chars += len(p["text"])
    return chars


def build(vid):
    from PIL import Image, ImageDraw, ImageFont
    g = json.load(open(f"{OUT}/{vid}.guide.json")); W = wdir(vid); SRC = src_path(vid); P = g["parts"]
    lint(g, vid)
    # transcripts for old TTS cache: remove stale mp3 if script text changed
    stamp = f"{W}/tts_texts.json"; old = json.load(open(stamp)) if os.path.exists(stamp) else {}
    for p in P:
        if old.get(p["key"]) != p["text"] and os.path.exists(f"{W}/{p['key']}.mp3"):
            os.remove(f"{W}/{p['key']}.mp3")
    t0 = time.time(); chars = tts(g, vid); json.dump({p["key"]: p["text"] for p in P}, open(stamp, "w")); tts_s = time.time() - t0
    ds = [dur(f"{W}/{p['key']}.mp3") for p in P]
    GAP = 0.25; starts = []; t = 0.15
    for d_ in ds:
        starts.append(t); t += d_ + GAP
    total = t + 0.3; N = len(P)
    print("durs", [round(x, 2) for x in ds], "total", round(total, 1))
    if total > 175:
        print("WARN length", round(total, 1), "s: Shorts cap is 3 min; trim or split Part 1/2")
    edges = [0] + [starts[i] - 0.05 for i in range(1, N)] + [total]
    segs = []
    for i, p in enumerate(P):
        a, b = edges[i], edges[i + 1]; cl = p["clips"]; ws = sum(c[1] for c in cl)
        for c_ in cl:  # optional 4th element: another source video id (fetched into work/guides/<id>/)
            segs.append((c_[0], (b - a) * c_[1] / ws, c_[2], src_path(c_[3]) if len(c_) > 3 else SRC))
    ct = g.get("crop_top", 0.12); cb = g.get("crop_bottom", 0.0); cl = g.get("crop_left", 0.0); cr = g.get("crop_right", 0.0); keep = 1 - ct - cb

    def png(name, text, size, y, color, box=False):
        im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d_ = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, size)
        lines = [text]
        if d_.textlength(text, font=f) > 980 and " " in text:
            w = text.split(" "); h = len(w) // 2; lines = [" ".join(w[:h]), " ".join(w[h:])]
        for j, l in enumerate(lines):
            tw = d_.textlength(l, font=f); x = (1080 - tw) / 2; yy = y + j * (size + 12)
            if box: d_.rounded_rectangle([x - 24, yy - 14, x + tw + 24, yy + size + 18], 18, fill=(0, 0, 0, 115))
            d_.text((x, yy), l, font=f, fill=color, stroke_width=5, stroke_fill="black")
        p_ = f"{W}/{name}.png"; im.save(p_); return p_
    ov = [(title_png(W, g["title_lines"]) if g.get("title_lines") else png("title", g["title"], 54, 130, "white"), None, None)]
    for i, p in enumerate(P):
        if p.get("label"):
            ov.append((png(p["key"], p["label"], 44, 330, "#FFE14D", True), starts[i], starts[i + 1] - 0.05 if i < N - 1 else total))
    cin = []
    for p in P: cin += ["-i", f"{W}/{p['key']}.mp3"]
    for s, d_, z, sp_ in segs: cin += ["-ss", str(s), "-t", f"{d_+0.2:.2f}", "-i", sp_]
    for o in ov: cin += ["-i", o[0]]
    nv = len(segs); fc = []
    for i in range(N): fc.append(f"[{i}:a]adelay={int(starts[i]*1000)}|{int(starts[i]*1000)}[a{i}]")
    for j, (s, d_, z, _sp) in enumerate(segs):
        fc.append(f"[{N+j}:v]fps=30,setpts=PTS-STARTPTS,crop=iw*(1-{cl}-{cr})/{z}:ih*{keep}/{z}:iw*{cl}+iw*(1-{cl}-{cr})*(1-1/{z})/2:ih*{ct}+ih*{keep}*(1-1/{z})*0.45,scale=1080:-2,setsar=1[v{j}]")
        fc.append(f"[{N+j}:v]fps=30,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[b{j}]")
        fc.append(f"[b{j}][v{j}]overlay=(W-w)/2:(H-h)/2[s{j}]")
        fc.append(f"[s{j}]trim=duration={d_:.3f},setpts=PTS-STARTPTS[t{j}]")
    fc.append("".join(f"[t{j}]" for j in range(nv)) + f"concat=n={nv}:v=1:a=0[bg]")
    lab = "bg"; base = N + nv
    for j, (p, a, b2) in enumerate(ov):
        en = f":enable='between(t,{a:.2f},{b2:.2f})'" if a is not None else ""
        nxt = "v" if j == len(ov) - 1 else f"o{j}"
        fc.append(f"[{lab}][{base+j}:v]overlay=0:0{en}[{nxt}]"); lab = nxt
    fc.append("".join(f"[a{i}]" for i in range(N)) + f"amix=inputs={N}:normalize=0,apad[aout]")
    t1 = time.time(); mp4 = f"{OUT}/{vid}.mp4"
    r = subprocess.run([FF, "-y", "-loglevel", "error"] + cin + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[aout]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", mp4], capture_output=True, text=True)
    if r.returncode: sys.exit("RENDER FAIL " + r.stderr[-600:])
    render_s = time.time() - t1; d_ = dur(mp4)
    # contact sheet: hook, each step mid + clip starts, close
    ts = [1.0, 3.0, 6.0]
    for i in range(1, N - 1): ts += [starts[i] + (starts[i + 1] - starts[i]) * 0.35, starts[i] + (starts[i + 1] - starts[i]) * 0.8]
    ts += [total - 3, d_ - 0.5]
    ts = ts[:20]; cols = 5; rows = (len(ts) + cols - 1) // cols
    sh = Image.new("RGB", (cols * 270, rows * 480))
    for i, t in enumerate(ts):
        fp = f"{W}/_c.jpg"
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=270:480", fp], check=True)
        x, y = (i % cols) * 270, (i // cols) * 480
        sh.paste(Image.open(fp), (x, y)); ImageDraw.Draw(sh).text((x + 4, y + 2), f"{t:.1f}s", fill="yellow", font=ImageFont.truetype(FONT, 22))
    sh.save(f"{OUT}/{vid}.contact.jpg", quality=88)
    # script + tip ranking
    open(f"{OUT}/{vid}.script.txt", "w").write(
        "RANKED TIPS (full transcript read; source %s)\n" % vid + "\n".join(f"{i+1}. {t}" for i, t in enumerate(g["tips"])) +
        f"\n\nFINAL SCRIPT ({sum(len(p['text'].split()) for p in P)} words, Liam, {d_:.1f} s)\n" + "\n".join(p["text"] for p in P) +
        "\n\nOverlays: title \"%s\"; " % g["title"] + ", ".join('"%s"' % p["label"] for p in P if p.get("label")) + "\n\nSHOT LIST (src time, weight, zoom)\n" +
        "\n".join(f"{p['key']}: {p['clips']}  # {p.get('proof','')}" for p in P) + "\n")
    # description: title line, hook, FULL steps, patch stamp, hashtags, credit LAST
    # evergreen guides (e.g. Elden Ring, patch-stable) stamp the build month, not the source's date
    stamp_d = datetime.datetime.now().strftime("%B %Y") if g.get("evergreen") else datetime.datetime.strptime(g["source_date"], "%Y%m%d").strftime("%B %-d, %Y")
    desc = (g["yt_title"] + "\n\n" + g["hook"] + "\n\n" + "\n".join(g["desc_steps"]) + f"\n\nWorks as of {stamp_d}; update if the game changes.\n\n" +
            " ".join(g["tags"]) + f"\n\nGuide via {g['creator']}: https://www.youtube.com/watch?v={g.get('source_id', vid)}\n" +
            "".join(f"Guide via {ch}: https://www.youtube.com/watch?v={cv}\n" for ch, cv in g.get("credits", [])))  # optional extra credit lines
    open(f"{OUT}/{vid}.desc.txt", "w").write(desc)
    cost = {"id": vid, "tts_chars_new": chars, "tts_usd_est": round(chars * TTS_USD_PER_CHAR, 3), "tts_secs": round(tts_s, 1), "render_secs": round(render_s, 1), "duration": round(d_, 1)}
    json.dump(cost, open(f"{OUT}/{vid}.COSTS.json", "w")); print("BUILT", mp4, cost)


def upload(vid, publish_at=None):
    g = json.load(open(f"{OUT}/{vid}.guide.json"))
    extra = ["--publish-at", publish_at] if publish_at else []
    tj = f"{OUT}/{vid}.thumb.jpg"  # custom cover (guide_thumb.py); shows on the channel page and in search, not the Shorts feed
    if not os.path.exists(tj) and g.get("thumb"):
        subprocess.run([sys.executable, B + "/guide_thumb.py", vid], check=False)
    if os.path.exists(tj):
        extra += ["--thumb", tj]
    r = subprocess.run([sys.executable, B + "/yt_upload_gaming.py", f"{OUT}/{vid}.mp4", "--title", g["yt_title"], "--desc-file", f"{OUT}/{vid}.desc.txt", "--privacy", "private", "--category", "20"] + extra, capture_output=True, text=True)
    open(f"{OUT}/{vid}.upload.txt", "w").write(r.stdout + r.stderr); print(r.stdout, r.stderr[-400:])


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    v = vid_id(a[0]); cmd = a[1] if len(a) > 1 else "auto"
    if cmd == "fetch": fetch(v)
    elif cmd == "sheet": sheet(v, float(a[2]), float(a[3]), float(a[4]) if len(a) > 4 else 1.0)
    elif cmd == "build": build(v)
    elif cmd == "upload":
        pa = a[a.index("--publish-at") + 1] if "--publish-at" in a else None
        upload(v, pa)
    else:
        fetch(v)
        if os.path.exists(f"{OUT}/{v}.guide.json"): build(v)
        else: print("SCRIPT STEP NEEDED: write", f"{OUT}/{v}.guide.json", "(see docstring)")
