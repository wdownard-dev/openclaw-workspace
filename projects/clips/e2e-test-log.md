# End-to-end flow test (started 2026-10-23 ~8:10 PM ET)
Goal (William): run the full chain campaign -> clip -> kit -> hosting -> scheduled posts on TikTok/Instagram/YouTube -> tracking/reporting, and record where the process breaks or needs a human. Vyro submission is out of scope for this test. Vyro and posting limits are known and handled separately.

Stage table (time, who, outcome, human touches, gaps):

## Stage 1: campaign sourcing (Scout) - DONE, ~4 min, no human touches
- Result: 10+ open campaigns read; MW4 (joined, 13 days, 26% paid, $1.50/1k, TikTok/IG/YT accepted) chosen for the test. New: Total Drama Roblox (Sinjin) $2.50/1k, not joined. Valorant Champs 6 days left, not joined.
- Gaps found:
  1. Vyro has no API/export; reads are DOM scraping via the browser tool (browser snapshot is useless on Vyro; URL lags a click; list rendered twice desktop/mobile). Works only with one pinned tab.
  2. Footage is never a plain URL; every source is a Frame.io share needing Playwright click-through. Only MW4 and Valorant are downloaded. Footage for the other open campaigns is unverified.
  3. Joining a campaign and payouts remain manual (legal terms). Scout cannot act on new campaigns without William.
  4. Vyro rules: "automated posting" listed as spam example; "bots, scrapers, or automation to collect or manipulate platform data" (s.8) could cover scripted Vyro reads. Unresolved risk; support question drafted at outbox/vyro-support-draft.md, not sent.
  5. Scan is reliable only when run from a spawned Scout with one tab; the daily scheduled job previously failed.

## Stage 2: clip selection, render, kits (Editor) - DONE, ~9.5 min, no human touches
- mw4-07 (default pattern, 39.3 s, 797-836 s of source) and mw4-08 (TEST: funny premise, shorter, 22.6 s, 169-192 s). 1080x1920, h264 60fps, AAC. Kits at campaigns/mrbeast-gaming-mw4/kits/.
- Gaps: (1) no ffprobe on host; (2) format_short.py formats but does not cut, cut step is an ad-hoc ffmpeg command, not reproducible (should be a script); (3) moment selection is manual, transcript timestamps loose and no speaker labels, relies on frame contact sheets, cannot listen to audio; (4) no check that the hook matches the first 3 s on screen (needed a re-render of both); (5) software encode of 7.5 GB 1080p60 source is slow; (6) kit text, candidates.md, playbook.md written by hand; (7) Buffer cannot set Shorts thumbnail or paid-partnership label; (8) hook for mw4-08 leads with a language premise: open decision for William.

## Stage 3: hosting + scheduling (Morpheus) - DONE, ~3 min, no human touches
- Cloudinary unsigned upload of both clips (31 MB, 25 MB), public 200 verified. Buffer createPost x4 returned status=scheduled: mw4-07 TikTok+IG Sat 2026-10-24 12:30 PM ET; mw4-08 TikTok+IG Sun 2026-10-25 7:00 PM ET. Post ids in buffer-posts.json, rows in results.csv.
- Gaps: (1) Cloudinary files cannot be deleted without the API secret (manual cleanup); (2) post ids/results rows are written by hand (a single publish script would fix this); (3) William's review happens in Buffer, there is no approval step in the chain besides that; (4) YouTube not included: API uploads are locked private pending audit, and the channel shows zero distribution.

## Stage 4: tracking/reporting - already live
- Every 3h silent check (YouTube + Buffer) with Telegram only on go-live/error/first views/5,000; 8:15 AM digest includes all platforms. First live data expected after mw4-01 posts at 9 PM tonight.

## Gap closed: single script (2026-10-23)
- pipeline/clip_job.py: spec JSON -> cut, format, verify (1080x1920, length, audio, contact sheet), thumbnail, host, Buffer schedule, log. A full run from an existing cut takes seconds; cut+render of a 23 s clip took 76 s on this host (earlier ad-hoc run was 3.5 min for two clips).
- Tested: dry run; live run to a throwaway 'zz-test' clip (TikTok + Instagram scheduled Nov 2); idempotent rerun; refusal on bad hook/hashtags/engagement bait/too-soon schedule; --unschedule deleted both Buffer posts. Test rows removed from results.csv/buffer-posts.json.
- Found: Buffer has deletePost/editPost, so scheduled posts can be fixed before they publish (useful for the mw4-08 hook decision).
- Remaining from the gap list: moment selection and hook-to-frame check (still judgement), Vyro automation risk, Cloudinary cleanup, YouTube path.

## Stage 5 (new campaign): join + footage test, Total Drama Roblox (Sinjin), 2026-10-23
- Package: Scout (Haiku) read dialog + both general terms in ~5 min; I verified its flagged quotes against saved text, and dropped one claim ("72 hours processing") that was not in the saved terms (Haiku error caught by checking). Sent to William on Telegram with files.
- Consent: William replied "Accept Total Drama Roblox (Sinjin)" 30 s after the package; matched the procedure; I clicked Join once after confirming title/terms. No payment/identity/payout prompt. Joined confirmed on My campaigns. Age 18+ was asked, not separately confirmed.
- Join gaps: Vyro accessibility snapshot is empty so clicks are by coordinates found via evaluate (brittle); URL lags one click (Flamingo slug shown); this is Vyro UI automation under the "automation" wording risk.
- Footage: fetch_frameio.py worked on a second campaign's link: 56m37s file, proxy 640x360 824 MB in 23 s, 1080p original 1.78 GB in 67 s. Gaps: (1) first run launched from a detached subshell died silently with no log/file (rerun in a managed background exec worked); (2) --smallest gives a 360p proxy, fine for transcript/moment search but unusable for the final render, so the flow needs "proxy for search, original for render"; (3) Frame.io menu offers Original 1080p plus proxies, picked by size text (fragile); (4) footage is a 56 min Roblox game recording with a facecam overlay: different layout from MW4, so format_short.py's blurred-background layout may need a check for the facecam.

## Stage 6: TDR clips (Editor, 2026-10-23 ~9:03-9:10 PM ET, about 7 min wall clock, no human touches)
- Work: brief.md from the join package, 2 specs (tdr-01 soup gag 1957.8-1981.4 s, default pattern; tdr-02 TEST host-dialogue contrast 2672.2-2700.0 s), 2 kits (TikTok/IG only), `clip_job.py --until thumbnail` for both. Lint passed first time; render took ~1 min per clip (software encode of the 1080p source), verify OK (1080x1920, 23.6 s and 27.8 s, audio -20.3 / -18.4 dB).
- Time split (approx): transcript read + moment search ~3 min (60 KB of text, 1,526 segments), contact sheets + frame checks ~2 min, brief/specs/kits ~1.5 min, two renders ~1 min each.
- Layout check (format_short.py on a facecam game recording): works, no change made. The blurred-background layout keeps the whole 16:9 frame, so the facecam (left edge, ~20% width) is fully visible, not cropped. Cost: the game band is only ~600 px tall on the 1920 canvas, so small in-game text (chat bubbles) is small on a phone; host dialogue boxes are readable. A game-region zoom option would help but was not needed.
- Gaps found:
  1. whisper base.en transcript on multi-voice Roblox voice chat is poor (misheard names, repeated "No." x50 hallucination at ~3250-3272 s, no speakers). Moment search needed frame contact sheets to prove anything. Editor cannot hear audio, so every spoken hook is unverified; I picked hooks with on-screen proof (chat bubble, host text boxes).
  2. The facecam in this file alternates between two different people and has black-box stretches (e.g. 1744-1800 s). Speaker attribution is unsafe, and a black facecam would look broken. No script checks for it.
  3. Whisper segment times are about +/-2 s off: cut points needed a frame check each (a loading screen sits just before the host intro at ~2670 s; the campfire cutscene starts at ~1982 s).
  4. tdr-02 contains ~1 s of black game screen (scene transition, around 14 s in). Left in; trim if reviewer dislikes.
  5. clip_job.py `verify` contact sheet shows frames at 0,1,2,3,5,10 s only; clips that pay off later (tdr-01 reveal at ~9.5 s) need an extra frame. I extracted one by hand.
  6. Kit thumbnail rule is YouTube-oriented; for TikTok/IG I left the pipeline's default 0.6 s frame and suggested an in-app cover time. Buffer cannot set the native paid-partnership label (Morpheus/William must tick it).
  7. Vyro dialog for Sinjin does not say to submit immediately (MW4's does): unverified.

## Stage 7: batch 3 (Editor, 2026-10-23 ~9:30-10:00 PM ET): mw4-09, mw4-10, tdr-03, tdr-04, TikTok + Instagram only
- Work: 4 specs, 4 kits, `clip_job.py --until thumbnail` for each (lint ok first time; render ~70 s per clip; mw4-10 and tdr-04 re-rendered once each after checking the first 0.3 s, see gap 4). No approval, hosting, scheduling, posting or Vyro.
- Pipeline fix (clip_job.py, verify stage only; lint, approval and hosting untouched): (1) `contact_full.jpg` = 8 evenly spaced frames across the whole clip, 4x2 grid at 360x640; the old 6-frame `contact.jpg` is unchanged. (2) `black_runs()` runs ffmpeg blackdetect (d=0.5 s, pic_th 0.92, pix_th 0.12) on the right 75% of the source-format `cut.mp4` (so a live facecam on the left does not mask a black game view); runs are printed as a WARNING with clip-time ranges and written to `jobs/<id>/blackdetect.txt`; verify still passes (flag, not failure). Tests: synthetic file (2.0 s test pattern + 1.2 s black + 1.0 s pattern + 0.3 s black) gives exactly one run (2.0-3.2 s), the 0.3 s black is ignored; a re-render of the tdr-02 range under a throwaway id gave "no black run over 0.5s" (checked: the single dark frames at 4.8/8.7/11.2/14.0 s are 1 frame each, not a >0.5 s run) and a correct contact_full.jpg; throwaway job and previews removed.
- Gaps found:
  1. Stage 6 gap 4 correction: tdr-02's "~1 s of black" is single black frames (1/60 s each at ~4.8, 8.7, 11.2, 14.0 s), not a 1 s run; blackdetect now proves it.
  2. blackdetect cannot see the first-frame fade-in or one-frame cuts. tdr-04 opened with a ~0.25 s fade from black (luma 19/38/53 -> 87) and mw4-10 opened with a 0.3 s different shot (luma 115 then 46 in the studio). Both were caught by reading per-frame luma (signalstats) by hand and fixed by moving the start; a "check the first 0.5 s for luma jumps / fades" step in verify would remove that manual step. Not added (scope).
  3. Chat-bubble moments are hard to find: the transcript has no signal for them and bubbles are tiny at 480-wide contact sheets. I wrote a one-off detector (scripts under workspace-editor/scripts/bubbles.py, white pill blobs at 1 fps) that found ~20 candidate ranges in the 56-min file; only one (2767-2771 s, "they took my v oice") was both readable and a gag. Worth turning into a `find_bubbles.py` helper if TDR continues.
  4. format_short.py: game band is ~600 px tall, so chat bubbles and host boxes are small on a phone; hooks must repeat the proof text. A game-region zoom option remains the best fix (same as Stage 6 gap).
  5. Whisper timestamps in the first 700 s of the TDR transcript come in uniform 1-s segments (quality visibly worse); I relied on frames for every cut point. mw4 transcript segments in 1300-1400 s are loose too.
  6. The ranges of mw4-09 (ends 972.4) and mw4-02 (starts 972.6) are adjacent in the same scene; `--approve`'s overlap check passes (strict overlap only) but the two posts tell consecutive beats. Morpheus may want to space them or accept.
  7. results.csv logging is done by the `log` stage only after hosting; nothing for these four rows exists yet, so the 3h tracker will not see them until Morpheus runs the full job.
