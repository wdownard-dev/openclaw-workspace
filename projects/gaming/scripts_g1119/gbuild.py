#!/usr/bin/env python3
"""gbuild.py SPEC.json [--no-render] : GTA 6 guide Short builder (GUIDE-RULES.md + fluxx7x look).

Differences from guide_make.py: multiple source segments (work/g1119/seg/*.mp4), per-source facecam blur mask,
ElevenLabs with-timestamps (Liam) so captions are word-by-word in sync, white bold centred captions, 9:16 over blurred copy.

SPEC: {"slug","title","yt_title","hook","tips":[...],"desc_steps":[...],"hashtags":"#GTA6 ...","tags":[...],"credits":["Footage via ...: url"],
       "source_date":"November 19, 2026","segs":{"key":{"file":"tg_jet","base":4085,"mask":[x,y,w,h]}},
       "parts":[{"key","text","label"|null,"clips":[["segkey",abs_start,weight],...],"proof":"..."}]}
"""
import json, os, re, subprocess, sys, time, base64, hashlib
from PIL import Image, ImageDraw, ImageFont

B = "/home/williamdownard/.openclaw/workspace/projects/gaming"
FF = "/home/williamdownard/openclaw-sites/bin/ffmpeg"
OUT = B + "/out"; SEG = B + "/work/g1119/seg"
VOICE = "TX3LPaxmHKxFdv7VOQHJ"
FONT = "/usr/share/fonts/opentype/fira/FiraSans-ExtraBold.otf"
FONT2 = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
USD = 0.22 / 1000
HEDGES = ["reportedly", "apparently", "supposedly", "according to", "allegedly", "rumored", "rumoured", "it seems", "might be", "i think"]


def dur(p):
    r = subprocess.run([FF, "-hide_banner", "-i", p, "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"time=(\d+):(\d+):([\d.]+)", r)[-1]
    return int(m[0]) * 3600 + int(m[1]) * 60 + float(m[2])


def tts(slug, p):
    d = f"{B}/work/g1119/tts_{slug}"; os.makedirs(d, exist_ok=True)
    h = hashlib.md5(p["text"].encode()).hexdigest()[:10]
    mp3, js = f"{d}/{p['key']}_{h}.mp3", f"{d}/{p['key']}_{h}.json"
    if os.path.exists(mp3) and os.path.exists(js):
        return mp3, json.load(open(js)), 0
    body = {"text": p["text"], "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.4, "similarity_boost": 0.75, "style": 0.35, "use_speaker_boost": True, "speed": 1.1}}
    open(f"{d}/b.json", "w").write(json.dumps(body))
    r = subprocess.run(["curl", "-s", "-m", "120", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
                        "-H", "xi-api-key: " + os.environ["ELEVENLABS_API_KEY"], "-H", "Content-Type: application/json", "-d", f"@{d}/b.json"], capture_output=True, text=True)
    try:
        j = json.loads(r.stdout)
        open(mp3, "wb").write(base64.b64decode(j["audio_base64"]))
    except Exception:
        sys.exit("TTS ERR " + r.stdout[:300])
    al = j.get("alignment") or j.get("normalized_alignment")
    json.dump(al, open(js, "w"))
    return mp3, al, len(p["text"])


def words_from_alignment(text, al):
    ch, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    out = []; cur = ""; s0 = None; e0 = None
    for c, a, b in zip(ch, st, en):
        if c.isspace():
            if cur: out.append((cur, s0, e0)); cur = ""; s0 = None
        else:
            if s0 is None: s0 = a
            cur += c; e0 = b
    if cur: out.append((cur, s0, e0))
    return out


def cap_png(word, path, size=84):
    w = re.sub(r"^[^\w$]+|[^\w$%']+$", "", word) or word
    im = Image.new("RGBA", (1080, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, size)
    tw = d.textlength(w, font=f)
    if tw > 1000: f = ImageFont.truetype(FONT, int(size * 1000 / tw)); tw = d.textlength(w, font=f)
    d.text(((1080 - tw) / 2, 22), w, font=f, fill="white", stroke_width=7, stroke_fill="black")
    im.save(path)


def line_png(path, text, size, y, color, box=False, H=170):
    im = Image.new("RGBA", (1080, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, size)
    tw = d.textlength(text, font=f)
    if tw > 1000: f = ImageFont.truetype(FONT, int(size * 1000 / tw)); tw = d.textlength(text, font=f)
    x = (1080 - tw) / 2
    if box: d.rounded_rectangle([x - 26, y - 12, x + tw + 26, y + size + 22], 20, fill=(0, 0, 0, 120))
    d.text((x, y), text, font=f, fill=color, stroke_width=6, stroke_fill="black")
    im.save(path)


def main():
    spec = json.load(open(sys.argv[1])); slug = spec["slug"]; P = spec["parts"]; N = len(P)
    W = f"{B}/work/g1119/build_{slug}"; os.makedirs(W, exist_ok=True)
    text = " ".join(p["text"] for p in P); low = text.lower()
    bad = [h for h in HEDGES if h in low]
    if bad: sys.exit("LINT hedge words " + str(bad))
    print("words", len(text.split()))
    chars = 0; mp3s = []; als = []
    for p in P:
        m, al, c = tts(slug, p); mp3s.append(m); als.append(al); chars += c
    ds = [dur(m) for m in mp3s]
    GAP = 0.2; starts = []; t = 0.15
    for d in ds: starts.append(t); t += d + GAP
    total = t + 0.4
    print("part durs", [round(x, 1) for x in ds], "total", round(total, 1), "tts chars new", chars, "usd", round(chars * USD, 3))
    if os.environ.get("DRY"): return
    edges = [0] + [starts[i] - 0.05 for i in range(1, N)] + [total]
    segs = []  # (segkey, rel_start, dur)
    for i, p in enumerate(P):
        a, b = edges[i], edges[i + 1]; ws = sum(c[2] for c in p["clips"])
        for k, s, w in p["clips"]:
            d = (b - a) * w / ws; sg = spec["segs"][k]; rel = s - sg["base"]
            sd = dur(f"{SEG}/{sg['file']}.mp4")
            if rel < 0 or rel + d > sd + 0.05: print(f"!! clip {k} {s} needs {d:.1f}s but seg has {sd - rel:.1f}s from there")
            segs.append((k, rel, d))
    # overlays
    ov = [(f"{W}/title.png", None, None, 120)]
    line_png(f"{W}/title.png", spec["title"], 60, 8, "white", H=150)
    for i, p in enumerate(P):
        if p.get("label"):
            line_png(f"{W}/lab{i}.png", p["label"], 66, 8, "#FFE14D", box=True, H=150)
            ov.append((f"{W}/lab{i}.png", starts[i], starts[i + 1] - 0.05 if i < N - 1 else total, 440))
    ci = 0
    for i, p in enumerate(P):
        ws = words_from_alignment(p["text"], als[i])
        for seq, disp in spec.get("cap_merge", []):
            norm = lambda w: re.sub(r"[^\w]", "", w).lower()
            k = 0
            while k + len(seq) <= len(ws):
                if [norm(w[0]) for w in ws[k:k + len(seq)]] == seq:
                    ws[k:k + len(seq)] = [(disp, ws[k][1], ws[k + len(seq) - 1][2])]
                k += 1
        for j, (w, s0, e0) in enumerate(ws):
            a = starts[i] + s0
            b = starts[i] + (ws[j + 1][1] if j + 1 < len(ws) else e0 + 0.12)
            pth = f"{W}/cap{ci}.png"; cap_png(w, pth); ci += 1
            ov.append((pth, a, b, 1065))
    print("caption words", ci)
    cin = []
    for m in mp3s: cin += ["-i", m]
    for k, rel, d in segs: cin += ["-ss", f"{rel:.2f}", "-t", f"{d + 0.2:.2f}", "-i", f"{SEG}/{spec['segs'][k]['file']}.mp4"]
    for o in ov: cin += ["-i", o[0]]
    nv = len(segs); fc = []
    for i in range(N): fc.append(f"[{i}:a]adelay={int(starts[i]*1000)}|{int(starts[i]*1000)}[a{i}]")
    for j, (k, rel, d) in enumerate(segs):
        mk = spec["segs"][k].get("mask")
        fc.append(f"[{N+j}:v]fps=30,setpts=PTS-STARTPTS,split=2[r{j}][q{j}]")
        fc.append(f"[r{j}]scale=1080:-2,setsar=1[f{j}]")
        if mk:
            x, y, w, h = [int(v) for v in (mk[0] * 1080, mk[1] * 608, mk[2] * 1080, mk[3] * 608)]
            fc.append(f"[f{j}]split=2[fa{j}][fb{j}];[fb{j}]crop={w}:{h}:{x}:{y},boxblur=28:6[fm{j}];[fa{j}][fm{j}]overlay={x}:{y}[v{j}]")
        else:
            fc.append(f"[f{j}]null[v{j}]")
        fc.append(f"[q{j}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[b{j}]")
        fc.append(f"[b{j}][v{j}]overlay=(W-w)/2:(H-h)/2[s{j}]")
        fc.append(f"[s{j}]trim=duration={d:.3f},setpts=PTS-STARTPTS[t{j}]")
    fc.append("".join(f"[t{j}]" for j in range(nv)) + f"concat=n={nv}:v=1:a=0[bg]")
    lab = "bg"; base = N + nv
    for j, (pth, a, b, y) in enumerate(ov):
        en = f":enable='between(t,{a:.2f},{b:.2f})'" if a is not None else ""
        nxt = "v" if j == len(ov) - 1 else f"o{j}"
        fc.append(f"[{lab}][{base+j}:v]overlay=0:{y}{en}[{nxt}]"); lab = nxt
    fc.append("".join(f"[a{i}]" for i in range(N)) + f"amix=inputs={N}:normalize=0,apad[aout]")
    open(f"{W}/fc.txt", "w").write(";\n".join(fc))
    mp4 = f"{OUT}/guide_1119_{slug}.mp4"; t1 = time.time()
    r = subprocess.run([FF, "-y", "-loglevel", "error"] + cin + ["-filter_complex_script", f"{W}/fc.txt", "-map", "[v]", "-map", "[aout]", "-t", f"{total:.2f}",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", mp4], capture_output=True, text=True)
    if r.returncode: sys.exit("RENDER FAIL " + r.stderr[-800:])
    d_ = dur(mp4); print("RENDERED", mp4, round(d_, 1), "s in", round(time.time() - t1), "s")
    # sheets: full (every ~3.5 s) + first 7 s strip
    def sheet(times, outp, cols):
        rows = (len(times) + cols - 1) // cols; sh = Image.new("RGB", (cols * 270, rows * 480))
        for i, t in enumerate(times):
            fp = f"{W}/_c.jpg"
            subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=270:480", fp], check=True)
            sh.paste(Image.open(fp), ((i % cols) * 270, (i // cols) * 480)); ImageDraw.Draw(sh).text(((i % cols) * 270 + 4, (i // cols) * 480 + 2), f"{t:.1f}s", fill="yellow", font=ImageFont.truetype(FONT2, 22))
        sh.save(outp, quality=86)
    n = int(d_ // 3.2); sheet([0.4 + k * (d_ - 0.8) / (n - 1) for k in range(n)][:30], f"{OUT}/guide_1119_{slug}.contact.jpg", 6)
    sheet([0.3 + k for k in range(8)], f"{OUT}/guide_1119_{slug}.first7.jpg", 8)
    # script + desc
    open(f"{OUT}/guide_1119_{slug}.script.txt", "w").write(
        "RANKED TIPS\n" + "\n".join(f"{i+1}. {t}" for i, t in enumerate(spec["tips"])) + f"\n\nFINAL SCRIPT ({len(text.split())} words, Liam, {d_:.1f} s)\n" + "\n".join(p["text"] for p in P) +
        f"\n\nOverlays: title \"{spec['title']}\"; " + ", ".join('"%s"' % p["label"] for p in P if p.get("label")) + "; word-by-word white captions\n\nSHOT LIST\n" +
        "\n".join(f"{p['key']}: {p['clips']}  # {p.get('proof','')}" for p in P) + "\n\nVERIFICATION\n" + spec["verify"] + "\n")
    desc = (spec["yt_title"] + "\n\n" + spec["hook"] + "\n\n" + "\n".join(spec["desc_steps"]) + f"\n\nWorks as of {spec['source_date']}; update if the game changes.\n\n" + spec["hashtags"] + "\n\n" + "\n".join(spec["credits"]) + "\n")
    open(f"{OUT}/guide_1119_{slug}.desc.txt", "w").write(desc)
    json.dump({"slug": slug, "title": spec["yt_title"], "tags": spec["tags"], "tts_chars_new": chars, "tts_usd_est": round(chars * USD, 3), "duration": round(d_, 1)}, open(f"{OUT}/guide_1119_{slug}.COSTS.json", "w"))
    print("DONE", slug)


if __name__ == "__main__":
    main()
