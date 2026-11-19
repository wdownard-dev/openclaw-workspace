# GTA 6 watcher (wrdgamingclipz)

Detect-only. Nothing here submits to OpusClip or posts. Plan: `GTA6-PLAN.md`. Launch 11/19 (Wikipedia lists 2026-11-19, PS5/Xbox Series).

## Files
- `candidates.json` creators with channel id, subs, avg views, cadence, verdict, evidence, `"approved"` flag.
- `watch.py` the watcher. `watch_state.json` dedupe, `watch_status.json` health (last scan time, errors), `watch.log`.
- `gaming_budget.py` + `gaming-caps.json` credit guard; `gaming-ledger.json` spend ledger (created on first `record`).
- `work/` raw resolver output (safe to delete).

## Run
    python3 watch.py                 # loop, every 12 min, 7 AM-11 PM ET (GAMEWATCH_INTERVAL_MIN to change)
    python3 watch.py --once --anytime --ignore-state   # test scan
    python3 watch.py --demo          # fake test alert
    python3 watch.py --once --only Kai
No API key; uses yt-dlp only (YouTube RSS returns 404 from this host). Scans take a few minutes for 14 channels.
Lines: `GAMEWATCH_VIDEO` / `GAMEWATCH_LIVE` (approved channels only), `GAMEWATCH_CANDIDATE ... UNAPPROVED` (info only),
`GAMEWATCH_ERROR` (throttled to once per 2 h). Filters: title/description mentions GTA 6/VI/Grand Theft Auto, or the channel
has `"gta_rp": true` and it is 11/19 or later; video <=24 h old and >=60 s; live only when actually live. Entries with
verdict `skip` are not scanned. Age-gated videos (e.g. some Rockstar trailers) are skipped by yt-dlp without cookies.

## Approve a channel
Edit `candidates.json`, set `"approved": true` on that entry (William's decision only). Standing approval for GTA clips applies
ONLY to approved entries; everything else stays "ask William / clip it".

## Alert to post
1. Alert from an approved channel -> check the budget: `python3 gaming_budget.py can-spend MINUTES` (exit 3 = no).
   Caps (gaming-caps.json): 600 credits launch week 11/19-11/25, 120/day, ~1 credit per source minute, auto-submit only
   sources <=40 min. Longer: cut the segment with ffmpeg first or ask William.
2. Submit to OpusClip (opusclip/opus.py), then `python3 gaming_budget.py record VIDEO_ID CREDITS --note ...`.
3. Screen: `opusclip/screen_clip.py PROJECT CLIP`, view every frame. Reject visible blood/gore/graphic injury, keep the first
   7 s clean of graphic violence, no isolated cutscene/story/ending clips (Rockstar takes those down), no leaked footage.
4. Post only inside 7 AM-11 PM ET, with a rewritten title, source credit ("Via <creator>"), and an original text line or
   voiceover on the clip (reused-content rule).
   YouTube: `opus.py post --account wrdgamingclipz` (postAccountId 6aee359f69f72aca6cb4207e)
   TikTok rvclips6 (postAccountId 6afa5abf5a226aba99eb2d09). Cadence per plan: YT 3/day (4 on 11/19-21), TikTok 2/day (3 on 11/19-20).

## Long-VOD moment workflow (zero OpusClip credits)
For a long approved-channel VOD/stream, cut moments ourselves instead of submitting the whole thing.
1. **Pick:** `python3 moment_pick.py VIDEO_ID [--top 14] [--window 30]` downloads the English auto-subs, scores 30 s windows for the
   streamer's own reaction (lowercase talk, "yo/bro/no way", laughter, rapid speech, repeats) and down-weights game-subtitle text
   (ALL-CAPS runs, `>>`). No LLM call. It writes `out/ID.moments.json` (about 1.4k tokens) and prints a numbered list; it flags a missing
   transcript (exit 2) or a mostly scripted VOD. The agent reads it, picks 3-5 moments and records them in `out/ID.picks.json`
   (`start`, `end`, one-line why, title idea). Auto-subs lag and miss streamer reactions drowned by game audio: widen the cut by a few s.
2. **Cut:** `python3 cut_moment.py VIDEO_ID --start S --end E [--name N]` downloads only that section (<=1080p), renders 1080x1920
   (blurred copy behind, 16:9 gameplay fitted in a band, source audio untouched, h264/aac, +faststart, max 60 s) and a 10-frame contact
   sheet. Outputs go to `out/`. Needs no ffmpeg on PATH (uses ~/openclaw-sites/bin/ffmpeg through a local proxy, because that static
   build segfaults on DNS).
3. **Screen:** view the whole contact sheet (and extra frames if needed). Reject visible blood/gore/graphic injury, keep the first 7 s
   clean, no isolated cutscene/story/ending clips, no leaked footage.
4. **Post:** `opusclip/opus.py post --account wrdgamingclipz ...` (or `clips/scripts/upload.py` for a local mp4). Standing approval
   applies only to channels with `"approved": true`; anything else, ask William. Add an original text line or voiceover (reused-content
   rule), rewrite the title, and credit the source ("Via <creator>"). Post only 7 AM-11 PM ET.

## Multi-signal picker (transcript + audio [+ chat])
    python3 signals_audio.py VIDEO_ID            # bestaudio download + loudness signals -> out/ID.audio.json (208 min VOD: ~10 s download, ~26 s compute)
    python3 signals_chat.py VIDEO_ID             # optional; prints CHAT_UNAVAILABLE (exit 0) when no chat replay (normal for edited uploads)
    python3 moment_pick.py VIDEO_ID --audio [--chat] [--top 14] [--gap 180]
Signals (10 s hop, 30 s window, all z-scored robustly against the video's own median/MAD): transcript reaction score (T, as before),
audio (A: RMS level, jump over the previous 2 min, and a shout/laughter proxy = share of loud 50 ms frames lifted by zero-crossing and
spectral flux), chat (C: messages per 30 s spike). A flag is set at z>=1.5. Rank = sum of z's + 2x the second-highest z, so agreement
beats a single strong signal. Picks are >= 3 min apart; windows >50% game-subtitle text are penalised. Output lines: `time [sec] flags
sc=combined tZ aZ scr=scripted_frac: text`. The agent then reads the list and picks by actual reaction content.
Known limits: loudness cannot separate the streamer from game explosions, music or screaming NPCs; a streamer who is loud all video
(e.g. Kai) gets TA on nearly everything, so agreement discriminates little there; auto-sub lag shifts text 2-5 s; no chat on edited
uploads; picks still need contact-sheet screening (black frames after mission fail/loading are common).

## Visual check (frames, no LLM)
Transcript+audio pick loud stretches, not visible action; this stage looks at the picture. Free: yt-dlp sections + ffmpeg + numpy.
    python3 moment_pick.py ID --audio --top 14                  # writes out/ID.moments.json
    python3 visual_check.py ID --moments out/ID.moments.json [--top 14] [--frames 8] [--keep] [--jobs 3]
    python3 moment_pick.py ID --audio --visual                  # merged ranking, flags T/A/V, drops listed with a reason -> out/ID.visual_rank.json
    python3 visual_check.py ID --sheets 8                       # labelled contact sheets of top 8 survivors -> out/ID.vsheetN.jpg
Then view the sheets, write `out/ID.picks_visual.json` (start,end,why,flags), cut with `cut_moment.py`.
- Downloads only each window at <=360p, video only (~1.2 MB each, ~17 s each; 14 windows, 3 parallel ~95 s), deleted after analysis.
  Thumbnails stay in `out/ID.vframes/`. Needs a prior `moment_pick.py` run (transcript fetch falls back to the `en-orig` track).
- Features (4 fps, 160x90 gray): motion (mean frame diff), p90 diff (bursts), scene cuts, black fraction (median luma, ignores HUD/chat),
  static fraction (4x4 block diffs + edge diffs, ignores ticking timers), flat fraction (fades/solid), longest static run, corner motion
  ratio (facecam, 4 corners), `visual_score` (high = motion + cuts, low black/static).
- Merge: `final = score + 8*(visual_score-0.9)`; V flag at visual_score>=1.1. Dropped: >40% black, >60% static, black+static >60%,
  or almost no motion.
- Limits: cannot tell action from dull riding with a busy camera, cutscenes from gameplay, 'Mission passed' text over moving scenes,
  or read faces. A tiny top-left facecam is invisible to motion stats. Thresholds are tuned on one 360p GTA 3 stream and one edited video;
  still view the sheets. YouTube can 429 subtitle fetches after many yt-dlp calls; wait a few minutes.

## Direct YouTube upload to wrdgamingclipz (setup pending William's consent, 2026-11-16)
- The host's `GOOGLE_OAUTH_REFRESH_TOKEN` belongs to **wrdclipz** (do not use it for gaming). Myth Ledger has its own token. wrdgamingclipz needs its own: `GOOGLE_OAUTH_REFRESH_TOKEN_GAMING`.
- Auth (one time): `python3 yt_auth_gaming.py url <public_client_id>` prints the consent URL; William opens it as the account that owns wrdgamingclipz and picks that channel; the browser then fails to load `http://127.0.0.1:8085/?...code=...`; he enters only the `code` value through `secrets request GOOGLE_OAUTH_CODE` (never in chat); then `python3 yt_auth_gaming.py code` stores the refresh token (channel id UCIbJfNm2nJKUCItsO0XGhiw is hard-checked before any upload).
- Upload: `python3 yt_upload_gaming.py FILE --title T --desc-file F --privacy public|unlisted|private [--category 20]`. Default privacy private. Scopes cannot delete videos.
- Fallback until then: `opus_upload.py FILE` (OpusClip no-clip project) then `../opusclip/opus.py post --account 6aee359f69f72aca6cb4207e`, but OpusClip burns its own captions in.

## Guide-Short factory (wrdgamingclipz)
Rules: `GUIDE-RULES.md`. Candidates: `guides_week1.json`. Tool: `guide_make.py` (see its docstring).
    python3 guide_make.py URL fetch          # video <=720p + captions -> work/guides/ID/
    python3 guide_make.py URL sheet S E [N]  # labelled frame sheets to verify on-screen proof
    # SCRIPT STEP: read transcript, rank tips, write out/ID.guide.json (reviewable, separate)
    python3 guide_make.py URL build          # Liam TTS + render + desc + contact sheet + script/tip file
    python3 guide_make.py URL upload         # PRIVATE only

- Metadata rules (hashtags, titles, tags; standing since 2026-11-18): see METADATA_RULES.md.
