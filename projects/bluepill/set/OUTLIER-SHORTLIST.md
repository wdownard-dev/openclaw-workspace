# OUTLIER-SHORTLIST.md: Set (video 3), Stage 1 outlier check, 2026-11-18

Method: YouTube Data API, 9 searches (order=viewCount, videoDuration=medium i.e. 4-20 min, published in the last 365 days, 25 results, English relevance, US) plus 1 all-time search for "Set Seth Egyptian god" (any length, 25 results). Then videos.list and channels.list on 170 unique videos (155 channels). Kept: English-looking, 6-40 min. Script: `outlier_set.py`. Raw data: `outlier-data-set-2026-11-18.json`. **Quota used: 1,008 units (10 searches x 100 + 8 lookup calls).** No API errors.

Caveats: the "medium" bucket excludes 20-40 min videos. Each pool is only the top 25 by views per query, so a median here is a median of a thin tail, not market demand; compare characters to each other, not to the 2026-11-11 tables. Subscriber counts are current. "Pool" = all kept videos returned by that character's queries (Set had 4 queries, the others 1).

## Per character (365 days, English, 6-40 min)
| Character | Pool n | Median views | Top-5 median | Videos >=100k | Best small-channel outlier (<30k subs) | Verdict |
|---|---|---|---|---|---|---|
| Baba Yaga | 13 | 248 | 17k | 2 | Slavique, 27.1k subs, 140k views, 17 min, "Baba Yaga Is Older Than You Think: The True Story of the Slavic Witch" | Best single-character angle in the set: "true story" framing works at small scale. |
| Medusa | 18 | 995 | 353k | 5 | Mythological Man, 11.4k subs, 712k, 12 min, "Every Monster From Greek Mythology Explained in 12 Minutes" | Demand is real, but the winners are monster compilations and a gaming-adjacent video, not a Medusa-only story. |
| Circe | 12 | 192 | 49k | 2 | Fact vs Film, 11.8k subs, 242k, 12 min, "Every Monster in The Odyssey, Explained" | Circe rides inside Odyssey compilations; a solo Circe video has no hit. |
| Gilgamesh | 14 | 477 | 2.4k | 1 | none (the 412k hit is Jake Doubleyoo, 570k subs, a comedy retelling) | One big-channel hit, nothing for a small channel. |
| Set (4 queries) | 45 | 105 | 3.0k | 0 | none; best result 4,961 views (14 min "Top 10 Most Powerful Egyptian Gods", 123 subs) | No standalone Set video in the last year got past 5k views. |
| Cu Chulainn | 2 | 166 | 166 | 0 | none | Almost no long-form supply or demand in this window. |

## Ranking (this check only)
1. Baba Yaga. 2. Medusa (as part of a monster/villain compilation). 3. Circe (inside an Odyssey compilation). 4. Gilgamesh. 5. Set. 6. Cu Chulainn (too thin to rank).

## Does Set hold up as the pick? No.
Set as a single-character video fails the check. Across four Set phrasings, including the "Egyptian villain" and "Egyptian god of chaos" hooks, 45 English videos from the last year returned zero above 5k views. The two Set-specific results that did well are both on big channels and older: Esoterica "Who is Set - The Egyptian God of the Desert, Violence & Foreigners" (27 min, 1.17M-subscriber channel, 456k views, June 2024) and the Gods of Egypt film clips (1.7M-8.7M, Hollywood footage, not the myth). That says an audience exists for "who is Set" on an established channel, and says nothing about a 3.6k-subscriber channel. Our hook angle is the only thing that could rescue a single character (OUTLIER-CHECK.md), and no video in this pool tests it. Set can be picked on interest, not on this data. If the goal is views, the data points to Baba Yaga, or to Set inside an "Every Egyptian god / villain" frame (Egyptian mythology median 419k in the 2026-11-11 round 2 data).

## What already exists on Set (top English long-form, 4+ min, from the pool; all-time search plus the 365-day searches)
| # | Views | Channel (subs) | Title | Len | Angle |
|---|---|---|---|---|---|
| 1 | 6.81M | See U in History (2.36M) | Egyptian Mythology: The Essential - Ra, Horus, Osiris, Seth, Anubis, Bastet | 15.6 | Pantheon overview; Set is one of six. Not a Set video. |
| 2 | 1.69M | Boxoffice Movie Scenes (6.2M) | Horus VS Set / Final God Form / Gods of Egypt | 4.8 | Film clip. Not the myth. |
| 3 | 456k | ESOTERICA (1.17M) | Who is Set - The Egyptian God of the Desert, Violence & Foreigners | 27.2 | The one dedicated long-form hit. Covers desert, violence, foreigners: the "why" half of our angle, in a scholar-lecture style. |
| 4 | 4.8k | See U in History (2.36M) | Seth: The God of Chaos in Egyptian Mythology | 9.6 | Chaos-god explainer. |
| 5 | 890 | Pyratheon (1.9k) | Horus vs Set: The Full Story of Egypt's Throne | 12.2 | The Contendings retold. |
| 6 | 334 | Mythic Origins (162) | Egyptian Mythology Explained: Ra, Osiris, Horus, Seth, Anubis | 10.9 | Pantheon overview. |
| 7 | 275 | Beyond the Scrolls (778) | Why Did Egyptians Worship Set? The Dark Truth About the Chaos God | 7.5 | Closest to ours by title (the worship question), still a "dark truth" frame. |
| 8 | 83 | History Vault HD (147) | Set: The God of Chaos Who Murdered a King | 15.3 | Murder-first. |

Gaps in the pool: only four dedicated long-form Set videos exist in the sample, and the pool is capped at 25 per query, so the list is the top of what the searches surfaced, not a census. Angle read from titles only; no transcripts fetched. By title, none frames Set as a role reversal (murderer in the myth, guard of the sun-barque every night, pharaoh namesake), none ties his fall to the Hyksos and the Assyrian and Persian conquests, and none tells how the Osiris-murder details we all know come from a Greek writer. Esoterica is the only one that touches foreigners, and it is a lecture, not a story told straight.
