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

## Writing rules (stage 2)
- Hook: 3 to 8 words, specific to what actually happens in the clip, no clickbait the clip does not pay off.
- Caption: one or two sentences of real context from the transcript and game: what is happening, why it matters. Do not quote the streamer in a way that changes meaning.
- Vary structure across uploads (question, statement, reaction, setup/payoff) so videos do not look templated; the render step rotates three visual styles.
- If the transcript is empty or unclear, write from the game and clip title only, and say so in the preview.
- Skip the clip (do not render) if it contains slurs, a minor, other players' personal info, or third-party copyrighted music/video.
- Never edit, mirror, speed-shift or otherwise disguise footage to dodge detection.

## Transcripts and models
Local only: `~/openclaw-sites/clips-venv/bin/python pipeline/transcribe.py` (faster-whisper base.en, CPU). Accuracy on real gameplay audio is unverified until the first real clip.
