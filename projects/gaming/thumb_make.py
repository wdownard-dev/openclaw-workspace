#!/usr/bin/env python3
"""wrdgamingclipz Shorts thumbnail generator, layout B (1080x1920 PNG).
Usage: python3 thumb_make.py [id ...]   (no ids = all). Plain python3 (PIL lives in ~/.local).
Frames come from out/thumbs/work/<id>/fNN.jpg (1 fps extracts of the finished Short) and the real
footage strip is cropped out of the Short's blurred-bar layout (rows in out/thumbs/work/strips.json)."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageStat
W, H = 1080, 1920
D = os.path.dirname(os.path.abspath(__file__))
WORK = f"{D}/out/thumbs/work"; OUT = f"{D}/out/thumbs"
FONT = "/usr/share/fonts/opentype/fira/FiraSans-ExtraBold.otf"
ACC = {"FORTNITE": (255, 214, 0), "ELDEN RING": (212, 175, 90), "GTA 6": (255, 92, 140)}
# id: (game, title lines, frame#, focus x 0-1, zoom>=1)
V = {
 "iSgpSI7KrJQ": ("FORTNITE", ["PIRATE SHOP", "TOKEN"], 12, .50, 1.0),
 "BEtSNncs-8Q": ("ELDEN RING", ["CARIAN REGAL", "SCEPTER"], 9, .50, 1.0),
 "v1331JIwRNs": ("ELDEN RING", ["BLOODHOUND'S", "STEP"], 8, .65, 1.0),
 "W0g79Gzpw6Y": ("ELDEN RING", ["MIMIC TEAR", "ASHES"], 6, .45, 1.0),
 "8gCNaCdIyyo": ("FORTNITE", ["MINI MIKU", "SPRITE"], 5, .45, 1.0),
 "Bk3drifXNas": ("FORTNITE", ["PIRATE TOKEN", "CHEST ROUTE"], 24, .55, 1.0),
 "8L0Ix62AJlg": ("FORTNITE", ["FROG STATUE", "2 RARE CHESTS"], 21, .60, 1.0),
 "6AnNLkEO8Cs": ("ELDEN RING", ["UCHIGATANA"], 25, .35, 1.0),
 "fM5XtZZl2ds": ("ELDEN RING", ["MOONVEIL", "KATANA"], 32, .50, 1.0),
 "O4-F81c2n6E": ("ELDEN RING", ["WONDROUS", "PHYSICK"], 15, .50, 1.0),
 "pchWVunshDQ": ("FORTNITE", ["JAM TRACK", "QUEST"], 1, .45, 1.0),
 "6m8FUczYGHU_poster": ("FORTNITE", ["WANTED POSTER", "CHEST"], 4, .45, 1.0),
 "6m8FUczYGHU_fruit": ("FORTNITE", ["DEVIL FRUIT", "QUEST"], 27, .50, 1.0),
 "Oxh7-i4mXLc": ("FORTNITE", ["LUCKY SPRITE", "CHEST ROUTE"], 25, .50, 1.0),
 "LkSzM6mbLC8": ("FORTNITE", ["SPRITE CHEST", "TRICK"], 31, .50, 1.0),
 "WZMrijY6TzI": ("ELDEN RING", ["BOLT OF", "GRANSAX"], 28, .58, 1.0),
 "S65gy4AC_kI": ("FORTNITE", ["BREAK EVERY", "CHEST"], 28, .50, 1.0),
 "AecawgyFqXg": ("ELDEN RING", ["MESSMER", "THE IMPALER"], 20, .55, 1.0),
 "tsK0MAnTik0": ("FORTNITE", ["GUM-GUM FRUIT", "EVERY MATCH"], 1, .55, 1.15),
}
F = lambda s: ImageFont.truetype(FONT, s)
def fit(d, t, maxw, start):
    s = start
    while d.textlength(t, font=F(s)) > maxw: s -= 4
    return s
def tx(d, xy, t, f, fill, sw):
    d.text(xy, t, font=f, fill=fill, anchor="mm", stroke_width=sw, stroke_fill=(0, 0, 0))
def footage(id, fr, focus, zoom):
    t, b = json.load(open(f"{WORK}/strips.json"))[id]
    im = Image.open(f"{WORK}/{id}/f{fr:02d}.jpg").convert("RGB").crop((0, t + 3, W, b - 3))
    side = int(im.height / zoom)
    x0 = int((W - side) * focus); y0 = (im.height - side) // 2
    im = im.crop((x0, y0, x0 + side, y0 + side)).resize((880, 880), Image.LANCZOS)
    lum = ImageStat.Stat(im.convert("L")).mean[0]
    if lum < 95:  # lift dark frames
        im = ImageEnhance.Brightness(im).enhance(min(1.9, 95 / max(lum, 20)))
    return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.08)).enhance(1.12)
def make(id):
    game, lines, fr, focus, zoom = V[id]; acc = ACC[game]
    bg = Image.new("RGB", (W, H)); d = ImageDraw.Draw(bg)
    for y in range(H):
        k = 0.22 + 0.30 * y / H; d.line([(0, y), (W, y)], fill=tuple(int(c * k) for c in acc))
    # game pill (top safe area: >= 220 px)
    f = F(52); lab = game; tw = d.textlength(lab, font=f)
    d.rounded_rectangle([W/2 - tw/2 - 36, 236, W/2 + tw/2 + 36, 322], 18, fill=acc)
    d.text((W/2, 279), lab, font=f, fill=(15, 15, 15), anchor="mm")
    # title
    size = min(fit(d, l, W - 110, 175) for l in lines)
    y = 340 + size * 0.5
    for l in lines:
        tx(d, (W/2, y), l, F(size), (255, 255, 255), 12); y += size * 0.95
    sy = y + 6
    tx(d, (W/2, sy), "QUICK GUIDE", F(60), acc, 8)
    py = int(sy + 52)
    pic = footage(id, fr, focus, zoom)
    d.rectangle([100 - 10, py - 10, 100 + 880 + 10, py + 880 + 10], fill=acc)
    bg.paste(pic, (100, py))
    assert py + 890 <= H - 160, (id, py)
    p = f"{OUT}/{id}.png"; bg.save(p, optimize=True); return p
if __name__ == "__main__":
    for id in (sys.argv[1:] or V):
        p = make(id); print(id, os.path.getsize(p) // 1024, "KB")
