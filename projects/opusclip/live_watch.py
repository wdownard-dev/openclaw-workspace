#!/usr/bin/env python3
"""Turn an official live stream into clips as fast as OpusClip allows.

OpusClip can only process a finished video, so this waits for the stream to end, submits the YouTube
URL straight away, waits for OpusClip to finish, then lists the clips (with scores) for screening.
Nothing is posted here. Run it as a background exec: it prints progress lines and exits when clips are ready.

  live_watch.py VIDEO_ID [--min 20] [--max 45] [--keywords a,b,c] [--max-wait-min 240] [--dry-run]

Needs OPUSCLIP_API_KEY (present when run through the OpenClaw exec tool).
"""
import argparse, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"


def status(vid):
    r = subprocess.run([YTDLP, "--no-warnings", "--skip-download", "--print",
                        "%(live_status)s|%(duration)s|%(channel)s|%(title)s", f"https://www.youtube.com/watch?v={vid}"],
                       capture_output=True, text=True, timeout=90)
    line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    p = line.split("|", 3)
    return (p + ["", "", "", ""])[:4] if line else ["error", "", "", (r.stderr or "")[-120:]]


def opus(*args):
    p = subprocess.run([sys.executable, os.path.join(HERE, "opus.py"), *args], capture_output=True, text=True, timeout=120)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def main():
    a = argparse.ArgumentParser()
    a.add_argument("video")
    a.add_argument("--min", type=int, default=20)
    a.add_argument("--max", type=int, default=45)
    a.add_argument("--keywords", default="")
    a.add_argument("--max-wait-min", type=int, default=240)
    a.add_argument("--dry-run", action="store_true")
    a = a.parse_args()
    t0 = time.time()
    seen = None
    while True:
        st, dur, ch, title = status(a.video)
        if st != seen:
            print(f"[{time.strftime('%H:%M:%S')}] {ch} | {title[:70]} | status {st}", flush=True)
            seen = st
        if st in ("was_live", "not_live") and dur not in ("", "NA", "None"):
            break
        if time.time() - t0 > a.max_wait_min * 60:
            print("TIMEOUT: stream did not finish in time", flush=True)
            return 2
        time.sleep(45)
    mins = max(1, int(float(dur) // 60))
    print(f"STREAM_ENDED {mins} min source (about {mins} OpusClip credits)", flush=True)
    if a.dry_run:
        print("DRY RUN: would submit now", flush=True)
        return 0
    cmd = ["submit", f"https://www.youtube.com/watch?v={a.video}", "--min", str(a.min), "--max", str(a.max)]
    if a.keywords:
        cmd += ["--keywords", a.keywords]
    rc, out, err = opus(*cmd)
    m = re.search(r'"projectId":\s*"([^"]+)"', out)
    if rc != 0 or not m:
        print(f"SUBMIT_FAILED {err or out[:200]}", flush=True)
        return 1
    proj = m.group(1)
    print(f"SUBMITTED project {proj} at {time.strftime('%H:%M:%S')}", flush=True)
    t1 = time.time()
    while time.time() - t1 < 40 * 60:
        rc, out, err = opus("status", proj)
        if out.startswith("COMPLETE"):
            break
        if "FAIL" in out.upper() or "ERROR" in out.upper():
            print(f"OPUS_FAILED {out[:200]}", flush=True)
            return 1
        time.sleep(30)
    else:
        print(f"OPUS_SLOW project {proj} still processing after 40 min", flush=True)
        return 2
    rc, out, err = opus("clips", proj)
    print(f"CLIPS_READY project {proj} after {int(time.time() - t0) // 60} min total, "
          f"{int(time.time() - t1) // 60} min in OpusClip\n{out}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
