#!/usr/bin/env python3
"""Visual check for moment candidates. Free (ffmpeg + numpy, no LLM). Posts/uploads/submits nothing.

  visual_check.py VIDEO_ID --moments out/ID.moments.json [--top 14] [--frames 8] [--keep] [--jobs 3]
  visual_check.py VIDEO_ID --sheets 8 [--rank out/ID.visual_rank.json]     # contact sheets for top survivors

Stage 1 (default): for each candidate window download ONLY that section at <=360p (video only), analyse ~4 fps grayscale
160x90 frames, save `--frames` evenly spaced jpg thumbnails to out/ID.vframes/, delete the section file (unless --keep),
write out/ID.visual.json. Features per window: motion (mean abs frame diff), p90 diff (motion bursts), scene changes,
black fraction, static fraction (near-zero pixel AND edge change), flat fraction (low-variance frames: fades, big flat UI),
longest static run (s), facecam corner motion ratio, visual_score (high = motion/scene change, low black/static).
Stage 2 (--sheets N): labelled contact sheet of N survivors from out/ID.visual_rank.json (written by moment_pick.py --visual).
"""
import argparse, concurrent.futures as cf, glob, json, os, re, shutil, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cut_moment as cm  # proxy + ffmpeg workaround + probe

W, H, FPS = 160, 90, 4


def fmt(t):
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def download(vid, s, e, dest_dir, port):
    tpl = os.path.join(dest_dir, f"w{int(s)}.%(ext)s")
    for old in glob.glob(os.path.join(dest_dir, f"w{int(s)}.*")):
        os.remove(old)
    for attempt in range(2):
        subprocess.run([cm.YTDLP, "--no-warnings", "--proxy", f"http://127.0.0.1:{port}", "--ignore-no-formats-error",
                        "--download-sections", f"*{s}-{e}", "--force-keyframes-at-cuts", "--ffmpeg-location", cm.FFMPEG,
                        "-f", "bv*[height<=360]/b[height<=360]/worst[height<=480]", "-o", tpl,
                        f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True, timeout=600)
        got = glob.glob(os.path.join(dest_dir, f"w{int(s)}.*"))
        if got:
            return got[0]
    return None


def read_gray(path):
    r = subprocess.run([cm.FFMPEG, "-loglevel", "error", "-i", path, "-an", "-vf", f"fps={FPS},scale={W}:{H},format=gray",
                        "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    n = len(a) // (W * H)
    return a[: n * W * H].reshape(n, H, W).astype(np.float32) / 255.0


def edges(f):
    gx = np.abs(np.diff(f, axis=2))[:, :-1, :]
    gy = np.abs(np.diff(f, axis=1))[:, :, :-1]
    return gx + gy


def features(g):
    n = len(g)
    if n < 6:
        return None
    d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))
    eg = edges(g)
    ed = np.abs(np.diff(eg, axis=0)).mean(axis=(1, 2))
    # robust to HUD/chat overlays: median pixel luma for black, 4x4 block diffs (75th pct) for static
    luma = np.median(g.reshape(n, -1), axis=1)
    sd = g.std(axis=(1, 2))
    black = luma < 0.05
    flat = sd < 0.05  # fades, solid colour, near-empty frames
    dgrid = np.abs(np.diff(g, axis=0))[:, : H // 4 * 4, : W // 4 * 4]
    blk = dgrid.reshape(n - 1, 4, H // 4, 4, W // 4).mean(axis=(2, 4)).reshape(n - 1, 16)
    egrid = np.abs(np.diff(eg, axis=0))[:, : (H - 1) // 4 * 4, : (W - 1) // 4 * 4]
    eblk = egrid.reshape(n - 1, 4, egrid.shape[1] // 4, 4, egrid.shape[2] // 4).mean(axis=(2, 4)).reshape(n - 1, 16)
    static = (np.percentile(blk, 75, axis=1) < 0.004) & (np.percentile(eblk, 75, axis=1) < 0.004)
    # longest run of static transitions, seconds
    run = best = 0
    for v in static:
        run = run + 1 if v else 0
        best = max(best, run)
    # scene cut: big jump relative to local flow, absolute floor to ignore ordinary driving motion
    med = float(np.median(d))
    cuts = int(np.sum((d > 0.15) & (d > 4 * med + 0.03)))
    # facecam inset: 4 corners, 24% x 26% each; keep the busiest corner vs the rest of the frame
    x1, y1 = int(W * 0.24), int(H * 0.26)
    dd = np.abs(np.diff(g, axis=0))
    corners = [float(sl.mean()) for sl in (dd[:, :y1, :x1], dd[:, :y1, W - x1:], dd[:, H - y1:, :x1], dd[:, H - y1:, W - x1:])]
    rest = float(d.mean()) + 1e-4
    cam = max(corners) / rest
    motion = float(d.mean())
    p90 = float(np.percentile(d, 90))
    bf, sf, ff = float(black.mean()), float(static.mean()), float(flat.mean())
    score = (0.6 * min(motion / 0.05, 2.0) + 0.4 * min(p90 / 0.12, 2.0) + 0.15 * min(cuts, 4)) * (1 - bf) * (1 - 0.8 * sf) * (1 - 0.4 * ff)
    return {"motion": round(motion, 4), "p90": round(p90, 4), "cuts": cuts, "black": round(bf, 3), "static": round(sf, 3),
            "flat": round(ff, 3), "static_run_s": round(best / FPS, 1), "cam_ratio": round(cam, 2),
            "cam_motion": round(max(corners), 4), "visual_score": round(float(score), 3)}


def sample_frames(path, dur, n, outdir, start):
    os.makedirs(outdir, exist_ok=True)
    names = []
    for i in range(n):
        t = dur * (i + 0.5) / n
        fp = os.path.join(outdir, f"{int(start)}_{i}.jpg")
        subprocess.run([cm.FFMPEG, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1", "-vf", "scale=320:-2", fp])
        names.append(os.path.basename(fp))
    return names


def analyse(vid, m, tmpdir, framedir, nframes, keep, port):
    s, e = m["start"], m["end"]
    t0 = time.time()
    path = download(vid, s, e, tmpdir, port)
    if not path:
        return {"start": s, "end": e, "error": "download failed"}
    size = os.path.getsize(path)
    g = read_gray(path)
    f = features(g)
    dur, res, _ = cm.probe(path)
    frames = sample_frames(path, dur or (e - s), nframes, framedir, s)
    if not keep:
        os.remove(path)
    if not f:
        return {"start": s, "end": e, "error": "too few frames"}
    f.update({"start": s, "end": e, "bytes": size, "secs": round(time.time() - t0, 1), "frames": frames})
    return f


def sheets(vid, n, out, rank_path):
    from PIL import Image, ImageDraw, ImageFont
    rank = json.load(open(rank_path or os.path.join(out, f"{vid}.visual_rank.json")))
    surv = [r for r in rank["ranked"] if not r.get("dropped")][:n]
    fdir = os.path.join(out, f"{vid}.vframes")
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    for i, r in enumerate(surv, 1):
        fr = r.get("frames") or []
        if not fr:
            continue
        cols, rows, tw, th = 4, (len(fr) + 3) // 4, 320, 180
        sheet = Image.new("RGB", (cols * tw, rows * th), "black")
        dur = r["end"] - r["start"]
        for k, name in enumerate(fr):
            im = Image.open(os.path.join(fdir, name)).resize((tw, th))
            x, y = (k % cols) * tw, (k // cols) * th
            sheet.paste(im, (x, y))
            d = ImageDraw.Draw(sheet)
            d.rectangle([x, y, x + 130, y + 22], fill="black")
            d.text((x + 3, y + 1), f"{fmt(r['start'] + dur * (k + 0.5) / len(fr))} (+{dur * (k + 0.5) / len(fr):.0f}s)", fill="yellow", font=font)
        p = os.path.join(out, f"{vid}.vsheet{i}.jpg")
        sheet.save(p, quality=85)
        print(f"SHEET {i} {p} start={r['start']:.0f} flags={r['sig']} vs={r['visual_score']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--moments")
    ap.add_argument("--top", type=int, default=14)
    ap.add_argument("--frames", type=int, default=8)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--sheets", type=int, default=0)
    ap.add_argument("--rank")
    a = ap.parse_args()
    vid = cm.video_id(a.video)
    if a.sheets:
        return sheets(vid, a.sheets, a.out, a.rank)
    mp = a.moments or os.path.join(a.out, f"{vid}.moments.json")
    moms = json.load(open(mp))["moments"][: a.top]
    tmpdir = os.path.join(a.out, f"{vid}.vtmp")
    framedir = os.path.join(a.out, f"{vid}.vframes")
    os.makedirs(tmpdir, exist_ok=True)
    port = cm.start_proxy()
    t0 = time.time()
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda m: analyse(vid, m, tmpdir, framedir, a.frames, a.keep, port), moms))
    if not a.keep:
        shutil.rmtree(tmpdir, ignore_errors=True)
    outp = os.path.join(a.out, f"{vid}.visual.json")
    json.dump({"video": vid, "fps": FPS, "windows": res, "runtime_s": round(time.time() - t0, 1)}, open(outp, "w"), separators=(",", ":"))
    tot = sum(r.get("bytes", 0) for r in res)
    print(f"{vid}: {len(res)} windows in {time.time() - t0:.0f}s, {tot / 1e6:.1f} MB downloaded (deleted={not a.keep})")
    for r in res:
        if "error" in r:
            print(f"  {fmt(r['start'])} ERROR {r['error']}")
        else:
            print(f"  {fmt(r['start']):>8} vs={r['visual_score']:.2f} mot={r['motion']:.3f} p90={r['p90']:.3f} cuts={r['cuts']} blk={r['black']:.2f} "
                  f"sta={r['static']:.2f} flat={r['flat']:.2f} run={r['static_run_s']}s cam={r['cam_ratio']}")
    print("wrote", outp)


if __name__ == "__main__":
    main()
