# ASSET-PLAN.md: art list, prompts and budget for "The Cyclops Case File" (video 1, storyboard of 2026-11-13)

Built from `video2/storyboard.json` (128 shots, 332 events). Nothing generated, called or spent. Labels: **[V]** counted in the storyboard or on disk; **[E]** estimate (per-call figures from FORMAT-BIBLE 5.3 and 6 and `video1/GENERATION-REPORT.md`); **[U]** untested.

Rules this plan follows: FORMAT-BIBLE 5.2 (PNG with alpha, feet anchor, `<char>__<pose>__<variant>.png`, cast.json), 5.3 (master first, one pose per call, master + previous accepted pose as refs, flat-ink clause, never two characters in one call, retry once then rewrite), 6 (plates 1536x864, negative space, no text in the image, no crop beyond 1.1x), and the frozen prompt template `prompt_t0` in `video1/build_manifest.py` (identity paragraph, SCENE with the inline flat clause, KEEP_T0 footer, STYLE_ORIG). Prompt drafts below give the SCENE text only; the build wraps each in the template unchanged.

Summary [V]: **34 painted plates in use, 29 already on disk, 5 new**; **4 map bases (new, cheap)**; **3 public-domain or code-rendered pictures**; **38 character sprite drawings (3 on disk, 35 new)**; **26 generated props (3 on disk) plus 19 code-drawn icons and overlays**. New spend about **$6-9** [E] over about 100 calls.

---

## 1. Painted plates (class A backgrounds, the skull and inset plates)

### 1.1 Reused from `video1/images/` and `tests/stress_test/gen/` (29 plates, 0 calls) [V]
Seconds on screen per the storyboard; shot ids in `STORYBOARD-CHECK.md` appendix.

| Plate | Content | Shots (beats) | s on screen | Note |
|---|---|---|---|---|
| NBG01 | cave on a sea cliff, overcast | 1, 5, 7 | 15.3 | crew cutouts go on the rocky strip (GENERATION-REPORT flag) |
| NBG02 | cave interior, cheese racks, lamb pens | 8, 11, 26, 62b-63, 66 | 22.7 | the most-used plate |
| NB01 | Cyclops hero close-up | 2, 56b | 6.9 | ring overlay on the eye at 56b |
| NB05 | giant's back at the fire, cowering silhouettes | 17, 21a, 27, 108a | 16.5 | counter in the upper right corner (negative space) |
| NB04 | Odysseus, hand on hilt | 21b | 3.2 | |
| NB06 | Odysseus small beside the club | 22a | 5.4 | |
| NB08 | wine offer two-shot | 29a | 6.1 | 20:1 counter upper right |
| NB09 | Cyclops drinks, profile | 29b | 3.2 | bowls stack in the upper right |
| NB10 | Cyclops asleep, Odysseus small | 34-35a | 5.5 | |
| NB11 | glowing stake, giant a black mass | 35b, 108b | 4.5 | |
| NB12 | Cyclops at cave mouth, hand over eye | 38 | 5.6 | Odysseus inset top right |
| NB13 | rams bound in threes at dawn | 41, 108c | 8.4 | |
| NB14_crop_left55 | Odysseus under the ram | 42a | 2.4 | **flagged**: NEEDS HUMAN DECISION in GENERATION-REPORT; the crop is about 2x and breaks the 1.1x rule. See section 7 |
| NB15 | giant hands on wool | 42b | 3.1 | |
| NB17 | Cyclops from behind on the cliff, arm raised | 47b | 3.6 | |
| NB18 | boulder splash beside the stern | 48a | 3.5 | |
| NB20 | sailor in a beach cave with a fire | 62a, 67 | 10.8 | the IMAGINED stamp lands on the baked sailor; the crew sprite is not used here |
| NB22 | Cyclops as smith at the anvil | 88, 114b | 9.5 | |
| NB23 | tongs, hammer, thunderbolt, hands only | 84a | 1.9 | |
| NB24 | seated Cyclops singing on the cliff | 95a | 6.5 | |
| NB25 | two mules straining at a stone | 101 | 8.0 | covers the NEW item "mule"; no mule sprite needed |
| NBG03 | night hillside, moon, glowing cave | 37, 39 | 13.3 | Cyclops silhouettes stand on the ground band against the moon |
| NBG04 | calm dawn sea | 46, 48b, 120 | 12.4 | ship cutout NP04 |
| NBG06 | Aeolian crater, glowing vent, night | 93a | 7.1 | |
| NBG07 | cyclopean wall, raking dawn | 97-98, 99, 105b, 114c | 19.0 | |
| NBG08 | Mycenae Lion Gate | 102, 104 | 18.0 | flagged (lions have heads); illustrative only |
| RC11 (`cy_v4_s11.png`) | Cyclops pushes the boulder, twilight | 13 | 7.2 | |
| RS08 (`s08.png`) | Odysseus, night beach | 121a | 6.0 | |
| RS10 (`s10.png`) | Odysseus shouting on the ship, storm | 47a | 3.3 | |

Not used from video1: NB02, NB03, NB07, NB16, NB19, NB21, NBG05, NBG09, NP02, RS07, RS09, RC02. NB16 (Cyclops bowed to the ram) is the fallback for beat 44 if William wants the ram speech on a plate instead of white.

### 1.2 New plates (5 generated, 1536x864) [E]
Refs follow video1 practice: `cy` = `tests/stress_test/refs/cy_v4_flat.png` with the CY identity paragraph; `land/stone/cave` = the style refs in `video1/refs/`; a base image as ref 1 for an edit.

| Id | Shots | Refs | SCENE prompt draft | Checks | Calls [E] |
|---|---|---|---|---|---|
| **NB_prayer** | 54 (11.4 s, the held beat) | cy + land | "DUSK, blue-violet sky with one band of pale light low on the horizon, wide shot. On a dark rocky shore in the foreground the Cyclops stands with his back to the camera, both huge arms raised to the sky, palms open, head tipped back, shown as a single flat near-black silhouette with his ragged hair, beard and hide wrap read only in outline; no face, no eye visible. Beyond him a dark calm sea and, very small and far out on the water, a single ship with one square sail. No sun, no glow, no god figure in the sky. The upper third of the frame is clear sky." | silhouette only, no eye, no Poseidon, cool palette, ship tiny | 2.5 (Cyclops plate) |
| **NB_forge** | 81-82, 83, 85, 87 (16.4 s) | cave + stone (style only, no character) | "DIM FORGE INTERIOR, warm orange from a single forge hearth at the left, medium-wide shot, empty stage. A great stone anvil on a stump stands at centre on a flat earthen floor, a bed of coals glowing in a stone hearth at the left with bellows, hammers and tongs hung on the rock wall at the right, a chain and a water trough, smoke drifting up into darkness. A clear flat band of floor across the lower third with nothing standing on it, so figures can be placed there; the upper right of the frame is dark and clear for labels. No people and no figures." | no figures, anvil central, clear floor band, flat ink | 1.3 (empty background) |
| **NBG02_mouth** | 12 (5.5 s) | base: `NBG02.png` as ref 1 (edit) + cave style | "Same cave interior as the reference, seen from deeper inside looking toward the entrance: the bright cave mouth fills the right half of the frame as a tall ragged arch of overcast grey daylight, the cheese racks and lamb pens along the left wall in shadow, the floor a flat band across the bottom with nothing standing on it. The daylight in the arch is a flat pale grey-white so a large dark figure standing in it would read as a silhouette. No people, no animals in the arch." | arch bright and empty, same palette as NBG02 | 1.5 (base edit, as NBG01 a4) |
| **NBG06_day** | 93b, 94 (8.5 s) | base: `NBG06.png` as ref 1 (edit) + land style | "Same island crater and coastline as the reference, redrawn in full daylight: pale blue sky, the sea slate blue, the vent no longer glowing but sending up one tall grey-white smoke plume that leans slightly to the right and reaches the top of the frame; the rock warm grey-brown in flat overcast light; the lower right corner is a clear band of shore so a figure can be placed there. No people." | daylight, plume reads at thumbnail, same layout as NBG06 | 1.5 |
| **board_base** | 3, 57-58, 73, 80, 96, 105a, 106-107, 112-113, 114a (55.5 s total) | none (generations endpoint, like the NP props) | "A detective's evidence board seen flat and front-on, filling a widescreen frame: a cork pinboard in a plain dark wood frame, four empty rectangular paper cards pinned in a two-by-two grid with brass pins, each card blank and cream, a few loose pins and a short length of red string in one corner, the top strip of cork above the cards left clear. Flat inked cartoon rendering, no text, no letters, no labels, no photographs on the cards." | four blank cards, clear top strip, no text | 1.3 |

The four board frames are filled in code (frame 1 the skull plate, frame 2 the anvil prop over the forge, frame 3 the Argolid map base, frame 4 the world map base), as are the dim, jitter, glow (ping) and blank states; the stamps are stamp events.

### 1.3 Public-domain and code-rendered pictures (0 generation calls)
| Id | Shots | Source | Status |
|---|---|---|---|
| `skull_front_pd.png` (+ `_small` cutout) | 61b, 65, 69b, 67, 68, 69a, 114d, 117 (31 s in all) | public-domain front-view photograph or engraving of a *Palaeoloxodon* (dwarf elephant) skull; the script says never generated | **species and licence still to confirm** (SCRIPT-V4 end matter h). Candidates to check: Wikimedia Commons *Palaeoloxodon falconeri* skull images (CC licences vary; need PD or CC BY with credit in the description). If no PD front view exists, a front-view photograph of any elephant skull under a usable licence with the species named on the chip |
| `greek_line_9_394.png` | 56a | code: the Greek of Odyssey 9 containing ὀφθαλμός rendered in a serif Greek face from the Perseus Allen text (public-domain text; cite Perseus) | needs the exact line chosen by the fact-checker (the storyboard id guesses 9.394; any Book 9 line with "the eye" serves) |
| `homer_bust_pd.png` | 110 | public-domain photograph or engraving of a Homer bust (e.g., the British Museum type), flattened to two tones in code so it sits with the flat ink | **source to pick**; alternative: one generated `homer__neutral__a.png` head sprite ($0.08) |

### 1.4 Map bases (4 new, code overlays for routes, pins, labels and the ship icon) [E]
Cheap-test method (`tests/cheap_test/`, about $0.06 per call, style ref only, no figures). 1536x864, flat ink, muted parchment-free palette (no scroll look, section 9).

| Base | Shots | SCENE prompt draft | Calls |
|---|---|---|---|
| `map_med` (serves `map_med_west` at 6 and `map_med_loop` at 55) | 6, 55 | "A flat inked map of the central and eastern Mediterranean from the heel of Italy and Sicily to the coast of Asia Minor, land in flat olive-cream with a thin dark-brown ink coastline, sea in flat slate blue, no place names, no lettering, no compass, no borders, a few small ink hatch marks for mountains; the whole frame is map, with the sea areas left plain so route lines and labels can be drawn over them." | 1.5 |
| `map_sicily` | 61a, 90 | "A flat inked map of Sicily with Malta below it and the toe of Italy at the upper right, the Aeolian islands as small dots north of Sicily, Mount Etna drawn as a small ink cone on the east coast, land flat olive-cream with a dark-brown coastline, sea flat slate blue, no names, no lettering, no compass." | 1.5 |
| `map_world` | 106-107, 109, 114d | "A flat inked world map, equirectangular, continents in flat olive-cream with a dark-brown ink coastline, oceans flat slate blue, no names, no lettering, no borders, no compass, Europe and the Middle East near the centre-left so pins there are easy to read." | 1.5 |
| `map_argolid` (frame 3 of the board only) | 97 (board), 105a | "A flat inked map of the Argolid peninsula in the Peloponnese with the Gulf of Argos, two small ink squares for the sites of Mycenae and Tiryns, land flat olive-cream, sea flat slate blue, no names, no lettering." | 1.5 |

---

## 2. Character sprites (white background, cutout by `pipeline/cutout.js`, 1,000 px tall masters)

Existing on disk [V]: `pipeline/remotion-v3a/public/img3/` has `ody.png` (Odysseus neutral, 448x1004), `ody_shout.png` (shouting, pointing), `cy.png` (Cyclops neutral, 646x1004), `cy_blind.png` (blinded, hand over eye), `crew.png` (the crew line-up on white), `sheep.png`, `sheep_f.png`, `ship3.png`, `boulder3.png`, `pos.png` (Poseidon, unused). Masters for the pose batches: `tests/stress_test/refs/odysseus_A_flat.png` and `cy_v4_flat.png` (the locked identity refs). **Caveat:** `cy.png` was cut from cyclops_A, which has the belt bells; any Cyclops sprite for this video must be cut from a cy_v4-based image, so the Polyphemus neutral is regenerated from `cy_v4_flat` (the master pose, gate G2), not reused.

Pose prompt wording per FORMAT-BIBLE 5.3: `refs = master + previous accepted pose; identity paragraph; "same character, pose: <pose text>, full body, feet visible, facing right, plain white background, nothing else in the frame"; flat-ink clause.` Pose texts below are the `<pose text>`.

### 2.1 Odysseus (14 drawings; 2 on disk, 12 new) [V count from storyboard; merged where one drawing serves two notes]
| Pose file | Pose text | Shots (beats) | Source |
|---|---|---|---|
| `odysseus__neutral__a` | master, standing, weight on one leg, arms relaxed | 4, 29a (plate), 98, 107, 109 | on disk (`ody.png`, from odysseus_A); re-cut from `odysseus_A_flat` |
| `odysseus__point__a` | shouting and pointing ahead with the right arm, mouth open | 3 (beside the board) | on disk (`ody_shout.png`) |
| `odysseus__walk__a` | mid-stride, walking, a wineskin slung on the shoulder, seen small | 1, 7 (in plate, 300 px) | new |
| `odysseus__talk__a` | both hands open at waist height, explaining, mouth open (also "handsopen" at 15) | 15, 23 | new |
| `odysseus__shrug__a` | shoulders up, palms out, eyebrows raised | 73, 103c | new |
| `odysseus__think__a` | one hand at the chin, eyes up and to the side, weight back | 19-20 (first), 71-72, 73, 112-113 | new |
| `odysseus__flat__a` | standing straight, arms at the sides, perfectly blank unimpressed face, small mouth (also "unamused") | 31, 32-33, 111, 118-119 | new |
| `odysseus__smug__a` | arms folded loosely, chin slightly raised, half smile, eyes sideways (also the inset "side-eye" at 38, mirrored) | 10, 38 | new |
| `odysseus__armscrossed__a` | arms folded tight, feet planted, mouth set, waiting | 11, 53 | new |
| `odysseus__sworddraw__a` | right hand on the hilt of a short sword at the hip, blade half drawn, leaning forward | 18 | new |
| `odysseus__swordlower__a` | the short sword lowered point-down at his side, shoulders dropped, deflated | 20 | new |
| `odysseus__offerbowl__a` | holding out a wide wooden bowl with both hands at chest height, face deadpan | 28 | new |
| `odysseus__tiptoe__a` | up on his toes, chin high, one fist on the hip, the other hand cupped at the mouth, calling | 50-51 | new |
| `odysseus__lookup__a` | standing with the head tipped far back, looking straight up, hands hanging, seen small | 99, 105b, 114c | new |
| (`tired_helm` at 55 uses `neutral` at 260 px on the map; not a drawing) | | | |

### 2.2 Polyphemus (8 drawings; master new from cy_v4, 7 poses new)
| Pose file | Pose text | Shots (beats) |
|---|---|---|
| `polyphemus__neutral__a` | master (G2): standing, club resting on the ground at his side, hunched asymmetric build, eye open | 4, 90 (small on the map), 115 |
| `polyphemus__wave__a` | one huge hand raised in a small awkward wave, half smile (at 85 the lamb prop is composited under the other arm) | 4, 85 |
| `polyphemus__leandown__a` | bent forward from the waist toward the viewer, hands on his knees, the one eye wide and curious, mouth open | 14 |
| `polyphemus__scorn__a` | straightened up, one hand flicking dismissively, lip curled, eyebrow down over the one eye | 16, 84b |
| `polyphemus__beam__a` | flushed cheeks, sloppy wide grin, swaying with a bowl in one hand (serves "drunk" at 30 and "beams" at 32) | 30, 32 |
| `polyphemus__tender__a` | kneeling on one knee, head bowed, one hand out flat and low as if patting an animal, soft closed-mouth expression, eye half closed (the ram prop stands under the hand; serves "lovesick" at 95 with the heart prop) | 44, 95b |
| `polyphemus__armswide__a` | both arms flung wide, palms up, pleading, eyebrow raised (serves "shrug" at 115 as a swap) | 52, 115 |
| `polyphemus__wounded__a` | one hand flat on his chest, mouth a small o, eyebrow up, hurt | 52, 116 |
| `polyphemus__silhouette__a` | not a drawing: the neutral sprite filled flat near-black in code | 12, 121 |

### 2.3 Crew (one crewman sprite, 6 poses; group sets built in code from it)
The crewman master is cut free from `crew_A` (`tests/chars_v3/gen/crew_A.png`, the style-A line-up; GENERATION-REPORT: use the leftmost full figure) and locked as `crew_master`. Pose texts name "the same sailor", never the group (crew-centred generation failed 0 of 7).

| Pose file | Pose text | Shots |
|---|---|---|
| `crew__neutral__a` | master: standing, short tunic, bare-headed, oar-callused hands at the sides | 4, 67, 76, 114d, 117 |
| `crew__point__a` | pointing hard to one side with the whole arm, mouth open, urging | 9, 69a |
| `crew__plead__a` | hands clasped at the chest, eyebrows up, a single sweat drop (serves "worried" at 24 and the pair at 49, mirrored) | 24, 49 |
| `crew__torch__a` | holding a burning torch up in one hand, the other hand raised in a hesitant hello, peering | 63, 64 |
| `crew__alarmed__a` | leaning back hard, both hands up, eyes wide, mouth open, one foot already turned to run | 66 |
| `crew__lookup__a` | head tipped back looking straight up, one hand shading the eyes, mouth open (serves "squint" at 68 with the magnifier prop at 75) | 68, 75, 100, 102 |
| Code-built groups: `crew__line12__a` (12 copies at 240 px, small offsets, poses mixed neutral and point), `crew__huddle4__a` (4 copies, two mirrored, leaning in), `crew__workers_group__a` (6 copies at 300 px, alternating lookup and point) | | 1, 7, 23, 104 |

### 2.4 Other Cyclopes, CYC2 (the neighbours and the three smiths; 6 drawings, all new)
They share Polyphemus's species rules (one eye, no bells, olive-brown) but must read as different individuals: a master (G2) with a shorter grey beard, cropped hair, a leather smith's apron over the hide kilt, and a slimmer, more symmetric build than Polyphemus. The three smiths are this one sprite three times with hand props and mirroring (UF's identical-soldiers method). Identity paragraph: the CY paragraph with the beard, hair, apron and build sentences replaced.

| Pose file | Pose text | Shots |
|---|---|---|
| `cyc2__neutral__a` | master: standing, arms loose, bored expression, eye half-lidded | 40 (x3), 93 (trio) |
| `cyc2__shrug__a` | shoulders up, palms out, eye rolled up (also the "hat tip" at 94 with a felt cap prop) | 40, 94 |
| `cyc2__back__a` | seen from behind, walking away, one hand raised in a dismissive wave over the shoulder (serves `trio_backs` and `trio_leaving`, three copies; `trio_silhouette` is the neutral filled black) | 37, 39 |
| `cyc2__smith_hammer__a` | smith's hammer raised over the shoulder in one fist, apron on, eye intent | 83 (x2, one mirrored), 87 (trio, hammers up) |
| `cyc2__smith_tongs__a` | holding long tongs out in front with both hands, leaning back from the heat | 83, 85 (trio stare) |
| `cyc2__smith_flat__a` | hammer hanging straight down from one hand, shoulders dropped, dead-flat expression, mouth a line | 86 |

### 2.5 New named characters (3 drawings)
| Pose file | Pose text (full identity in the call, no other character named) | Shots |
|---|---|---|
| `empedocles__neutral__a` | "a Greek philosopher of the fifth century BC: an older man with a long grey beard and bald crown, a plain undyed himation wrapped over one shoulder, bare feet, standing with one hand raised as if lecturing; NO laurel wreath, NO blue sash, NO red tunic" (so he does not read as Odysseus) | 74 |
| `thucydides__neutral__a` | "a Greek historian: a lean middle-aged man with close-cropped hair and a short dark beard, a plain grey himation, standing holding a rolled papyrus scroll at his side; no wreath, no sash" | 92, 93 (small inset) |
| `thucydides__palmsup__a` | same character, pose: both palms turned up at waist height, head tilted, an honest "I cannot tell" face | 92 |

---

## 3. Props and icons

### 3.1 Generated props on white (26; via the generations endpoint with no reference, which returned transparent cutout-ready PNGs 4 of 4 in video1) [E]
Each prompt: the NP01 wording with the object swapped in: "A <object> ... on pure white. Flat ink, one cel-shadow tone. Simplified proportions." + the NP render paragraph + STYLE_NP. About $0.05 per call, 1.2 calls each.

| Prop file | Object text | Shots | On disk? |
|---|---|---|---|
| `prop__cheese__a` | a round wheel of pale cheese with a wedge cut out, on a wooden board | 5, 8 | new |
| `prop__wineskin__a` | a bulging dark goatskin wine bag with a wooden stopper and a carrying strap | 7 | new |
| `prop__gift_basket__a` | a woven wicker gift basket with a cloth and a bow, empty | 11 | new (script NEW item) |
| `prop__lightning__a` | a jagged gold thunderbolt, two forks | 16, 84 | new |
| `prop__club__a` | an uprooted olive-wood club with grey-green bark, knot stubs and silver-green leaves at the thick end, lying horizontal | 22b | new |
| `prop__stake__a` | a long sharpened olive-wood pole, the point charred black, no metal, NOT a sword | 22b, 26, 35a | new |
| `prop__flames__a` | a small campfire of three logs with flat orange flames | 22b | new |
| `prop__dung__a` | a soft heap of dried sheep droppings and straw, stylised, brown, a few flies as dots | 26 | new |
| `prop__bowl__a` | a wide shallow wooden drinking bowl, dark red wine inside | 29b | new |
| `prop__ram__a` | a large ram with heavy curled horns and thick cream wool, side view, standing | 44 | reuse `sheep.png` if horns read; else new |
| `prop__ram_with_feet__a` | the same ram from the side with a pair of sandalled human feet and shins showing beneath its belly | 43, 45 | new |
| `prop__sheeptrio__a` | three sheep walking abreast, bound together across the chests with twisted willow rope | 41 | new |
| `prop__giftbox__a` | a small wooden chest with the lid open, a gold cup inside | 52 | new |
| `prop__magnifier__a` | a large hand magnifying glass with a brass rim and wooden handle | 56a, (75 in hand) | new |
| `prop__book_fossil_hunters__a` | a thick hardback book standing upright, plain dark cover, NO text on the cover (the title is lettered by code) | 71 | new |
| `prop__fossil_bone__a` | a single large fossil long bone, grey-brown, cracked | 73, 74 | new |
| `prop__drawer_closed__a` / `prop__drawer_open_empty__a` | a small wooden card-index drawer with a brass label holder, closed; the same drawer pulled open and empty | 75 | new (2) |
| `prop__hammer__a` | a smith's hammer, iron head, wooden haft | 82 | new |
| `prop__anvil__a` | a smith's anvil on a tree-stump base | 117, board frame 2 | new |
| `prop__wall_block__a` | a single huge rough limestone block, unworked, taller than a man | 100, 103, 117 | new |
| `prop__boulder__a` | a rounded grey boulder | 103 | on disk (`boulder3.png`) |
| `prop__folktale_scroll__a` | a loosely rolled papyrus scroll with one end unrolled, no text | 110, 117 | new |
| `prop__bag__a` | a leather sack tied at the neck with a cord, bulging | 120 | new |
| `prop__wand__a` | a slim dark wand with a small knob at the end | 120 | new |
| `prop__whirlpool__a` | a stylised whirlpool of concentric slate-blue rings | 120 | new (or code) |
| `prop__etna_icon__a` | a small volcano cone with a smoke plume | 90 | new (or code) |
| `NP01.png` dwarf elephant, `NP03.png` axe in trough, `NP04.png` ship (+ `NP04_listing` = NP04 rotated 12 degrees in code) | | 57, 59-60, 61a, 70; 36; 46, 48b, 120 | on disk |

### 3.2 Code-drawn icons and overlays (0 calls)
`ring_small`, `ring_large`, `eye_icon`, `oneeye_crossed`, `ship_crossed` (NP04 small with an X), `ship_icon` (NP04 at 90 px), `height_line`, `person_silhouette` (plain modern figure, flat grey), `waterdrops`, `pin`, `bone_pin`, `book_icon`, `arrow_left`, `pointer`, `heart`, `flame_glow`, `dustpuff`, `source_slip_empty`, the hand-drawn `X` crossout, the four board frame states, the stamps (UNPROVEN, PLAUSIBLE, REAL, PROBABLY OLDER + THAN HOMER, CASE OPEN, IMAGINED, ?), counters and chips. All use the display face and accent colours chosen at G2.

---

## 4. Call plan and cost [E]
Per-call figures: plates $0.10-0.15 (bible 6); Cyclops-only plates 2.5 attempts, empty backgrounds 1.3, base edits 1.5 (GENERATION-REPORT recommendation 2); maps $0.06 x 1.5 (cheap test); sprites $0.05-0.10 x 1.5 (bible 5.3); props $0.05 x 1.2 (video1 NP rows, 4 of 5 accepted).

| Group | Items | Calls | Cost |
|---|---|---|---|
| New plates | 5 | 8 (2.5 + 1.3 + 1.5 + 1.5 + 1.3) | $0.8-1.2 |
| Map bases | 4 | 6 | $0.36 |
| Odysseus poses | 12 | 18 | $0.9-1.8 |
| Polyphemus master + poses | 8 | 12 | $0.6-1.2 |
| Crew poses (master cut free) | 5 | 8 | $0.4-0.8 |
| Other Cyclopes master + poses | 6 | 9 | $0.45-0.9 |
| Empedocles, Thucydides | 3 | 5 | $0.25-0.5 |
| Props | 23 new | 28 | $1.4 |
| Contingency (one rewrite round on the two Cyclops masters and NB_prayer) | | 6 | $0.5-0.9 |
| **Total** | **66 generated items** | **about 100 calls** | **$5.7-9.1** |

Against the bible's episode-1 estimate of $12-20: lower because 29 plates, 3 sprites and 4 props already exist. Review time is not costed. Order of work (gate G2 first): the three masters (Polyphemus from cy_v4, crewman cut, CYC2) and the accent and font, then the Odysseus and Polyphemus batches, then props (fast, cheap, no refs), then the five plates and four maps.

---

## 5. Reuse already on disk, by folder [V]
- `video1/images/`: 26 plates and 3 props listed in 1.1 and 3.1; `video1/refs/` holds the locked refs and style anchors (`odysseus_A_flat`, `cy_v4_flat`, `sty_cave`, `sty_land`, `sty_stone`, `flock_ref`, `ship_flat`).
- `tests/stress_test/gen/`: `cy_v4_s11` (RC11), `s08` (RS08), `s10` (RS10); `refs/cy_v4_flat.png` is the Polyphemus master source.
- `tests/chars_v3/gen/`: `crew_A.png` (crewman master source), `odysseus_A.png`, `pose_ody_A.png`, `sheep_A.png`.
- `pipeline/remotion-v3a/public/img3/`: `ody.png`, `ody_shout.png`, `boulder3.png`, `sheep.png`, `ship3.png` reusable; `cy.png` and `cy_blind.png` are cyclops_A (bells) and are not used.
- `pipeline/cutout.js`, `pipeline/remotion-v3a/cut_a.js`, `tests/stress_test/flat.js`, `video1/make_sheets.js`: cutout, flatten and contact-sheet tools; `video2/spike/` renders `sprite`, `label`, `counter`, `route` and must add `chip`, `stamp`, `bubble`, `swap`, `sfx` and the `board` bg type [U].
- `brand/`: avatars and banner only; nothing for the episode (the end card needs the display face from G2).

---

## 6. Sprite and plate counts against the bible
| Set | Bible target | Plan | Note |
|---|---|---|---|
| Lead (Odysseus) | 14 | 14 (2 on disk) | |
| Antagonist (Polyphemus) | 8 | 8 | silhouette is code |
| Two more speaking characters | 5 each | crew 6, other Cyclopes 6 | one extra each for the smith props and the alarmed slide-out |
| Group sets | 6 | 7, all code-built from single sprites | line12, huddle4, workers, plead pair, CYC2 trios x3 |
| Props | ~10 | 26 generated + 19 code | the script names many props; each is one cheap no-ref call |
| New named characters | (script) | 3 | Empedocles 1, Thucydides 2 |
| Painted plates | ~44 + 4-5 maps | 34 (5 new) + 4 maps | video1 art covers 29 |
| **Total new drawings** | ~48 | **35 sprites + 23 props + 5 plates + 4 maps = 67** | |

---

## 7. Shots whose art is not covered or is at risk
1. **Beat 42a, NB14_crop_left55 (s053, 2.4 s).** The only accepted version is a 2x crop (soft) and the uncropped candidates show an open eye and a reaching giant. Options: (a) accept the soft crop for 2.4 s; (b) regenerate as a Cyclops-free plate "ram walking toward camera, Odysseus hanging under it" with the `ody` ref only (Odysseus-only plates passed 5 of 6), 2 calls, $0.2-0.3; (c) composite `prop__ram_with_feet__a` on NBG02 (free). Recommended: (b).
2. **Skull plate** (8 shots, 31 s): no file yet; species and licence to confirm before the storyboard is built. If no public-domain front view exists, the fallback is NB19 (generated cave floor with a small skull, soft when cropped) for the cave moment only, and a labelled line drawing (code) for the sockets and nasal cavity.
3. **Homer bust** (beat 110): no file yet; public-domain source to pick, or one generated head.
4. **Greek line** (beat 56a): needs the fact-checker's chosen line and a Greek-capable font with a commercial licence.
5. **NB20 at beat 67**: the IMAGINED stamp lands on a baked back-view sailor; if William wants the stamp on a front-facing sprite, play 67 on white with `crew__neutral__a` (the storyboard note allows the swap; class B instead of A).
6. **Board pings at 13, 36, 44** depend on the board frame art existing early; they are optional (OPEN-DECISIONS).
7. **Other Cyclopes look**: a new master; the risk is that it reads as Polyphemus (same species rules). The apron, grey beard and symmetric build are the differentiators; G2 decides.
8. **Empedocles and Thucydides**: generic bearded Greeks; the "no wreath, no sash, no red" clause is there so they do not read as Odysseus; readability at 780 px untested [U].
9. **Sprites at small sizes**: the walking Odysseus at 300 px (beats 1, 7) and the lookup pose at 220 px (99, 105b, 114c) are below the 280 px face-readability bar; they are silhouette-scale on purpose (the wall and cave carry the shot), as the bible allows for wide shots.
10. **Fourteen poses in one session is untested** (bible 5.3 [U]); plan the Odysseus batch in two sessions of six and review the first before the second.
