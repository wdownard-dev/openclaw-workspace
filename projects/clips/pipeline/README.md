# Clip pipeline

Hard rule: nothing runs for a streamer unless `permissions.md` shows the exact status `approved`
(`replied`, `contacted`, `candidate` all refuse). Every upload needs William's yes on that specific preview.

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
- Still manual: choosing the moment, checking `jobs/<id>/contact.jpg` that the hook matches the opening seconds, Cloudinary cleanup, Vyro submission. Does not touch YouTube or Vyro.
- Buffer also supports deletePost/editPost, so a bad scheduled post can be removed or changed before it publishes.
- After `clip_job.py` finishes, Morpheus sends William the Short as a FILE (message tool, media=previews/<id>.mp4, forceDocument=true) with the hook, platforms, scheduled time and TikTok caption, and offers "change" (fix via Buffer editPost/deletePost). This step is Morpheus's, not the script's (scripts cannot send messages).
