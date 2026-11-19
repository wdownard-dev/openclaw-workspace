# BRIEF-WARDROBE: Baba Yaga library step 1 (text only, no images, no spend)

Worker: Sonnet. Context cap 100k. No images generated, no audio, no spend, no messages. Do not read session history. Write only inside `projects/bluepill/babayaga/library/` (create it). Never touch `projects/bluepill/library/` (Greek) or `projects/bluepill/norse/library/` (read-only references).

## Why
William's rule (Norse precedent): we skip wardrobe option sheets only if each wardrobe is right the first time. Every character must be instantly recognisable as who they are meant to be (traditional Slavic folklore iconography as the Wheeler/Ralston/Afanasyev tellings give it), drawn in OUR stick-figure style (round cream face, dot eyes, thick ink outline, flat warm shading; see `projects/bluepill/library/characters/odysseus/CHARACTER.md`, `CHARACTER-STYLE-REF.md`, `video2/tests/stickfig/prompts/STYLE.txt`). This text pass is the checkpoint William reads before any image is generated. Gate 2 (script read) is cleared: William said "length is fine, let's work on the picture library" on 11/18, so draft 2 is the working script.

## Read
- `babayaga/SCRIPT-B-draft2.md` (the script; `state:` lines name who is present and where; `shot:` lines name props and places). The cast and place list is built from these, not from the older `CAST.md`.
- `babayaga/CAST.md` (earlier cast sketch; it is stale in places: it lists Vasilisa as eight, but the hook now says "a young girl" and the body shows her at eight at the deathbed and of marrying age at the errand; it assumes more cards than the script uses; use it only as a starting list)
- `babayaga/SCRIPT-B-NOTES.md` (chapter table, source choices, cut list)
- `PROCESS.md` Stage 3 (library steps; simplified card spec) and rule 21 (variant cards, exact card id per beat)
- `norse/library/WARDROBE.md` as the FORMAT precedent (card table with card_id, tier, iconography with locators, identity line, scale, beats; places table; props table; variant ledger; risks; cost estimate; William's decisions section is left empty for him). Copy the structure, not the content.
- `babayaga/REF-SLAVIQUE.md` only to see what the competing video looks like; we differ in packaging and look.

## Deliver `babayaga/library/WARDROBE.md`
1. **Card table.** Derive the cast from the script's `state:` lines (every distinct figure or group that appears in any beat). Expected set, adjust to what the script actually shows: Baba Yaga (mortar, broom, iron-toothed, bone leg: decide which tells are bold enough), Vasilisa (and whether the deathbed child and the errand-age girl need two cards: rule 21; state which beats use which; prefer ONE card if the script's own header says one Vasilisa card in every beat), the doll, the dying mother, the merchant father if he appears, the stepmother, the two stepsisters (must read as two, not clones), the three riders (white, red, black, each with horse; must stay separate cards so colour cannot drift), the three pairs of hands, the tale 2 cast the script uses (girl, stepmother or aunt if they appear, the cat, the dog(s), the gate, the birch, the maid), and any crowd or group the script shows. SIMPLE tier (single front image) for anything with one or two beats. For each card give:
   - stable `card_id` (snake_case, used later in `state.json`),
   - tier FULL (front + three-quarter turnaround + one face close-up) or SIMPLE,
   - traditional iconography with source locator (Wheeler 1912 "Wassilissa the Beautiful", Ralston 1873 "The Baba Yaga" and "Vasilissa the Fair", Afanasyev no.103/104 as the script's `trace:` lines already cite them; reuse those locators, mark `(verify)` where unsure),
   - the final identity line (at most 5-6 bold tells that survive a wide shot, ready to paste into a prompt, with clothing colours, one signature prop, silhouette note),
   - scale (Vasilisa 1.0 as the human reference; Baba Yaga about 1.15 plus the mortar; hut, gate and skull sizes by the script's shot lines),
   - the beats she/he/it appears in (ids from the script) so priority is visible.
   - Colour rule from the script header: palette night blue-black, ember orange (skull lamp and candle are the only warm light), bone cream; white, red and black are RESERVED for the three riders. So no other character wears pure white, red or black. The doll's red dress in the old CAST.md breaks this: resolve it (state the conflict and propose a fix, e.g. a rust or ochre dress). Same for the stepmother's red dress.
   - Pairwise confusion check: no two characters share silhouette + colour (stepmother vs sisters vs Baba Yaga in a dark wide shot; the three riders at night; Vasilisa vs the tale 2 girl). Flag and fix.
2. **Places table.** Merge the script's `state:` locations into the fewest MASTER places (one master each; every variant derived by edit: time of day, gate open or shut, skulls lit or dark, ash mounds present or absent, etc.). The script header names some derived states (hut gate shut/open; best room with/without ash mounds): honour them. List each master, its variants, the beats each serves and the locations it absorbs. No new place for a single beat unless unavoidable (say why). Scale and lighting notes (fence skulls glow cold pale white, never orange; ember orange is only the lamp and candle).
3. **Props table.** Keep only props a beat shows. Give each a master or "no card, prompt text only" with a one-line reason. Hero props needing masters: the skull lamp (ember eyes), the gate of legs/arms/toothed mouth if it is a prop rather than a place, the hut on fowl's legs if it is a place master, the mortar and broom if they are not part of Baba Yaga's card. Scale note on every animal and prop.
4. **Variant ledger.** Every variant with the beat id where it changes (skull states, hut gate states, best-room ash states, candle lit/snuffed, any figure change), so rule 21 can be applied mechanically.
5. **Risks.** What could still read wrong at 540p, and what William should look at first (Baba Yaga's bone leg, the skull lamp, the three riders at night, the sisters as two).
6. **Cost estimate** for the image step: card images, place masters, derived variants, dollars at about $0.04 per OpenAI gpt-image-2.6 image with a 20% re-roll allowance. Target about $4 for the whole round (PROCESS Stage 3), say so if the count pushes past that and what to cut.
7. Leave a final section **"WILLIAM'S DECISIONS"** empty (heading only).

## Output
Final message (max 12 lines): file written, counts (cards, places, props, variants), any colour conflict or character pair you changed, estimated image spend, open questions for William. Nothing else.
