#!/usr/bin/env python
"""NULL//SMIRK AI co-host renderer (variant A). Run with the tts-venv python.
  render_cohost.py prep   CLIP.mp4 --story "..." --handle @name [--slug s] [--facts-file f.json] [--urls U...] [--structure id]
  render_cohost.py check  SLUG                      fact-check report only
  render_cohost.py render SLUG [--skip-tts] [--allow-repeat]   guard -> TTS -> render -> out/SLUG-{cohost.mp4,factcheck.md,description.txt}
See README.md. Script writing is done by the agent (prompts/script_prompt.md -> work/SLUG/script.json)."""
import argparse, hashlib, json, os, random, re, shutil, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import facts as F
import factcheck as FC

CFG = F.CFG
W, H, SR = 1080, 1920, 24000
FPS = CFG["fps"]
STATE = os.path.join(HERE, "state.json")
LEVEL = CFG.get("interrupt_level", "low")
LV = CFG["levels"][LEVEL]
AI_TAG = CFG.get("ai_tag", "always")


def set_level(name):
    global LEVEL, LV
    if name:
        LEVEL, LV = name, CFG["levels"][name]


def set_ai_tag(v):
    global AI_TAG
    if v:
        AI_TAG = v


def wrap_lines(text, width):
    import textwrap
    n = -(-len(text) // width)
    return textwrap.wrap(text, -(-len(text) // n) + 3 if n > 1 else width, break_long_words=False)  # balanced lines, no one-word widows


def wdir(slug):
    d = os.path.join(HERE, "work", slug)
    os.makedirs(d, exist_ok=True)
    return d


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"history": []}


# ------------------------------------------------------------------ prep
def cmd_prep(a):
    slug = a.slug or re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(a.clip))[0].lower()).strip("-")
    d = wdir(slug)
    clip = os.path.abspath(a.clip)
    json.dump({"clip": clip, "story": a.story, "handle": a.handle}, open(os.path.join(d, "job.json"), "w"), indent=1)
    t0 = time.time()
    tj = os.path.join(d, "transcript.json")
    if not os.path.exists(tj):
        subprocess.run([CFG["whisper_python"], "-I", os.path.join(HERE, "transcribe.py"), clip, tj, CFG["whisper_model"], CFG["whisper_dir"]], check=True)
    tr = json.load(open(tj))
    with open(os.path.join(d, "transcript.txt"), "w") as f:
        for s in tr["segments"]:
            f.write(f"[{s['start']:6.2f}-{s['end']:6.2f}] {s['text']}\n")
            f.write("    words: " + " ".join(f"{w['w']}@{w['start']}" for w in s["words"]) + "\n")
    print(f"transcript: {len(tr['segments'])} segments ({time.time()-t0:.0f}s)")
    if a.urls:
        for u in a.urls:
            F.fetch(slug, u)
    fnote = ""
    if a.facts_file:
        shutil.copy(a.facts_file, os.path.join(d, "facts.json"))
        fnote = "- Facts file supplied by the operator: copied to work/%s/facts.json (still verified against fetched pages; run facts.py fetch for its URLs)." % slug
    structures = json.load(open(os.path.join(HERE, "structures.json")))
    hist = load_state()["history"]
    recent = [h["structure"] for h in hist[-2:]]
    if a.structure:
        st = next(s for s in structures if s["id"] == a.structure)
    else:
        pool = [s for s in structures if s["id"] not in recent] or structures
        st = random.Random(hashlib.sha1(slug.encode()).hexdigest()).choice(pool)
    prev = hist[-1] if hist else None
    prev_note = f"previous output '{prev['slug']}' used structure '{prev['structure']}'" if prev else "no previous output"
    tpl = open(os.path.join(HERE, "prompts", "script_prompt.md")).read()
    sub = {"slug": slug, "story": a.story, "handle": a.handle, "structure": st["id"], "structure_name": st["name"], "structure_guide": st["guide"], "level": LEVEL, "max_interj": LV["max_interjections"], "max_interj_s": LV["max_interjection_s"], "max_cards": LV["max_cards"], "card_lo": LV["card_dur"][0], "card_hi": LV["card_dur"][1], "outro_max": LV["outro_max_s"],
           "reaction_style": st["reaction_style"], "duration": f"{tr['duration']:.1f}", "max_words": CFG["max_line_words"],
           "facts_file_note": fnote, "previous_note": prev_note}
    for k, v in sub.items():
        tpl = tpl.replace("{{" + k + "}}", str(v))
    open(os.path.join(d, "prompt.md"), "w").write(tpl)
    print(f"slug={slug} structure={st['id']}\nprompt: {os.path.join(d, 'prompt.md')}\nnext: write {os.path.join(d, 'facts.json')} and {os.path.join(d, 'script.json')}, then: render_cohost.py render {slug}")


def cmd_gaps(a):
    tr = json.load(open(os.path.join(wdir(a.slug), "transcript.json")))
    ws = [w for sg in tr["segments"] for w in sg["words"]]
    print(f"pauses >= {a.min} s between transcript words (source-clip seconds); start spoken interjections inside these:")
    for x, y in zip(ws, ws[1:]):
        if y["start"] - x["end"] >= a.min:
            print(f"  {x['end']:6.2f} - {y['start']:6.2f}  ({y['start'] - x['end']:.2f} s)  after '{x['w']}', before '{y['w']}'")


# ------------------------------------------------------------------ check
def run_check(slug):
    passed, md, valid = FC.check(slug, level=LEVEL)
    return passed, md, valid


def cmd_check(a):
    passed, md, _ = run_check(a.slug)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    open(os.path.join(HERE, "out", f"{a.slug}-factcheck.md"), "w").write(md)
    print(md if not passed else f"fact-check PASS -> out/{a.slug}-factcheck.md")
    sys.exit(0 if passed else 1)


# ------------------------------------------------------------------ TTS
def synth(slug, script, d):
    import soundfile as sf
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    cs, cl = script["clip"]["start"], script["clip"]["len"]
    lines = [dict(r, kind="interjection") for r in script.get("interjections", [])] + [dict(o, kind="outro") for o in script["outro"]]
    for l in lines:
        sp = LV["outro_speed"] if l["kind"] == "outro" else CFG["speed"]
        wav = np.concatenate([r[2].numpy() for r in pipe(l["text"], voice=CFG["voice"], speed=sp)])
        l["wav"] = np.concatenate([wav, np.zeros(int(0.10 * SR))]).astype(np.float32)
        l["dur"] = len(l["wav"]) / SR
    tl, last_end = [], 0.0
    problems = []
    for l in [x for x in lines if x["kind"] == "interjection"]:
        start = max(l["t"] - cs, 0.1, last_end + 0.3)
        l.update(start=start, end=start + l["dur"])
        last_end = l["end"]
        if l["dur"] > LV["max_interjection_s"]:
            problems.append(f"interjection {l['id']} is {l['dur']:.1f}s, max {LV['max_interjection_s']}s at interrupt_level {LEVEL}")
        words_all = [w for sg in json.load(open(os.path.join(d, "transcript.json")))["segments"] for w in sg["words"]]
        spoken_end = l["end"] - 0.12
        for w in words_all:
            if w["start"] < spoken_end + cs + 0.02 and w["start"] > start + cs - 0.02:
                problems.append(f"interjection {l['id']} ({start + cs:.2f}-{spoken_end + cs:.2f} source s) runs over source speech '{w['w']}' at {w['start']}s")
                break
        for a_, b_ in script["clip"].get("protect", []):
            if start + cs < b_ and l["end"] + cs > a_:
                problems.append(f"interjection {l['id']} ({start + cs:.1f}-{l['end'] + cs:.1f} source s) overlaps protected key line {a_}-{b_}")
        if l["end"] > cl - 0.2:
            problems.append(f"interjection {l['id']} ends at {l['end']:.1f}s, past clip end {cl}s")
        tl.append(l)
    cur = cl - CFG["fade"] + 0.1
    for l in [x for x in lines if x["kind"] == "outro"]:
        l.update(start=cur, end=cur + l["dur"])
        cur = l["end"] + CFG["outro_gap"]
        tl.append(l)
    total = max(t["end"] for t in tl) + CFG["tail"]
    outro_s = total - (cl - CFG["fade"])
    if outro_s > LV["outro_max_s"]:
        problems.append(f"outro is {outro_s:.1f}s, max {LV['outro_max_s']}s at interrupt_level {LEVEL}: shorten the outro lines")
    if problems:
        print("line durations:", {l["id"]: round(l["dur"], 2) for l in lines})
        print("REFUSING TO RENDER (timing):\n- " + "\n- ".join(problems))
        sys.exit(4)
    mix = np.zeros(int(total * SR), np.float32)
    for t in tl:
        i = int(t["start"] * SR)
        mix[i:i + len(t["wav"])] += t["wav"]
    mix *= 0.92 / max(1e-6, np.abs(mix).max())
    sf.write(os.path.join(d, "voice.wav"), mix, SR)
    for t in tl:
        t.pop("wav")
    json.dump({"total": total, "timeline": tl}, open(os.path.join(d, "timeline.json"), "w"), indent=1)
    return tl, mix, total


def place_cards(script):
    """cards -> [{id,start,end,text,label,facts}] in video time"""
    cs = script["clip"]["start"]
    out = []
    for c in script.get("cards", []):
        st = max(c["t"] - cs, 0.1)
        out.append(dict(c, start=st, end=st + c.get("dur", 2.5)))
    return out


# ------------------------------------------------------------------ ASS
def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def chunk_words(text, n=4):
    w = text.split()
    k = -(-len(w) // n)
    return [" ".join(c) for c in np.array_split(np.array(w, dtype=object), k)]


def esc(s):
    return s.replace("{", "(").replace("}", ")")


def pretty_url(u):
    return re.sub(r"^https?://(www\.)?", "", u)


def short_src(f):
    """host + page title (from the fact's 'source' field, minus the author in parentheses) for the small on-screen credit"""
    host = re.sub(r"^www\.", "", re.sub(r"^https?://", "", f["url"]).split("/")[0])
    title = re.sub(r"\s*\(.*?\)\s*$", "", f.get("source", ""))
    return f"{host} - {title}" if title else pretty_url(f["url"])


def write_ass(slug, script, tl, total, valid, d, cards):
    fn = CFG["font"]
    cl = script["clip"]["len"]
    handle = script["clip"]["handle"]
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,{fn},62,&H00FFFFFF,&H000000FF,&H00281E1C,&H00000000,-1,0,0,0,100,100,0,0,1,5,1,8,50,50,1215,1
Style: CapOut,{fn},74,&H00FFFFFF,&H000000FF,&H00281E1C,&H00000000,-1,0,0,0,100,100,0,0,1,7,2,8,50,50,1310,1
Style: Tag,{fn},30,&H00FFFFFF,&H00000000,&H90281E1C,&H90281E1C,-1,0,0,0,100,100,2,0,3,8,0,9,0,32,34,1
Style: Part,{fn},56,&H0028281C,&H00000000,&H004AFF9B,&H004AFF9B,-1,0,0,0,100,100,3,0,3,12,0,8,0,0,1180,1
Style: Name,{fn},66,&H00FF9CC9,&H00000000,&H00281E1C,&H00000000,-1,0,0,0,100,100,6,0,1,4,0,2,0,0,1630,1
Style: Credit,{fn},44,&H00FFFFFF,&H00000000,&H00000000,&H00000000,-1,0,0,0,100,100,1,0,1,4,1,1,48,0,70,1
Style: CardHead,{fn},58,&H004AFF9B,&H00000000,&H00281E1C,&H00000000,-1,0,0,0,100,100,3,0,1,5,0,8,60,60,1560,1
Style: CardBody,{fn},50,&H00FFFFFF,&H00000000,&H00281E1C,&H00000000,-1,0,0,0,100,100,0,0,1,5,0,8,60,60,1630,1
Style: Box,{fn},40,&HE0281E1C,&H00000000,&H004AFF9B,&H00000000,0,0,0,0,100,100,0,0,1,3,0,7,0,0,0,1
Style: CardLabel,{fn},30,&H004AFF9B,&H00000000,&H00000000,&H00000000,-1,0,0,0,100,100,3,0,0,0,0,7,0,0,0,1
Style: CardText,{fn},42,&H00FFFFFF,&H00000000,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,0,0,0,7,0,0,0,1
Style: CardSrc2,{fn},28,&H00D8D8D8,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,0,0,0,7,0,0,0,1
Style: CardSrc,{fn},32,&H00E0E0E0,&H00000000,&H00281E1C,&H00000000,0,0,0,0,100,100,0,0,1,4,0,8,60,60,1740,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    t_out = cl - CFG["fade"]
    ev = [f"Dialogue: 0,{ts(0)},{ts(total)},Credit,,0,0,0,,Source: {esc(handle)}  (clip footage)",
          f"Dialogue: 0,{ts(t_out + 0.4)},{ts(total)},Name,,0,0,0,,{{\\an8\\pos(540,215)}}NULL//SMIRK"]
    if AI_TAG == "always":
        ev.append(f"Dialogue: 0,{ts(0)},{ts(total)},Tag,,0,0,0,,AI CO-HOST")
    elif AI_TAG == "intro_outro":
        ev.append(f"Dialogue: 0,{ts(0)},{ts(3.0)},Tag,,0,0,0,,{{\\fad(0,300)}}AI CO-HOST")
        ev.append(f"Dialogue: 0,{ts(t_out + 0.2)},{ts(total)},Tag,,0,0,0,,AI CO-HOST")
    for t in tl:
        if t["kind"] == "interjection":
            lines_ = wrap_lines(t["text"].upper(), 24)
            ev.append(f"Dialogue: 0,{ts(t['start'])},{ts(t['end'] + 0.25)},Cap,,0,0,0,,{{\\an8\\pos(540,{CFG['layout']['cap_y']})}}{'\\N'.join(esc(x) for x in lines_)}")
        else:
            # outro: the whole sentence stays on screen for the whole line, wrapped over several lines (never chunked or cut)
            lines_ = wrap_lines(t["text"].upper(), 22)
            end = t["end"] + 0.35
            ev.append(f"Dialogue: 0,{ts(t['start'])},{ts(end)},CapOut,,0,0,0,,{{\\an8\\pos(540,1200)}}{'\\N'.join(esc(x) for x in lines_)}")
            if t.get("part"):
                ev.append(f"Dialogue: 1,{ts(t['start'])},{ts(end)},Part,,0,0,0,,{{\\an8\\pos(540,1120)}}{t['part'].upper().replace('QUESTION', 'YOUR TURN').replace('OPINION', 'MY TAKE')}")
        c = t.get("card")
        if c:
            end = t["end"] + 0.4
            ev.append(f"Dialogue: 1,{ts(t['start'])},{ts(end)},CardHead,,0,0,0,,{{\\an8\\pos(540,1560)}}{esc(c['head'].upper())}")
            ev.append(f"Dialogue: 1,{ts(t['start'])},{ts(end)},CardBody,,0,0,0,,{{\\an8\\pos(540,1630)}}{esc(c['body'])}")
            srcs = [valid[f] for f in t.get("facts", []) if f in valid]
            if srcs:
                s = srcs[0]
                dt = "" if s["date"] == "Unknown" else f" ({s['date']})"
                ev.append(f"Dialogue: 1,{ts(t['start'])},{ts(end)},CardSrc,,0,0,0,,{{\\an8\\pos(540,1700)}}Source: {esc(short_src(s))}{dt}")
    # comment cards: dark rounded-ish box left of NULL, tail pointing at NULL, text wrapped by hand
    import textwrap
    for c in cards:
        lines_ = textwrap.wrap(c["text"], 24)
        srcs = [valid[f] for f in c.get("facts", []) if f in valid]
        src_line = ""
        if srcs:
            sv = srcs[0]
            src_line = f"{re.sub(r'^www[.]', '', re.sub(r'^https?://', '', sv['url']).split('/')[0])}" + ("" if sv["date"] == "Unknown" else f" ({sv['date']})")
        label = c.get("label", "NOTE")
        h = 44 + len(lines_) * 50 + (36 if src_line else 0) + 16
        x0, w = CFG["layout"]["card_x"], CFG["layout"]["card_w"]
        y0 = int(CFG["layout"]["card_cy"] - h / 2)
        t0, t1 = ts(c["start"]), ts(c["end"])
        fad = "{\\fad(160,160)}"
        ev.append(f"Dialogue: 2,{t0},{t1},Box,,0,0,0,,{{\\an7\\pos({x0},{y0})\\p1\\fad(160,160)}}m 0 0 l {w} 0 {w} {h} 0 {h}{{\\p0}}")
        ev.append(f"Dialogue: 2,{t0},{t1},Box,,0,0,0,,{{\\an7\\pos({x0 + w},{y0 + h // 2 - 22})\\p1\\fad(160,160)}}m 0 0 l 30 22 0 44{{\\p0}}")
        ev.append(f"Dialogue: 3,{t0},{t1},CardLabel,,0,0,0,,{{\\an7\\pos({x0 + 18},{y0 + 8})\\fad(160,160)}}{esc(label.upper())}")
        ev.append(f"Dialogue: 3,{t0},{t1},CardText,,0,0,0,,{{\\an7\\pos({x0 + 18},{y0 + 44})\\fad(160,160)}}{'\\N'.join(esc(x) for x in lines_)}")
        if src_line:
            ev.append(f"Dialogue: 3,{t0},{t1},CardSrc2,,0,0,0,,{{\\an7\\pos({x0 + 18},{y0 + 44 + len(lines_) * 50 + 2})\\fad(160,160)}}{esc(src_line)}")
    open(os.path.join(d, "captions.ass"), "w").write(hdr + "\n".join(ev) + "\n")


def make_bg(d):
    from PIL import Image, ImageDraw
    px = np.zeros((H, W, 3), np.float32)
    top, bot = np.array([12, 8, 34]), np.array([34, 14, 70])
    g = np.linspace(0, 1, H)[:, None, None]
    px[:] = top * (1 - g) + bot * g
    im = Image.fromarray(px.astype(np.uint8))
    dr = ImageDraw.Draw(im, "RGBA")
    for i, (x, y, r) in enumerate([(120, 260, 260), (960, 520, 190), (200, 1500, 300), (930, 1700, 230), (540, 900, 470)]):
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(139, 77, 255, 12 + 4 * (i % 3)))
    for y in range(0, H, 96):
        dr.line([(0, y), (W, y)], fill=(155, 255, 74, 10), width=2)
    im.save(os.path.join(d, "outro_bg.png"))


# ------------------------------------------------------------------ avatar
def build_events(tl, script):
    ev = []
    for t in tl:
        for x in t.get("expr") or [["0", "smug"]]:
            ev.append([t["start"] + float(x[0]), x[1], float(x[2]) if len(x) > 2 else None])
        ev.append([t["end"] + 0.35, "smug", None])
    cs = script["clip"]["start"]
    for x in script.get("expressions", []):
        st = max(x["t"] - cs, 0.05)
        dur = float(x.get("dur", 1.4))
        ev.append([st, x["expr"], dur])
        ev.append([st + dur + 0.15, "smug", None])
    for c in script.get("cards", []):                      # NULL "reads" its own card: a held expression
        if c.get("expr"):
            st = max(c["t"] - cs, 0.05)
            ev.append([st + 0.2, c["expr"], min(1.6, c.get("dur", 2.5))])
            ev.append([st + 0.2 + min(1.6, c.get("dur", 2.5)) + 0.15, "smug", None])
    ev.sort(key=lambda e: e[0])
    for i, e in enumerate(ev):
        if e[2] is None:
            e[2] = (ev[i + 1][0] - e[0]) if i + 1 < len(ev) else 99
    return ev


def raw_pose(N, t, ev):
    cur = None
    for s, nm, dd in ev:
        if s <= t:
            cur = (s, nm, dd)
    if cur is None:
        return N.EXPR["smug"]
    s, nm, dd = cur
    if nm == "roll":
        u = (t - s) / max(dd, 0.1)
        return N.roll_pose(min(1.0, max(0.0, u))) if u <= 1.0 else N.EXPR["smug"]
    return N.EXPR[nm]


def mouth_states(mix, n):
    hop = SR // FPS
    env = np.array([np.sqrt(np.mean(mix[i * hop:(i + 1) * hop + hop // 2] ** 2) + 1e-12) if i * hop < len(mix) else 0 for i in range(n)])
    ref = np.percentile(env[env > 0.01], 90) if (env > 0.01).any() else 1
    e = env / ref
    st = np.digitize(e, [0.12, 0.38, 0.70])
    pad = np.pad(st, 1, mode="edge")
    return np.median(np.stack([pad[:-2], pad[1:-1], pad[2:]]), axis=0).astype(int), np.clip(e, 0, 1.2)


def ease(x):
    x = min(max(x, 0), 1)
    return x * x * (3 - 2 * x)


def stream_mascot(proc, mix, n, tl, script, T0):
    from PIL import Image
    sys.path.insert(0, CFG["nullv2_dir"])
    import null_v2 as N
    N.RES = 800
    L = CFG["layout"]
    ev = build_events(tl, script)
    st, env = mouth_states(mix, n)
    MOUTHS = ["closed", "small", "open", "wide"]
    t_out = script["clip"]["len"] - CFG["fade"]
    cur = dict(N.EXPR["smug"])
    blink_times = [2.1 + 3.4 * i for i in range(40)]
    for f in range(n):
        t = f / FPS
        tgt = raw_pose(N, t, ev)
        cur = {k: cur[k] + (tgt[k] - cur[k]) * 0.45 for k in cur}
        p = dict(cur)
        spk = env[f] if st[f] > 0 else 0.0
        bounce = 2.0 * round(min(1, spk) * 3)
        p["bLy"] -= bounce
        p["bRy"] -= bounce
        nb = min(abs(t - b) for b in blink_times)
        if nb < 0.09 and p["laugh"] < 0.3 and p["squint"] < 0.1:
            p["blink"] = 1.0 - nb / 0.09 * 0.15
        tilt = p["tilt"] + 2.2 * np.sin(t * 0.55) + 0.8 * np.sin(t * 1.3 + 1)
        im = N.compose(CFG["variant"], MOUTHS[st[f]], p)
        k = ease((t - t_out) / 0.7)
        size = int(L["mascot_small"] + (L["mascot_big"] - L["mascot_small"]) * k)
        x = int(L["small_xy"][0] + (L["big_xy"][0] - L["small_xy"][0]) * k)
        y = int(L["small_xy"][1] + (L["big_xy"][1] - L["small_xy"][1]) * k)
        y += int(7 * np.sin(t * 2.6)) - int(12 * min(1, spk))
        im = im.rotate(tilt, resample=Image.BICUBIC, center=(N.RES / 2, N.RES * 0.78)).resize((size, size), Image.LANCZOS)
        al = LV["mascot_alpha"] + (1.0 - LV["mascot_alpha"]) * k
        if al < 0.999:
            r_, g_, b_, a_ = im.split()
            im = Image.merge("RGBA", (r_, g_, b_, a_.point(lambda v, al=al: int(v * al))))
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.alpha_composite(im, (x, y))
        proc.stdin.write(layer.tobytes())
        if f % 150 == 0:
            print(f"  frame {f}/{n}  {time.time() - T0:.0f}s", flush=True)
    proc.stdin.close()


# ------------------------------------------------------------------ description
def write_description(slug, script, valid, out_path, dur):
    handle = script["clip"]["handle"]
    used = []
    for o in script.get("interjections", []) + script.get("cards", []) + script["outro"]:
        for f in o.get("facts", []):
            if f in valid and f not in used:
                used.append(f)
    title = script.get("title", slug)
    lines = [f"TITLE: {title}", "", "DESCRIPTION:",
             script.get("description_intro", "").strip() or "A clip with an AI co-host adding sourced context.", "",
             "WHAT NULL ADDS (from official sources):"]
    for c in script.get("cards", []):
        lines.append(f"- {c['text']}")
    for o in script["outro"]:
        if o["part"] == "takeaway":
            lines.append(f"- {o['text']}")
    lines += ["", "SOURCES:"]
    seen = set()
    for f in used:
        v = valid[f]
        if v["url"] in seen:
            continue
        seen.add(v["url"])
        dt = "" if v["date"] == "Unknown" else f" ({v['date']})"
        lines.append(f"- {v.get('source', pretty_url(v['url']))}{dt}: {v['url']}")
    lines += ["", f"Clip footage: Source: {handle}. Footage belongs to its creator; this video adds commentary and context.", "",
              CFG["disclosure"], "", "#NULLSMIRK #AIcohost",
              "", "--- NOT FOR PASTING (William, confirm in YouTube Studio before posting) ---",
              "Altered/synthetic content label: NULL is a stylized, non-realistic cartoon with a synthetic voice, not a real person or a realistic scene, so YouTube's disclosure rule should not apply. Studio is the authority: confirm the answer on the upload form.",
              "Paid-promotion/ownership: if the footage comes from a paid partnership or campaign, check that the campaign terms allow reuse on this channel."]
    open(out_path, "w").write("\n".join(lines) + "\n")


# ------------------------------------------------------------------ render
def cmd_render(a):
    slug = a.slug
    d = wdir(slug)
    job = json.load(open(os.path.join(d, "job.json")))
    script = json.load(open(os.path.join(d, "script.json")))
    passed, md, valid = run_check(slug)
    out_dir = os.path.join(HERE, "out")
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, f"{slug}-factcheck.md"), "w").write(md)
    if not passed:
        print("REFUSING TO RENDER: fact-check failed\n" + md)
        sys.exit(2)
    hist = load_state()["history"]
    if hist and hist[-1]["structure"] == script["structure"] and hist[-1]["slug"] != slug and not a.allow_repeat:
        print(f"REFUSING: structure '{script['structure']}' was used by the previous output ({hist[-1]['slug']}); pick another or --allow-repeat")
        sys.exit(3)
    T0 = time.time()
    if a.skip_tts and os.path.exists(os.path.join(d, "timeline.json")):
        import soundfile as sf
        dj = json.load(open(os.path.join(d, "timeline.json")))
        tl, total = dj["timeline"], dj["total"]
        mix, _ = sf.read(os.path.join(d, "voice.wav"), dtype="float32")
        # keep newest card/expr edits from script
        byid = {x["id"]: x for x in script.get("interjections", []) + script["outro"]}
        for t in tl:
            t.update({k: v for k, v in byid[t["id"]].items() if k in ("card", "expr", "facts")})
    else:
        tl, mix, total = synth(slug, script, d)
    t_tts = time.time() - T0
    cards = place_cards(script)
    write_ass(slug, script, tl, total, valid, d, cards)
    make_bg(d)
    ss, cl, fade = script["clip"]["start"], script["clip"]["len"], CFG["fade"]
    n = int(total * FPS)
    ass = os.path.join(d, "captions.ass")
    L = CFG["layout"]
    duck = "1"
    ij = [t for t in tl if t["kind"] == "interjection"]
    if ij:
        g = 10 ** (LV.get("duck_db", -6) / 20)
        duck = "if(" + "+".join(f"between(t,{t['start'] - 0.08:.2f},{t['end'] + 0.12:.2f})" for t in ij) + f",{g:.3f},1)"
    fc = (
        f"[0:v]trim=start={ss}:end={ss + cl},setpts=PTS-STARTPTS,fps={FPS},split[a][b];"
        f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:6,eq=brightness=-0.08[bg];"
        f"[b]crop={L['clip_crop_w']}:1080,scale={W}:{L['clip_h']}[fg];[bg][fg]overlay=0:{L['clip_y']},format=yuv420p[clipv];"
        f"[1:v]format=yuv420p,fps={FPS}[ob];"
        f"[clipv][ob]xfade=transition=fade:duration={fade}:offset={cl - fade}[base];"
        f"[base][2:v]overlay=0:0:format=auto[m];"
        f"[m]ass={ass}:fontsdir={CFG['fontsdir']}[v];"
        f"[0:a]atrim=start={ss}:end={ss + cl},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=0.9,volume='{duck}':eval=frame[du];"
        f"[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.6[v2];"
        f"[du]afade=t=out:st={cl - 0.6}:d=0.6[du2];"
        f"[du2][v2]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95,apad,atrim=0:{total:.3f}[a]"
    )
    out = os.path.join(out_dir, f"{slug}-cohost.mp4")
    crf = 23
    cmd = [CFG["ffmpeg"], "-y", "-hide_banner", "-loglevel", "error", "-i", job["clip"],
           "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", os.path.join(d, "outro_bg.png"),
           "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", os.path.join(d, "voice.wav"), "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
           "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-maxrate", "6M", "-bufsize", "12M",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    t1 = time.time()
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    stream_mascot(p, mix, n, tl, script, T0)
    p.wait()
    mb = os.path.getsize(out) / 1e6
    write_description(slug, script, valid, os.path.join(out_dir, f"{slug}-description.txt"), total)
    # original vs source accounting (seconds)
    outro_s = total - (cl - fade)
    spans = [(t["start"], t["end"]) for t in tl if t["kind"] == "interjection"] + [(c["start"], c["end"]) for c in cards]
    spans.sort()
    union, cur_s, cur_e = 0.0, None, None
    for x, y in spans:
        y = min(y, cl - fade)
        if cur_e is None or x > cur_e:
            if cur_e is not None:
                union += cur_e - cur_s
            cur_s, cur_e = x, y
        else:
            cur_e = max(cur_e, y)
    if cur_e is not None:
        union += cur_e - cur_s
    spoken = sum(t["end"] - t["start"] for t in tl)
    orig = outro_s + union
    acct = {"interrupt_level": LEVEL, "total_s": round(total, 1), "source_clip_s": cl, "outro_s": round(outro_s, 1),
            "in_clip_added_content_s": round(union, 1), "cards": len(cards), "spoken_interjections": sum(1 for t in tl if t["kind"] == "interjection"),
            "cohost_voice_s": round(spoken, 1), "original_content_s": round(orig, 1), "original_share_pct": round(100 * orig / total, 1),
            "clip_only_share_pct": round(100 * (cl - fade - union) / total, 1), "mb": round(mb, 1), "render_s": round(time.time() - T0), "tts_prep_s": round(t_tts)}
    json.dump(acct, open(os.path.join(d, "accounting.json"), "w"), indent=1)
    st = load_state()
    st["history"] = [h for h in st["history"] if h["slug"] != slug] + [{"slug": slug, "structure": script["structure"], "date": time.strftime("%Y-%m-%d")}]
    json.dump(st, open(STATE, "w"), indent=1)
    print(f"done {out} rc={p.returncode} {mb:.1f} MB; {acct}")
    if mb > CFG["max_mb"]:
        print("WARN: over size limit; raise crf")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prep"); p.add_argument("clip"); p.add_argument("--story", required=True); p.add_argument("--handle", required=True)
    p.add_argument("--slug"); p.add_argument("--facts-file"); p.add_argument("--urls", nargs="*"); p.add_argument("--structure")
    p = sub.add_parser("check"); p.add_argument("slug")
    p = sub.add_parser("render"); p.add_argument("slug"); p.add_argument("--skip-tts", action="store_true"); p.add_argument("--allow-repeat", action="store_true")
    p = sub.add_parser("gaps"); p.add_argument("slug"); p.add_argument("--min", type=float, default=0.4)
    for sp in sub.choices.values():
        sp.add_argument("--interrupt-level", choices=list(CFG["levels"]))
        sp.add_argument("--ai-tag", choices=["always", "intro_outro", "off"])
    a = ap.parse_args()
    set_level(a.interrupt_level)
    set_ai_tag(a.ai_tag)
    {"prep": cmd_prep, "check": cmd_check, "render": cmd_render, "gaps": cmd_gaps}[a.cmd](a)
