# Blue Pill outlier check, 2026-11-11

Method: YouTube Data API (search.list, order=viewCount, videoDuration=long, published in the last 365 days, 12 queries, up to 12 results each), then videos.list and channels.list. 134 videos from 115 channels; 68 kept after filtering to 6-40 min. Outlier = views relative to channel subscribers. Script: outlier_search.py, data: outlier-data-2026-11-11.json. About 1,300 quota units used.

## Caveats (read first)
- `videoDuration=long` means videos over 20 min only, so this check CANNOT say whether 20+ min beats 10-12 min. The length of the winners is a bias of the filter.
- Top-12-per-query is a small sample. View counts are unaudited and some channels look AI-farmed (not verified).
- Several hits are non-English (Hindi, Urdu, Indonesian, French, Spanish). English-only demand is not isolated.
- Subscriber counts are current, views are lifetime, so ratios flatter older videos on channels that have grown.

## Demand by query (median views of top results, count of videos >= 100k)
| Query | n | Median views | >=100k |
|---|---|---|---|
| mythical creatures real animals | 8 | 3.16M | 8 |
| greek gods animated | 4 | 2.10M | 4 |
| myths that turned out to be true | 10 | 1.67M | 10 |
| greek mythology explained | 4 | 1.21M | 4 |
| egyptian gods explained | 5 | 547k | 5 |
| norse mythology explained | 6 | 358k | 6 |
| who was cleopatra | 7 | 198k | 5 |
| what really happened at troy | 8 | 150k | 5 |
| who was zeus | 4 | 109k | 2 |
| who was medusa | 6 | 39k | 2 |
| who was hades | 5 | 7.9k | 0 |

Reading: compilation and myth-vs-reality formats beat single-subject "who was" videos for discovery. Single-subject videos are weakest unless the subject is huge (Cleopatra) or the angle is a hook (the "real story" or DNA/tomb angles).

## Small-channel outliers (under 150k subs, 100k+ views)
- Arcyst, 3.8k subs, 1.03M views, 29 min: "Every GOD OF WAR explained in under 30 minutes"
- Mr. Discovery, 5.3k subs, 1.08M views, 21 min: "How Every Greek Villain Died"
- Yorp, 11.3k subs: "Every Legendary Sword in Mythology Explained in 25 Minutes" (1.11M) and "Every Legendary Weapon of the Gods Explained in 21 Minutes" (464k)
- Mr L, 4.4k subs, 252k views, 28 min: "Every Mythical Creature That's Half Human Explained in 28 Minutes"
- The Ninth Scribe, 3.6k subs, 183k views: "The Book of Enoch Reveals Who Zeus Actually Was..." (a hook-angle single subject)
- Galaxy Vault, 48.5k subs, 1.12M views: Cleopatra DNA angle
- Edukasi Dunia Satwa, 115k subs, 3.5M views (Indonesian): "10 mythical creatures that turned out to be real", part 3 of a series

Pattern: "Every ___ in Mythology Explained in N minutes" style catalogue videos from channels with under 12k subscribers reached around 1M views. That is the strongest signal in this check.

## Other signals
- Large channels: "Historically" (1.64M subs) titles carry "[No AI]" and pull 2.5M-10.6M views, which suggests audience sensitivity to AI-made content. Our stick-figure, human-reviewed format is a different thing but we should expect "AI slop" scrutiny and disclose process honestly if asked.
- "Myths/Conspiracies/Urban legends that turned out to be true" formats are consistent 2M-6M view performers on large channels, in line with the Paint Explainer reference.
- Strong repeating-title patterns: "Every X Explained in N Minutes", "How Every X Died", "Myths that turned out to be true", "Mythical creatures that turned out to be real".

## Implications for the plan
1. Open with catalogue and myth-vs-reality videos (format B), keep "Who was ___" (format A) for hook-angle or high-demand subjects, and treat it as the secondary series.
2. First topics to test, ranked by signal: (a) Greek/Norse/Egyptian "Every ___ explained" catalogues (villains, weapons, monsters, gods' deaths), (b) "Myths that turned out to be true" with a fresh angle, (c) "Mythical creatures that turned out to be real".
3. Test length separately: this check was biased to 20+ min. Spike at 12-15 min, and run a second search without the duration filter before committing to 20-30 min scripts.
4. Don't copy the winning titles; use the patterns, with our own topics and angles.
5. Saturation risk: Greek myths are crowded. Egyptian and Norse had lower medians but also fewer entrants, worth a second look. Less covered mythologies (Mesopotamian, Slavic, Japanese, Celtic, Mesoamerican) are untested here.

---

# Round 2 (2026-11-11 evening): no length filter, more mythologies

Method: 14 queries x two duration buckets (4-20 min and 20+ min), top 15 by views each, last 365 days, English relevance, US region. 311 new videos, 219 channels; merged with round 1 for 402 unique, 286 English-looking videos of 3-60 min analysed. About 2,800 quota units (about 4,100 for the day across both rounds, against a 10k default; check before running more). Scripts: outlier_search2.py, outlier_analyze2.py; data: outlier-data2-2026-11-11.json.

Caveats: same sample bias as round 1 (top results by views, not a random sample); "English" is inferred from audio-language tag and title characters; subscriber counts are current; keyword buckets are small for some mythologies (Norse 6, Slavic 9, Japanese 9); Hindu mythology was not searched.

## Length: 8-16 minutes is as good as 20+ for small channels
| Length | n | Median views | Videos >=100k | >=100k from channels <30k subs |
|---|---|---|---|---|
| 3-8 min | 11 | 22k | 36% | 1 |
| 8-12 min | 40 | 243k | 62% | 15 |
| 12-16 min | 37 | 252k | 59% | 6 |
| 16-20 min | 42 | 82k | 47% | 7 |
| 20-30 min | 90 | 337k | 68% | 18 |
| 30-60 min | 66 | 341k | 69% | 3 |

Reading: 20+ min has a higher hit rate and median, but small channels land most of their 100k+ outliers at 8-12 min (15) and 20-30 min (18); at 30+ min almost only big channels win (3). A 10-15 minute video is a defensible start and costs less to script, voice and render. Round 1's apparent 20+ min advantage was a filter artefact.

## Title patterns
| Pattern | n | Median views | >=100k | of which from <30k-sub channels |
|---|---|---|---|---|
| "Every ___ explained" | 68 | 104k | 50% | 27 of 34 |
| "...turned out to be true/real" | 35 | 871k | 91% | 3 of 32 |
| "How ___ died" | 6 | 153k | 66% | 3 of 4 |
| "Real story / the truth" | 16 | 162k | 62% | 1 of 10 |
| "Who was / who is" | 3 | 21k | 33% | 0 of 1 |

Reading: "Every ___ explained" is the pattern small channels crack (27 of its 34 hits are from channels under 30k subs). "Turned out to be true" has a higher ceiling and hit rate but mostly big channels. "Who was" barely appears and underperforms, consistent with round 1.

## Mythology comparison (title keyword match, English)
| Mythology | n | Median views | >=100k |
|---|---|---|---|
| Egyptian | 20 | 419k | 75% |
| Mesopotamian | 11 | 346k | 90% |
| Japanese | 9 | 323k | 100% |
| Norse | 6 | 193k | 83% |
| Celtic | 10 | 85k | 50% |
| Greek | 54 | 59k | 42% |
| Aztec/Maya | 17 | 34k | 23% |
| Slavic | 9 | 17k | 22% |

Reading: Greek has the most videos by far and the lowest median among the big groups, so it is the most saturated. Egyptian, Mesopotamian and Japanese look like the best view-per-competition lanes in this sample. Small n; treat as directional.

## New channels break out fast
Channels created in 2026 with 1M+ views on a single video: Mythological Man (created 2026-04-30, 34 videos, 11.1k subs; 5 videos over 150k; "Every Mythology in the World Explained" 1.29M, 12 min), Odrin (created 2026-08-24, 7 videos, 2.3k subs; "Terrifying Myths That Turned Out To Be True Explained" 1.03M, 12 min), Arcyst (5 videos, 3.8k subs, 1.03M), Mr. Discovery (created 2026-06, 8 videos, 5.3k subs, 1.08M). Older small channels also work: Yorp (since 2023, 41 videos, 11.3k subs, 6 videos over 150k).

Caution: views-to-subscribers ratios of 100x-500x are unusual and mean the audience watches without subscribing (search/suggested traffic). That helps views and ad revenue but makes the 1,000-subscriber YPP threshold slower than the view counts suggest. Some of these channels may be AI-produced at volume; I did not verify.

## Visual style of the small-channel winners (thumbnails)
- The dominant look is the creature/god line-up: a row of labelled characters in one flat, consistent art style ("Every Greek Monster and How It Died", "Half-Human Family", "Every Mythology in the World Explained" with icon portraits, Japanese yokai grid).
- Mix of simple flat cartoons (Hard Times in Hellas, Odrin, Cryptic Chronicles), stylised illustrated AI-looking art (Mythological Man, Mr L, MythLore Unpacked), and a few gory painterly thumbnails (Mr. Discovery).
- Explicit "stick-figure/animated" titled videos in the sample have a lower hit rate (16 videos, median 58k, none from small channels), but that keyword catches mostly gaming and fan animation, so it is not a clean read on our style.
- The line-up thumbnail and the "Every ___" structure are cheap for us to produce with our character kit.

## Other
- Engagement among 100k+ English videos: median like rate 1.5%, comments 0.08%.
- Non-English results were 12% of the raw pool.
- "[No AI]" titled videos from a big channel (3 in sample): median 8.9M views, so audience pushback on AI content is real.

## Updated recommendations
1. **Length:** spike at 10-12 minutes, first full videos at 10-15 minutes. Revisit 20+ min after we have retention data.
2. **Lead format:** "Every ___ Explained" catalogue (small-channel proven), with "myths that turned out to be true" as the high-ceiling second series, "who was" as occasional hook-angle videos.
3. **Mythology order to test:** Egyptian, Mesopotamian, Japanese, Norse first; Greek only with a distinct angle (villains' deaths, "before Zeus"); avoid Slavic and Aztec/Maya as a launch lane. Hindu mythology is untested.
4. **Thumbnail system:** labelled character line-ups in our own flat style, built from the character kit.
5. **Channel name and identity** should signal "every myth explained" breadth, not one mythology.
6. **Plan for slow subscribers:** budget extra time to 1,000 subs; build subscribe prompts into scripts and end screens; Shorts from each video.
7. **Differentiation is the risk,** since many near-identical "Every ___" channels exist; research depth, sourcing and a distinct voice are what we add.
