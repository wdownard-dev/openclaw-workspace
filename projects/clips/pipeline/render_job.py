#!/usr/bin/env python3
"""Stage 3: render a job's Short once hook and caption are written.

Usage: render_job.py JOB_DIR
Reads job.json, re-checks permission, renders short.mp4 with format_short.py, writes the YouTube
title/description into job.json and sets status to `rendered`.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from guard import is_approved  # noqa: E402


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    d = sys.argv[1]
    jp = os.path.join(d, "job.json")
    job = json.load(open(jp))
    perms = sys.argv[sys.argv.index("--permissions") + 1] if "--permissions" in sys.argv else None
    if not (is_approved(job["streamer"], perms) if perms else is_approved(job["streamer"])):
        sys.exit(f"REFUSED: {job['streamer']} is no longer 'approved'.")
    if not job["hook"].strip():
        sys.exit("hook is empty: write the hook and caption first.")
    out = os.path.join(d, "short.mp4")
    subprocess.run([sys.executable, os.path.join(HERE, "format_short.py"), job["source"], out,
                    "--hook", job["hook"], "--caption", job["caption"], "--credit", job["streamer"],
                    "--style", str(job["style"])], check=True)
    desc = job["caption"].strip()
    desc += f"\n\nClip from {job['streamer']}" + (f": {job['clip_url']}" if job["clip_url"] else "")
    desc += "\nPosted with the streamer's permission.\n#Shorts"
    job.update(output=out, title=job["hook"].strip()[:95], description=desc, status="rendered")
    json.dump(job, open(jp, "w"), indent=2)
    print(f"rendered {out}\ntitle: {job['title']}")


if __name__ == "__main__":
    main()
