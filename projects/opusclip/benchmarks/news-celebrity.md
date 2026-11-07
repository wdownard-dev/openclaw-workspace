# Benchmark: News and celebrity-news Shorts (posting patterns)

Collected 2026-11-06 (Fri, ~16:00-16:20 ET) with yt-dlp, read-only. Latest ~30 Shorts per channel from the `/shorts` tab. All hours are America/New_York. Conclusions are **directional**.

## Table

| Channel | Subs | n | Span of the n posts | Posts/day* | Top hours (ET, 3h blocks) | Wkday/Wkend | Views median / mean | Top-3 views | Breakouts (>3x median) | Median length | Title style |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [Forbes Breaking News](https://www.youtube.com/@ForbesBreakingNews/shorts) | 5.63M | 30 | 45d | 0.7 (10 in last 14d) | 15-18 (14 of 30), 12-15 (7) | 97/3% | 18.2k / 53.7k | 919k, 71k, 59k | 13% | 21.5s | Speaker + quote, no hashtags; "BREAKING NEWS:" prefix on 13% (includes the 919k hit) |
| [Inside Edition](https://www.youtube.com/@InsideEdition/shorts) | 13.8M | 30 | 31d | ~1.0 (10 in last 14d) | 06-09 (11 of 30), 12-15 (8) | 87/13% | 16.2k / 26.6k | 179k, 107k, 69k | 10% | 78.5s | Short human-interest headline + `#shorts` (100%) |
| [E! News](https://www.youtube.com/@enews/shorts) | 2.67M | 30 | 3.7d | ~8 (6-9 per day) | 15-18 (8), 18-21 (7) | n/a (span has no weekend) | 9.2k / 16.4k | 87k, 44k, 42k | 23% | 40s | Full-sentence caption, emoji, hashtags on 23% |
| [TMZ](https://www.youtube.com/@TMZ/shorts) | 5.2M | 29 | 1.8d | ~10-13 (6, 13, 10 so far) | 18-21 (10), 12-15 (9) | n/a | 2.8k / 3.9k | 12.8k, 11.4k, 10.8k | 10% | 95s | Plain headline, mostly politics/celebrity, no hashtags |
| [NewsNation](https://www.youtube.com/@NewsNation/shorts) | 2.8M | 30 | 3.1d | ~6-9 | 15-18 (11), 12-15 (7) | n/a | 3.5k / 6.4k | 37k, 26k, 15k | 13% | 105s | Headline + `\| Show name` suffix on 47% |
| [WPLG Local 10](https://www.youtube.com/@WPLGLocal10/shorts) | 1.12M | 28 | 3.8d | ~3-11 (avg 5.6) | 21-24 (7), 18-21 (6), 06-09 (5) | n/a | 938 / 4.1k | 42.5k, 28k, 11.9k | 18% | 33s | Plain local-TV headline; crime, crashes, bodycam |
| [Page Six](https://www.youtube.com/@pagesix/shorts) | 309k | 27 | 2.2d | ~8-10 | 09-18 evenly (7/7/7) | n/a | 604 / 1.45k | 8.9k, 4.9k, 4.8k | 22% | 43s | Caption + `#shorts` (100%), emoji |
| [KVUE (Austin)](https://www.youtube.com/@KVUETV/shorts) | 271k | 30 | 1.8d | ~9-18 (9, 18, 3 so far) | 21-24 (12), 18-21 (9) | n/a | 454 / 1.0k | 6.3k, 4.7k, 2.2k | 30% | 49.5s | Plain local headline, no hashtags |

\* Posts/day: where the 30 posts span <14 days I used n / span (a floor on the true rate, and the per-date counts are shown instead of a 14-day figure). Only Forbes and Inside Edition span more than 14 days.

**Not collected:** Daily Mail (only 2 rows came back, no usable stats; skipped). Small "celebrity news" clipper channels surfaced by YouTube search had near-zero views (under ~200), so none made the shortlist. See caveats.

## Pattern (directional)

- **Two cadence tiers.** Volume shops (TMZ, E!, Page Six, NewsNation, KVUE, WPLG) post roughly 6-18 Shorts per weekday. Curated re-cutters (Forbes Breaking News, Inside Edition) post about 0.7-1 per day. The volume shops do not get more views per post: their medians are 0.5k-9k, versus 16-18k for the two slow channels.
- **Timing windows.** Volume channels cluster in the afternoon, 12:00-18:00 ET (E!, NewsNation, Forbes, Page Six), with TMZ peaking 18:00-21:00. Local TV (KVUE, WPLG) leans to the evening, 18:00-24:00, around local newscasts, and WPLG has a second bump at 06:00-09:00. Inside Edition's most common slot is 06:00-09:00 (11 of 30), then early afternoon.
- **Weekends.** Where the span covers weekends (Forbes, Inside Edition) weekend posting is 3% and 13%. For the other six, the sample is Mon/Tue-Fri, so the weekend split is unknown.
- **Speed.** Not measurable from metadata. Titles and content point to same-day posting (Forbes clips are of current-week political events, WPLG posts the day's crash and bodycam stories, TMZ and Page Six post about that day's events). Speed to post is **unknown** in hours.
- **Length.** Medians vary widely: local TV and Forbes are short (21-50s), E! and Page Six are about 40s, and Inside Edition, TMZ and NewsNation run 78-105s (with some 2-3 minute clips, so some of these are borderline long). Forbes ranges 9-91s with a 21s median.
- **Titles.** Mostly plain declarative headlines with names and quotes. No channel uses all-caps. "BREAKING NEWS:" appears on 13% of Forbes titles, including its 919k outlier (n=4, so only a hint). Hashtags are inconsistent: `#shorts` on 100% of Inside Edition and Page Six titles, none on most others. A "| Show" suffix is used by NewsNation (47%). Only Forbes frames clips as a person's quote or reaction, with no source credit in the title.
- **Breakouts.** 10-30% of posts exceed 3x the channel median, so most channels have a fat right tail. The high rates on KVUE (30%) and Page Six (22%) partly reflect a low, noisy median with a recency bias (see caveats). The strongest absolute hit was Forbes at 919k, about 50x its median.

## Caveats

- **These are mostly mainstream outlets, not pure Shorts clippers.** Only Forbes Breaking News (re-cuts of official and press-event footage) and, loosely, the local-TV channels match the "official-source re-cutter" description. I did not find an independent, Shorts-only breaking or celebrity-arrest clipper with clear traction. YouTube search returned only tiny channels, and the DuckDuckGo search I tried was blocked by a bot check. Treat the shortlist as the closest reachable proxy, not a clipper-specific benchmark.
- **Views are a weak proxy and age-biased.** For channels whose 30 posts span only 2-4 days, the newest clips have had little time to accumulate views, so medians and breakout shares are understated or noisy. n=27-30 per channel.
- **Views versus subscribers are low across the board** (for example TMZ median 2.8k on 5.2M subs, WPLG 0.9k on 1.1M). Subscriber counts reflect long-form and cross-platform audiences, so the Shorts feed is probably not the main draw.
- **Not visible:** upload-to-event delay, whether clips were reposted or cross-posted, YouTube-side distribution, and any deleted or unlisted Shorts. The Shorts tab may omit or reorder some items. Post counts come from the tab's visible items only.
- Top-hour counts are small (n=27-30), so only the broad windows above are meaningful, not exact hours.
- Raw data (JSONL) is in `/home/williamdownard/openclaw-sites/news-data/`; scripts are in `/home/williamdownard/openclaw-sites/news-scripts/`.
