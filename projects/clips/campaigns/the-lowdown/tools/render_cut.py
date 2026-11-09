#!/usr/bin/env python3
"""Render a 1080x1920 TikTok draft from campaign-supplied footage: cut/join ranges, optional hook text and
word-synced subtitles (burned with libass), no speed/pitch/mirror changes, source audio untouched (no loudnorm).
Usage: render_cut.py SRC OUT --segs "0-14.32,17.18-34.9" [--hook TEXT --hook-secs 3] [--words words.json]
       [--sub-color yellow|white] [--sub-margin 420] [--hook-margin 230] [--blur] [--fix a=b ...]
--blur: source is not 9:16; fit full frame over a blurred copy (same as render_draft.py band layout).
--fix FROM=TO: replace words in subtitles (e.g. Viro=Vyro). Subtitles use the word times in --words (source timeline)."""
import argparse, json, os, re, subprocess, tempfile
FFMPEG = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--segs", required=True)
ap.add_argument("--hook", default=""); ap.add_argument("--hook-secs", type=float, default=3)
ap.add_argument("--words"); ap.add_argument("--sub-color", default="white")
ap.add_argument("--sub-margin", type=int, default=420); ap.add_argument("--hook-margin", type=int, default=230)
ap.add_argument("--blur", action="store_true"); ap.add_argument("--fix", nargs="*", default=[])
ap.add_argument("--hook-size", type=int, default=76)
a = ap.parse_args()
segs = [tuple(float(x) for x in s.split("-")) for s in a.segs.split(",")]
total = sum(e - s for s, e in segs)
def ass_time(t):
    h, rem = divmod(t, 3600); m, s = divmod(rem, 60); return f"{int(h)}:{int(m):02d}:{s:05.2f}"
def to_out(t):  # source time -> output time (None if cut)
    o = 0
    for s, e in segs:
        if s - 0.01 <= t < e: return o + max(0, t - s)
        o += e - s
    return None
def wrap(text, width):
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > width and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return "\\N".join(lines)
fix = dict(f.split("=", 1) for f in a.fix)
ev = []
if a.hook:
    ev.append(f"Dialogue: 1,{ass_time(0)},{ass_time(min(a.hook_secs, total))},Hook,,0,0,0,,{wrap(a.hook.replace('{','(').replace('}',')'), 20)}")
if a.words:
    words = [w for w in json.load(open(a.words)) if to_out(w["s"]) is not None]
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        txt = w["w"]
        if len(cur) >= 4 or re.search(r"[.,?!]$", txt):
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    for i, c in enumerate(chunks):
        t0 = to_out(c[0]["s"]); nxt = to_out(chunks[i + 1][0]["s"]) if i + 1 < len(chunks) else None
        t1 = min(c[-1]["e"] - c[0]["s"] + t0 + 0.4, nxt if nxt is not None and nxt > t0 else 1e9, t0 + 2.2, total)
        txt = " ".join(fix.get(re.sub(r"[.,?!]$", "", w["w"]), w["w"]) if re.sub(r"[.,?!]$", "", w["w"]) in fix else w["w"] for w in c)
        txt = re.sub(r"[,.]$", "", txt).replace(" .com", ".com")
        ev.append(f"Dialogue: 0,{ass_time(t0)},{ass_time(t1)},Sub,,0,0,0,,{wrap(txt, 22)}")
col = {"white": "&H00FFFFFF", "yellow": "&H0000F0FF"}[a.sub_color]
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Hook,DejaVu Sans,{a.hook_size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,2,8,50,50,{a.hook_margin},1
Style: Sub,DejaVu Sans,58,{col},&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,2,2,60,60,{a.sub_margin},1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""" + "\n".join(ev) + "\n"
n = len(segs)
vtrim = "".join(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e-s-0.02:.3f}:d=0.02[a{i}];" for i, (s, e) in enumerate(segs))
cc = "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac];"
with tempfile.TemporaryDirectory() as td:
    ap_ = os.path.join(td, "t.ass"); open(ap_, "w", encoding="utf-8").write(ass)
    subs = f"subtitles={ap_}:fontsdir=/usr/share/fonts/truetype/dejavu"
    if a.blur:
        v = ("[vc]fps=30,split=2[x][y];[x]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[bg];"
             f"[y]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,{subs}[v]")
    else:
        v = f"[vc]fps=30,scale=1080:1920,setsar=1,{subs}[v]"
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", a.src, "-filter_complex", vtrim + cc + v,
           "-map", "[v]", "-map", "[ac]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", a.out]
    subprocess.run(cmd, check=True)
print("wrote", a.out, f"{total:.1f}s")
