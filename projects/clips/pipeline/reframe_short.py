#!/usr/bin/env python3
"""REFRAME layout: turn a 16:9 clip into a full-frame 1080x1920 short by cropping a 9:16 window that follows the speaker.

Not the control arm: `format_short.py` (blurred band) is untouched. This file is the second layout in Test 1
(strategy/2026-10-30-test1-plan.md). Only crops, scales, cuts and text are used: no mirroring, no speed or pitch change,
no noise, no outside visuals or music (pipeline/README.md bans disguising footage).

Two subcommands:

  analyze CUT.mp4 [--speakers "0-5.2:david,5.2-9:host"] [--out plan.json] [--sheet shots.jpg]
      Detects the source's own shots, finds faces in each (OpenCV YuNet), labels the one wearing the green cap "david"
      (the other face is "host") and prints/writes a DRAFT crop plan. A human must view the draft against frames and edit it (speaker hints from `--motion` are weak; check mouths in frames):
      shots without faces (overhead card cams, b-roll) get centre framing and are flagged "review". Needs the reframe venv
      (~/openclaw-sites/reframe-venv, opencv-python-headless) and the YuNet model (~/openclaw-sites/reframe-models/yunet.onnx).

  render CUT.mp4 OUT.mp4 --plan plan.json --hook "text" [--caption "text"] [--style 1|2|3]
      Renders the plan. Needs only ffmpeg. CUT must be the 4K (or any 16:9) clip cut from the original, with its audio; the
      audio is copied as-is (re-encoded to AAC with the cut's own fade).

Plan = JSON list of entries that tile the clip from 0 to its duration, in order:
  {"t0": 0.0, "t1": 3.2, "cx": 0.31, "cy": 0.5, "zoom": 1.0, "cx_to": 0.31, "cy_to": 0.5, "zoom_to": 1.0, "why": "..."}
  cx, cy: centre of the window as a fraction of the source frame (0-1). zoom: 1.0 = full source height (a 2160 -> 1215 px wide
  window of a 4K frame); 1.25 = 25% punch-in. *_to give a linear move to a new centre/zoom over the entry (a pan or a push);
  omit them for a static entry. Hard punch-ins are just two entries with different zoom. The window is clamped inside the frame.
Text: the same ASS hook (first 4 s) and caption (from 1 s) as format_short.py, same fonts, sizes and colours. Position differs
because the picture is full-frame: faces sit in the top third, so the hook goes above the caption in the lower third
(HOOK_MARGIN_V / CAP_MARGIN_V below) instead of over a blurred band.
"""
import argparse, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from format_short import STYLES, ass_time, esc, wrap, duration  # noqa: E402  (text helpers only; band path unchanged)

FFMPEG = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")
MODEL = os.path.expanduser("~/openclaw-sites/reframe-models/yunet.onnx")
HOOK_MARGIN_V = 560  # px from the bottom edge; hook sits above the caption
CAP_MARGIN_V = 300   # same as the band layout


def probe(path):
    err = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Video:.*?, (\d{3,5})x(\d{3,5})", err)
    f = re.search(r"(\d+(?:\.\d+)?) fps", err)
    return int(m[1]), int(m[2]), float(f[1])


def ev(v, lo, hi):
    return max(lo, min(hi, v))


def segment_filter(i, e, fps, sw, sh):
    """One plan entry -> filter chain ending in [s<i>] at 1080x1920."""
    a, b = round(e["t0"] * fps), round(e["t1"] * fps)
    z0 = float(e.get("zoom", 1.0))
    z1 = float(e.get("zoom_to", z0))
    cx0, cy0 = float(e.get("cx", 0.5)), float(e.get("cy", 0.5))
    cx1, cy1 = float(e.get("cx_to", cx0)), float(e.get("cy_to", cy0))
    head = f"[v{i}]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS"
    ramp = (cx0, cy0, z0) != (cx1, cy1, z1)
    base_h = sh
    base_w = int(round(base_h * 9 / 16 / 2)) * 2
    if not ramp:
        h = int(round(sh / z0 / 2)) * 2
        w = int(round(h * 9 / 16 / 2)) * 2
        x = ev(cx0 * sw - w / 2, 0, sw - w)
        y = ev(cy0 * sh - h / 2, 0, sh - h)
        return f"{head},crop={w}:{h}:{x:.1f}:{y:.1f},scale=1080:1920:flags=lanczos,setsar=1[s{i}]"
    d = max((b - a) / fps, 0.04)
    k = f"min(1,t/{d:.4f})"
    zx = f"({z0}+({z1}-{z0})*{k})"
    cx = f"({cx0}+({cx1}-{cx0})*{k})"
    cy = f"({cy0}+({cy1}-{cy0})*{k})"
    return (f"{head},scale=w='trunc(iw*{zx}/2)*2':h='trunc(ih*{zx}/2)*2':eval=frame:flags=bicubic,"
            f"crop={base_w}:{base_h}:x='max(0,min(iw-ow,{cx}*iw-ow/2))':y='max(0,min(ih-oh,{cy}*ih-oh/2))',"
            f"scale=1080:1920:flags=lanczos,setsar=1[s{i}]")


def check_plan(plan, dur, fps):
    if not plan:
        sys.exit("plan is empty")
    if abs(plan[0]["t0"]) > 1e-6:
        sys.exit("plan must start at t0=0")
    for p, q in zip(plan, plan[1:]):
        if abs(p["t1"] - q["t0"]) > 1e-6:
            sys.exit(f"plan gap/overlap between {p['t1']} and {q['t0']}")
    if abs(plan[-1]["t1"] - dur) > 0.15:
        sys.exit(f"plan ends at {plan[-1]['t1']} but clip is {dur:.3f}s")
    plan[-1]["t1"] = dur  # the cut's length is rounded to whole frames; let the last entry run to the end
    for e in plan:
        if e["t1"] - e["t0"] < 2 / fps:
            sys.exit(f"plan entry {e} is shorter than 2 frames")


def render(cut, out, plan, hook, caption, style):
    sw, sh, fps = probe(cut)
    dur = duration(cut)
    check_plan(plan, dur, fps)
    font, hsz, hcol, csz, ccol = STYLES[style]
    events = [f"Dialogue: 0,{ass_time(0)},{ass_time(min(4, dur))},Hook,,0,0,0,,{wrap(esc(hook), 22)}"]
    if caption:
        events.append(f"Dialogue: 0,{ass_time(min(1.0, dur))},{ass_time(dur)},Cap,,0,0,0,,{wrap(esc(caption), 34)}")
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Hook,{font},{hsz},{hcol},&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,2,2,60,60,{HOOK_MARGIN_V},1
Style: Cap,{font},{csz},{ccol},&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5,2,2,60,60,{CAP_MARGIN_V},1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
""" + "\n".join(events) + "\n"
    n = len(plan)
    with tempfile.TemporaryDirectory() as td:
        ass_path = os.path.join(td, "t.ass")
        open(ass_path, "w", encoding="utf-8").write(ass)
        parts = [f"[0:v]split={n}" + "".join(f"[v{i}]" for i in range(n))]
        parts += [segment_filter(i, e, fps, sw, sh) for i, e in enumerate(plan)]
        parts.append("".join(f"[s{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,"
                     f"subtitles={ass_path}:fontsdir=/usr/share/fonts/truetype/dejavu[v]")
        fg = ";".join(parts)
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", cut, "-filter_complex", fg, "-map", "[v]", "-map", "0:a?",
               "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
               "-t", f"{dur:.3f}", "-movflags", "+faststart", out]
        subprocess.run(cmd, check=True)
    print(f"wrote {out} ({dur:.1f}s, {n} crop entries, reframe from {sw}x{sh})")


# ---------------------------------------------------------------- analysis (draft plan)

def detect_shots(cut, thresh=0.3, min_len=0.4):
    err = subprocess.run([FFMPEG, "-i", cut, "-vf", f"scale=480:-2,select='gt(scene,{thresh})',showinfo", "-an", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", err)]
    dur = duration(cut)
    bounds = [0.0]
    for c in cuts:
        if c - bounds[-1] >= min_len and dur - c >= min_len:
            bounds.append(c)
    bounds.append(dur)
    return list(zip(bounds[:-1], bounds[1:]))


def mouth_motion(cap, cv2, np, report, fps, W, H, bin_s=0.5):
    """Active-speaker heuristic for shots with 2+ faces: frame-difference energy in the lower half of each face box,
    sampled at ~10 fps and summed per bin. A speaking mouth moves more than a listening one; head or hand motion also counts,
    so the result is a hint to check against the transcript, not a verdict. Adds shot['motion'] = {label: [energy per bin]}
    and shot['auto_speaker'] = [(t0, t1, label)] with a 0.6 s switch hysteresis."""
    step = max(1, int(round(fps / 10)))
    for s in report:
        tr = [t for t in s["tracks"]]
        if len(tr) < 2:
            continue
        prev = {}
        energy = {t["label"] + "@" + str(t["x"]): {} for t in tr}
        f0, f1 = int(s["t0"] * fps), int(s["t1"] * fps)
        for f in range(f0, f1, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, f)
            ok, frame = cap.read()
            if not ok:
                continue
            tt = f / fps
            b = int((tt - s["t0"]) / bin_s)
            for t in tr:
                key = t["label"] + "@" + str(t["x"])
                fw = t["w"] * W
                x0, x1 = int(max(0, t["x"] * W - fw * 0.7)), int(min(W, t["x"] * W + fw * 0.7))
                y0, y1 = int(t["y"] * H), int(min(H, t["y"] * H + fw * 0.9))
                roi = cv2.cvtColor(frame[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
                if roi.size == 0:
                    continue
                roi = cv2.resize(roi, (48, 32)).astype(np.float32)
                if key in prev:
                    energy[key][b] = energy[key].get(b, 0.0) + float(np.abs(roi - prev[key]).mean())
                prev[key] = roi
        nb = int((s["t1"] - s["t0"]) / bin_s) + 1
        s["motion"] = {k: [round(v.get(i, 0.0), 1) for i in range(nb)] for k, v in energy.items()}
        keys = list(energy)
        cur, run, spans = None, 0, []
        for i in range(nb):
            vals = {k: s["motion"][k][i] for k in keys}
            top = max(vals, key=vals.get)
            if cur is None:
                cur = top
            elif top != cur and vals[top] > 1.4 * max(vals[cur], 1e-6):
                run += 1
                if run >= 2:
                    cur, run = top, 0
            else:
                run = 0
            spans.append(cur)
        out, start = [], 0
        for i in range(1, nb + 1):
            if i == nb or spans[i] != spans[start]:
                out.append((round(s["t0"] + start * bin_s, 2), round(min(s["t1"], s["t0"] + i * bin_s), 2), spans[start].split("@")[0]))
                start = i
        s["auto_speaker"] = out


def analyze(cut, speakers, out_json, sheet, motion=False):
    try:
        import cv2
        import numpy as np
    except ImportError:
        sys.exit("analyze needs the reframe venv: ~/openclaw-sites/reframe-venv/bin/python pipeline/reframe_short.py analyze ...")
    shots = detect_shots(cut)
    cap = cv2.VideoCapture(cut)
    fps = cap.get(cv2.CAP_PROP_FPS)
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale = 960 / W
    det = cv2.FaceDetectorYN.create(MODEL, "", (960, int(H * scale)), 0.6, 0.3, 5000)

    def is_green_cap(img, x, y, w, h):
        y0, y1 = max(0, int(y - 0.7 * h)), max(1, int(y + 0.15 * h))
        x0, x1 = max(0, int(x)), min(img.shape[1], int(x + w))
        roi = img[y0:y1, x0:x1]
        if roi.size == 0:
            return False
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        m = (hsv[..., 0] > 40) & (hsv[..., 0] < 90) & (hsv[..., 1] > 60) & (hsv[..., 2] > 25)
        return m.mean() > 0.22

    report = []
    for (t0, t1) in shots:
        tracks = []
        step = max(1, int(fps / 3))
        f0, f1 = int((t0 + 0.1) * fps), int((t1 - 0.1) * fps)
        for f in range(f0, max(f0 + 1, f1), step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, f)
            ok, frame = cap.read()
            if not ok:
                continue
            small = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            _, faces = det.detect(small)
            for r in (faces if faces is not None else []):
                x, y, w, h = [float(v) for v in r[:4]]
                cx, cy = (x + w / 2) / small.shape[1], (y + h / 2) / small.shape[0]
                green = is_green_cap(small, x, y, w, h)
                for tr in tracks:
                    if abs(tr["x"] - cx) < 0.08 and abs(tr["y"] - cy) < 0.15:
                        k = tr["n"]
                        tr["x"] = (tr["x"] * k + cx) / (k + 1)
                        tr["y"] = (tr["y"] * k + cy) / (k + 1)
                        tr["w"] = (tr["w"] * k + w / small.shape[1]) / (k + 1)
                        tr["green"] += green
                        tr["n"] += 1
                        break
                else:
                    tracks.append({"x": cx, "y": cy, "w": w / small.shape[1], "green": int(green), "n": 1})
        tracks = [t for t in tracks if t["n"] >= 2]
        for t in tracks:
            t["label"] = "david" if t["green"] / t["n"] > 0.5 else "host"
            t["x"], t["y"], t["w"] = round(t["x"], 3), round(t["y"], 3), round(t["w"], 3)
            del t["green"]
        tracks.sort(key=lambda t: t["x"])
        report.append({"t0": round(t0, 3), "t1": round(t1, 3), "tracks": tracks})

    if motion:
        mouth_motion(cap, cv2, np, report, fps, W, H)
    spk = []
    for part in (speakers or "").split(","):
        if part.strip():
            span, who = part.split(":")
            a, b = span.split("-")
            spk.append((float(a), float(b), who.strip()))

    def who_at(t):
        for a, b, w in spk:
            if a <= t < b:
                return w
        return "auto"

    plan = []
    for s in report:
        cuts_ = sorted({s["t0"], s["t1"]} | {round(a, 3) for a, b, w in spk if s["t0"] < a < s["t1"]})
        for a, b in zip(cuts_[:-1], cuts_[1:]):
            want = who_at((a + b) / 2)
            trk = [t for t in s["tracks"] if t["label"] == want] or sorted(s["tracks"], key=lambda t: -t["w"])[:1]
            if trk:
                t = trk[0]
                plan.append({"t0": a, "t1": b, "cx": t["x"], "cy": 0.5, "zoom": 1.0, "why": f"{want}->{t['label']} face @{t['x']}"})
            else:
                plan.append({"t0": a, "t1": b, "cx": 0.5, "cy": 0.5, "zoom": 1.0, "why": "no face: REVIEW (centre default)"})
    for s in report:
        print(f"shot {s['t0']:6.2f}-{s['t1']:6.2f}  " + ("; ".join(f"{t['label']}@x{t['x']} y{t['y']} w{t['w']}" for t in s["tracks"]) or "no faces"))
        if s.get("auto_speaker"):
            print("     mouth-motion speaker hint: " + ", ".join(f"{a:.1f}-{b:.1f}:{w}" for a, b, w in s["auto_speaker"]))
    if out_json:
        json.dump({"shots": report, "plan": plan}, open(out_json, "w"), indent=1)
        print(f"wrote {out_json}")
    if sheet:
        mids = [(s["t0"] + s["t1"]) / 2 for s in report]
        cols = 6
        tiles = []
        for i, t in enumerate(mids):
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
            ok, fr = cap.read()
            if not ok:
                continue
            th = cv2.resize(fr, (320, 180))
            cv2.putText(th, f"{i}: {report[i]['t0']:.1f}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            tiles.append(th)
        while len(tiles) % cols:
            tiles.append(np.zeros((180, 320, 3), np.uint8))
        rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
        cv2.imwrite(sheet, np.vstack(rows))
        print(f"wrote {sheet}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze")
    a.add_argument("cut")
    a.add_argument("--speakers", default="")
    a.add_argument("--out")
    a.add_argument("--sheet")
    a.add_argument("--motion", action="store_true", help="add the mouth-motion speaker hint (slow, unreliable: it misread a smirking listener as the speaker)")
    r = sub.add_parser("render")
    r.add_argument("cut")
    r.add_argument("output")
    r.add_argument("--plan", required=True)
    r.add_argument("--hook", required=True)
    r.add_argument("--caption", default="")
    r.add_argument("--style", type=int, default=1, choices=[1, 2, 3])
    n = ap.parse_args()
    if n.cmd == "analyze":
        analyze(n.cut, n.speakers, n.out, n.sheet, n.motion)
    else:
        plan = json.load(open(n.plan))
        render(n.cut, n.output, plan["plan"] if isinstance(plan, dict) else plan, n.hook, n.caption, n.style)


if __name__ == "__main__":
    main()
