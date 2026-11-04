# Project Red Pill: LEARNINGS (living document)

**Purpose (William, 2026-11-03):** find what works, not who to clip. Which niches, which video types, which formats and hooks get views, retention and subscribers on a small YouTube Shorts channel (wrdclipz), with the matching TikTok only as a feeder. Creators are interchangeable test material. Keep testing until one niche or video type can be pinpointed to focus on. Every post gets tracked; every win and miss gets a written reason.

Files: `experiment-log.csv` (one row per post, attributes + metrics + why), `hook-test-plan.md` (frozen hook-text test), audits in `audit-*.md`, strategy in `strategy-*.md`.

## How we learn (rules)
1. **Log before posting.** Every scheduled post is a row in `experiment-log.csv` with niche, content type, format, hook type, hook text Y/N, OpusClip score (curved + raw /40), group (core pick / control / hook test), and the audit's prediction. Predictions are written BEFORE results.
2. **Dimensions we compare** (one at a time where possible): niche (gaming, GTA 6, AI/tech, news, streamer/creator moments, others later); content type (funny moment, news commentary, explainer, reaction, primary source); format (gameplay vs talking head vs screen recording; overlay Y/N); hook type; clip length; posting slot; OpusClip score band (>=90 vs <90 control).
3. **Metrics that count** (Shorts count any start as a view, so raw views are weak): YouTube average % viewed, viewed vs swiped away, impressions, subs gained; TikTok average watch time / length, 2 s retention, followers. Read at 24 h, 72 h, 7 d. Views are context, not the outcome.
4. **Judge niches by pooled results, not single clips.** One clip is noise (our one TikTok outlier was 40x the median). Need >= 4 to 6 clips per niche/type before calling a pattern; label every conclusion with n and say "directional" until n is big enough.
5. **Diversify on purpose.** Each weekly batch should include at least 3 niches/types so comparisons exist. Do not over-invest in a niche from 1 to 3 good clips.
6. **Write the why.** For each clip with results, fill `why_it_did_or_didnt_work` (hook, premise, face, length, topic heat, slot, platform) and `result_vs_prediction`. Record mistakes here too (below).
7. **Safety rules never relax for a test** (accuracy on facts, no distress audio, no unverified claims about named people, posted wait rules).

## Coverage so far (as of 2026-11-03 night, 17 posts scheduled 11/3 to 11/9)
| Niche / type | Posts | Sources | Notes |
|---|---|---|---|
| Gaming: co-op funny moments | 6 YouTube + 2 TikTok (incl. hook test) | SMii7Y only | single source: confounded with the creator |
| AI / make-money tech: talking head + screen | 4 YouTube + 2 TikTok | NateHerk only | single source |
| GTA 6 news commentary | 3 YouTube | T5G2, TmarTn2 | pre-load/launch push comes 11/10 to 11/22 |
| News (primary source) | 1 YouTube | NTSBgov | prediction: under-perform |
| Streamer / creator moments (a lead lane) | 0 | none | gap: xQc held (official-channel check), Mizkif closed (Klein rumor) |
| Breaking news / gossip, sports, business, others | 0 | none | untested |

**Gaps to fix in the next batch:** (a) more than one source per niche, so we can separate niche from creator; (b) a real streamer/creator-moment sample (the other lead lane); (c) at least one or two untested niches; (d) GTA 6 launch-week content from pre-load through 11/22.

## Open experiments
- **Hook text (11/6 to 11/8):** 4 clips, hook version on one platform, plain on the other, counterbalanced. Frozen rule in `hook-test-plan.md`; verdict ~11/11. Directional only; discuss with William before touching `enableAutoHook`.
- **Score control (11/5, 11/9):** two clips scored 85 (SMii7Y crate, Nate AI slop) vs same-source clips >= 90. Question: does the 90 cutoff predict anything? Small n; read together with later clips.
- **Audit predictions (72 h, YouTube Shorts):** over-perform = monkey alligator, monkey sacrifice, GTA cops; under-perform = Nate "Make it better", NTSB debris, xQc Ford (xQc not scheduled, so score the first two plus any replacement). Holds if at least 2 of 3 land in each group.

## What we have learned
- (Nothing from results yet. First posts go live 11/3 10 PM ET.) Record the first lessons here as they arrive, newest first, each with n, date, and the evidence row(s) in `experiment-log.csv`.

## Mistakes and fixes
- 2026-11-03: scheduled the monkey-sacrifice clip a day late (UTC conversion: ET is UTC-5 after DST ended 11/1; 11 AM = 16:00Z, 5 PM = 22:00Z, 10 PM = 03:00Z next day). Caught the same hour, cancelled and rescheduled. Rule: print the converted ET time of every schedule and check the list (`GET /api/publish-schedules?q=byPage`) after each batch.
- 2026-11-03: OpusClip API returns HTTP 429 when schedules are created in bursts; space calls 8 s apart and retry after the stated delay.
- 2026-11-03: the first audit missed TmarTn2 because its clip file was not on disk yet; check all project files exist before an audit.
- 2026-11-03: the agent browser cannot sign in to OpusClip (Google blocks automated browsers, Cloudflare human check); editor work needs William's own browser.
