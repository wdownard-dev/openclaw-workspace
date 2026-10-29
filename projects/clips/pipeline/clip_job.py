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
  schedule: {"tiktok": "2026-10-24T12:30-04:00", "instagram": "..."}  (ISO with offset; optional - missing or {} means
    unscheduled: the job stops after `thumbnail`, nothing is hosted or uploaded),
  footage: "campaign-supplied" | {"streamer": "Name"}  (streamers must be `approved` in permissions.md),
  notes (optional), pattern ("default" or "test: <what varies>"),
  instagram_variant (optional): {start, end, hook, caption, style}; the top-level start/end/hook/caption/style then become the
    TikTok variant. Each variant is cut/formatted/verified/hosted/reviewed separately in jobs/<id>/<platform>/ and `schedule`
    uses each platform's own file. Specs without it render once into jobs/<id>/ exactly as before.
  required_mentions (optional): e.g. ["@hardscope"]; each must appear exactly once (case-insensitive) in tiktok_caption and
    instagram_caption and no other @handle may appear. Not linted when absent.
  submission (optional, default "vyro"): where the post link is submitted; sets the note written by the `log` stage.

Review gate (William, 2026-10-23: Morpheus approves clips; William gets a summary): hosting and scheduling refuse until
`--approve hook,truth,rules,safety,audio` has been recorded in jobs/<id>/review.json by the reviewer after actually viewing
jobs/<id>/contact.jpg plus frames, and reading the transcript for the clip's range. Editor (who made the clip) never approves.
`--approve` also fails automatically if the clip's source range overlaps another spec from the same source (a spec's own
variants are skipped). With variants it records one review.json (with its own short_sha) per platform directory.
Lint also fails if tiktok_caption and instagram_caption (or the two platform hooks) are the same once tags/mentions are
stripped, or if a hook was already used by another spec of the same campaign.

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


def variants(spec):
    """[(platform, params)]. Without instagram_variant: one entry (None, params) rendered into jobs/<id>/ as always.
    With it: the top-level fields are the TikTok variant; the instagram variant overrides any of start/end/hook/caption/style."""
    base = {k: spec[k] for k in ("start", "end", "hook", "caption") if k in spec}
    base["style"] = spec.get("style", 1)
    v = spec.get("instagram_variant")
    if not v:
        return [(None, base)]
    return [("tiktok", base), ("instagram", {**base, **v})]


def variant_label(cid, plat):
    return cid if plat is None else f"{cid}-{plat}"


def variant_dir(d, plat):
    return d if plat is None else os.path.join(d, plat)


def source_ranges(spec):
    return [(p["start"], p["end"]) for _, p in variants(spec) if "start" in p and "end" in p]


def norm_hook(h):
    return re.sub(r"\W+", " ", h.lower()).strip()


HANDLE_RE = r"(?<![\w@])@\w+(?:\.\w+)*"


def norm_caption(c):
    c = re.sub(HANDLE_RE, " ", re.sub(r"#\w+", " ", c))
    return re.sub(r"\W+", " ", c.lower()).strip()


def other_specs(spec):
    """Other specs of the same campaign (valid JSON with an id)."""
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "specs", "*.json"))):
        try:
            o = json.load(open(p))
        except ValueError:
            continue
        if isinstance(o, dict) and o.get("id") and o["id"] != spec.get("id") and o.get("campaign") == spec.get("campaign"):
            out.append(o)
    return out


def lint(spec, allow_question):
    errs = []
    for k in ("id", "campaign", "source", "start", "end", "hook", "caption", "required_tags", "tiktok_caption",
              "instagram_caption", "footage"):
        if k not in spec:
            errs.append(f"spec missing '{k}'")
    if errs:
        return errs
    if not os.path.exists(spec["source"]):
        errs.append(f"source not found: {spec['source']}")
    for plat, p in variants(spec):
        pre = f"{plat}: " if plat else ""
        if not isinstance(p.get("hook"), str) or not isinstance(p.get("start"), (int, float)) or not isinstance(p.get("end"), (int, float)):
            errs.append(f"{pre}variant needs hook, start and end")
            continue
        n = len(p["hook"].split())
        if not 3 <= n <= 8:
            errs.append(f"{pre}hook has {n} words (rule: 3-8)")
        if p["hook"].strip().endswith("?") and not allow_question:
            errs.append(f"{pre}hook ends with '?': pass --allow-question-hook if it describes a dilemma, not asks for engagement")
        if not 15 <= p["end"] - p["start"] <= 59:
            errs.append(f"{pre}clip length {p['end'] - p['start']:.1f}s outside 15-59s")
    if errs:
        return errs
    vs = variants(spec)
    if len(vs) == 2 and norm_hook(vs[0][1]["hook"]) == norm_hook(vs[1][1]["hook"]):
        errs.append("tiktok and instagram hooks are the same")
    mine = {norm_hook(p["hook"]) for _, p in vs}
    for o in other_specs(spec):
        for _, op in variants(o):
            if isinstance(op.get("hook"), str) and norm_hook(op["hook"]) in mine:
                errs.append(f"hook {op['hook']!r} is already used by {o['id']} (same campaign)")
    if norm_caption(spec["tiktok_caption"]) == norm_caption(spec["instagram_caption"]):
        errs.append("tiktok_caption and instagram_caption are the same once tags/mentions are removed")
    if not re.fullmatch(r"[a-z0-9_-]+", str(spec.get("submission", "vyro"))):
        errs.append("submission must be a lowercase word such as 'vyro' or 'whop'")
    if "required_mentions" in spec:
        rm = spec["required_mentions"]
        if not isinstance(rm, list) or not all(isinstance(m, str) and re.fullmatch(r"@\w+(?:\.\w+)*", m) for m in rm):
            errs.append("required_mentions must be a list of @handles")
        else:
            req_m = [m.lower() for m in rm]
            for k in ("tiktok_caption", "instagram_caption"):
                found = [m.lower() for m in re.findall(HANDLE_RE, spec[k])]
                for m in req_m:
                    if found.count(m) != 1:
                        errs.append(f"{k}: {m} must appear exactly once (found {found.count(m)})")
                extra = sorted({m for m in found if m not in req_m})
                if extra:
                    errs.append(f"{k}: unexpected @handles {extra}")
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
    sched = spec.get("schedule") or {}
    if not isinstance(sched, dict):
        errs.append("schedule must be an object like {\"tiktok\": \"<ISO time with offset>\"}")
        sched = {}
    for p, t in sched.items():
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
    vs = variants(spec)
    for plat, _ in vs:
        os.makedirs(variant_dir(d, plat), exist_ok=True)
    sched = spec.get("schedule") or {}

    def short_path(plat):
        return os.path.join(variant_dir(d, plat), f"{variant_label(cid, plat)}.mp4")

    if a.status:
        if vs[0][0] is None:
            print(json.dumps(load_state(d), indent=1))
        else:
            print(json.dumps({plat: load_state(variant_dir(d, plat)) for plat, _ in vs}, indent=1))
        return
    if a.unschedule:
        for plat_v, _ in vs:
            vd = variant_dir(d, plat_v)
            st = load_state(vd)
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
            st["done"] = [s for s in st["done"] if s not in ("schedule", "log")]
            save_state(vd, st)
        still = set()
        for plat_v, _ in vs:
            still |= set(load_state(variant_dir(d, plat_v))["buffer"])
        bp = os.path.join(ROOT, "buffer-posts.json")
        posts = json.load(open(bp))
        for plat in ("tiktok", "instagram"):
            if f"{cid}-{plat}" in posts and plat not in still:
                del posts[f"{cid}-{plat}"]
        json.dump(posts, open(bp, "w"), indent=1)
        return

    if a.approve:
        got = set(a.approve.split(","))
        missing = set(REVIEW_CHECKS) - got
        if missing:
            sys.exit(f"REFUSED: approval must confirm every check; missing {sorted(missing)}")
        for plat, _ in vs:
            if not os.path.exists(short_path(plat)) or not os.path.exists(os.path.join(variant_dir(d, plat), "contact.jpg")):
                sys.exit("REFUSED: render first (--until verify) so there is something to review")
        mine = source_ranges(spec)
        for other in sorted(glob.glob(os.path.join(ROOT, "specs", "*.json"))):
            o = json.load(open(other))
            if o["id"] == cid or o.get("source") != spec["source"]:
                continue  # a spec's own variants are never compared with each other
            for os_, oe in source_ranges(o):
                if any(os_ < me and ms < oe for ms, me in mine):
                    sys.exit(f"REFUSED: source range overlaps {o['id']} ({os_}-{oe} s)")
        at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for plat, _ in vs:
            json.dump({"approved": True, "reviewer": a.reviewer, "checks": sorted(got), "note": a.note, "at": at,
                       "short_sha": hashlib.sha256(open(short_path(plat), "rb").read()).hexdigest()},
                      open(os.path.join(variant_dir(d, plat), "review.json"), "w"), indent=1)
            print(f"[{variant_label(cid, plat)}] approved by {a.reviewer}")
        return

    errs = lint(spec, a.allow_question_hook)
    if errs:
        sys.exit("REFUSED:\n  " + "\n  ".join(errs))
    print(f"[{cid}] lint ok")
    prev_dir = os.path.join(ROOT, "previews")
    os.makedirs(prev_dir, exist_ok=True)
    submission = spec.get("submission", "vyro")
    sub_name = {"vyro": "Vyro", "whop": "Whop"}.get(submission, submission.capitalize())
    done_lines = []

    for plat_v, p in vs:
        lab = variant_label(cid, plat_v)
        vd = variant_dir(d, plat_v)
        st = load_state(vd)
        cut, short = os.path.join(vd, "cut.mp4"), short_path(plat_v)
        thumb, contact = os.path.join(vd, "thumbnail.jpg"), os.path.join(vd, "contact.jpg")
        last = STAGES.index(a.until)
        # platforms this file is posted to: a variant only goes to its own platform; a single render goes to every scheduled one
        sched_plats = [x for x in sched if plat_v is None or x == plat_v]
        if not sched_plats and last > STAGES.index("thumbnail"):
            last = STAGES.index("thumbnail")
            print(f"[{lab}] UNSCHEDULED: no schedule entry" + (f" for {plat_v}" if plat_v else "")
                  + "; stopping after thumbnail (nothing hosted, uploaded or scheduled). Add a schedule to the spec to continue.")

        def need(stage):
            return stage not in st["done"]

        def finish(stage):
            st["done"].append(stage)
            save_state(vd, st)
            print(f"[{lab}] {stage} done")

        for stage in STAGES[: last + 1]:
            if not need(stage):
                continue
            if a.dry_run and stage in ("host", "schedule", "log"):
                print(f"[{lab}] DRY RUN {stage}: would " + {"host": "upload the Short to Cloudinary",
                      "schedule": "create Buffer posts: " + ", ".join(f"{x} @ {sched[x]}" for x in sched_plats),
                      "log": "append results.csv rows and buffer-posts.json"}[stage])
                continue
            if stage == "cut":
                ln = p["end"] - p["start"]
                run([FFMPEG, "-y", "-loglevel", "error", "-ss", str(p["start"]), "-t", str(ln), "-i", spec["source"],
                     "-af", f"afade=t=out:st={ln - 0.4:.2f}:d=0.4", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                     "-c:a", "aac", "-b:a", "192k", cut])
            elif stage == "format":
                run([sys.executable, os.path.join(HERE, "format_short.py"), cut, short, "--hook", p["hook"],
                     "--caption", p["caption"], "--style", str(p["style"])])
            elif stage == "verify":
                i = ffinfo(short)
                bad = []
                if (i.get("w"), i.get("h")) != (1080, 1920):
                    bad.append(f"size {i.get('w')}x{i.get('h')} (need 1080x1920)")
                if not 15 <= i.get("duration", 0) <= 59:
                    bad.append(f"duration {i.get('duration')}")
                if not i["audio"]:
                    bad.append("no audio track")
                vd_ = subprocess.run([FFMPEG, "-i", short, "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
                m = re.search(r"mean_volume: (-?[\d.]+) dB", vd_)
                if m and float(m[1]) < -40:
                    bad.append(f"audio near silent ({m[1]} dB)")
                # contact sheet: frames at 0,1,2,3,5,10 s so a human/agent can confirm the hook matches the opening
                run([FFMPEG, "-y", "-loglevel", "error", "-i", short, "-vf",
                     "select='eq(n,0)+eq(n,60)+eq(n,120)+eq(n,180)+eq(n,300)+eq(n,600)',scale=270:480,tile=6x1", "-frames:v", "1", contact])
                # second sheet: 8 evenly spaced frames across the whole clip (payoffs later than 10 s are otherwise unseen)
                contact_full = os.path.join(vd, "contact_full.jpg")
                run([FFMPEG, "-y", "-loglevel", "error", "-i", short, "-vf",
                     f"fps=8/{i['duration']:.3f},scale=360:640,tile=4x2", "-frames:v", "1", contact_full])
                blacks = black_runs(cut)
                with open(os.path.join(vd, "blackdetect.txt"), "w") as f:
                    f.write("\n".join(f"{x:.1f}-{y:.1f}" for x, y in blacks) + ("\n" if blacks else ""))
                if bad:
                    sys.exit(f"[{lab}] VERIFY FAILED: " + "; ".join(bad))
                print(f"[{lab}] verify ok: 1080x1920, {i['duration']:.1f}s, audio mean {m[1] if m else '?'} dB. "
                      f"Look at {contact} to confirm the hook matches the first 3 s (not automated), and {contact_full} for the whole clip.")
                if blacks:
                    print(f"[{lab}] WARNING black frames over {BLACK_MIN_S}s (clip time, s): "
                          + ", ".join(f"{x:.1f}-{y:.1f} ({y - x:.1f}s)" for x, y in blacks) + " - trim or accept consciously")
                else:
                    print(f"[{lab}] blackdetect: no black run over {BLACK_MIN_S}s")
            elif stage == "thumbnail":
                run([FFMPEG, "-y", "-loglevel", "error", "-ss", "0.6", "-i", short, "-frames:v", "1", "-q:v", "2", thumb])
                shutil.copy(short, os.path.join(prev_dir, f"{lab}.mp4"))
                shutil.copy(thumb, os.path.join(prev_dir, f"thumbnail-{lab}.jpg"))
            elif stage == "host":
                rp_ = os.path.join(vd, "review.json")
                if not os.path.exists(rp_):
                    sys.exit(f"[{lab}] NOT APPROVED: review the clip, then run --approve " + ",".join(REVIEW_CHECKS))
                rv = json.load(open(rp_))
                if rv.get("reviewer") == "editor" or not rv.get("approved"):
                    sys.exit(f"[{lab}] review invalid (reviewer {rv.get('reviewer')})")
                if rv["short_sha"] != hashlib.sha256(open(short, "rb").read()).hexdigest():
                    sys.exit(f"[{lab}] clip changed after review; re-review and --approve again")
                out = run(["curl", "-sS", "-F", f"file=@{short}", "-F", f"upload_preset={PRESET}",
                           f"https://api.cloudinary.com/v1_1/{CLOUD}/video/upload"], timeout=900).stdout
                r = json.loads(out)
                if "secure_url" not in r:
                    sys.exit(f"[{lab}] HOST FAILED: {out[:300]}")
                head = subprocess.run(["curl", "-sI", r["secure_url"]], capture_output=True, text=True).stdout.lower()
                if " 200" not in head.split("\n")[0] or "video/mp4" not in head:
                    sys.exit(f"[{lab}] HOST CHECK FAILED: {head[:200]}")
                st["hosted"] = {"url": r["secure_url"], "public_id": r["public_id"]}
            elif stage == "schedule":
                if "url" not in st.get("hosted", {}):
                    sys.exit(f"[{lab}] nothing hosted yet")
                for plat in sched_plats:
                    t = sched[plat]
                    if plat in st["buffer"]:
                        print(f"[{lab}] {plat} already scheduled ({st['buffer'][plat]}), skipping")
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
                        sys.exit(f"[{lab}] SCHEDULE FAILED for {plat}: {json.dumps(r)[:300]}")
                    st["buffer"][plat] = post["id"]
                    save_state(vd, st)
                    print(f"[{lab}] {plat} scheduled {post['dueAt']} id {post['id']}")
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
                            when = datetime.fromisoformat(sched[plat]).strftime("%Y-%m-%d %H:%M %Z%z")
                            w.writerow([cid, spec["campaign"], f"{plat}_via_buffer", f"{when} (scheduled)", "", "", "", "",
                                        p["hook"], round(ffinfo(short)["duration"], 1),
                                        f"Buffer post {pid}; {spec.get('pattern', 'default')}; NOT submitted to {sub_name}; {spec.get('notes', '')}".strip()])
                json.dump(posts, open(bp, "w"), indent=1)
            finish(stage)

        if a.until == "log" and "log" in st["done"]:
            done_lines.append(f"[{lab}] DONE. Preview: previews/{lab}.mp4, thumbnail-{lab}.jpg. Scheduled: " +
                              ", ".join(f"{x} {sched[x]}" for x in st["buffer"]))

    if a.dry_run:
        print(f"[{cid}] dry run complete (cut/format/verify/thumbnail ran locally; nothing hosted or scheduled)")
    else:
        for line in done_lines:
            print(line)


if __name__ == "__main__":
    main()
