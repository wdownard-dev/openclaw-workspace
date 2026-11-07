"""NULL - hooded esports 'streamer' silhouette: glowing eyes, equalizer mouth, no real face."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib import *

SLUG, NAME, TAGLINE = "null", "NULL", "No face. All takes."
VOICE, SPEED = "am_onyx", 0.97
LINE = "I'm Null. No face, no mercy, just takes. Don't blink, you might miss the play."
ACCENT = (150, 255, 80)
BG = ((10, 6, 24), (24, 10, 48))

GR = hexc("#9bff4a"); GRD = hexc("#4fc21a"); VI = hexc("#8b4dff"); VOID0 = hexc("#020106"); VOID1 = hexc("#0b0720")
F0 = hexc("#2c2350"); F1 = hexc("#171235"); F2 = hexc("#0c0922"); CH = hexc("#1d1a30")


def draw(mouth="closed", blink=False):
    c = Canvas()
    # --- hoodie body
    body = c.mask("poly", catmull([(70, 620), (85, 505), (150, 440), (300, 460), (450, 440), (515, 505), (530, 620)], True, 10))
    c.glow(body, VI, 8, 0.45)
    c.fill(body, Lin((0, 440), (0, 600), [(0, F0), (1, F2)]))
    c.fill(c.sub(body, c.shift(body, 8, 6)), hexc("#b58bff", 150))     # rim light
    # drawstrings + pocket + emblem
    for sx in (-1, 1):
        s = c.mask("line", catmull([(300 + sx * 52, 470), (300 + sx * 58, 520), (300 + sx * 48, 565)], False, 8), w=6)
        c.fill(s, hexc("#e9e4ff"), clip=body)
        c.fill(c.mask("ell", (300 + sx * 48 - 6, 560, 300 + sx * 48 + 6, 580)), GR, clip=body)
    hexa = [(300 + 30 * np.cos(np.radians(a)), 540 + 30 * np.sin(np.radians(a))) for a in range(0, 360, 60)]
    # --- hood
    hood = c.mask("poly", catmull([(300, 38), (400, 78), (460, 190), (480, 330), (535, 470), (410, 470), (190, 470), (65, 470), (120, 330), (140, 190), (200, 78)], True, 14))
    c.glow(hood, VI, 10, 0.55, grow=1)
    c.fill(hood, Rad((260, 150), 420, [(0, hexc("#3a2f6e")), (0.5, F1), (1, F2)], ry=460))
    c.fill(c.sub(hood, c.shift(hood, 9, 7)), hexc("#cfa8ff", 170))
    c.fill(c.sub(hood, c.shift(hood, -7, 6)), hexc("#9bff4a", 70))
    # cloth folds
    for pts in ([(150, 250), (135, 330), (110, 420)], [(450, 250), (468, 330), (490, 420)], [(215, 90), (170, 140), (158, 200)]):
        c.fill(c.mask("line", catmull(pts, False, 8), w=5), hexc("#0c0922", 140), clip=hood)
    # --- void (face opening)
    voidm = c.mask("poly", catmull([(300, 128), (385, 160), (428, 270), (410, 365), (300, 425), (190, 365), (172, 270), (215, 160)], True, 12))
    c.fill(voidm, Rad((300, 290), 200, [(0, VOID1), (0.6, VOID0), (1, VOID0)], ry=230))
    # inner shadow rim of the opening
    c.fill(c.sub(voidm, c.shift(voidm, -6, -8)), hexc("#3c2a78", 110))
    c.fill(c.blur(c.sub(c.mask("rr", (150, 100, 450, 460), r=80), c.shift(voidm, 0, 18)), 8), hexc("#000000", 0))

    # --- eyes
    ey = 270
    ang = {"closed": 14, "small": 12, "open": 8, "wide": 0}[mouth]
    for sx in (-1, 1):
        ex = 300 + sx * 52
        if blink:
            em = c.mask("line", [(ex - 30, ey + 6), (ex + 30, ey + 6 - sx * 0)], w=5)
        else:
            big = {"closed": 0, "small": 3, "open": 7, "wide": 14}[mouth]
            pts = [(ex - sx * 34, ey - 8 + ang * 0.0 - ang * 0.6), (ex + sx * 30, ey - 24 + ang * 0.0 + ang * 0.5 - big * .4), (ex + sx * 24, ey + 12 + big * .6), (ex - sx * 28, ey + 6 + big * .5)]
            # slanted slit: inner corners lower (angry) unless wide
            pts = [(ex - sx * 36, ey - 26 + ang * 1.2 - big * .3), (ex + sx * 36, ey - 26 + ang * .1 - big * .3 - 0), (ex + sx * 30, ey + 8 + big * .55), (ex - sx * 30, ey + 14 + big * .55 + ang * 0.2)]
            # sx=-1: left eye, inner corner is +x side
            if sx == -1:
                pts = [(ex - 36, ey - 26 + ang * .1 - big * .3), (ex + 36, ey - 26 + ang * 1.4 - big * .3), (ex + 30, ey + 8 + big * .55), (ex - 30, ey + 12 + big * .55)]
            else:
                pts = [(ex + 36, ey - 26 + ang * .1 - big * .3), (ex - 36, ey - 26 + ang * 1.4 - big * .3), (ex - 30, ey + 8 + big * .55), (ex + 30, ey + 12 + big * .55)]
            em = c.mask("poly", catmull(pts, True, 8))
        c.glow(em, GR, 14, 1.0, grow=2)
        c.glow(em, GR, 5, 1.0)
        c.fill(em, Lin((0, ey - 28), (0, ey + 20), [(0, hexc("#f4ffe0")), (1, GR)]))

    # --- equalizer mouth
    my = 372
    bars = 9
    hs = {"closed": [1] * 9, "small": [3, 4, 6, 8, 10, 8, 6, 4, 3], "open": [5, 9, 15, 22, 28, 22, 15, 9, 5], "wide": [8, 16, 26, 34, 44, 34, 26, 16, 8]}[mouth]
    for i, h in enumerate(hs):
        x = 300 + (i - 4) * 14
        if mouth == "closed":
            bm = c.mask("rr", (x - 4, my - 2, x + 4, my + 2), r=2)
        else:
            bm = c.mask("rr", (x - 4.5, my - h / 2 - 2, x + 4.5, my + h / 2 + 2), r=4)
        c.glow(bm, GR, 7, 0.8)
        c.fill(bm, Lin((0, my - 30), (0, my + 30), [(0, hexc("#e8ffcc")), (1, GRD)]))

    # --- headphones (over the hood)
    band = c.mask("arc", ((88, 6, 512, 520), 195, 345), w=26)
    c.glow(band, GR, 6, 0.4)
    c.fill(band, Lin((0, 20), (0, 160), [(0, hexc("#4a4a6a")), (1, CH)]))
    c.fill(c.mask("arc", ((88, 10, 512, 520), 220, 300), w=5), hexc("#ffffff", 70))
    for sx in (-1, 1):
        x0 = 300 + sx * 218
        cup = c.mask("rr", (x0 - 42, 215, x0 + 42, 365), r=32)
        c.glow(cup, GR, 8, 0.7)
        c.fill(cup, Lin((x0 - 42, 0), (x0 + 42, 0), [(0, hexc("#4a4a6a")), (1, CH)]))
        c.fill(c.mask("rr", (x0 - 42, 215, x0 + 42, 365), r=32, w=5, outline=True), GR)
        c.fill(c.mask("ell", (x0 - 24, 258, x0 + 24, 322)), CH)
        c.fill(c.mask("ell", (x0 - 24, 258, x0 + 24, 322), w=4, outline=True), VI)
        c.fill(c.mask("poly", [(x0 - 6, 276), (x0 - 6, 304), (x0 + 12, 290)]), GR)
        c.fill(c.mask("ell", (x0 - 30, 224, x0 - 14, 238)), hexc("#ffffff", 110), clip=cup)
    # mic boom
    boom = c.mask("line", catmull([(300 - 218, 365), (300 - 205, 430), (255, 432), (238, 412)], False, 8), w=6)
    c.fill(boom, hexc("#4a4a6a"))
    c.fill(c.mask("ell", (222, 396, 252, 428)), CH)
    c.fill(c.mask("ell", (228, 402, 246, 422)), GR)
    c.fade_bottom(560, 600)
    return c.out()
