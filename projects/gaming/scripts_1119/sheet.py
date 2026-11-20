#!/usr/bin/env python3
"""Screening sheets for a finished 1080x1920 Short: first-7s strip (8 frames, 1/s from 0.3 s) and a full 10-frame sheet.
Usage: sheet.py CLIP.mp4 OUTPREFIX [--start-only]
"""
import os, subprocess, sys, tempfile, json
from PIL import Image, ImageDraw

FF = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")


def frame(clip, t, path):
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", clip, "-frames:v", "1", "-vf", "scale=270:480", path], check=True)


def dur(clip):
    r = subprocess.run([FF, "-i", clip], capture_output=True, text=True).stderr
    for ln in r.splitlines():
        if "Duration" in ln:
            h, m, s = ln.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0


def sheet(clip, times, out, cols):
    tmp = tempfile.mkdtemp()
    ims = []
    for i, t in enumerate(times):
        p = os.path.join(tmp, f"{i}.png")
        frame(clip, t, p)
        im = Image.open(p).convert("RGB")
        ImageDraw.Draw(im).text((6, 6), f"{t:.1f}s", fill=(255, 255, 0))
        ims.append(im)
    rows = (len(ims) + cols - 1) // cols
    W = Image.new("RGB", (270 * cols, 480 * rows))
    for i, im in enumerate(ims):
        W.paste(im, ((i % cols) * 270, (i // cols) * 480))
    W.save(out, quality=85)


clip, pre = sys.argv[1], sys.argv[2]
d = dur(clip)
sheet(clip, [0.3 + i * 0.95 for i in range(8)], pre + ".first7.jpg", 4)
if "--start-only" not in sys.argv:
    sheet(clip, [min(d - 0.3, 0.5 + i * (d - 1) / 9) for i in range(10)], pre + ".sheet.jpg", 5)
print(json.dumps({"dur": d}))
