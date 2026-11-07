# Project Red Pill: LEARNINGS (news lane)

Direction (William, 2026-11-06): wrdclipz is a **news channel**. Official-source clips on breaking stories, posted fast. Gaming is a separate channel William creates. The broad niche test (gaming, AI, GTA, creator moments) is finished and closed; its record is below. How the lane runs day to day: `NEWS-PLAYBOOK.md`. Per-post data: `experiment-log.csv`.

## How we learn
1. **Log every post** in `experiment-log.csv`: story, source, how old the source was when we posted, the radar signal that found it, OpusClip score, title, then results. Write the prediction before the result.
2. **Metrics that count.** Views are weak (Shorts counts any start). Use average % viewed, swiped-away rate, impressions, traffic source and subscribers from YouTube Studio. Public view counts are read by the tracker; the rest comes from William's Studio screenshots. Read at 24 h, 72 h, 7 d.
3. **Pool before concluding.** One clip is noise. Label every conclusion with n and say "directional" until n >= 6 comparable clips.
4. **Questions the news lane must answer:** how much does speed (source age at post) matter; which story types travel (disaster, crime briefing, court, weather, other); official briefing versus other formats; clip length and title style; posting hour.
5. **Write the why** for every clip with results (topic heat, speed, hook, length, face, platform).
6. **Safety rules never relax** (list in `NEWS-PLAYBOOK.md`).

## What we have learned (newest first)
- **2026-11-06, directional (n=2 clips, one topic): the Palm Beach Learjet crash out-reached everything else by about 150x.** YouTube Studio, 28 days through 11/5: Learjet 60 crash clip 1,315 views (avg view 0:19, 70.4%); NTSB debris briefing 1,243 views (0:35, 96.4%); next best is Monkey vs alligator at 7. The audit predicted NTSB would under-perform; wrong. The NTSB clip has no hook, face or overlay and still held 96% of viewers, so on a hot topic a plain primary-source clip can be enough. The Learjet clip was posted before the experiment (origin and source unrecorded). Both ride one story, so topic heat and format are not separated. Evidence rows: NTSB 11/4 11:00, Learjet 11/3.
- **Pending:** the two Citibank clips (11/6 11:41 and 12:29, official HCSO source) are the first fast-lane test. Read at 24 h and 72 h; compare to the Learjet pair; record source age at posting (about 20 to 27 h).

## Pre-pivot record (11/3 to 11/6, closed)
Tiny reach on everything that was not news. YouTube Studio 11/5: Monkey vs alligator 7 views (78% viewed), monkey sacrifice 4 (65%), crate through the hell cave 2. GTA 6 and AI clips had not yet shown reach. No pattern can be claimed from these (n of 4 to 7 views each). Conclusion kept: on this channel today, non-news clips got almost no distribution; news clips got about 1,300 views each. The cancelled hook-text test never produced a result and is closed.

## Mistakes and fixes
- 2026-11-03: scheduled a clip a day late (UTC conversion). ET is UTC-5 after DST ended 11/1: 11 AM = 16:00Z, 5 PM = 22:00Z, 10 PM = 03:00Z next day. Print the converted ET time of every schedule and check the list after each batch.
- 2026-11-03: OpusClip API returns HTTP 429 in bursts; space calls 8 s apart.
- 2026-11-03: the agent browser cannot sign in to OpusClip (Google blocks automated browsers, Cloudflare human check); editor work needs William's own browser.
- 2026-11-06: OpusClip's auto title and hashtags can misstate the facts (one said "training scenario" for a real shooting). Always read the clip transcript and rewrite the title and description before posting.
- 2026-11-06: the radar loop cannot see stored secrets (the YouTube key) when run by the scheduler as a stream; it must stay key-less. The agent adds key-backed numbers afterwards.
