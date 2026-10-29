# PLAN.md consistency review, 2026-10-28 ~8:20 PM ET (Morpheus)

Scope: PLAN.md (224 lines, 60 KB), USER.md directives, Editor/Scout AGENTS.md, pipeline/README.md, live Buffer state. Nothing was changed except this file.

## A. Real conflicts (act on these)
1. **Same-minute collision, Thu 10/29 7:00 PM ET:** hs3-03 TikTok (moved there tonight) and tdr-03 TikTok are both scheduled on @rvclips6 at 23:00Z. Needs one moved.
2. **TikTok-only direction vs scheduled Instagram posts:** Buffer still holds IG posts for tdr-03 (Thu 7:30 PM), mw4-10 (Fri 7:30 PM) and tdr-04 (Sat 1:00 PM). The 8:08 PM direction says no new IG scheduling. Decide: delete them or keep as already-approved.
3. **Approval rule (top of PLAN.md):** "Human approval (via Telegram) before every upload" vs USER.md 2026-10-23 delegation (Morpheus approves; William gets a summary). The header was never updated, so a new reader (or a restarted agent) will wait for approvals William no longer wants to give.
4. **Vyro submission rule:** USER.md says submit every live TikTok to Vyro as soon as it goes live. The Strategist brief (open decision 1 and experiment 1) recommends submitting only traction-gated posts. William approved freeing the slots but did not decide the policy, so both rules are live.
5. **Vyro approval mechanics are stated three ways:** (a) PLAN 10/22: block lifts when one post is approved; (b) USER.md 10/28: approval only at 5,000 views; (c) PLAN 10/24: views count from submission even while pending vs the campaign dialog "only approved posts count". Unresolved, and all three are in the file.
6. **Posting cadence:** PLAN says new accounts 1-3 posts/day/platform and Editor was set to ~5/day; tonight is 3 HardScope TikToks in 4 hours. Strategist recommended a cap of 2/day. No decision recorded.
7. **mw4-10 (Fri), mw4-12, mw4-13:** MW4 is locked for new posts and 97% paid; these posts cannot earn. Strategist open decision 5 is unanswered. Also unverified whether mw4-09 went out tonight.
8. **Whop rules not in brief.md:** campaigns/hardscope-ep3/brief.md and candidates.md assume a plain link paste. Confirmed tonight: account must be linked inside Content Rewards (TikTok done, IG not) and the clip must be submitted within 30 minutes (William's rule: 5). Not recorded in the brief.

## B. Stale text that will mislead (update or archive)
9. Title and goal: "Shorts from streamers + GTA 6 launch", Twitch-only, channel sticks&bones, YouTube-first. Reality: campaign clips on TikTok via Buffer for Vyro and Whop.
10. Phases 1-5 (GTA 6 timeline, streamer outreach, preload week) and "Open questions" are unchecked tasks nobody is working on; streamer outreach is dormant (20 contacted, 1 "replied", 0 approved).
11. "RESUME HERE (10/22)", two "TOP PRIORITY" blocks, and "TOP PRIORITY TOMORROW (10/23)" are outdated pinned sections. Item 1 (Buffer) is done but still unchecked.
12. AUTOMATION CHAIN and "Honest limits": says William posts manually and pastes TikTok/IG links. Buffer now posts and Morpheus submits.
13. VYRO EXPERIMENT section: Valorant campaign (closed), "ONLY hashtag #valorantchamps", YouTube Shorts as the platform. Also "no other hashtags/mentions" in Editor's AGENTS.md vs HardScope's required #unpacked + @hardscope.
14. MONITORING: "NOT covered: TikTok/Instagram view counts" and results-feed item 3 are out of date (sync_buffer.py exists, but lags and results.csv views_48h is blank).
15. Log ordering: 10/21-10/24 entries run newest-first, 10/28 sections run oldest-first at the bottom. Easy to read the wrong end as "latest".
16. The 10/28 6:15 PM entry lists IG schedule times that were later deleted; the 6:05 entry says "submit Whop link at 7:50". Correct only by reading downstream entries.
17. Ops items with a date: YouTube OAuth app still in Testing (tokens expire about 10/28, i.e. today) and the audit watcher still runs, although YouTube is paused. NUC cutover status is unrecorded (last entry 10/24: waiting on William).
18. Hosting cleanup: Cloudinary files are removed manually; none removed since 10/23.

## C. Agent instructions out of sync with PLAN
19. **Editor AGENTS.md:** YouTube Studio manual-upload kit, goal "5,000 views per post" (Vyro) vs HardScope's 2,000-view minimum payout, no mention of Whop, the 30-minute window, per-platform variants, or TikTok-only focus.
20. **Scout AGENTS.md:** "YouTube Shorts clips project", no mention of TikTok/Whop; PLAN says Scout runs on Haiku.
21. **pipeline/README.md:** stage 5 `publish_job.py ... after a clear yes from William` (YouTube) vs delegated approval; "Still manual: Vyro submission" vs standing OK.
22. **Strategist (new):** does not yet know the TikTok-only rule.

## D. Proposed fix (needs William's go on A3-A7)
1. Today: move tdr-03 or hs3-03 off 7:00 PM; delete or keep the three IG posts.
2. Rewrite the top of PLAN.md into a one-screen CURRENT STATE (goal, platforms, approval rules, submission rules, cadence, open decisions) and move everything else into `archive/PLAN-2026-10-22-24.md`, keeping the log intact.
3. Add Whop rules to brief.md; add a TikTok-only/Whop/30-min section to Editor and Scout AGENTS.md; update pipeline/README.md; add the TikTok rule to Strategist.
4. Decisions to record: Vyro submission policy (every post vs traction-gated), cadence cap, mw4-10/12/13, MW4 footage after budget.

## Resolution log (2026-10-28 ~8:45 PM ET)
A1 collision: fixed (hs3-03 -> Thu 12:30 PM). A2 IG posts: deleted (mw4-10, tdr-03, tdr-04). A3 approval rule: USER.md structure confirmed, plus "weigh all agents' input". A4 Vyro submission policy: superseded by Strategist's submit-at-post-time rule (William: yes). A5 approval mechanics: answered via Vyro's AI chat (strategy/vyro-approval-mechanics.md s.5). A6 cadence: 2/day, 4 h apart, 7 days from 10/29. A7 MW4 posts: leave for information. A8 Whop rules: added to brief.md. B9-B22 stale text and agent instructions: PLAN.md rewritten (old file archived), USER.md condensed, Editor/Scout/Strategist AGENTS.md and pipeline README updated. Still open from B: YouTube OAuth in Testing (decide), NUC cutover status, Cloudinary cleanup, results.csv views_48h blank.
