# Campaign pre-screen, 2026-10-28 (Morpheus, read-only)

Requested by William 2026-10-28: pre-screen before presenting options. Ranking is on likely views, not rate (USER.md rule).

## Screen criteria
1. Runway: at least 3 days left. Vyro review takes "a few days" and the new-account rule blocks further submissions until a post is approved, so a campaign ending in 1-2 days is not reachable.
2. Not sponsored with fixed caption lines or a no-edit clip bank.
3. Budget being claimed (paid% moving) but not nearly spent.
4. Rules workable for a small cold account.
5. Other clippers' TikTok results (where obtainable).
Not done: Frame.io footage previews (durations and content unverified for every campaign).

## Evidence gathered
- TikTok tag pages block logged-out browsing; DuckDuckGo started a bot challenge after ~8 queries (not bypassed). Bing/Brave via curl return no TikTok links. Vyro campaign leaderboard shows only our own ranking and does not load other clippers.
- Valorant Microdrama, 5 clipper posts found (2-3 weeks old): 1,891 (72 followers), 798 and 574 (3.2k followers), 299 (30 followers), 79 (38 followers). None near the 5,000-view payout threshold. Official 2.9M-follower creator post: ~590k.
- Vyro-side demand signal (paid% change Oct 27 -> Oct 28): StinkyAsher 12->15, Flamingo 9->11, Microdrama 9->10, Kevin Langue 58->59, Ground Stop 43->44, TDR Streamer Tournament 7->8, TDR Sinjin 9->9 (flat), Mitch 0->0, Valorant Champs 2->2.
- Submission allowance seems per campaign: MW4 took 3 submissions then blocked; TDR took 3 then blocked (observed Oct 23-27). Inference: each newly joined campaign gives about 3 more submission slots before an approval is needed. Two observations only.

## Verdicts
- Out (runway): Kevin Langue (2d), Valorant Champs (2d), TDR Streamer Tournament (1d), Ground Stop (1d).
- Out (sponsored, rigid terms): Ketone-IQ campaigns.
- Out (weak evidence): Valorant Microdrama (clipper posts do not reach 5k), TDR Mitch (0% paid after ~7 days listed).
- Candidates: TDR StinkyAsher (5d, 15%, rising), TDR Flamingo (5d, 11%, rising), Joy 101 (13d, 0%, non-gaming, sensitive-topic rules, 30s min, no performance data).
- Joined, keep: TDR Sinjin.
All joins still need William's Accept/Confirm flow.

## Apify TikTok screen, 2026-10-28 ~5 PM ET (non-TDR, per William)
Method: clockworks~tiktok-scraper via protected APIFY_API_KEY; 30 newest videos per hashtag; ~$1.10 for the run. Hashtag-wide numbers are skewed by big accounts, so the "partner" tags (what clippers must use) are the closest proxy for campaign clipper results.
- Kevin Langue (#kevinlanguepartner, n=30, median 931 views, p75 1.5k, 5 of 30 >= 5k, 4 of those from accounts with <1k followers; 56k/24k/11k from 1-12 follower accounts but 9-23 days old; 0-7 day old posts mostly ~1k). Main #kevinlangue tag: 14 of 21 recent posts >= 5k. Campaign ends ~Oct 30 (2d at 7:30 AM), 59% paid, single source video, so timing is the problem, not the niche. Watch for his next campaign.
- Valorant Microdrama (#valorantmicrodrama, 20 small accounts, 0 >= 5k, median ~250): poor.
- Valorant Champs (#valorantchamps: big-account event highlights dominate; small-account hits are gameplay/edit highlights, not podcast clips; campaign ends ~Oct 30): skip.
- Ground Stop (#groundstoppodcast, n=30, median 239, 1 >= 5k): skip.
- Joy 101 / Hoda Kotb (#hodakotb recent 30d small accounts median ~240, #iheartpodcasts median 278, #joy101 only 6 recent posts): weak clipper evidence; longest runway (~Nov 10), 0% paid. A targeted caption search timed out (no data).
- MW4 now shows "Locked for new posts".
- Note: posts with #VALORANTpartner about the "Hush" agent are a different Valorant program, not this campaign.
