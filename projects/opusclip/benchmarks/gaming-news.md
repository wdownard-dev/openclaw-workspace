# Benchmark: GTA 6 and new-game news clippers (YouTube Shorts)

Collected 2026-11-06 (~16:00-16:25 ET), read-only. **Status: INCOMPLETE.** yt-dlp pulls hung after the first three channels (shared IP, several parallel yt-dlp jobs on the box, no JS runtime for yt-dlp). Only 3 channels have timestamped posting data, and each has only 11-16 Shorts, not 30. DuckDuckGo blocked the bot, so candidates came from YouTube search through yt-dlp.

## Channels with posting data (Shorts tab, latest 11-16 items)

| Channel | Subs | Shorts sampled / window | Posts/day (14d) | Top posting hours (ET) | Wkend share | Views median / mean / top-3 | Breakouts (>3x median) | Median len | Last post |
|---|---|---|---|---|---|---|---|---|---|
| [TmarTn2](https://www.youtube.com/channel/UC36MGPfPwOWafAXauiV4LdA) | 5.68M | 12 / 8.7 days | ~1.4 | 17h(3), 18h(2), 10h(2) | 3 of 12 | 121K / 135K / 340K, 244K, 163K | 0% | 30s | ~24h ago |
| [Luke Stephens CLIPS](https://www.youtube.com/channel/UCCT0-fxrMR-2Jv-DNs-MSHA) | 58.3K | 11 / 76 days | ~0.2 (3 in 14d) | scattered (12h, 03h, 04h; n=3) | 1 of 3 | 63K / 98K / 229K, 225K, 217K | 27% (3 of 11) | 51s | ~4h ago |
| [MrBossFTW](https://www.youtube.com/channel/UC0PMQXAwF6O6aeTpv962miA) | 3.19M | 16 / ~984 days | 0 (stale) | n/a | n/a | 25K / 27K / 52K, 39K, 39K | 0% | 58s | Shorts tab last updated Dec 2024; not a current Shorts poster |

Treat MrBossFTW as excluded: his channel is long-form now, and the Shorts tab is old.

## Candidates found but NOT measured (no posting data pulled)

| Channel | Subs (YouTube search) | Notes |
|---|---|---|
| [TGG](https://www.youtube.com/channel/UC72PuhDwKtZ5MikpGNhPAtA) | 2.29M | GTA 6 news; pull never completed |
| [Top5Gaming / T5G](https://www.youtube.com/@T5G) | n/a | Shorts tab is mostly Fortnite right now; top Shorts 700K+; pull never completed |
| [Sav](https://www.youtube.com/channel/UC0siHv9ReVxBp3bJYWGeNAw) | 62.1K | GTA 6 weekly news; long-form seen, Shorts unknown |
| [GTA6 Game Lovers](https://www.youtube.com/channel/UC2PKGKfAUQc9-K7HOVCyi4A) | 125K | pull never completed |
| [GTA Insights](https://www.youtube.com/channel/UC5HCO9Q7Y5ZETGhWjaI3zng) | 27.7K | pull never completed |
| [Battlehub Zone](https://www.youtube.com/channel/UCeU3SJPcF1U3xqSgd-MEH5g) | n/a | CoD / MW4 / BF6 Shorts clipper; flat Shorts-tab view counts 1K-8K (one MW4 Short about 1.0M in search); pull never completed |
| [Moxly](https://www.youtube.com/channel/UC1wsgif3wVAAmWIoLt1SKmA) | n/a | GTA 6 news Shorts, about 1.4K views on the latest; likely small |
| [Hazard](https://www.youtube.com/channel/UCI1-J45WXprOQQ_m9pmfW9A) | n/a | GTA Online and GTA 6 Shorts, 7K-49K on the latest; mixed topic |
| TheGamingRevolution, InkTV, LegacyKillaHD | n/a | MW4/DMZ, CoD and GTA 6 channels; mostly long-form, Shorts sparse |

Many tiny "GTA 6 News/Leaks/Shorts" channels (under 300 subs, mostly AI or reuploads) turned up in channel search and were skipped as noise.

## Directional patterns (from the 3 channels above; low n)

- **Cadence:** The one high-volume channel (TmarTn2) posts about 1-2 Shorts/day, with two or three on the busiest days. Luke Stephens CLIPS is slower, about 1-2 per week at 11 Shorts over ~76 days. Neither runs a high-frequency clip farm.
- **Timing:** TmarTn2 clusters in the late-morning to early-evening window, 10:00-18:00 ET (3 of 12 posts at 17h, others at 10h-18h), mostly weekdays (9 of 12). Luke's 3 recent posts are spread across the clock, so no signal there.
- **Speed:** Unknown. Not measured against source videos or events. TmarTn2's "Rockstar Updated the GTA 6 Release Time" hit 340K on Tue 11-03, and the "Netflix mission" Short was posted Thu 11-05, but I did not link either to a source event timestamp.
- **Length:** TmarTn2 median 30s; Luke Stephens CLIPS about 51s. Both well under the 60s cap.
- **Titles:** Nearly all use caps emphasis (92-94% in TmarTn2 and MrBossFTW, 64% in Luke's). TmarTn2 puts an emoji in about 92% of titles and few hashtags (17%). Luke Stephens CLIPS uses hashtags in 82% and a trailing "..." teaser style. No "BREAKING" and no source credit in any title sampled.
- **Breakouts:** TmarTn2's views are steady (121K median, none above 3x). Luke Stephens CLIPS is spikier (27% above 3x median, top 3 at 217-229K against a 63K median), driven by opinion and take hooks ("No Chance GTA 6 Runs Past 30FPS...", "Fans Are Attacking Critics Over...").
- **Views vs. subs:** Luke Stephens CLIPS gets about 1K-4K views per 1K subs on its median, far above its 58K subs. TmarTn2's median is about 2% of its 5.7M subs, so it's more a steady audience than a viral one.

## Caveats

- n is 11-16 Shorts per channel, with no timestamped data for the other candidates. Treat everything above as directional, not a benchmark.
- View counts are a weak proxy: they depend on age (recent posts are still accumulating) and on the algorithm, and the flat Shorts-tab counts are rounded.
- Weekend and hour distributions have too few points to trust, especially Luke Stephens CLIPS (3 posts in 14 days).
- Subs for non-measured channels come from YouTube channel search and may be rounded or stale.
- Not measured: speed to post, whether the clips re-cut a named source, and the T5G / TGG / Battlehub / GTA6 Game Lovers numbers. Rerun the pulls with fewer parallel jobs and `--js-runtimes node` when the box is quieter; the scripts are in /tmp/gn/scripts (outside the repo).
