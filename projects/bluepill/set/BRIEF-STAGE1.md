# BRIEF: Set (video 3), Stage 1 for The Myth Ledger

Worker: Sonnet, cap 100k context. Do NOT read session history. Everything you need is in files.

## Topic and angle (William approved topic 2026-11-18; Gate 1 still open for the angle and hook)
Set, Egyptian god of storm, desert and foreigners. Angle: "The villain was a promotion gone wrong." Tell the Osiris murder straight (cold open), then turn: the same god guards Ra's sun-barque every night and spears Apophis, pharaohs name themselves after him (Seti I, Seti II), the Contendings of Horus and Set ends with Set reconciled as thunder god beside Ra. Then the why: Set is god of foreigners and the desert, the Hyksos worshipped him, and under later conquest (Assyrians, Persians) the god of outsiders became the enemy; his name was chiselled from monuments. Close: the villain was built over centuries, partly by politics.
Format model: the Cyclops video ("told straight, then where it came from").

## STANCE RULE (William, 2026-11-18, binding)
Take definitive stances. Do not write "but older texts say otherwise", "scholars disagree", "some say". When two sources conflict, pick the version that tells the better story and state it flatly, with its source named. Record in the research file which version you picked and why, so the fact-check stage can verify it, but the narration-facing material (hooks, spine) contains no hedging.

## Guardrails
Public-domain sources only (Pyramid Texts, Coffin Texts, Book of the Dead, Contendings of Horus and Set / Chester Beatty I, Plutarch Isis and Osiris, Papyrus Jumilhac if useful). Cite the source tradition per claim. Stylised violence. No living people. Distinct research and twist from videos 1 and 2.

## Files to read (and nothing else)
- `../PROCESS.md` Stage 1 only (lines 29-36) and the model rule at the top
- `../OUTLIER-CHECK.md` (existing numbers; Egyptian gods explained median 547k, "who was" singles weak, hook angle is what saves a single character)
- `../outlier_search2.py` (reuse as a template; YouTube Data API key is in env YOUTUBE_API_KEY)
- `../refs/RECIPE-2026-11-13.md` sections 4, 6, 7 (hook and format recipe)
- `../norse/` titles only (`ls`), to see what hooks videos 1 and 2 used

## Tasks
1. Outlier check on the shortlist, using the script as a template. Queries: Set / Seth Egyptian god, Seth vs Horus, Egyptian god of chaos, "Egyptian villain", Medusa, Circe, Gilgamesh, Baba Yaga, Cu Chulainn (hook-style phrasings such as "the real story of ...", "explained"). English, last 365 days, 6-40 min. Budget about 1,000 quota units; stop if the API errors. Write `OUTLIER-SHORTLIST.md`: per character, median views, count of 100k+, best small-channel outlier, and a one-line verdict. Include a final ranking and say flatly whether Set holds up as the pick. Save raw data as JSON next to it.
2. Find what already exists on Set: top 8 English videos by views, with title, channel, subs, views, length. Note which angle each takes and what none of them cover. Do not fetch transcripts unless it is cheap.
3. Source pull for the spine: from your knowledge of the primary texts, list the 10-14 load-bearing facts of the angle (each with source and passage reference), choosing the dramatic version wherever sources conflict (see STANCE RULE). Write `SPINE.md`: a numbered beat list from cold open to close, one line per beat, with source per beat. No hedge language.
4. Hook lab: 8 distinct hooks for the first 15 seconds, each 2-3 sentences of spoken narration in the channel voice (read `../VOICE.md`), each a different mechanism (question, contradiction, stat, scene, reversal, etc.). Mark your top 2 and why. Write `HOOKS.md`.
5. Title and thumbnail concepts: 6 titles, 3 thumbnail ideas, in `PACKAGING-IDEAS.md`. Put your pick first.

## Output
Files in `projects/bluepill/set/` : OUTLIER-SHORTLIST.md, SPINE.md, HOOKS.md, PACKAGING-IDEAS.md, plus data JSON. Then your final message to the parent: under 250 words, the verdict on Set, your top 2 hooks verbatim, the top title, any API errors, and quota units used. Do not message anyone else.

## Verification
Re-read each output file once for hedge phrases ("some say", "scholars", "however older texts") and remove them from narration-facing material. Confirm the JSON data file exists and the quota figure you report matches the calls made.
