"""VOLT - neon cyber-fox with a glowing visor."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib import *

SLUG, NAME, TAGLINE = "volt", "VOLT", "Fast takes. Faster foxes."
VOICE, SPEED = "af_nova", 1.08
LINE = "Hey, I'm Volt, your neon fox co-host. I spot clutch plays, call the fails, and never miss a highlight."
ACCENT = (40, 230, 255)
BG = ((16, 6, 36), (40, 10, 60))

CY = hexc("#35e6ff"); CYD = hexc("#0aa8d8"); NAVY = hexc("#120a2c"); MAG = hexc("#ff2bd6")
OR1 = hexc("#ffa23c"); OR2 = hexc("#ff6a1f"); OR3 = hexc("#c9360f"); WH = hexc("#fff6ee"); WH2 = hexc("#ffd9c2")


def draw(mouth="closed", blink=False):
    c = Canvas()
    ramp = {"closed": 0, "small": 0, "open": -4, "wide": -10}[mouth]

    # --- bust / jacket
    body = c.mask("poly", catmull([(40, 620), (60, 520), (150, 462), (300, 490), (450, 462), (540, 520), (560, 620)], True, 10))
    c.glow(body, CY, 6, 0.45)
    c.fill(body, Lin((0, 470), (0, 600), [(0, hexc("#2a1760")), (1, hexc("#0e0726"))]))
    c.fill(c.mask("poly", [(210, 470), (300, 520), (390, 470), (340, 460), (300, 480), (260, 460)]), CYD)
    c.fill(c.mask("poly", [(230, 470), (300, 508), (370, 470), (345, 462), (300, 490), (255, 462)]), CY)
    for sx in (-1, 1):
        x = 300 + sx * 150
        c.fill(c.mask("line", [(x - sx * 60, 520), (x, 505), (x + sx * 70, 545)], w=5), CY, clip=body)
        c.fill(c.mask("line", [(x - sx * 40, 560), (x + sx * 20, 548), (x + sx * 70, 580)], w=4), MAG, clip=body)
    # --- ears
    for sx in (-1, 1):
        ox = 300 + sx * 1
        pts = [(300 + sx * 190, 40), (300 + sx * 215, 230), (300 + sx * 70, 195)]
        ear = c.mask("poly", catmull(pts, True, 8))
        c.glow(ear, CY, 5, 0.5)
        c.fill(ear, Lin((300 + sx * 190, 40), (300 + sx * 150, 230), [(0, hexc("#2a0f2e")), (0.35, OR3), (1, OR2)]))
        inner = c.mask("poly", catmull([(300 + sx * 182, 95), (300 + sx * 192, 205), (300 + sx * 112, 190)], True, 8))
        c.fill(inner, Lin((300 + sx * 182, 95), (300 + sx * 150, 205), [(0, hexc("#ff2bd6")), (1, hexc("#6a0e63"))]), clip=ear)
        c.fill(c.mask("poly", catmull([(300 + sx * 182, 95), (300 + sx * 192, 205), (300 + sx * 112, 190)], True, 8), outline=True, w=4), CY, clip=ear)
    # --- head
    head_pts = [(120, 215), (200, 150), (300, 135), (400, 150), (480, 215), (510, 330), (420, 425), (300, 485), (180, 425), (90, 330)]
    head = c.mask("poly", catmull(head_pts, True, 12))
    c.glow(head, CY, 9, 0.55, grow=2)
    # cheek tuft spikes (outside head)
    for sx in (-1, 1):
        for (a, b, d_) in [((300 + sx * 205, 330), (300 + sx * 248, 372), (300 + sx * 195, 385))]:
            t = c.mask("poly", [a, b, d_])
            c.fill(t, WH2)
    c.fill(head, Rad((300, 200), 330, [(0, OR1), (0.55, OR2), (1, OR3)], ry=300))
    # white muzzle / cheeks
    white = c.mask("poly", catmull([(88, 330), (170, 352), (240, 330), (300, 352), (360, 330), (430, 352), (512, 330), (430, 430), (300, 490), (170, 430)], True, 6))
    c.fill(white, Lin((0, 330), (0, 490), [(0, WH), (1, WH2)]), clip=head)
    # forehead marks
    for sx in (-1, 1):
        c.fill(c.mask("poly", [(300 + sx * 20, 145), (300 + sx * 52, 150), (300 + sx * 30, 205)]), hexc("#7a1d3c"), clip=head)
        c.fill(c.mask("line", [(300 + sx * 70, 160), (300 + sx * 110, 170), (300 + sx * 140, 190)], w=3), CY, clip=head)
    # soft shading + highlight
    c.fill(c.blur(c.shift(head, 0, 26), 10), hexc("#8a1f0c", 110), clip=c.sub(head, c.shift(head, 0, -14)))
    c.fill(c.blur(c.mask("ell", (170, 120, 340, 190)), 12), hexc("#ffffff", 70), clip=head)

    # --- brows (LED)
    lift = {"closed": 0, "small": 0, "open": -5, "wide": -14}[mouth]
    for sx in (-1, 1):
        bm = c.mask("line", [(300 + sx * 85, 222 + lift), (300 + sx * 140, 208 + lift - 6), (300 + sx * 185, 226 + lift)], w=8)
        c.glow(bm, CY, 5, 0.9)
        c.fill(bm, hexc("#bff6ff"))

    # --- visor
    vis = c.mask("rr", (105, 238, 495, 338), r=48)
    pods = [c.mask("ell", (90 + s * 395, 262, 120 + s * 395, 312)) for s in (0, 1)]
    for p in pods:
        c.glow(p, CY, 4, 0.8)
        c.fill(p, NAVY)
        c.fill(p, CY, clip=c.sub(p, c.shift(p, 3, 3)))
    c.glow(vis, CY, 8, 0.85, grow=1)
    c.fill(vis, Lin((0, 238), (0, 338), [(0, hexc("#3b1a78")), (1, hexc("#0e0630"))]))
    c.fill(c.mask("rr", (105, 238, 495, 338), r=48, w=5, outline=True), CY)
    # eyes inside visor
    for sx in (-1, 1):
        ex = 300 + sx * 100
        if blink:
            em = c.mask("line", [(ex - 38, 290), (ex + 38, 290)], w=7)
            c.glow(em, CY, 4, 0.9)
            c.fill(em, hexc("#d8fbff"))
        else:
            big = 1.0 + {"closed": 0, "small": 0.04, "open": 0.1, "wide": 0.2}[mouth]
            ew, eh = 40 * big, 36 * big
            # slanted fierce eye
            pts = [(ex - sx * ew, 292 - eh * 0.2 * sx * -1 * 0 - eh * 0.55), (ex + sx * ew, 292 - eh * 0.95), (ex + sx * ew, 292 + eh * 0.55), (ex - sx * ew, 292 + eh * 0.7)]
            em = c.mask("poly", catmull(pts, True, 8))
            c.glow(em, CY, 7, 1.0)
            c.fill(em, Lin((0, 262), (0, 320), [(0, hexc("#e8feff")), (1, CY)]))
            pu = c.mask("ell", (ex - 13, 281, ex + 13, 307))
            c.fill(pu, NAVY, clip=em)
            c.fill(c.mask("ell", (ex - 9, 283, ex - 1, 292)), WH, clip=em)
    # visor gloss
    gl = c.mask("poly", [(130, 242), (230, 242), (190, 292), (112, 292)])
    c.fill(gl, hexc("#ffffff", 46), clip=vis)
    c.fill(c.mask("line", [(250, 245), (275, 245)], w=3), hexc("#ffffff", 120), clip=vis)

    # --- nose + mouth
    nose = c.mask("poly", catmull([(272, 372), (328, 372), (300, 402)], True, 8))
    c.fill(nose, Lin((0, 372), (0, 402), [(0, hexc("#3d2a55")), (1, NAVY)]))
    c.fill(c.mask("ell", (285, 375, 305, 383)), hexc("#ffffff", 150), clip=nose)
    DK = hexc("#22071f")
    my = 440
    if mouth == "closed":
        m = c.mask("line", catmull([(255, my - 4), (278, my + 8), (300, my - 2), (322, my + 8), (345, my - 4)], False, 8), w=5)
        c.fill(m, DK)
        c.fill(c.mask("line", [(300, 402), (300, my - 2)], w=4), DK)
    else:
        c.fill(c.mask("line", [(300, 402), (300, my - 6)], w=4), DK)
        dims = {"small": (26, 12), "open": (38, 24), "wide": (48, 38)}[mouth]
        rx, ry = dims
        top = my - 6
        mm = c.mask("poly", catmull([(300 - rx, top), (300, top + 4), (300 + rx, top), (300 + rx * 0.7, top + ry * 1.2), (300, top + ry * 1.7), (300 - rx * 0.7, top + ry * 1.2)], True, 10))
        c.fill(mm, DK)
        c.fill(c.mask("ell", (300 - rx * 0.7, top + ry * 0.9, 300 + rx * 0.7, top + ry * 2.1)), hexc("#ff4f8b"), clip=mm)
        if mouth in ("open", "wide"):
            for sx in (-1, 1):
                c.fill(c.mask("poly", [(300 + sx * (rx * 0.82), top + 2), (300 + sx * (rx * 0.55), top + 2), (300 + sx * (rx * 0.7), top + 14)]), WH, clip=mm)
        c.fill(c.mask("poly", catmull([(300 - rx, top), (300, top + 4), (300 + rx, top), (300 + rx * 0.7, top + ry * 1.2), (300, top + ry * 1.7), (300 - rx * 0.7, top + ry * 1.2)], True, 10), outline=True, w=3), DK)
    c.fade_bottom(560, 600)
    return c.out()
