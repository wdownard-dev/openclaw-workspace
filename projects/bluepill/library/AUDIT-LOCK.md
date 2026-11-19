# AUDIT-LOCK - library contradiction audit

Scope: all characters, places, props at full resolution (labelled strips in _work/aud/), .md, manifests, refs/, CAST-CHECK, SCRIPT-V5 shot lines.

## Pass/fail

| Check | Result | Note |
|---|---|---|
| A1 Odysseus: laurel not helmet; turnaround/face/expr/wardrobe agree | PASS | blue tunic, gold belt, meander, red cloak, sword, laurel in all |
| A2 Odysseus helmet variant non-canonical in manifest | PASS after fix (B2) |  |
| A3 Polyphemus exactly one eye in turnaround/face/expressions | PASS |  |
| A4 Polyphemus_blinded: band in every image; scarred hollow non-canonical | PASS | also silhouette has no eye |
| A5 Neighbour giants one eye each | PASS | all 12 expression heads + turnaround |
| A6 Crew/sailor/workers/bard/hesiod/abel/pausanias/hackman/maron/ram/sheep internal agreement with .md | PASS with minors M2,M3,M9,M10 |  |
| B1 Crew/sailor/workers shared skin + ink style | PASS after fix (B1) | workers cream matches crew A |
| B2 Polyphemus larger than neighbours | PASS (text only) | M6: no numeric scale |
| B3 Maron/bard/Hesiod/Abel/Pausanias/Hackman distinct | PASS (M7 closest pair) |  |
| C1 Cave exterior variants same scene (boulder, tree, mouth) | PASS |  |
| C2 Cave interior variants same scene (racks, pens, fire pit) | PASS |  |
| C3 Boulder prop = exterior boulder; sealed exterior = interior sealed boulder side | PASS | left outside <-> right inside consistent |
| C4 Sheep in cave = sheep sheet | MINOR FAIL (M5) |  |
| C5 Ship identical across prop/furled/beached/sea/night/dusk/deck | PASS | vertical blue/cream stripes, 7 oar holes, prow eye, meander band, teal hull |
| C6 Tiryns wall = Lion Gate = sunset | PASS |  |
| C7 Hillside dusk/dawn same hills | PASS |  |
| C8 Three hilltops: caves visible, no figures | PASS |  |
| D Props vs script: stake raw/sharp/fire, skull one hole no sockets, map no text, wine goatskin+bowl, torch, ox-cart | PASS (M8, M11) |  |
| E1 refs/ == canonical manifest PNGs, none stale, md5 match | PASS | 79 refs; helmet kept as documented variant |
| E2 CAST-CHECK folders/paths exist | PASS |  |
| E3 .md text matches images | PASS after fixes (B3,M1-M3) |  |
| F Script vs library | see script lines |  |

## Contradictions

| ID | Severity | File | What | Status |
|---|---|---|---|---|
| B1 | blocker | characters/crewman/turnaround_b.png, turnaround_c.png | Crew B/C were generated text-only: heavy painterly body, cast shadows, thick limbs vs crew A thin ink stick-style (not one ink style/costume tone). | FIXED: regenerated both from crew A as image ref (prompts/crewman_b_turn_v4.txt, _c_), old copies in _superseded/crew_bc_v3/, refs/ + crewman/sheet.jpg refreshed; verified side by side. |
| B2 | blocker | characters/odysseus/manifest.json (+build_library.py) | turnaround_helmet.png was canonical:true; required non-canonical. | FIXED: canonical:false, variant:true, note 'helmet beats only (329,448,551,588)'; README, CHARACTER.md, CAST-CHECK updated; file still copied to refs/ because script needs it. |
| B3 | blocker | places/cave_exterior/PLACE.md | Text said boulder is 'beside the mouth on the right'; every image shows it to the LEFT of the mouth (consistent with interior, where it rolls aside to the right when viewed from inside). | FIXED: PLACE.md + build_library.py text corrected. |
| M1 | minor | CAST-CHECK.md / cast_check.py | Crew listed as 'grey tunics'; images and CHARACTER.md are grey-brown/khaki-brown. | FIXED: now 'brown tunics'. |
| M2 | minor | characters/maron/CHARACTER.md | Said 'short wooden staff' and omitted the gold sun brooch; images show a head-height staff and brooch. | FIXED text. |
| M3 | minor | characters/polyphemus/CHARACTER.md | 'teal and ochre patches': images show teal patches with ochre stitching only; wardrobe.png also shows a rope belt the text omits. | FIXED patch wording; rope belt in wardrobe.png not in text (left). |
| M4 | minor | places/cliff_notched_peak/ | Stale empty folder. | FIXED: removed. |
| M5 | minor | places/cave_interior/* | Sheep in the cave pens have pale cream faces; characters/sheep sheet has dark grey-brown faces with dark ears. | OPEN: keep sheep sheet for outdoor shots; cave pens only background, faces tiny. |
| M6 | minor | characters/neighbour_cyclops (turnaround, face) | Painterly textured shading and ground shadow vs Polyphemus flat style. No numeric heights in any .md; 'smaller than Polyphemus' is only stated, not drawn on a shared scale. | OPEN: add relative-size note in shot prompts (Polyphemus ~1.25-1.3x neighbours). |
| M7 | minor | characters/hesiod vs pausanias | Both wide-brim straw/ochre sun hat + staff. Distinct by shape (flat brim vs domed petasos), tunic (brown fleece vs ochre + cloak + satchel) and colour (tan vs golden), but closest pair. | OPEN: acceptable; in shots keep Pausanias's satchel/cloak and Hesiod's scroll visible. |
| M8 | minor | characters/workers/turnaround.png vs props/ox_cart.png | Workers haul the block on a log-roller sledge, not an ox-cart; props/ox_cart is a separate two-ox cart. Nothing contradicts the script (ox-carts only in beats 28,143). | OPEN: do not describe worker scene as an ox-cart. |
| M9 | minor | expressions.png of bard, hesiod, pausanias, hackman | CHARACTER.md says 'expression heads'; these sheets show small full-body figures (hackman/pausanias) or figures (bard, hesiod). | OPEN. |
| M10 | minor | odysseus / crew expressions.png | Hair reads reddish-orange in expression heads vs brown in turnarounds. | OPEN. |
| M11 | minor | props/stake_fire.png | Fire-hardened state is a red tip + char, not glowing the whole stake; script 353 glows the stake in coals (shot handled by compositing). | OPEN. |

## Fixes logged
- B1: crewman turnaround_b/_c regenerated with crew A as ref (2 calls, $0.1025 total; SPEND.csv ids crewman_b_v4, crewman_c_v4). Verified visually, installed, refs and sheet.jpg refreshed.
- B2/B3/M1-M4: manifest + text edits (build_library.py, stage_v3.py, chars_new.py, docs.py, cast_check.py patched so rebuilds keep them).

## Script lines to change (SCRIPT-V5.md, not edited)

| Line | Current | Proposed |
|---|---|---|
| 16 | twelve tiny grey-tunic crew | twelve tiny brown-tunic crew |
| 20 | six grey figures walking out | six faded/grey-toned figures (intentional tint) or six brown-tunic crew |
| 242 | eight grey crew | eight brown-tunic crew |
| 278 | six grey figures standing in a row | six brown-tunic crew standing in a row |
| 282 | six grey figures sitting | six brown-tunic crew sitting |
| 440 | a crewman's grey tunic | a crewman's brown tunic |
| 651 | a single grey sailor with a torch | a single brown-tunic sailor with a torch |
| 67 | pebble beach below tall green cliffs | sandy beach below tall sandstone cliffs (library beach is sand, golden cliffs with green patches) |
| 329 | patting Odysseus's helmet | OK but needs characters/odysseus/turnaround_helmet (non-canonical); same for 448, 551, 588 |

Totals: blockers 3 found / 3 fixed / 0 remaining; minors 11 (4 fixed, 7 open); script lines 9; spend $0.10 of $3.00.
