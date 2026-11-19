#!/usr/bin/env python3
"""wrdgamingclipz long-form walkthrough pipeline (16:9, 1280x720, 2-6 min, Videos page). Generalises work/lf/tools/build.py (Pirate Shop Token).
Rules: GUIDE-RULES.md + out/GTA6_LAUNCH_PLAYBOOK.md. Nothing here uploads or changes anything public.

  longform_make.py SLUG fetch            video-only <=1080p LANDSCAPE per source + English transcript -> work/longform/SLUG/<key>/ (skips sources with "file")
  longform_make.py SLUG sheet KEY S E [step]  labelled frame sheet of one source (verify on-screen proof before choosing clips)
  longform_make.py SLUG check            lint out/SLUG.longform.json only (no TTS, no render)
  longform_make.py SLUG build [--no-tts] TTS (cached) + render + chapters + description + contact sheet
  longform_make.py SLUG thumb            1280x720 layout-B thumbnail
  longform_make.py SLUG shorts           propose 3-4 Short cut points from the finished long-form -> out/SLUG.shorts.json
  longform_make.py SLUG all [--no-tts]   check, build, thumb, shorts
  longform_make.py SLUG upload           PRIVATE upload via yt_upload_gaming.py (hard-coded private; William triggers it)
Outputs: out/SLUG.longform.mp4, .desc.txt, .chapters.txt, .thumb.jpg, .contact.jpg, .COSTS.json, .shorts.json, .script.txt

SCRIPT STEP (separate, reviewable, written by us after reading ALL transcripts) = out/SLUG.longform.json:
 {"slug","game","accent":[r,g,b],"overlay_title":"HOW TO ...","yt_title":"...","hook":"description hook sentence",
  "min_sources":2, "strict":false, "evergreen":true, "source_date":"20261119" (only if not evergreen),
  "sources":{"J":{"id":"ytid","creator":"Janga","url":"...","file":"optional local mp4 override",
                  "crop":{"mode":"fill","anchor_y":1.0}  | {"mode":"bars","box":[x,y,w,h],"out_h":616,"y":52}}},
  "steps":[{"key":"hook|s1..|end","text":"spoken text (ours, never transcript text)","label":"on-screen step text or null",
            "chapter":"chapter title","desc":"full description line (or null)",
            "clips":[{"src":"J","start":15.2,"weight":1,"zoom":1.12,"max":3.2}],
            "facts":[{"claim":"...","proof":[{"src":"J","t":222},{"src":"R","t":312}]}],
            "cache_seed":"optional legacy mp3 path to adopt into the TTS cache"}],
  "desc_extra":["bonus line"], "tags":["#GTA6"], "thumb":{"lines":["PIRATE","TOKEN"],"sub":"FULL GUIDE","at":8.0,"focus":0.5,"zoom":1.0},
  "shorts_hint":{"ranked_tips":[...]}}
Segment durations: each step's clips share the step's time by weight; a clip's "max" caps its length (rest redistributed).
"""
import json, os, re, sys, time, hashlib, base64, shutil, subprocess, datetime

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
FF = "/home/williamdownard/openclaw-sites/bin/ffmpeg"
OUT = B + "/out"
VOICE = "TX3LPaxmHKxFdv7VOQHJ"  # Liam
VSET = {"stability": 0.4, "similarity_boost": 0.75, "style": 0.35, "use_speaker_boost": True, "speed": 1.1}
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TFONT = "/usr/share/fonts/opentype/fira/FiraSans-ExtraBold.otf"
HEDGES = ["reportedly", "apparently", "supposedly", "according to", "allegedly", "rumored", "rumoured", "it seems", "might be", "i think"]
TTS_USD_PER_CHAR = 0.22 / 1000
GAP = 0.25
GTA6_ACCENT = (255, 92, 140)  # pink; orange used as the gradient partner for GTA 6
GTA6_ORANGE = (255, 140, 50)


# ---------- helpers ----------
def info(p):
    r = subprocess.run([FF, "-hide_banner", "-i", p, "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"time=(\d+):(\d+):([\d.]+)", r)[-1]
    d = int(m[0]) * 3600 + int(m[1]) * 60 + float(m[2])
    wh = re.search(r"Video:.*?, (\d{2,5})x(\d{2,5})", r)
    return d, (int(wh.group(1)), int(wh.group(2))) if wh else None


def dur(p):
    return info(p)[0]


def load(slug):
    p = f"{OUT}/{slug}.longform.json"
    if not os.path.exists(p):
        sys.exit("SCRIPT STEP NEEDED: write " + p + " (see docstring)")
    return json.load(open(p))


def wdir(slug, key=None):
    d = f"{B}/work/longform/{slug}" + (f"/{key}" if key else "")
    os.makedirs(d, exist_ok=True)
    return d


def src_file(L, key):
    s = L["sources"][key]
    if s.get("file"):
        f = s["file"] if os.path.isabs(s["file"]) else B + "/" + s["file"]
        if os.path.exists(f):
            return f
        sys.exit(f"SOURCE FILE MISSING {f}")
    d = wdir(L["slug"], key)
    fs = [f for f in os.listdir(d) if f.startswith("src.")]
    if not fs:
        sys.exit(f"SOURCE {key} not fetched: run fetch")
    return d + "/" + fs[0]


def transcript(L, key):
    s = L["sources"][key]
    cands = [s.get("transcript"), f"{B}/work/guides/{s['id']}/transcript.txt", f"{wdir(L['slug'], key)}/transcript.txt"]
    for c in cands:
        if c and os.path.exists(c):
            return open(c).read()
    return ""


# ---------- fetch ----------
def fetch(L):
    import cut_moment as c
    port = c.start_proxy()
    px = ["--proxy", f"http://127.0.0.1:{port}", "--ffmpeg-location", c.FFMPEG, "--no-warnings"]
    for key, s in L["sources"].items():
        d = wdir(L["slug"], key)
        url = s.get("url") or "https://www.youtube.com/watch?v=" + s["id"]
        have_src = s.get("file") and os.path.exists(B + "/" + s["file"] if not os.path.isabs(s["file"]) else s["file"])
        if not have_src and not any(f.startswith("src.") for f in os.listdir(d)):
            # video-only, up to 1080p, landscape only (portrait/Shorts sources are rejected)
            r = subprocess.run([c.YTDLP, *px, "-f", "bv*[height<=1080][width>height]", "-o", d + "/src.%(ext)s", url], capture_output=True, text=True)
            if r.returncode:
                sys.exit(f"DOWNLOAD FAIL {key} " + r.stderr[-300:])
            f = [f for f in os.listdir(d) if f.startswith("src.")][0]
            _, wh = info(f"{d}/{f}")
            if wh and wh[0] <= wh[1]:
                sys.exit(f"SOURCE {key} is not landscape {wh}")
        tp = d + "/transcript.txt"
        if not os.path.exists(tp) and not transcript(L, key):
            fs = []
            for _ in range(3):
                subprocess.run([c.YTDLP, *px, "--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", "en-orig,en", "--sub-format", "json3", "-o", d + "/tr", url], capture_output=True, text=True)
                fs = sorted(f for f in os.listdir(d) if f.startswith("tr.") and f.endswith(".json3"))
                if fs:
                    break
                time.sleep(8)
            if not fs:
                sys.exit(f"NO TRANSCRIPT for {key} (captions unavailable or 429)")
            lines, cur_t, cur = [], None, []
            for e in json.load(open(f"{d}/{fs[0]}"))["events"]:
                tx = "".join(g.get("utf8", "") for g in e.get("segs", [])).replace("\n", " ").strip()
                if not tx:
                    continue
                t = e["tStartMs"] / 1000
                cur_t = t if cur_t is None else cur_t
                if t - cur_t > 6 and cur:
                    lines.append(f"[{int(cur_t)//60}:{int(cur_t)%60:02d} = {cur_t:.0f}s] " + " ".join(cur)); cur_t, cur = t, []
                cur.append(tx)
            if cur:
                lines.append(f"[{int(cur_t)//60}:{int(cur_t)%60:02d} = {cur_t:.0f}s] " + " ".join(cur))
            open(tp, "w").write("\n".join(lines) + "\n")
        sf = src_file(L, key)
        print("SRC", key, sf, info(sf)[1], "| TRANSCRIPT", (tp if os.path.exists(tp) else "existing") , len(transcript(L, key)), "chars")


def sheet(L, key, s, e, step=1.0):
    from PIL import Image, ImageDraw, ImageFont
    sp = src_file(L, key); d = wdir(L["slug"], key); ts = []; t = s
    while t <= e:
        ts.append(t); t += step
    for k in range(0, len(ts), 20):
        im = Image.new("RGB", (4 * 400, 5 * 225))
        for i, t in enumerate(ts[k:k + 20]):
            fp = f"{d}/_f.jpg"
            subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", sp, "-frames:v", "1", "-vf", "scale=400:225", fp], check=True)
            x, y = (i % 4) * 400, (i // 4) * 225
            im.paste(Image.open(fp), (x, y)); ImageDraw.Draw(im).text((x + 4, y + 2), f"{t:.1f}s", fill="yellow", font=ImageFont.truetype(FONT, 22))
        o = f"{d}/sheet_{int(s)}_{k//20}.jpg"; im.save(o, quality=80); print(o)


# ---------- lint ----------
def shingles(txt, n=8):
    w = re.findall(r"[a-z0-9']+", txt.lower())
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def check(L, quiet=False):
    errs, warns = [], []
    S = L["steps"]
    text = " ".join(p["text"] for p in S); low = text.lower()
    bad = [h for h in HEDGES if h in low]
    if bad: errs.append("hedge words: " + str(bad))
    used = {c["src"] for p in S for c in p["clips"]}
    undefined = used - set(L["sources"])
    if undefined: errs.append("clips reference undefined sources " + str(undefined))
    mins = L.get("min_sources", 2)
    if len(used) < mins: errs.append(f"only {len(used)} source(s) used in clips; min_sources={mins}")
    if len(L["sources"]) < mins: errs.append(f"only {len(L['sources'])} source(s) declared; min_sources={mins}")
    trs = {k: transcript(L, k) for k in L["sources"]}
    for k, t in trs.items():
        if not t: warns.append(f"no transcript on disk for source {k}: cannot lint names/numbers or copying")
    ours = shingles(text)
    for k, t in trs.items():
        shared = ours & shingles(re.sub(r"\[[^\]]*\]", " ", t))
        if shared: errs.append(f"script copies >=8-word runs from source {k}: {sorted(shared)[:3]} (must be our own words)")
    words = len(text.split())
    if not 250 <= words <= 1000: warns.append(f"{words} words (long-form target ~300-900 for 2-6 min)")
    alltr = " ".join(trs.values()).lower()
    ordw = {"Step", "Here's", "Route", "Got", "Drop", "Equip", "Expect", "Don't", "Or", "You", "It", "Mistakes", "Then", "And", "Add", "Land", "Open", "Pick", "Load", "Carry", "Get", "Every", "Finish", "Bring", "Shoot", "Solo", "Spread", "Drive", "Two", "One", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Next", "Use", "Take", "Check", "Grab", "Head", "Make", "If", "Do", "That", "This", "The", "In", "On"}
    if alltr:
        miss = sorted(w for w in set(re.findall(r"\b[A-Z][a-zA-Z']{2,}\b", text)) - ordw if w.lower() not in alltr)
        nums = sorted(n for n in set(re.findall(r"\b\d+\b", text)) if n not in alltr)
        if miss or nums: warns.append(f"not in any transcript (verify; captions mishear names): {miss} {nums}")
    # facts: two distinct sources each (strict for GTA 6)
    nf = 0
    for p in S:
        for f in p.get("facts", []):
            nf += 1
            if len({x["src"] for x in f["proof"]}) < 2: (errs if L.get("strict") else warns).append(f"fact single-source in step {p['key']}: {f['claim']}")
    if L.get("strict") and nf == 0: errs.append("strict mode: steps need 'facts' entries (claim + 2 proof sources)")
    for p in S:
        if not p["clips"]: errs.append(f"step {p['key']} has no clips")
        for c in p["clips"]:
            if not c.get("start", 0) >= 0: errs.append(f"bad clip start in {p['key']}")
    if not L.get("evergreen") and not L.get("source_date"): errs.append("need evergreen:true or source_date (YYYYMMDD) for the patch stamp")
    for sk, s in L["sources"].items():
        if s.get("rockstar_footage"): warns.append(f"source {sk} marked rockstar_footage: confirm claim/takedown risk (playbook rule)")
    if not quiet:
        print("words", words, "| sources used", sorted(used))
        for w in warns: print("LINT WARN", w)
    if errs:
        for e in errs: print("LINT FAIL", e)
        sys.exit(1)
    return warns


# ---------- TTS (cached) ----------
def tts(L, allow_net=True):
    cache = f"{B}/work/longform/audio_cache"; os.makedirs(cache, exist_ok=True); chars = 0; files = []
    for p in L["steps"]:
        h = hashlib.sha1((p["text"] + json.dumps(VSET, sort_keys=True) + VOICE).encode()).hexdigest()[:16]
        mp = f"{cache}/{h}.mp3"; al = f"{cache}/{h}.align.json"
        if not os.path.exists(mp) and p.get("cache_seed"):
            seed = p["cache_seed"] if os.path.isabs(p["cache_seed"]) else B + "/" + p["cache_seed"]
            if os.path.exists(seed):
                shutil.copy(seed, mp)
                sa = seed.replace(".mp3", ".align.json")
                if os.path.exists(sa): shutil.copy(sa, al)
                print("SEEDED cache from", seed)
        if not os.path.exists(mp):
            if not allow_net: sys.exit(f"CACHE MISS for step {p['key']} and --no-tts set (no spend)")
            key = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("ELEVENLABS_API_KEY missing")
            wd = wdir(L["slug"]); body = {"text": p["text"], "model_id": "eleven_multilingual_v2", "voice_settings": VSET}
            open(wd + "/b.json", "w").write(json.dumps(body))
            r = subprocess.run(["curl", "-s", "-m", "180", "-o", wd + "/resp.json", "-w", "%{http_code}", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128", "-H", "xi-api-key: " + key, "-H", "Content-Type: application/json", "-d", "@" + wd + "/b.json"], capture_output=True, text=True)
            if r.stdout.strip() != "200": sys.exit("TTS ERR " + r.stdout + open(wd + "/resp.json").read()[:300])
            j = json.load(open(wd + "/resp.json")); open(mp, "wb").write(base64.b64decode(j["audio_base64"])); json.dump(j["alignment"], open(al, "w"))
            chars += len(p["text"])
        files.append(mp)
    return files, chars


# ---------- timeline ----------
def timeline(L, files):
    ds = [dur(f) for f in files]; starts = []; t = 0.15
    for d in ds: starts.append(t); t += d + GAP
    total = t + 0.5; n = len(ds)
    edges = [0] + [starts[i] - 0.05 for i in range(1, n)] + [total]
    segs = []  # (step_index, src, start, dur, zoom)
    for i, p in enumerate(L["steps"]):
        need = edges[i + 1] - edges[i]; cl = p["clips"]; alloc = [None] * len(cl); free = list(range(len(cl)))
        while free:
            ws = sum(cl[k].get("weight", 1) for k in free); rem = need - sum(x for x in alloc if x)
            capped = [k for k in free if cl[k].get("max") and cl[k]["max"] < rem * cl[k].get("weight", 1) / ws]
            if not capped:
                for k in free: alloc[k] = rem * cl[k].get("weight", 1) / ws
                break
            for k in capped: alloc[k] = cl[k]["max"]; free.remove(k)
        if abs(sum(x or 0 for x in alloc) - need) > 0.05: print("WARN step", p["key"], "need", round(need, 1), "got", round(sum(x or 0 for x in alloc), 1), "(raise max or add clips)")
        for k, c in enumerate(cl): segs.append((i, c["src"], c["start"], alloc[k] or 0.5, c.get("zoom", 1.0)))
    return ds, starts, edges, total, segs


def chapters_from(L, edges, total):
    """Chapters from the render timeline (step edges). YouTube needs >=3 chapters, first at 0:00, each >=10 s: shorter ones merge into the next."""
    ch = []
    for i, p in enumerate(L["steps"]):
        if p.get("chapter"): ch.append([0 if i == 0 else edges[i], p["chapter"]])
    ch[0][0] = 0
    out = []; i = 0
    while i < len(ch):
        t, lab = ch[i]; nxt = ch[i + 1][0] if i + 1 < len(ch) else total
        while nxt - t < 10 and i + 1 < len(ch):  # merge short chapter with the next
            i += 1; lab = lab + " and " + ch[i][1].split(": ", 1)[-1] if False else lab + " / " + ch[i][1]
            nxt = ch[i + 1][0] if i + 1 < len(ch) else total
        out.append((t, lab)); i += 1
    return [(int(t), lab) for t, lab in out]


def mmss(t): return f"{t//60}:{t%60:02d}"


# ---------- build ----------
def build(L, allow_net=True):
    from PIL import Image, ImageDraw, ImageFont
    slug = L["slug"]; S = L["steps"]; n = len(S); W = wdir(slug)
    warns = check(L)
    t0 = time.time(); files, chars = tts(L, allow_net); tts_s = time.time() - t0
    ds, starts, edges, total, segs = timeline(L, files)
    print("durs", [round(x, 1) for x in ds], "total", round(total, 1), "words", sum(len(p["text"].split()) for p in S))
    if not 120 <= total <= 360: print("WARN length", round(total, 1), "s (target 2-6 min)")
    srcs = {k: src_file(L, k) for k in L["sources"]}; native = {k: info(v)[1] for k, v in srcs.items()}

    def png(name, text, size, y, color, box=False):
        im = Image.new("RGBA", (1280, 720), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = ImageFont.truetype(FONT, size)
        tw = d.textlength(text, font=f); x = (1280 - tw) / 2
        if box: d.rounded_rectangle([x - 22, y - 12, x + tw + 22, y + size + 16], 16, fill=(0, 0, 0, 120))
        d.text((x, y), text, font=f, fill=color, stroke_width=4, stroke_fill="black")
        q = f"{W}/o_{name}.png"; im.save(q); return q
    ov = [(png("title", L["overlay_title"], 40, 22, "white"), None, None)]
    for i, p in enumerate(S):
        if p.get("label"): ov.append((png(p["key"], p["label"], 38, 86, "#FFE14D", True), starts[i], (starts[i + 1] - 0.05) if i < n - 1 else total))
    cin = []
    for f in files: cin += ["-i", f]
    for _, s, st, d, z in segs: cin += ["-ss", f"{st:.2f}", "-t", f"{d+0.3:.2f}", "-i", srcs[s]]
    for o in ov: cin += ["-i", o[0]]
    nv = len(segs); fc = []
    for i in range(n): fc.append(f"[{i}:a]adelay={int(starts[i]*1000)}|{int(starts[i]*1000)}[a{i}]")
    for j, (_, s, st, d, z) in enumerate(segs):
        k = n + j; cr = L["sources"][s].get("crop", {"mode": "fill", "anchor_y": 0.5})
        pre = "" if native[s] == (1280, 720) else "scale=1280:720,setsar=1,"  # 1080p etc. -> coordinate space of the crops
        head = f"[{k}:v]fps=30,setpts=PTS-STARTPTS,{pre}"
        if cr["mode"] == "fill":
            ay = cr.get("anchor_y", 0.5); ax = cr.get("anchor_x", 0.5)
            ycoord = f"{ay}*(720-720/{z})" if ay not in (0, 1) else ("0" if ay == 0 else f"720-720/{z}")
            xcoord = f"(1280-1280/{z})/2" if ax == 0.5 else f"{ax}*(1280-1280/{z})"
            fc.append(f"{head}crop=1280/{z}:720/{z}:{xcoord}:{ycoord},scale=1280:720,setsar=1,trim=duration={d:.3f},setpts=PTS-STARTPTS[t{j}]")
        else:
            x, y, w, h = cr["box"]; oh = cr.get("out_h", int(720 * 0.855)); oy = cr.get("y", (720 - oh) // 2)
            fc.append(f"{head}split[x1][x2];[x1]scale=1280:720,boxblur=30:5[bb{j}];[x2]crop={w}:{h}:{x}:{y},scale=1280:{oh},setsar=1[ff{j}];[bb{j}][ff{j}]overlay=0:{oy},trim=duration={d:.3f},setpts=PTS-STARTPTS[t{j}]")
    fc.append("".join(f"[t{j}]" for j in range(nv)) + f"concat=n={nv}:v=1:a=0[bg]")
    lab = "bg"; base = n + nv
    for j, (p, a, b2) in enumerate(ov):
        en = f":enable='between(t,{a:.2f},{b2:.2f})'" if a is not None else ""
        nxt = "v" if j == len(ov) - 1 else f"o{j}"
        fc.append(f"[{lab}][{base+j}:v]overlay=0:0{en}[{nxt}]"); lab = nxt
    fc.append("".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,apad[aout]")
    mp4 = f"{OUT}/{slug}.longform.mp4"; t1 = time.time()
    r = subprocess.run([FF, "-y", "-loglevel", "error"] + cin + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[aout]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", mp4], capture_output=True, text=True)
    if r.returncode: sys.exit("RENDER FAIL " + r.stderr[-800:])
    render_s = time.time() - t1; fd, wh = info(mp4)
    assert wh == (1280, 720), f"render is {wh}"
    if abs(fd - total) > 0.15: print("WARN render duration", fd, "!= timeline", round(total, 2))
    json.dump({"starts": starts, "edges": edges, "total": total, "render_dur": fd, "segs": segs}, open(f"{W}/timeline.json", "w"))
    # chapters computed from the final render's timeline (edges verified against the rendered duration above)
    chs = chapters_from(L, edges, fd)
    open(f"{OUT}/{slug}.chapters.txt", "w").write("\n".join(f"{mmss(t)} {lab}" for t, lab in chs) + "\n")
    # description: title line, hook, full steps, chapters, patch stamp, hashtags, credits LAST
    stamp_d = datetime.datetime.now().strftime("%B %Y") if L.get("evergreen", True) else datetime.datetime.strptime(L["source_date"], "%Y%m%d").strftime("%B %Y")
    steps_txt = [p["desc"] for p in S if p.get("desc")]
    desc = (L["yt_title"].upper() + "\n\n" + L["hook"] + "\n\nFULL STEPS\n" + "\n".join(steps_txt) +
            ("\n" + "\n".join(L["desc_extra"]) if L.get("desc_extra") else "") +
            "\n\nCHAPTERS\n" + "\n".join(f"{mmss(t)} {lab}" for t, lab in chs) +
            f"\n\nWorks as of {stamp_d}; update if the game changes.\n\n" + " ".join(L["tags"]) + "\n\n" +
            "\n".join(f"Guides via {s['creator']}: {s.get('url') or 'https://www.youtube.com/watch?v=' + s['id']}" for s in L["sources"].values()) + "\n")
    open(f"{OUT}/{slug}.desc.txt", "w").write(desc)
    # contact sheet: one frame per clip midpoint
    cuts = []; t = 0
    for i, s, st, d, z in segs: cuts.append((t, t + d, s, st)); t += d
    cols = 5; w, h = 384, 216; rows = (len(cuts) + cols - 1) // cols; sh = Image.new("RGB", (cols * w, rows * h)); ft = ImageFont.truetype(FONT, 18)
    for i, (a, b, s, st) in enumerate(cuts):
        tt = (a + b) / 2; fp = f"{W}/_cf.jpg"
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{tt:.2f}", "-i", mp4, "-frames:v", "1", "-vf", f"scale={w}:{h}", fp])
        try: im = Image.open(fp)
        except Exception: continue
        x, y = (i % cols) * w, (i // cols) * h; sh.paste(im, (x, y)); ImageDraw.Draw(sh).text((x + 3, y + h - 22), f"{tt:.0f}s {s}{st:.0f}", fill="yellow", font=ft, stroke_width=2, stroke_fill="black")
    sh.save(f"{OUT}/{slug}.contact.jpg", quality=85)
    open(f"{OUT}/{slug}.script.txt", "w").write(
        f"LONG-FORM SCRIPT {slug} ({sum(len(p['text'].split()) for p in S)} words, Liam, {fd:.1f} s)\n" + "\n".join(p["text"] for p in S) +
        "\n\nSOURCES\n" + "\n".join(f"{k}: {s['creator']} {s.get('id','')}" for k, s in L["sources"].items()) + "\n\nSHOT LIST (src,start,dur,zoom)\n" +
        "\n".join(f"{S[i]['key']}: {s}@{st:.1f} {d:.1f}s z{z}" for i, s, st, d, z in segs) + "\n")
    cost = {"slug": slug, "tts_chars_new": chars, "tts_usd_est": round(chars * TTS_USD_PER_CHAR, 3), "tts_secs": round(tts_s, 1), "render_secs": round(render_s, 1), "duration": round(fd, 2), "words": sum(len(p['text'].split()) for p in S)}
    json.dump(cost, open(f"{OUT}/{slug}.COSTS.json", "w")); print("BUILT", mp4, cost)
    return starts, edges, fd


# ---------- thumbnail (layout B, landscape) ----------
def thumb(L):
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageStat
    slug = L["slug"]; mp4 = f"{OUT}/{slug}.longform.mp4"; T = L["thumb"]
    acc = tuple(L.get("accent") or (GTA6_ACCENT if "GTA" in L.get("game", "").upper() else (255, 214, 0)))
    acc2 = GTA6_ORANGE if "GTA" in L.get("game", "").upper() else tuple(int(c * 0.6) for c in acc)
    fp = f"{wdir(slug)}/th_frame.png"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{T.get('at', 8.0)}", "-i", mp4, "-frames:v", "1", fp], check=True)
    fr = Image.open(fp).convert("RGB").crop((0, 140, 1280, 720))  # drop the title/step overlay band (y<140)
    W_, H_ = 1280, 720; bg = Image.new("RGB", (W_, H_)); d = ImageDraw.Draw(bg)
    for x in range(W_):  # horizontal accent gradient, dark (layout B uses a dark accent wash)
        k = x / W_; c = tuple(int((acc[i] * (1 - k) + acc2[i] * k) * (0.22 + 0.2 * k)) for i in range(3)); d.line([(x, 0), (x, H_)], fill=c)
    F = lambda s: ImageFont.truetype(TFONT, s)
    game = L.get("game", "").upper(); lines = T["lines"]; pad = 44; colw = 540
    tw = d.textlength(game, font=F(40)); d.rounded_rectangle([pad, 40, pad + tw + 56, 108], 14, fill=acc); d.text((pad + 28, 74), game, font=F(40), fill=(15, 15, 15), anchor="lm")
    size = 190
    while max(d.textlength(l, font=F(size)) for l in lines) > colw - 10: size -= 6
    y = 150 + size * 0.5
    for l in lines:
        d.text((pad, y), l, font=F(size), fill=(255, 255, 255), anchor="lm", stroke_width=10, stroke_fill=(0, 0, 0)); y += size * 0.95
    d.text((pad, y + 14), T.get("sub", "FULL GUIDE"), font=F(62), fill=acc, anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
    side = 600; zoom = T.get("zoom", 1.0); s2 = int(min(fr.height, fr.width) / zoom); x0 = int((fr.width - s2) * T.get("focus", 0.5)); y0 = (fr.height - s2) // 2
    pic = fr.crop((x0, y0, x0 + s2, y0 + s2)).resize((side, side), Image.LANCZOS)
    lum = ImageStat.Stat(pic.convert("L")).mean[0]
    if lum < 95: pic = ImageEnhance.Brightness(pic).enhance(min(1.9, 95 / max(lum, 20)))
    pic = ImageEnhance.Color(ImageEnhance.Contrast(pic).enhance(1.08)).enhance(1.12)
    px, py = W_ - side - 50, (H_ - side) // 2
    d.rectangle([px - 10, py - 10, px + side + 10, py + side + 10], fill=acc); bg.paste(pic, (px, py))
    p = f"{OUT}/{slug}.thumb.jpg"; bg.save(p, quality=92); print("THUMB", p, os.path.getsize(p) // 1024, "KB")


# ---------- shorts proposals ----------
def shorts(L):
    tl = json.load(open(f"{wdir(L['slug'])}/timeline.json")); S = L["steps"]; edges = tl["edges"]
    rank = {t: i for i, t in enumerate(L.get("shorts_hint", {}).get("step_priority", []))}
    cand = []
    body = [i for i, p in enumerate(S) if p["key"] not in ("hook", "end") and p.get("label")]
    for a in body:
        for b in (a, a + 1):
            if b not in body: continue
            idx = list(range(a, b + 1)); words = sum(len(S[i]["text"].split()) for i in idx)
            cl = [(S[i]["key"], c) for i in idx for c in S[i]["clips"]]
            by = {}
            for _, c in cl: by[c["src"]] = by.get(c["src"], 0) + 1
            top = max(by, key=by.get); purity = by[top] / len(cl)
            if purity < 0.75: continue  # guide_make takes one source per Short
            sec = edges[idx[-1] + 1] - edges[idx[0]]
            # a Short = our hook + these steps + close, 35-45 s, 90-115 words; score fit + purity + priority
            fit = 1 - abs(words + 30 - 100) / 100
            score = fit + purity + (0.5 if S[idx[0]]["key"] in rank and rank[S[idx[0]]["key"]] < 4 else 0) - 0.05 * (len(idx) - 1)
            cand.append({"steps": [S[i]["key"] for i in idx], "score": round(score, 2), "words_in_longform": words, "longform_start": round(edges[idx[0]], 1), "longform_end": round(edges[idx[-1] + 1], 1), "source": top, "source_purity": round(purity, 2), "source_id": L["sources"][top].get("id"), "creator": L["sources"][top].get("creator"),
                         "src_cut_points": [{"step": k, "src_start": c["start"], "zoom": c.get("zoom", 1.0)} for k, c in cl if c["src"] == top], "idx": idx, "crop": L["sources"][top].get("crop")})
    cand.sort(key=lambda c: -c["score"]); picked = []; usedsteps = set()
    for c in cand:
        if usedsteps & set(c["steps"]): continue
        picked.append(c); usedsteps |= set(c["steps"])
        if len(picked) == 4: break
    out = []
    for c in picked:
        idx = c.pop("idx"); crop = c.pop("crop")
        clips = [[cc["start"], cc.get("weight", 1), cc.get("zoom", 1.0)] for i in idx for cc in S[i]["clips"] if cc["src"] == c["source"]]
        c["guide_stub"] = {"_note": "STUB for guide_make.py: write own hook (goal + payoff) and close (comment prompt), keep 90-115 words; one goal per Short; copy to out/<source_id>.guide.json only after the script is rewritten and clips verified on sheets (guide_make caches by source id: use a new copy of the work dir if this source already has a Short)",
                           "title": L["overlay_title"], "yt_title": f"{L['overlay_title'].title()}: {S[idx[0]].get('chapter', '')} #Shorts", "evergreen": True, "creator": c["creator"], "source_id": c["source_id"], "crop_hint": crop,
                           "parts": [{"key": "hook", "text": "TODO hook: goal + payoff in 2 s", "label": None, "clips": clips[:1]}] + [{"key": f"s{n+1}", "text": S[i]["text"], "label": S[i].get("label"), "clips": [[cc["start"], cc.get("weight", 1), cc.get("zoom", 1.0)] for cc in S[i]["clips"] if cc["src"] == c["source"]]} for n, i in enumerate(idx)] + [{"key": "end", "text": "TODO close: effort + comment prompt", "label": None, "clips": clips[-1:]}],
                           "desc_steps": [S[i]["desc"] for i in idx if S[i].get("desc")], "tags": L["tags"]}
        out.append(c)
    json.dump({"slug": L["slug"], "note": "Cut-point PROPOSALS. William/agent reviews; building a Short goes through guide_make.py (GUIDE-RULES.md).", "shorts": out}, open(f"{OUT}/{L['slug']}.shorts.json", "w"), indent=1)
    for c in out: print("SHORT", c["steps"], f"{c['longform_start']}-{c['longform_end']}s", c["creator"], "score", c["score"])
    if not out: print("no single-source windows found: no Short proposals")


def upload(L):
    slug = L["slug"]; tags = ",".join(t.lstrip("#") for t in L["tags"])
    cmd = [sys.executable, B + "/yt_upload_gaming.py", f"{OUT}/{slug}.longform.mp4", "--title", L["yt_title"], "--desc-file", f"{OUT}/{slug}.desc.txt", "--thumb", f"{OUT}/{slug}.thumb.jpg", "--tags", tags, "--privacy", "private", "--category", "20"]
    r = subprocess.run(cmd, capture_output=True, text=True); open(f"{OUT}/{slug}.upload.txt", "w").write(r.stdout + r.stderr); print(r.stdout, r.stderr[-400:])


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    L = load(a[0]); cmd = a[1]; net = "--no-tts" not in a
    if cmd == "fetch": fetch(L)
    elif cmd == "sheet": sheet(L, a[2], float(a[3]), float(a[4]), float(a[5]) if len(a) > 5 else 1.0)
    elif cmd == "check": check(L)
    elif cmd == "build": build(L, net)
    elif cmd == "thumb": thumb(L)
    elif cmd == "shorts": shorts(L)
    elif cmd == "upload": upload(L)
    elif cmd == "all": build(L, net); thumb(L); shorts(L)
    else: sys.exit(__doc__)
