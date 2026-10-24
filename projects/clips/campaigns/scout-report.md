# Vyro campaign scout report

Run: 2026-10-23 ~8:00-8:04 PM ET, by Scout (E2E test, stage 1). Source: signed-in app.vyro.com session, one dedicated browser tab, read-only (only clicked campaign cards, "Load more" and "Show more"; nothing joined, submitted, typed or changed). Every campaign figure below was read from its detail dialog on this date. Percent paid and days left change hourly.

15 campaigns listed after one "Load more": 11 open, 4 "Locked for new posts". Joined: only MrBeast Gaming MW4 (My campaigns page: Live 1, Past 0; 3 submissions pending, 0 approved; Earned $0, Views 0, 13d left, 26% paid out).

## Ranked: best campaigns for a gaming-oriented Shorts channel
All open campaigns accept TikTok videos, YouTube Shorts and Instagram Reels unless noted. Every one requires 5,000 views/post for payout (max $1,000/post), likes/comments ON, no boosting, no botting, and every footage source is a PUBLIC Frame.io share (f.io link returns HTTP 200 without login; verified by curl, nothing downloaded).

| # | Campaign | Ends | Paid | Rate/1k | Min len | Joined | Collab | Footage | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | MrBeast Gaming: Escape Call of Duty's DMZ (CoD MW4) | 13d | 26% | $1.50 | 15 s | YES | not allowed | 1 file, already local (25m12s) | Best: gaming fit, joined, footage and 6 clips already made, longest runway |
| 2 | Total Drama Roblox: Sinjin "ROBLOX TOTAL DRAMA ISLAND is mean…" (NEW, 7h old) | 13d | 0% | $2.50 | 15 s | no | allowed (story banned) | 1 Frame.io video | Highest rate, full budget, longest runway. Roblox audience skews young; needs join |
| 3 | Valorant Champs Shanghai Podcast | 6d | 2% | $1.50 | 15 s | no | allowed in settings, text says "Collab & story posts are NOT allowed" (follow stricter) | 2h24m podcast, already local | Footage ready, 5 suggested moments; 6d and only 2% paid after 7d suggests the bar is hard |
| 4 | Total Drama Roblox: Mitch Gaming | 9d | 1% | $2.50 | 15 s | no | not allowed | 1 Frame.io video | Same terms as #2, shorter runway |
| 5 | Total Drama Roblox: StinkyAsher | 9d | 10% | $2.50 | 15 s | no | not allowed | 1 Frame.io video | Same terms as #2 |
| 6 | Total Drama Roblox: Flamingo | 9d | 6% | $2.50 | 15 s | no | not allowed | 1 Frame.io video | Same terms as #2 |
| 7 | Valorant Microdrama series | 9d | 4% | $1.50 | 15 s | no | not allowed | episodes (Frame.io) | Scripted drama; split in "Part 1, 2, 3" or brand-safe memes; weaker clip fit |
| 8 | Total Drama Roblox: Streamer Tournament (Jenny Hoyos upload) | 5d | 5% | $2.50 | 15 s | no | not allowed | 1 Frame.io video | Same terms, only 5d left |

## Top 5 detail for the end-to-end test (the five extra checks)
Hashtags: MW4 = #MW4 required, #MW4partner disclosure (or native label). TDR (all) = #TotalDramaRoblox required, #paidpartnership disclosure (or native label). Valorant Champs = no required hashtag, disclosure #valorantchamps only.

1. MW4 (JOINED). (a) Footage supplied: yes, https://f.io/_a1-OEVL, one file 'Escape Abandoned City.mp4'. Download is a manual-style Frame.io "Download" button, but scripts/fetch_frameio.py (Playwright) already automated it and the 7.5 GB file is local (clips-work/mrbeast-mw4-source.mp4 + transcript). No plain direct file URL exists; a script must click through Frame.io. (b) Joined: yes (My campaigns). (c) Platforms: TikTok videos, YouTube Shorts, Instagram Reels. (d) Brief wording on automation/scheduling/third-party tools: NONE (read the full brief; the closest lines are "We review every post for botted views" and "Clips running as a paid ad will be rejected (e.g. 'boosting' your clip as a promoted post)"). Vyro-wide wording (Clipper Terms and Content Requirements s.10) does apply, see below. (e) 20-40 s vertical clip: yes, already proven (mw4-01..06 are 31-44 s, 1080x1920). Note: collab/tags not allowed; likes/comments ON.
2. TDR Sinjin. (a) Frame.io https://f.io/Y1AoLXR8, public, same click-through download (no script run yet for this file; durations unverified). (b) not joined. (c) all 3 platforms. (d) No automation wording in the brief (checked the full text). (e) Feasible in principle (tournament vlog footage); duration and content NOT checked (unverified, requires a preview).
3. Valorant Champs Shanghai. (a) Frame.io https://f.io/1XI8aRT3, already downloaded (3.0 GB, 2h24m) and transcribed. (b) not joined (dialog has no "You've joined" line; PLAN.md notes William closed it). (c) all 3 platforms. (d) No automation wording in the brief. (e) Feasible (podcast, 5 suggested timestamps 31:59, 36:14, 55:09, 1:04:34, 2:07:00), needs reframing from landscape talking heads; no logos/watermarks/other hashtags.
4. TDR Mitch Gaming. (a) https://f.io/cn710FBZ (public). (b) not joined. (c) all 3. (d) none in brief. (e) unverified (not previewed).
5. TDR StinkyAsher. (a) https://f.io/7acN1ASv (public). (b) not joined. (c) all 3. (d) none in brief. (e) unverified (not previewed).

### Vyro-wide wording on automation (applies to every campaign, exact quotes)
- Clipper Content Requirements s.10 (https://vyro.com/content-requirements, fetched Oct 23): "Clippers may promote their own content and campaigns, but must not: Promote Client or its campaigns through spam (e.g., mass messaging, comment spam, or automated posting)."
- Clipper Terms (https://vyro.com/clipper-terms, last modified Dec 20, 2025): "Neither you nor anyone working on your behalf may (A) promote or advertise Client, a Client Campaign, Client Content, or Clipper Content through spam (e.g., mass messaging, comment spam, or automated posting); or (B) run paid advertisements…" Also: "(vii) engage in data mining, scraping, AI/LLM-training or other unauthorized data collection" and Content Requirements s.8: "Unauthorized Data Access: Using bots, scrapers, or automation to collect or manipulate platform data."
- Read: no sentence bans scheduling tools or third-party tools by name. "Automated posting" appears only as an example of SPAM. Whether a scheduler like Buffer posting one clip per platform counts is NOT stated (unverified, open question for Vyro support). The "scrapers/automation to collect or manipulate platform data" line could cover scripted reads of the Vyro site; I use the signed-in browser read-only.

## Avoid / skip
- iHeart "Don't Lie To Me" (5d, 40% paid, $2.00/1k): dating/relationships podcast (poor fit), strict caption template (CTA + "Don't Lie To Me, an iHeart podcast" + #DontLieToMe #ad), every clip/caption must be unique, min 30 s, review takes days.
- Ketone-IQ "Shark Tank Edits" (13d, 2%, $1.50) and "YT Only: Cinematic edits" (6d, 1%, $1.50, YouTube Shorts only): sponsored brand deals (#KetoneIQPartner), provided edit must be posted untrimmed, mandatory caption lines. Skip per the sponsored-campaign rule.
- Locked (no new posts): MrBeast "Lose 150 Lbs Together" (7d, 100%, $1.00), SPEED VEGAS 1 (5d, 100%, $2.10, Reels only, 7 s min), Shark Tank S18 E3 (4d, 100%, $2.00, 30 s min, Disney work-for-hire + AI-tool restriction, unique clips), Valorant Microdrama Episode 1 (12h, 6%, $1.50).

## Warnings
- Ending within 3 days: only Valorant Microdrama Episode 1 (12h left, locked). No open campaign ends within 3 days; shortest open: iHeart and TDR Streamer Tournament (5d), Valorant Champs (6d), Ketone Cinematic (6d).
- Over 80% paid out: Lose 150 Lbs, SPEED VEGAS, Shark Tank S18 (all 100%, locked). No open campaign is over 70%.
- Near the end of every campaign, if earnings exceed the remaining budget, payouts are split evenly across eligible clips (dilution).
- Joined campaign MW4: 26% paid (was 21% on Oct 22 ~9:40 PM, about +5 points per day, 13d left), 3 pending / 0 approved ~22 h after the first submissions.

## What changed since the last report (Oct 22 ~9:40 PM)
- NEW: Total Drama Roblox, Sinjin 'ROBLOX TOTAL DRAMA ISLAND is mean…' (posted 7h ago, 13d, 0%, $2.50, collab allowed).
- No longer listed: Kevin Langue "4 Imposters vs 1 Real Ghost Hunter", Ground Stop Podcast, MrBeast x Kizik (ended or removed; reason unverified).
- MW4 21% to 26% paid; 14d to 13d. iHeart 31% to 40%. Valorant Champs 7d to 6d, 2% unchanged. TDR Mitch 0% to 1%; StinkyAsher 9% to 10%; Flamingo 6%; Streamer Tournament 3% to 5% (6d to 5d). Microdrama 2% to 4%. Ketone Shark Tank Edits 0% to 2%.
- Correction: Mitch Gaming was recorded as 0% paid, today 1%. The TDR Mitch collab rule is "not allowed" (earlier notes agree).
- The 'Payouts active' text on My campaigns is a tab label, not an account status (confirmed earlier).

## Campaign details (one block each)
### 1. MrBeast Gaming: Escape Call of Duty's DMZ, Win $1,000,000 (Call of Duty: MW4) JOINED
13d, 26% paid, $1.50/1k. TikTok videos, YouTube Shorts, Instagram Reels (no carousels/images). Min 15 s. Required #MW4; disclosure #MW4partner (hashtag or native label). Collab and story not allowed. Likes/comments ON. No logos, other hashtags, watermarks. No misrepresenting MrBeast or Call of Duty. Source https://f.io/_a1-OEVL.
### 2. TDR Sinjin
13d, 0%, $2.50/1k. All 3 platforms, 15 s. #TotalDramaRoblox, #paidpartnership. Collab allowed, story banned. Source 'NEW Total Drama Roblox With YOUTUBERS is a MESSSSS.mp4' https://f.io/Y1AoLXR8.
### 3. Valorant Champs Shanghai Podcast
6d, 2%, $1.50/1k. All 3 platforms, 15 s. Disclosure #valorantchamps. Source https://f.io/1XI8aRT3. Own moments allowed.
### 4-6, 8. Total Drama Roblox (Mitch Gaming https://f.io/cn710FBZ; StinkyAsher https://f.io/7acN1ASv; Flamingo https://f.io/k1aKSCNp; Streamer Tournament https://f.io/bxcDZy3B)
Same rules: $2.50/1k, all 3 platforms, 15 s, #TotalDramaRoblox + #paidpartnership, collab and story banned, no outside logos/hashtags/watermarks. Paid/ends: Mitch 1%/9d, StinkyAsher 10%/9d, Flamingo 6%/9d, Streamer Tournament 5%/5d.
### 7. Valorant Microdrama series
9d, 4%, $1.50/1k. All 3 platforms, 15 s. Required #valorant; disclosure #ValorantPartner; no unrelated/general hashtags. Option 1: sequential "Part 1, 2, 3"; option 2: brand-safe memes (no profanity, NSFW, derogatory content). Collab and story banned. Source https://f.io/ySICjlo0.
### iHeart, Ketone-IQ x2, locked campaigns: see Avoid.

## Method and scan limits
- Whole scan took about 4 minutes by the system clock (8:00 to ~8:04 PM ET) in one tab, targetId pinned on every call, no tab recycling.
- Dialog text read via an in-page script (click card, click "Show more", read [role=dialog]). The URL returned right after a click lags one campaign behind, so each reading was matched by the title inside the dialog.
- Not read: durations/content of the non-MW4 Frame.io files (no previews fetched); Vyro clipper-terms page was read only the first 20,000 of 67,687 characters plus a keyword search of the rest.
