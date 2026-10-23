#!/usr/bin/env python3
"""Download and transcribe a campaign's supplied footage.

Usage (project venv python):
  prepare_campaign.py SLUG FRAMEIO_URL [--preview] [--keep-days N]

  --preview   download the SMALLEST proxy (for evaluating a campaign BEFORE joining; never post from it)
  (default)   download the Original (only run this after William has joined the campaign)

Writes under /home/williamdownard/openclaw-sites/clips-work/campaigns/SLUG/:
  source[-preview].mp4, source[-preview].json (transcript), info.json (duration, size, mode, timestamps).
Prints one summary line. Uses scripts/fetch_frameio.py (Playwright: opens the share and clicks Download
like a person) and pipeline/transcribe.py (local faster-whisper). Nothing leaves this machine.
"""
import json, os, re, subprocess, sys, time

HOME = os.path.expanduser("~")
VENV_PY = f"{HOME}/openclaw-sites/clips-venv/bin/python"
FFMPEG = f"{HOME}/openclaw-sites/bin/ffmpeg"
ROOT = "/home/williamdownard/.openclaw/workspace/projects/clips"
BASE = f"{HOME}/openclaw-sites/clips-work/campaigns"


def duration(path):
    p = subprocess.run([FFMPEG, "-hide_banner", "-i", path], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", p.stderr)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        sys.exit(__doc__)
    slug, url = args[0], args[1]
    preview = "--preview" in sys.argv
    out_dir = f"{BASE}/{slug}"
    os.makedirs(out_dir, exist_ok=True)
    tag = "source-preview" if preview else "source"
    video, transcript = f"{out_dir}/{tag}.mp4", f"{out_dir}/{tag}.json"
    t0 = time.time()
    if not os.path.exists(video):
        cmd = [VENV_PY, f"{ROOT}/scripts/fetch_frameio.py", url, video, "--debug-dir", f"{out_dir}/debug"]
        if preview:
            cmd += ["--smallest"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode or not os.path.exists(video):
            sys.exit("DOWNLOAD FAILED: " + (r.stdout + r.stderr)[-500:])
    if not os.path.exists(transcript):
        r = subprocess.run([VENV_PY, f"{ROOT}/pipeline/transcribe.py", video, transcript], capture_output=True, text=True)
        if r.returncode:
            sys.exit("TRANSCRIBE FAILED: " + (r.stdout + r.stderr)[-500:])
    info = {"slug": slug, "url": url, "mode": "preview" if preview else "original", "video": video,
            "transcript": transcript, "duration_s": duration(video),
            "size_mb": round(os.path.getsize(video) / 1e6, 1), "prepared_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    json.dump(info, open(f"{out_dir}/info-{tag}.json", "w"), indent=2)
    print(f"READY {slug} ({info['mode']}): {info['duration_s']:.0f}s, {info['size_mb']} MB, {time.time()-t0:.0f}s -> {out_dir}")


if __name__ == "__main__":
    main()
