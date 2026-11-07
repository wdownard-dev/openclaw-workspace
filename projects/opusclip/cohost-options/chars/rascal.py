"""RASCAL - grumpy-smug cartoon raccoon with a crimson gaming headset."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib import *

SLUG, NAME, TAGLINE = "rascal", "RASCAL", "Zero chill. Maximum snark."
VOICE, SPEED = "bm_lewis", 1.0
LINE = "Oh great, another run to judge. Name's Rascal. I steal the best moments and roast the rest."
ACCENT = (255, 90, 80)
BG = ((22, 10, 14), (46, 18, 26))

INK = hexc("#1a1320"); FUR0 = hexc("#c9ccd8"); FUR1 = hexc("#8e93a8"); FUR2 = hexc("#575c75")
MASK = hexc("#241c2e"); WH = hexc("#f6f4fa"); WH2 = hexc("#cfd0de"); PINK = hexc("#f08aa4"); NOSE = hexc("#1b1422")
RED = hexc("#ff4b4b"); RED2 = hexc("#a81a2e"); HD0 = hexc("#2a2433"); HD1 = hexc("#15101c"); ORG = hexc("#ff9a3c")


def draw(mouth="closed", blink=False):
    c = Canvas()
    # --- hoodie bust
    body = c.mask("poly", catmull([(60, 620), (70, 520), (140, 470), (300, 495), (460, 470), (530, 520), (540, 620)], True, 10))
    c.fill(body, Lin((0, 470), (0, 600), [(0, hexc("#3a3347")), (1, HD1)]))
    c.fill(c.sub(body, c.shift(body, 6, 6)), hexc("#ffffff", 70))
    c.fill(c.mask("poly", catmull([(200, 480), (300, 540), (400, 480), (360, 470), (300, 495), (240, 470)], True, 6)), hexc("#2a2433"))
    c.fill(c.mask("line", [(120, 520), (150, 580)], w=7), ORG, clip=body)
    c.fill(c.mask("line", [(480, 520), (450, 580)], w=7), ORG, clip=body)
    for sx in (-1, 1):
        s = c.mask("line", [(300 + sx * 40, 500), (300 + sx * 46, 560)], w=6)
        c.fill(s, hexc("#efe9ff"), clip=body)
    # --- ears
    for sx in (-1, 1):
        ear = c.mask("poly", catmull([(300 + sx * 150, 175), (300 + sx * 215, 60), (300 + sx * 262, 195)], True, 10))
        c.fill(ear, Lin((0, 60), (0, 200), [(0, hexc("#2a2230")), (0.5, FUR2), (1, FUR1)]))
        c.fill(c.mask("poly", catmull([(300 + sx * 172, 170), (300 + sx * 213, 100), (300 + sx * 240, 180)], True, 8)), PINK, clip=ear)
        c.fill(c.mask("poly", catmull([(300 + sx * 150, 175), (300 + sx * 215, 60), (300 + sx * 262, 195)], True, 10), outline=True, w=5), INK)
        c.fill(c.mask("poly", catmull([(300 + sx * 205, 72), (300 + sx * 215, 60), (300 + sx * 232, 100)], True, 4)), WH, clip=ear)
    # --- head
    head_pts = [(300, 100), (410, 125), (500, 215), (530, 320), (480, 410), (390, 460), (300, 472), (210, 460), (120, 410), (70, 320), (100, 215), (190, 125)]
    head = c.mask("poly", catmull(head_pts, True, 12))
    # cheek fur tufts
    for sx in (-1, 1):
        t = c.mask("poly", [(300 + sx * 225, 330), (300 + sx * 290, 372), (300 + sx * 240, 392), (300 + sx * 275, 425), (300 + sx * 200, 420)])
        c.fill(t, FUR1)
    c.fill(head, Rad((290, 190), 380, [(0, FUR0), (0.5, FUR1), (1, FUR2)], ry=340))
    # forehead stripe
    c.fill(c.mask("poly", catmull([(300, 100), (330, 130), (318, 250), (300, 300), (282, 250), (270, 130)], True, 8)), MASK, clip=head)
    c.fill(c.mask("poly", catmull([(300, 150), (312, 170), (308, 255), (300, 280), (292, 255), (288, 170)], True, 8)), FUR2, clip=head, alpha=0.6)
    # bandit mask (butterfly)
    mk = c.mask("poly", catmull([(100, 270), (160, 232), (250, 238), (300, 262), (350, 238), (440, 232), (500, 270), (490, 330), (410, 358), (340, 330), (300, 318), (260, 330), (190, 358), (110, 330)], True, 8))
    c.fill(mk, Lin((0, 232), (0, 358), [(0, hexc("#3a2f48")), (1, MASK)]), clip=head)
    # muzzle
    mz = c.mask("poly", catmull([(300, 305), (370, 330), (420, 390), (385, 450), (300, 472), (215, 450), (180, 390), (230, 330)], True, 10))
    c.fill(mz, Rad((300, 360), 150, [(0, WH), (1, WH2)]), clip=head)
    # shading / highlight
    c.fill(c.blur(c.shift(head, 0, 24), 12), hexc("#2a2540", 120), clip=c.sub(head, c.shift(head, 0, -16)))
    c.fill(c.blur(c.mask("ell", (170, 118, 340, 180)), 12), hexc("#ffffff", 90), clip=head)
    c.fill(c.mask("poly", catmull(head_pts, True, 12), outline=True, w=5), INK)

    # --- eyes (half-lidded)
    for sx in (-1, 1):
        ex, ey = 300 + sx * 85, 292
        if blink:
            c.fill(c.mask("arc", ((ex - 36, ey - 28, ex + 36, ey + 22), 25, 155), w=8), WH)
        else:
            op = {"closed": 0.55, "small": 0.6, "open": 0.78, "wide": 1.0}[mouth]
            sc = {"closed": 1.0, "small": 1.0, "open": 1.05, "wide": 1.15}[mouth]
            e = c.mask("ell", (ex - 36 * sc, ey - 36 * sc, ex + 36 * sc, ey + 36 * sc))
            c.fill(e, WH)
            c.fill(c.blur(c.mask("ell", (ex - 28, ey - 10, ex + 28, ey + 44)), 6), hexc("#8e93a8", 90), clip=e)
            px = ex - sx * 4
            c.fill(c.mask("ell", (px - 17, ey - 16, px + 17, ey + 22)), hexc("#3b2a1b"), clip=e)
            c.fill(c.mask("ell", (px - 11, ey - 10, px + 11, ey + 16)), INK, clip=e)
            c.fill(c.mask("ell", (px - 8, ey - 14, px + 2, ey - 4)), WH, clip=e)
            # lid cuts the top part of the eye (grumpy/smug)
            lidline = ey - 36 * sc + 72 * sc * (1 - op)
            lid = c.mask("poly", [(ex - 50, ey - 60), (ex + 50, ey - 60), (ex + sx * -50 + 0, lidline + sx * 10 + 6), (ex + sx * 50, lidline - sx * 0 - 2)])
            lid = c.mask("poly", [(ex - 50, ey - 60), (ex + 50, ey - 60), (ex + 50, lidline + (6 if sx == 1 else -6) * -1 + 0), (ex - 50, lidline + (6 if sx == 1 else -6))]) if False else \
                c.mask("poly", [(ex - 50, ey - 60), (ex + 50, ey - 60), (ex + 50, lidline + (-sx) * 0 + (10 if sx == -1 else 0) * 0 + (0 if sx == 1 else 0)), (ex - 50, lidline)]) 
            # slope: inner side lower -> angrier
            inner_drop = 12
            ix = ex - sx * 40; ox = ex + sx * 40
            lid = c.mask("poly", [(ix - sx * 10, ey - 60), (ox + sx * 10, ey - 60), (ox, lidline - 2), (ix, lidline + inner_drop)])
            c.fill(lid, Lin((0, ey - 40), (0, ey + 10), [(0, FUR1), (1, FUR2)]), clip=None)
            c.fill(c.mask("poly", [(ix, lidline + inner_drop), (ox, lidline - 2)], ) if False else c.mask("line", [(ix, lidline + inner_drop), (ox, lidline - 2)], w=6), INK, clip=e)
        # brows (thick, angled)
        lift = {"closed": 0, "small": -1, "open": -5, "wide": -14}[mouth]
        ix = ex - sx * 44; ox = ex + sx * 40
        bm = c.mask("line", [(ix, 238 + lift + 14), (ox, 226 + lift)], w=13)
        c.fill(bm, hexc("#12101a"))
    # --- nose
    nz = c.mask("poly", catmull([(270, 340), (330, 340), (345, 360), (300, 388), (255, 360)], True, 8))
    c.fill(nz, Lin((0, 340), (0, 388), [(0, hexc("#3a2c4a")), (1, NOSE)]))
    c.fill(c.mask("ell", (278, 346, 308, 358)), hexc("#ffffff", 170), clip=nz)
    # whiskers dots
    for sx in (-1, 1):
        for i, (dx, dy) in enumerate([(55, 395), (75, 410), (45, 418)]):
            c.fill(c.mask("ell", (300 + sx * dx - 2.5, dy - 2.5, 300 + sx * dx + 2.5, dy + 2.5)), hexc("#5a5470"))
    # --- mouth
    my = 418
    c.fill(c.mask("line", [(300, 388), (300, my)], w=4), INK)
    if mouth == "closed":
        m = c.mask("line", catmull([(250, my + 12), (275, my + 6), (300, my + 4), (330, my + 4), (360, my - 10)], False, 8), w=6)
        c.fill(m, INK)
    else:
        rx, ry = {"small": (24, 12), "open": (36, 26), "wide": (46, 40)}[mouth]
        mm = c.mask("poly", catmull([(300 - rx, my), (300, my + 8), (300 + rx, my), (300 + rx * .75, my + ry), (300, my + ry * 1.35), (300 - rx * .75, my + ry)], True, 10))
        c.fill(mm, hexc("#2a0f1c"))
        c.fill(c.mask("ell", (300 - rx * .6, my + ry * .75, 300 + rx * .6, my + ry * 1.7)), hexc("#ff6f8f"), clip=mm)
        if mouth in ("open", "wide"):
            c.fill(c.mask("rr", (300 - rx * .5, my + 2, 300 + rx * .5, my + 14), r=3), WH, clip=mm)
        c.fill(c.mask("poly", catmull([(300 - rx, my), (300, my + 8), (300 + rx, my), (300 + rx * .75, my + ry), (300, my + ry * 1.35), (300 - rx * .75, my + ry)], True, 10), outline=True, w=4), INK)
    # --- headset
    band = c.mask("arc", ((76, 52, 524, 470), 197, 343), w=26)
    c.fill(band, Lin((0, 52), (0, 200), [(0, hexc("#46405a")), (1, HD1)]))
    c.fill(c.mask("arc", ((76, 56, 524, 470), 225, 300), w=5), hexc("#ffffff", 70))
    c.fill(c.mask("arc", ((90, 66, 510, 460), 205, 335), w=4), RED)
    for sx in (-1, 1):
        x0 = 300 + sx * 224
        cup = c.mask("rr", (x0 - 46, 248, x0 + 46, 400), r=34)
        c.glow(cup, RED, 8, 0.55)
        c.fill(cup, Lin((x0 - 46, 0), (x0 + 46, 0), [(0, hexc("#4c455e")), (1, HD1)]))
        c.fill(c.mask("rr", (x0 - 46, 248, x0 + 46, 400), r=34, w=6, outline=True), RED)
        c.fill(c.mask("ell", (x0 - 24, 296, x0 + 24, 352)), HD1)
        c.fill(c.mask("poly", [(x0 - 12, 340), (x0, 305), (x0 + 12, 340), (x0 + 4, 340), (x0, 322), (x0 - 4, 340)]), RED)
        c.fill(c.mask("ell", (x0 - 34, 258, x0 - 16, 272)), hexc("#ffffff", 100), clip=cup)
    boom = c.mask("line", catmull([(300 - 224, 400), (300 - 212, 468), (195, 470), (175, 432)], False, 8), w=7)
    c.fill(boom, hexc("#46405a"))
    c.fill(c.mask("ell", (155, 412, 195, 452)), HD1)
    c.fill(c.mask("ell", (160, 417, 190, 447)), RED)
    c.fill(c.mask("ell", (165, 422, 178, 434)), hexc("#ffb0b0"))
    c.fade_bottom(565, 600)
    return c.out()
