# ASSETS-REPORT.md: art generation for "The Cyclops Case File" (video 1), run of 2026-11-13

Scope: step 7 of FORMAT-BIBLE section 10, the list in `video2/ASSET-PLAN.md`, G2 decisions applied (Polyphemus master = cy_v4 cutout; CYC2 = one edit call off that master; Odysseus master = the accepted cutout; one Odysseus-only "under the ram" plate). Labels: [V] counted from files or `assets/SPEND.csv`; [E] estimate.

## 1. Headline

- **83 API calls, 82 returned an image, 1 aborted (a curl killed mid-request, no charge). Estimated spend $3.90 against the $10 hard cap** [V, `assets/SPEND.csv`, token-priced: 99,393 output tokens at $30/M = $2.98; 81,624 image-input tokens at $10/M = $0.82; 19,451 text tokens at $5/M = $0.10]. The plan's $6-9 was high because 1024x1024 sprites cost about $0.045-0.065 and 1536x864 props $0.029, and the first-attempt pass rate was 84%.
- **Accepted: 33 new sprite drawings, 26 props, 6 plates, 4 maps = 69 generated items, plus 3 reused masters cut, 2 code silhouettes, 3 code group sets, 17 alias copies, 3 sourced pictures, 1 rendered Greek line.** Rejected: 13 calls (12 sprite, 1 plate).
- Everything is under `video2/assets/`: `sprites/` (56 PNG + sidecar JSON + 6 `<char>.cast.json`), `props/` (26), `plates/` (6), `maps/` (6 files for 4 bases), `sourced/` (+ `SOURCES.md`), `rejects/` (+ `REJECTS.log`), `sheets/` (15 contact sheets), `gen/` (raw API outputs), `prompts/`, `SPEND.csv`.
- Not touched: `storyboard.json`, audio, anything in `video1/`. No uploads.

## 2. Counts by group [V]

| Group | Planned | Calls | Accepted | Rejected | Notes |
|---|---|---|---|---|---|
| Masters (no spend) | 3 | 0 | 3 | 0 | `polyphemus__neutral__a` cut from `cy_v4_flat`, `odysseus__neutral__a` from `odysseus_A_flat`, `odysseus__point__a` from the existing `ody_shout` cutout, `crew__neutral__a` cut from `crew_A` |
| New masters | 3 | 3 | 3 | 0 | `cyc2__neutral__a` (one edit off the Polyphemus master: grey cropped hair, short grey beard, apron, symmetric build, narrower eye), `empedocles__neutral__a`, `thucydides__neutral__a` (generations endpoint) |
| Odysseus poses | 12 | 12 | 12 | 0 | walk, talk, shrug, think, flat, smug, armscrossed, sworddraw, swordlower, offerbowl, tiptoe, lookup; chained master + previous pose |
| Polyphemus poses | 7 | 7 | 7 | 0 | wave, leandown, scorn, beam, tender, armswide, wounded |
| CYC2 poses | 5 | 5 | 5 | 0 | shrug, back, smith_hammer, smith_tongs, smith_flat |
| Crew poses | 5 | 14 | 5 | 9 | point, plead, torch failed three times each (model sheets, then full scenes); all 5 passed first time with the instruction-first prompt (section 5) |
| Thucydides pose | 1 | 4 | 1 | 3 | same failure and same fix |
| Props | 26 | 26 | 26 | 0 | all first attempt, 1536x864 generations, cut to alpha |
| Plates | 6 | 7 | 6 | 1 | NB_ram a1 had Odysseus beside the ram; a2 has him under the belly |
| Maps | 4 | 4 | 4 | 0 | |
| **Total** | | **83** (82 ok) | **69 generated + 3 reused** | **13** | |

Sprite counts against the bible: Odysseus 14 (target 14), Polyphemus 8 incl. code silhouette (8), crew 6 + 3 code groups, CYC2 6, new named 3. The storyboard's merged names (`odysseus__handsopen`, `__unamused`, `__smug_sideeye`, `__tired_helm`, `polyphemus__drunk`, `__lovesick`, `__shrug`, `__lamb_wave`, `crew__worried`, `__squint`, `__torch_wave`, `__magnifier`, `cyc2__smith_hat_tip`, `__trio_*`, `__smiths_trio_*`) exist as copies of the accepted pose they map to (listed in each `cast.json` under `aliases`); mirroring, tinting, the lamb, hat and magnifier props are renderer work as ASSET-PLAN says.

## 3. Checks done

- Every sprite viewed on a 3-ground tile (black, mid-grey, white) in `assets/checks/*_check.jpg`; the all-sprites sheet on grey (`sheets/11_all_sprites.jpg`) shows no fringes or white pockets. Flood-fill cutout with pocket clearing (`assets/cut.js`), 8 px pad, feet anchor and `height_px_at_1080` in each sidecar JSON.
- Immutable features held on every accepted pose [V, viewed]: Odysseus wreath, blue sash, beard 14 of 14; Polyphemus one eye, rope belt, nothing hanging, no bells 8 of 8; CYC2 one eye, apron, rope belt 6 of 6. Style: flat ink, same line weight and palette throughout; no text in any accepted image.
- Props: single object, clean closed outline, white ground, no text (the book cover is blank as asked; the stake is a charred pole, not a sword; the ram has horns).
- Plates: 1536x864, no text; NB_prayer is a silhouette only (no eye, no god); NB_forge has no figures and a clear floor band; NBG02_mouth has the bright empty arch on the right; board_base has four blank cards and a clear top strip; NB_ram has no giant.

## 4. Things William should eyeball (contact sheets)

1. `assets/sheets/11_all_sprites.jpg`: every sprite cutout on grey (56 cells). Also `02_round1_poses.jpg`, `04_round2_poses.jpg`, `05_round3_partial.jpg`, `05b_round3_rest.jpg`, `08_round4_poses.jpg`, `10_crew_v2.jpg` (raw outputs per batch) and `01_new_masters.jpg` (CYC2, Empedocles, Thucydides: do they read as different people from Polyphemus and Odysseus?).
2. `assets/sheets/09_plates_raw.jpg` and `12_groups_plates_final.jpg`: the 6 plates and the 3 code groups. Flags: **NB_prayer** has no visible ship on the water (the prompt asked for a tiny one; the renderer can drop the NP04 ship icon at about 60 px if wanted); **NBG06_day** redrew the island in daylight but the "clear shore band at the lower right" is open sea, so a sprite there would stand on water (place at left on the rocks, or keep 93b/94 as an inset); it also drifts from NBG06's layout (greener, different cone). **NB_ram** replaces the flagged `NB14_crop_left55` for beat 42a: the storyboard still points at the old file, so the build needs a one-line swap (not done here, storyboard untouched).
3. `assets/sheets/07_maps_raw.jpg`: **map_med** is a cartoon Mediterranean (Italy, Sicily, Greece, Aegean, Crete, Asia Minor present, coastlines approximate, as TOOLS.md already warned); **map_argolid** is generic coast with two squares and does not read as the Argolid (only used as board frame 3 at small size); map_sicily and map_world are good. All text-free, flat, slight paper grain.
4. `assets/sheets/06_props_cut.jpg`: 26 props on grey.
5. `assets/sheets/03_sourced.jpg`: the skull plate and cutout, the Homer bust (two-tone; heavy at small sizes, see SOURCES.md), the Greek line render.

## 5. Lessons for the bible (section 5.3)

- **Descriptive identity prompts for unnamed characters turn into model sheets or scenes.** With the frozen template, "Image 1 shows the character: a young ancient Greek sailor..." gave a turnaround sheet with text (3 of 3), then a ship-and-storm scene (3 of 3), then a sunset scene with the pose ignored (3 of 3); "Thucydides, a Greek historian" gave a model sheet 3 of 3. Odysseus, Polyphemus and CYC2 (named, with the locked identity paragraphs) passed 24 of 24 with the same template. The fix was an **instruction-first prompt** ("TASK: redraw the man in image 1 in a NEW POSE. Output ONE drawing ... on a plain pure white background with absolutely nothing else ... NEW POSE: ..."), which then passed 6 of 6 (`prompts_def.py: sprite_prompt_v2`). Recommend: use v2 for every sprite call from now on; it also needs only the master as ref.
- 1024x1024 medium costs about 1,449 output tokens ($0.045 before refs), **more** than 1536x864 (924 tokens, $0.028); props and plates are the cheap size, sprites the dear one. Each reference image adds about 1,088 input tokens ($0.011).
- Chained refs (master + previous accepted pose) held identity for 12 Odysseus poses in one session with no drift seen [V, sheet 11], so the "fourteen poses in one session" [U] in the bible can be marked tested.
- Background shells launched from a tool call were killed once mid-batch (one aborted call, logged as `api_error`, $0); the detached `background=true` mode of the exec tool was reliable. Every call, including the aborted one, has a row in `SPEND.csv`.

## 6. Sourcing (no spend), see `assets/sourced/SOURCES.md`

- **Skull:** Othenio Abel, *Die vorweltlichen Tiere in Märchen, Sage und Aberglauben* (1923), text figure 9, p. 35, front-view elephant skull engraving; Internet Archive scan `vorweltlichentier00` (Public Domain Mark; pre-1929 and author d. 1946). **The caption names no species** ("Elefantenschädel"), so the chip must say "elephant skull (Abel 1923)", not "Sicilian dwarf elephant". The brief's "Abel 1914 figure 5" was not found: both 1914 books carry the argument in prose only. The only *Palaeoloxodon falconeri* front views found are CC BY-SA museum photographs on Commons (not used).
- **Homer:** Baumeister 1885 engraving of the Capitoline bust (Commons `File:Homer.png`, public domain), flattened to two tones; an 1808 Leney engraving (Library of Congress, public domain) kept as an alternative.
- **Greek line:** Odyssey **9.394** ὣς τοῦ σίζ᾽ ὀφθαλμὸς ἐλαϊνέῳ περὶ μοχλῷ. (Perseus `tlg0012.tlg002.perseus-grc2`, Murray's 1919 Loeb Greek; CC BY-SA 4.0 digital text, credit Perseus). The storyboard id `greek_line_9_394` was right. Perseus has no separate Allen text for the Odyssey; the Allen OCT reading of this line is the same words [E]. Rendered in GFS Didot (OFL) as `greek_line_9_394.png`.

## 7. Uncovered or still open

1. Code-drawn icons and overlays (ring, eye_icon, oneeye_crossed, ship_crossed, ship_icon, height_line, person_silhouette, waterdrops, pin, bone_pin, book_icon, arrow_left, pointer, heart, flame_glow, dustpuff, source_slip_empty, X, board frame states, stamps, counters, chips): renderer work per ASSET-PLAN 3.2, not produced here.
2. `NP04_listing` (NP04 rotated 12 degrees) and `prop__boulder__a` (= `boulder3.png`): renderer copies from video1, not duplicated here.
3. The storyboard's `NB14_crop_left55.png` at beat 42a should become `NB_ram.png` (one-line change at build time).
4. The skull cutout `skull_front_pd_small.png` is a silhouette-masked engraving (white paper kept inside the outline); on dark grounds it reads as a white card with the drawing, which is how the script treats it.
5. Dashboard spend not checked (Cloudflare wall, as before); the $3.90 is token-priced and should be within about 10% of the usage page.

## 8. How to re-run

`assets/gen.py` (API, cap, log), `prompts_def.py` (all prompts), `mk_jobs.py` / `mk_jobs_lib.py` (job files), `chain.py` (one character's sequential poses; `VARIANT=2` selects the instruction-first prompt), `cut.js` (cutout + sidecar + 3-ground check), `sheet.js` (contact sheets), `build_cast.py` (cast.json, aliases, silhouettes), `groups.js` (crew groups), `sourced/render_greek.js`.
