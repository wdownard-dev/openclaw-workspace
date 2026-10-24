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
