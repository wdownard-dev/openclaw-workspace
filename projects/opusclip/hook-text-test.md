# Do burned-in hooks matter? Evidence, OpusClip mechanics, and a test design (Strategist, 2026-11-03 ~8:30 PM ET)

Advisory only. I submitted nothing to OpusClip, posted, scheduled and contacted nobody, and changed no file except this report. Labels: **[doc]** OpusClip or platform page I read tonight, **[vendor]** a company selling something, **[obs]** observational data, **[own]** our files, **[judgment]** mine.

## Answer
**Do burned-in hooks make a difference? Unproven. My read is "probably a small plus, mostly on clips whose opening is setup, a stammer or no face", but there is no controlled test I could find, nothing specific to Shorts, and we have n = 0 posted clips with hook text.** Run a cheap 4-clip test in slots we already planned (11/6 to 11/8), not in the GTA-earmarked slots. It can only detect a large effect (about 10 points or more), so treat the result as a direction, not proof.

## 1. Evidence (quality labelled; weak overall)
| Source | What it says | Quality |
|---|---|---|
| Content Labs, 5,354 TikTok + Instagram videos (2,258 TikTok) | Median views: visual+text 25,492 (n=1,176); visual+text+spoken 14,587 (n=3,572); visual+spoken only 1,828 (n=382); visual only 973 (n=223). On TikTok alone: V+T+S 18,400, V+T 13,550, V+S 4,526 | **[vendor, obs]**. Selection and method unclear (creators who add text are likely more polished or bigger), no account-size control, no Shorts data. Direction only: text in the first second goes with higher medians; stacking text on spoken adds little on TikTok |
| Verizon Media/Publicis 2019 (5,616 US adults); Facebook internal test 2016-17 (+12% view time on captioned video ads) | 80% say they are more likely to finish a captioned video | **[survey/vendor, second-hand via 3Play, QuickReel, VidMint blogs]**. Self-reported or ad-unit data. It is about captions, which our clips **already have** (karaoke), so it says nothing about extra hook text |
| YouTube | Shorts Analytics has "viewed vs swiped away"; no universal benchmark, no published cutoff that stops distribution. Since 3/31/2025 a Shorts view counts when a Short starts or replays, with no minimum watch time. A Shorts product lead is quoted (2023, Creator Insider) saying "grabbing people in the first few seconds tends to be important" | **[doc via third-party glossary creatoressentials.com; quote second-hand via viralfaceless.io, video not checked]**. Nothing says on-screen text raises distribution |
| OpusClip's own help page | Calls its headline "designed to ... improve short-form retention and engagement" | **[vendor claim]**, no data given |
| Creator test videos and 3-second-hook blogs (opus.pro, eliro, smmnut; "70% decide in 3 s") | Assertions without methods | **Discard.** One YouTube "spoken hook vs on-screen text, two-week paired test" appeared in search; I could not open it, so I cite no result |
| **[own]** | n = 0 hook-text clips. TikTok @rvclips6: 19 posts, median about 190 views, one outlier (mw4-08, 6 words, worked on mute, n=1). The audit found the karaoke caption on frame 1 just echoes the first words ("THE DEVS ARE TRYING"), never the stakes | no hook-text variation, so no evidence |

**Net:** conflicting? No, just thin. Everything points the same weak way (silent viewers, text helps, first seconds matter), but it is correlation, mostly from larger accounts, mostly not Shorts. **Real risk to name:** a bait line can raise the viewed rate and lower retention if the payoff is weaker than the promise **[judgment, supported by the creatoressentials guide]**, and text that clutters over the karaoke caption can hurt. **Metric trap:** because Shorts views now count any start, **raw views are a poor outcome** here; use viewed rate and average % viewed.

## 2. What OpusClip's "visual hook" actually is
**Documented [doc, help.opus.pro fetched 11/3]:**
- **Auto headline** (old name "Auto hook"): one-line AI text overlay at the start of a clip, generated from OpusClip's analysis of the content, applied to the **top 10 clips** of a project, style from the Brand Template (font, size, color, box), editable in the editor. **API switch: `curationPref.enableAutoHook: true`, off by default for API projects.** It only applies to a new clipping run. No credit price is listed on that page.
- **Viral hook** (template): animated text **plus zoom and sound effects** over the opening. Text is auto-filled from the transcript of your opening ("your own words"), editable (text, color, size, position), can hide captions while it plays, SFX can be switched off, remove restores the opening. Best on single-speaker talking heads with one continuous opening shot. **Credits: 20 at clipping (up to 10 clips), 2 for one hook in the editor.** Already-made clips: results page, Edit clip, Hook panel.
- **Text overlays** (custom): up to 5 layers via the editor's Text tab; you write the text, set position and duration. No credit price listed.
- **Duplicate clip:** free, independent copy, all settings carried over.

**Our data:** every dry-run clip has `renderPref.enableVisualHook: false` and no `enableAutoHook` in `curationPref` (my read of the clip JSON), which matches the API default of off. `enableVisualHook` is **not in the API reference**. I believe it is the clip-level flag for the hook feature but **could not verify the mapping to Auto headline or Viral hook.**

**Can `opus.py` or the API do it?**
- At submit: `opus.py submit` sends only `curationPref{clipDurations, genre, topicKeywords}` and `renderPref{layoutAspectRatio}`. The documented route is adding `"enableAutoHook": true` to `curationPref` (one line in `opus.py`). **That is a pipeline change, so William's decision.** The documented `renderPref` keys are only `layoutAspectRatio` and `quickstartConfig.enableRemoveFillerWords`; I would not try `renderPref.enableVisualHook` (unknown fields may be ignored or rejected, and testing it costs a 10-credit-minimum project).
- On an existing clip: **no documented API endpoint.** The MCP server's `opusclip_edit_clip` lists captions, emoji, filler removal, trim, caption style and dubbing, not hooks or text (list may be incomplete). MCP also needs OAuth and a Pro Beta/Max/Business plan, which is a new connection, so not recommended without William.
- **Manual route (works for the existing 8 projects; projects expire 2026-12-04):** web app, project, clip, **Duplicate** (free), **Edit clip**, Text tab (custom overlay) or Hook tab (viral hook, 2 credits), export, then check the exported file's first 3 seconds, then post. Check `opus.py clips PROJECT` lists the duplicate and its export URL carries the text; if not, download the HD export and upload by hand (William's call).
- **Credits to re-render or export:** no charge is documented anywhere I read (documented charges: 1 per source minute at import, hook 2 in the editor or 20 at clipping, thumbnail 7, X post 3). The editor shows a credit preview before applying; check it. Planning number: **0 to 2 credits per clip.**
- **Side note:** if the plan is Pro Beta/Max, the API has a 900-credit monthly cap [doc]. November API use looks like about 680 (dry run 141, GTA 426, other ~110) so it fits, but check `opusclip_get_usage`-style usage in the web app before the launch burst.

**Treatment to test:** a plain **custom text overlay** (Text tab), not the viral hook. It isolates text (the viral hook bundles zoom and SFX, which confounds), its words can state stakes instead of repeating the transcript, and we control accuracy (no AI-written claim on a news or GTA clip). The Auto headline is the only automatable path, so if the manual test wins, check what the Auto headline writes on 3 clips before adopting it.

## 3. Designs compared
| Design | Verdict |
|---|---|
| **A. Same moment, with vs without hook, same channel, different days** | **Reject.** A second upload of the same moment is a duplicate: reused-content and unoriginal-content risk (hs3-01 was already flagged on TikTok), the second post's audience has seen the first, and day and order effects creep in. Cosmetic text does not make it a new clip, and our rules ban identical reposts disguised as new. I have not verified a specific YouTube near-duplicate rule; the risk is enough to skip it |
| **B. Different but similar clips (same source, adjacent score), coin flip on which gets hook** | Safe on duplicates, **but clip-to-clip noise swamps the effect.** All 34 clips scored 90+ with hook sub-scores 7 to 9, and our one outlier was 40x the median. Needs about 8 clips (4 pairs); 4 of 4 pairs agreeing gives only p = 0.06 to 0.13. YouTube-only and clean on platform |
| **C. Same clips, hook version on one platform, plain on the other, counterbalanced (recommended)** | **No duplicate on any platform** (each platform gets one copy, as the plan already does). Comparing a clip with itself removes the biggest noise source. Cost: platform is a confound, handled by flipping which platform gets the hook. Uses scale-free metrics so the two platforms' sizes do not matter |

## 4. The test (Design C): 4 clips, slots already planned
All four are in the audit's 7-day order, so **no extra slots and none of Mon 11/9 5 PM or Tue 11/10.** Counterbalanced so each platform carries the hook on one early and one late post and one talking head and one game clip.

| Slot (ET) | Clip | Type | Hook version to | Plain version to |
|---|---|---|---|---|
| Fri 11/6 11 AM | A1 Nate "Make it better" (99) | talking head, about 10 s setup | **YouTube** | TikTok |
| Fri 11/6 5 PM | Y4 SMii7Y LeBron (95), read first | game, no face | TikTok | **YouTube** |
| Sat 11/7 5 PM | A2 Nate "model sets the ceiling" (96) | talking head, quotable | TikTok | **YouTube** |
| Sun 11/8 11 AM | Y6 SMii7Y crab (93), read first | game, no face | **YouTube** | TikTok |

Substitute **A3** (Sun 11/8 5 PM) if Y4 or Y6 fails its read. **Keep GTA clips out:** their overlay wording carries accuracy rules ("per T5G", no "leak").
**Hold constant:** same text style, position (top third, clear of the karaoke caption and the Shorts or TikTok UI), 0 to 2.5 s, no SFX, no zoom, same title and caption pattern on both versions, same source-credit line. **Overlay text:** one stakes or context line of 8 words or fewer that does **not** just repeat the first spoken words (the karaoke caption already shows those). Drafts from the audit's section 4, to edit after someone reads the opening: A1 "I told Claude Code 'make it better' 100 times"; Y4 "Monkey LeBron"; A2 and Y6 written after the read. **Write and freeze the four lines before any results exist.**
**Lead time:** the four edits (about 10 to 15 min each) must be done by Thu 11/5 evening. Someone with the OpusClip web login does them (William, or Morpheus in the browser).
**Credit cost:** about **0 to 8** (text overlays, no charge documented; worst case 2 per clip if the viral hook is used). Cap the whole test at **16**, including one extension round. Far under the 60 budget; none of it comes out of the GTA 450.

**Measure at 72 h (re-check YouTube at 7 d), per clip and platform:**
- **Primary (same on both platforms): average % viewed** on YouTube; **average watch time divided by clip length** on TikTok.
- **Secondary:** YouTube **viewed vs swiped away** and "Shown in feed" (impressions); TikTok retention at 2 s (read off the curve); views at 24 h and 72 h, subs gained. Views are context, not the outcome.
- Log the audit's §5 columns plus **hook version Y/N, overlay text, platform**.

**Sample-size reality [judgment, calculation mine, assumes independent impressions]:** to see a 10-point difference in a viewed rate near 50% you need about **385 impressions per arm**; for 15 points about **165**; for 5 points about **1,530**. We have no YouTube baseline (channel starts 11/4) and TikTok medians are about 190 views, so each clip will have roughly 100 to 500 impressions: **noise of about 3 to 5 points per clip before clip effects.** The test can see an effect of about 10 to 15 points, not a 3-point gain.

**Decision rule (set now, do not move):** for each clip, effect e = (hook platform's metric minus plain platform's metric), with the average YouTube-minus-TikTok platform gap over all four clips removed. Compute at 72 h, using only clips with at least 200 views on each platform (else wait to 7 d; with fewer than 3 usable clips, "not enough data").
- **Adopt** (overlay on the top picks; then check Auto headline) if **mean e is at least +5 points, at least 3 of 4 clips are positive, and none is -5 or worse.**
- **Drop** (leave hooks off, stop spending effort) if **mean e is 0 or below, or 2 or more clips are negative.**
- **Otherwise one extension round** of 4 more clips, then adopt only if **at least 6 of 8 are positive and mean e is at least +4.**
- **How much to believe a pass:** by luck alone, 3 of 4 positive happens 31% of the time; 6 of 8 happens 14%. The bar is low on purpose, because the change is cheap and reversible, but **tell William "directional signal", not "hooks work".** Also read the within-platform split (YouTube hook clips A1, Y6 vs plain A2, Y4) as a sanity check only.

## 5. Recommendation
**Test now, in the planned 11/6 to 11/8 slots; do not wait for GTA, and do not use the GTA slots.** Reasons: no extra slots, 0 to 8 credits, 72 h readouts land by Wed 11/11 (Y6 posts 11/8 11 AM), in time to decide hook text for the pre-load and launch bursts (11/12 on), and a clean test is hardest to run once cadence goes to 3 and 4 a day. **Fallback:** if nobody can do the editor work by Thu 11/5 evening, or William does not want a hook version on TikTok @rvclips6, **run it after launch (from about 11/24)** with Design B (4 matched pairs, YouTube only), and skip the hook until then. **Skip entirely** only if William decides hook text is not worth about 40 to 60 minutes of manual editor time; the credit cost is not a reason.
**Do not** turn on Auto headline for all clips and compare with the earlier posts (week-over-week on a 3-day-old channel confounds everything).

## Open decisions for William
1. Run the 4-clip test 11/6 to 11/8 (yes, or wait until after launch)?
2. OK to put a hook-text version on TikTok @rvclips6 for two of the four clips?
3. Who does the editor work by Thu 11/5 evening (William, or Morpheus in the browser)?
4. If the test passes, approve adding `enableAutoHook: true` to `opus.py submit` (pipeline change) after we read sample output?
