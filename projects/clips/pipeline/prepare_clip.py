#!/usr/bin/env python3
"""Stage 1: create a job for one clip (guard check, copy, local transcript, job.json).

Usage:
  prepare_clip.py CLIP --streamer NAME --game GAME [--clip-url URL] [--permissions FILE]

Refuses unless the streamer is `approved` in permissions.md. Creates jobs/<id>/ with the clip,
transcript.json and job.json. The hook and caption are filled in by the writing step (see README.md),
then render_job.py renders the Short.
"""
import argparse, json, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from guard import is_approved, DEFAULT  # noqa: E402

VENV_PY = os.path.expanduser("~/openclaw-sites/clips-venv/bin/python")
JOBS = os.path.join(HERE, "jobs")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("--streamer", required=True)
    ap.add_argument("--game", required=True)
    ap.add_argument("--clip-url", default="")
    ap.add_argument("--permissions", default=DEFAULT)
    a = ap.parse_args()

    if not is_approved(a.streamer, a.permissions):
        sys.exit(f"REFUSED: {a.streamer} is not marked 'approved' in permissions.md. No clip will be processed.")
    os.makedirs(JOBS, exist_ok=True)
    jid = time.strftime("%Y%m%d-%H%M%S") + "-" + re.sub(r"[^a-z0-9]+", "", a.streamer.lower())
    d = os.path.join(JOBS, jid)
    os.makedirs(d)
    clip = os.path.join(d, "source" + os.path.splitext(a.clip)[1])
    shutil.copy(a.clip, clip)
    subprocess.run([VENV_PY, os.path.join(HERE, "transcribe.py"), clip, os.path.join(d, "transcript.json")], check=True)
    transcript = json.load(open(os.path.join(d, "transcript.json")))
    n = len(os.listdir(JOBS))
    job = {"id": jid, "streamer": a.streamer, "game": a.game, "clip_url": a.clip_url,
           "source": clip, "duration": transcript["duration"], "transcript": transcript["text"],
           "style": (n % 3) + 1, "hook": "", "caption": "", "status": "needs_writing"}
    json.dump(job, open(os.path.join(d, "job.json"), "w"), indent=2)
    print(f"job {jid} created ({job['duration']}s, style {job['style']}). Next: write hook + caption into {d}/job.json")


if __name__ == "__main__":
    main()
