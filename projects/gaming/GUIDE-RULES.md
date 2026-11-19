# Guide / walkthrough Short rules (wrdgamingclipz, v1 from the Fortnite Pirate Shop Token test, 2026-11-16)

Proven example: out/walk_v4.mp4 (live: https://www.youtube.com/shorts/iSgpSI7KrJQ). Method: 'medium rework' = our own script and our own voice over the source guide's footage (their audio muted).

## Required elements (in this order)
1. HOOK = goal + payoff in the first 2 s ('Here's how to get X'). Best: open on a proof shot (the reward screen).
2. SETUP / LOADOUT FIRST: anything you must equip or do before starting goes before location (the sprite lesson).
3. WHERE to go, then HOW to get it in 2-3 steps.
4. CLOSE with effort/expectation plus a comment prompt ('Got X? Drop a comment and tell me how many ... it took you').
5. One goal per Short. Script 90-115 words, 35-45 s. A bigger guide becomes Part 1/2.

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
