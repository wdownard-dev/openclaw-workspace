#!/usr/bin/env python
"""AI cartoon co-host demo builder (free/local: Kokoro TTS, Pillow mascot, ffmpeg).
Run with the tts-venv python:  /home/williamdownard/openclaw-sites/tts-venv/bin/python build.py
Stages: 1) TTS per line -> voice.wav + timeline  2) ASS captions  3) outro background
        4) mouth-synced mascot RGBA stream piped into ffmpeg  5) mix (duck) + encode.
Edit config.json to change the script, voice, clip or timing.
"""
import json, os, subprocess, sys, time
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
FFMPEG = "/home/williamdownard/openclaw-sites/bin/ffmpeg"
CFG = json.load(open(os.path.join(HERE, "config.json")))
W, H, FPS, SR = 1080, 1920, 30, 24000
os.chdir(HERE)
T0 = time.time()

# ---------------------------------------------------------------- 1. TTS
def synth_all():
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    timeline, chunks, cursor = [], [], 0.0
    lines = [dict(l, part="clip") for l in CFG["interjections"]] + [dict(l, part="outro") for l in CFG["outro"]]
    for l in lines:
        wav = np.concatenate([r[2].numpy() for r in pipe(l["text"], voice=CFG["voice"], speed=CFG["speed"])])
        wav = np.concatenate([wav, np.zeros(int(0.12 * SR))]).astype(np.float32)
        start = l["at"] if l["part"] == "clip" else CFG["outro_start"] + l["at"]
        if l["part"] == "outro" and timeline and timeline[-1]["part"] == "outro":
            start = max(start, timeline[-1]["end"] + CFG["outro_gap"]) if l["at"] == 0 else start
        timeline.append(dict(l, start=start, end=start + len(wav) / SR, wav=wav))
    total = max(t["end"] for t in timeline) + 1.0
    mix = np.zeros(int(total * SR), np.float32)
    for t in timeline:
        i = int(t["start"] * SR)
        mix[i:i + len(t["wav"])] += t["wav"]
    mix *= 0.92 / max(1e-6, np.abs(mix).max())
    sf.write("voice.wav", mix, SR)
    for t in timeline:
        t.pop("wav")
    json.dump(timeline, open("timeline.json", "w"), indent=1)
    return timeline, mix

# ---------------------------------------------------------------- 2. ASS captions
def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"

def chunk_words(text, n=5):
    w = text.split()
    k = -(-len(w) // n)  # ceil: even-sized chunks, no orphan words
    return [" ".join(c) for c in np.array_split(np.array(w, dtype=object), k)]

def write_ass(timeline, total):
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,Fira Sans Condensed,84,&H00FFFFFF,&H000000FF,&H00281E1C,&H00000000,-1,0,0,0,100,100,0,0,1,7,2,8,60,60,1180,1
Style: CapOut,Fira Sans Condensed,92,&H00FFFFFF,&H000000FF,&H00281E1C,&H00000000,-1,0,0,0,100,100,0,0,1,7,2,8,60,60,1310,1
Style: Tag,Fira Sans Condensed,60,&H00FFFFFF,&H00000000,&H009650FF,&H009650FF,-1,0,0,0,100,100,3,0,3,14,0,8,0,0,95,1
Style: Part,Fira Sans Condensed,56,&H0028281C,&H00000000,&H0028C4FF,&H0028C4FF,-1,0,0,0,100,100,3,0,3,12,0,8,0,0,1190,1
Style: Demo,Fira Sans Condensed,38,&H00DDDDDD,&H00000000,&H00000000,&H00000000,-1,0,0,0,100,100,2,0,1,3,0,8,0,0,185,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = [f"Dialogue: 0,{ts(0)},{ts(total)},Tag,,0,0,0,,AI CO-HOST",
          f"Dialogue: 0,{ts(0)},{ts(total)},Demo,,0,0,0,,DEMO SCRIPT  -  synthetic voice and cartoon mascot"]
    for t in timeline:
        ch = chunk_words(t["text"])
        weights = np.array([len(c) for c in ch], float)
        dur = t["end"] - t["start"] - 0.1
        edges = t["start"] + np.concatenate([[0], np.cumsum(weights / weights.sum())]) * dur
        style = "Cap" if t["part"] == "clip" else "CapOut"
        for i, c in enumerate(ch):
            e = edges[i + 1] + (0.25 if i == len(ch) - 1 else 0)
            ev.append(f"Dialogue: 0,{ts(edges[i])},{ts(e)},{style},,0,0,0,,{c.upper()}")
        if t.get("label"):
            ev.append(f"Dialogue: 1,{ts(t['start'])},{ts(t['end'] + 0.25)},Part,,0,0,1195,,{t['label']}")
    open("captions.ass", "w").write(hdr + "\n".join(ev) + "\n")

# ---------------------------------------------------------------- 3. outro background
def make_bg():
    im = Image.new("RGB", (W, H))
    px = np.zeros((H, W, 3), np.float32)
    top, bot = np.array([34, 24, 84]), np.array([12, 70, 120])
    g = np.linspace(0, 1, H)[:, None, None]
    px[:] = top * (1 - g) + bot * g
    im = Image.fromarray(px.astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA")
    for i, (x, y, r) in enumerate([(120, 260, 260), (960, 520, 190), (200, 1500, 300), (930, 1700, 230), (540, 1000, 480)]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 10 + 4 * (i % 3)))
    for y in range(0, H, 96):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 12), width=2)
    im.save("outro_bg.png")

# ---------------------------------------------------------------- 4. mascot stream
def mouth_states(mix, nframes):
    hop = SR // FPS
    env = np.array([np.sqrt(np.mean(mix[i * hop:(i + 1) * hop + hop // 2] ** 2) + 1e-12) if i * hop < len(mix) else 0 for i in range(nframes)])
    ref = np.percentile(env[env > 0.01], 90) if (env > 0.01).any() else 1
    e = env / ref
    state = np.where(e < 0.10, 0, np.where(e < 0.45, 1, 2))
    # 3-frame median to remove flicker
    pad = np.pad(state, 1, mode="edge")
    return np.median(np.stack([pad[:-2], pad[1:-1], pad[2:]]), axis=0).astype(int), np.clip(e, 0, 1)

def ease(x):
    x = min(max(x, 0), 1)
    return x * x * (3 - 2 * x)

def stream_mascot(proc, mix, nframes):
    names = ["closed", "half", "open"]
    base = {n: [Image.open(f"frames/mascot_{n}{b}.png") for b in ("", "_blink")] for n in names}
    cache = {}
    def get(n, blink, size):
        k = (n, blink, size)
        if k not in cache:
            if len(cache) > 400:
                cache.clear()
            cache[k] = base[n][blink].resize((size, size), Image.LANCZOS)
        return cache[k]
    st, env = mouth_states(mix, nframes)
    t_out = CFG["outro_start"] + 0.2
    for f in range(nframes):
        t = f / FPS
        k = ease((t - t_out) / 0.7)
        size = int(CFG["mascot_small"] + (CFG["mascot_big"] - CFG["mascot_small"]) * k)
        x = int(CFG["small_xy"][0] + (CFG["big_xy"][0] - CFG["small_xy"][0]) * k) - (size - CFG["mascot_small"]) // 2 * 0
        y = int(CFG["small_xy"][1] + (CFG["big_xy"][1] - CFG["small_xy"][1]) * k)
        x -= int((size - CFG["mascot_small"]) * 0.0)
        # idle bob + speech bounce
        y += int(7 * np.sin(t * 2.6)) - int(14 * env[f] * (st[f] > 0))
        blink = 1 if (f % 96) in (0, 1, 2, 3) and st[f] == 0 else 0
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.alpha_composite(get(names[st[f]], blink, size), (x, y))
        proc.stdin.write(layer.tobytes())
    proc.stdin.close()

# ---------------------------------------------------------------- 5. ffmpeg
def main():
    if "--skip-tts" in sys.argv and os.path.exists("voice.wav"):
        timeline = json.load(open("timeline.json"))
        mix, _ = sf.read("voice.wav", dtype="float32")
    else:
        timeline, mix = synth_all()
    t_tts = time.time() - T0
    total = CFG["total"]
    write_ass(timeline, total)
    make_bg()
    ss, cl = CFG["clip_start"], CFG["clip_len"]
    to = CFG["outro_start"]
    fade = 0.6
    nframes = int(total * FPS)
    fc = (
        f"[0:v]trim=start={ss}:end={ss + cl},setpts=PTS-STARTPTS,fps={FPS},split[a][b];"
        f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:6,eq=brightness=-0.18[bg];"
        f"[b]scale={W}:-2[fg];[bg][fg]overlay=0:{CFG['clip_y']},format=yuv420p[clipv];"
        f"[1:v]format=yuv420p,fps={FPS}[ob];"
        f"[clipv][ob]xfade=transition=fade:duration={fade}:offset={cl - fade}[base];"
        f"[base][2:v]overlay=0:0:format=auto[m];"
        f"[m]ass=captions.ass:fontsdir=/usr/share/fonts/opentype/fira[v];"
        f"[0:a]atrim=start={ss}:end={ss + cl},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=0.9[ca];"
        f"[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.6,asplit[v1][v2];"
        f"[ca][v1]sidechaincompress=threshold=0.015:ratio=12:attack=15:release=450:makeup=1[du];"
        f"[du]afade=t=out:st={cl - 0.6}:d=0.6[du2];"
        f"[du2][v2]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95,apad,atrim=0:{total}[a]"
    )
    out = CFG["output"]
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
           "-i", CFG["clip"],
           "-loop", "1", "-framerate", str(FPS), "-t", str(total), "-i", "outro_bg.png",
           "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", "voice.wav",
           "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
           "-t", str(total), "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-maxrate", "9M", "-bufsize", "18M",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    t1 = time.time()
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    stream_mascot(p, mix, nframes)
    p.wait()
    print(f"TTS+prep {t_tts:.1f}s, render {time.time() - t1:.1f}s, total {time.time() - T0:.1f}s, rc={p.returncode}")

if __name__ == "__main__":
    main()
