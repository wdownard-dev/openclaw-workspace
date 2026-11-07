"""NULL v2 ("NULL//SMIRK") - hooded faceless streamer with attitude.

Two variants:  A = 'subtle' (personality only through glowing brows/eyes/smirk-mouth)
               B = 'raccoon' (adds raccoon ears on the hood, neon bandit-mask band, tiny smirk)
Layered: base(variant) = hood/body/headphones (no face), face parts are separate transparent layers:
   eyes_layer(variant, pose), brows_layer(variant, pose), mouth_layer(variant, mouth, pose), mask_layer(variant)
compose(variant, mouth, pose) -> 600x600 RGBA.  Everything drawn at 3x and downscaled (lib.Canvas).
Poses are plain dicts (see EXPR); lerp_pose() blends them so the video can ease between expressions.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(HERE, "..", "chars"))
from lib import *
from PIL import Image

NAME, TAGLINE = "NULL//SMIRK", "No face. All takes. Mild contempt."
ACCENT = (150, 255, 80)
BG = ((10, 6, 24), (24, 10, 48))
GR = hexc("#9bff4a"); GRD = hexc("#4fc21a"); VI = hexc("#8b4dff"); VOID0 = hexc("#020106"); VOID1 = hexc("#0b0720")
F0 = hexc("#2c2350"); F1 = hexc("#171235"); F2 = hexc("#0c0922"); CH = hexc("#1d1a30")
RES = 600          # output size of every layer (set before first compose; layers are downscaled from a 3x canvas)


def _out(c):
    c.size = RES
    return c.out()


EY = 272           # eye line
EX = 54            # eye offset from centre

# ------------------------------------------------------------------ poses
# brow = (y, angle, arch): y = centre height, angle>0 -> inner end lower (stern), arch>0 -> bowed up
BASE = dict(eL=0.55, eR=0.60, slant=3.0, squint=0.0, gx=0.10, gy=0.18, laugh=0.0, blink=0.0,
            bLy=224, bLa=4, bLh=2, bRy=216, bRa=0, bRh=5, smirk=0.65, mscale=1.0, tilt=0.0)


def P(**kw):
    d = dict(BASE); d.update(kw); return d


EXPR = {
    "smug":    P(),
    "laugh":   P(eL=0.4, eR=0.4, laugh=1.0, bLy=214, bLa=-3, bLh=5, bRy=208, bRa=-3, bRh=6, smirk=1.0, mscale=1.1, tilt=-2.0),
    "squint":  P(eL=0.50, eR=0.50, squint=0.26, slant=7, gx=0.0, gy=0.2, bLy=233, bLa=9, bLh=0, bRy=233, bRa=9, bRh=0, smirk=-0.15, mscale=0.9),
    "raised":  P(eL=0.42, eR=0.92, slant=4, bLy=234, bLa=7, bLh=0, bRy=186, bRa=-3, bRh=11, smirk=0.35, tilt=2.5),
    "roll":    P(eL=0.86, eR=0.86, slant=0, bLy=212, bLa=-2, bLh=5, bRy=204, bRa=-2, bRh=6, smirk=0.1),
    "glance":  P(eL=0.62, eR=0.66, slant=2, gx=1.0, gy=0.05, bLy=224, bLa=3, bLh=2, bRy=210, bRa=0, bRh=7, smirk=0.55, tilt=-1.5),
    "glanceL": P(eL=0.62, eR=0.66, slant=2, gx=-1.0, gy=0.05, bLy=218, bLa=0, bLh=6, bRy=222, bRa=3, bRh=2, smirk=0.5, tilt=1.5),
    "blink":   P(blink=1.0),
}


def lerp_pose(a, b, t):
    return {k: a[k] + (b[k] - a[k]) * t for k in a}


def roll_pose(t):
    """Eye-roll: look right -> up -> left -> settle. t in 0..1. Returns pose."""
    import math
    base = EXPR["roll"]
    if t < 0.15:
        g = (0.2 + 0.8 * (t / 0.15), 0.1); raise_ = t / 0.15
        gx, gy = g
    elif t < 0.8:
        a = -math.pi * (t - 0.15) / 0.65     # 0 .. -180 deg sweeping over the top
        gx, gy = math.cos(a), math.sin(a)
        raise_ = 1.0
    else:
        u = (t - 0.8) / 0.2
        gx, gy = -1.0 + 1.0 * u + 0.1 * u, 0.1 * u + 0.0
        raise_ = 1 - u
    p = lerp_pose(EXPR["smug"], base, min(1, raise_ * 1.2))
    p.update(gx=gx, gy=gy, tilt=-3 * raise_ * (1 if t < 0.8 else 1))
    return p


_Q = dict(eL=0.08, eR=0.08, squint=0.08, gx=0.12, gy=0.12, laugh=0.25, blink=0.25, smirk=0.1, mscale=0.05, slant=0.5, tilt=1e9)


def key(p):
    return tuple(round(v / _Q.get(k, 1.0)) for k, v in p.items())


# ------------------------------------------------------------------ helpers
def vramp(c, y0, y1):
    """Mask: 255 above y0, fading to 0 at y1 (final-space y)."""
    ys = (np.arange(c.N, dtype=np.float32) + 0.5) / c.S
    r = np.clip((y1 - ys) / float(y1 - y0), 0, 1)
    r = np.repeat(r[:, None], c.N, 1)
    return Image.fromarray((r * 255).astype(np.uint8))


def halfplane(c, p0, p1, keep="above"):
    """Polygon covering everything above (or below) the line p0->p1 (x from -50..650)."""
    (x0, y0), (x1, y1) = p0, p1
    m = (y1 - y0) / (x1 - x0)
    ya, yb = y0 + m * (-50 - x0), y0 + m * (650 - x0)
    far = -200 if keep == "above" else 800
    return c.mask("poly", [(-50, far), (650, far), (650, yb), (-50, ya)])


def void_mask(c):
    return c.mask("poly", catmull([(300, 128), (385, 160), (428, 270), (410, 365), (300, 425), (190, 365), (172, 270), (215, 160)], True, 12))


# ------------------------------------------------------------------ base (hood, body, headphones)
def base(variant="A"):
    B = variant == "B"
    c = Canvas()
    body = c.mask("poly", catmull([(70, 620), (85, 505), (150, 440), (300, 460), (450, 440), (515, 505), (530, 620)], True, 10))
    c.glow(body, VI, 8, 0.35)
    c.fill(body, Lin((0, 440), (0, 600), [(0, F0), (1, F2)]))
    # rim light only on the upper shoulders, fading out well above the bottom corners (fixes the old lower-left streak)
    c.fill(c.sub(body, c.shift(body, 8, 6)), hexc("#b58bff", 130), clip=vramp(c, 470, 530))
    for sx in (-1, 1):
        s = c.mask("line", catmull([(300 + sx * 52, 470), (300 + sx * 58, 520), (300 + sx * 48, 565)], False, 8), w=6)
        c.fill(s, hexc("#e9e4ff"), clip=body)
        c.fill(c.mask("ell", (300 + sx * 48 - 6, 560, 300 + sx * 48 + 6, 580)), GR, clip=body)

    # raccoon ears (variant B) sit behind the hood so the hood outline stays identical
    if B:
        for sx in (-1, 1):
            pts = [(300 + sx * 168, 170), (300 + sx * 172, 70), (300 + sx * 160, 22), (300 + sx * 120, 36), (300 + sx * 78, 96)]
            ear = c.mask("poly", catmull(pts, True, 10))
            c.glow(ear, VI, 8, 0.9, grow=2)
            c.fill(ear, Lin((0, 20), (0, 170), [(0, hexc("#4a3d86")), (1, F1)]))
            ipts = [(300 + sx * 156, 150), (300 + sx * 158, 80), (300 + sx * 152, 50), (300 + sx * 128, 58), (300 + sx * 100, 100)]
            inner = c.mask("poly", catmull(ipts, True, 8))
            c.fill(inner, Lin((0, 40), (0, 150), [(0, hexc("#2a1a5c")), (1, hexc("#07041a"))]), clip=ear)
            c.fill(c.mask("poly", catmull(ipts, True, 8), outline=True, w=3.5), VI, clip=ear, alpha=0.95)
            c.fill(c.sub(ear, c.shift(ear, -sx * 5, 5)), hexc("#cfa8ff", 200), clip=vramp(c, 60, 130))
            c.fill(c.mask("poly", catmull(pts, True, 10), outline=True, w=4), hexc("#a47dff"), alpha=0.85)
    hood = c.mask("poly", catmull([(300, 38), (400, 78), (460, 190), (480, 330), (535, 470), (410, 470), (190, 470), (65, 470), (120, 330), (140, 190), (200, 78)], True, 14))
    c.glow(hood, VI, 10, 0.5, grow=1)
    c.fill(hood, Rad((260, 150), 420, [(0, hexc("#3a2f6e")), (0.5, F1), (1, F2)], ry=460))
    c.fill(c.sub(hood, c.shift(hood, 9, 7)), hexc("#cfa8ff", 160), clip=vramp(c, 330, 440))
    c.fill(c.sub(hood, c.shift(hood, -7, 6)), hexc("#9bff4a", 60), clip=vramp(c, 260, 400))
    for pts in ([(150, 250), (135, 330), (110, 420)], [(450, 250), (468, 330), (490, 420)], [(215, 90), (170, 140), (158, 200)]):
        c.fill(c.mask("line", catmull(pts, False, 8), w=5), hexc("#0c0922", 140), clip=hood)
    # soft contact shadow where the hood meets the body
    c.fill(c.blur(c.mask("rr", (60, 452, 540, 484), r=14), 7), hexc("#050310", 150), clip=body)

    vm = void_mask(c)
    c.fill(vm, Rad((300, 290), 200, [(0, VOID1), (0.6, VOID0), (1, VOID0)], ry=230))
    c.fill(c.sub(vm, c.shift(vm, -6, -8)), hexc("#3c2a78", 110))

    # headphones (B: band sits lower so the ears can peek out above it)
    top = 50 if B else 6
    band = c.mask("arc", ((88, top, 512, 520), 195, 345), w=26)
    c.glow(band, GR, 6, 0.4)
    c.fill(band, Lin((0, top + 14), (0, top + 154), [(0, hexc("#4a4a6a")), (1, CH)]))
    c.fill(c.mask("arc", ((88, top + 4, 512, 520), 220, 300), w=5), hexc("#ffffff", 70))
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
    boom = c.mask("line", catmull([(300 - 218, 365), (300 - 205, 430), (255, 432), (238, 412)], False, 8), w=6)
    c.fill(boom, hexc("#4a4a6a"))
    c.fill(c.mask("ell", (222, 396, 252, 428)), CH)
    c.fill(c.mask("ell", (228, 402, 246, 422)), GR)
    c.fade_bottom(560, 600)
    return _out(c)


# ------------------------------------------------------------------ face layers
def mask_layer(variant):
    """Neon bandit-mask band + forehead stripe (variant B only)."""
    c = Canvas()
    if variant != "B":
        return _out(c)
    vm = void_mask(c)
    half = [(300, 272), (270, 247), (226, 238), (190, 255), (198, 292), (242, 311), (282, 300)]
    pts = half + [(600 - x, y) for x, y in reversed(half)]
    mk = c.mask("poly", catmull(pts, True, 10))
    c.fill(mk, Lin((0, 238), (0, 312), [(0, hexc("#8b4dff", 52)), (1, hexc("#8b4dff", 22))]), clip=vm)
    ring = c.mask("poly", catmull(pts, True, 10), outline=True, w=3.2)
    c.glow(ring, VI, 7, 0.55)
    c.fill(ring, hexc("#b58bff"), clip=vm, alpha=0.7)
    st = c.mask("poly", catmull([(300, 140), (306, 156), (304, 190), (300, 200), (296, 190), (294, 156)], True, 6))
    c.glow(st, VI, 5, 0.6)
    c.fill(st, hexc("#a275ff"), clip=vm, alpha=0.6)
    return _out(c)


def _eye_shape(c, ex, sx, p, side):
    """Return the eye mask for one eye (sx=-1 left/viewer, +1 right)."""
    o = p["eL"] if side == "L" else p["eR"]
    o = max(0.0, o * (1 - p["blink"]))
    cy = EY
    ell = c.mask("ell", (ex - 39, cy - 23, ex + 39, cy + 23))
    # lid: covers the top (1-o) of the eye; inner end lower by `slant`
    lid_y = cy - 23 + (1 - o) * 46
    inner, outer = ex - sx * 40, ex + sx * 40
    keep = halfplane(c, (inner, lid_y + p["slant"]), (outer, lid_y - p["slant"] * 0.3), keep="below")
    m = c.inter(ell, keep)
    if p["squint"] > 0:   # lower lid pushes up
        floor_y = cy + 23 - p["squint"] * 26
        m = c.inter(m, halfplane(c, (ex - 40, floor_y + 4 * sx), (ex + 40, floor_y - 4 * sx), keep="above"))
    return m


def eyes_layer(variant, p):
    c = Canvas()
    vm = void_mask(c)
    for sx, side in ((-1, "L"), (1, "R")):
        ex = 300 + sx * EX
        if p["laugh"] > 0.5:                      # happy ^ ^ eyes
            em = c.mask("arc", ((ex - 30, EY - 8, ex + 30, EY + 40), 205, 335), w=10)
            c.glow(em, GR, 13, 0.9, grow=1); c.glow(em, GR, 5, 1.0)
            c.fill(em, Lin((0, EY - 14), (0, EY + 6), [(0, hexc("#f4ffe0")), (1, GR)]), clip=vm)
            continue
        if p["blink"] > 0.8:
            em = c.mask("line", catmull([(ex - 35, EY + 6 + sx * 1), (ex, EY + 12), (ex + 35, EY + 6 - sx * 1)], False, 8), w=5.5)
            c.glow(em, GR, 10, 0.9); c.glow(em, GR, 4, 1.0)
            c.fill(em, hexc("#e8ffcc"), clip=vm)
            continue
        em = _eye_shape(c, ex, sx, p, side)
        if not em.getbbox():
            continue
        c.glow(em, GR, 14, 1.0, grow=2)
        c.glow(em, GR, 5, 1.0)
        c.fill(em, Lin((0, EY - 22), (0, EY + 22), [(0, hexc("#f4ffe0")), (0.55, hexc("#c9ff8f")), (1, GR)]), clip=vm)
        # hot lid edge
        edge = c.sub(em, c.shift(em, 0, 5))
        c.fill(edge, hexc("#ffffff", 160), clip=em)
        # pupil: dark pill that follows the gaze; eye-roll hides it under the lid
        px, py = ex + p["gx"] * 17, EY + 2 + p["gy"] * 11 - 3
        pup = c.mask("rr", (px - 6.5, py - 14, px + 6.5, py + 14), r=6)
        c.fill(pup, hexc("#0b2a08", 215), clip=em)
    return _out(c)


def brows_layer(variant, p):
    c = Canvas()
    for sx, side in ((-1, "L"), (1, "R")):
        ex = 300 + sx * EX
        y, a, h = p["b" + side + "y"], p["b" + side + "a"], p["b" + side + "h"]
        pts = [(ex - sx * 37, y + a), (ex, y - h), (ex + sx * 37, y - a)]
        br = c.mask("line", catmull(pts, False, 10), w=9.5)
        c.glow(br, GR, 9, 0.85)
        c.fill(br, Lin((0, y - 12), (0, y + 12), [(0, hexc("#efffd6")), (1, GR)]), alpha=0.95)
    return _out(c)


def mouth_layer(variant, mouth, p):
    c = Canvas()
    B = variant == "B"
    my = 366 if B else 372
    sc = (0.80 if B else 1.0) * p["mscale"]
    n = 7 if B else 9
    sp = 13 * sc if B else 14 * sc
    bw = 3.8 if B else 5.0
    sm = p["smirk"]
    mid = (n - 1) / 2
    hs = {"closed": [1] * n,
          "small": [3, 5, 8, 10, 8, 5, 3],
          "open": [6, 14, 22, 28, 22, 14, 6],
          "wide": [10, 22, 32, 42, 32, 22, 10]}[mouth]
    if not B:
        hs = {"closed": [1] * n, "small": [3, 4, 6, 8, 10, 8, 6, 4, 3], "open": [5, 9, 15, 22, 28, 22, 15, 9, 5],
              "wide": [8, 16, 26, 34, 44, 34, 26, 16, 8]}[mouth]
    if p["laugh"] > 0.5 and mouth == "closed":
        hs = [4, 8, 12, 14, 12, 8, 4] if B else [4, 7, 10, 13, 15, 13, 10, 7, 4]
    pts = []
    for i in range(n):
        u = (i - mid) / mid
        lift = sm * 22 * sc * (np.clip((u + 0.25) / 1.25, 0, 1) ** 1.7) - sm * 3 * max(0, -u)
        hh = hs[i] * (1 + 0.38 * sm * max(0, u)) * (1 - 0.22 * sm * max(0, -u)) * (sc if B else 1.0)
        x = 300 + (i - mid) * sp
        cy = my - lift
        pts.append((x, cy))
        if mouth == "closed" and not B:
            h = 5 + (8 * sm * max(0, u) ** 2 if sm > 0 else 0) + (hh - 1 if p["laugh"] > 0.5 else 0)
            bm = c.mask("rr", (x - bw, cy - h / 2 - 1, x + bw, cy + h / 2 + 1), r=3)
        elif mouth == "closed" and B:
            continue
        else:
            bm = c.mask("rr", (x - bw, cy - hh / 2 - 2, x + bw, cy + hh / 2 + 2), r=bw)
        c.glow(bm, GR, 7, 0.8)
        c.fill(bm, Lin((0, my - 30), (0, my + 30), [(0, hexc("#e8ffcc")), (1, GRD)]))
    if mouth == "closed" and B:       # tiny glowing smirk: thin curved line with a hooked right end
        line = [(x, y) for x, y in pts]
        hook = (line[-1][0] + 5 * sc, line[-1][1] - 5 * sc)
        ln = c.mask("line", catmull(line + [hook], False, 10), w=4.6)
        c.glow(ln, GR, 7, 0.9)
        c.fill(ln, Lin((0, my - 24), (0, my + 8), [(0, hexc("#e8ffcc")), (1, GRD)]))
    return _out(c)


# ------------------------------------------------------------------ compose
_base = {}
_cache = {}


def _box():
    f = RES / 600.0
    return tuple(int(v * f) for v in (150, 100, 450, 440))


def _get(name, fn, *args):
    """Render a face layer once per quantised pose and keep only its crop (small in memory)."""
    k = (name,) + tuple(a if not isinstance(a, dict) else key(a) for a in args)
    if k not in _cache:
        if len(_cache) > 1500:
            _cache.clear()
        _cache[k] = fn(*args).crop(_box())
    return _cache[k]


def compose(variant, mouth, pose, tilt_deg=0.0):
    if variant not in _base:
        _base[variant] = base(variant)
        _base[variant + "mask"] = mask_layer(variant)
    im = _base[variant].copy()
    if variant == "B":
        im.alpha_composite(_base[variant + "mask"])
    # eyes depend on shape params only; brows on brow params; mouth on (mouth, smirk, mscale, laugh)
    ep = {k: pose[k] for k in ("eL", "eR", "slant", "squint", "gx", "gy", "laugh", "blink")}
    bp = {k: pose[k] for k in ("bLy", "bLa", "bLh", "bRy", "bRa", "bRh")}
    mp = {k: pose[k] for k in ("smirk", "mscale", "laugh")}
    full_e = dict(BASE); full_e.update(ep)
    full_b = dict(BASE); full_b.update(bp)
    full_m = dict(BASE); full_m.update(mp)
    bx = _box()[:2]
    im.alpha_composite(_get("eyes", eyes_layer, variant, full_e), bx)
    im.alpha_composite(_get("brows", brows_layer, variant, full_b), bx)
    im.alpha_composite(_get("mouth", mouth_layer, variant, mouth, full_m), bx)
    return im


def export_set(variant, outdir):
    os.makedirs(outdir, exist_ok=True)
    names = ["smug", "laugh", "squint", "raised", "glance", "glanceL", "blink"]
    for nm in names:
        for mo in MOUTHS:
            compose(variant, mo, EXPR[nm]).save(os.path.join(outdir, f"nullv2{variant}_{nm}_{mo}.png"))
    for i, t in enumerate((0.25, 0.5, 0.75)):
        for mo in MOUTHS:
            compose(variant, mo, roll_pose(t)).save(os.path.join(outdir, f"nullv2{variant}_roll{i + 1}_{mo}.png"))


if __name__ == "__main__":
    for v in sys.argv[1:] or ["A", "B"]:
        export_set(v, os.path.join(HERE, f"frames_{v}"))
        print("exported", v)
