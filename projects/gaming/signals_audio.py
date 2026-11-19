#!/usr/bin/env python3
"""Audio-only loudness signals for a long VOD. Downloads bestaudio (no video), posts nothing, costs no credits.

  signals_audio.py VIDEO_ID_OR_URL [--hop 10] [--window 30] [--out DIR]

Decodes to 16 kHz mono PCM with ffmpeg (local file only) and per window computes:
  rms_db   RMS level (dBFS)
  jump_db  window RMS minus median RMS of the previous 2 min (sudden-jump signal)
  peak_db  peak minus the same local baseline
  shout    proxy for laughter/shouting: high short-term (50 ms) energy fraction x zero-crossing/spectral-flux lift
Each is z-scored against the video's own distribution (robust median/MAD), then combined: az = mean of top signals.
Honest limits: loudness cannot tell game explosions or music from a streamer; the shout proxy is energy + ZCR + flux only.
Writes OUT/<id>.audio.json: {"hop","window","windows":[[start, az, rms_z, jump_z, shout_z], ...]}.
"""
import argparse, glob, json, os, re, subprocess, sys, time
import numpy as np

YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"
FFMPEG = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 16000


def video_id(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|live/)([\w-]{11})", s)
    return m.group(1) if m else s.strip()


def fetch_audio(vid, out):
    os.makedirs(out, exist_ok=True)
    have = [p for p in glob.glob(os.path.join(out, f"{vid}.audio.*")) if not p.endswith((".json", ".part", ".pcm"))]
    if not have:
        subprocess.run([YTDLP, "--no-warnings", "-f", "bestaudio", "-o", os.path.join(out, "%(id)s.audio.%(ext)s"),
                        f"https://www.youtube.com/watch?v={vid}"], check=False)
        have = [p for p in glob.glob(os.path.join(out, f"{vid}.audio.*")) if not p.endswith((".json", ".part", ".pcm"))]
    return have[0] if have else None


def robust_z(x):
    med = np.median(x)
    mad = np.median(np.abs(x - med)) * 1.4826
    if mad < 1e-9:
        mad = np.std(x) + 1e-9
    return (x - med) / mad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--hop", type=int, default=10)
    ap.add_argument("--window", type=int, default=30)
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    a = ap.parse_args()
    vid = video_id(a.video)
    t0 = time.time()
    path = fetch_audio(vid, a.out)
    if not path:
        print(f"AUDIO_UNAVAILABLE {vid}: download failed")
        sys.exit(2)
    t1 = time.time()
    pcm = os.path.join(a.out, f"{vid}.audio.pcm")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", pcm], check=True)
    x = np.memmap(pcm, dtype=np.int16, mode="r")
    n = len(x)
    frame = SR // 20  # 50 ms frames
    nf = n // frame
    fr_per_hop = a.hop * 20
    fr_per_win = a.window * 20
    rms_f = np.empty(nf, dtype=np.float32)
    zcr_f = np.empty(nf, dtype=np.float32)
    flux_f = np.empty(nf, dtype=np.float32)
    prev = None
    CH = 20000  # frames per chunk
    for c0 in range(0, nf, CH):
        c1 = min(nf, c0 + CH)
        blk = np.asarray(x[c0 * frame:c1 * frame], dtype=np.float32).reshape(-1, frame) / 32768.0
        rms_f[c0:c1] = np.sqrt((blk ** 2).mean(1) + 1e-12)
        zcr_f[c0:c1] = (np.diff(np.signbit(blk), axis=1)).mean(1)
        spec = np.abs(np.fft.rfft(blk * np.hanning(frame), axis=1))
        spec = spec / (spec.sum(1, keepdims=True) + 1e-9)
        if prev is not None:
            first = np.abs(spec[0] - prev).sum()
        else:
            first = 0.0
        flux = np.concatenate([[first], np.abs(np.diff(spec, axis=0)).sum(1)])
        flux_f[c0:c1] = flux
        prev = spec[-1]
    db_f = 20 * np.log10(rms_f)
    starts = list(range(0, max(1, nf - fr_per_win + 1), fr_per_hop))
    rows = []
    rms_w = []
    peak_w = []
    hi_w = []
    zf_w = []
    for s in starts:
        sl = slice(s, s + fr_per_win)
        e = db_f[sl]
        rms_w.append(20 * np.log10(np.sqrt((rms_f[sl] ** 2).mean())))
        peak_w.append(np.percentile(e, 99))
        hi_w.append(0.0)  # filled after video baseline known
        zf_w.append((zcr_f[sl].mean(), flux_f[sl].mean()))
    rms_w = np.array(rms_w)
    peak_w = np.array(peak_w)
    # local baseline: median RMS of previous 2 min (12 hops of 10 s scaled by hop)
    back = max(1, 120 // a.hop)
    base = np.array([np.median(rms_w[max(0, i - back):i]) if i > 0 else rms_w[0] for i in range(len(rms_w))])
    jump = rms_w - base
    peakj = peak_w - base
    # shout proxy: fraction of 50 ms frames above the video's 90th-percentile level, lifted by ZCR and spectral flux z
    thr = np.percentile(db_f, 90)
    loud_frac = np.array([(db_f[s:s + fr_per_win] > thr).mean() for s in starts])
    zcr_z = robust_z(np.array([v[0] for v in zf_w]))
    flux_z = robust_z(np.array([v[1] for v in zf_w]))
    shout = loud_frac * (1.0 + 0.5 * np.clip(zcr_z, 0, 3) + 0.5 * np.clip(flux_z, 0, 3))
    z_rms, z_jump, z_peakj, z_shout = robust_z(rms_w), robust_z(jump), robust_z(peakj), robust_z(shout)
    az = (z_rms + z_jump + 0.5 * z_peakj + z_shout) / 3.5
    for i, s in enumerate(starts):
        rows.append([s // 20, round(float(az[i]), 2), round(float(z_rms[i]), 2), round(float(z_jump[i]), 2), round(float(z_shout[i]), 2)])
    outp = os.path.join(a.out, f"{vid}.audio.json")
    json.dump({"video": vid, "hop": a.hop, "window": a.window, "duration": n / SR,
               "cols": ["start", "az", "rms_z", "jump_z", "shout_z"], "windows": rows}, open(outp, "w"), separators=(",", ":"))
    os.remove(pcm)
    sz = os.path.getsize(path) / 1e6
    print(f"AUDIO {vid}: {len(rows)} windows, {n / SR / 60:.0f} min; download {t1 - t0:.0f}s ({sz:.0f} MB), compute {time.time() - t1:.0f}s")
    print("wrote", outp)


if __name__ == "__main__":
    main()
