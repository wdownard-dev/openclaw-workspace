#!/usr/bin/env python3
"""Upload built guide Shorts PRIVATE with publishAt + thumbnail. Usage: upload_queue.py ID@ISO_TIME [ID@ISO_TIME ...]
Stops at the first failure (never retries, never public, never deletes). Logs to out/upload_queue.log."""
import re, shutil, subprocess, sys, datetime
log = open("out/upload_queue.log", "a")
def say(m):
    m = f"{datetime.datetime.now().isoformat(timespec='seconds')} {m}"; print(m); log.write(m + "\n"); log.flush()
for item in sys.argv[1:]:
    sid, at = item.split("@", 1)
    r = subprocess.run(["python3", "guide_make.py", sid, "upload", "--publish-at", at], capture_output=True, text=True)
    out = r.stdout + r.stderr
    m = re.search(r"video id: (\S+)", out)
    if r.returncode != 0 or not m:
        say(f"STOP {sid}: {out.strip()[-400:]}"); sys.exit(1)
    vid = m.group(1); say(f"UPLOADED {sid} -> {vid} publishAt {at}")
    shutil.copy(f"out/thumbs/{sid}.png", f"out/thumbs/{vid}.png")
    t = subprocess.run(["python3", "apply_thumbs.py", vid], capture_output=True, text=True)
    say(f"THUMB {vid}: {(t.stdout + t.stderr).strip()[-200:]}")
