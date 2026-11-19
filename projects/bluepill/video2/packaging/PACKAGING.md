# PACKAGING: "The Cyclops" (The Myth Ledger, video 2)
Nothing uploaded or sent. Library untouched. Image spend: 3 Gemini 3.1 Flash calls, about 1,120 output image tokens each (about $0.20 at list price, well under the $1.50 cap); no rerolls.

## 1. Titles (all under 60 chars)
1. **The ENTIRE Story of the Cyclops in 10 Minutes** (45) — reference idiom ("The ENTIRE History of X in N Minutes"). Runtime is 9:28 of voice, so "10 Minutes" is honest.
2. Where Did the Cyclops Actually Come From? (41) — question form; mirrors the script's own hook.
3. The Cyclops, the Stake and a Man Named Nobody (46) — curiosity form; names the twist without spoiling the escape.
4. 6 Men Entered the Cave. The Giant Ate 6. (41) — number form (script: twelve go in, six never come out).
5. Why Odysseus Told the Cyclops His Name Was Nobody (49) — "Why X..." form, like "Why Romans Never Used Archers".

**Pick: #1** for the channel's first long-form: it is the proven idiom (the 974k Japan reference), says what the video is, and searches well. Use #3 or #5 as the A/B test title if YouTube's Test & Compare is available.

## 2. Thumbnails (1280x720, Gemini 3.1 Flash image, library cards + place plates as refs; text by Pillow, Permanent Marker)
Files: `thumb_A.jpg`, `thumb_B.jpg`, `thumb_C.jpg`, 3-up `thumbs_3up.jpg`; model outputs without text in `raw/`; generator `gen_thumbs.py`, text pass `text_thumbs.py`.
- **A, "NOBODY"**: Polyphemus's one huge firelit eye, tiny beardless Odysseus with the stake. Single figure, one eye, one word; reads at phone size. On-model (Polyphemus, Odysseus beardless, firelit cave). Minor: the "Y" brushes the giant's hair.
- **B, "THE ESCAPE"**: Odysseus clinging under the ram, giant's hand on its back. Good story beat, but Odysseus's pose is awkward/lays across the belly and the subject is smaller; weakest at thumbnail size.
- **C, "THE REAL CYCLOPS?"**: elephant skull beside the giant's face. Strongest curiosity gap, but busy: model added extra stick figures, ships, sheep, and the giant's hair came out red (off-model). Text covers the lower middle. Would need a reroll or a Pillow crop to use.

**Pick: A.** One eye, one word, one tiny hero; highest contrast, and "NOBODY" pays off the ending. C is the best second candidate (or a swap after launch).

## 3. Description (paste-ready)
```
Twelve men follow Odysseus into a cave, and six of them never come out. The giant who owns it seals the door with a stone twenty-two wagons could not move. Odysseus's only weapon is a sharpened stake, a skin of wine, and a name: Nobody.

And then the real question: where did the Cyclops come from? The poet who gave us the giant, the fossil that may have inspired him, and what nobody can actually prove.

Chapters:
00:00 The cave
00:36 The Cave
02:08 The Meals
03:26 Nobody
05:11 The Rams
06:20 The Curse
07:49 Where Did He Come From?

Sources:
- Homer, The Odyssey, Book 9 (Samuel Butler translation, Project Gutenberg #1727)
- Hesiod, Theogony (the Cyclopes with one eye)
- Othenio Abel, 1914 elephant-skull hypothesis, as reported and assessed by Jason Colavito
- Pausanias, Description of Greece, 2.25.8 (the walls of Tiryns)
- Oskar Hackman, 1904, on the one-eyed-giant folktale type
- Adrienne Mayor, on fossils and the Cyclops: "we just can't prove that"

Dialogue and Homer's wording are condensed and paraphrased for the video; check the sources above for the originals.

The Myth Ledger: one myth, told straight, with the sources on the table.
```
Notes: the first two lines (before "And then the real question") are the fold; they work on their own. No links included because none were verified; add the Gutenberg URL (https://www.gutenberg.org/ebooks/1727) if wanted, since FACTCHECK-V5 read it directly. Cold open is "The cave" at 00:00 to avoid duplicating the next chapter name; rename to "Intro" if preferred. Hackman's title and the Mayor book title were not verified in the factcheck, so they are named by author only.

## 4. Tags (18)
cyclops, polyphemus, odyssey, odysseus, homer, greek mythology, greek myths, mythology explained, nobody odysseus, cyclops origin, elephant skull cyclops, myth history, ancient greece, the odyssey explained, hesiod, myth vs history, animated mythology, the myth ledger

## 5. YouTube chapters (00:00 first; from `audio-v5/beats_timing.json` first-beat starts of each passage)
```
00:00 The cave
00:36 The Cave
02:08 The Meals
03:26 Nobody
05:11 The Rams
06:20 The Curse
07:49 Where Did He Come From?
```
Caveat: these are voice-track times. SCRIPT-V5's header lists later times (0:36, 2:20, 3:48, 5:45, 7:06, 8:49) because it assumed pauses and chapter cards; the rendered edit's real times (about 10:15 total) will drift later by 12-60 s. **Re-time against the final render before publishing.**
