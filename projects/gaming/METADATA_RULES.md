# Metadata rules (wrdgamingclipz Shorts)

Standing rules, approved by William 2026-11-18, from `out/TAG_RESEARCH_20261118.md` (raw data `out/tag_research_20261118.json`).
Implemented in `clip_queue.py` (`make_yt_title`, `finish_title`, `make_hashtags`, `make_tags`, `make_tiktok`); applied to the live channel on 2026-11-18 (before/after snapshots `out/metadata_audit_20261118_before2.json` / `_after2.json`, plan `out/metadata_plan_20261118b.json`).

**Evidence caveat.** The research is a YouTube search sample (652 videos, 582 kept at <=180 s; GTA 6 n=292, Fortnite n=178, Elden Ring n=92; small channels GTA 133, Fortnite 58, Elden Ring 83). It is survivor-biased toward high-view videos and every finding is a correlation, not an A/B test. YouTube's own guidance ranks title, thumbnail and topic above tags. Treat the rules as defaults to follow and re-check after a few weeks of our own view data.

## Hashtags
- Max 3 per video, `#GTA6` first on GTA clips (the first three appear above the title; more than 15 and YouTube ignores all of them).
- Never `#Shorts`, never `#GTA6Gameplay` (0 of 12 small-channel hits), never hashtags in the title. Skip `#viral #fyp #trending #gaming` on YouTube.
- Slots 2-3: `#GrandTheftAuto6`, `#GTAVI`, a topical tag (`#ViceCity`, `#Bigfoot`), `#RockstarGames` for news/trailer only. A streamer tag only when that person is actually in the clip.
- TikTok caption (separate): `#GTA6` + two content tags + `#fyp`.
- Fortnite: `#Fortnite` first, then `#DevilFruit` / `#Luffy` / topical. Elden Ring: `#EldenRing` first. Quest/guide hashtags (`#FortniteQuests`, `#FortniteGuide`, `#FortniteXP`) are the first to drop.

## Titles
- <=60 characters (Fortnite <=45), no all-caps words (acronyms like GTA, PS5, FPS, DLC are fine), no repeated phrases ("Vice Beach: Vice Beach Got Cooked"), no hashtags.
- GTA titles lead with the hook or a number, not "GTA 6 <Type>:". The game name goes mid or end ("Fighter Jets Chase Typical Gamer in GTA 6"). Game name in the first three words did worse (9% vs 31% >=10k, fresh cohort). Exception: walkthrough series titles keep "GTA 6 Walkthrough Part N" because that is the search phrase.
- Prefer these patterns where the clip supports them: a number or count ("5 Things ...", 71% vs 24% hit), a comparison ("GTA 6 vs GTA 5"), a spec/edition/purchase angle ("30 FPS on PS5 Pro", "Standard vs Ultimate"), a named Easter egg reference.
- Streamer-name titles only when that person is in the clip AND it is one specific quotable moment ("xQc Isn't Buying 30 FPS"), not "<name> reacts to ...". Streamer-name titles in the fresh cohort hit only 6% (n=36).
- Avoid "leak" in titles unless verified (2% hit, n=41).
- Never claim something the footage does not show. When the clip is unknown, keep the title conservative.
- Fortnite: sprite and Luffy/Gum-Gum moment titles, <=45 characters, 10-30 s clips. Avoid guide and quest titles (quest videos 4% >=10k, n=26).
- Videos with meaningful views: change tags/hashtags only, not the title, unless it breaks a rule above.

## Tags
- GTA: 8-10 tags. Core: `gta 6`, `gta6`, `grand theft auto 6`, `grand theft auto vi`, `gta vi`, `rockstar games`; then 3-4 phrases that appear in the title or footage (subject, mechanic, location, named person). Add `gta 6 easter egg` / `gta 6 secrets` / `gta 6 details` for easter eggs, `gta 6 walkthrough part 1` only for part-1 walkthroughs, `gta 6 release date` only for release-date content, `gta 6 trailer` / `gta 6 news` for news.
- Never tag things not in the video (`ishowspeed`, `adin ross`, `kai cenat`, `gta 5`, other games).
- Fortnite: 8-10; include both `fortnite pirate token` and `pirate shop token` / `fortnite pirate shop token` for token videos, plus `fortnite sprites`, `luffy fortnite`, `fortnite gum gum fruit` where relevant.
- Elden Ring: 8-10; `elden ring dlc` and `shadow of the erdtree` only for DLC content.
- Tags are a weak signal (spelling variants only); do not pad.

## Procedure for live edits
Use `yt_edit_gaming.py VIDEO_ID --title ... --desc-file ... --tags ...` (it carries `privacyStatus` and `publishAt` through; check with `--dry-run`, which prints a STATUS line). Save a before snapshot first, read each video back after saving. YouTube returns tags sorted, so compare them as a set; they can take ~30 s to appear.
