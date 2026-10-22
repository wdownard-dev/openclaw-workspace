#!/usr/bin/env python3
"""Stage 5: upload a rendered job to YouTube after William's explicit approval.

Usage: publish_job.py JOB_DIR --approved-by-william [--privacy private|unlisted|public]

Refuses without the explicit flag, without a rendered short, or if the streamer is not `approved`.
Default privacy is private (uploads from an unaudited API project are locked private anyway).
Run it only after William has said yes to this specific preview.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from guard import is_approved  # noqa: E402


def main():
    if len(sys.argv) < 3 or "--approved-by-william" not in sys.argv:
        sys.exit("REFUSED: pass --approved-by-william only after William approved this exact preview.\n" + __doc__)
    d = sys.argv[1]
    privacy = sys.argv[sys.argv.index("--privacy") + 1] if "--privacy" in sys.argv else "private"
    jp = os.path.join(d, "job.json")
    job = json.load(open(jp))
    if job.get("status") not in ("rendered", "previewed"):
        sys.exit(f"REFUSED: job status is {job.get('status')}, expected rendered/previewed.")
    if not is_approved(job["streamer"]):
        sys.exit(f"REFUSED: {job['streamer']} is not 'approved'.")
    up = os.path.join(HERE, "..", "scripts", "upload.py")
    r = subprocess.run([sys.executable, "-I", up, job["output"], "--title", job["title"],
                        "--description", job["description"], "--privacy", privacy, "--yes"],
                       capture_output=True, text=True)
    print(r.stdout + r.stderr)
    if r.returncode == 0:
        job["status"] = "uploaded"
        job["upload_log"] = r.stdout.strip()[-400:]
        json.dump(job, open(jp, "w"), indent=2)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
