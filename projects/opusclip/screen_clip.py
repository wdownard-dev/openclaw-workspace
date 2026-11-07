#!/usr/bin/env python3
"""Screening helper: everything needed to approve or reject a clip before it posts.

  screen_clip.py PROJECT_ID CLIP_ID [--frames 6]

Prints the clip's title, score, length, transcript, OpusClip's description and a list of automatic text flags
(sensitive words, 911/dispatch/scream/blood words, motive words). Downloads the rendered clip and extracts evenly
spaced frames to screens/<clip>/frame_N.jpg: LOOK AT EVERY FRAME with the image viewer before posting. A clip with
frames nobody looked at does not post. Blood, gore, graphic injury or a sure takedown = reject; a person shot or down
without blood, 911 and distress audio are allowed (William, 2026-11-06). Needs OPUSCLIP_API_KEY (present when run through the OpenClaw exec tool).
"""
import json, os, re, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import opus  # noqa: E402

FFMPEG = "/home/williamdownard/openclaw-sites/bin/ffmpeg"
FLAGS = {
    "sensitive": r"\b(child sex|child porn\w*|sexual abuse|csam|rape[ds]?|sexual assault|suicide|molest\w*|minor)\b",
    "distress audio": r"\b(911|dispatch(?:er)?|scream\w*|screaming|begging|help me|please don't|shots? fired)\b",
    "graphic": r"\b(blood|bleeding|body|bodies|dead body|corpse|gunshot wound|shot (?:in|to)|dying|dies)\b",
    "motive stated": r"\b(because|motivated|motive|angry over|over a debt|over the debt)\b",
    "naming a person": r"\b(suspect|gunman|shooter|killer|victim)\b.{0,40}\b(named|identified as|[A-Z][a-z]+ [A-Z][a-z]+)\b",
    "allegation": r"\b(allegedly|accused|charged|arrested)\b",
}


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    project, clip = sys.argv[1], sys.argv[2]
    n = int(sys.argv[sys.argv.index("--frames") + 1]) if "--frames" in sys.argv else 6
    res = opus.call("GET", f"/api/exportable-clips?q=findByProjectId&projectId={project}")
    res = res if isinstance(res, list) else res.get("data", [])
    c = next((x for x in res if x["id"] == clip or x["id"].endswith("." + clip.split(".")[-1])), None)
    if not c:
        sys.exit(f"clip {clip} not found in project {project}")
    text = c.get("text", "") or ""
    out = {"clip": c["id"], "title": c.get("title"), "score": c.get("score"), "seconds": round(c["durationMs"] / 1000),
           "description": c.get("description"), "transcript": text.replace(" __silence", ""),
           "text_flags": {k: sorted(set(m.group(0) for m in re.finditer(rx, text, re.I))) for k, rx in FLAGS.items()
                          if re.search(rx, text, re.I)}}
    d = os.path.join(HERE, "screens", c["id"].split(".")[-1])
    os.makedirs(d, exist_ok=True)
    mp4 = os.path.join(d, "clip.mp4")
    urllib.request.urlretrieve(c["uriForExport"], mp4)
    secs = max(c["durationMs"] / 1000, 1)
    frames = []
    for i in range(n):
        t = secs * (i + 0.5) / n
        f = os.path.join(d, f"frame_{i + 1}.jpg")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", "-q:v", "3", f],
                       check=False, timeout=60)
        if os.path.exists(f):
            frames.append(f)
    out["frames"] = frames
    out["reminder"] = "View every frame. Reject on visible blood, gore or graphic injury, or content that is a sure YouTube takedown. A person shot or down without blood, 911 or distress audio are allowed (William, 11/6): report them, do not reject."
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
