"""WISP - friendly mint ghost with RGB gamer headphones."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib import *

SLUG, NAME, TAGLINE = "wisp", "WISP", "Cozy vibes. Chaotic commentary."
VOICE, SPEED = "af_sky", 1.0
LINE = "Boo! Don't worry, I'm the friendly kind of haunting. I'm Wisp, and I'll cheer every single win."
ACCENT = (140, 255, 215)
BG = ((6, 24, 30), (14, 44, 52))

INK = hexc("#12303a"); TEAL = hexc("#2fc9b0"); MINT = hexc("#eafff8"); PINK = hexc("#ff5cb0"); CYAN = hexc("#52e6ff")
CHAR = hexc("#2a2f3f"); CHAR2 = hexc("#171a27")


def draw(mouth="closed", blink=False):
    c = Canvas()
    # sparkles
    def star(cx, cy, r, col):
        c.fill(c.mask("poly", [(cx, cy - r), (cx + r * .22, cy - r * .22), (cx + r, cy), (cx + r * .22, cy + r * .22), (cx, cy + r), (cx - r * .22, cy + r * .22), (cx - r, cy), (cx - r * .22, cy - r * .22)]), col)
    star(70, 150, 26, hexc("#8ffcdc")); star(540, 120, 18, PINK); star(555, 330, 12, hexc("#8ffcdc")); star(45, 400, 14, PINK)

    # --- body
    cx = 300
    dome = c.mask("ell", (125, 62, 475, 400))
    trunk = c.mask("rr", (125, 232, 475, 520), r=10)
    bumps = [c.mask("ell", (125 + i * 87.5, 470, 125 + (i + 1) * 87.5, 560)) for i in range(4)]
    body = c.union(dome, trunk, *bumps)
    # cut notches between scallops (makes the wave read stronger)
    c.glow(body, hexc("#6ff5d2"), 12, 0.7, grow=3)
    # arms
    for sx in (-1, 1):
        arm = c.mask("poly", catmull([(300 + sx * 150, 360), (300 + sx * 215, 395), (300 + sx * 235, 440), (300 + sx * 200, 440), (300 + sx * 150, 415)], True, 8)) \
            if mouth != "wide" or sx == 1 else \
            c.mask("poly", catmull([(300 + sx * 150, 340), (300 + sx * 200, 290), (300 + sx * 240, 255), (300 + sx * 212, 245), (300 + sx * 160, 295)], True, 8))
        c.fill(arm, Lin((0, 360), (0, 440), [(0, hexc("#c9f9ec")), (1, hexc("#8fe8d4"))]))
    c.fill(body, Rad((250, 190), 400, [(0, MINT), (0.45, hexc("#b7f3e3")), (1, hexc("#5cc7bd"))], ry=420))
    # belly/lower translucency
    c.fill(body, Lin((0, 330), (0, 560), [(0, (255, 255, 255, 0)), (1, hexc("#2fc9b0", 110))]))
    # rim stroke
    inner = c.shift(body, 0, 0)
    c.fill(c.sub(body, c.blur(c.shift(body, 0, 0), 0)), (0, 0, 0, 0))
    edge = c.sub(body, c.mask("rr", (131, 232, 469, 700), r=0)) if False else None
    # soft highlight
    c.fill(c.blur(c.mask("ell", (165, 100, 300, 190)), 14), hexc("#ffffff", 190), clip=body)
    c.fill(c.blur(c.mask("ell", (385, 250, 450, 400)), 12), hexc("#2fc9b0", 70), clip=body)
    # scallop shading lines
    for i in range(1, 4):
        x = 125 + i * 87.5
        c.fill(c.blur(c.mask("line", [(x, 520), (x, 548)], w=6), 3), hexc("#2a9d92", 110), clip=body)

    # --- face
    for sx in (-1, 1):
        ex, ey = 300 + sx * 72, 292
        # blush
        c.fill(c.blur(c.mask("ell", (ex + sx * 20 - 36, 338, ex + sx * 20 + 36, 372)), 6), hexc("#ff7fb5", 150), clip=body)
        if blink:
            m = c.mask("arc", ((ex - 32, ey - 14, ex + 32, ey + 30), 200, 340), w=8)
            c.fill(m, INK)
        else:
            sc = {"closed": 1.0, "small": 1.0, "open": 1.05, "wide": 1.12}[mouth]
            e = c.mask("ell", (ex - 36 * sc, ey - 48 * sc, ex + 36 * sc, ey + 48 * sc))
            c.fill(e, Lin((0, ey - 50), (0, ey + 50), [(0, hexc("#0c2330")), (1, hexc("#1a5360"))]))
            c.fill(c.blur(c.mask("ell", (ex - 24, ey + 6, ex + 24, ey + 52)), 5), hexc("#52e6ff", 150), clip=e)
            c.fill(c.mask("ell", (ex - 20, ey - 36, ex - 2, ey - 14)), hexc("#ffffff"), clip=e)
            c.fill(c.mask("ell", (ex + 8, ey + 14, ex + 20, ey + 26)), hexc("#ffffff", 220), clip=e)
        # brows
        lift = {"closed": 0, "small": -2, "open": -6, "wide": -14}[mouth]
        bm = c.mask("arc", ((ex - 34, ey - 84 + lift, ex + 34, ey - 52 + lift), 205, 335), w=6)
        c.fill(bm, hexc("#2b8f8a"))
    # mouth
    my = 372
    if mouth == "closed":
        c.fill(c.mask("arc", ((278, my - 20, 322, my + 6), 20, 160), w=6), INK)
    else:
        rx, ry = {"small": (13, 10), "open": (22, 21), "wide": (31, 33)}[mouth]
        mm = c.mask("ell", (300 - rx, my - ry * 0.5, 300 + rx, my + ry * 1.3))
        c.fill(mm, INK)
        c.fill(c.mask("ell", (300 - rx * .7, my + ry * 0.55, 300 + rx * .7, my + ry * 1.7)), hexc("#ff7aa8"), clip=mm)

    # --- headphones
    band = c.mask("arc", ((108, 28, 492, 430), 192, 348), w=24)
    c.glow(band, PINK, 6, 0.5)
    c.fill(band, Lin((0, 30), (0, 130), [(0, hexc("#3a4058")), (1, CHAR2)]))
    c.fill(c.mask("arc", ((108, 32, 492, 430), 215, 300), w=5), hexc("#ffffff", 70))
    c.fill(c.mask("arc", ((122, 46, 478, 420), 200, 340), w=4), PINK)
    for sx in (-1, 1):
        x0 = 300 + sx * 196
        cup = c.mask("rr", (x0 - 38, 238, x0 + 38, 372), r=30)
        c.glow(cup, PINK, 7, 0.75)
        c.fill(cup, Lin((x0 - 38, 0), (x0 + 38, 0), [(0, hexc("#3d4560")), (1, CHAR2)]))
        c.fill(c.mask("rr", (x0 - 38, 238, x0 + 38, 372), r=30, w=5, outline=True), PINK)
        ring = c.mask("ell", (x0 - 22, 280, x0 + 22, 330))
        c.fill(ring, Lin((x0 - 22, 280), (x0 + 22, 330), [(0, PINK), (0.5, hexc("#b86cff")), (1, CYAN)]))
        c.fill(c.mask("ell", (x0 - 12, 292, x0 + 12, 318)), CHAR2)
        c.fill(c.mask("ell", (x0 - 28, 248, x0 - 14, 262)), hexc("#ffffff", 120), clip=cup)
    # mic boom (left)
    boom = c.mask("line", catmull([(262, 370), (255, 410), (232, 420), (222, 404)], False, 8), w=6)
    c.fill(boom, hexc("#3a4058"))
    mic = c.mask("ell", (210, 384, 238, 414))
    c.fill(mic, CHAR2, clip=None)
    c.fill(c.mask("ell", (215, 389, 233, 409)), PINK)
    return c.out()
