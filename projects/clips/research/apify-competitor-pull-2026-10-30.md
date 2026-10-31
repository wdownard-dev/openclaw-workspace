# Apify competitor pull: what top clips on our campaign tags look like (2026-10-30)

Scout, for Morpheus. Public TikTok data only. No logins, no posting, no account actions, no video downloads. Thumbnails are the TikTok cover image (frame 0) only.

## 1. Spend and account state

| Item | Amount |
|---|---|
| Apify plan | FREE, $5 monthly usage cap (`maxMonthlyUsageUsd: 5`) |
| Usage this cycle before this task (cycle 2026-10-28 to 2026-11-27) | $2.497 |
| Source of that pre-task spend | Six `clockworks/tiktok-scraper` runs on 2026-10-28, 20:22–20:57 UTC (run IDs `TPBIveDW7DhRGckQJ`, `d0GHsh8IAPDucls11`, `UbRHLni0b5vCC5vPU`, `L648pnJwYrMosOuh7`, `Y9UEXoOHZoaIxrNDt`, `bLvu7F9CxCKfp8h5p`). Not started by this task. |
| Run 1: `clockworks/tiktok-hashtag-scraper`, run `hqZgrF1W5RnWYUn75` | $0.450, 150 items |
| Run 2: `clockworks/tiktok-scraper` (keyword search), run `G0nfqw2SiltmFIevO` | $0.142, 38 items |
| **This task's spend** | **$0.592 of the $2.00 approval** |
| Cycle total after this task | $3.089 (under the $5 cap) |

Each run was started with `maxTotalChargeUsd` ($1.00 and $0.75). Neither cap was hit. The Apify token was read from the `APIFY_API_KEY` env var and never printed.

Actor choice: the hashtag scraper was the cheapest per-item actor in the store (about $0.005 per item at list price). The keyword scraper was used because hashtag feeds did not isolate campaign clips (see section 4).

## 2. What was pulled

**Run 1: hashtag feed** (`clockworks/tiktok-hashtag-scraper`, 30 posts requested per tag, 150 returned, 0 duplicates)
- `#unpacked`, `#TotalDramaRoblox`, `#MW4`, `#MW4partner`, `#FamilyGuy`
- Tags come from the campaign briefs: `mrbeast-gaming-mw4/brief.md` requires `#MW4` and `#MW4partner`; `family-guy-halloween/join-package.md` requires `#FamilyGuy` (FTC: `#HuluPartner`); `total-drama-roblox/join-package.md` requires `#TotalDramaRoblox`; HardScope's brief uses `#unpacked`.

**Run 2: keyword search** (`clockworks/tiktok-scraper`, 25 requested per query, 38 returned)
- "Total Drama Island Roblox": 12 results
- "MrBeast Gaming MW4 clip": 13 results
- "Family Guy Halloween hell": 13 results
- "HardScope unpacked clip": **0 results** (no HardScope clips came back at all)

Combined: 188 rows, 182 unique videos after de-duplication across the two runs. 102 of those match a strict campaign rule (see section 3).

Files in `projects/clips/research/apify-data/`:
- `hashtag_raw_items.json`, `search_raw_items.json`: raw actor output
- `run_meta.json`, `search_run_meta.json`: run IDs, dataset IDs, costs
- `combined_posts.csv` / `.json`: flattened fields, with a `bucket` column
- `campaign_matched_unique.json`: the 102 strict campaign matches
- `hashtag_posts_flat.csv` / `.json`: hashtag run only
- `thumbs/`: 12 cover images plus `index.json`

Scripts are in `projects/clips/research/apify-scripts/` (run with `python3 -I`).

Fields kept per post: author handle, author follower count, verified flag, video URL, posted time (UTC), duration, width and height, views, likes, comments, shares, saves (`collectCount`), caption, hashtags, music name and original-sound flag, ad/sponsored flags, slideshow flag, cover URL, language.

## 3. Method and filters

- Sorted by views. The hashtag feed is not sorted by views, so this is our sort.
- **Strict campaign buckets** (caption or hashtags must contain):
  - MW4: `mrbeast` or `mw4partner`
  - Total Drama Roblox: `total drama`, `totaldrama`, `totalrobloxdrama`, `#trd`, `tdi`
  - Family Guy: `family guy`, `familyguy` or `hulupartner`, plus `hell`, `halloween` or `hulupartner`
  - HardScope/Unpacked: `hardscope` or `unpacked`
- Posts that only matched the game name (generic COD MW4 gameplay edits, the *Unpacking* game, Pokémon or soccer card openings) are kept in the data but excluded from campaign stats.
- Counts by bucket (unique videos): MW4 40, Total Drama Roblox 39, Family Guy 18, Unpacked 5. Other or generic: 80.

## 4. Findings

### 4a. The hashtag feed mostly does not show campaign clips

- `#MW4` returned mostly the COD MW4 game (gameplay edits, "Shopping in MW4" edits, `wargamingnc` game promos). It had 30 posts, none tied to the MrBeast event unless the caption said so.
- `#unpacked` returned the *Unpacking* game and unrelated unboxing or card-pack content. Zero HardScope posts.
- `#TotalDramaRoblox` and `#FamilyGuy` were the cleanest tags.
- Practical result: hashtag feeds on these tags are not a campaign-level sample. Keyword search, or a creator list from Vyro/Whop, gives better coverage.

### 4b. Campaign-matched stats (102 unique posts)

| Bucket | n | Median views | Median followers | Share under 1k followers | Median duration | Share 30 s or less | Share original sound |
|---|---:|---:|---:|---:|---:|---:|---:|
| MW4 / MrBeast | 40 | 11,302 | 1,062 | 50% | 24 s | 60% | 78% |
| Total Drama Roblox | 39 | 5,015 | 1,080 | 49% | 24 s | 59% | 95% |
| Family Guy hell | 18 | 2,447 | 98 | 72% | 35 s | 39% | 89% |
| Unpacked / HardScope | 5 | 16,800 | 8,811 | 20% | 29 s | 60% | 60% |
| **All 102** | 102 | 5,319 | 836 | 52% | 25 s | 56% | 85% |

Other all-102 figures: median engagement (likes+comments+shares+saves)/views 5.5%; 88% portrait files (height over width); 76% use three or more hashtags; median caption 100 characters; 87% posted since 2026-10-16.

Top 10 campaign-matched posts by views: median duration 35 s (only 20% are 30 s or less), median engagement 13%, 100% original sound, median followers 55.8k (skewed by large accounts).

**Small-account outliers (under 1,000 followers, at least 5,000 views):** 15 posts in the campaign-matched set. Examples:
- `trd_uploads`: 932,500 views, 363 followers (fan account, a re-upload of the official trailer)
- `perfectclips_1`: 682,000 views, 743 followers (MW4)
- `ter1yaky`: 524,100 views, 229 followers (Family Guy)
- `cloutopia`: 334,400 views, 929 followers (MW4)
- `clipsahoytvv`: 197,200 views, 418 followers (Family Guy)

Small accounts can hit 5k+ on these campaigns. Follower count is not a gate.

### 4c. Layout and hook, from 12 cover images (frame 0 only)

I eyeballed these. Estimates are rough, about ±5% of frame height.

| Account (views / followers, duration) | Layout (frame 0) | On-screen text | Facecam | Logo or handle visible |
|---|---|---|---|---|
| royaldropp (3.7M / 1.1M, 34 s) | 9:16 frame, black bars top and bottom, footage in centre (~55% of height) | Large Spanish caption across lower-middle | No | No |
| streamermomente_ (940k / 103k, 15 s) | 9:16, black bars top and bottom, footage in centre | Short English caption, lower-middle | No | No |
| perfectclips_1 (682k / 743, 31 s) | 9:16, blurred copy bands top and bottom, sharp strip in centre (~50%) | Caption mid-lower, "MrBeast really just created another villain" | **Yes**, small inset top-left | No |
| swagg (510k / 1.5M, 82 s) | 9:16, split: streamer facecam top half, footage bottom half, full-width | Caption top-centre, subtitles at bottom | Yes, top half | Not visible |
| socialinfos (508k / 466k, 32 s) | 9:16, black bars top and bottom | Two-line Spanish caption in centre | **Yes**, inset bottom-left with name tag | No |
| cloutopia (334k / 929, 33 s) | 9:16, black bars top and bottom | Cyan "IF" overlay plus caption, lower-middle | **Yes**, inset top-left with name tag | No |
| trd_luvr13682 (1.9M / 1,200, 59 s) | 9:16 full-frame gameplay | Large white outlined captions, mid-screen | No | No |
| trd_uploads (933k / 363, 57 s) | 9:16, black bars top and bottom, 16:9 trailer | All-caps white title in top band | No | No |
| campistanoaceptad0 (230k / 42k, 60 s) | Landscape 16:9 gameplay, dimmed | Spanish caption, lower-middle | No | No |
| ter1yaky (524k / 229, 61 s) | 9:16, black bars top and bottom, 16:9 footage | "Part 1" title in top band | No | No |
| foxfamilyguy (872k / 2.9M, 36 s) | 9:16, blurred bands top and bottom, sharp centre; Fox/Hulu logos in top band | None beyond logo lockup | No | **Yes** (official Fox/Hulu lockup) |
| clipsahoytvv (197k / 418, 68 s) | 9:16, blurred bands top and bottom, sharp strip in centre (~45%) | White box caption top, "FAMILY GUY HALLOWEEN COSTUMES" | No | No |

Pattern across the 12 covers (observable): six use black letterbox bars around 16:9 footage; three use blurred copy bands (one of them the official Fox/Hulu lockup); two are full-frame or split; one is landscape. Four of the 12 show a streamer facecam (perfectclips_1, socialinfos, cloutopia, swagg). Captions are large, short and mostly lower-third or mid-screen.

### 4d. Findings on how top clips differ from ours

1. **Length is not the lever.** Top-10 campaign clips run about 35 s (median). Ours run 16 to 39 s (mw4-12 15.8 s, mw4-08 22.6 s, tdr-01 23.6 s, tdr-02 27.8 s, mw4-07 39 s, mw4-13 37 s). Ours are shorter than the top-10 median, which contradicts the "shorter wins" idea in `playbook.md`. Observable from metadata, n=10.
2. **Account size and distribution.** Our profile has 3 followers (strategy/2026-10-30-analytics-readings.md). 52% of campaign-matched posts come from accounts under 1k followers, and 15 of them hit 5k+ views. The gap is distribution (For You reach, and the hook in the first seconds), not account size. Observable; cause is a guess.

## 5. Observable vs guessed

**Observable (from data or covers):**
- Length and median duration (metadata)
- Follower counts and the share of small accounts (metadata)
- Hashtags used (captions; e.g. `#mw4partner` on 38 of 40 MW4 matches, `#hulupartner` on 14 of 18 Family Guy matches, `#mrbeast` on 27)
- Original sound share (metadata)
- Letterbox vs blurred-band vs split layout, facecam inset, text placement (covers, frame 0 only)

**Guessed (not observable from this data):**
- Whether the top clips use a hook in the first 1–3 s (we only have frame 0; the cover may not be the first frame played)
- Retention and average watch time (not in the actor output)
- Whether any of these clips were restricted for re-upload packaging (no restriction data in the actor output)
- Posting time and day (createTime is in the data; not analysed here)
- Which layout performs better. The competitor covers show several layouts with high views, so layout alone does not look decisive.

Layout comparison to ours: `strategy/2026-10-30-analytics-readings.md` describes our layout as "real footage ~32% of frame over blurred copy + static text." Competitor blurred-band covers in this sample show a sharp strip at roughly 45–50% of height (eyeballed, ±5%). If the 32% figure is a height measurement, our sharp strip is narrower than the blurred-band competitors. Check our own frame to confirm; the ratio is not in the data.

## 6. Compliance flags for Morpheus

- Copying hashtags: `#mrbeast`, `#callofduty`, `#swagg`, `#fyp` and similar are common on top posts but are not in our briefs. The MW4 brief allows `#MW4 #MW4partner` only ("No other logos, hashtags..."). Do not add them without a check.
- Competitor clips use MrBeast and Fox/Hulu footage with captions. This pull recorded only public metadata and frame-0 covers. Nothing was saved to any campaign folder, and no competitor footage was downloaded.
- HardScope: nothing came back for "HardScope unpacked clip". The HardScope side of this question is unanswered.

## 7. What could not be fetched or measured

- **HardScope / #unpacked campaign clips**: zero results from the keyword search; the hashtag feed returned game and unrelated content.
- **Frames**: only cover images (frame 0) were saved. No multi-frame extraction, no hook timing.
- **Retention and watch-time curves**: not provided by the actors used.
- **Keyword search depth**: the search actor returned about half of the requested results (12–13 of 25 per query). A larger search would cost about $0.003 per extra item.
- **Our own per-post stats**: taken from the 2026-10-30 analytics readings file (9 posts, screen recordings). Not compared post-by-post here.
- **Family Guy "hell" specifically**: the Halloween special is the only tag match. The brief's "hell" term appears in some captions; coverage of the hell clips is thin (18 matches).
- **Post-by-post time series**: not pulled; views are a single snapshot at the time of the run.

## 8. Checks performed

- Usage endpoint read before and after the task; cycle total reconciles to run costs ($2.497 before, $3.089 after, delta $0.592).
- Hashtag run: 150 items, 0 duplicates, all five tags returned 30 each.
- Search run: 38 items, 0 duplicates; one query returned 0 results.
- Covers: 12 downloaded and read with `view_image`. Descriptions in section 4c are from those images.
- Summary numbers recomputed from `combined_posts.json` by `summarize.py`.
