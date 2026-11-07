# OpusClip pipeline: niches, channels, funnel and test (Strategist, 2026-11-03)

Advisory only. I changed nothing: not `channels.txt`, no OpusClip job, no post, no contact. Evidence labels: **[own]** our data, **[V]** read from a primary page on 2026-11-03, **[claim]** third-party or marketing, **[judgment]** mine.

**Answer:** Start the YouTube channel in **one niche: business / startups / AI-business talk** (7 sources below). Plan B is streamer moments. Be prepared for a slow start: our one earlier cold YouTube channel got zero distribution on 6 clipped Shorts, and our TikTok clips get about 80 to 200 views. **Permission is the biggest unresolved risk**, and the 9.7 threshold needs a dry run before it goes live.

## What our own data says
- **[own] TikTok, 18 posts, 10/23 to 10/30:** median 164.5 views, and 1 post above 5,000. By campaign, MW4 (gaming, 90 to 96% male, 18-24, US) had median 385 (n=7), HardScope 171.5 (n=4), Family Guy 30.5 (n=4), TDR 10 (n=3). Confounders: burst posting, campaign timing, footage. Only a hint that gaming audiences reach best.
- **[own] YouTube:** 6 clipped Shorts (mw4-01..06, 10/22) got zero distribution. Cause never investigated (n=6, posted 15 minutes apart, wrong category on one). Check whether that channel is the destination before reusing it.
- **[own] hs3-01** was restricted as "unoriginal, low-quality" (the notice names watermarks and logos). Retention did not predict reach above the seed stage (n=18).
- **No data exists on niche, creator or OpusClip score.** The ranking below is judgment, so treat it as a hypothesis for the test.

## 1. Niches, ranked for a new channel (TikTok as funnel)
| # | Niche | Why (judgment unless noted) | Main weakness |
|---|---|---|---|
| 1 | **Business / startups / money talk** | Viewers subscribe for a repeat dose of ideas; clips are self-contained (numbers, frameworks, contrarian takes); mid-size sources exist; business views are worth more per view [claim: autoclip.dev] | Crowded lane. Narrow it ("startup ideas") rather than "business advice" |
| 2 | **AI / tech / startup interviews** | Newsworthy guests, less clip saturation, sticky audience | Smaller audience; investor-opinion clips can misquote or drift into politics |
| 3 | **Streamer / gaming moments** | Best reach hint in our data (see above), 18-24 male | Weak subscriber loyalty, highest Content ID and brand-safety risk, no permission yet (xQc and 20 other streamers contacted 10/22, none approved) |
| 4 | **Comedy / storytelling podcasts** | Hot-mic, funny-premise clips travel on TikTok (n=1, mw4-08) | Offensive content, music and TV Content ID, weak ad suitability |

One channel should hold one niche. Mixing niches on one channel confuses YouTube's audience matching and the subscribe reason [judgment].

## 2. Channels (all 25 or more checked on 2026-11-03)
**Verification note:** I had no shell, so I could not run yt-dlp. I loaded each `youtube.com/@handle/videos` page in the browser and read subscribers, lengths and views [V]. Run `scout.py` or `yt-dlp --flat-playlist --playlist-end 3` once to confirm before relying on this list. Subscribers and views are snapshots.

**Niche 1: Business**
| Handle | Subs | Recent long-form | Why it suits clipping |
|---|---|---|---|
| @MyFirstMillionPod | 969K | 40 to 125 min, 36K to 146K views | Idea-dense two-host banter, quotable numbers |
| @GregIsenberg | 738K | 31 to 50 min, 55K to 105K | "One-person business" frameworks; mid-size, so permission is reachable |
| @CodieSanchezCT | 2.27M | 13 to 23 min, 61K to 106K | One speaker, easy crop |
| @AlexHormozi | 4.61M | 10 to 52 min, 174K to 778K | Biggest supply of punchy frameworks; most saturated. Uploads about 1 per week, so supply is thin |
| @starterstory | 895K | 12 to 19 min, 46K to 304K | Founder-revenue stories. Partly screen recordings, so check framing |
| @LeilaHormozi | 1.77M | 12 to 68 min, 130K to 333K | Same style as Hormozi; avoid both Hormozis in one batch |

**Niche 2: AI / tech** (@GregIsenberg and @20VC also fit here)
| Handle | Subs | Recent long-form | Notes |
|---|---|---|---|
| @20VC | 225K | 24 to 80 min, 16K to 78K | Frequent uploads, small enough to ask |
| @LennysPodcast | 650K | 37 to 88 min, 39K to 160K | Product and startup how-to |
| @DwarkeshPatel | 1.46M | 25 to 97 min, 167K to 1.6M | Deep Q&A, very quotable; slower pace |
| @Bg2Pod | 106K | 45 to 100 min, 10K to 311K | Infrequent uploads |
| @allin | 1.17M | 40 to 103 min, 62K to 747K | Heavy politics and market opinion; brand-safety flag |
| @peterdiamandis | 543K | 104 to 144 min, 281K to 448K | News roundups |

**Niche 3: Streamers** (all 7 or more verified)
| Handle | Subs | Recent | Notes |
|---|---|---|---|
| @xQcOW | 2.51M | 11 to 86 min | **Only written rule found:** channel text asks uploaders of his Twitch content to follow a "grace period" [V]; also in `clips/permissions.md` (24 h grace, no duplicating his official channels) |
| @summit1g | 832K | 21 to 26 min, 60K to 272K | Posts his own highlights; contacted 10/22, no reply logged |
| @Jynxzi | 7.09M | 30 to 88 min | R6 streamer, high-energy moments |
| @ludwig | 7.1M | 26 to 38 min, 944K to 1.9M | Already produced and edited, so more transformation required |
| @penguinz0 | 18.3M | 8 to 15 min | Commentary on others' content, so clipping compounds reuse; many videos fall under 10 min |

**Niche 4: Comedy podcasts:** @KILLTONY 2.81M (1 to 2 h), @TheoVon 4.8M (1.5 to 2.4 h), @BussinWithTheBoys 743K, @smartless 212K (about 50 to 60 min, the most brand-safe). Not recommended for the first run.

**Dropped (did not resolve):** @DwarkeshPatrick (right handle is @DwarkeshPatel), @AsmonGold, @PowerfulJRE, @PowerfuldJV, @Flagrant2. **@FlagrantPodcast and @NewHeightsShow resolve to unrelated 3-subscriber channels**, so do not use them. **@garyvee** resolves but its uploads are mostly under 10 minutes, which `scout.py` skips. **@mizkif, @TimDillonShow, @H3Podcast, @HasanAbi, @Valuetainment** are excluded for politics, drama or defamation risk. **@MrBeastGaming** footage was permitted only through the closed Vyro campaign.

## 3. Funnel design
**Reality check [judgment]:** the TikTok account has almost no audience (@rvclips6 had 3 followers). At 200 views a clip, a 1% clickthrough is about 2 visits. TikTok will not be the main traffic source for weeks, so **YouTube Shorts must earn its own distribution**. I also could not verify when a TikTok profile may carry a link (the support page would not load). William should check this on the account.

**TikTok formats that give a reason to click (honest only):**
1. **Part 1 / payoff on YouTube:** cut at the setup with an on-screen line like "Full answer on YouTube". The payoff must really exist there (a 3 to 8 min video or Part 2 Short). No bait.
2. **Numbered framework** ("3 things...") with the full list on YouTube.
3. **Contrarian claim + proof,** or a **specific number reveal**.
- Our best post (mw4-08, n=1) named a whole idea in 6 words and was understood on mute. The 10/30 diagnosis found that spoiler hooks and slow openers hurt. Start at the peak, and keep the hook honest to the clip.
- Never write "comment X for the guide" or imply a creator endorses us.

**What the YouTube channel publishes:**
- **Shorts** from the same clips, but with a different hook, caption and title than TikTok. Identical cross-posts are a reuse-flag risk.
- **One 8 to 12 min "best of" video per week** with added commentary, context or voice-over. This is the transformation YouTube's policy wants and it gives viewers a reason to subscribe. Original long-form can come later.
- Credit every source and link the full episode. Use a neutral channel name (not "Hormozi Clips"), no source avatars, **no affiliate links.**

## 4. Risk notes
- **YouTube reused content [V, support.google.com/youtube/answer/1311392]:** borrowed content "you need to change it significantly to make it your own". Reviewers look at the channel's main theme and most-viewed videos. **Permission does not fix this** [claim: Clyper summary of the policy]. Shorts policy [V, answer/12504220] lists unedited clips and re-uploads as non-original, and ineligible for revenue. Monetization is far off anyway (10M Shorts views in 90 days, or 1,000 subs plus 4,000 watch hours). The immediate risks are reach and strikes, not ads.
- **Copyright:** none of the 25 channels I checked has a CC licence on its newest 2 videos or a clip policy in its description, except xQc's grace-period note [V]. Silence is not permission. A DMCA strike from a creator is the worst case (3 strikes ends a channel). **Recommend William decides whether to ask:** mid-size sources first (@GregIsenberg, @20VC, @starterstory, @LennysPodcast, @Bg2Pod). I never contact anyone. Whop and other clipping programs for these creators are unchecked leads. A Hormozi "35,000 clips" figure is a vendor claim.
- **Content ID:** low for talk shows without music, higher for guest B-roll and ad reads. High for streamers (game audio, licensed music). Mute or replace third-party music.
- **TikTok "unoriginal" [own]:** hs3-01's restriction named watermarks and logos. **Check the OpusClip plan adds no OpusClip watermark** (unverified). Full-frame reframing and word-synced captions are real edits, but no threshold is published.
- **Brand safety:** Business has the least (avoid income-claim marketing, crypto and gambling segments, and treat figures as the guest's claim). AI/tech: avoid politics (@allin) and misquoted investor opinions. Streamers and comedy: profanity is fine per William, but avoid slurs, minors, defamation of real people and drug jokes.

## 5. Starting set and 7-day test
**channels.txt (7):** `MyFirstMillionPod`, `GregIsenberg`, `CodieSanchezCT`, `AlexHormozi`, `starterstory`, `20VC`, `LennysPodcast`. This keeps one identity, "startups and business ideas". Roughly 12 or more qualifying uploads per week across them. Run `scout.py --backfill` once, or the first run only records existing videos and yields nothing.

**Plan B (week 2, or a second account pair if William wants a true niche comparison):** `xQcOW`, `summit1g`, `Jynxzi`, `ludwig`.

**Design:** 7 days, cap 2 TikToks/day 4 h apart and 2 Shorts/day (the cadence that fixed our burst problem [own], n=3 signal), so at most about 14 posts per platform. **That is below n=10 per pattern, so the week cannot pick a winning creator or niche.** It can only show whether the pipeline gets any distribution. Hold layout, captions and slots constant, rotate sources, and log score, source, length, hook and slot for every clip.

| Measure (where) | Signal | Dead |
|---|---|---|
| YouTube Short views (Studio) | Median 500 or more, and at least 3 Shorts above 1,000 | Median under 100, repeating the zero-distribution result |
| YouTube subs (Studio) | 10 or more net, or 3 or more subs per 1,000 views | 0 to 2 |
| TikTok views at 24 h | Median 300 or more (about 2x our 164.5 baseline, n=18) | Under 100, or any restriction banner |
| TikTok to YouTube (Studio, Traffic source, External: tiktok.com; TikTok profile link clicks) | 10 or more visits | Under 3 means the funnel is not working yet |

The thresholds are my judgment, set before the data so we cannot move them afterward. Expect clickthrough to be unmeasurable this week. If both platforms are "dead", the next change is a transformation (commentary or weekly compilation), not a new niche.

## 6. The 9.7 auto-post threshold
**Sensible as a starting cut, with conditions.**
- **The score is OpusClip's prediction, not a measurement.** I have seen no OpusClip scores, so I do not know the scale (opus.py does not print it) or what share of clips reach 9.7. **Before the first auto-post:** dry-run 20 clips and report the distribution. Aim for roughly 10 to 25% passing. If more than half pass, 9.7 is not a filter. If under 5% pass, the test starves.
- **The score checks nothing about safety.** Add non-score rules to the auto lane: source must be in channels.txt; at most 1 clip per source video per day; no overlapping segments; hold any clip with a slur, minor, or drug/medical/financial claim (keyword scan); no watermark. Any restriction banner, strike or claim pauses the auto lane.
- **Does the score matter?** Log every posted clip (score, band, 24 h and 72 h TikTok views, 72 h and 7 d YouTube views). After at least 30 posted clips, compute the rank correlation (Spearman). At n=30 it takes about |rho| 0.36 to be real. Range restriction (we only post 9.0 and above) will hide a weak effect, so in week 2 post a small calibration sample: one clip per band (9.7+, 9.0 to 9.69, 8.0 to 8.99) from the same source video.
- **Does deliberation add value?** Compare lower-score clips we approved against the auto lane. If they match or beat it, drop the threshold. If they lose, the score earns trust.

**Deliberation protocol (about 5 min per day, batched once daily):** each clip card carries score, source, OpusClip's one-line reason, and three questions: (1) Does the hook make sense on mute in 3 s, starting at the peak? (2) Is it honest (no spoiler, no misattributed speaker, accurate context)? (3) Is it safe and new (no slurs, minors or claims, not a repeat segment)? **Post** only if all 3 are yes and 2 of 3 reviewers agree. **Fix** (re-cut start or end) once, then re-ask. Otherwise **skip**. Default is skip if no answer within 24 h, and the reason is logged. William is pulled in only for safety doubts or a skipped clip he wants posted.
