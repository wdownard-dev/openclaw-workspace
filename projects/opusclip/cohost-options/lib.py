"""Tiny supersampled vector-ish drawing toolkit on top of Pillow + numpy.
Everything is drawn at S x the final size, then downscaled with LANCZOS (premultiplied alpha, so edges stay clean).
Coordinates are always in final (600 px) space.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageChops, ImageFilter

MOUTHS = ["closed", "small", "open", "wide"]


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(c0, c1, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c0, c1))


def catmull(pts, closed=True, n=14):
    """Smooth Catmull-Rom spline through pts -> dense polyline."""
    p = list(pts)
    if closed:
        P = [p[-1]] + p + [p[0], p[1]]
    else:
        P = [p[0]] + p + [p[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = [np.array(q, float) for q in P[i - 1:i + 3]]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                                   + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)))
    if not closed:
        out.append(tuple(P[-2]))
    return out


class Lin:
    """Linear gradient between final-space points p0->p1 with stops [(t, rgba), ...]."""
    def __init__(self, p0, p1, stops):
        self.p0, self.p1, self.stops = p0, p1, stops

    def render(self, box, S):
        x0, y0, x1, y1 = box
        ys, xs = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        xs, ys = (xs + 0.5) / S, (ys + 0.5) / S
        d = np.array(self.p1, np.float32) - np.array(self.p0, np.float32)
        t = ((xs - self.p0[0]) * d[0] + (ys - self.p0[1]) * d[1]) / float(d @ d)
        return _stops(t, self.stops)


class Rad:
    def __init__(self, c, r, stops, ry=None):
        self.c, self.r, self.stops, self.ry = c, r, stops, ry or r

    def render(self, box, S):
        x0, y0, x1, y1 = box
        ys, xs = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        xs, ys = (xs + 0.5) / S, (ys + 0.5) / S
        t = np.sqrt(((xs - self.c[0]) / self.r) ** 2 + ((ys - self.c[1]) / self.ry) ** 2)
        return _stops(t, self.stops)


def _stops(t, stops):
    t = np.clip(t, 0, 1)
    ts = [s[0] for s in stops]
    ch = [np.interp(t, ts, [s[1][i] for s in stops]) for i in range(4)]
    return Image.fromarray(np.stack(ch, -1).astype(np.uint8), "RGBA")


class Canvas:
    def __init__(self, size=600, S=3):
        self.size, self.S, self.N = size, S, size * S
        self.im = Image.new("RGBA", (self.N, self.N), (0, 0, 0, 0))

    # ---- masks -------------------------------------------------------
    def mask(self, kind, g, r=0, w=0, outline=False):
        S = self.S
        m = Image.new("L", (self.N, self.N), 0)
        d = ImageDraw.Draw(m)
        kw = dict(fill=None, outline=255, width=max(1, int(w * S))) if outline else dict(fill=255)
        if kind == "ell":
            d.ellipse([v * S for v in g], **kw)
        elif kind == "rr":
            d.rounded_rectangle([v * S for v in g], r * S, **kw)
        elif kind == "poly":
            pts = [(x * S, y * S) for x, y in g]
            if outline:
                d.line(pts + [pts[0]], fill=255, width=int(w * S), joint="curve")
            else:
                d.polygon(pts, fill=255)
        elif kind == "line":  # open polyline with round caps
            pts = [(x * S, y * S) for x, y in g]
            d.line(pts, fill=255, width=int(w * S), joint="curve")
            for (x, y) in (pts[0], pts[-1]):
                d.ellipse([x - w * S / 2, y - w * S / 2, x + w * S / 2, y + w * S / 2], fill=255)
        elif kind == "arc":  # (box, start, end)
            box, a0, a1 = g
            d.arc([v * S for v in box], a0, a1, fill=255, width=int(w * S))
            # round caps
            cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
            rx, ry = (box[2] - box[0]) / 2, (box[3] - box[1]) / 2
            for a in (a0, a1):
                x, y = cx + rx * np.cos(np.radians(a)), cy + ry * np.sin(np.radians(a))
                d.ellipse([(x - w / 2) * S, (y - w / 2) * S, (x + w / 2) * S, (y + w / 2) * S], fill=255)
        return m

    @staticmethod
    def union(*ms):
        out = ms[0]
        for m in ms[1:]:
            out = ImageChops.lighter(out, m)
        return out

    @staticmethod
    def sub(a, b):
        return ImageChops.subtract(a, b)

    @staticmethod
    def inter(a, b):
        return ImageChops.multiply(a, b)

    def shift(self, m, dx, dy):
        return ImageChops.offset(m, int(dx * self.S), int(dy * self.S))

    def blur(self, m, rad):
        return m.filter(ImageFilter.GaussianBlur(rad * self.S))

    # ---- painting ----------------------------------------------------
    def fill(self, m, paint, clip=None, alpha=1.0):
        if clip is not None:
            m = ImageChops.multiply(m, clip)
        box = m.getbbox()
        if not box:
            return m
        layer = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), paint) if isinstance(paint, tuple) \
            else paint.render(box, self.S)
        a = m.crop(box)
        la = np.asarray(layer.getchannel("A"), np.float32) / 255.0
        am = (np.asarray(a, np.float32) * la * alpha).astype(np.uint8)
        layer.putalpha(Image.fromarray(am))
        self.im.alpha_composite(layer, (box[0], box[1]))
        return m

    def shape(self, kind, g, paint, r=0, w=0, outline=None, ow=0, clip=None, alpha=1.0):
        """Fill a shape and optionally stroke it (stroke is drawn inward). Returns the fill mask."""
        m = self.mask(kind, g, r=r, w=w)
        self.fill(m, paint, clip, alpha)
        if outline is not None and ow:
            st = self.mask(kind, g, r=r, w=ow, outline=True)
            self.fill(ImageChops.multiply(st, m) if kind in ("poly",) else st, outline, clip, alpha)
        return m

    def glow(self, m, color, rad, k=1.0, grow=0):
        """Soft halo of a mask (draws only color with blurred alpha)."""
        S = self.S
        pad = int(rad * S * 3)
        box = m.getbbox()
        if not box:
            return
        box = (max(0, box[0] - pad), max(0, box[1] - pad), min(self.N, box[2] + pad), min(self.N, box[3] + pad))
        c = m.crop(box)
        if grow:
            c = c.filter(ImageFilter.MaxFilter(int(grow * S) * 2 + 1))
        c = c.filter(ImageFilter.GaussianBlur(rad * S))
        a = (np.asarray(c, np.float32) * min(1.0, k) * color[3] / 255.0).astype(np.uint8)
        layer = Image.new("RGBA", c.size, color[:3] + (255,))
        layer.putalpha(Image.fromarray(a))
        self.im.alpha_composite(layer, (box[0], box[1]))

    def fade_bottom(self, y0, y1):
        """Alpha ramp to 0 between final-space y0..y1 (hologram bust fade)."""
        S = self.S
        a = np.asarray(self.im.getchannel("A"), np.float32)
        ys = (np.arange(self.N, dtype=np.float32) + 0.5) / S
        ramp = np.clip((y1 - ys) / float(y1 - y0), 0, 1)[:, None]
        ramp = ramp * ramp * (3 - 2 * ramp)
        self.im.putalpha(Image.fromarray((a * ramp).astype(np.uint8)))

    def out(self):
        return self.im.resize((self.size, self.size), Image.LANCZOS)


def save_set(module, outdir):
    """Render module.draw(mouth, blink) for all mouth states -> PNGs."""
    import os
    os.makedirs(outdir, exist_ok=True)
    for mo in MOUTHS:
        for bl in (False, True):
            module.draw(mo, bl).save(os.path.join(outdir, f"{module.SLUG}_{mo}{'_blink' if bl else ''}.png"))
