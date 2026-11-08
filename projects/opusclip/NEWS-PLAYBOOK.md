# Project Red Pill: News Playbook (single source of truth)

Set by William, 2026-11-06. If another file or note disagrees with this one, this one wins. Gaming is a separate channel and project, and it is not covered here. The TikTok campaign project (Vyro, `projects/clips`, its Strategist/Editor/Scout agents) is separate and untouched.

## 1. What this is
wrdclipz (YouTube) is a news channel. We clip **official-source** coverage of breaking stories and post fast. Evidence so far (directional, n=2): the Learjet crash clips got about 1,300 views each, everything else single digits. Goal: learn how much speed and story type matter, and grow the channel. See `LEARNINGS.md`.

## 2. The pipeline
1. **Detect** (automatic, free):
   - `radar_loop.py`: stream automation, every 15 min, 7 AM to 11 PM ET. Key-less. Finds events reported by many outlets in the last 2 h and checks for an official channel live now (`RADAR_LIVE`) or an official video up in the last 24 h (`RADAR_ALERT`); very big events with no official video yet are `RADAR_EARLY`.
   - `radar.py`: the fuller scan with YouTube view velocity, Trends, Google News, TMZ and Page Six (headlines only), Reddit, Bluesky, Mastodon. Runs from the 2-hour sweep automation and on demand: `python3 radar.py --no-state --query "story"`.
2. **Alert**: one short message to William: story, why it is spicy or weak, numbers, link, safety notes, credit cost, next step.
3. **"clip it"** from William starts the clip and also authorizes posting: once a clip passes screening it posts immediately, with no second approval (William, 11/6). Nothing is submitted or posted by the radar itself. William can pull a post at any time.
   - Uploaded video: `python3 opus.py submit URL --min 20 --max 45 --keywords ...`, then poll `opus.py status`; about 12 min for a 28 min source.
   - Live stream: `python3 live_watch.py VIDEO_ID` as a background exec. It waits for the stream to end, submits, waits for OpusClip, lists the clips. OpusClip cannot process a stream while it is running.
4. **Screen** every clip before posting (section 4). Read the clip transcript (`text` field of `/api/exportable-clips`) and look at about 6 frames: download `uriForExport` and extract frames with `/home/williamdownard/openclaw-sites/bin/ffmpeg`, then view them. A clip with frames we have not looked at does not post.
5. **Post** the best 1 to 2 clips that pass screening and score >= 80, with a title and description I write (never OpusClip's auto text): `python3 opus.py post PROJECT CLIP --account <YouTube id> --title ... --desc ... --yes`. Account ids: `python3 opus.py accounts` (YouTube wrdclipz 6aea02988e21955f59a43b64).
6. **Log** a row in `experiment-log.csv` at posting: lane=news, radar signal, source age at post, event-to-post hours, score, title.
7. **Read results** at 24 h, 72 h, 7 d (tracker reads public views; William supplies Studio screenshots for retention, impressions, traffic source). Update `LEARNINGS.md`.

## 2b. Story priority (William, 2026-11-06): automatic, but methodical
When a clip we posted starts to do well, that story becomes a priority for 48 hours and we follow it up automatically within strict limits.
- **Tracking:** every 15 min the loop snapshots views on our recent Shorts (key-less, `radar_track.json`, log `radar_track.log`). A news clip is HOT when it has 300+ views within 36 h of posting, or is gaining 60+ views an hour (rate over the last 10 to 65 min, at least 25 views). Starting thresholds; tune from data. Non-news clips are tracked but never trigger a priority.
- **What a priority does:** the loop watches the story every 15 min with no outlet threshold and prints `RADAR_FOLLOWUP`: a new official live stream or video (VIDEO, LIVE), a surge of new headlines (NEWS), or a reminder that the next unused clip is due (BANKED_DUE).
- **Automatic actions (the stream job's agent does these, then reports to William):**
  - **Banked clips (no credits):** post the next unused clip (score >= 80) from the same OpusClip project when the limits allow.
  - **New official source (costs credits):** submit it to OpusClip (a VIDEO, or a LIVE stream once it ends), then screen and post the best clip. The stream-triggered agent cannot schedule timers, so it records the job in a pending queue (`followup.py pending-add`) and the loop sends a `PENDING_CHECK` reminder every 10 min until the clip is posted (abandoned after 4 h). Over the credit limit, or a source over 40 min: ask William instead.
  - **Never automatic:** NEWS surges are information only. Stories that are not priorities stay alert-only until William says "clip it".
- **Guardrails** (`followup.py`, edit the constants there): at most 3 auto posts per story per 24 h; at least 3 h between posts (a brand-new official briefing may skip the spacing); posting window 7 AM to 11 PM ET (banked reminders 8 AM to 10 PM); at most 60 credits per story and 120 a day on automatic submissions.
- **Screening before every automatic post** (`screen_clip.py PROJECT CLIP`): transcript read, text flags checked, every extracted frame viewed. Reject and record (`followup.py reject`) on: visible blood, gore or graphic injury on any frame (a person shot or down without blood is allowed); a clear YouTube policy violation we are sure would get the video pulled (911, dispatch and distress audio are allowed); a motive stated as fact; an unverified claim about a named person; content that does not match the story or repeats what we posted. A clip with unviewed frames never posts. Titles and descriptions are always rewritten by me, attributed to the agency.
- **Logging:** every automatic post goes into `experiment-log.csv` through `followup.py log-post`.
- **Duration:** 48 h; extended 24 h at a time while the clip still gains 20+ views an hour (max 7 days).
- **Spacing** counts the last post of any clip from the same OpusClip project (read from the experiment log), so renaming a priority cannot reset it.
- **By hand:** `python3 radar_loop.py --rename "old words" "new words"` (keeps everything), `--prioritize "story words" --hours 48 --project <OPUS_PROJECT_ID>`, `--unprioritize "words"`, `--priorities`; `python3 followup.py status`.
- **Story words:** the auto words are rough; on HOT I check them and replace them with better ones.

## 3. Sources
- **Clip from (priority):** official agency channels (sheriff, police, fire, NTSB, FAA, NWS/NHC, NASA, courts that stream, other government). Posted by the agency, public-interest, fast.
- **TV-network, TMZ and similar video:** allowed if it is good (William, 11/6), but only with William's explicit approval first, for each clip. Copyright and Content ID risk: say so when asking. Alerts list these as "non-official options", never as the default.
- **Information only (headlines, never clipped):** Google Trends, Google News, TMZ, Page Six, Reddit, Bluesky, Mastodon. X is not connected (xAI cost); revisit only if the radar proves late.
- **Source wait rules:** if a source plainly posts a wait rule, respect it.
- **Source age:** skip a source older than 48 h. Prefer one under 24 h.

## 4. Safety (never relaxed)
- Shocking real footage is wanted (William, 11/6): footage of a person shot or down without blood, 911 calls, dispatch audio and victim distress audio are all allowed. Reject only visible blood, gore or graphic injury, and anything we are sure is a clear YouTube policy violation that would get the video pulled. Officially released bodycam, surveillance and 911 releases are fine.
- Attribute to the agency ("Per HCSO: ..."). State no motive as fact when reports conflict. Allegations are allegations. No unverified claims about named people.
- Child-abuse and sexual-violence stories are blocked by the radar. Politics and elections are held for William.
- Rewrite any OpusClip title or description that misstates the facts.
- Routine road crashes are not filtered out. The loop flags them as "routine-looking" and raises the bar to 8 outlets, and I judge whether the people involved (a celebrity, an official, a child, a famous place) make it a story. Every decision is logged in `radar_loop_decisions.jsonl`; the weekly review checks what the filters hid.

## 5. Credits (OpusClip Pro, 3,600 per year plus the 41 trial credits)
- Balance on 11/3 was 3,641. About 1 credit per source minute. Since then: dry run (about 150, estimate) and Citibank (28), so roughly 3,460 left (estimate; confirm from the OpusClip screen).
- No weekly cap for now (William, 11/6): this phase is information gathering and he can add credits. An even pace would be about 70 a week, so track usage in the weekly review. Prefer short sources (under 20 min). Every alert states its credit cost. Do not submit without William's "clip it".

## 6. Files
- Active: `NEWS-PLAYBOOK.md`, `LEARNINGS.md`, `experiment-log.csv`, `radar.py`, `radar_loop.py`, `live_watch.py`, `opus.py`, `radar_state.json`, `radar_loop_state.json`, `radar_track.json`, `followup.py`, `screen_clip.py`.
- Health and tuning: `radar_loop_status.json` (last scan time, checked daily), `radar_loop.log`, `radar_loop_decisions.jsonl` (every candidate event and what was decided).
- Archived, not in use: `archive/pre-pivot-2026-11-06/` (source channel list, queue, dry-run files, old strategy and GTA 6 plans, hook-text test).

## 7. Automations
News clip radar (stream, every 15 min); News clip radar: velocity sweep (every 2 h, 8:15 AM to 10:15 PM); Red Pill daily tracker (9 AM); Red Pill weekly learning review (Sunday 7 PM). Everything else in the automations list belongs to the TikTok campaign project.

## 8. Decisions (William, 2026-11-06)
- "clip it" authorizes screening and posting; posts immediately after a clean screen. YouTube only (no TikTok). Official agency sources are the priority; TV-network/TMZ video only with his explicit approval. No weekly credit cap for now. GTA 6 clips cancelled (reuse for the gaming channel). Gaming channel: William will say when it is live.
- Open: re-publish the Google OAuth app so the YouTube tokens stop expiring (William will do this after the clean-up and needs my help). Until then, retention and impressions come from his Studio screenshots.
- **Score bar lowered to 80 (William, 2026-11-07):** posting bar is now OpusClip score >= 80 (was 90), for hand-approved and automatic posts. Reason: in the log (n=27, all scored 84-99) score did not predict views; screening, story match and no-repeat are the real gates and are unchanged. Below 80, ask William with a one-line reason. We must keep learning from what is getting views: the daily tracker reports the top clips and compares median views by score band; once at least 6 posted clips score 80-89, check them against the 90+ group and adjust again. Pick clips by what has been getting views (story heat at post time first), not by score alone.
- Monetization status for the Strategist: projects/opusclip/MONETIZATION-STATUS.md (refreshed daily by the Red Pill tracker via monetization.py).
