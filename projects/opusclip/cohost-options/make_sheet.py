#!/usr/bin/env python
"""Contact sheet (3x2) + montage concat. Usage: tts-venv/bin/python make_sheet.py"""
import sys, os, importlib, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "chars"))
FD = "/usr/share/fonts/opentype/fira/"
ORDER = ["volt", "quarter", "wisp", "null", "rascal", "orb"]
CW, CH, PAD = 620, 800, 20
sheet = Image.new("RGB", (3 * CW + 4 * PAD, 2 * CH + 3 * PAD), (10, 8, 16))
for i, s in enumerate(ORDER):
    m = importlib.import_module(s)
    cell = np.zeros((CH, CW, 3), np.float32)
    top, bot = np.array(m.BG[0], np.float32), np.array(m.BG[1], np.float32)
    ys = np.linspace(0, 1, CH, dtype=np.float32)[:, None, None]
    cell[:] = top * (1 - ys) + bot * ys
    yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
    g = np.clip(1 - np.sqrt(((xx - CW / 2) / 330) ** 2 + ((yy - 300) / 330) ** 2), 0, 1) ** 2 * 0.35
    cell = cell * (1 - g[..., None]) + np.array(m.ACCENT, np.float32) * g[..., None]
    im = Image.fromarray(cell.astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    spr = Image.open(os.path.join(HERE, s, f"{s}_small.png")).resize((580, 580), Image.NEAREST if s == "quarter" else Image.LANCZOS)
    im.alpha_composite(spr, (20, 40))
    d.text((CW / 2, 662), m.NAME, font=ImageFont.truetype(FD + "FiraSansCondensed-ExtraBold.otf", 84), fill=(255, 255, 255, 255), anchor="mm", stroke_width=2, stroke_fill=m.ACCENT + (255,))
    d.text((CW / 2, 726), m.TAGLINE, font=ImageFont.truetype(FD + "FiraSans-Medium.otf", 30), fill=(235, 235, 245, 255), anchor="mm")
    d.text((CW / 2, 764), f"voice: {m.VOICE}", font=ImageFont.truetype(FD + "FiraSans-Regular.otf", 22), fill=m.ACCENT + (255,), anchor="mm")
    d.rounded_rectangle([0, 0, CW - 1, CH - 1], 24, outline=m.ACCENT + (120,), width=3)
    mask = Image.new("L", (CW, CH), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, CW - 1, CH - 1], 24, fill=255)
    r, c = divmod(i, 3)
    sheet.paste(im.convert("RGB"), (PAD + c * (CW + PAD), PAD + r * (CH + PAD)), mask)
sheet.save(os.path.join(HERE, "contact-sheet.png"), optimize=True)
print("sheet", os.path.getsize(os.path.join(HERE, "contact-sheet.png")) // 1024, "KB")

lst = os.path.join(HERE, "clips", "list.txt")
open(lst, "w").write("".join(f"file '{os.path.join(HERE, 'clips', s + '.mp4')}'\n" for s in ORDER))
subprocess.run(["/home/williamdownard/openclaw-sites/bin/ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                "-c", "copy", "-movflags", "+faststart", os.path.join(HERE, "montage.mp4")], check=True)
print("montage", os.path.getsize(os.path.join(HERE, "montage.mp4")) // 1024, "KB")
