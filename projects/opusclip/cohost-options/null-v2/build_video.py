#!/usr/bin/env python
"""NULL v2 video builder (same structure as ../../cohost-demo/build.py, but the mascot is the layered NULL v2 rig).
Usage: tts-venv/bin/python build_video.py configs/demo.json [--skip-tts]
Config keys: variant (A|B), voice, speed, clip, clip_start, clip_len, fade, outro_start, outro_gap, out,
  interjections[{at,text,expr:[[offset,name|'roll',dur?],...]}], reactions[{at,expr,dur}] (silent, segment time),
  outro[{label,text,at?,expr:[...]}], small_xy, mascot_small, mascot_big, big_xy.
Expressions: smug laugh squint raised glance glanceL blink roll (see null_v2.EXPR).
Per frame: pose = low-pass(step pose from the expression events) + talking brow bounce + scheduled blink + idle head tilt;
mouth state from voice loudness (4 levels); layers rendered/cached by null_v2.compose.
"""
import json, os, subprocess, sys, time
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import null_v2 as N
CFG = json.load(open(sys.argv[1]))
FFMPEG = "/home/williamdownard/openclaw-sites/bin/ffmpeg"
W, H, FPS, SR = 1080, 1920, 30, 24000
WORK = os.path.join(HERE, "work", os.path.splitext(os.path.basename(sys.argv[1]))[0])
os.makedirs(WORK, exist_ok=True)
T0 = time.time()
N.RES = 800


# ---------------------------------------------------------------- TTS
def synth_all():
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="b" if CFG["voice"].startswith("b") else "a", repo_id="hexgrad/Kokoro-82M")
    timeline, cursor = [], 0.0
    lines = [dict(l, part="clip") for l in CFG["interjections"]] + [dict(l, part="outro") for l in CFG["outro"]]
    for l in lines:
        wav = np.concatenate([r[2].numpy() for r in pipe(l["text"], voice=CFG["voice"], speed=CFG["speed"])])
        wav = np.concatenate([wav, np.zeros(int(0.12 * SR))]).astype(np.float32)
        start = l["at"] if l["part"] == "clip" else CFG["outro_start"] + l["at"]
        if l["part"] == "outro" and timeline and timeline[-1]["part"] == "outro" and l["at"] == 0:
            start = timeline[-1]["end"] + CFG["outro_gap"]
        timeline.append(dict(l, start=start, end=start + len(wav) / SR, wav=wav))
    total = max(t["end"] for t in timeline) + 1.2
    mix = np.zeros(int(total * SR), np.float32)
    for t in timeline:
        i = int(t["start"] * SR)
        mix[i:i + len(t["wav"])] += t["wav"]
    mix *= 0.92 / max(1e-6, np.abs(mix).max())
    sf.write(os.path.join(WORK, "voice.wav"), mix, SR)
    for t in timeline:
        t.pop("wav")
    json.dump(dict(total=total, timeline=timeline), open(os.path.join(WORK, "timeline.json"), "w"), indent=1)
    return timeline, mix, total


# ---------------------------------------------------------------- ASS captions
def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def chunk_words(text, n=5):
    w = text.split()
    k = -(-len(w) // n)
    return [" ".join(c) for c in np.array_split(np.array(w, dtype=object), k)]


def write_ass(timeline, total):
    name = CFG.get("name", "NULL//SMIRK")
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,Fira Sans Condensed,84,&H00FFFFFF,&H000000FF,&H00281E1C,&H00000000,-1,0,0,0,100,100,0,0,1,7,2,8,60,60,1180,1
Style: CapOut,Fira Sans Condensed,92,&H00FFFFFF,&H000000FF,&H00281E1C,&H00000000,-1,0,0,0,100,100,0,0,1,7,2,8,60,60,1310,1
Style: Tag,Fira Sans Condensed,60,&H00FFFFFF,&H00000000,&H004AFF9B,&H004AFF9B,-1,0,0,0,100,100,3,0,3,14,0,8,0,0,95,1
Style: Part,Fira Sans Condensed,56,&H0028281C,&H00000000,&H004AFF9B,&H004AFF9B,-1,0,0,0,100,100,3,0,3,12,0,8,0,0,1190,1
Style: Demo,Fira Sans Condensed,38,&H00DDDDDD,&H00000000,&H00000000,&H00000000,-1,0,0,0,100,100,2,0,1,3,0,8,0,0,185,1
Style: Name,Fira Sans Condensed,66,&H00FF9CC9,&H00000000,&H00281E1C,&H00000000,-1,0,0,0,100,100,6,0,1,4,0,2,0,0,70,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = [f"Dialogue: 0,{ts(0)},{ts(total)},Tag,,0,0,0,,AI CO-HOST",
          f"Dialogue: 0,{ts(0)},{ts(total)},Demo,,0,0,0,,DEMO SCRIPT  -  synthetic voice and cartoon mascot",
          f"Dialogue: 0,{ts(CFG['outro_start'] + 0.6)},{ts(total)},Name,,0,0,0,,{name}"]
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
    open(os.path.join(WORK, "captions.ass"), "w").write(hdr + "\n".join(ev) + "\n")


def make_bg():
    px = np.zeros((H, W, 3), np.float32)
    top, bot = np.array([12, 8, 34]), np.array([34, 14, 70])
    g = np.linspace(0, 1, H)[:, None, None]
    px[:] = top * (1 - g) + bot * g
    im = Image.fromarray(px.astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA")
    for i, (x, y, r) in enumerate([(120, 260, 260), (960, 520, 190), (200, 1500, 300), (930, 1700, 230), (540, 900, 470)]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=(139, 77, 255, 12 + 4 * (i % 3)))
    for y in range(0, H, 96):
        d.line([(0, y), (W, y)], fill=(155, 255, 74, 10), width=2)
    im.save(os.path.join(WORK, "outro_bg.png"))


# ---------------------------------------------------------------- expression timeline
def build_events(timeline):
    ev = []     # (start, name, dur)
    seg = lambda t: t     # reactions are in absolute video time (clip segment starts at 0)
    for t in timeline:
        for x in t.get("expr", [["0", "smug"]]):
            off, nm = float(x[0]), x[1]
            dur = float(x[2]) if len(x) > 2 else None
            ev.append([t["start"] + off, nm, dur])
        # return to smug a beat after the line
        ev.append([t["end"] + 0.35, "smug", None])
    for r in CFG.get("reactions", []):
        ev.append([r["at"], r["expr"], r.get("dur", 1.4)])
        ev.append([r["at"] + r.get("dur", 1.4) + 0.2, "smug", None])
    ev.sort(key=lambda e: e[0])
    for i, e in enumerate(ev):             # open-ended events last until the next one
        if e[2] is None:
            e[2] = (ev[i + 1][0] - e[0]) if i + 1 < len(ev) else 99
        else:
            e[2] = e[2]
    return ev


def raw_pose(t, ev):
    cur = None
    for s, nm, d in ev:
        if s <= t:
            cur = (s, nm, d)
    if cur is None:
        return N.EXPR["smug"]
    s, nm, d = cur
    if nm == "roll":
        u = (t - s) / max(d, 0.1)
        return N.roll_pose(min(1.0, max(0.0, u))) if u <= 1.0 else N.EXPR["smug"]
    if t - s > d and d < 50:      # timed event expired -> smug
        return N.EXPR["smug"]
    return N.EXPR[nm]


def mouth_states(mix, n):
    hop = SR // FPS
    env = np.array([np.sqrt(np.mean(mix[i * hop:(i + 1) * hop + hop // 2] ** 2) + 1e-12) if i * hop < len(mix) else 0 for i in range(n)])
    ref = np.percentile(env[env > 0.01], 90) if (env > 0.01).any() else 1
    e = env / ref
    st = np.digitize(e, [0.12, 0.38, 0.70])
    pad = np.pad(st, 1, mode="edge")
    return np.median(np.stack([pad[:-2], pad[1:-1], pad[2:]]), axis=0).astype(int), np.clip(e, 0, 1.2)


def ease(x):
    x = min(max(x, 0), 1)
    return x * x * (3 - 2 * x)


def stream_mascot(proc, mix, n, timeline):
    v = CFG["variant"]
    ev = build_events(timeline)
    st, env = mouth_states(mix, n)
    MOUTHS = ["closed", "small", "open", "wide"]
    t_out = CFG["outro_start"] + 0.2
    cur = dict(N.EXPR["smug"])
    sm, bg = CFG["mascot_small"], CFG["mascot_big"]
    blink_times = [2.1 + 3.4 * i for i in range(40)]
    for f in range(n):
        t = f / FPS
        tgt = raw_pose(t, ev)
        a = 0.45
        cur = {k: cur[k] + (tgt[k] - cur[k]) * a for k in cur}
        p = dict(cur)
        spk = env[f] if st[f] > 0 else 0.0
        bounce = 2.0 * round(min(1, spk) * 3)          # quantised so layers can be cached
        p["bLy"] -= bounce; p["bRy"] -= bounce
        # scheduled blink (not during laugh/roll/squint) + natural idle tilt
        nb = min(abs(t - b) for b in blink_times)
        if nb < 0.09 and p["laugh"] < 0.3 and p["squint"] < 0.1:
            p["blink"] = 1.0 - nb / 0.09 * 0.15
        tilt = p["tilt"] + 2.2 * np.sin(t * 0.55) + 0.8 * np.sin(t * 1.3 + 1)
        mouth = MOUTHS[st[f]]
        im = N.compose(v, mouth, p)
        k = ease((t - t_out) / 0.7)
        size = int(sm + (bg - sm) * k)
        x = int(CFG["small_xy"][0] + (CFG["big_xy"][0] - CFG["small_xy"][0]) * k)
        y = int(CFG["small_xy"][1] + (CFG["big_xy"][1] - CFG["small_xy"][1]) * k)
        y += int(7 * np.sin(t * 2.6)) - int(12 * min(1, spk))
        im = im.rotate(tilt, resample=Image.BICUBIC, center=(N.RES / 2, N.RES * 0.78))
        im = im.resize((size, size), Image.LANCZOS)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.alpha_composite(im, (x, y))
        proc.stdin.write(layer.tobytes())
        if f % 150 == 0:
            print(f"  frame {f}/{n}  {time.time() - T0:.0f}s", flush=True)
    proc.stdin.close()


# ---------------------------------------------------------------- ffmpeg
def main():
    if "--skip-tts" in sys.argv and os.path.exists(os.path.join(WORK, "voice.wav")):
        d = json.load(open(os.path.join(WORK, "timeline.json")))
        timeline, total = d["timeline"], d["total"]
        mix, _ = sf.read(os.path.join(WORK, "voice.wav"), dtype="float32")
    else:
        timeline, mix, total = synth_all()
    write_ass(timeline, total)
    make_bg()
    ss, cl = CFG["clip_start"], CFG["clip_len"]
    fade = CFG.get("fade", 0.6)
    n = int(total * FPS)
    ass = os.path.join(WORK, "captions.ass")
    fc = (
        f"[0:v]trim=start={ss}:end={ss + cl},setpts=PTS-STARTPTS,fps={FPS},split[a][b];"
        f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:6,eq=brightness=-0.18[bg];"
        f"[b]scale={W}:-2[fg];[bg][fg]overlay=0:{CFG.get('clip_y', 400)},format=yuv420p[clipv];"
        f"[1:v]format=yuv420p,fps={FPS}[ob];"
        f"[clipv][ob]xfade=transition=fade:duration={fade}:offset={cl - fade}[base];"
        f"[base][2:v]overlay=0:0:format=auto[m];"
        f"[m]ass={ass}:fontsdir=/usr/share/fonts/opentype/fira[v];"
        f"[0:a]atrim=start={ss}:end={ss + cl},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=0.9[ca];"
        f"[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.6,asplit[v1][v2];"
        f"[ca][v1]sidechaincompress=threshold=0.015:ratio=12:attack=15:release=450:makeup=1[du];"
        f"[du]afade=t=out:st={cl - 0.6}:d=0.6[du2];"
        f"[du2][v2]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95,apad,atrim=0:{total:.3f}[a]"
    )
    out = os.path.join(HERE, CFG["out"])
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
           "-i", CFG["clip"],
           "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", os.path.join(WORK, "outro_bg.png"),
           "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", os.path.join(WORK, "voice.wav"),
           "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
           "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-maxrate", "8M", "-bufsize", "16M",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    stream_mascot(p, mix, n, timeline)
    p.wait()
    print(f"done {out} rc={p.returncode} total {total:.1f}s build {time.time() - T0:.0f}s")


if __name__ == "__main__":
    main()
