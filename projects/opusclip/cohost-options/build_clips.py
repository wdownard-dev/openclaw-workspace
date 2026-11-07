#!/usr/bin/env python
"""Render one character's talking clip: Kokoro TTS -> mouth-synced 1080x1920 card -> <slug>.mp4
Usage: tts-venv/bin/python build_clips.py slug [--skip-tts]
Reads PNGs from ./<slug>/<slug>_{closed,small,open,wide}[_blink].png (run make_frames.py first).
"""
import sys, os, importlib, subprocess, time
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "chars"))
FFMPEG = "/home/williamdownard/openclaw-sites/bin/ffmpeg"
W, H, FPS, SR = 1080, 1920, 30, 24000
FD = "/usr/share/fonts/opentype/fira/"
slug = sys.argv[1]
mod = importlib.import_module(slug)
MOUTHS = ["closed", "small", "open", "wide"]
PIXEL = slug == "quarter"
LEAD, TAIL = 0.55, 0.8


def font(name, size):
    return ImageFont.truetype(FD + name, size)


def synth():
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="b" if mod.VOICE.startswith("b") else "a", repo_id="hexgrad/Kokoro-82M")
    wav = np.concatenate([r[2].numpy() for r in pipe(mod.LINE, voice=mod.VOICE, speed=mod.SPEED)])
    wav = np.concatenate([np.zeros(int(LEAD * SR)), wav, np.zeros(int(TAIL * SR))]).astype(np.float32)
    wav *= 0.9 / max(1e-6, np.abs(wav).max())
    sf.write(os.path.join(HERE, slug, f"{slug}_voice.wav"), wav, SR)
    return wav


def make_bg(pulse):
    rng = np.random.RandomState(abs(hash(slug)) % 1000 + 7)
    top = np.array(mod.BG[0], np.float32); bot = np.array(mod.BG[1], np.float32)
    ys = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    img = top * (1 - ys) + bot * ys * np.ones((1, W, 1), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    acc = np.array(mod.ACCENT, np.float32)
    r = np.sqrt(((xx - 540) / 640) ** 2 + ((yy - 720) / 700) ** 2)
    g = np.clip(1 - r, 0, 1) ** 2 * (0.30 + 0.12 * pulse)
    img = img * (1 - g[..., None]) + acc * g[..., None]
    # floor grid (perspective-ish) in lower third
    fy = (yy - 1180) / 740.0
    floor = fy > 0
    lines = np.zeros((H, W), np.float32)
    hz = np.abs(((np.clip(fy, 1e-3, 1)) ** 2 * 18) % 1 - 0.5)
    lines = np.where(floor & (hz > 0.46), 0.10 * fy, 0)
    vx = (xx - 540) / (np.clip(fy, 0.02, 1) * 900 + 1)
    vl = np.abs((vx * 5) % 1 - 0.5)
    lines = np.maximum(lines, np.where(floor & (vl > 0.47), 0.10 * fy, 0))
    img = img * (1 - lines[..., None]) + acc * lines[..., None]
    # sparkles
    for _ in range(46):
        x, y = rng.randint(30, W - 30), rng.randint(60, 1250)
        a = rng.uniform(0.10, 0.45); s = rng.choice([2, 3, 4])
        img[y:y + s, x:x + s] = img[y:y + s, x:x + s] * (1 - a) + 255 * a
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").convert("RGBA")


def label_layer():
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    acc = mod.ACCENT + (255,)
    # AI CO-HOST pill
    f = font("FiraSans-Bold.otf", 40)
    txt = "AI CO-HOST"
    tw = d.textlength(txt, font=f) + sum([0]) + 9 * 6
    px0 = (W - tw) / 2 - 44
    d.rounded_rectangle([px0, 96, px0 + tw + 88, 176], 40, fill=(0, 0, 0, 150), outline=acc, width=4)
    d.ellipse([px0 + 26, 128, px0 + 46, 148], fill=acc)
    x = px0 + 66
    for ch in txt:
        d.text((x, 136), ch, font=f, fill=(255, 255, 255, 255), anchor="lm")
        x += d.textlength(ch, font=f) + 6
    # name + tagline
    fn = font("FiraSansCondensed-ExtraBold.otf", 190)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).text((W / 2, 1275), mod.NAME, font=fn, fill=acc, anchor="mm")
    from PIL import ImageFilter
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    L.alpha_composite(glow)
    d.text((W / 2 + 5, 1280), mod.NAME, font=fn, fill=(0, 0, 0, 160), anchor="mm")
    d.text((W / 2, 1275), mod.NAME, font=fn, fill=(255, 255, 255, 255), anchor="mm", stroke_width=3, stroke_fill=mod.ACCENT + (255,))
    ft = font("FiraSans-Medium.otf", 54)
    d.text((W / 2, 1405), mod.TAGLINE, font=ft, fill=(235, 235, 245, 255), anchor="mm")
    d.rounded_rectangle([W / 2 - 90, 1458, W / 2 + 90, 1466], 4, fill=acc)
    return L


def caption_chunks(wav):
    words = mod.LINE.split()
    k = max(1, round(len(words) / 4))
    chunks = [" ".join(c) for c in np.array_split(np.array(words, dtype=object), k)]
    env = np.abs(wav)
    act = np.where(np.convolve(env, np.ones(SR // 50) / (SR // 50), "same") > 0.01)[0]
    t0, t1 = act[0] / SR, act[-1] / SR
    lens = np.array([len(c) for c in chunks], float)
    bounds = t0 + np.concatenate([[0], np.cumsum(lens) / lens.sum()]) * (t1 - t0)
    f = font("FiraSansCondensed-ExtraBold.otf", 82)
    imgs = []
    for c in chunks:
        im = Image.new("RGBA", (W, 190), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        lines = [c]
        if d.textlength(c, font=f) > 980:
            h = len(c.split()) // 2
            lines = [" ".join(c.split()[:h]), " ".join(c.split()[h:])]
        for i, ln in enumerate(lines):
            y = 95 + (i - (len(lines) - 1) / 2) * 90
            d.text((W / 2, y), ln, font=f, fill=(255, 255, 255, 255), anchor="mm", stroke_width=9, stroke_fill=(10, 8, 20, 255))
        imgs.append(im)
    return imgs, bounds


def mouth_states(wav, n):
    hop = SR // FPS
    env = np.array([np.sqrt(np.mean(wav[i * hop:(i + 1) * hop + hop // 2] ** 2) + 1e-12) if i * hop < len(wav) else 0 for i in range(n)])
    ref = np.percentile(env[env > 0.01], 90)
    e = env / ref
    st = np.digitize(e, [0.12, 0.38, 0.70])
    pad = np.pad(st, 1, mode="edge")
    return np.median(np.stack([pad[:-2], pad[1:-1], pad[2:]]), axis=0).astype(int), np.clip(e, 0, 1.2)


def main():
    t0 = time.time()
    wav = synth() if "--skip-tts" not in sys.argv else sf.read(os.path.join(HERE, slug, f"{slug}_voice.wav"), dtype="float32")[0]
    dur = len(wav) / SR
    n = int(dur * FPS)
    bgA, bgB = make_bg(0), make_bg(1)
    L = label_layer()
    bgA.alpha_composite(L); bgB.alpha_composite(L)
    caps, cb = caption_chunks(wav)
    st, env = mouth_states(wav, n)
    size = 880 if PIXEL else 900
    frames = {}
    for mo in MOUTHS:
        for bl in (0, 1):
            im = Image.open(os.path.join(HERE, slug, f"{slug}_{mo}{'_blink' if bl else ''}.png"))
            frames[(mo, bl)] = im.resize((size, size), Image.NEAREST if PIXEL else Image.LANCZOS)
    blink_at = [int(x * FPS) for x in (1.7, 3.9, 6.0)]
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", os.path.join(HERE, slug, f"{slug}_voice.wav"), "-map", "0:v", "-map", "1:a", "-t", f"{dur:.3f}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
           "-movflags", "+faststart", os.path.join(HERE, "clips", f"{slug}.mp4")]
    os.makedirs(os.path.join(HERE, "clips"), exist_ok=True)
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    still = None
    for f in range(n):
        t = f / FPS
        pulse = 0.5 + 0.5 * np.sin(t * 2.2)
        base = Image.blend(bgA, bgB, float(pulse))
        blink = int(any(b <= f < b + 4 for b in blink_at) and st[f] <= 1)
        s = size
        ox = (W - s) // 2
        bob = 9 * np.sin(t * 2.4) - (12 * env[f] if st[f] > 0 else 0)
        if PIXEL:
            by = 250 + int(round(bob / 11)) * 11
            spr = frames[(MOUTHS[st[f]], blink)]
        else:
            k = 1 + 0.012 * np.sin(t * 2.4 + 0.6)       # breathing, anchored at the bottom centre
            s = int(size * k)
            by = 250 + int(bob) + (size - s)
            ox = (W - s) // 2
            spr = frames[(MOUTHS[st[f]], blink)]
            if s != size:
                spr = spr.resize((s, s), Image.BILINEAR)
        base.alpha_composite(spr, (ox, by))
        ci = int(np.searchsorted(cb, t, side="right") - 1)
        if 0 <= ci < len(caps) and t <= cb[-1] + 0.4:
            base.alpha_composite(caps[ci], (0, 1540))
        p.stdin.write(base.convert("RGB").tobytes())
        if f == int(n * 0.45):
            still = base.convert("RGB").copy()
    p.stdin.close(); p.wait()
    os.makedirs(os.path.join(HERE, "stills"), exist_ok=True)
    still.save(os.path.join(HERE, "stills", f"{slug}.png"))
    print(f"{slug}: {dur:.1f}s audio, rc={p.returncode}, {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
