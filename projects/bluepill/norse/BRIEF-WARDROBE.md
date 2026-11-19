# BRIEF-WARDROBE: Norse library step 1 (text only, no images, no spend)

Worker: Sonnet. Context cap 100k. No images, no audio, no spend, no messages. Do not read session history. Write only inside `projects/bluepill/norse/library/` (create it). Do not touch the Greek `library/`.

## Why
William approved skipping the wardrobe option sheets ONLY IF we get each wardrobe right the first time: every character must be instantly recognisable as the character they are meant to be (their traditional iconography), in OUR stick-figure style (round cream face, dot eyes, thick ink outline, flat warm shading; see `projects/bluepill/library/characters/odysseus/CHARACTER.md`, `CHARACTER-STYLE-REF.md`, and `video2/tests/stickfig/prompts/STYLE.txt`). This text pass is the checkpoint William will read before any image is generated.

## Read
- `norse/SCRIPT-N-LOCKED.md` (locked script; `state:` lines name who is present, with variants such as "Odin (one eye)", "Tyr (hand)", "Tyr (stump)")
- `norse/SCRIPT-N-NOTES.md` (cast list with draft identities, new places, new props, scale line)
- `PROCESS.md` Stage 3 (library steps; simplified card spec) and rule 21 (variant cards, exact card id per beat)
- `VOICE.md` only if you need tone; not needed for this task
- One example of a finished card for format: `library/refs/` (any `*__card*` or turnaround png is fine to just list; do not view images unless needed) and `library/characters/odysseus/CHARACTER.md`

## Deliver `norse/library/WARDROBE.md`
1. **Card table (27 cards).** Cast = the 28 of the notes with these changes: Tyr is TWO cards (`tyr_hand`, `tyr_stump`); Thor has a disguise card derived by edit from Thor (`thor_disguise`); Heimdall, Garm, Modi+Magni (one card, two boys), and the scribe get simple single-image cards; dwarf, Ask+Embla (also Lif+Lifthrasir), giantess (also Thokk), Yggdrasil animals (eagle, Nidhogg, Ratatosk on ONE shared card) are simple single-image cards; Vili+Ve one card. Odin is ONE-EYED in every beat (`odin_one_eye`), no two-eyed Odin. For each card give:
   - stable `card_id` (snake_case, used later in `state.json`),
   - card tier: FULL (front + three-quarter turnaround, one face close-up) or SIMPLE (single front image),
   - **traditional iconography** that makes the character recognisable (what the sources and standard depictions agree on), with a source locator for anything from the Eddas (Gylfaginning chapter, Grimnismal/Voluspa stanza; Bellows 1923 and Brodeur 1916 are the texts we use; sacred-texts.com is blocked from this host, use archive.org or Gutenberg),
   - the final **identity line** (at most 5-6 bold tells that survive a wide shot, written ready to paste into a prompt, including clothing colours, one signature prop, silhouette note),
   - scale (Odin 1.0 as the human reference; per the notes: dwarfs 0.5, giants 3.0-4.0, Fenrir cub/growing/grown, etc.),
   - beats the character appears in (ids from the locked script) so priority is visible.
   Iconography must include at least: Odin (one eye, wide-brimmed hat, long beard, cloak; spear Gungnir only if a beat needs it), Thor (hammer Mjolnir, red beard, belt/gauntlets only if bold enough), Loki (distinct from Thor/Odin at a glance), Tyr (single-handed war-god look: shield or sword, plain), Heimdall (horn Gjallarhorn, bright white), Hel (half black, half white), Baldr (radiant), Frigg, Hod (blind), Sigyn (bowl), Vidar (iron shoe), Surt (flame sword), Garm (hound), Fenrir and Jormungandr (scale and silhouette), Snorri (13th-century Icelandic chieftain, quill). Explain in one line each why a stranger would recognise them. Where traditional iconography is too fine for a stick figure (beard braids, runes), say what simplification keeps the recognition.
   - Check pairwise confusion: no two characters share silhouette + colour (flag any pair that would confuse in a wide shot, and fix by colour or silhouette).
2. **Places table.** Merge the 45 distinct `state:` locations in the locked script into about 18 MASTER places (one master each; every variant derived by edit: time of day, door state, etc.). List each master, its variants, the beats each serves, and the locations it absorbs. Include scale/lighting notes. No new place for a single beat unless unavoidable (say why).
3. **Props table.** From the notes' 16 props, keep only the ones a beat actually shows; give each a master or "no card, prompt text only" with a one-line reason. Scale note on every animal and prop (Mjolnir, Gleipnir ribbon, boat, Mimir's well, etc.).
4. **Variant ledger.** Every variant (odin_one_eye only, tyr_hand to tyr_stump at N-078, fenrir stages, thor_disguise, hel child, etc.) with the beat id where it changes, so rule 21 can be applied mechanically.
5. **Risks.** What could still read wrong at 540p; what William should look at first.
6. A short **cost estimate** for the image step: number of card images, place masters, derived variants, and dollars at about $0.04 per OpenAI image (gpt-image-2.6), with a 20% re-roll allowance.

## Output
Final message (max 12 lines): files written, counts (cards, places, props, variants), any pair of characters you changed to avoid confusion, estimated image spend, and open questions for William.
