#!/usr/bin/env python
"""contact-sheet-null-v2.png: variants A and B side by side, 4 expressions each (reads frames_A/ frames_B/)."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/opentype/fira/"
f = lambda n, s: ImageFont.truetype(FD + n, s)
SHOW = [("smug", "closed", "NEUTRAL SMUG"), ("raised", "small", "RAISED BROW"), ("squint", "closed", "UNIMPRESSED"), ("laugh", "wide", "SMIRK-LAUGH")]
CELL, PAD, TOP = 400, 18, 190
W = 2 * (CELL * 2 + PAD * 3) + 90
H = TOP + CELL * 2 + 80 + 130
bg = Image.new("RGB", (W, H), (14, 9, 32))
d = ImageDraw.Draw(bg)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(14 + 12 * t), int(9 + 4 * t), int(32 + 30 * t)))
d.text((W // 2, 62), "NULL//SMIRK  -  v2 co-host options", font=f("FiraSansCondensed-ExtraBold.otf", 78), fill=(255, 255, 255), anchor="mm")
d.text((W // 2, 124), "No face. All takes. Mild contempt.   (code-drawn, transparent PNGs, supersampled)", font=f("FiraSans-Medium.otf", 34), fill=(200, 190, 230), anchor="mm")
titles = {"A": ("A  SUBTLE", "attitude only via brows, lids and a lopsided smirk"),
          "B": ("B  RACCOON-HOODED", "raccoon ears, neon bandit band, tiny smirk")}
colw = CELL * 2 + PAD * 3
for ci, v in enumerate("AB"):
    x0 = 45 + ci * (colw + 0)
    d.rounded_rectangle([x0, TOP - 36, x0 + colw - PAD, TOP + CELL * 2 + 16], 26, fill=(20, 12, 46), outline=(139, 77, 255), width=3)
    d.text((x0 + 24, TOP - 8 - 4), titles[v][0], font=f("FiraSansCondensed-ExtraBold.otf", 46), fill=(155, 255, 74), anchor="lm")
    for i, (ex, mo, label) in enumerate(SHOW):
        im = Image.open(os.path.join(HERE, f"frames_{v}", f"nullv2{v}_{ex}_{mo}.png")).resize((CELL, CELL), Image.LANCZOS)
        cx = x0 + PAD + (i % 2) * (CELL + PAD)
        cy = TOP + 30 + (i // 2) * (CELL - 8)
        glowbg = Image.new("RGBA", (CELL, CELL), (24, 14, 52, 255))
        glowbg.alpha_composite(im)
        bg.paste(glowbg.convert("RGB"), (cx, cy))
        d.rounded_rectangle([cx, cy, cx + CELL, cy + CELL], 12, outline=(70, 50, 130), width=2)
        d.text((cx + 12, cy + 14), label, font=f("FiraSansCondensed-Bold.otf", 30), fill=(235, 235, 250), anchor="lm")
    d.text((x0 + 24, TOP + CELL * 2 + 56), titles[v][1], font=f("FiraSans-Medium.otf", 28), fill=(200, 190, 230), anchor="lm")
d.text((W // 2, H - 40), "Also in each set: eye-roll (3 frames), side-glance L/R, blink, 4 mouth states (closed/small/open/wide)", font=f("FiraSans-Medium.otf", 30), fill=(170, 160, 210), anchor="mm")
out = os.path.join(HERE, "contact-sheet-null-v2.png")
bg.save(out, optimize=True)
print(out, os.path.getsize(out) // 1024, "KB", bg.size)
