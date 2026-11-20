#!/usr/bin/env python3
"""finalize.py RAW.mp4 OUT.mp4 "text line" [--trim START END]
Adds the original on-screen text line (same recipe as clip_queue.add_text_line: PIL PNG overlay, static ffmpeg has no
drawtext), optional trim in seconds (re-encodes), then writes OUT.contact.jpg via sheet.py.
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

FF = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")
HERE = os.path.dirname(os.path.abspath(__file__))

raw, out, text = sys.argv[1], sys.argv[2], sys.argv[3]
trim = []
if "--trim" in sys.argv:
    i = sys.argv.index("--trim")
    trim = ["-ss", sys.argv[i + 1], "-to", sys.argv[i + 2]]

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
lines, cur = [], ""
for w in text.split():
    t = (cur + " " + w).strip()
    if d.textlength(t, font=font) > 960 and cur:
        lines.append(cur); cur = w
    else:
        cur = t
lines.append(cur)
h = 70 * len(lines) + 30
d.rectangle([40, 150, 1040, 150 + h], fill=(0, 0, 0, 150))
for i, ln in enumerate(lines):
    d.text((540, 170 + i * 70), ln, font=font, fill=(255, 221, 0, 255), anchor="ma")
png = out + ".png"
img.save(png)
# text shown 0.3 - 8 s, like the queue clips
flt = "[0:v][1:v]overlay=0:0:enable='between(t,0.3,8)'[v]"
r = subprocess.run([FF, "-y", "-loglevel", "error"] + trim + ["-i", raw, "-i", png, "-filter_complex", flt, "-map", "[v]", "-map", "0:a?",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", out], capture_output=True, text=True)
os.remove(png)
if r.returncode:
    sys.exit(r.stderr[-400:])
base = out[:-4]
subprocess.run([sys.executable, os.path.join(HERE, "sheet.py"), out, base + ".screen"], check=True)
os.replace(base + ".screen.sheet.jpg", base + ".contact.jpg")
print("OK", out)
