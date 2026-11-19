# REPORT: Norse picture library, one round

Not locked. `LOCKED.md` not written (William locks after review).

## Spend (SPEND.csv, cap $6.50): $5.49 total, 118 successful image calls, 2 safety rejections ($0)
| Step | USD | Notes |
|---|---|---|
| A: Odin test (with and without style ref) | 0.09 | ref copied Odysseus; dropped |
| B: 12 FULL turnarounds | 0.43 | |
| B: 14 SIMPLE cards | 0.62 | |
| B: 12 face close-ups (incl. re-rolls) | 0.90 | faces use the turnaround as a ref (costlier) |
| B: 12 derived character cards + 3 re-derives | 0.75 | |
| C: 17 place masters + 5 props (+2 re-rolls) | 0.85 | |
| C: 27 place variants (+8 re-derives) | 1.83 | 8 crops free |
| Re-rolls (Thor x2, Hod, Baldr dead, Ymir dead, Thor disguise, boat, sea, 3 variants, 5 sea variants) | about 1.0 (inside the lines above) | one re-roll round |
Estimate was $4.80; actual $5.49.

## Counts
38 character cards (26 base + 12 derived, incl. `odin_armed`, `thor_disguise`), 5 prop cards, 17 place masters, 35 place variants (8 crops, 27 edits), 5 prop masters. Cards: `refs/<id>__card.png`. `cards.json` (54 state names + 3 explicit variant names) and `cards_beat_overrides.json`.

## What does not fully meet the identity lines
- Odin: the hat has a wide brim but a pointed crown (wizard-ish).
- Thor and Hod: red tunics added under the cloaks by the model (Hod red tunic, also Vidar and Heimdall). Not in the lines.
- `ymir_dead`: only partially clean (see AUDIT-LOCK).
- `tyr_stump`: the bandage is small.
- Thor's first prompt was refused by the image safety filter; "grey stone mallet" is the working wording (the card line still says hammer).

## Look at these first
1. Odin's patch (card `odin_one_eye`, `odin_armed`).
2. Hod's diagonal band (`hod`).
3. Tyr hand vs stump next to Odin and Thor.
4. Heimdall (horn) and Hel (split face).
5. Thor vs `thor_disguise`.

## Script gaps (rule 21)
Script `state:` lines say "Thor" for the disguise beats (N-081 to N-100), "Odin (one eye)" for N-144-146 and "Fenrir (bound)" for the sword beats (N-078-079). They need to be patched to name `Thor (disguise)`, `Odin (armed)`, `Fenrir (bound, sword)`, or the plate builder must use `cards_beat_overrides.json`.

## Files
CONTACT-CHARACTERS.jpg, CONTACT-PLACES.jpg, CAST-CHECK.md, AUDIT-LOCK.md, cards.json, edge_checks.json, SPEND.csv.
