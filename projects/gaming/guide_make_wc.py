#!/usr/bin/env python3
"""PROTOTYPE: guide_make.py + word-by-word centered captions (Stage 2 of the Eclipse dry run, 2026-11-21).
Does NOT modify guide_make.py; imports its helpers (dur, wdir, src_path, lint, FF, OUT, VOICE, FONT) and re-implements tts+build.

  guide_make_wc.py ID [--fill]     builds out/ID.wc.mp4 (or out/ID.wc_fill.mp4 with --fill) + contact sheet out/ID.wc.contact.jpg
                                   reads out/ID.guide.json (same schema). Writes no script/desc files (guide_make.py owns those).

How it differs from guide_make.py build():
  * TTS via ElevenLabs POST /v1/text-to-speech/{voice}/with-timestamps (same voice/model/settings) -> per-character alignment
    cached in work/guides/ID/<key>.wc.json (+ <key>.wc.mp3). Words are rebuilt from the characters.
  * Captions: one PIL PNG per word (white bold, thick black outline, UPPERCASE, centered at y~48%, punctuation stripped).
    All word PNGs go into ONE concat-demuxer input (a transparent PNG fills the gaps) -> a single overlay in the filter graph,
    so the graph stays the same size whatever the word count (140 words = 1 caption input, not 140 overlay filters).
  * The yellow step labels are dropped; the title stays at the top. Title overlay stays.
  * --fill: gameplay fills the 9:16 frame (centre crop of the 16:9 source, optional 4th clip item = focus x 0..1, default 0.5)
    instead of the blurred-letterbox look. A 720p source is upscaled ~2.7x, so it is soft.
"""
import json, os, re, subprocess, sys, time, base64
B = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, B)
import guide_make as gm
from PIL import Image, ImageDraw, ImageFont

FF, OUT, VOICE, FONT = gm.FF, gm.OUT, gm.VOICE, gm.FONT


def tts_ts(g, vid):
    """per part: mp3 + word list [(word, start, end)] from the with-timestamps endpoint; cached by script text."""
    W = gm.wdir(vid); chars = 0; res = {}
    for p in g["parts"]:
        k = p["key"]; mp3 = f"{W}/{k}.wc.mp3"; js = f"{W}/{k}.wc.json"
        if os.path.exists(js) and json.load(open(js)).get("text") == p["text"]:
            res[k] = json.load(open(js)); continue
        open(f"{W}/b.json", "w").write(json.dumps({"text": p["text"], "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.4, "similarity_boost": 0.75, "style": 0.35, "use_speaker_boost": True, "speed": 1.1}}))
        r = subprocess.run(["curl", "-s", "-m", "120", "-w", "\n%{http_code}", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
                            "-H", "xi-api-key: " + os.environ["ELEVENLABS_API_KEY"], "-H", "Content-Type: application/json", "-d", f"@{W}/b.json"], capture_output=True, text=True)
        body, code = r.stdout.rsplit("\n", 1)
        if code.strip() != "200":
            sys.exit("TTS ERR " + code + body[:200])
        j = json.loads(body); open(mp3, "wb").write(base64.b64decode(j["audio_base64"]))
        al = j["alignment"]; words = []; cur = ""; st = None; en = None
        for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
            if c.isspace():
                if cur: words.append((cur, st, en)); cur = ""; st = None
                continue
            if st is None: st = a
            cur += c; en = b
        if cur: words.append((cur, st, en))
        rec = {"text": p["text"], "words": words, "mp3": mp3}; json.dump(rec, open(js, "w")); res[k] = rec; chars += len(p["text"])
    return res, chars


def word_png(word, path, size=118):
    t = re.sub(r"[^\w'&$%-]", "", word).upper()
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, size)
    while d.textlength(t, font=f) > 960 and size > 50:
        size -= 6; f = ImageFont.truetype(FONT, size)
    x = (1080 - d.textlength(t, font=f)) / 2
    d.text((x, 880), t, font=f, fill="white", stroke_width=11, stroke_fill="black")
    im.save(path)


def build(vid, fill=False):
    g = json.load(open(f"{OUT}/{vid}.guide.json")); W = gm.wdir(vid); SRC = gm.src_path(vid); P = g["parts"]
    gm.lint(g, vid)
    t0 = time.time(); rec, chars = tts_ts(g, vid); tts_s = time.time() - t0
    ds = [gm.dur(rec[p["key"]]["mp3"]) for p in P]
    GAP = 0.25; starts = []; t = 0.15
    for d_ in ds: starts.append(t); t += d_ + GAP
    total = t + 0.3; N = len(P); print("durs", [round(x, 2) for x in ds], "total", round(total, 1))
    edges = [0] + [starts[i] - 0.05 for i in range(1, N)] + [total]
    segs = []
    for i, p in enumerate(P):
        a, b = edges[i], edges[i + 1]; ws = sum(c[1] for c in p["clips"])
        for c in p["clips"]: segs.append((c[0], (b - a) * c[1] / ws, c[2], c[3] if len(c) > 3 else 0.5))
    ct = g.get("crop_top", 0.0); cb = g.get("crop_bottom", 0.0); keep = 1 - ct - cb
    # title (top) png
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d_ = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, 54); tl = g["title"]
    lines = [tl]
    if d_.textlength(tl, font=f) > 980 and " " in tl:
        w = tl.split(" "); h = len(w) // 2; lines = [" ".join(w[:h]), " ".join(w[h:])]
    for j, l in enumerate(lines): d_.text(((1080 - d_.textlength(l, font=f)) / 2, 130 + j * 66), l, font=f, fill="white", stroke_width=5, stroke_fill="black")
    title_png = f"{W}/wc_title.png"; im.save(title_png)
    # word pngs + concat list (absolute timeline: transparent gaps)
    t1 = time.time(); blank = f"{W}/wc_blank.png"; Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)).save(blank)
    ev = []  # (png, start)
    n = 0
    for i, p in enumerate(P):
        ws = rec[p["key"]]["words"]
        for j, (w, a, b) in enumerate(ws):
            fp = f"{W}/wc_w{n:03d}.png"; word_png(w, fp); n += 1
            st = starts[i] + a; nxt = starts[i] + ws[j + 1][1] if j + 1 < len(ws) else starts[i] + b + 0.12
            ev.append((fp, st, min(nxt, starts[i] + b + 0.35) if j + 1 < len(ws) else nxt))
    lst = []; cur = 0.0
    for fp, a, b in ev:
        if a > cur + 0.01: lst.append((blank, a - cur))
        lst.append((fp, b - a)); cur = b
    if total > cur: lst.append((blank, total - cur))
    with open(f"{W}/wc_list.txt", "w") as fh:
        for fp, dd in lst: fh.write(f"file '{fp}'\nduration {dd:.3f}\n")
        fh.write(f"file '{lst[-1][0]}'\n")
    print("caption words", n, "png render", round(time.time() - t1, 1), "s")
    cin = []
    for p in P: cin += ["-i", rec[p["key"]]["mp3"]]
    for s, d2, z, fx in segs: cin += ["-ss", str(s), "-t", f"{d2+0.2:.2f}", "-i", SRC]
    cin += ["-i", title_png, "-f", "concat", "-safe", "0", "-i", f"{W}/wc_list.txt"]
    nv = len(segs); fc = []
    for i in range(N): fc.append(f"[{i}:a]adelay={int(starts[i]*1000)}|{int(starts[i]*1000)}[a{i}]")
    for j, (s, d2, z, fx) in enumerate(segs):
        if fill:  # centre-ish 9:16 crop of the 16:9 frame, focus x = fx
            fc.append(f"[{N+j}:v]fps=30,setpts=PTS-STARTPTS,crop=ih*9/16/{z}:ih/{z}:(iw-ih*9/16/{z})*{fx}:(ih-ih/{z})*0.5,scale=1080:1920:flags=lanczos,setsar=1,trim=duration={d2:.3f},setpts=PTS-STARTPTS[t{j}]")
        else:
            fc.append(f"[{N+j}:v]fps=30,setpts=PTS-STARTPTS,crop=iw/{z}:ih*{keep}/{z}:iw*(1-1/{z})/2:ih*{ct}+ih*{keep}*(1-1/{z})*0.45,scale=1080:-2,setsar=1[v{j}]")
            fc.append(f"[{N+j}:v]fps=30,setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[b{j}]")
            fc.append(f"[b{j}][v{j}]overlay=(W-w)/2:(H-h)/2[s{j}]")
            fc.append(f"[s{j}]trim=duration={d2:.3f},setpts=PTS-STARTPTS[t{j}]")
    fc.append("".join(f"[t{j}]" for j in range(nv)) + f"concat=n={nv}:v=1:a=0[bg]")
    fc.append(f"[bg][{N+nv}:v]overlay=0:0[o1]")
    fc.append(f"[{N+nv+1}:v]fps=30,format=rgba[cap]")
    fc.append("[o1][cap]overlay=0:0:format=auto:eof_action=pass[v]")
    fc.append("".join(f"[a{i}]" for i in range(N)) + f"amix=inputs={N}:normalize=0,apad[aout]")
    t2 = time.time(); mp4 = f"{OUT}/{vid}.wc{'_fill' if fill else ''}.mp4"
    r = subprocess.run([FF, "-y", "-loglevel", "error"] + cin + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[aout]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", mp4], capture_output=True, text=True)
    if r.returncode: sys.exit("RENDER FAIL " + r.stderr[-800:])
    render_s = time.time() - t2; dd = gm.dur(mp4)
    # contact sheet: 20 frames at word-aligned moments (first word of each part + mid-part) so captions are visible
    ts = [1.0]
    for i in range(N): ts += [starts[i] + 0.35, starts[i] + ds[i] * 0.6]
    ts = ts[:20]; cols = 5; rows = (len(ts) + cols - 1) // cols; sh = Image.new("RGB", (cols * 270, rows * 480))
    for i, t_ in enumerate(ts):
        fp = f"{W}/_c.jpg"; subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t_:.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=270:480", fp], check=True)
        x, y = (i % cols) * 270, (i // cols) * 480; sh.paste(Image.open(fp), (x, y)); ImageDraw.Draw(sh).text((x + 4, y + 2), f"{t_:.1f}s", fill="yellow", font=ImageFont.truetype(FONT, 22))
    sh.save(f"{OUT}/{vid}.wc{'_fill' if fill else ''}.contact.jpg", quality=88)
    cost = {"id": vid, "fill": fill, "tts_chars_new": chars, "tts_usd_est": round(chars * gm.TTS_USD_PER_CHAR, 3), "tts_secs": round(tts_s, 1), "caption_words": n, "render_secs": round(render_s, 1), "duration": round(dd, 1)}
    json.dump(cost, open(f"{OUT}/{vid}.wc{'_fill' if fill else ''}.COSTS.json", "w")); print("BUILT", mp4, cost)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    build(gm.vid_id(a[0]), "--fill" in a)
