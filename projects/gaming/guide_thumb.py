#!/usr/bin/env python3
"""wrdgamingclipz guide-Short thumbnail (cover) template. William picked style 1 on 2026-11-21.

A full-bleed 1080x1920 portrait cover that fills the phone screen even though the video itself is letterboxed on blur:
tight 9:16 crop of ONE source frame with the subject large, a light fade at the bottom, and a two-line headline at the bottom
(line 1 white, line 2 yellow, heavy italic Anton, both lines stretched to the same width, thick dark outline plus shadow).
No logo, no credit text. Optional white-bordered inset card (map, weapon card) above the headline.

  guide_thumb.py ID                       build from out/ID.guide.json "thumb" block (see below)
  guide_thumb.py ID --src SRC_ID --t 53 --x0 388 --l1 "PAUL WALKER'S" --l2 "ECLIPSE" [--inset SRC_ID:T:x0:y0:x1:y1[:px:py]]
  guide_thumb.py ID --frame path.png ...  use an existing 16:9 frame (any size) instead of extracting one

guide.json block (all optional except l1/l2 and a frame source):
  "thumb": {"src": "0KkxxY3iJjQ", "t": 53, "x0": 388, "l1": "PAUL WALKER'S", "l2": "ECLIPSE",
            "inset": {"src": "0KkxxY3iJjQ", "t": 26, "box": [0, 0, 1280, 720], "pos": [40, 1140]}}
  x0 = left edge (in source pixels, 1280x720 frame) of the 405 px wide 9:16 crop; pick it so the subject is centred.
  Output: out/ID.thumb.png (lossless preview) and out/ID.thumb.jpg (<2 MB, for YouTube thumbnails.set via yt_upload_gaming.py --thumb).
Frames come from work/guides/<src>/src.* (the fetched guide source); needs no network.
"""
import argparse, json, os, subprocess, sys

B = os.path.dirname(os.path.abspath(__file__))
FF = "/home/williamdownard/openclaw-sites/bin/ffmpeg"
ANTON = B + "/assets/fonts/Anton-Regular.ttf"
W, H = 1080, 1920
YEL = (255, 214, 10)
WHITE = (255, 255, 255)


def src_file(src):
    d = f"{B}/work/guides/{src}"
    fs = [f for f in os.listdir(d) if f.startswith("src.")]
    if not fs:
        sys.exit(f"no source video in {d} (run guide_make.py {src} fetch)")
    return f"{d}/{fs[0]}"


def grab(src, t, out):
    r = subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(t), "-i", src_file(src), "-frames:v", "1", out], capture_output=True, text=True)
    if r.returncode or not os.path.exists(out):
        sys.exit("frame grab failed: " + r.stderr[-300:])
    return out


def fit_line(txt, fill, width=1000, stroke=13, skew=0.17, maxsize=300):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    size = maxsize
    while True:
        f = ImageFont.truetype(ANTON, size)
        if d.textlength(txt, font=f) <= width or size <= 40:
            break
        size -= 2
    tw = int(d.textlength(txt, font=f)); pad = stroke * 3
    lw, lh = tw + pad * 2 + int(size * skew), int(size * 1.35) + pad * 2
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    sh = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((pad + 6, pad + 12), txt, font=f, fill=(0, 0, 0, 230), stroke_width=stroke, stroke_fill=(0, 0, 0, 230))
    lay = Image.alpha_composite(lay, sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(lay).text((pad, pad), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=(20, 12, 0, 255))
    lay = lay.transform(lay.size, Image.AFFINE, (1, skew, -skew * lh / 2, 0, 1, 0), resample=Image.BICUBIC)
    return lay.crop(lay.getbbox())


def build(vid, frame, x0, l1, l2, inset=None):
    from PIL import Image, ImageDraw
    fr = Image.open(frame).convert("RGB")
    fw, fh = fr.size
    cw = round(fh * 9 / 16)  # 9:16 crop width at the frame's height
    x0 = max(0, min(int(x0), fw - cw))
    im = fr.crop((x0, 0, x0 + cw, fh)).resize((W, H), Image.LANCZOS).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for y in range(H):  # bottom fade behind the headline
        a = int(255 * max(0, (y / H - 0.62) / 0.38) ** 1.6 * 0.6)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    im = Image.alpha_composite(im, ov)
    if inset:
        pf = grab(inset["src"], inset["t"], f"{B}/work/thumbs/_inset_{vid}.png")
        ic = Image.open(pf).convert("RGB").crop(tuple(inset.get("box", (0, 0, 1280, 720))))
        iw = inset.get("w", 440); ih = int(iw * ic.height / ic.width); ic = ic.resize((iw, ih), Image.LANCZOS)
        x, y = inset.get("pos", (40, 1140)); b = 8; dd = ImageDraw.Draw(im)
        dd.rectangle([x - b - 4, y - b + 4, x + iw + b + 4, y + ih + b + 12], fill=(0, 0, 0, 160))
        dd.rectangle([x - b, y - b, x + iw + b, y + ih + b], fill=(255, 255, 255, 255)); im.paste(ic, (x, y))
    a = fit_line(l1, WHITE); b2 = fit_line(l2, YEL)
    y2 = 1850 - b2.height; y1 = y2 - a.height + 6
    im.alpha_composite(a, ((W - a.width) // 2, y1)); im.alpha_composite(b2, ((W - b2.width) // 2, y2))
    out = f"{B}/out/{vid}.thumb"
    im.convert("RGB").save(out + ".png")
    q = 92
    while True:
        im.convert("RGB").save(out + ".jpg", quality=q)
        if os.path.getsize(out + ".jpg") < 1_900_000 or q <= 60:
            break
        q -= 8
    print("THUMB", out + ".png", out + ".jpg", os.path.getsize(out + ".jpg") // 1024, "KB")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id"); ap.add_argument("--src"); ap.add_argument("--t", type=float); ap.add_argument("--x0", type=int)
    ap.add_argument("--l1"); ap.add_argument("--l2"); ap.add_argument("--frame"); ap.add_argument("--inset")
    a = ap.parse_args()
    th = {}
    gp = f"{B}/out/{a.id}.guide.json"
    if os.path.exists(gp):
        th = json.load(open(gp)).get("thumb", {}) or {}
    src = a.src or th.get("src"); t = a.t if a.t is not None else th.get("t")
    x0 = a.x0 if a.x0 is not None else th.get("x0"); l1 = a.l1 or th.get("l1"); l2 = a.l2 or th.get("l2")
    inset = th.get("inset")
    if a.inset:
        p = a.inset.split(":"); inset = {"src": p[0], "t": float(p[1]), "box": [int(v) for v in p[2:6]]}
        if len(p) >= 8: inset["pos"] = [int(p[6]), int(p[7])]
    if not (l1 and l2) or x0 is None or not (a.frame or (src and t is not None)):
        sys.exit("need l1, l2, x0 and a frame (--frame, or src + t); see --help")
    os.makedirs(f"{B}/work/thumbs", exist_ok=True)
    frame = a.frame or grab(src, t, f"{B}/work/thumbs/_frame_{a.id}.png")
    build(a.id, frame, x0, l1, l2, inset)


if __name__ == "__main__":
    main()
