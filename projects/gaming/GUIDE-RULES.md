# Guide / walkthrough Short rules (wrdgamingclipz, v1 from the Fortnite Pirate Shop Token test, 2026-11-16)

Proven example: out/walk_v4.mp4 (live: https://www.youtube.com/shorts/iSgpSI7KrJQ). Method: 'medium rework' = our own script and our own voice over the source guide's footage (their audio muted).

## Required elements (in this order)
1. HOOK = goal + payoff in the first 2 s ('Here's how to get X'). Best: open on a proof shot (the reward screen).
2. SETUP / LOADOUT FIRST: anything you must equip or do before starting goes before location (the sprite lesson).
3. WHERE to go, then HOW to get it in 2-3 steps.
4. CLOSE with effort/expectation plus a comment prompt ('Got X? Drop a comment and tell me how many ... it took you').
5. One goal per Short. NO length target: the guide is as long as it needs to be to be built correctly (William, 2026-11-21: 90 s or 3 min are both fine; hard ceiling is the 3 min Shorts cap, past that split Part 1/2). Never pad, never cut a step that people need.

## Optional elements (include only if the source supports them)
- Requirements: fold into the hook line ('You can do it solo').
- What goes wrong / mistake to avoid: a clause inside the where-step, not its own beat.
- Proof/effort numbers (how long, how many tries): only if the transcript states them.

## Hard rules
- Read the WHOLE transcript (intro included). List every tip, rank them, and make sure the biggest ones are in the Short before building.
- Every claim, name and number must be supported by the transcript; re-verify against the transcript text (auto-captions mishear names). Unsupported = drop it or say it generically.
- No hedge words ('reportedly', 'apparently', 'supposedly', 'according to'). No disclaimers or credit text on the video. Credit line only at the END of the description ('Guide via <channel>: <url>').
- Every step needs on-screen proof (footage that visibly matches what the voice says) or it is cut/merged. Check frames around each transcript timestamp (1 fps sheets), 2-3 short sub-clips (4-8 s) per step; zoom up to ~1.15x to enlarge small action and push the HUD out of frame.
- Voice: ElevenLabs Liam (TX3LPaxmHKxFdv7VOQHJ; eleven_multilingual_v2, stability 0.4, similarity 0.75, style 0.35). Daniel is Blue Pill only.
- Title text at top (searchable), numbered yellow step text synced to each step, nothing else on screen. Captions: rely on YouTube's auto-captions, do not burn in (posting directly through the API avoids OpusClip's captions).
- Description: searchable title line, hook sentence, FULL steps as text (including tips cut from the Short), patch stamp ('Works as of <source date>; update if the game changes'), hashtags, credit line last.
- No visible gore, black frames, menus, lobby or loading screens in the cut; first 7 s clean.
- Facts players will rely on: prefer two sources agreeing; if a claim is single-source and unverifiable, soften by choosing generic wording, not hedge words.

## Pipeline notes
- Build scripts: work/walk4_build.py (render), visual_check.py, moment_pick.py, cut_moment.py; upload with yt_upload_gaming.py (channel-guarded, default private), edit with yt_edit_gaming.py (never deletes).
- Download video-only <=720p (section downloads 403); static ffmpeg has no drawtext (PIL PNG overlays) and segfaults on DNS (local files only).
- Measured cost per Short: TTS about 570-640 chars (~$0.12-0.14), render ~41 s, ~3.5-4 min machine time, ~10-12k Claude tokens once automated (estimate), ~3 min of William's review. 10/week ~ $1.40 + ~120k tokens + 30 min review.
- Overlaps with real GTA 6 footage after 11/19: prefer approved streamers' gameplay or our own capture over the guide creator's footage (reused-content risk).

## GTA 6 guide template (William, 2026-11-21; the Paul Walker Eclipse dry run, version A)
- THE RECIPE (William, 2026-11-21): 3-4 walkthrough/secret-location guides a day PLUS 1-2 wow-moment clips a day (approved streamers, proven moments). Guides drive; wow moments are nice. Guide builders: keep the approved-topic queue about 2 days deep (7-8 topics); the wow-moment lane posts at most 2 a day and never takes the slots guides need.
- Topics are approved, sources are not. Pick the best source for an approved topic ourselves; this is a temporary route until William can capture his own GTA 6 footage (own footage then replaces creator footage).
- Voice: fluid, conversational, NO counting ("First, ...", "Then, when you get there, ...", "Once you've found it, ...", "Now just ...", "And if you want to keep it, ..."). Never say "one, two, three" and never number the on-screen text.
- On screen: title only, in the headline style: guide.json "title_lines": [line 1 (yellow Anton), line 2 (white Anton)], e.g. ["PAUL WALKER'S ECLIPSE", "IN GTA 6"]. No step labels (a label without matching proof is worse than none).
- Beats: payoff hook in the first sentence, where (map footage if the source has it), how/route, what to watch out for, how to keep it if relevant, close with "save this route" plus a comment prompt.
- Facts: where creators disagree, find the answer from a third source or on-screen proof before dropping it; a missing step that players need (e.g. where to register) is a gap to close, not to omit. Say plainly when it cannot be closed.
- Letterbox layout (16:9 fitted over blurred copy) is the approved look; the full-screen crop upscales 720p about 2.7x and looks soft.
- Reference look: projects/gaming/refs/tt_mislead_7710367109397712142/RECIPE.md; dry run report: out/eclipse_dryrun.REPORT.md; approved sample: out/0KkxxY3iJjQ.flowA_title.mp4.

## Guide thumbnail / cover template (William, 2026-11-21: style 1 approved)
- Every guide gets a separate full-bleed 1080x1920 cover (it fills the phone screen even though the video is letterboxed on blur). Tool: `guide_thumb.py` (docstring has the guide.json "thumb" block). Outputs out/ID.thumb.png and out/ID.thumb.jpg (<2 MB, for `yt_upload_gaming.py --thumb`).
- Look: ONE source frame cropped tight to 9:16 with the subject large (x0 picked so the subject is centred), light bottom fade, two-line headline at the bottom (line 1 white, line 2 yellow, heavy italic Anton, each line stretched to the full width, thick dark outline + shadow). No GTA VI logo (William: it looks terrible), no credit text, no arrows unless asked.
- Wording: line 1 = who/what family ("PAUL WALKER'S", "FREE", "SECRET"), line 2 = the thing ("ECLIPSE", "ROCKET LAUNCHER"); two to four words per line; payoff words, not the full title. Do not copy another channel's exact wording.
- Optional white-bordered inset card (map, weapon card) above the headline for guides where the item card or map is the proof.
- Pick the frame where the subject is clear and fits a 405 px wide (of 720) crop: cars from behind/3/4 on a road, weapons in hand or the item card, locations with the landmark. Workers report 2-3 "cover frame candidates" per guide.
- The 720p source is soft when cropped to portrait; own capture later replaces it.
- Reference approved sample: out/0KkxxY3iJjQ.v2.thumb.png.
- Delivery (William, 2026-11-21): a custom thumbnail shows on the channel page and in search, not in the Shorts feed; William still wants it on every guide because that is how people browse the channel. `guide_make.py upload` now attaches out/ID.thumb.jpg automatically (builds it from the guide.json "thumb" block if missing). The Shorts feed itself uses the video's own frames, so keep the first second of the video a clear, clean frame of the subject.
