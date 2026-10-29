# Clip pipeline

> **Current route (2026-10-28):** campaign clips use `clip_job.py` below, TikTok only (William's focus), approved by Morpheus after weighing Editor, Scout and Strategist input; William gets summaries. The six-stage table is the legacy streamer/YouTube route, paused with YouTube and the streamer outreach. Whop campaigns also need the link submitted within 5 minutes of going live (see `campaigns/hardscope-ep3/brief.md`).


Hard rule: nothing runs for a streamer unless `permissions.md` shows the exact status `approved`
(`replied`, `contacted`, `candidate` all refuse). Every upload needs William's yes on that specific preview (legacy streamer/YouTube route only; for campaign clips Morpheus approves, see `clip_job.py` below and USER.md).

| Stage | Who | Command |
|---|---|---|
| 0. Get clip | agent | Fetch an approved streamer's clip file (method TBD, see PLAN.md) |
| 1. Prepare | script | `python3 -I pipeline/prepare_clip.py CLIP --streamer NAME --game GAME --clip-url URL` (guard + local transcript + job.json) |
| 2. Write | agent | Read `job.json` (`transcript`, `game`, `streamer`), write `hook` and `caption` into it (rules below) |
| 3. Render | script | `python3 -I pipeline/render_job.py pipeline/jobs/<id>` -> `short.mp4`, title, description |
| 4. Preview | agent | Send `short.mp4` + title to William on Telegram as a FILE (message tool, media=<path under the workspace>, forceDocument=true). In-chat Telegram video looks stretched on his phone; files play correctly. |
| 5. Publish | script | After a clear yes: `python3 -I pipeline/publish_job.py pipeline/jobs/<id> --approved-by-william` (private by default) |

## Upload kit (required with every rendered clip)
Editor writes `campaigns/<campaign>/kits/<clip-id>.md`: title (<=70 chars), description (context + required tags only), thumbnail (best of 3 frames, `previews/thumbnail-<clip-id>.jpg`), upload-settings checklist (not made for kids; paid promotion when the brief requires disclosure; no altered content; Gaming; comments on; Public), and TikTok/Reels captions. Morpheus sends William the video AND thumbnail as files plus the text. William's standing rule, 2026-10-22.

## Writing rules (stage 2)
- Hook: 3 to 8 words, specific to what actually happens in the clip, no clickbait the clip does not pay off.
- Caption: one or two sentences of real context from the transcript and game: what is happening, why it matters. Do not quote the streamer in a way that changes meaning.
- Vary structure across uploads (question, statement, reaction, setup/payoff) so videos do not look templated; the render step rotates three visual styles.
- If the transcript is empty or unclear, write from the game and clip title only, and say so in the preview.
- Skip the clip (do not render) if it contains slurs, a minor, other players' personal info, or third-party copyrighted music/video.
- Never edit, mirror, speed-shift or otherwise disguise footage to dodge detection.

## Transcripts and models
Local only: `~/openclaw-sites/clips-venv/bin/python pipeline/transcribe.py` (faster-whisper base.en, CPU). Accuracy on real gameplay audio is unverified until the first real clip.

## One-command route for campaign clips: `clip_job.py` (2026-10-23)
`python3 -I pipeline/clip_job.py specs/<clip-id>.json` runs cut -> format -> verify -> thumbnail -> host (Cloudinary) -> schedule (Buffer: TikTok + Instagram Reels) -> log (results.csv, buffer-posts.json). See the docstring and `specs/example.json`.
- Editor picks the moment and writes the spec (hook, caption, start/end, captions, required tags, schedule). Editor may run it only with `--until thumbnail` (local, no external effects). Morpheus runs the full job: hosting and scheduling are outward-facing.
- Lint refuses: hook not 3-8 words, wrong or extra hashtags, engagement-bait wording, clip length outside 15-59 s, streamer not `approved`, campaign without a brief, schedule less than 45 min ahead (leaves William time to review in Buffer).
- `--dry-run` runs the local stages only. `--unschedule` deletes this clip's still-scheduled Buffer posts. Reruns are idempotent (state in `pipeline/jobs/<id>/state.json`); a hosted file or Buffer post is never created twice.
- Still manual or separate: choosing the moment, checking `jobs/<id>/contact.jpg` that the hook matches the opening seconds, Cloudinary cleanup. Link submissions (Whop within 5 min; Vyro only when traction-gated) are done by Morpheus under USER.md rules, not by the script. The script does not touch YouTube, Vyro or Whop.
- Per-platform variants (2026-10-28): an optional `instagram_variant` block (start/end/hook/caption/style) makes the top-level fields the TikTok variant; each is rendered, reviewed, hosted and scheduled separately under `pipeline/jobs/<id>/<platform>/` (files `<id>-<platform>.mp4`, previews `previews/<id>-<platform>.mp4`). Specs without it behave as before. Empty or missing `schedule` = unscheduled: the job stops after `thumbnail` (no upload). Optional `required_mentions` (e.g. ["@hardscope"]) is linted for exactly-once in both captions with no other @handle; lint also refuses identical captions/hooks across platforms and hooks reused within a campaign. `submission` (default "vyro") sets the `log` note ("NOT submitted to Vyro/Whop").
- Buffer also supports deletePost/editPost, so a bad scheduled post can be removed or changed before it publishes.
- **Approval (William, 2026-10-23): Morpheus approves, William gets a summary.** Flow: Editor writes the spec and runs `--until thumbnail`; Morpheus reviews; only then `--approve hook,truth,rules,safety,audio` is recorded and the full job runs. Review means: (1) hook: view `jobs/<id>/contact.jpg` and extra frames; the hook must match what the first 3 s show or say; (2) truth: read the transcript for the range; hook, caption and kit must not misrepresent who said or did what, or the outcome; (3) rules: campaign brief rules (required tags only, no logos/credit/bait, collab/tag bans), kit complete; (4) safety: no slurs, minors, personal info, third-party music, sponsor reads the brief forbids; (5) audio: clear, not near-silent, no clipped start. `--approve` also fails if the source range overlaps another spec and is invalidated if the file changes. Reject (do not approve) means send the spec back to Editor with the reason; after two rejections of the same clip, tell William. Approval is recorded in `jobs/<id>/review.json`; the full-run gate refuses to host without it and Editor never approves its own work.
- Summary to William (Telegram, short, no per-clip request): after scheduling, one message: clip id, hook, platform, scheduled time, pattern/test label, and anything rejected and why. Live links and numbers arrive via the 3h tracker and the 8:15 AM digest. Send a video file only if he asks. A bad post can still be fixed before it publishes (Buffer editPost/deletePost).
