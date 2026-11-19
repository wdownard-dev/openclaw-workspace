# BRIEF-LIBRARY: Norse picture library, one round (images; real spend, hard cap $6.50)

Worker: Sonnet (this run is itself the worker; do not spawn others). Context cap 100k: view contact sheets, never every image. No messages to anyone except your final reply. Do not read session history. Write only inside `projects/bluepill/norse/library/`. Never modify the Greek `projects/bluepill/library/` (read-only reference).

## Read first (in this order)
1. `norse/library/WARDROBE.md` INCLUDING the last section "WILLIAM'S DECISIONS" (binding; supersedes the tables above it: black eye patch on Odin, `odin_armed`, Hod's diagonal white face bandage like a bandaged-eye cartoon (NOT a blindfold), colour changes).
2. `PROCESS.md` Stage 3 (library, simplified card spec) and rule 21 (card id per character per beat).
3. `library/characters/odysseus/CHARACTER.md` and `video2/tests/stickfig/prompts/STYLE.txt` (the style block appended to every prompt) and `library/AUDIT-LOCK.md` (checks A-F pattern).
4. `norse/library/gen.py` (copy of the Greek generator: `gen.py run|edit|batch`, logs every call in `norse/library/SPEND.csv`). Set `CAP = 6.50` at the top. `OPENAI_API_KEY` is in the environment. On a STOP file or the cap, stop and report.

## Method (video 1 lessons are rules)
- Same look as the Greek library: round cream face, dot eyes, thick dark ink outline, flat warm shading, plain flat cream background, no scenery, no text. The Odysseus turnaround (`library/refs/odysseus__turnaround.png`) may be passed as a STYLE-ONLY reference ("match only the drawing style, line weight and shading; change the character entirely"). Test this on Odin first (step A); if the model copies Odysseus's face or clothes, drop the reference and use the style block only.
- ONE round: build every prompt from the identity line in WARDROBE.md (pasted verbatim) plus the style block. No options, no unused variants.
- Step A (test, about $0.30): `odin_one_eye` FULL card turnaround. View it. Check: black eye patch clear at small size, wide hat, long grey beard, dark blue cloak, one dot eye. If it fails, adjust the prompt once and re-run once. Report what you changed.
- Step B: all other FULL cards (turnaround: front + three-quarter on one cream strip, feet on one baseline; plus one face close-up), then SIMPLE cards (single front image). Derived variant cards (tyr_stump from tyr_hand, thor_disguise from thor, odin_armed from odin_one_eye, fenrir stages, loki forms, ymir_dead, baldr_dead) are made by EDIT from the base card ("edit image 1, change only ..."), never regenerated.
- Step C: place masters (17), 1536x1024, one master each, then every derived variant by edit; "crop" variants are free (Pillow crops from the master, no model call). Verify each derived edit against its master with an edge-correlation check (0.6-0.75 is a pass; pixel diff is useless under lighting change; reuse `library/derive.py` logic if helpful). Props: only the 5 prop masters in the table; all other props are prompt text.
- Step D: compose one labelled CARD per character per the simplified spec in PROCESS.md Stage 3 step 6 (title, ONE identity line of at most 5-6 bold tells, front + three-quarter turnaround, one face close-up; SIMPLE = single front; scale note on every animal and prop) into `norse/library/refs/<card_id>__card.png`. Use `library/compose.py` as the pattern (Pillow).
- Step E: `cast_check.py` pattern: every `state:` card name and place in `norse/SCRIPT-N-LOCKED.md` must map to a card id or place master. Write `norse/library/CAST-CHECK.md`; 0 MISSING is the bar. Also write `norse/library/cards.json`: `{state_name: card_id}` for every variant name that appears in `state:` lines (rule 21).
- Step F: audit A-F style to `norse/library/AUDIT-LOCK.md`: one-eye/patch consistency across every Odin image, Tyr hand vs stump, Hod band, Heimdall horn, Hel split, colour clashes from the pairwise table, variants match their masters. Mark non-canonical images NOT USED. Fix blockers with at most ONE re-roll round (cap-aware).
- Do NOT write `LOCKED.md`. William locks after review.

## Review artefacts for William (cheap to read)
- `norse/library/CONTACT-CHARACTERS.jpg` (every card, labelled, about 4 columns, 2400 px wide) and `CONTACT-PLACES.jpg` (every master with its variants beside it). View these two yourself for the audit instead of opening images one by one.
- `norse/library/REPORT.md`: spend by step vs the estimate ($4.80), re-rolls, anything that does not meet the identity line, the first things William should look at (Odin's patch, Hod's band, Tyr stump, Heimdall, Hel).

## Final message (max 10 lines)
Files, number of cards/places/variants generated, total spend from SPEND.csv, CAST-CHECK result (MISSING count), AUDIT blockers remaining, and open questions. Nothing else.
