#!/usr/bin/env python3
"""One command from a clip spec to scheduled, logged posts: cut -> format -> verify -> thumbnail -> host -> schedule -> log.

Usage:
  clip_job.py SPEC.json                       run every stage up to and including log (resumes where it stopped)
  clip_job.py SPEC.json --until verify        stop after a stage (cut, format, verify, thumbnail, host, schedule, log)
  clip_job.py SPEC.json --dry-run             print what would happen, change nothing external (no upload, no Buffer call)
  clip_job.py SPEC.json --unschedule          delete this clip's scheduled Buffer posts (only status=scheduled) and clear state
  clip_job.py SPEC.json --status              show state
  clip_job.py SPEC.json --approve CHECKS      Morpheus's review gate (see below); required before host/schedule

Spec (JSON), see specs/example.json:
  id, campaign, source (absolute mp4), start, end (seconds in source), hook, caption, style (1-3),
  required_tags (list, e.g. ["#MW4","#MW4partner"]), tiktok_caption, instagram_caption,
  schedule: {"tiktok": "2026-10-24T12:30-04:00", "instagram": "..."}  (ISO with offset),
  footage: "campaign-supplied" | {"streamer": "Name"}  (streamers must be `approved` in permissions.md),
  notes (optional), pattern ("default" or "test: <what varies>").

Review gate (William, 2026-10-23: Morpheus approves clips; William gets a summary): hosting and scheduling refuse until
`--approve hook,truth,rules,safety,audio` has been recorded in jobs/<id>/review.json by the reviewer after actually viewing
jobs/<id>/contact.jpg plus frames, and reading the transcript for the clip's range. Editor (who made the clip) never approves.
`--approve` also fails automatically if the clip's source range overlaps another spec from the same source.

Safety rules enforced here:
  - Nothing is scheduled less than MIN_LEAD_MIN minutes ahead, so William can review in Buffer first.
  - Captions must contain every required tag and no other hashtags; no caption or hook may end with "?" asking for engagement
    (hooks may be questions only if --allow-question-hook is passed); hook 3-8 words.
  - Never submits to Vyro, never touches YouTube, never emails.
  - Per-clip state in jobs/<id>/state.json makes reruns idempotent: a hosted file or a Buffer post is never created twice.
State and artifacts: pipeline/jobs/<id>/ (cut.mp4, <id>.mp4, contact.jpg, thumbnail.jpg, state.json). Previews are copied to
projects/clips/previews/ (git-ignored) so the message tool can send them to William as files.
"""
import argparse, csv, glob, hashlib, json, os, re, shutil, subprocess, sys, urllib.error, urllib.request
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
FFMPEG = os.path.expanduser("~/openclaw-sites/bin/ffmpeg")
STAGES = ["cut", "format", "verify", "thumbnail", "host", "schedule", "log"]
MIN_LEAD_MIN = 45
REVIEW_CHECKS = ["hook", "truth", "rules", "safety", "audio"]
CLOUD, PRESET = "e5wsi8wu", "clips_unsigned"
CHANNELS = {"tiktok": "6adbec46778b240e2fa670dd", "instagram": "6adbea4e778b240e2fa63f1c"}
sys.path.insert(0, HERE)


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def ffinfo(path):
    err = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True).stderr
    info = {"audio": "Audio:" in err}
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    if m:
        info["duration"] = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
    m = re.search(r"Video:.*?, (\d{3,5})x(\d{3,5})", err)
    if m:
        info["w"], info["h"] = int(m[1]), int(m[2])
    return info


BLACK_MIN_S = 0.5


def black_runs(path):
    """Black runs longer than BLACK_MIN_S in the source-format cut, as [(start, end)] in clip seconds.
    Looks at the right 75% of the frame only, so a facecam overlay on the left (often still live during a game
    black screen) does not hide a black game view."""
    err = subprocess.run([FFMPEG, "-i", path, "-vf", f"crop=iw*0.75:ih:iw*0.25:0,blackdetect=d={BLACK_MIN_S}:pic_th=0.92:pix_th=0.12",
                          "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    return [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", err)]


def load_state(d):
    p = os.path.join(d, "state.json")
    return json.load(open(p)) if os.path.exists(p) else {"done": [], "hosted": {}, "buffer": {}}


def save_state(d, st):
    json.dump(st, open(os.path.join(d, "state.json"), "w"), indent=1)


def lint(spec, allow_question):
    errs = []
    for k in ("id", "campaign", "source", "start", "end", "hook", "caption", "required_tags", "tiktok_caption",
              "instagram_caption", "schedule", "footage"):
        if k not in spec:
            errs.append(f"spec missing '{k}'")
    if errs:
        return errs
    if not os.path.exists(spec["source"]):
        errs.append(f"source not found: {spec['source']}")
    n = len(spec["hook"].split())
    if not 3 <= n <= 8:
        errs.append(f"hook has {n} words (rule: 3-8)")
    if spec["hook"].strip().endswith("?") and not allow_question:
        errs.append("hook ends with '?': pass --allow-question-hook if it describes a dilemma, not asks for engagement")
    if not 15 <= spec["end"] - spec["start"] <= 59:
        errs.append(f"clip length {spec['end'] - spec['start']:.1f}s outside 15-59s")
    req = {t.lower() for t in spec["required_tags"]}
    for k in ("tiktok_caption", "instagram_caption"):
        tags = {t.lower() for t in re.findall(r"#\w+", spec[k])}
        if tags != req:
            errs.append(f"{k}: hashtags {sorted(tags)} must be exactly {sorted(req)}")
        if re.search(r"\b(like|comment|share|follow|subscribe)\b[^.]*\b(this|below|now|if)\b", spec[k], re.I):
            errs.append(f"{k}: looks like engagement bait")
    f = spec["footage"]
    if isinstance(f, dict):
        from guard import is_approved, DEFAULT
        if not is_approved(f["streamer"], DEFAULT):
            errs.append(f"streamer {f['streamer']} is not 'approved' in permissions.md")
    elif f != "campaign-supplied":
        errs.append("footage must be 'campaign-supplied' or {'streamer': name}")
    elif not os.path.exists(os.path.join(ROOT, "campaigns", spec["campaign"], "brief.md")):
        errs.append(f"campaign '{spec['campaign']}' has no campaigns/{spec['campaign']}/brief.md")
    for p, t in spec["schedule"].items():
        if p not in CHANNELS:
            errs.append(f"unknown platform {p}")
            continue
        due = datetime.fromisoformat(t)
        if due.tzinfo is None:
            errs.append(f"schedule.{p} needs a UTC offset")
        elif due < datetime.now(timezone.utc) + timedelta(minutes=MIN_LEAD_MIN):
            errs.append(f"schedule.{p} is less than {MIN_LEAD_MIN} min ahead (no time for William to review)")
    return errs


def gql(q):
    req = urllib.request.Request("https://api.buffer.com", data=json.dumps({"query": q}).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + os.environ["BUFFER_API_KEY"]})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        return {"errors": [{"message": f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"}]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--until", choices=STAGES, default="log")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--unschedule", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--allow-question-hook", action="store_true")
    ap.add_argument("--approve", metavar="CHECKS", help="comma list; must include " + ",".join(REVIEW_CHECKS))
    ap.add_argument("--reviewer", default="morpheus")
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    cid = spec["id"]
    d = os.path.join(HERE, "jobs", cid)
    os.makedirs(d, exist_ok=True)
    st = load_state(d)

    if a.status:
        print(json.dumps(st, indent=1))
        return
    if a.unschedule:
        for plat, pid in list(st["buffer"].items()):
            r = gql('{ post(input:{id:"%s"}){ status } }' % pid)
            status = ((r.get("data") or {}).get("post") or {}).get("status")
            if status != "scheduled":
                print(f"{plat} {pid}: status {status}, not deleting")
                continue
            r = gql('mutation { deletePost(input:{id:"%s"}){ __typename ... on MutationError { message } } }' % pid)
            print(plat, pid, json.dumps(r)[:200])
            if "errors" not in r and "message" not in json.dumps(r.get("data")):
                del st["buffer"][plat]
        bp = os.path.join(ROOT, "buffer-posts.json")
        posts = json.load(open(bp))
        for plat in ("tiktok", "instagram"):
            if f"{cid}-{plat}" in posts and plat not in st["buffer"]:
                del posts[f"{cid}-{plat}"]
        json.dump(posts, open(bp, "w"), indent=1)
        st["done"] = [s for s in st["done"] if s not in ("schedule", "log")]
        save_state(d, st)
        return

    if a.approve:
        got = set(a.approve.split(","))
        missing = set(REVIEW_CHECKS) - got
        if missing:
            sys.exit(f"REFUSED: approval must confirm every check; missing {sorted(missing)}")
        if not os.path.exists(os.path.join(d, f"{cid}.mp4")) or not os.path.exists(os.path.join(d, "contact.jpg")):
            sys.exit("REFUSED: render first (--until verify) so there is something to review")
        for other in sorted(glob.glob(os.path.join(ROOT, "specs", "*.json"))):
            o = json.load(open(other))
            if o["id"] != cid and o.get("source") == spec["source"] and o["start"] < spec["end"] and spec["start"] < o["end"]:
                sys.exit(f"REFUSED: source range overlaps {o['id']} ({o['start']}-{o['end']} s)")
        json.dump({"approved": True, "reviewer": a.reviewer, "checks": sorted(got), "note": a.note,
                   "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "short_sha": hashlib.sha256(open(os.path.join(d, f"{cid}.mp4"), "rb").read()).hexdigest()},
                  open(os.path.join(d, "review.json"), "w"), indent=1)
        print(f"[{cid}] approved by {a.reviewer}")
        return

    errs = lint(spec, a.allow_question_hook)
    if errs:
        sys.exit("REFUSED:\n  " + "\n  ".join(errs))
    print(f"[{cid}] lint ok")
    cut, short = os.path.join(d, "cut.mp4"), os.path.join(d, f"{cid}.mp4")
    thumb, contact = os.path.join(d, "thumbnail.jpg"), os.path.join(d, "contact.jpg")
    prev_dir = os.path.join(ROOT, "previews")
    os.makedirs(prev_dir, exist_ok=True)
    last = STAGES.index(a.until)

    def need(stage):
        return stage not in st["done"]

    def finish(stage):
        st["done"].append(stage)
        save_state(d, st)
        print(f"[{cid}] {stage} done")

    for stage in STAGES[: last + 1]:
        if not need(stage):
            continue
        if a.dry_run and stage in ("host", "schedule", "log"):
            print(f"[{cid}] DRY RUN {stage}: would " + {"host": "upload the Short to Cloudinary",
                  "schedule": "create Buffer posts: " + ", ".join(f"{p} @ {t}" for p, t in spec["schedule"].items()),
                  "log": "append results.csv rows and buffer-posts.json"}[stage])
            continue
        if stage == "cut":
            ln = spec["end"] - spec["start"]
            run([FFMPEG, "-y", "-loglevel", "error", "-ss", str(spec["start"]), "-t", str(ln), "-i", spec["source"],
                 "-af", f"afade=t=out:st={ln - 0.4:.2f}:d=0.4", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                 "-c:a", "aac", "-b:a", "192k", cut])
        elif stage == "format":
            run([sys.executable, os.path.join(HERE, "format_short.py"), cut, short, "--hook", spec["hook"],
                 "--caption", spec["caption"], "--style", str(spec.get("style", 1))])
        elif stage == "verify":
            i = ffinfo(short)
            bad = []
            if (i.get("w"), i.get("h")) != (1080, 1920):
                bad.append(f"size {i.get('w')}x{i.get('h')} (need 1080x1920)")
            if not 15 <= i.get("duration", 0) <= 59:
                bad.append(f"duration {i.get('duration')}")
            if not i["audio"]:
                bad.append("no audio track")
            vd = subprocess.run([FFMPEG, "-i", short, "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
            m = re.search(r"mean_volume: (-?[\d.]+) dB", vd)
            if m and float(m[1]) < -40:
                bad.append(f"audio near silent ({m[1]} dB)")
            # contact sheet: frames at 0,1,2,3,5,10 s so a human/agent can confirm the hook matches the opening
            run([FFMPEG, "-y", "-loglevel", "error", "-i", short, "-vf",
                 "select='eq(n,0)+eq(n,60)+eq(n,120)+eq(n,180)+eq(n,300)+eq(n,600)',scale=270:480,tile=6x1", "-frames:v", "1", contact])
            # second sheet: 8 evenly spaced frames across the whole clip (payoffs later than 10 s are otherwise unseen)
            contact_full = os.path.join(d, "contact_full.jpg")
            run([FFMPEG, "-y", "-loglevel", "error", "-i", short, "-vf",
                 f"fps=8/{i['duration']:.3f},scale=360:640,tile=4x2", "-frames:v", "1", contact_full])
            blacks = black_runs(cut)
            with open(os.path.join(d, "blackdetect.txt"), "w") as f:
                f.write("\n".join(f"{a:.1f}-{b:.1f}" for a, b in blacks) + ("\n" if blacks else ""))
            if bad:
                sys.exit(f"[{cid}] VERIFY FAILED: " + "; ".join(bad))
            print(f"[{cid}] verify ok: 1080x1920, {i['duration']:.1f}s, audio mean {m[1] if m else '?'} dB. "
                  f"Look at {contact} to confirm the hook matches the first 3 s (not automated), and {contact_full} for the whole clip.")
            if blacks:
                print(f"[{cid}] WARNING black frames over {BLACK_MIN_S}s (clip time, s): "
                      + ", ".join(f"{a:.1f}-{b:.1f} ({b - a:.1f}s)" for a, b in blacks) + " - trim or accept consciously")
            else:
                print(f"[{cid}] blackdetect: no black run over {BLACK_MIN_S}s")
        elif stage == "thumbnail":
            run([FFMPEG, "-y", "-loglevel", "error", "-ss", "0.6", "-i", short, "-frames:v", "1", "-q:v", "2", thumb])
            shutil.copy(short, os.path.join(prev_dir, f"{cid}.mp4"))
            shutil.copy(thumb, os.path.join(prev_dir, f"thumbnail-{cid}.jpg"))
        elif stage == "host":
            rp_ = os.path.join(d, "review.json")
            if not os.path.exists(rp_):
                sys.exit(f"[{cid}] NOT APPROVED: review the clip, then run --approve " + ",".join(REVIEW_CHECKS))
            rv = json.load(open(rp_))
            if rv.get("reviewer") == "editor" or not rv.get("approved"):
                sys.exit(f"[{cid}] review invalid (reviewer {rv.get('reviewer')})")
            if rv["short_sha"] != hashlib.sha256(open(short, "rb").read()).hexdigest():
                sys.exit(f"[{cid}] clip changed after review; re-review and --approve again")
            out = run(["curl", "-sS", "-F", f"file=@{short}", "-F", f"upload_preset={PRESET}",
                       f"https://api.cloudinary.com/v1_1/{CLOUD}/video/upload"], timeout=900).stdout
            r = json.loads(out)
            if "secure_url" not in r:
                sys.exit(f"[{cid}] HOST FAILED: {out[:300]}")
            head = subprocess.run(["curl", "-sI", r["secure_url"]], capture_output=True, text=True).stdout.lower()
            if " 200" not in head.split("\n")[0] or "video/mp4" not in head:
                sys.exit(f"[{cid}] HOST CHECK FAILED: {head[:200]}")
            st["hosted"] = {"url": r["secure_url"], "public_id": r["public_id"]}
        elif stage == "schedule":
            if "url" not in st.get("hosted", {}):
                sys.exit(f"[{cid}] nothing hosted yet")
            for plat, t in spec["schedule"].items():
                if plat in st["buffer"]:
                    print(f"[{cid}] {plat} already scheduled ({st['buffer'][plat]}), skipping")
                    continue
                due = datetime.fromisoformat(t).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                text = spec[f"{plat}_caption"]
                meta = "metadata: { instagram: { type: reel, shouldShareToFeed: true } }" if plat == "instagram" else ""
                q = (f'mutation {{ createPost(input: {{ text: {json.dumps(text)} channelId: "{CHANNELS[plat]}" '
                     f'schedulingType: automatic mode: customScheduled dueAt: "{due}" '
                     f'assets: [{{ video: {{ url: "{st["hosted"]["url"]}" metadata: {{ thumbnailOffset: 600 }} }} }}] {meta} }}) '
                     f'{{ ... on PostActionSuccess {{ post {{ id status dueAt }} }} ... on MutationError {{ message }} }} }}')
                r = gql(q)
                post = ((r.get("data") or {}).get("createPost") or {}).get("post")
                if not post or post["status"] != "scheduled":
                    sys.exit(f"[{cid}] SCHEDULE FAILED for {plat}: {json.dumps(r)[:300]}")
                st["buffer"][plat] = post["id"]
                save_state(d, st)
                print(f"[{cid}] {plat} scheduled {post['dueAt']} id {post['id']}")
        elif stage == "log":
            bp = os.path.join(ROOT, "buffer-posts.json")
            posts = json.load(open(bp))
            rp = os.path.join(ROOT, "results.csv")
            existing = {(r["clip_id"], r["platform"]) for r in csv.DictReader(open(rp, encoding="utf-8"))}
            with open(rp, "a", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                for plat, pid in st["buffer"].items():
                    posts[f"{cid}-{plat}"] = pid
                    if (cid, f"{plat}_via_buffer") not in existing:
                        when = datetime.fromisoformat(spec["schedule"][plat]).strftime("%Y-%m-%d %H:%M %Z%z")
                        w.writerow([cid, spec["campaign"], f"{plat}_via_buffer", f"{when} (scheduled)", "", "", "", "",
                                    spec["hook"], round(ffinfo(short)["duration"], 1),
                                    f"Buffer post {pid}; {spec.get('pattern', 'default')}; NOT submitted to Vyro; {spec.get('notes', '')}".strip()])
            json.dump(posts, open(bp, "w"), indent=1)
        finish(stage)

    if a.dry_run:
        print(f"[{cid}] dry run complete (cut/format/verify/thumbnail ran locally; nothing hosted or scheduled)")
    elif a.until == "log" and "log" in st["done"]:
        print(f"[{cid}] DONE. Preview: previews/{cid}.mp4, thumbnail-{cid}.jpg. Scheduled: " +
              ", ".join(f"{p} {spec['schedule'][p]}" for p in st["buffer"]))


if __name__ == "__main__":
    main()
