"""ORB-7 - glossy 3D-look floating droid with an LED-matrix face."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib import *
from PIL import Image

SLUG, NAME, TAGLINE = "orb", "ORB-7", "Beep boop. Actually correct."
VOICE, SPEED = "af_kore", 1.0
LINE = "Greetings, human. I am Orb Seven. I calculate a ninety nine percent chance this clip is awesome."
ACCENT = (70, 190, 255)
BG = ((6, 12, 30), (10, 28, 60))

BLU = hexc("#3ec1ff"); BLU2 = hexc("#1b7cff"); CORE = hexc("#e6fbff"); GL0 = hexc("#050a1e"); GL1 = hexc("#14275a")


def led_grid(c, m, step=5.0):
    """Darken thin grid lines over a mask -> LED matrix look."""
    S = c.S
    g = Image.new("L", (c.N, c.N), 0)
    px = g.load()
    stp = int(step * S)
    lw = max(1, int(S * 1.3))
    arr = np.zeros((c.N, c.N), np.uint8)
    for k in range(0, c.N, stp):
        arr[k:k + lw, :] = 255
        arr[:, k:k + lw] = 255
    c.fill(Image.fromarray(arr).convert("L"), hexc("#06143a", 120), clip=m)


def draw(mouth="closed", blink=False):
    c = Canvas()
    cx, cy, R = 300, 282, 205
    # floor glow
    c.glow(c.mask("ell", (160, 538, 440, 560)), BLU2, 14, 0.9)
    c.fill(c.blur(c.mask("ell", (190, 540, 410, 556)), 5), hexc("#0a1030", 190))
    # antenna
    c.fill(c.mask("line", [(300, 80), (300, 36)], w=8), hexc("#8ea3c9"))
    tip = c.mask("ell", (288, 14, 312, 38))
    c.glow(tip, BLU, 8, 1.0)
    c.fill(tip, CORE)
    # back half of ring
    ring_box = (34, 318, 566, 458)
    back = c.mask("arc", (ring_box, 180, 360), w=16)
    c.glow(back, BLU2, 6, 0.6)
    c.fill(back, hexc("#2a4a96"))
    # --- shell sphere
    sph = c.mask("ell", (cx - R, cy - R, cx + R, cy + R))
    c.glow(sph, BLU2, 14, 0.55, grow=1)
    c.fill(sph, Rad((235, 190), 330, [(0, hexc("#ffffff")), (0.28, hexc("#dfe9fb")), (0.62, hexc("#8ea6d6")), (1, hexc("#34457f"))], ry=330))
    # rim light bottom (cyan bounce)
    c.fill(c.blur(c.sub(sph, c.shift(sph, 0, -16)), 5), hexc("#3ec1ff", 190), clip=sph)
    # side seams
    c.fill(c.mask("arc", ((cx - R + 6, cy - R + 6, cx + R - 6, cy + R - 6), 150, 210), w=5), hexc("#7186b8", 180))
    c.fill(c.mask("arc", ((cx - R + 6, cy - R + 6, cx + R - 6, cy + R - 6), 330, 390), w=5), hexc("#5568a0", 180))
    # --- side pods
    for sx in (-1, 1):
        x0 = cx + sx * (R - 4)
        pod = c.mask("rr", (x0 - 24, cy - 62, x0 + 24, cy + 40), r=22)
        c.glow(pod, BLU, 7, 0.8)
        c.fill(pod, Lin((x0 - 24, 0), (x0 + 24, 0), [(0, hexc("#6d83b8")), (0.5, hexc("#2a3a72")), (1, hexc("#141f4a"))]))
        c.fill(c.mask("rr", (x0 - 24, cy - 62, x0 + 24, cy + 40), r=22, w=5, outline=True), BLU)
        c.fill(c.mask("ell", (x0 - 9, cy - 28, x0 + 9, cy + 6)), CORE)
    # --- face plate
    fp = c.mask("ell", (cx - 168, cy - 120, cx + 168, cy + 118))
    c.fill(c.mask("ell", (cx - 174, cy - 126, cx + 174, cy + 124)), hexc("#b7c6e8"))     # bezel
    c.fill(fp, Lin((0, cy - 120), (0, cy + 118), [(0, GL1), (0.5, GL0), (1, hexc("#0a1740"))]))
    c.glow(fp, BLU, 3, 0.0)
    # glass reflection
    c.fill(c.mask("poly", catmull([(cx - 140, cy - 62), (cx - 70, cy - 104), (cx + 40, cy - 112), (cx - 10, cy - 78), (cx - 90, cy - 40)], True, 8)), hexc("#ffffff", 36), clip=fp)

    # --- LED face
    col = CORE
    for sx in (-1, 1):
        ex, ey = cx + sx * 80, cy - 14
        if blink:
            em = c.mask("rr", (ex - 34, ey + 14, ex + 34, ey + 24), r=5)
        else:
            h = {"closed": 66, "small": 70, "open": 78, "wide": 92}[mouth]
            w = {"closed": 54, "small": 56, "open": 60, "wide": 66}[mouth]
            em = c.mask("rr", (ex - w / 2, ey - h / 2, ex + w / 2, ey + h / 2), r=w * 0.42)
        c.glow(em, BLU, 14, 1.0, grow=2)
        c.glow(em, BLU, 5, 1.0)
        c.fill(em, Lin((0, ey - 40), (0, ey + 40), [(0, CORE), (1, BLU)]))
        led_grid(c, em)
        # brows
        lift = {"closed": 0, "small": -3, "open": -8, "wide": -18}[mouth]
        br = c.mask("line", [(ex - sx * 34, 160 + lift + 8 * (1 if mouth == "closed" else 0)), (ex + sx * 30, 150 + lift)], w=7)
        c.glow(br, BLU, 6, 0.9)
        c.fill(br, hexc("#9ae2ff"))
    my = cy + 58
    if mouth == "closed":
        mm = c.mask("arc", ((cx - 46, my - 34, cx + 46, my + 10), 25, 155), w=8)
    elif mouth == "small":
        mm = c.mask("rr", (cx - 26, my - 6, cx + 26, my + 10), r=8)
    elif mouth == "open":
        mm = c.mask("rr", (cx - 36, my - 8, cx + 36, my + 30), r=17)
    else:
        mm = c.mask("rr", (cx - 44, my - 10, cx + 44, my + 44), r=24)
    c.glow(mm, BLU, 10, 1.0, grow=1)
    c.fill(mm, Lin((0, my - 10), (0, my + 40), [(0, CORE), (1, BLU)]))
    led_grid(c, mm)

    # sphere gloss (specular)
    c.fill(c.blur(c.mask("ell", (140, 92, 290, 148)), 9), hexc("#ffffff", 170), clip=sph)
    c.fill(c.mask("ell", (176, 100, 232, 116)), hexc("#ffffff", 210), clip=sph)
    # --- front half of ring
    front = c.mask("arc", (ring_box, 0, 180), w=16)
    c.glow(front, BLU, 7, 0.9)
    c.fill(front, Lin((0, 396), (0, 458), [(0, hexc("#9ad8ff")), (0.5, BLU), (1, BLU2)]))
    c.fill(c.mask("arc", ((44, 324, 556, 454), 20, 160), w=3), hexc("#ffffff", 150))
    # ring end-pods
    for sx in (0, 1):
        x = 40 + sx * 520
        p = c.mask("ell", (x - 14, 374, x + 14, 402))
        c.glow(p, BLU, 6, 0.9)
        c.fill(p, hexc("#e2f6ff"))
    return c.out()
