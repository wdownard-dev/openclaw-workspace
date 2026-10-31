# Why @rvclips6 is not performing on TikTok: diagnosis, 2026-10-30 (Fri evening, updated 8:20 PM ET)

Diagnosis only. Nothing was changed: no pipeline, schedule, post, Buffer, Vyro, Whop or account action. The Appeal button was not used.

## Update 8 PM: what the analytics change
**New #1: change the framing before testing anything else.** TikTok has now enforced its unoriginal-content rule on one of our posts, and all 19 posts share that format. **Pull tdr-04.** The account does not look blocked. The flag does not explain our low views, so the framing fix protects the account first and may or may not raise views.

**Evidence:** William's Studio recordings for 19 posts, read by Morpheus from frames (`2026-10-30-analytics-readings.md`), plus my public page reads at 8:13 to 8:20 PM. Likes are public counts from 7:17 PM. "n/r" means not read.

| Clip | Views | For You % | Avg watch | Full watch % | New followers (Studio) | Likes | Banner |
|---|---:|---:|---|---:|---:|---:|---|
| mw4-08 | 8,524 | ~99 | 12.5 s, 55% | n/r | 78 | 182 | Not confirmed |
| mw4-07 | 760 | 93.9 | 10.0 s, 25% | 10.75 | 0 | 17 | None |
| mw4-16 | 760 | 98.3 | 8.9 s, 51% | 26.57 | 18 | 19 | None |
| mw4-09 | 385 | 97.6 | 13.7 s, 35% | 17.44 | 4 | 4 | None |
| hs3-04 | 343 | 93.9 | 9.8 s, 24% | 12.17 | 9 | 9 | None |
| tdr-02 | 325 | 96.9 | 5.4 s, 19% | 7.98 | 8 | 9 | None |
| fg-02 | 319 | ~98 | 8.5 s, 57% | 30.49 | 0 | 7 | Not confirmed |
| hs3-02 | 264 | 91.6 | 13.3 s, 29% | 15.38 | 4 | 5 | Not confirmed |
| mw4-10 | 223 at ~70 min | 99.6 | 9.8 s, 59% | 29.07 | 1 | n/r | None |
| mw4-12 | 192 | 95.9 | 9.1 s, 57% | 23.47 | 3 | 3 | None |
| mw4-13 | 137 | 90.9 | 12.2 s, 33% | 20.28 | 1 | 0 | Not confirmed |
| mw4-01 | 130 | 70.9 | 5.3 s, 15% | 5.97 | 1 | 1 | None |
| **hs3-01** | 79 | n/r | 10.9 s, 47% | 28.4 | 0 | 0 | **FLAGGED** |
| fg-01 | 48 | Hidden | 8.1 s, 53% | 28.57 | 0 | 0 | None |
| hs3-03 | 48 | Hidden | 2.6 s, 11% | 0 | 0 | 0 | None |
| fg-04 | 13 | Hidden | 8.0 s, 53% | 21.43 | 0 | 0 | None |
| tdr-01 | 10 | Hidden | 2.5 s | 0 | 0 | 0 | None |
| fg-05 | 9 | Hidden | 2.8 s, 18% | 10 | 0 | 0 | Not confirmed |
| tdr-03 | 8 | Hidden | 1.6 s, 8% | 0 | 0 | 0 | Not confirmed |

### What each open question now looks like
| Question | Answer | Confidence |
|---|---|---|
| Is any post restricted? | **Yes.** hs3-01: "not eligible for the For You feed because it violates our Community Guidelines", reason "Unoriginal, low-quality, and QR code content" | High, n=1, William's screenshot |
| Can public data detect a flag? | **No.** hs3-01's public fields match the other 17 posts I read: empty `warnInfo`, same `penaltyContext`, `isProhibited` false. My earlier "public flags are clean" had no diagnostic value. TikTok says restrictions appear in the analytics tool, so only Studio can show them | High for these 18 posts (mw4-10's fields not read) |
| Is the account blocked? | **Unlikely.** mw4-10 got 223 views in ~70 min, 99.6% For You, after a 24 h gap. That is 4.6x the best of the last 5 posts | Medium-high, one post, and it is our best-fit campaign |
| Did the flag cause the low views? | **No evidence it did.** The flagged post out-reached 6 posts, and 4 of those show no banner (fg-01, hs3-03, fg-04, tdr-01). When hs3-01 was flagged is unknown | Medium |
| What caused the 5-post collapse? | **Two separate failures, not one cause** (below). Account limit is out; burst stays as a partial cause | Medium |
| Where do views come from? | **For You.** 11 of 12 readable posts are 91 to 99.6% For You; mw4-01 is the exception at 70.9%. Under 100 views Studio hides the share, so we still cannot say how much For You the 8-to-48-view posts got | High for the 12; unknown for the rest |
| Does retention explain mw4-08? | **No.** Its 55% trails mw4-10 (59%), mw4-12 and fg-02 (57%). Its 12.5 s trails mw4-09 and hs3-02. Most viewers stop at 0:01 to 0:04 where that was read, mw4-08 included (0:02). Its full-watch rate was not read | Medium-high, but that one figure is missing |
| Does retention predict reach? | **Not above the seed stage.** mw4-07 had 10.75% full watch and 760 views; fg-01 had 28.57% and 48 views. Full watch mostly tracks length | Medium, n=18 |
| Is the audience right? | **For MW4, yes:** 90 to 96% male, 60 to 67% 18-24, 95 to 99% US where read. TDR is a different crowd: tdr-02 was 68% female. TikTok picks viewers per post, so the account is not locked to one audience | Medium |
| Does HardScope meet the 40% T1 rule? | hs3-04 is 96% US, so that post passes | High, n=1 |
| Do 127 "new followers" against 3 on the profile matter? | **Unresolved.** Do not trust either figure yet (see "The follower mismatch") | Low |

### The collapse: two different failures
| Failure | Posts | Evidence | Likely cause |
|---|---|---|---|
| **Viewers leave almost at once** | tdr-01, tdr-03, hs3-03, fg-05 | Avg watch 1.6 to 2.8 s; three have 0% full watch. tdr-01 did this on 10/26 with no burst; tdr-03 did it after a 5.3 h gap | Weak opening and weak fit. Very small samples (6 to 48 viewers) |
| **Viewers stay, but few are shown it** | fg-01, fg-04 | 53% avg watch, 21 to 29% full watch, yet 48 and 13 views | Burst is the best candidate, unproven |

**Best natural comparison (n=3, a signal only):** same campaign, same 15 s length, similar retention. fg-02 got 319 views with no TikTok in the prior 4 h, fg-01 got 48 with one, and fg-04 got 13 with three.

**Still against burst as the whole story:** the 10/28 burst did not decay (137, 79, 385, 264, 343), and mw4-10 also returned to our best campaign.

### Is hs3-01's logo card the trigger?
**Possible, but not the likely single cause. My estimate is about 1 in 4 (judgment).**
- **For:** TikTok's definition names it: content "may be unoriginal if it has a watermark or logo on it".
- **Against, hs3-04:** it is unflagged, and frames show a large white wrap printed with a repeated logo that appears to read UNPACKED.
- **Against, other source graphics:** hs3-02 carries the show's price overlay and trivia graphic with no sign of a flag (its banner is unconfirmed). hs3-01 has those kinds of graphics too.
- **I could not find the card:** the 12-frame sheet does not show it. Scanning the live post every 0.4 s from 17 to 23.4 s found no full-frame dark card: dark pixels in the center band peak at 13%, around 17.8 to 18.6 s. A small card or one before 17 s remains possible. Screenshots failed, so I never saw these frames directly. **Morpheus should supply the timecode.**
- **Rival explanations, all unproven:**
  - The 58 to 81.5 s moment sits at the episode's start, so other clippers may have posted it too (a duplicate match).
  - It was our first post in this category.
  - TikTok's reviews may simply be inconsistent. Its page describes automated review first, with extra review if content "gains popularity or has been reported".

**That last line is the strongest reason to fix the format now:** a breakout post may get extra review just as it starts paying. mw4-08 is therefore the first banner to confirm.

### What makes footage "something new", by campaign
TikTok's wording is "unoriginal or reused material without anything new" and "without any new, creative edits". I found no published threshold, so **nobody here can promise a given edit clears it.** The aim is changes a viewer can see and value: full-frame picture, pacing, spoken captions, accurate context. Never mirror, speed-shift, pitch-shift or add noise. That disguises footage, and `pipeline/README.md` already bans it.

| Campaign | Status | Crop or reframe | Zoom | Captions and text | Overlays | Source of rule |
|---|---|---|---|---|---|---|
| **HardScope** | Live, budget unchecked since 10/28 | **Allowed** | **Allowed** | **Allowed**; must match the clip, no clickbait | Text yes. No outside visuals, music or effects | "Make your own edits; no 1:1 copies"; "new visual/pacing"; "only use the footage provided". The no-burned-in-logos note is our own pipeline note, not a campaign rule |
| **Total Drama Roblox** | Live, about 6 days left | **Grey: do not do it without an answer from Vyro** | **Grey** | **Likely OK**, already in use. Must not misrepresent | No logos, watermarks or unaffiliated content | Vyro Content Requirements s.4 says "do not alter or modify" Client Content. The campaign only bars edits that misrepresent. Clipper Terms treat "unique additions" as Clipper Content. Moving or removing the facecam is the riskiest change |
| **Family Guy** | 100% paid, closed | Not named, but "create edits" covers it | Same | **Explicitly allowed:** POV and meme text | No outside visuals; music only as allowed | Must not alter the "DNA" or misrepresent; 15 s cap. The brief overrides Clipper Terms on conflict |
| **MW4** | Locked, no new posts | Allowed: "get creative with your clips, edits and memes" | Same | Allowed | No other logos or watermarks | Vyro s.4 still applies; footage rights after the budget unverified |

**Decision: run the framing test on HardScope only.** It is the one live campaign that asks for this kind of edit. My earlier plan to run it on TDR was wrong. Family Guy and MW4 cannot take new posts.

**Practical point:** specs render from `source-1080p`, where a 9:16 crop is about 608 px wide and must be upscaled. The local 4K original gives about 1,215 px, so full-frame clips should render from it.

### tdr-04 (Sat 10/31, 12:30 PM): pull it
**Morpheus should unschedule it and cancel the 12:33 PM Vyro submit job before 12:30 PM Saturday.** Confidence is medium and the stakes are low either way.
- **No result would change a decision.** At 300 views or at 8, we still would not prioritize TDR, and the gate no longer needs it.
- **Almost no money at stake.** A post needs 5,000 views after submission. No TDR post has passed 325, and only 1 of our 19 posts has passed 5,000.
- **Risk is small but real.** "No flag seen on TDR" covers tdr-01 and tdr-02 only; tdr-03 is unconfirmed. Another same-format post adds exposure while the meaning of a Community Guidelines flag is unknown.
- **Case for keeping it:** it would give a spaced, non-MW4 reading. HardScope's first spaced test post gives us that anyway.
- **Reversible:** the clip stays built and approved, and it also saves a Vyro pending slot.

### The follower mismatch
**The facts:** Studio's per-post "new followers" sum to 127. The public profile shows 3 followers at 8:13 PM, following 79, 259 likes received and 0 videos liked.

**New pattern:** on 8 of the 11 posts with non-zero likes or new followers, new followers are within 1 of likes: 1/1, 18/19, 4/4, 9/9, 8/9, 4/5, 3/3 and 1/0. The exceptions are mw4-07 (0/17), fg-02 (0/7) and mw4-08 (78/182). A near 1:1 ratio is not what real viewers normally do.

| Explanation, my order | Why | What would show it |
|---|---|---|
| Frame misread, or the field does not mean net followers | Read from frames every 3 s; the near-match with likes fits a misread | One clear William screenshot of hs3-04 or mw4-16 |
| TikTok removed the followers as inauthentic | TikTok says it removes "fake likes, followers, or other inflated signals". The like-follow pattern would fit bot accounts. We have bought nothing | A follower spike around 10/25 to 10/26, then a drop, or a notice in the inbox |
| Real people followed, then left | 98% leaving in days would be extreme | Spike, then gradual decay |
| Public count is lagging | Unlikely after 5 days | Followers list has far more than 3 |

**What William should check (read-only, about 5 min):**
1. **Followers:** the Studio follower chart against the actual followers list. Note any spike or drop, with dates.
2. **Standing:** account status under Settings and the system notifications in the inbox. The menu name is from memory, so it may differ.
3. **Following 79:** who followed those accounts, and how? I found no record, and Buffer does not follow accounts. If any tool did it, that matters: TikTok bans automation "designed to bypass our systems" and can restrict an account's For You reach.

**What it may mean for standing:**
- **On its own, nothing.** It is not evidence of a penalty.
- **If follower removal is confirmed:** still no sign of wrongdoing by us, but likes may be partly inauthentic too. Vyro's terms also require reasonable efforts to verify follower authenticity and to act on known problems, so William should see this.
- **If account status shows a restriction or more than one violation:** pause all posts until William decides.
- **Until this is resolved:** do not use followers or likes as a success metric.

### Still unverified
- **Banners:** fg-05, tdr-03, hs3-02 and fg-02 were not visible in the recordings. The readings also leave mw4-08 and mw4-13 outside the clear group. For You share does not clear them: it is a share of traffic, and a flag could come later.
- **Standing:** account status has not been read, and I could not find whether this flag counts as a strike or how repeats are treated.
- **The flag:** what triggered it and when are both unknown.
- **The frame readings:** every Studio figure comes through Morpheus reading video frames, not from an export.
- **mw4-10:** still at ~70 min; its 24 h reading is due Sat 7 PM.

## The answer
1. **The footage is not the limit.** Other clippers drew about 1M views from HardScope Ep. 3 and burned the Family Guy budget from 16% to 100% in about a day. We got 734 and 389 views from the same material. Caveats: big accounts may dominate those totals, and pending views also burn budget.
2. **Likely causes, in my new order:**
   - The re-upload format now has an enforced penalty attached (risk first; its effect on views is unproven).
   - The moments and hooks describe events instead of giving people a reason to react.
   - Bursts and weak campaign fit choke individual posts.
3. **Nobody knows why mw4-08 hit 8,524.** Studio data adds no explanation. We built a strategy on one outlier.
4. **Biggest uncertainty:** whether a framing change satisfies TikTok or lifts views. It is untested, and 5 clean posts would prove little (section 5).

## 1. Scoreboard (18 TikTok posts read at 7:17 PM; mw4-10 is in the Studio table above)
**Freshness:**
- **FRESH:** views, likes, comments, shares and saves, read from TikTok's public post pages on 10/30 at 7:17 PM ET.
- **STALE:** average watch comes from the Buffer snapshot of 10/30 6:10 PM ET. It differs from Studio by up to 0.4 s; the Studio table above takes priority.
- **Earlier readings:** from William's screenshots, PLAN.md, the 10/28 brief and `strategy/vyro-approval-mechanics.md`.

Posted times are TikTok's own create times.

| Clip | Campaign | Posted (ET) | Hook | Len (s) | Views (age) | L / C / Sh / Sv | Avg watch (s, % of length) | Earlier readings |
|---|---|---|---|---|---:|---|---|---|
| mw4-01 | MW4 | Fri 10/23 9:01 PM | Eight tags. $500,000. | 34.5 | 130 (166 h) | 1/0/0/0 | 5.3, 15% | 95 @13 h; 122 @49 h |
| mw4-07 | MW4 | Sat 10/24 2:02 PM | Holding this tag makes you a target | 39.3 | 760 (149 h) | 17/0/1/0 | 10.0, 25% | 751 @32 h |
| **mw4-08** | MW4 | Sun 10/25 7:01 PM | Their plan to fool proximity chat | 22.6 | **8,524** (120 h) | 182/0/1/10 | 12.5, 55% | 8,041 @2.8 h; 8,509 @71 h |
| mw4-16 | MW4 | Mon 10/26 12:31 PM | Across the map, another team wasn't so lucky | 17.5 | 760 (103 h) | 19/0/0/0 | 8.9, 51% | 753 @54 h |
| tdr-01 | TDR | Mon 10/26 7:02 PM | The muted player's excuse: soup | 23.6 | 10 (96 h) | 0/0/0/0 | 2.4, 10% | 2 @47 h |
| mw4-12 | MW4 | Tue 10/27 12:32 PM | Losing would waste all those childhood CoD hours | 15.8 | 192 (79 h) | 3/0/0/0 | 9.1, 57% | 186 @30 h |
| tdr-02 | TDR | Tue 10/27 7:02 PM | The "relaxing" challenge: jump off a cliff | 27.8 | 313 (72 h) | 8/0/0/0 | 5.3, 19% | 302 @23 h; 325 at 8:13 PM |
| mw4-13 | MW4 | Wed 10/28 12:32 PM | A million dollars in a couple minutes | 37.0 | 137 (55 h) | 0/2/0/0 | 12.2, 33% | 129 @5.6 h |
| hs3-01 | HardScope | Wed 10/28 6:30 PM | David gifts the host a Pokémon card | 23.5 | 79 (49 h) | 0/0/0/0 | 11.1, 47% | none |
| mw4-09 | MW4 | Wed 10/28 7:03 PM | Tim and Fatboy were doing well so far | 38.7 | 385 (48 h) | 4/0/0/0 | 13.7, 35% | none |
| hs3-02 | HardScope | Wed 10/28 8:30 PM | He risked four prizes for one comic | 45.4 | 264 (47 h) | 5/0/0/0 | 13.3, 29% | hs3-02 + hs3-04: 590 on Whop @~16 h |
| hs3-04 | HardScope | Wed 10/28 9:30 PM | David gets a gift from the host | 40.3 | 343 (46 h) | 9/0/0/0 | 9.8, 24% | see hs3-02 |
| fg-02 | Family Guy | Thu 10/29 10:25 AM | Satan quits and hands over the job | 15.0 | 319 (33 h) | 7/0/0/1 | 8.7, 58% | 114 @0.8 h; 139 @1.7 h |
| fg-01 | Family Guy | Thu 10/29 11:01 AM | Satan misses the fire and torture | 15.1 | 48 (32 h) | 0/0/1/0 | 8.2, 55% | 1 @1.1 h |
| hs3-03 | HardScope | Thu 10/29 12:32 PM | David gets his own Unpacked trading card | 23.8 | 48 (31 h) | 0/0/0/0 | 2.9, 12% | none |
| fg-04 | Family Guy | Thu 10/29 1:11 PM | Jack the Ripper gets skipped in hell | 15.0 | 13 (30 h) | 0/0/0/0 | 8.6, 57% | none |
| fg-05 | Family Guy | Thu 10/29 1:45 PM | His last memory: driving off a cliff | 15.1 | 9 (30 h) | 0/0/0/0 | 2.8, 18% | none |
| tdr-03 | TDR | Thu 10/29 7:02 PM | "They took my voice," reads the chat bubble | 21.5 | 8 (24 h) | 0/0/0/0 | 1.7, 8% | 2 @1.05 h |

**Other posts:**
- mw4-10 went live at 7 PM tonight; its figures are in the Studio table.
- tdr-04 is due Sat 12:30 PM (recommendation: pull). fg-03 was never posted.

**Totals (18 posts at 7:17 PM):** 12,342 views, median 164.5. mw4-08 is 69% of all views.

| Campaign | Posts | Total views | Median |
|---|---:|---:|---:|
| MW4 | 7 | 10,888 | 385 |
| HardScope | 4 | 734 | 171.5 |
| Family Guy | 4 | 389 | 30.5 |
| TDR | 3 | 331 | 10 |

**Account (public, 8:13 PM):** created Fri 10/23 ~7:21 PM ET, first post 1.7 h later, 3 followers, following 79, no bio, 259 likes received, 0 videos liked by the account, 19 videos.

**Ages barely matter here.** Posts stop growing fast, so comparing posts 24 h and older is fair. Share of the final count reached by the earliest reading:

| Post | Share of final count | Age at reading |
|---|---:|---:|
| mw4-08 | 94% | 2.8 h |
| mw4-13 | 94% | 5.6 h |
| hs3-02 + hs3-04 | 97% | ~16 h |
| tdr-02 | 96% | 23 h |
| mw4-12 | 97% | 30 h |
| mw4-07 | 99% | 32 h |

No post has had a second wave. The one slower curve is fg-02: 44% at 1.7 h, then growth through 33 h.

**Fix `results.csv`:** its times are wrong for mw4-07 (says 12:30, was 2:02 PM), hs3-02 (says 10/29 12:30, was 10/28 8:30 PM) and hs3-03 (says 10/29 7 PM, was 12:32 PM). Its `views_48h` column is empty.

## 2. What separates the best from the worst
n is tiny everywhere, so **nothing below is a finding; these are signals at best.**

| Comparison | Numbers | Read | Confounders |
|---|---|---|---|
| Pre-burst vs last 5 | 13 posts, median 313, 2 under 100 vs 5 posts, median 13, max 48. mw4-10 after a 24 h gap: 223 at ~70 min | Not an account limit. Two failure types (see Update) | Burst, category switch, 4 of 5 are non-gaming, all 5 are short, ages 24 to 32 h |
| Average watch under 3 s | tdr-01, tdr-03, hs3-03, fg-05 (n=4): all at 48 views or fewer | Fits "first seconds lost the viewer", but with 6 to 48 viewers it is noisy | fg-01 and fg-04 also stayed low despite 8+ s watch, so retention is not the only cut-off |
| mw4-08 vs the rest | Watch 55% (below mw4-10 59%, fg-02 and mw4-12 57%); likes 2.1% (below hs3-04 2.6%, tdr-02 2.6%, mw4-16 2.5%); ~99% For You; 5 search queries | **Nothing we can see explains it.** Full-watch rate is the one unread figure. The launch window is the leading guess | Launch-window timing (the source says "brand new", date unverified), Sunday 7 PM, third post on a new account |
| "Shock" (William's read) | shock=yes: 8,524 / 760 / 13 / 9 | Not supported or refuted (n=4); the two dead ones were in the burst | Campaign, burst, length |
| Length | Up to 25 s (n=11): median 48. Over 25 s (n=7): median 313, floor 130 | **"Shorter is better" has no support here.** Short clips win on full-watch % almost by arithmetic, without winning views | All last-5 posts are short, and Family Guy forces 15 s. Without the last 5, short (n=6) has median 255.5 |
| Hook language | Top posts name a specific idea (proximity chat, target tag); bottom posts narrate ("David gets...", "reads the chat bubble") | My judgment, unmeasured | Campaign |

**What is flat across all posts, so we cannot test it from our own data:**
- Same layout, same static text, same Buffer route, "original sound".
- Comments plus shares total 5 in 12,342 views (0.4 per 1,000). mw4-08 had 0 comments and 1 share on 8.5k views.
- Like rates reach 2.6% and mw4-08 sits at 2.1%, while mw4-13 got 0 likes on 137 views. Likes are unremarkable (and now in question, see "The follower mismatch"), but comments and shares are almost absent: people tolerate the clips without acting on them.

## 3. Diagnosis, re-ranked (risk to the account, then likely effect on views)
| # | Factor (old rank) | My read | Evidence | Confidence |
|---|---|---|---|---|
| 1 | **Re-upload format and the unoriginal-content rule** (2) | The only factor with an enforced penalty. Every post is exposed, and a popular post may get extra review. It is not shown to be what holds views down | hs3-01 flag, n=1. At least 12 of 19 posts show no banner, and mw4-08 reached 8.5k in this format, so it is no hard block | High that the rule applies to us; low-medium that fixing it lifts views |
| 2 | **Moment choice, hook, first 3 s** (1) | Still the biggest likely lever on views, but it did not explain mid-tier reach | 4 posts under 3 s avg watch stayed at 48 views or fewer. Above that, retention does not track views. See "Why the moments fall flat" | Medium |
| 3 | **Cadence burst** (4) | A real partial cause of the Thursday collapse. William's cadence rule already addresses it, so no test is needed | fg-02, fg-01, fg-04: 319, 48, 13 with similar retention (n=3). mw4-10: 223 at ~70 min after a 24 h gap. Against: 10/28's burst did not decay. With 0 TikToks in the prior 4 h (n=11) median 192; with 1+ (n=7) median 48 | Medium |
| 4 | **Campaign and audience fit** (5) | MW4 fits a clear audience but is closed. TDR is the weakest fit. HardScope has a qualifying audience and looks underused | MW4 median 385 vs TDR 10 (n=3). MW4 90 to 96% male, 18-24 skew, US. tdr-02 68% female, 8 to 19% watch. hs3-04 96% US | Medium |
| 5 | **Account: cold start, no identity** (3) | Downgraded. Reach is almost all For You to strangers, so follower count is not the blocker, and TikTok matches viewers per post | 91 to 99.6% For You on 11 of 12 readable posts. Peers on #kevinlanguepartner had 4 of 5 hits from accounts under 1k followers (10/28 screen). The follower count itself is unresolved | Medium |
| 6 | **Audio and burned captions** (6) | Probably costing retention, unmeasured | No word-by-word captions. **Nobody has listened to a clip:** Editor works from whisper text and frames | Low-medium |
| 7 | **Account standing** (12) | No account-wide block in evidence, but the account status page is unread and the following count is unexplained | mw4-10 distributed normally. See "The follower mismatch" | Medium on no block; low on the rest |
| 8 | **Post time** (7) | Not the separator | The ~7 PM slot ranges from 8 to 8,524 (n=5, median 313); 12:30 PM n=4, median 164.5 | Low impact |
| 9 | **Length** (8) | Not a lever yet | Section 2. On 12 of 18 posts, average watch is about 8 to 14 s, whether the clip runs 15 or 45 s | Low impact |
| 10 | **Caption search phrases** (9) | Specific terms get picked up, but traffic stays tiny | mw4-08 drew 5 queries; hs3-02 and fg-02 drew a few. Nearly all traffic is For You, and posts die within 24 h. "Modern Warfare 4:" prefix (n=4) median 288.5 vs plain (n=3) median 760 | Low |
| 11 | **Buffer vs native** (11) | Less likely than before | mw4-08 and mw4-10 got ~99% For You through Buffer, and only 1 of 19 Buffer posts is confirmed flagged. No native control exists | Low |
| 12 | **Hashtags** (10) | Not a lever | Briefs mandate them, and they match across best and worst posts within a campaign | High that it is not a lever |

### Why the moments fall flat
- **Hooks often spoil the payoff:** "His last memory: driving off a cliff" gives away the line before it lands. So does "Satan quits and hands over the job". On mw4-09, the on-screen "Then a rival team takes out Fatboy" gives away the ambush.
- **Other hooks say nothing:** "David gets a gift from the host" sat on the episode's biggest reaction. "He thinks the car is his" was written, but only for the Instagram cut.
- **Weak openers (frames):**
  - hs3-03 opens on shop b-roll (2.6 s avg watch, most stopped at 0:01).
  - fg-05 opens on three rings in water, and the line lands at 3.7 to 6.4 s.
  - mw4-16 opens on a road, then an aerial shot.
  - mw4-12 opens on an aerial shot.
- **mw4-08, by contrast:** a face and an on-screen speaker label appear within the first seconds, and "switch to Arabic" stays on screen.
- **Process cause:**
  - Editor cannot hear the audio.
  - The candidate score has no "would someone send this?" test.
  - The hook-must-match-the-first-3-s rule is good, but we meet it by weakening the hook. We should meet it by starting the clip at the peak.

### Why the packaging looks re-uploaded
- `pipeline/format_short.py` puts the 1080x608 footage in the middle of a 1920-tall frame over a blurred copy of itself. **The real footage is 32% of the screen height.**
- The same treatment applies to all 19 posts. The three "styles" only change the font and color.
- A hook shows for 4 s, plus one static sentence for the whole clip. There are no spoken captions, no zooms, no crop.
- On a phone, a MW4 face is a small box inside a thin strip.
- TikTok's guidelines (released 8/25/2026, effective 9/24/2026): "Content is also ineligible for the FYF if it includes unoriginal or reused material without anything new."
- The hs3-01 notice defines this as content "just imported or copied from other sources without any new, creative edits". **Our text overlay did not protect hs3-01.** It also did not stop 12 clear posts, so enforcement looks post-by-post and inconsistent.

### Suppression check
The views are lumpy:

| Views | Posts |
|---|---:|
| Up to 15 | 4 |
| 16 to 100 | 3 |
| 101 to 400 | 8 |
| 401 to 1,000 | 2 |
| 1,001 to 8,523 | 0 |
| 8,524 | 1 |

- **Normal-looking band:** 8 posts sit at 101 to 400, a plausible small test audience that then stopped. Peer medians are about 240 to 930 views (10/28 screen), so this band is ordinary for small accounts. Seven of these posts are 91 to 98% For You; mw4-01 is 70.9%.
- **Very low band:** tdr-01, fg-04, fg-05 and tdr-03, at 15 views or fewer. tdr-01 and fg-04 show no banner, so very low reach happens without a flag. fg-05 and tdr-03 are unconfirmed.
- **Public fields:** they do not separate flagged from unflagged posts, so they cannot be used as a check. Morpheus's trackers and yt-dlp cannot see a flag; only Studio can.
- **Flag rate:** 1 confirmed of 19. 12 show no banner and 6 are unconfirmed. Earlier I called this unresolved; per-post enforcement is now confirmed.

**My read:** per-post enforcement is real and no account-wide block is in evidence. The low distribution has more than one cause, and the flag is not shown to be one of them.

## 4. Source-footage review
**What mw4-08 had that the others lacked:**
- One idea a Call of Duty player understands instantly, with no knowledge of the video.
- A specific, surprising word ("Arabic").
- The speaker visible and labeled as the idea is said.
- A real game term ("proximity chat").

The closest repeat, mw4-16, kept the idea (760 views, tied for second) but opened on a road and an aerial shot, cut to the studio under the key line, and never named the language. mw4-12 was relatable but had a weak opening. The pattern is "instantly understood insider idea", not just "short" or "shock" (n=2 at most, signal only).

**Strongest unused moments, best first. These come from whisper transcripts and need a listen and a frame check.**

**HardScope Ep. 3: best remaining pool (joined, live, faces, 4K).** The audience passes the T1 rule on the one post read. Do not re-cut 58 to 81.5 s (the flagged moment).

| Source (s) | Moment | Note |
|---|---|---|
| 568-585 | Pulls Scarlet Witch, then: saw "the Scarlet Witch... in a Prius" on Ventura | Quotable, absurd, about 17 s |
| 437-498 | "One pack for 1200? For tennis?" then a run of hits and a quad autograph | Money plus reactions; one "Fuck" at 493 |
| 516-541 | "I genuinely think Robert Downey is a superhero" | The most arguable take, so it could draw comments |
| 743-770 | Vault: people whispered "good luck, bitch" as he walked in | Check exact end point |
| 1144-1163 | Transaction times out, then "what's the damage?", "it's a 12.7" | Bill reveal; confirm the amount and unit on screen |
| 722-738 | "One card to change the entire day... Olive Garden?" then Emperor Zurg | Reaction pull |
| Timing unverified, before 399 | Mbappe club story ("definitely like some Spanish artist") | Soccer angle |
| 1013-1027 | "What if he signed it? 'I'm out this bitch.'" | Short gag |
| 1067-1078 | "Does it smell like him?" "...we're doing blow..." | **Highest shock, but a drug joke about a brand's show. Hold for William's call against "nothing that could create negative press"** |

Stay off the kid segment (minors rule). **Pool limit:** these are 9 moments, and tests 1 and 2 want 20 clips between them. Editor needs to find more, or test 2 must wait for the next footage William approves.

**TDR Sinjin: good text, weak picture (joined, about 6 days left).** Keep for reference; I do not recommend new TDR clips now. Locate these by transcript phrase, since I did not pull timecodes. Speakers cannot be named.
- Hot mic: "could his shorts be any shorter", then "everybody heard that". This is the same family as mw4-08: other players can hear you.
- "They took my voice" continued just past tdr-03's cut: the "I'm Ezekiel... wait, I'm Ezekiel" confusion and "I can't say real words".
- "Why are we voting out the hot people", "I have pretty privilege".
- Ezekiel's hair: "your hair is stringy", "spaghetti noodle hair", "use one of my strands as a jump rope".
- "I love you guys more than my parents".

Avoid the sexual-joke runs (Owen with no pants, "breathe into my ear", "boo thang"). On Roblox footage that is a needless risk.

**MW4: strong moments, but it cannot earn.** The campaign is locked at 100% paid, and footage rights after the budget are unverified. For learning only, if William allows it:
- "Did you guys eliminate me?... I'm so sorry, Mr. B" (725-735). MrBeast confronting his killer is probably the best unused star moment.
- "If I kill them bro, that's like 250k each... I trust them!" (inside 1096-1132, mw4-06, which went to YouTube only).
- "If Tim dies, you don't get any" (972-1016, mw4-02, YouTube only).

**Family Guy: locked at 100%, closed.** One lesson: "Your Hell is July 4th" for the dog (p3) is a relatable, visual gag, stronger than the "dark confession" picks in my reading. Darker was not automatically better.

## 5. Recommendations (one variable each, TikTok only, within the 2-a-day, 4-h-apart rule)
**The old gate is retired.** mw4-10 cleared 100 views within ~70 min, so the account-level question no longer needs tdr-04. Read mw4-10 at 24 h for the record.

**New pause rule:** if the next two spaced, non-TDR posts are both under 50 views at 24 h, pause and have William re-check Studio and account status.

**Do first (all free):**
1. William does the account and follower checks in "The follower mismatch", and confirms banners on the 6 unconfirmed posts, starting with mw4-08.
2. Morpheus pulls tdr-04 and its Vyro job.
3. Morpheus checks HardScope's TikTok budget and end date. Test 1 depends on them.

**Stop now:**
- Posting the blurred-band format outside test 1's control arm.
- Using public fields or view counts as a flag check.
- Using followers or likes as a success metric until the mismatch is resolved.
- Re-cutting hs3-01's moment.
- Reading mw4-08 as proof of "short" or "shock".
- Cutting to 15 s by default.
- Adding search-phrase tests.
- Campaign-hopping during tests.
- Extra burst exceptions.

**Precaution, not a test:** avoid starting or ending a cut on a held logo card. At a flag rate of about 1 in 19, we could never measure this. Ordinary set dressing does not need removing.

**Peak-first or framing first?** **Framing first.** Peak-first may still have the bigger upside on views, and the analytics do not weaken it; the first seconds are where viewers leave. But framing goes first for three reasons:
- It is the only factor with an enforced penalty attached.
- Every later test would need re-reading if the format changes afterward.
- A flagged winner would pay nothing.

| # | Experiment | One variable | Sample and setup | Success metric | Conclusion rule |
|---|---|---|---|---|---|
| 1 | **Full-frame reframe** (pipeline layout work, 4K source) | Blurred band vs 9:16 reframe that follows the speaker, with punch-ins on reactions. Same hook and text rules, same open rules | HardScope, **5 daily pairs (n=10)**. Each day one of each, 12:30 and 7 PM, coin flip for which goes where. Submit to Whop within 5 min. William checks Studio at 24 h | Primary: 24 h views. Also avg watch %. Flags as a stop rule | **Pass:** reframe wins at least 4 of 5 days, median at least 2x, avg watch % not lower: retire the band. **No view gain, no flag:** still prefer the reframe on risk, and stop expecting views from it. **Any flag on a reframe:** stop, framing alone is not enough, go to test 3 sooner. **Any new flag on a band post:** drop the band arm now |
| 2 | **Peak-first cold open** | Clip starts at the peak vs at the setup | Winning format, **5 pairs (n=10)**, lengths within 3 s. HardScope if Editor finds enough moments, otherwise the next footage William approves | 24 h median at least 2x **and** higher avg watch seconds. Stretch: one post at 2,000+ (Whop's minimum payout) | **Pass:** Editor default. **Watch rises, views do not:** the limit is after the open, go to test 4. **No change:** the open is not the limit |
| 3 | **Word-by-word captions** | Spoken captions vs static summary sentence | **6 vs 6**, winning format. Someone must listen before approval | Avg watch % up by 10+ points; 24 h median at least 1.5x | **Pass:** standard, and it adds visible new work. **Fail:** drop it and avoid the pipeline cost |
| 4 | **Send-it premise** | Insider or arguable idea vs reveal or wholesome moment | **6 vs 6**, winning format. Tag each clip before posting | Comments plus shares per 1,000 at least 3x the 0.4 baseline | **Pass:** add "would someone send this?" to candidate scoring. **Fail:** drop the idea |
| 5 | **Native vs Buffer** (needs William's explicit go under USER.md) | Posting route | **3 pairs**, same clip type and slot. Run only if tests 1 and 2 both fail and Studio shows no flags | Native at least 3x in all 3 pairs | **Pass:** the API route is the limiter, and William decides. **Otherwise:** close the theory for good |

**Limits of these tests:**
- **Flags cannot be proven fixed at this sample size.** At about 1 in 19, an unchanged format would pass 5 posts clean about 3 times in 4. Zero flags on 5 reframed posts is not proof.
- **All arms under 10 give a signal, not a finding.** Extend to 10 per arm before making a permanent rule.
- **The control arm carries some flag risk.** If account status shows more than one violation, drop it and compare against existing posts, accepting the weaker evidence.
- **Cadence:** the rule ends about 11/05. I recommend William extends it through these tests.

**Decision for William, hs3-01 appeal:** I recommend one truthful appeal (campaign-supplied footage, our own edits), after reading account status. hs3-01 earns nothing because it missed Whop's window, so the value is learning how a review treats our format. I do not know of a downside, but could not verify that. Do not delete the post: it is the evidence.

## 6. Missing data and how to get it
**Received tonight:** traffic sources, retention, audience and the hs3-01 reason, for all 19 posts.

**From William (about 5 minutes, highest value):**
1. **Account status** and inbox system notifications: any violation, date, or other flagged post.
2. **Follower checks:** Studio chart against the followers list, plus one clear "new followers" screenshot.
3. **Following 79:** who followed these accounts, and how.
4. **Banners:** the top of Studio for mw4-08, mw4-13, hs3-02, fg-02, fg-05 and tdr-03.
5. **mw4-08 full-watch %.**
6. **From now on:** the Studio banner on every new post at 24 h, since nothing else can see it.

**From Morpheus:**
- The timecode of hs3-01's logo card.
- HardScope budget and end date.
- mw4-10 at 24 h, and views at 1 h and 24 h for every new post.
- Correct the `results.csv` times and fill in the view columns.
- Log TikToks in the prior 4 h from actual times; PLAN.md undercounts fg-05 (it had 4).
- Have someone listen to each clip before approval.

**William's decision, about $1:** a top-20 Apify pull for #unpacked. Logged-out tag pages returned no data for me. This is now the fastest outside check on test 1: whether winning clippers crop and caption, and whether they posted hs3-01's moment.

**William's decision, only if TDR continues past tdr-04:** ask Vyro whether crops and zooms count as "altering Client Content" under s.4. With about 6 days left, I would not bother.

**Rule check, corrected:** I said the TDR brief requires both the hashtag and the paid-partnership label. The campaign's own text says "HASHTAG OR NATIVE PLATFORM LABEL", so `#paidpartnership` alone meets it. `brief.md` overstates this and should be fixed.

## What I could not verify
- **No shell in this run:** no ffmpeg, ffprobe or yt-dlp. Fresh counts came from public TikTok post pages through the browser, logged out, read-only. Screenshots timed out, so I could not view frames from the live hs3-01 post; the logo check uses a brightness scan.
- **I did not watch or hear any clip.** I reviewed frame sheets or thumbnails for 15 of 19 posts (not mw4-01, mw4-13, fg-01 or mw4-10; those are from specs and notes). First-3-s judgments are from these frames and specs, not motion.
- **Sources:** I read the full whisper text for MW4, TDR and HardScope, and Family Guy part 3. The other Family Guy parts I know only through Editor's notes. No source video was viewed in full, and whisper errors are likely, especially on TDR.
- **Not available to me:** TikTok Studio directly, account status, how TikTok counts or escalates flags, other clippers' clips on these campaigns, the MW4 launch date, and current HardScope budget and end date. TikTok's help pages on account status would not load. I read TikTok's Integrity and Authenticity and Enforcement pages tonight.
- **Causal claims here are my judgment.** Everything in section 3 is inferred from one account in its first week.
