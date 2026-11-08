# USER.md - User Model

Format: `<!-- observed: YYYY-MM-DD | status: active|superseded -->` then one imperative directive. On change, mark the old one superseded; no contradictions. Durable facts go in MEMORY.md. 4,000-character budget.

## Directives

<!-- observed: 2026-10-23 | status: active -->

- Always favor clean experiments and measured evidence over short-term money or volume (clips).

<!-- observed: 2026-10-28 | status: active -->

- Approve clips myself (Morpheus) via `--approve` in `projects/clips/pipeline/clip_job.py`, weighing input from all agents first (Editor's notes, Scout's research, Strategist's briefs in `projects/clips/strategy/`). William gets summaries only (clip, platform, time, link), never per-clip approval requests. Escalate only: a new campaign to join, a rule conflict, money, accounts or legal terms, an unapproved streamer, a clip rejected twice.

<!-- observed: 2026-10-28 | status: active -->

- Focus on TikTok (William, 2026-10-28; campaign project only, NOT projects/opusclip): no Instagram or YouTube variants, scheduling or submissions until he says TikTok has real traction. Existing IG/YouTube posts stay up. Never post outside the Buffer route without his explicit go.

<!-- observed: 2026-10-23 | status: active -->

- Own the "go" for routine clip work (Editor jobs, rendering, scheduling) on campaigns William already joined, campaign-supplied footage only. It does not cover joining campaigns, YouTube, money, accounts or legal terms.

<!-- observed: 2026-10-28 | status: active -->

- Submit each live TikTok link to its Whop campaign within 5 minutes of going live (Whop rejects after 30 min; TikTok account must be linked in Content Rewards). Link paste only; stop and tell William if anything else is asked.

<!-- observed: 2026-10-28 | status: active -->

- Submit to Vyro only TikToks, only to Total Drama Roblox (MW4 locked), at post time: best 2 go in when live; 3rd slot for a post running early (~1,000 views in hour 1, read via yt-dlp). Vyro counts only post-submission views and approves at 5,000 of them (Vyro chat), so late submission forfeits views. Only "Submit post" > "Use a link instead"; once per post; never Join/payouts/settings. Never delete a pending submission (wrong row deleted 2026-10-28). On a "wait before posting again" dialog, stop and log.

<!-- observed: 2026-10-28 | status: active -->

- Post at most 2 TikToks per day, 4+ hours apart, from 2026-10-29 for 7 days (Strategist's recommendation, William agreed); log TikToks in the previous 4 hours with each post.

<!-- observed: 2026-10-22 | status: active -->

- Send any video preview he asks for as a file (forceDocument on Telegram); in-chat video looks stretched on his phone.

<!-- observed: 2026-10-22 | status: active -->

- Automate everything except legal acceptance; keep him out of routine runs; report outcomes honestly, including failures.

<!-- observed: 2026-10-24 | status: active -->

- Join campaigns only via `projects/clips/JOIN-PROCEDURE.md`: package on Telegram, he replies "Accept", I restate campaign, creator, rate, click Join only after "Confirm". Silence or an older accept is not consent. Stop on any payment, identity or payout prompt.

<!-- observed: 2026-10-28 | status: active -->

- Rank campaigns on likely views (niche fit, footage, runway, audience), not rate per 1k: he distrusts high rates.

<!-- observed: 2026-10-28 | status: active -->

- When he is mobile, message him on Telegram (`telegram:5390086974`) for posts going live, submissions, decisions, blockers, results. Short; no no-news pings.

<!-- observed: 2026-10-28 | status: active -->

- Treat profanity as acceptable ("clean audio" means audio quality; swears give shock value). Still apply each campaign's brief rules (no slurs, NSFW, FaZe, politics, minors).

<!-- observed: 2026-10-30 | status: active -->

- Never tap Appeal on a TikTok restriction (hs3-01 flagged 'unoriginal content'): William said no appeal. Fix the format instead.

<!-- observed: 2026-11-03 | status: superseded by the 2026-11-06 Project Red Pill entry below -->

- Project Red Pill (William's name, 2026-11-03) = the OpusClip/YouTube experiment in projects/opusclip; use the name to keep it separate from the TikTok/campaign project. Rules: OpusClip score threshold is >= 80 (William, 2026-11-07; supersedes 90 from 2026-11-03 and 9.7; score did not predict views in the log, so pick clips by what is getting views and keep tracking; API scores are 0-100 curved integers): at or above 80 a clip is a posting candidate; below 80, deliberate with William and Strategist. Fact-stating clips (GTA 6, news) still get a human accuracy pass; before posting a batch, audit whether the clips will actually perform. This project is YouTube-first (William, 2026-11-03): the main goal is growing a YouTube channel, and its matching TikTok account only drives viewers to it. The campaign project is unchanged. Source channels come from Strategist's niche picks, not top creators. William may revise the threshold later. Permission policy (William, 2026-11-03): ignore source permission unless a wait rule (e.g. a 24-hour rule) is plainly posted by the source; if one is, respect it and wait before posting. Then be first: have the clip generated and approved during the wait and schedule it (opus.py schedule --at) to go live as soon as the wait expires (source upload time + wait, plus a few minutes of buffer). Lead lanes: creator/streamer moments AND gaming; news and AI make-money are tests. GTA 6 is a HUGE push (plan: projects/opusclip/gta6-push-plan.md; credit cap 450; YouTube Shorts 3/day from 11/10 and 4/day 11/19-21; TikTok 2/day, 3 on 11/19-20, revert to 2 on any warning). No watermark on Red Pill clips: leave OpusClip watermark off as generated (William, 2026-11-03, supersedes the keep-watermark note). Rockstar footage is allowed for GTA 6 clips (William, 2026-11-03).

<!-- observed: 2026-11-03 | status: superseded by the 2026-11-06 Project Red Pill entry below -->

- Project Red Pill is a LEARNING experiment (William, 2026-11-03, 'imperative'): the goal is to find what works (which niches, which video types, which formats and hooks), not to back a specific creator. Always track every post's results and what we did right and wrong; keep the experiment log and LEARNINGS.md current (projects/opusclip/experiment-log.csv, projects/opusclip/LEARNINGS.md), vary niche/type/format on purpose so results are comparable, and keep testing until a niche or video type can be pinpointed to focus on. Source creators are interchangeable test material; never treat a creator as the strategy. Hook-text test (frozen plan: projects/opusclip/hook-test-plan.md) runs 11/6-11/8; discuss results with William before adding enableAutoHook. TikTok for Red Pill = wrdclipz TikTok Business via OpusClip (not @rvclips6); posting only when William releases it, except the 4 hook-test posts he approved.

<!-- observed: 2026-11-06 | status: active -->

- Project Red Pill = the OpusClip/YouTube project in projects/opusclip, separate from the TikTok/Vyro campaign project (projects/clips and its Strategist, Editor and Scout agents), which is unchanged. Current direction (William, 2026-11-06): wrdclipz YouTube is a NEWS channel. Clip official-source coverage of breaking stories (sheriff, police, NTSB, FAA, NWS and other agencies) and post fast; do not cast a wide net or wait a month. Gaming is a separate channel William is creating, with its own project. The single source of truth is projects/opusclip/NEWS-PLAYBOOK.md; learnings are in projects/opusclip/LEARNINGS.md and every post is logged in projects/opusclip/experiment-log.csv. If anything disagrees with the playbook, the playbook wins. Standing rules: OpusClip score >= 90 to post; watermark off; never post OpusClip's auto title or description unchecked (rewrite to the facts, attribute to the agency); safety rules in the playbook never relax (no visible blood or gore and nothing that is a sure YouTube takedown; shocking real footage is WANTED, William 11/6: a person shot or down without blood, 911 calls, dispatch and victim distress audio are all allowed, steer into it; no motive as fact, allegations as allegations, child-abuse stories blocked, politics held for William); officially released bodycam is allowed (11/6); TV-network or TMZ-type video only with William's explicit approval first (official agency sources are the priority); celebrity arrests and similar celebrity news are IN SCOPE for wrdclipz (William, 11/6: 'the kind of stuff I want to lean into'), so do not downgrade them as a weak fit, but still raise copyright/Content ID risk and ask for approval per TV-network clip; no submit to OpusClip without William saying 'clip it' (credits are limited, about 70 a week); the radar (radar_loop.py every 15 min, radar.py sweep every 2 h) alerts only and never submits or posts. When William says post now, post immediately. Story priority (William, 2026-11-06): when a clip we posted starts to do well, prioritize that story for 48 h and follow it up automatically but methodically (posting banked clips, submitting new official sources, within the limits in followup.py, always screened frame by frame first for blood, gore, sure-takedown content and false claims; details in NEWS-PLAYBOOK.md section 2b). Decisions 2026-11-06: 'clip it' authorizes screening and an immediate post (frames checked first); YouTube only; official agency sources first, TV-network/TMZ video only with William's explicit approval; no weekly credit cap for now (info-gathering phase); routine-looking road crashes are flagged, not filtered; GTA 6 clips cancelled; William will say when the gaming channel is live; re-publishing the Google OAuth app is planned after the clean-up (he needs help).

<!-- observed: 2026-11-07 | status: active -->

- TikTok links William sends (wrdclipz news lane) are story signals: things that made him stop and watch. Not every link is a clip order, and many are just reference for what grabs attention (William, 11/7: 'just reference'). Unless he says clip it or asks, do not research or send analysis: log it as a reference, at most one short line back. Find the story and the best video source, tell him in a few lines what it is and what is available, and clip only when it is clearly relevant to the news lane or he says so. When he names the source he wants (e.g. a third-party reupload), use that one, say the copyright risk once, and proceed; do not steer him to a different source. Trim third-party ads or promos off before posting, credit the original creator, keep descriptions to confirmed facts.

<!-- observed: 2026-10-23 | status: superseded -->

- (Superseded: submit-every-post-to-Vyro, now traction-gated; "Accept <full name>"; "Prioritize TikTok", now the focus rule.)

## Related

- [Agent workspace](/concepts/agent-workspace)
