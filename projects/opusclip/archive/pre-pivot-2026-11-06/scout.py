#!/usr/bin/env python3
"""Find new long-form uploads from the channels in channels.txt.

Reads handles (one per line, # comments ok), lists each channel's newest uploads with yt-dlp
(metadata only, no downloads), and appends videos not seen before to queue.jsonl.
The first run for a channel only records what is already there (no backfill) unless --backfill.

  scout.py            # scan, print new candidates
  scout.py --backfill # treat the current newest uploads as new on the first run
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
YTDLP = "/home/williamdownard/openclaw-sites/ytdlp-venv/bin/yt-dlp"
MIN_SECONDS = 600
PER_CHANNEL = 5
STATE = os.path.join(HERE, "state.json")
QUEUE = os.path.join(HERE, "queue.jsonl")


def ytdlp(args, timeout=90):
    r = subprocess.run([YTDLP, "--no-warnings", *args], capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip().splitlines()


def main():
    backfill = "--backfill" in sys.argv
    state = json.load(open(STATE)) if os.path.exists(STATE) else {"channels": {}, "seen": []}
    seen = set(state["seen"])
    handles = [l.strip() for l in open(os.path.join(HERE, "channels.txt"))
               if l.strip() and not l.startswith("#")]
    found = []
    for h in handles:
        try:
            rows = ytdlp(["--flat-playlist", "--playlist-end", str(PER_CHANNEL), "--print",
                          "%(id)s\t%(duration)s\t%(view_count)s\t%(title)s",
                          f"https://www.youtube.com/@{h}/videos"])
        except subprocess.TimeoutExpired:
            print(f"timeout: {h}", file=sys.stderr)
            continue
        first_run = h not in state["channels"]
        state["channels"][h] = int(time.time())
        for row in rows:
            vid, dur, views, title = (row.split("\t") + ["", "", "", ""])[:4]
            if vid in seen:
                continue
            seen.add(vid)
            if first_run and not backfill:
                continue
            if not dur.isdigit() or int(dur) < MIN_SECONDS:
                continue
            found.append({"id": vid, "channel": h, "duration": int(dur), "title": title,
                          "url": f"https://www.youtube.com/watch?v={vid}",
                          "found_at": int(time.time()), "status": "new"})
    state["seen"] = sorted(seen)
    json.dump(state, open(STATE, "w"))
    with open(QUEUE, "a") as q:
        for f in found:
            q.write(json.dumps(f) + "\n")
    for f in found:
        print(f"NEW {f['channel']} | {f['duration']//60} min | {f['title']} | {f['url']}")
    print(f"scanned {len(handles)} channels, {len(found)} new long-form", file=sys.stderr)


if __name__ == "__main__":
    main()
