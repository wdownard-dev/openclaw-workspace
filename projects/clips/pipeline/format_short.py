#!/usr/bin/env python3
"""Turn a landscape clip into a 1080x1920 Short with a hook line and a context caption.

Usage:
  format_short.py INPUT OUTPUT --hook "text" [--caption "text"] [--credit "Streamer name"]
                  [--max-seconds 59] [--style 1|2|3]

Layout: blurred, scaled-up copy of the clip fills the frame; the sharp clip sits in the middle at
full width. Text is burned in with libass (the static ffmpeg build has no drawtext). Three caption
styles rotate so uploads do not all look identical. Always credits the streamer.

Only run this on clips from creators who gave written permission (see projects/clips/permissions.md).
"""
import argparse, os, subprocess, sys, tempfile

FFMPEG = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")
STYLES = {  # (font, hook size, hook colour, caption size, caption colour) in ASS BGR hex
    1: ("DejaVu Sans", 78, "&H00FFFFFF", 54, "&H0000F0FF"),
    2: ("DejaVu Sans", 84, "&H0000F0FF", 56, "&H00FFFFFF"),
    3: ("DejaVu Serif", 74, "&H00FFFFFF", 52, "&H00B4FFB4"),
}


def ass_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def esc(text):
    return text.replace("\\", "").replace("{", "(").replace("}", ")").replace("\n", "\\N")


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return "\\N".join(lines)


def duration(path):
    p = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True)
    for line in p.stderr.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    sys.exit("Could not read duration")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--hook", required=True)
    ap.add_argument("--caption", default="")
    ap.add_argument("--credit", default="")
    ap.add_argument("--max-seconds", type=float, default=59)
    ap.add_argument("--style", type=int, default=1, choices=[1, 2, 3])
    a = ap.parse_args()

    font, hsz, hcol, csz, ccol = STYLES[a.style]
    dur = min(duration(a.input), a.max_seconds)
    events = [f"Dialogue: 0,{ass_time(0)},{ass_time(min(4, dur))},Hook,,0,0,0,,{wrap(esc(a.hook), 22)}"]
    if a.caption:
        events.append(f"Dialogue: 0,{ass_time(min(1.0, dur))},{ass_time(dur)},Cap,,0,0,0,,{wrap(esc(a.caption), 34)}")
    if a.credit:
        events.append(f"Dialogue: 0,{ass_time(0)},{ass_time(dur)},Credit,,0,0,0,,Clip: {esc(a.credit)}")
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Hook,{font},{hsz},{hcol},&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,2,8,60,60,230,1
Style: Cap,{font},{csz},{ccol},&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5,2,2,60,60,300,1
Style: Credit,{font},38,&H00DDDDDD,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,3,1,1,50,50,120,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""" + "\n".join(events) + "\n"

    with tempfile.TemporaryDirectory() as td:
        ass_path = os.path.join(td, "t.ass")
        open(ass_path, "w", encoding="utf-8").write(ass)
        fg = (
            "[0:v]split=2[a][b];"
            "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[bg];"
            "[b]scale=1080:-2[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,"
            f"subtitles={ass_path}:fontsdir=/usr/share/fonts/truetype/dejavu[v]"
        )
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-t", str(dur), "-i", a.input, "-filter_complex", fg,
               "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
               "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", a.output]
        subprocess.run(cmd, check=True)
    print(f"wrote {a.output} ({dur:.1f}s)")


if __name__ == "__main__":
    main()
