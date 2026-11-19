# REVIEW-cards-v1-2026-11-12.md: Editor's card audit of Video 1 draft

Read-only audit. Nothing generated, uploaded or sent. Scratch files (frames, contact sheets) are in `/tmp/ed_audit/` and `workspace-editor/audit_tmp/`.

**Method.** `video1/draft/video1_draft.mp4`, Remotion's bundled ffmpeg, frames at 15%, 50% and 88% of every non-picture shot (64 shots: 25 card, 19 diagram, 9 map, 6 white cutaway, 5 chapter card; 192 frames, 16 contact sheets, all viewed). Narration per shot comes from `shots_timed.json` and was spot-checked against `audio/words.json` at 1:47, 2:44 and 6:20 (all match). I also viewed all 44 accepted images in `video1/images` so every reuse suggestion below is a picture I have actually seen.

## 1. William's two named cards

- **1:47 is shot 28 (`CODE:tally-six`, 1:46 to 1:49, 3.5 s).** Frames: a single bar draws, then six vertical bars in three pairs, then the italic line "six men, two at a time" in very small type. Narration: "Homer gives the detail. We will leave it out." The card visually does the opposite of the line (it draws the detail), it is a dark void with six sticks, and it follows two shots that already said the number. REPLACE.
- **2:44 is shot 40 (`CODE:card-hesiod-teaser`, 2:40 to 2:45, 5.3 s).** Frames: "A DIFFERENT POET", then "Hesiod", then "Theogony, line 145 / c. 700 BC". Narration: "For a plain statement, one eye in the forehead, we need a different poet." It is a nameplate with no picture for the one thing the line is about, a one-eyed smith. The Hesiod *names* card William means (6:16 to 6:30) is shot 90, `CODE:ledger-names`, 7.9 s. It is the longest text card in the video: "names three Cyclopes", then BRONTES thunder / STEROPES lightning / ARGES bright over the voice saying exactly that. Both are REPLACE.

## 2. Totals

| Verdict | Shots | Seconds | Share of 612.8 s |
|---|---|---|---|
| KEEP | 26 | 111.0 | 18.1% |
| IMPROVE | 10 | 43.4 | 7.1% |
| REPLACE | 23 | 101.6 | 16.6% |
| Chapter cards (treatment change) | 5 | 10.0 | 1.6% |
| **Total non-picture** | **64** | **266.0** | **43.4%** |

(Matches the 44% in the pipeline recommendation. 30 shots, 122.5 s, 20% of runtime, are pure text on a dark card with no imagery at all.)

Worst runs with no picture: 5:16 to 5:43 (shots 76 to 81, 27 s: two arrow diagrams and four text cards in a row), 8:26 to 8:58 (32 s, but mostly chapter card, ledger and the good maps), 5:47 to 6:08 (shots 83 to 86, 17 s), 9:17 to 9:42 (133 to 137, 17 s), 0:00 to 0:17 (17 s, but those are good: map, scale, skull).

## 3. Card-by-card (time = shot start in the cut)

Replacement tier: **T1** existing accepted image or crop, **T2** code-built from existing assets, **T3** new generated image (N1 to N6, defined in section 4), **T4** better card.

| # | Time | Shows | Narration | Verdict and evidence | Fix |
|---|---|---|---|---|---|
| 1 | 0:00 | Mediterranean, Sicily in rust, push-in | Elephant lived on Sicily | KEEP. Real map with motion. | none |
| 2 | 0:04 | NP01 dwarf elephant next to Odysseus, 1.7 m rule | Less than a metre tall at the shoulder | KEEP. Scale chart tells what the voice can't. | none |
| 3 | 0:08 | Skull front, circle on hole | Skull has one enormous hole | KEEP. | none |
| 4 | 0:11 | "1914" large, then "A palaeontologist ties the hole to the Cyclops", "Othenio Abel" | In 1914 a palaeontologist argued... | **REPLACE.** 5.8 s of a number and a repeat of the caption. | T3 N1 "Abel's study" with small lower-third "1914 / Othenio Abel". T1 fallback: DG-01 skull plate with a date stamp. |
| 6 | 0:22 | Skull plate beside Cyclops eye, "?" | If it is right... honest mistake | KEEP. Best idea in the cold open. | none |
| 8 | 0:32 | "THE PLAN", empty for ~1.5 s, then row "1 The poem" appears | So we will go slowly: the poem first | **REPLACE.** Half the shot is a blank dark card. | T2 triptych in the style of shot 122: NB02 (poem), NB19 or skull plate (bones), NB21 (people who disagree), tiles fill on the words. |
| 9 | 0:35 | Rows 2 and 3 appear | then the bones, then the people who disagree | **REPLACE.** Same card. | Same triptych, 8 and 9 merge into one 6.2 s build. |
| 10 | 0:38 | Numeral "I / The poem" (first frames ghost the roadmap text under the numeral) | silent, sting | Chapter card, see section 6. Crossfade ghosting is sloppy. | Section 6. |
| 23 | 1:24 | Boulder at left, wagon icons count to 17 then 22 | Twenty-two four-wheeled wagons | KEEP. Counter synced to the number is the card done right. Wagons are small; enlarge if time. | none |
| 28 | 1:46 | Tally bars, "six men, two at a time" | Homer gives the detail. We will leave it out. | **REPLACE** (William). Contradicts the line, nothing to look at. | T1 RS07 close-up of Odysseus' face in firelight, a reaction shot ("he saw it, we won't show it"). Alt T1: NBG03 cave glow from outside at night, no figures. Optional T3 N7. |
| 33 | 2:04 | Wine bowl, row of 20 squares, 1 rust and 20 blue | Mixed with twenty measures of water | KEEP, polish optional. The ratio is information; the bar is a bit abstract (20 jug icons would read better). | low priority |
| 38 | 2:30 | "SEARCH: ODYSSEY, BOOK 9", "'one eye' 0 hits", "'forehead' 0 hits" | Search the whole of Book Nine... never writes 'one eye' | IMPROVE. The concept (an absence) is a good beat, but it is a list. | T2: typing search box over scrolling Greek text of Od. 9, result "0 matches". |
| 40 | 2:40 | "A DIFFERENT POET / Hesiod / Theogony, line 145 / c. 700 BC" | one eye in the forehead, we need a different poet | **REPLACE** (William). | T3 N4 three Cyclopes at the forge, slow push to the foreheads, lower-third "Hesiod, Theogony, c. 700 BC". Interim T1: NB22. |
| 41 | 2:45 | NP02 drill boring a plank on cream | Homer compares it to a shipwright boring a plank | KEEP. Illustrates the simile. | none |
| 42 | 2:51 | NP03 axe quenched in barrel | smith quenching an axe | KEEP. Same. | none |
| 56 | 3:56 | "II / The bones" | silent | Chapter card. | Section 6. |
| 57 | 3:58 | Cyclops cutout standing on cream, ground line | So that is the myth. Is there anything solid underneath it? | IMPROVE. A cutout on blank cream; the line says "underneath" and the picture shows nothing under. | T2: cutaway: Cyclops cutout on the ground, strata below, the skull plate buried under his feet. |
| 58 | 4:02 | "Die Tiere der Vorwelt / Othenio Abel, 1914" | Abel thought there might be | **REPLACE.** A book title is not a picture. | T3 N1 (desk, open book). Option: Abel's fig. 5 plate from the 1914 book (RESEARCH-V1 says it is public domain; not fetched, licence unchecked). |
| 59 | 4:07 | Map: Sicily, Malta, Cyprus, Crete, Aegean dots appear | Dwarf elephants lived on islands | KEEP. | none |
| 60 | 4:12 | Same map, route lines draw | Sicily, Malta, Crete, Cyprus | KEEP. | none |
| 61 | 4:17 | Scale chart: 4 m ancestor pops in beside the dwarf and Odysseus | Descended from a straight-tusked elephant | KEEP. | none |
| 62 | 4:21 | NP01 + Odysseus, "under 1 m at the shoulder" (frame-for-frame the same as shot 2) | island life shrank them | IMPROVE. Repeats shot 2 in 1.9 s. | T2: animate the 4 m elephant shrinking to 1 m inside the 61 chart; fold 61+62. |
| 64 | 4:26 | Skull plate, "where a face would put two eyes" ghost circles | Look at the skull from the front | KEEP. | none |
| 65 | 4:28 | Eye sockets circled and labelled | Eye sockets are small, low at the sides | KEEP. | none |
| 66 | 4:32 | Trunk opening circled | Huge hole in the middle | KEEP. This skull sequence (64 to 66, 124 to 125, 136, 143) is the video's strongest teaching graphic. | none |
| 70 | 4:49 | "The First Fossil Hunters / Princeton University Press, 2000 / Stanford folklorist..." | Mayor, a Stanford folklorist... | **REPLACE.** 6.3 s of a book title. | T1 NB21 (giant bone in temple) wide, with lower-third "Adrienne Mayor, folklorist, Stanford". Shift 71 to 73 to different NB21 crops so one image doesn't run 20 s. |
| 74 | 5:09 | "THE LEDGER: Mayor on the Cyclops / careful" | On the Cyclops, though, Mayor herself is careful | **REPLACE.** Two words in a table. | T3 N3 scholar's bench (lower-third quote on 75 stays). |
| 76 | 5:16 | Boxes MYTH → BONES? | We do not know which came first | IMPROVE. Real logic (two possible orders) drawn as words in boxes. | T2: replace boxes with Cyclops cutout and skull plate and the two arrows. |
| 77 | 5:22 | Both rows, top row highlighted | Perhaps the myth came first | IMPROVE. Same diagram, 9.5 s total with 76. | Same. |
| 78 | 5:26 | "Abel: Empedocles reported the bones", UNVERIFIED stamp | Then there is a problem with the most famous version | **REPLACE.** | T3 N2 archive of scrolls. |
| 79 | 5:29 | "Empedocles / Greek philosopher, c. 492-432 BC" | Abel claimed Empedocles reported finding such bones | **REPLACE.** A name on black. | N2, lower-third nameplate. |
| 80 | 5:35 | "Claim: bones reported on Sicily / Ancient source: none" | No surviving ancient source says so | **REPLACE.** | T2 citation-chain diagram over N2: Abel 1914 → Empedocles → [empty scroll slot]. 78 to 80 = 13.4 s of text becomes one picture sequence. |
| 81 | 5:39 | "The critics / Mark Witton & Richard Hing / Interdisciplinary Science Reviews, 2024" | Witton and Hing put it bluntly | **REPLACE.** | N3 with lower-third nameplate, merge with 82. |
| 83 | 5:47 | World map, two label boxes, no markers | Elephant fossils and one-eyed monsters turn up all over the world | IMPROVE. Idea is right, execution is two boxes on an empty map. | T2: markers for the fossil finds and the one-eyed-monster traditions (needs a sourced list; check RESEARCH-V1 before drawing). |
| 84 | 5:52 | Mediterranean map, Sicily (identical to shot 1) | No ancient text or artwork makes the Sicilian link stand out | **REPLACE.** A repeat of the opening map for a line about absence. | N2 (the archive with an empty gap). |
| 85 | 5:57 | "Aguirre & Buxton / Cyclops · Oxford University Press, 2020" | Make a similar point | **REPLACE.** | N3 with lower-third. |
| 86 | 6:02 | "THEIR VERDICT: PLAUSIBLE ✓ / CHAIN OF ARGUMENT [empty]" | Plausible... but lack a chain of argument | **REPLACE.** | Keep the two-line text as a small overlay on N3, same shot as 85, 87. |
| 88 | 6:09 | "III / Other Cyclopes" | silent | Chapter card. | Section 6. |
| 90 | 6:14 | "names three Cyclopes" for 4+ s, then BRONTES/STEROPES/ARGES with meanings | Hesiod names three Cyclopes... Thunder, Lightning, and Bright | **REPLACE** (William). Longest card, 7.9 s, with a near-empty first half. | T3 N4: pan across the three Cyclopes, one name label per figure on its word. Interim T1: NB22 plus NB23 crop with a lower-third. |
| 95 | 6:37 | Shepherd (RC02) beside smith (NB22) | Same name, same eye, different job | KEEP. | none |
| 96 | 6:40 | "Walter Burkert / suggested the smith Cyclopes may reflect real guilds" | Burkert suggested... guilds of metalworkers | **REPLACE.** Name card for a claim that is a picture (a workshop of human smiths). | T3 N5 bronze workshop, lower-third. Interim T1: NB22 crop. |
| 97 | 6:47 | Sicily, Etna and Lipari/Stromboli dots in sequence | Virgil puts Brontes and Steropes in a forge under Etna | KEEP. | none |
| 106 | 7:30 | Argolid map, Mycenae then Tiryns | There is a third strand | KEEP. Plate is mostly an empty brown blob; polish only. | low priority |
| 107 | 7:32 | Adds Argos | and it is real | KEEP. | low priority |
| 116 | 8:09 | "Tiryns walls → Cyclops / Fossil bones → giants / Skull (unproven) ⇢ Cyclops" | The Greeks attached giants to things they could not explain | IMPROVE. A good thesis line, rendered as a 3-row text table. | T1/T2: three tiles from existing pictures: NBG07 → Cyclops, NB21 → giants, skull plate dashed → Cyclops. |
| 120 | 8:26 | "IV / The ledger" | silent | Chapter card. | Section 6. |
| 121 | 8:28 | "SOLID ✓ / NOT SOLID [empty box]" | Start with what is solid | **REPLACE.** Two column heads and a tick. | T1: NBG08 (Lion Gate masonry) slow push; "solid" is literally the wall. |
| 122 | 8:31 | Three tiles: shepherd, smith, wall-builders | Three different Cyclops stories | KEEP. Picture-led, works. | none |
| 123 | 8:36 | "A SINGLE EYE IS STATED BY: Hesiod ✓ Euripides ✓ Theocritus ✓ Homer: implied" | A single eye is stated by Hesiod, Euripides, Theocritus. Homer implies it. | IMPROVE. 6.5 s of a checklist. | T1 four tiles from existing images: NB22, NBG05, NB24, NB01 (eye covered/dashed for "implied"). |
| 124 | 8:43 | Skull with island inset map | Dwarf elephants really lived on those islands | KEEP. | none |
| 125 | 8:45 | Skull, hole circled | skulls really do have a hole in the middle | KEEP. | none |
| 126 | 8:48 | World map, markers appear, counter 180 → 200+ | Over two hundred versions | KEEP. | none |
| 127 | 8:54 | Same, Iceland to Korea | from Iceland to Korea | KEEP. | none |
| 133 | 9:17 | "cyclopia / a birth defect in which the eye sits below the nose, not above it" | though in that condition the eye sits below the nose | **REPLACE.** A word and its definition; the claim is about position, so show position. | T2: two plain face outlines, "myth: eye in forehead" (cy_v4 crop) vs "cyclopia: eye below nose" (icon-level only). No clinical imagery (ad safety, taste). |
| 134 | 9:21 | "FOUR CANDIDATES / PROOF" table fills | Each has an air of plausibility | **REPLACE.** | T1/T2: four tiles (NBG06 volcano, NB22 smith, the cyclopia diagram, skull plate). |
| 135 | 9:25 | Same table, "none" in every row | and none has proof | **REPLACE.** | Same tiles, "NONE" stamp over each. Merge 134+135 (5.8 s). |
| 136 | 9:27 | Skull, HYPOTHESIS stamp | A hypothesis, plausible, unproven | KEEP. | none |
| 137 | 9:32 | "V / Verdict" | silent | Chapter card. | Section 6. |
| 140 | 9:39 | "THE NAME COVERS AT LEAST FOUR THINGS: 1 Hesiod's thunderbolt smiths..." | The name covers at least four different things | **REPLACE.** The list is redundant: shots 141 to 142 show those four things as pictures. | Delete the card. Start the four-panel build at 140 (zero new images). |
| 141 | 9:42 | Four-panel build, pictures | Hesiod's smiths, Homer's shepherd, Sicilian tradition | KEEP. | none |
| 143 | 9:50 | Skull, SUSPECT stamp | A suspect, not a conviction | KEEP. | none |
| 145 | 10:00 | "NEXT TIME: The winds, the witch, and the other monsters of the Odyssey" | Next time | **REPLACE.** | T3 N6 teaser: ship between whirlpool and cliff, many-headed shadow behind a rock (silhouette only). Interim T2: NBG04 + NP04 ship with wind streaks. |
| 146 | 10:04 | "SUSPECTS TO CHECK: Scylla ? Charybdis ? Sirens ? Laestrygonians ?" | Some have real-world suspects too | IMPROVE. | Same N6 image under a small caption list. |
| 147 | 10:09 | Repeats the "winds, witch" line, logo, "Subscribe..." | Subscribe | IMPROVE (minor). The end card is fine as a card; the repeated heading is a duplicate of 145. | Drop the duplicate heading. |

## 4. New images needed (T3), prompt-ready (style A: flat inked, same template and refs as the accepted set)

Rule I applied: one new image replaces two to four cards, with lower-third nameplates doing the job of the name cards.

| ID | Replaces | Prompt line | Safety |
|---|---|---|---|
| **N1** Abel's study, 1914 | 4, 58 | "Flat inked illustration, a lamplit scholar's study in 1914 Vienna: cluttered oak desk, an elephant skull front-on in the foreground, an open book, a pencil sketch of a one-eyed giant face pinned to the wall behind, warm lamplight, rain on a window; scholar seen from behind, small, no face." | clean |
| **N2** The empty slot | 78, 79, 80, 84 | "Flat inked, an ancient library room: wall of pigeonholes full of papyrus scrolls, one pigeonhole empty and dark, oil lamp, dust in the light, cool grey-green palette, no people." | clean |
| **N3** Scholar's bench | 74, 81, 85, 86 | "Flat inked, a modern palaeontologist's workbench: elephant skull cast, open journals, magnifier, desk lamp, shelves of bones, soft window light, no people." | clean |
| **N4** Three Cyclopes at the forge | 40, 90 | "Flat inked, a cavern forge, three Cyclopes (cy_v4 design, one eye each in the forehead) hammering a glowing thunderbolt on one anvil, sparks, furnace glow, blue-black cavern around, working scene, no humans." | Highest risk (Cyclops). Budget 2.5 calls. |
| **N5** Bronze workshop | 96 | "Flat inked, a Bronze Age metalworkers' workshop: three ordinary human smiths at clay furnaces and an anvil, moulds and tools on racks, warm furnace light, seen from a distance." | clean |
| **N6** Next-time teaser | 145, 146 | "Flat inked, a wooden ship at sea between a whirlpool on the left and a cliff on the right, stormy teal sky, a many-headed shadow looming behind the cliff, silhouette only, small ship." | Silhouette only, no gore. |
| N7 (optional) | 28 (alt to RS07) | "Flat inked, the inside of a cave seen from the sealed entrance at night: a giant's long shadow thrown across the wall by a fire, two tiny shadow figures far back, nothing explicit." | Crew only as shadows, not as subject. |

**Cost.** 6 required images. Per the generation report: reject rate 42% overall (27 of 64 calls), 1.73 calls per accepted image on average, 1.2 to 1.3 for places and props, about 2.5 for anything with the Cyclops. Estimate: 4 × 1.3 + 2.5 + 2.0 = **9.7, call it 10 to 11 calls = $1.00 to $1.65** at $0.10 to $0.15. Plan a cap of 16 calls ($2.40). With N7 add about 2 calls ($0.20 to $0.30). A flat 42% reject rate on 6 images gives 10.3 calls, same range. Two Cyclops images (N4, and N7 if wanted) are where overruns will come from; use the "change the method, not the adjectives" retry rule after two rejects.

The T1 and T2 fixes need no generation. By count: **23 REPLACE cards**. 14 take a T3 image (N1: 4, 58; N2: 78, 79, 80, 84; N3: 74, 81, 85, 86; N4: 40, 90; N5: 96; N6: 145). The other 9 are T1 or T2 only (8, 9, 28, 70, 121, 133, 134, 135, 140). The 10 IMPROVE items are all T1 or T2. **6 new images** cover all 14.

## 5. Pacing

Total runtime does not change: shots are locked to narration. Replacements are picture shots of the same 2 to 6 s, so the cut rate stays at about 14 cuts per minute, but the amount of *change on screen* rises, because (a) the 27 s run at 5:16 to 5:43 and the 17 s runs at 5:47 and 9:17 stop being static text, and (b) every new picture holds with a push-in and a lower-third reveal (the existing picture shots already do this and passed the jerk check). Merge short neighbours where they share an image (8+9, 61+62, 78 to 80, 85+86, 134+135, 140 into 141) so the held cut count drops slightly; keep the 14 sub-2.5 s shots as they are. Shot 90 (7.9 s) should get an internal pan so it is not a single hold.

## 6. The five chapter cards (0:38, 3:56, 6:09, 8:26, 9:32)

They are 2.0 s each, 10 s total (1.6%), and exist for the sting. Frames show a dark card, the numeral, a rule, the chapter name, with a crossfade from the previous shot; the first frames of chapter I even show the roadmap text ghosting under the numeral. Recommendation: keep the 2.0 s window and the sting, drop the dark card, put the numeral and title over a darkened relevant image with a slow push-in: **I** NB02 (the hall, fire, Odysseus telling the tale), **II** NB19 (skull on the cave floor, pushed in) or N1, **III** N4 (or NB22 until N4 exists), **IV** NBG07 (the walls, "what is solid"), **V** NB01 (Cyclops face) or the skull plate. Cost: zero new images.

## 7. Recommended target mix (share of runtime)

| Type | Now | Target |
|---|---|---|
| Picture (baked, cutouts, picture tiles, triptychs) | 56% | about 68% |
| Quote or overlay text on a relevant picture | included above | about 8% (counted separately, text sits over art) |
| Map | 6.6% | about 7% (8 good maps kept) |
| Diagram (skull, scale, counters, chain) | 12.9% | about 14% |
| Pure card (end card, at most one more) | 20% (cards + chapters + white + text ledgers) | **3% or less** |

(After the fix, non-picture time is about 24%: maps 7%, diagrams 14%, cards 3%. Every one of those is a real map, skull, scale or counter graphic except the end card.)

## 8. Priority order (fix these first)

1. Shot 90 and 40 (Hesiod names and teaser, 13.2 s): interim NB22/NB23 with lower-thirds, final N4.
2. Shot 28 (tally, William's named card): RS07 reaction. Done in a minute.
3. Shots 78 to 80 (Empedocles, 13.4 s of text): archive image and citation chain.
4. Shots 76 and 77 (arrows, 9.5 s): cutouts and skull.
5. Shots 85 and 86 (Aguirre, Buxton, 8.4 s) and 81 (Witton): N3 with lower-thirds.
6. Shot 96 (Burkert, 6.3 s): N5.
7. Shots 70 and 74 (Mayor): NB21 and N3.
8. Shots 8 and 9 (roadmap, 6.2 s): triptych.
9. End section: 121, 123, 133, 134, 135, 140 (about 28 s): all T1 or T2 using existing images.
10. Shots 4 and 58 (Abel, 10.8 s): N1.
Then: the five chapter cards, 57, 62, 83, 84, 116, 38, 145 to 147.

**Fast first draft for William:** items 2, 4, 8, 9, the chapter cards and the T1/T2 parts of 1, 3, 5 to 7 need no new generation (all existing images), so a second render can follow straight after code changes. Generate N4 first (highest value, 40 and 90), then N2, N3, N1, N5, N6.

## 9. What I cannot judge

Motion (whether the ledger rows, stamps, counters and push-ins feel good at speed; I saw three stills per shot), audio (stings, voice, bed), caption timing against speech, legibility at phone size, and whether a given generated image will pass (the 42% reject rate applies). The narration per shot is aligned from `words.json` via `shots_timed.json`; I spot-checked it, I did not re-scan every word. Witton and Hing, Aguirre and Buxton, Mayor's book and Abel's German are second-hand in RESEARCH-V1, so the lower-third attributions should keep the paraphrase wording. I did not verify the Abel 1914 plate's licence.
