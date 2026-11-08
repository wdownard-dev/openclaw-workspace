# wrdclipz: YouTube mechanics and policy for 500-1,000 subscribers and monetization

Research date: 2026-11-07 (ET). Read-only. Sources: YouTube Help Center, YouTube Data API docs, Creator Insider (public pages), our public channel page, and local files (`NEWS-PLAYBOOK.md`, `data/subscriber-analytics-2026-11-07.json`, `MONETIZATION-STATUS.md`). Nothing was logged into, changed, posted or contacted. Where I could not confirm a claim from a source I fetched, it is marked **unverified**. Nothing here is legal advice.

Facts about our channel used throughout (from the analytics JSON and the public page, 2026-11-07):
- Joined Nov 3, 2026; 0 subscribers; 16 videos; 4,642 public views (the analytics file shows 2,569 views over the 3 days that had data: Nov 3: 1,310, Nov 4: 12, Nov 5: 1,247).
- Subscribers gained: 0 on 2,569 views. Two clips (Learjet) hold 2,556 of those views. Average view percentage on the channel: 86.3%. So people watch to the end and still do not subscribe.
- Audience: 93% male, all viewers 35+, 85% aged 45+ (55-64 male 30.8%, 65+ male 25.2%, 45-54 male 22.1%, 35-44 male 15%); about 82% mobile (2,098 of 2,563 device views); US 889 views, CA 301, GB 245, AU 142.
- We are in the US, which is on the YPP "expanded program" country list (support.google.com/youtube/answer/13429240, "United States" in the list; fetched 2026-11-07).

---

## (1) How a Shorts viewer subscribes, and the levers

### What is documented
- **Where the Subscribe button lives.** "You can find a Subscribe button under any YouTube video or on a channel's page." (Help, "Subscribe to YouTube channels", https://support.google.com/youtube/answer/4489286, fetched 2026-11-07.) The Shorts player's own Subscribe button next to the channel handle is standard in the app, but the Help pages I fetched do not describe it, so treat its exact placement as **unverified** from documentation (it is observable in the app).
- **YouTube measures where subscribers came from.** Analytics > Content > Subscribers: "This report shows the number of subscribers that you gained from each content type: videos, Shorts, live streams, posts, and others. 'Others' include subscriptions from YouTube search and your channel page." (https://support.google.com/youtube/answer/12220281, fetched 2026-11-07.) Use this to measure every lever below. Subscribers gained from Shorts count toward Creator Awards milestones (https://support.google.com/youtube/answer/10059070).
- **Channel page for non-subscribers.** Studio > Customization > Home tab > Layout > ADD section > **Channel trailer**: "Your channel trailer offers a preview of your channel so viewers can learn more and subscribe." It shows only to non-subscribers and only once per viewer. **Spotlight** (featured video) is for returning subscribers. Up to 12 custom sections (Videos, Playlists, Posts, "For you", and so on). (https://support.google.com/youtube/answer/3219384, fetched 2026-11-07.)
- **Banner, avatar, watermark.** Studio > Customization > Profile. Banner: 2560x1440 recommended, safe area 1235x338 at minimum size; YouTube's own advice is to put an upload schedule in the banner. Watermark options: "End of video / Custom start time / Entire video", but the watermark is "available in landscape view" only, so it does nothing for vertical Shorts. (https://support.google.com/youtube/answer/10456525 and https://support.google.com/youtube/answer/12950272.)
- **Profile links.** Up to 14 links; "Your first link will be prominently displayed in the profile section near the subscribe button." (https://support.google.com/youtube/answer/2657964.)
- **Related video on a Short** (links a Short to long-form, another Short, or a live): Studio > Content > click the Short > Related Video > pick a public or unlisted video > Save. "Viewers will see a clickable link below your channel handle." Requires **advanced feature access**. (https://support.google.com/youtube/answer/14075157.) URLs in Shorts descriptions and comments are not clickable; the Related Video link and channel profile links are. (https://support.google.com/youtube/answer/13748639.)
- **Advanced feature access** (needed for Related Video, pinned comments, clickable links in long-form descriptions, chapters, and for applying to monetization). Verified by phone for "intermediate"; "advanced" comes from channel history or ID/video verification. Check ours in Studio > Settings > Channel > Feature eligibility. (https://support.google.com/youtube/answer/9890437.) **Whether wrdclipz has it is unverified** (I cannot log in). A channel created Nov 3 probably does not have it automatically.
- **Comments.** YouTube's own advice: heart comments, pin a comment, reply to comments; pinning needs advanced access. (https://support.google.com/youtube/answer/11913117.) You can reply to a comment with a Short (https://support.google.com/youtube/answer/12816427). Posts tab (polls, images) is YouTube's suggested between-uploads engagement tool (https://support.google.com/youtube/answer/11912631).
- **Series and consistency.** YouTube's viewer guidance: "Create a series of videos from topics that have already proven popular with your viewers" to build regular viewers (https://support.google.com/youtube/answer/13615784). "Be consistent... Maintain a regular upload schedule... add your schedule to your channel banner, channel trailer and in your videos" (https://support.google.com/youtube/answer/11913421). The Upload Schedule tips page notes topical news channels cannot plan far ahead and suggests Shorts, Live and Posts polls to keep interaction going between uploads (https://support.google.com/youtube/answer/13616979).
- **New: Shorts Series.** Announced at Made On YouTube, Sept 25, 2026: "organizing your vertical videos into structured seasons and episodes, complete with custom thumbnails and sequential playback." (Creator Insider, https://www.youtube.com/watch?v=AkNszeQ77MM, published 2026-09-25.) Rollout timing, eligibility and where it is surfaced are **unverified**; check Studio for it.
- **New: "Engaged views" vs views.** Since March 31, 2025 a Shorts view counts on start; "engaged views" is the old metric (people who chose to keep watching) and is what YPP eligibility and earnings still use. (https://support.google.com/youtube/answer/10059070 and the policy changelog https://support.google.com/youtube/answer/10008196.) Since Aug 24, 2026 views count on first frame in all formats (https://support.google.com/youtube/answer/12220281).

### What is not documented, so unverified
- The effect size of any subscribe call-to-action, pinned comment, banner text or playlist on Shorts-to-subscriber conversion. YouTube publishes no conversion rates. I found no credible measured source I could fetch; do not rely on any number. Our own data is the only evidence: 0 subscribers from 2,569 views.
- Posting cadence as a ranking factor: YouTube says "Consistency" and "sustainable" frequency, with no numbers (https://support.google.com/youtube/answer/13616979).
- Whether our audience (older US men watching breaking local crime news) skews toward "watch once, never subscribe". Plausible, unverified. The Shorts feed shows each viewer a stream of unrelated Shorts; subscribers usually come from a viewer wanting more of the same, so a clear repeatable promise ("official bodycam and agency briefings, same day") should matter more than a CTA. This is an inference, not a documented fact.

### What a visitor sees right now (see section 2) and why that matters
A viewer who taps the avatar from a Short lands on the channel page, where the first impression is a tiny "Posting clips daily!" line, no trailer, no Home tab, and a mixed bag of videos.

### Actions for us (1), ordered by impact and effort
1. Check Settings > Channel > Feature eligibility; if Advanced is off, verify by ID/video (William, 5 minutes). This unlocks Related Video, pinned comments, links and the monetization application. High impact, low effort.
2. Add a Related Video to each news Short pointing to the 3:36 supercut or the relevant story playlist (needs #1). Medium-high impact (the only documented Shorts-to-long-form bridge, and it feeds watch hours), low effort per Short. Could be automated through the API only if the API exposes it; **unverified**, so do it in Studio first.
3. Turn the Home tab on, add a channel trailer (a 30-60 s explainer of what the channel is and its source rule), and sections: "Latest Shorts", one playlist per running story, "Full briefings" (long-form). Medium impact, low effort.
4. Spoken and on-screen subscribe line in the last 2 seconds of each Short, worded as a promise ("Follow for same-day official footage"), plus a pinned comment saying the same. Low-medium impact (unmeasured), low effort. Measure with Analytics > Content > Subscribers by format; run it for 20+ Shorts before judging.
5. Reply to every comment within a few hours (we currently have 1 comment in total, so volume is tiny). Low effort, low impact now, builds the habit.
6. Group Shorts into a single running series per story (playlists now; Shorts Series if it is available). Medium impact for retention of viewers across clips, low effort.
7. Put the cadence in the banner after we know what cadence we can sustain.

---

## (2) Is our account setup leaving subscribers on the table?

### Observed on the public page, 2026-11-07 (browser, signed out, https://www.youtube.com/@wrdclipz)
- **Banner:** present (black/red film-clapper "wrdclipz" logo). No tagline, schedule or source promise in it.
- **Avatar:** same logo. Fine.
- **Name/handle:** wrdclipz / @wrdclipz. The name says "clips" but not "news"; nothing indicates the niche.
- **Description:** exactly "Posting clips daily!" Nothing about what kind of clips, that sources are official agencies, or that we are independent of those agencies.
- **Links:** none (the About panel shows only the channel URL; "to see email address" requires sign-in, so contact info state is unknown).
- **Tabs:** Videos, Shorts, Search only. **No Home tab**, so no trailer, spotlight or sections are shown to anyone.
- **Videos tab:** one video, "4 Teens Arrested for Beating Disabled Teen at Bonfire | Volusia Sheriff" (3:36, 0 views, posted 16 minutes before I looked).
- **Shorts tab:** mixed. News clips ("Per HCSO: ..." Citibank series, Island Boys/NBC 6, Learjet) sit next to non-news clips from other creators: "I told Claude Code 'Make it better' 100 times | Source: @NateHerk", "We tried to carry a crate through the hell cave (game) | Source: @SMii7Y", "Monkey vs alligator... (game)", "GTA 6 police: arrests and K-9s, per T5G | Source: @T5G2".
- **Subscribe button:** present at the top ("Subscribe", prominent).
- Joined Nov 3, 2026; 16 videos; 4,642 views (public About panel).

### Why it likely costs us
1. The channel does not tell a visitor what to expect. A visitor coming from a Learjet Short who sees gaming and AI-tool clips has no reason to subscribe for "more news".
2. No trailer and no Home tab removes the one channel-page element YouTube documents for converting non-subscribers.
3. The off-topic clips are also a monetization risk (section 4): reviewers look at "Main theme", "Most viewed videos", "Newest videos" and "Channel's About section" (https://support.google.com/youtube/answer/1311392).
4. The default landing tab is Videos, which currently shows one 0-view video.

### Fixes, with where each lives in YouTube Studio (do not apply without William; all reversible)
| Fix | Where |
|---|---|
| Rewrite description (first line: what and why) | Customization > Profile > Description > Publish |
| Add one link (first link shows near Subscribe) | Customization > Profile > Links |
| Add contact email (for business inquiries) | Customization > Profile > Contact info |
| Banner: add a one-line promise + cadence | Customization > Profile > Banner image |
| Turn Home tab on | Customization > Home tab > toggle |
| Channel trailer (non-subscribers) | Customization > Home tab > Layout > ADD section > Channel trailer |
| Sections (Latest Shorts, story playlists, Full briefings) | Customization > Home tab > ADD section |
| Check Advanced access | Settings > Channel > Feature eligibility |
| 2-Step Verification (required for YPP) | Google Account > Security (not Studio) |

Suggested description (William to approve; no claim in it is false today): "Same-day clips of breaking news from official sources: sheriffs, police, fire, NTSB, FAA, courts and other agencies. Every video credits the agency. Independent channel, not affiliated with any agency. Short clips daily, full briefings weekly." Remove "daily" unless we are posting daily.

### Actions for us (2)
1. William: decide what to do with the non-news and other-creator clips on the channel (gaming, GTA 6, NateHerk): move to the gaming channel when it exists, or set them private/unlisted. They dilute the topic and add reused-content risk. Reversible. High impact, low effort.
2. Rewrite the description and add one profile link and contact info. High impact, 5 minutes.
3. Turn on the Home tab, add the trailer and 3 sections. Medium impact, 20 minutes.
4. Verify Advanced access (see section 1, action 1).
5. Turn on 2-Step Verification and confirm no strikes (YPP prerequisites) now, so these do not block us later.

---

## (3) Long-form as a funnel and the watch-hours math

### Rules (current text, https://support.google.com/youtube/answer/72851, fetched 2026-11-07)
Full YPP (ads, memberships, Supers, Premium revenue): "Get 1,000 subscribers with 4,000 qualified watch hours in the last 12 months, or ... 1,000 subscribers with 10 million qualified Shorts views in the last 90 days." Qualified watch hours are from long-form videos set public. They "don't count" if from private/unlisted/deleted videos, ad campaigns, Shorts, or unconverted live streams. "Any qualified watch hours from Shorts views in the Shorts Feed won't count towards the 4,000 qualified public watch hours threshold."

Earlier-access tier (https://support.google.com/youtube/answer/13429240 and https://support.google.com/youtube/answer/94522): 500 subscribers, 3 public uploads in the last 90 days, and either 3,000 qualified long-form watch hours in 12 months or 3 million qualified Shorts views in 90 days. Unlocks fan funding (memberships, Super Chat/Stickers, Super Thanks) and Shopping, but **not ads**. The US is in the country list.

Shorts ad revenue: separate path. "Starting February 1, 2027, to be eligible to earn a share of Shorts ad revenue from the Creator Pool and YouTube Premium revenue for each month, you will need to have at least 10 million qualified Shorts views in the last 90 days." (https://support.google.com/youtube/answer/12504220, fetched 2026-11-07.) That is a hard, large bar for a news channel with 2,600 views total. Watch Page (long-form) ads need only the 1,000 / 4,000 tier.

Review: after meeting thresholds and applying, "typically in about 1 month"; if rejected, reapply after 30 days, or 90 days if not the first rejection (https://support.google.com/youtube/answer/72851). Subscriber and hour counts dropping after you apply do not matter once you have applied.

### The arithmetic for our 3:36 supercut (216 seconds)
4,000 hours = 14,400,000 seconds. 3,000 hours = 10,800,000 seconds.

| Average view duration | % of 3:36 | Views for 4,000 h | Views for 3,000 h |
|---|---|---|---|
| 216 s (everyone finishes; unrealistic) | 100% | 66,700 | 50,000 |
| 130 s | 60% | 110,800 | 83,100 |
| 108 s | 50% | 133,300 | 100,000 |
| 76 s | 35% | 189,500 | 142,100 |

Formula: required views = hours x 3,600 / average view duration in seconds. Our Shorts show 86% average view percentage, but long-form retention on a clip compilation from a cold audience is usually far lower; plan on 40-60%, **unverified** for our channel (we have 0 views on long-form). So roughly 100,000-190,000 public long-form views for 4,000 hours, or 75,000-140,000 for the 3,000-hour early tier, from the 3:36 format alone.

Alternatively longer videos: a 10-minute video watched 40% on average (240 s) needs 60,000 views for 4,000 hours; watch time per view is the lever, so fewer, longer, narrated briefings reach hours faster than many 3-minute ones. The length of long-form is only constrained by quality and retention.

Compare with Shorts: 3 million Shorts views in 90 days (early tier) is about 33,000 a day; 10 million in 90 days is about 111,000 a day. Our best two Shorts each got about 1,300 lifetime views. The long-form route needs a one-time stock of roughly 100,000-190,000 views over 12 months (about 270-520 a day), which is a much smaller flow than 33,000 Shorts views a day. For a channel at our size, long-form hours (plus the 500-subscriber early tier) is the more achievable route on paper, but only if long-form gets distribution at all (suggested, search, browse), which our one long-form video has not yet shown (0 views at 16 minutes old).

Format caveat: any square or vertical video up to 3 minutes uploaded after Oct 15, 2024 is categorized as a Short (https://support.google.com/youtube/answer/15424877). The 3:36 supercut is over 3 minutes, so it is long-form regardless of aspect ratio, but a vertical long-form video is a poor fit for watch-page distribution; whether the supercut is horizontal or vertical is **unverified** from here. Make it 16:9 for the Watch Page. A 2:55 vertical version would instead become a Short and its hours would not count.

How news long-form gets found: search (named events: "Citibank Tampa shooting bodycam"), suggested next to related videos, and browse. Search queries for breaking news are time-limited, so evergreen angles ("what the footage shows", timelines) may keep earning hours.

### Actions for us (3)
1. Treat long-form as the main watch-hours engine: one narrated 5-10 minute weekly briefing per top story, 16:9, with a title that matches search ("Tampa Citibank shooting: what the sheriff's video shows"). High impact, medium-high effort.
2. Keep the 3:36 supercut but make it horizontal and add original voiceover and context (see section 4); tag it into a story playlist; point every related Short at it (needs Advanced access).
3. Track progress each day in `MONETIZATION-STATUS.md` (already automated); add a line for "projected views needed at current average view duration".
4. Do not use ad campaigns to buy hours (excluded from the thresholds, "ad campaigns" in the exclusion list; only "Follow-on Views" count, https://support.google.com/youtube/answer/94522), and never inflate views or subs (Creator integrity, https://support.google.com/youtube/answer/1311392).
5. The 500-subscriber early tier plus 3 uploads in 90 days (we have 16) gives fan funding only; the realistic first milestone is 500 subscribers, then 3,000 hours.

---

## (4) Monetization policy risk for a channel made of other people's official footage

### Exact current wording (https://support.google.com/youtube/answer/1311392, "YouTube channel monetization policies", fetched 2026-11-07)

What reviewers look at: "our reviewers may focus on your channel's: Main theme; Most viewed videos; Newest videos; Biggest proportion of watch time; Video metadata (including titles, thumbnails, and descriptions); Channel's 'About' section." They also say content should "Be your original creation. If you borrow content from someone else, you need to change it significantly to make it your own."

Reused content: "Reused content refers to channels that repurpose content that's already on YouTube or another online source without adding significant original commentary, substantive modifications, or educational or entertainment value. Reused content may also be known as duplicative or scraped content (taking unique or original content from other websites and publishing it as your own)."

Scope: "Our reused content policy applies to your channel as a whole. If you have videos that violate our guidelines, or if we cannot clearly tell that you made the content, monetization may be removed from your entire channel."

What is allowed: "we allow reused content if viewers can tell that there's a meaningful difference between the original video and your video." Examples include: "Using clips for a critical review"; "Reaction videos where you comment on the original video"; "Edited footage from other creators where you add a storyline and commentary"; "Reused content from other online sources where the creator is either visible in the content or explains how the creator added to the content"; "Edited footage with audio and visual effects on top of the video's reused content that demonstrates substantive editing and shows it's unique to your channel."

What violates: "Taking someone else's content, making minimal changes, and calling it your own original work would be a violation of this guideline. ... This policy applies even if you have permission from the original creator. Reused content is separate from YouTube's Copyright enforcement, which means it's not based on copyright, permission, or fair use." Not-allowed examples include "Short videos you compiled from other social media websites"; "Promotion of other people's content (even if you have permission)"; "Content downloaded or copied from another online source without any substantive modifications"; "Content that exclusively features readings of other materials you did not originally create, like text from websites or news feeds."

Inauthentic content (renamed July 15, 2025): "content that is repetitive or mass-produced"; "There is no change to our reused content policy which reviews content like commentary, clips, compilations, and reaction videos." Not allowed examples include "Similar or repetitive content with low educational value, commentary, narratives, or minimal variation across videos", "Image slideshows, templated storylines, or scrolling text with minimal or no narrative, commentary, or educational value", and "AI-generated content made with generic or unoriginal templates giving the impression of mass production without adding the creator's original, authentic insights or perspective". Allowed: "Same intro and outro for your videos, but the bulk of your content is different"; "each video has a distinct storyline, focus, or concept".

Shorts-specific: Shorts monetization sits on top of the same policies, and ineligible views "may occur" for "Non-original Shorts, such as unedited clips from others' movies or TV shows, reuploading other creators' content from YouTube or other platform, or compilations with no original content added". (https://support.google.com/youtube/answer/12504220.)

Unsatisfying or off-putting content (also relevant to violent news): not allowed: "Content that repeatedly uses disturbing themes (such as violence or loss) without building a cohesive narrative" and content "designed to shock or surprise viewers for the sole purpose of getting views". Allowed: "Content with a cohesive storyline that doesn't rely solely on shock value to generate views".

Advertiser-friendly (not the same as eligibility): all ad-monetized content "must follow our advertiser-friendly content guidelines" and on Shorts "only views of content that follow our advertiser-friendly guidelines will be eligible for revenue sharing." Violent crime footage (shootings, beatings) is the most likely cause of limited or no ads on individual videos even if the channel is approved. (https://support.google.com/youtube/answer/6162278, linked from the policy page; I did not read the full page in this pass; **detail unverified**.) October 2026 changelog: certain "content of public interest (e.g., congressional proceedings, debates over ongoing government actions) will be eligible to earn ad revenue" (https://support.google.com/youtube/answer/10008196), which helps for government proceedings, not for crime footage.

### What "transformative" means here
YouTube does not use the word in the policy; its test is "viewers can tell that there's a meaningful difference between the original video and your video" and the creator "adds significant original commentary, substantive modifications, or educational or entertainment value". Fair use is a separate legal question: Help says fair use "is separate" and "none of the above options guarantee avoiding copyright issues" (https://support.google.com/youtube/answer/2797466). Note the explicit line "This policy applies even if you have permission from the original creator". So an agency's footage being official, public and posted by the agency does not exempt us from the reused-content test. Whether a given agency's footage is public domain (US federal works generally are; state and local agencies vary) is a general-knowledge point, **unverified** for each source and not a YouTube-policy exemption.

### Content ID and TV-network clips
- Any Short over one minute with an active copyright claim "of any type, including manual claims" is blocked globally, not playable or recommended and not monetizable, with no strike (https://support.google.com/youtube/answer/15424877 and the Oct 2024 changelog). Shorts of 60 seconds or less are not blocked by this rule but can still get claims and rev-share splits.
- Content ID claims on TV-network footage can redirect or split revenue to the rightsholder (**general knowledge, unverified here**; see https://support.google.com/youtube/answer/6013276). Copyright strikes are separate and active strikes block YPP (https://support.google.com/youtube/answer/72851).
- Implication: the playbook rule (official agency sources by default; network/TMZ only with William's approval each time) is the right risk posture. For Shorts, keep clips at 60 seconds or less when the source is not an agency.

### Where we stand today (honest read)
The channel is currently clips with an attribution title and a source credit. OpusClip clips are cut-downs of agency videos with captions; the 3:36 supercut is a compilation. Nothing visible adds original commentary, narration, context or analysis. By the policy's own examples ("Short videos you compiled from other social media websites", "Content downloaded or copied from another online source without any substantive modifications", compilations "with little or no narrative"), this is the shape most at risk of a reused-content rejection at the YPP review, and the review is channel-wide. The risk is highest for the Shorts feed (non-original Shorts views are ineligible even after approval). Review happens only once we reach the thresholds, and a rejection costs 30-90 days, so fix before applying, not after. This is an assessment, not a documented outcome; YouTube's reviewers decide.

### What would count as significant original value for a news channel (inference from the policy examples)
- Original voiceover that adds what a viewer cannot get from the agency video: who/what/where/when, timeline, what is confirmed vs unconfirmed, what happens next (case status, charges, court date), why it matters. Not a reading of the agency press release (policy lists "readings of other materials... like text from websites or news feeds" as not allowed).
- Context cards: map, timeline, charge sheet summary, the agency's quote on screen with attribution, before/after footage from other agency sources, a "what we don't know yet" line.
- Multi-source synthesis in the long-form briefing: combine 2-3 official videos with narrated explanation (the "Edited footage from other creators where you add a storyline and commentary" example).
- A visible human or consistent voice (the policy example: "creator is either visible in the content or explains how the creator added to the content").
- Variety: policy punishes templated, interchangeable output. Vary structure, not just topic (the allowed example: same intro/outro, different bulk).
- AI help is allowed ("using AI to edit your video scripts"); AI that reads a generic template with no insight is not (see section 5).
- The channel description and metadata should say what we add (reviewers read them).

### Actions for us (4)
1. Add original narration and context to every long-form briefing (required before applying). Highest impact on eligibility, medium-high effort. Use a script with: setup, what the footage shows, what is known/unknown, next step.
2. For Shorts, add a short on-screen context line and a 5-10 second voiceover or text lead-in that is not just the agency's caption; keep Shorts at 60 seconds or less when the source is not an agency. Medium impact, low-medium effort; may reduce virality, so A/B against plain clips.
3. Do not apply to YPP until the Videos tab has several narrated long-form videos and the channel's most-viewed and newest videos show original value. Reviewer sampling lists "most viewed" and "newest" explicitly.
4. Remove or move off-topic and other-creator clips (gaming, GTA 6, NateHerk) before applying (section 2).
5. Keep titles and descriptions attributing the agency and stating what we added ("Narration and context by wrdclipz") so the review can "clearly tell that you made the content".
6. Keep Content ID-risk sources (TV networks, TMZ) out of long-form and out of the first review window; William's per-clip approval rule already covers this.
7. Review the advertiser-friendly guidelines for violent crime footage and decide whether to prioritize non-graphic, procedural stories (arrests, court, NTSB, weather) for ad suitability. William's call; current playbook allows shocking footage, which will likely get limited ads.

---

## (5) AI-assisted and automated channels

### AI labels and disclosure (https://support.google.com/youtube/answer/14328491, fetched 2026-11-07)
- "We require creators to disclose AI-generated or altered content that seems realistic." Must disclose content that: "Makes a real person appear to say or do something they didn't do"; "Alters footage of a real event or place"; "Generates a realistic scene that didn't actually occur"; "Creates music that's the main focus of the video."
- Not required: "Production assistance, like using generative AI tools to create or improve a video outline, script, thumbnail, title, or infographic"; "Caption creation"; "Video sharpening, upscaling or repair and voice or audio repair"; "Cloning one's own voice to create voice overs or dubs"; minor aesthetic edits.
- "Note: Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money." YouTube may also apply the label automatically.
- Where: Studio upload flow > Attributes > "AI use". Via API: `status.containsSyntheticMedia` appears in the Data API revision history (https://developers.google.com/youtube/data/revision_history); exact semantics **unverified** here.
- Implication: unaltered agency footage clipped and captioned needs no AI label. If we use a synthetic narrator voice (not our own cloned voice), whether that needs disclosure is not spelled out; it would not "alter footage of a real event", so probably not required, **unverified**. Do not generate any depiction or reconstruction (re-enactments, AI "what it looked like") without labeling. Our AI-tooling clips (OpusClip) crop and caption, not alter, which is fine.

### Inauthentic and AI-related monetization rules (section 4 quotes)
- "AI-generated content made with generic or unoriginal templates giving the impression of mass production without adding the creator's original, authentic insights or perspective" is not allowed to monetize.
- "If you use automated tools or templates to help create your content, the final product must still demonstrate your creative vision and provide educational or entertainment value."
- AI personas: "channels that use AI-generated personas to deliver information on sensitive topics" including politics, health, legal, finance are not allowed to monetize. We hold politics for William already; an AI news anchor persona giving politics commentary would hit this. (Same policy page.)
- "Deceptive or misleading imagery or narratives, such as realistic visuals tricking viewers into believing a fake celebrity death or natural disaster has occurred" is off-putting content. Our attribution-first titling ("Per HCSO: ...") is the opposite of that, which helps.

### Automation and spam
- Channel-wide "Mass-produced, generic, repetitive" content is the stated risk. A radar-to-post pipeline that posts 1-2 clips per story is fine in principle; many near-identical clips per story (e.g., seven Citibank Shorts in a row from one agency video: HCSO, Security Guard, Surveillance, Rifle...) can read as repetitive: "Similar or repetitive content with low educational value, commentary, narratives, or minimal variation across videos" (https://support.google.com/youtube/answer/1311392). Assess the story-priority rule (up to 3 auto posts per story per 24 h) against this once we have narration.
- Creator integrity: no artificially inflated views, subs or engagement; we do none of that.
- Community Guidelines also apply to channel descriptions; "YouTube may hide channel descriptions that don't follow our Community Guidelines" (May 2026 changelog, https://support.google.com/youtube/answer/10008196). Unrelated to us but note any contact info must be business-appropriate.
- Inactivity: "we may turn off monetization on channels that haven't uploaded a video or posted to the Posts tab for 6 months or more" (https://support.google.com/youtube/answer/72851). Not a concern for a daily poster.

### API upload default privacy (the current state)
- **Changed Nov 2, 2026, five days ago.** Data API revision history: "Videos uploaded through the videos.insert method from unverified API projects are no longer restricted to private viewing mode. This change reverses the policy announced on July 28, 2020, which restricted videos uploaded from unverified API projects created after that date to private viewing mode until the project completed an audit." Also: "If you don't specify a value for the status.privacyStatus property in a videos.insert request, the uploaded video's privacy status defaults to public. Certain uploads might default to private based on creator account settings." (https://developers.google.com/youtube/data/revision_history, entry "November 2, 2026"; also https://developers.google.com/youtube/data/reference/rest/v3/videos/insert.)
- Implication: our posting path (OpusClip posting to YouTube, OAuth app) is not locked private by YouTube any more. Before this date the restriction would have applied to unaudited API projects; our clips have been posting public, which suggests OpusClip's own project is not affected. We should still set `privacyStatus` explicitly when we upload ourselves. The account-level default (Help: default is public for adults, private for creators aged 13-17, https://support.google.com/youtube/answer/157177) does not apply to us.
- The upload endpoint's current doc lists quota impact as "100 calls per day" with a quota cost of 1 unit in a separate "Video Uploads" bucket (https://developers.google.com/youtube/data/reference/rest/v3/videos/insert); default project quota is otherwise 10,000 units/day and extra quota needs a compliance audit (revision history). Not a constraint at our volume.
- Nov 3, 2026: `thumbnails.set` now supports custom thumbnails for Shorts after processing (revision history). Our Google OAuth app tokens expiring is an unrelated open item in the playbook.
- Custom thumbnails and uploads above the default daily limits need phone verification (Feature eligibility table, https://support.google.com/youtube/answer/9890437).

### Actions for us (5)
1. Keep AI use limited to clipping, captions, script help and (if used) a synthetic voice reading our own original script; do not alter footage; do not recreate scenes. No disclosure needed for that, but when in doubt tick "AI use" (the page says disclosure alone does not limit reach or earnings). Low effort.
2. Set `privacyStatus` explicitly on every API upload and verify the resulting visibility in the response (the Nov 2 change reversed a rule our tooling may have worked around). Low effort.
3. Cap clips per story and require visible variation (different official source, different angle, narration) so the channel does not read as templated; revisit the 3-per-story rule. Medium impact, low effort.
4. Do not use an AI persona for politics, legal or health commentary. William already holds politics; keep it that way.
5. Re-read this page's policy block quarterly; the policy text changed July 2025, May 2026 and Oct 2026 (changelog).

---

## Top 10 actions (impact first, effort noted)

1. **Add original narration and context to long-form and Shorts** so viewers "can tell there's a meaningful difference" from the agency video; do this before applying to YPP. (High impact, medium-high effort.) Section 4.
2. **Fix what a visitor sees:** rewrite the description (what, official sources, credit, cadence), add a profile link and contact info, add a banner tagline. (High impact, 10 minutes.) Section 2.
3. **Turn on the Home tab and add a channel trailer for non-subscribers** plus sections (Latest Shorts, story playlists, Full briefings). (Medium-high impact, 20 minutes.) Sections 1-2.
4. **Verify Advanced feature access** (Settings > Channel > Feature eligibility; verify with ID if needed) to unlock Related Video, pinned comments, clickable links and the YPP application. (High impact, low effort.) Section 1.
5. **Clean the channel's theme:** move or hide the gaming, GTA 6 and other-creator clips (William's call; reversible) so the main theme is clearly news. (High impact for review, low effort.) Sections 2 and 4.
6. **Make long-form the watch-hours engine:** weekly narrated 5-10 min 16:9 briefings; plan for roughly 100,000-190,000 views of the 3:36 format (or fewer with longer, well-retained videos) for 4,000 hours, 75,000-140,000 for the 3,000-hour early tier. (High impact, medium-high effort.) Section 3.
7. **Link every news Short to long-form via Related Video**, and group Shorts into story playlists or Shorts Series. (Medium impact, low effort per item.) Sections 1 and 3.
8. **Add a promise-style subscribe line and pinned comment**, reply to comments, and measure subscribers by format (Analytics > Content > Subscribers) for 20+ posts before judging. (Low-medium impact, low effort.) Section 1.
9. **Limit repetition:** fewer near-identical clips per story, and keep non-agency sources to 60 seconds or less (a Short over one minute with any claim is blocked). (Medium impact, low effort.) Sections 4 and 5.
10. **Prerequisites and hygiene:** 2-Step Verification on, no strikes, AdSense ready, "Get notified" in Studio > Earn, explicit `privacyStatus` on API uploads, apply only after the narrated library exists (review takes about a month; a rejection costs 30-90 days). (Low effort, avoids delay.) Sections 3 and 5.

---

## Open questions (unverified, need William or Studio access)
- Does the account have Advanced feature access (Settings > Channel > Feature eligibility)? Does it show the Shorts Series option?
- Is the 3:36 supercut horizontal or vertical? Its distribution depends on that.
- Subscriber source breakdown (Analytics > Content > Subscribers) and the subscribed/not-subscribed split: the API call for the subscribed-status report failed in our analytics file (HTTP 500), so ask William for a screenshot.
- Exact detail of Creator Insider's "Prioritizing Original Content on YouTube Shorts" (chapter at 4:30, https://www.youtube.com/watch?v=SmT_pTMF2ms, published 2026-10-16) and the "Shorts Bonus Program Pilot" in the same video: I could read only the description, not the transcript. Watch the 5-minute segment before finalizing the Shorts approach, since an original-content push on Shorts bears directly on us.
- Whether advertiser-friendly rules cut ads on our violent-crime clips (read https://support.google.com/youtube/answer/6162278 in full).
- Whether the main YPP review would consider our process "original" in practice: only YouTube can say.

## Sources
All fetched 2026-11-07 unless noted.
- YouTube channel monetization policies (reused content, inauthentic content, unsatisfying/off-putting, AI personas, creator integrity; changelog notes July 15, 2025): https://support.google.com/youtube/answer/1311392
- YPP overview and eligibility (4,000 hours / 10M Shorts views; review timing; reapply windows): https://support.google.com/youtube/answer/72851
- Expanded YPP (500 subscribers; country list incl. US): https://support.google.com/youtube/answer/13429240
- Choose how to monetize (tier table): https://support.google.com/youtube/answer/94522
- YouTube Shorts monetization policies (Creator Pool, 45%, 10M threshold from Feb 1, 2027, ineligible views, blocked Shorts): https://support.google.com/youtube/answer/12504220
- Understand three-minute Shorts (aspect ratio rule, claimed content over one minute blocked): https://support.google.com/youtube/answer/15424877
- Shorts views and engaged views: https://support.google.com/youtube/answer/10059070
- How engagement metrics are counted / Content tab subscriber source: https://support.google.com/youtube/answer/12220281 and https://support.google.com/youtube/answer/2991785
- Customize channel layout (Home tab, trailer, spotlight, sections): https://support.google.com/youtube/answer/3219384
- Manage channel branding (banner, avatar, watermark): https://support.google.com/youtube/answer/10456525
- Manage channel profile (description, links, handle): https://support.google.com/youtube/answer/2657964
- Channel banner and profile picture tips: https://support.google.com/youtube/answer/12950272
- Add a related video to your Shorts: https://support.google.com/youtube/answer/14075157
- Sharing links with your audiences (what is clickable): https://support.google.com/youtube/answer/13748639
- Feature access (Standard / Intermediate / Advanced): https://support.google.com/youtube/answer/9890437
- Subscribe to channels: https://support.google.com/youtube/answer/4489286
- Tips: fanbase https://support.google.com/youtube/answer/11913421, new/casual/regular viewers https://support.google.com/youtube/answer/13615784, upload schedule https://support.google.com/youtube/answer/13616979, comments https://support.google.com/youtube/answer/11913117, Posts https://support.google.com/youtube/answer/11912631, why Shorts https://support.google.com/youtube/answer/13363900
- Reply to comments with a Short: https://support.google.com/youtube/answer/12816427
- Copyright on YouTube / fair use: https://support.google.com/youtube/answer/2797466
- Disclosing use of GenAI content: https://support.google.com/youtube/answer/14328491
- YouTube policy updates changelog (Nov 2026, Oct 2026, May 2026, July 2025, Oct 2024, March 2025): https://support.google.com/youtube/answer/10008196
- Video privacy settings: https://support.google.com/youtube/answer/157177
- YouTube Data API revision history (Nov 2, 2026 unverified-project privacy change; Nov 3, 2026 Shorts thumbnails): https://developers.google.com/youtube/data/revision_history
- videos.insert reference (quota, privacyStatus default): https://developers.google.com/youtube/data/reference/rest/v3/videos/insert
- Creator Insider (public channel page, listing as of 2026-11-07): https://www.youtube.com/@CreatorInsider/videos; Shorts Series (2026-09-25) https://www.youtube.com/watch?v=AkNszeQ77MM; Shorts Bonuses and "Prioritizing Original Content on YouTube Shorts" (2026-10-16, description only) https://www.youtube.com/watch?v=SmT_pTMF2ms; Home page/Ask YouTube (2026-09-25) https://www.youtube.com/watch?v=9ODlofcSciM
- Our channel (public, signed out): https://www.youtube.com/@wrdclipz and /shorts
- Local: `projects/opusclip/NEWS-PLAYBOOK.md`, `projects/opusclip/data/subscriber-analytics-2026-11-07.json`, `projects/opusclip/MONETIZATION-STATUS.md`
- Not reachable or not used: Google/DDG web search (blocked by a bot challenge; not bypassed), the "YouTube Algorithm 2026" Creator Insider video (no description or transcript retrievable), the full advertiser-friendly guidelines page (not read this pass).
