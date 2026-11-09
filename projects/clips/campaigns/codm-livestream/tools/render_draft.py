#!/usr/bin/env python3
"""Render one 1080x1920 TikTok draft from campaign-supplied footage (cut, crop, blurred band, ASS text).
Cuts, scales, crops and burns text only; no mirroring, speed/pitch change or other disguise.
Usage: render_draft.py SRC OUT --start S --end E [--crop x,y,w,h] [--native916] --hook TEXT
         [--cap TEXT] [--cap-from 1.0] [--label TEXT] [--hook-secs 4]
Text is burned with libass (the static ffmpeg has no drawtext), same fonts/sizes family as pipeline/format_short.py."""
import argparse, os, subprocess, tempfile
FFMPEG = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")

def ass_time(t):
    h, rem = divmod(t, 3600); m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

def esc(t): return t.replace("\\", "").replace("{", "(").replace("}", ")")

def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return "\\N".join(lines)

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--start", type=float, default=0); ap.add_argument("--end", type=float, required=True)
ap.add_argument("--crop"); ap.add_argument("--native916", action="store_true")
ap.add_argument("--hook", required=True); ap.add_argument("--hook-secs", type=float, default=4)
ap.add_argument("--cap", default=""); ap.add_argument("--cap-from", type=float, default=1.0)
ap.add_argument("--label", default=""); ap.add_argument("--label-margin", type=int, default=330)
ap.add_argument("--label-from", type=float, default=0); ap.add_argument("--label-top", action="store_true")
ap.add_argument("--loudnorm", action="store_true")
a = ap.parse_args()
dur = a.end - a.start
ev = [f"Dialogue: 0,{ass_time(0)},{ass_time(min(a.hook_secs, dur))},Hook,,0,0,0,,{wrap(esc(a.hook), 20)}"]
if a.cap: ev.append(f"Dialogue: 0,{ass_time(a.cap_from)},{ass_time(dur)},Cap,,0,0,0,,{wrap(esc(a.cap), 32)}")
if a.label: ev.append(f"Dialogue: 0,{ass_time(a.label_from)},{ass_time(dur)},Label,,0,0,0,,{wrap(esc(a.label), 40)}")
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Hook,DejaVu Sans,80,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,7,2,8,50,50,{'260' if a.native916 else '230'},1
Style: Cap,DejaVu Sans,52,&H0000F0FF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5,2,2,60,60,{'420' if a.native916 else '300'},1
Style: Label,DejaVu Sans,38,&H00DDDDDD,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,1,{8 if a.label_top else 2},60,60,{a.label_margin},1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""" + "\n".join(ev) + "\n"
with tempfile.TemporaryDirectory() as td:
    ap_ = os.path.join(td, "t.ass"); open(ap_, "w", encoding="utf-8").write(ass)
    crop = ""
    if a.crop:
        cx, cy, cw, ch = a.crop.split(","); crop = f"crop={cw}:{ch}:{cx}:{cy},"
    if a.native916:
        fg = f"[0:v]fps=30,scale=1080:1920,setsar=1,subtitles={ap_}:fontsdir=/usr/share/fonts/truetype/dejavu[v]"
    else:
        fg = (f"[0:v]fps=30,{crop}split=2[a][b];"
              "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[bg];"
              "[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,"
              f"subtitles={ap_}:fontsdir=/usr/share/fonts/truetype/dejavu[v]")
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-ss", str(a.start), "-t", str(dur), "-i", a.src,
           "-filter_complex", fg, "-map", "[v]", "-map", "0:a?",
           "-af", ("loudnorm=I=-16:TP=-1.5:LRA=11," if a.loudnorm else "") + f"afade=t=out:st={dur-0.3:.2f}:d=0.3",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", a.out]
    subprocess.run(cmd, check=True)
print("wrote", a.out, f"{dur:.1f}s")
