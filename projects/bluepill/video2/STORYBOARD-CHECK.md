# STORYBOARD-CHECK.md: the plan for "The Cyclops Case File" measured against FORMAT-BIBLE sections 2 and 3

Date 2026-11-13. Measured on `video2/storyboard.json` (the PLAN, not a render) against the final narration timings in `audio/words.json` (10:40.9 of voice; the plan runs to 10:41.8 with the end card). Nothing generated, uploaded or sent. Labels: **[V]** measured on the plan by script; **[E]** estimate.

How the plan was measured. Every shot start and every event `at` was resolved to seconds from `words.json` (the four TEXT-CHIP beats from `beats_timing.json`). A **picture change** is a shot start (hard cut). A **pop** is a sprite, label, counter, stamp, bubble or swap event that lands more than 0.2 s after its shot's cut (events placed on the cut are part of the picture change, not pops); pops within 0.1 s of each other count once. A **visible moment** is any picture change or non-SFX event, merged within 0.1 s. Chips and routes count as visible moments but not as pops. **Non-character shots** are those where no story character is on screen (the sprite flag `character:false` in each shot record). **White-dominant** is any shot on a white background (classes B, C and the white E counters).

## 1. Verification (task rules)
| Check | Result |
|---|---|
| `storyboard.json` parses | yes [V] |
| Every word index exists in `words.json` | yes, 0 errors [V] |
| Every event's word belongs to its shot's beat (or shared beats) | yes, 0 errors [V] |
| Shots referencing cut beats 77, 78, 79, 89, 91 | 0 [V] |
| Spoken beats without a shot | 0 of 112 [V] |
| TEXT-CHIP beats 59, 81, 97, 106 | placed at the `beats_timing.json` marker as a 2.5 s title label on the first shot of the next beat (each shares that shot; see section 5, exception E6) [V] |
| Events outside their shot's time window | 0 [V] |

## 2. Cadence against section 2 targets
| Measure | UF | Target | **Plan** | Pass |
|---|---|---|---|---|
| Picture changes per minute | 10.7 | 9.5-12 | **11.97** (128 cuts in 10.70 min) | yes |
| Pops, swaps, label appearances per minute | 7.4 | 6-8 | **14.4** | **no**, see exception E1 |
| All visible change moments per minute | 18.1 | 16-19 | **27.3** | **no**, same cause as E1 |
| Median gap between visible changes | 2.2 s | ≤ 2.5 s | **1.7 s** | yes |
| p90 gap | 6.7 s | ≤ 7 s | **4.5 s** | yes |
| Longest gap | 24 s | ≤ 15 s; one held beat 20-24 s | **11.4 s** (beat 54, the prayer plate, the scripted held beat) | yes |
| Gaps over 8 s | 1.3 per min | ≤ 1 per min | **1 in 10.7 min** (the held beat) | yes |
| Median shot / p90 shot | 4.2 / 12.3 s | 4-4.5 / ≤ 12 s | **4.9 s / 8.6 s**; longest 11.8 s | p90 yes; median 0.4 s long, see E2 |
| Frozen frames | 91% | ≥ 85% | plan has no camera moves; motion only in 2 route draws (4.2 s), 1 slide-out (0.15 s), 18 counter ticks and 14 stamp/pop eases of 0.2 s: about 2% of frames in motion [E] | yes |
| Frames in constant slow motion | 4% | ≤ 5% | 0% (no Ken Burns, no push) | yes |

**Density rules 1-5**
1. No sentence without a visible change: every beat has a cut or a pop [V]. No gap over 8 s except the held beat [V]; none over 15 s [V].
2. Non-character runs: longest 7.4 s (s076 skull plate, beat 61b); no run of more than two non-character shots [V]. Fixed during planning by putting a sprite on the long map, board and skull stretches (Odysseus beside the board at 3, 73 and 112-113; the elephant on the Sicily map at 61a; Polyphemus on the Etna map at 90; Thucydides on the night volcano at 93; the crew sprite at the Lion Gate at 102; Odysseus on the world map at 109) and by splitting the two 9-11 s skull beats (61, 69) into a character half and a plate half.
3. New picture at least every 12 s: longest shot 11.8 s [V]. New event at least every 7 s: one gap of 11.4 s, the held beat [V].
4. Pops land on word onset (`off` 0 by default; the build adds 0-0.15 s). The five 0.6 s stamp lead-ins (80, 96, 105, 113) and the two scripted holds (20, 119) use negative offsets so the picture is in place before the word.
5. One idea per pop: no two labels within 0.5 s except the paired place labels at beat 99 (TIRYNS, MYCENAE, 0.8 s apart) and the counter-plus-prop pairs at 103, which land together as one moment on purpose [V].

## 3. Class shares against section 3 targets (runtime 641.8 s)
| Class | Target | Target s | **Plan s** | **Plan %** | Pass |
|---|---|---|---|---|---|
| A. Painted scene, character-led | 53% | 340 | **275.0** | **42.8%** | **no** (E3) |
| B. White cutaway | 23% | 148 | **184.8** | **28.8%** | **no** (E3) |
| C. Text beside a character | 5% | 32 | **43.5** | **6.8%** | near |
| D. Map | 11% | 71 | **40.8** | **6.4%** | low (E4) |
| E. Counter or prop card (incl. the case board) | 4% | 26 | **59.3** | **9.2%** | **no** (E5) |
| F. Inset or diagram (skull plate, Greek line, Homer inset) | 3% | 19 | **34.4** | **5.4%** | high (E5) |
| G. Title card (black cuts, end card) | ≤ 1% | 6 | **4.1** | **0.6%** | yes |
| **Text, map, diagram only (D+E+F+G)** | ≤ 19%, cap 22% | | **138.6** | **21.6%** | under the cap, over the target (E5) |
| Pure text cards | cap 2% | | 0 | 0% | yes (the end card is 1.4 s) |
| White-dominant frames | 15-25% | | 251.5 | **39.2%** | **no** (E3) |
| Near-black frames (black cuts, NB11) | ≤ 8% | | 8.6 | 1.3% [E] | yes |
| Shots carrying text (label, bubble, counter, stamp or chip) | 40-45% | | 72 of 128 | **56%** | high; 18 chips are 14 points of it (E1) |

By section [V]: cold open A 42 / B 27 / E 31; Act 1 A 48 / B 43 / D 4 / F 3; the turn A 11 / E 52 / F 38; suspect 1 A 17 / B 17 / C 36 / E 11 / F 16; suspect 2 A 61 / B 23 / D 11; suspect 3 A 75 / B 4 / C 6 / E 15; suspect 4 A 22 / B 8 / D 36 / E 28; verdict A 37 / B 50.

## 4. What was fixed in the plan before this report
First draft of the plan measured 13.7 cuts per minute, 31 pops per minute, text on 81% of shots, 11 non-character runs over 8 s and 24% text-only. Changes made: 18 shots merged (bowl cuts at 29 became pops; 19-20, 32-33, 34-35a, 44-45, 50-51, 57-58, 62b-63, 112-113, 115-116, 118-119 share a picture; the four chip-beat frame fills ride the next shot); 41 labels and bubbles that the script's visual notes do not ask for were removed; sprites that the note places at the cut are on the cut; a character was put into every map, board and skull stretch longer than 8 s; three white cutaways the notes do not fix as white moved onto plates (66 cave, 67 beach cave, 87-88 forge and smith plates); the 20:1 counter at 29 moved onto the wine-offer plate NB08.

## 5. Exceptions, each with the beats involved
- **E1. Pops 14.4 per minute against 6-8; visible moments 27 against 16-19.** Cause: the script's visual notes ask for a named pop in nearly every beat (cheese wheels one at a time, bowls one per word, four pins and a counter at 109, four props at 117, three icons at 120, the three stamps at 107, the skull rings at 61) and 18 source chips are a separate obligation (section 8 accuracy rule). Every pop in the plan traces to a visual note, a numeral, a name or a verdict. The cut rate is on target, so the surplus is pops, not pictures. Recommended handling: keep the plan for the animatic (G3); if it feels busy, thin first the prop pops that do not carry a number or a name (the lamb and sheep at 8 and 26 are already gone; next: the second cheese wheel at 8, the water drops at 29, the dust puff at 66, the pointer at 102, the three stamps re-landing at 114). Thinning 40 pops brings the plan to about 10.6 per minute; reaching 8 needs about 70 removed, which would cut below what the script asks for. **William's call.**
- **E2. Median shot 4.9 s against 4-4.5 s.** Because dialogue lines on white run to the attribution ("said Odysseus") that George speaks. Dropping the 15 bare attributions (REPASS-FABLE section 3, item 1) would also fix this; not a storyboard change.
- **E3. Class A 43% against 53%; class B 29% against 23%; white-dominant 39% against 15-25%.** The V4 script places 35 character lines and 7 narrator gags on white cutaways by name ("white cutaway", "white;") and the storyboard follows the notes. The bible's own B + C targets (28%) already exceed its white-dominant ceiling (25%), so the ceiling cannot be met while the B target is met; the two targets need reconciling. Levers if William wants more paint: (a) play the dialogue pairs at 14-16, 30-33 and 49-53 on the cave and shore plates with sprites (about 45 s moves B to A, white to about 32%); (b) a tinted cutaway ground (cream or the plate's dominant colour) instead of pure white, which the bible's colour rule would also accept (mean luminance stays above 105). Recommended: (b) for all B shots plus (a) for 49-53 only.
- **E4. Maps 6.4% against 11%.** The script asks for five map moments (6, 55, 61a, 90, 109 plus the frame-4 world map at 106-107). Each is held to the sentence that earns it. No change recommended; padding maps would raise the text-only share.
- **E5. Class E 9.2% against 4%, F 5.4% against 3%, text-only 21.6% against a 19% target (22% cap).** The case board is this episode's spine: the script visits it at 3, 13, 36, 44 (pings), 57-58, 73, 80, 96, 105, 107, 112-113, 114. The skull plate is the evidence for suspect 1 and appears at 61, 65, 69. Each visit is at the length of its sentence. Under the hard cap; over the target by 2.6 points. Lever: move the Odysseus-beside-the-board sprite into the board picture permanently (a "detective" inset) and reclassify nothing; or drop the board ping at 13 (OPEN-DECISIONS default says drop if it bothers).
- **E6. TEXT-CHIP beats have no separate shot.** The audio gap at each chip marker is 0.45 s, too short to read a title on its own picture; the frame-fill cut lands at the marker and the title rides the next beat's first shot for 2.5 s (chip rule). Beats 59, 81, 97, 106 therefore share shots s075, s096, s113, s124.
- **E7. The one held beat is beat 54** (s068, the prayer plate, 11.4 s, no pops): the script's "only grave moment". Within the allowance.
- **E8. Beat 2's second sentence has no pop** ("So where did he come from?"): the note says "no text" on the Cyclops close-up; the cut on "A giant" serves the whole beat.

## 6. Checks still open (not measurable on a plan)
Luminance means, true white-dominant pixel counts, fringe checks and pop lag are measured on the render (section 8). The style names used in the JSON (`impact`, `place`, `bubble`, `crossout`, `chip_title`, `board`, `title`) and the accent colours are placeholders until gate G2 picks the face and colour (OPEN-DECISIONS section 3).

## Appendix: shot list (id | beats | class | picture | start s | length s | note)
| id | beats | class | picture | start | len | note |
|---|---|---|---|---|---|---|
| s001 | 1 | A | NBG01.png | 0.0 | 3.6 | cliff-cave exterior; Odysseus + 12 tiny crew cutouts walking in |
| s002 | 1 | E | NBG01.png | 3.6 | 1.5 | same plate, counter ticks 12 to 6 on the hard cut; cave mouth only (crop 1.1x) |
| s003 | 2 | A | NB01.png | 5.2 | 5.0 | Cyclops close-up (NB01), no text, held for the whole beat |
| s005 | 3 | E | board_base.png | 10.2 | 8.4 | case board (NEW), four empty frames; Odysseus sprite beside it so a character is on screen |
| s006 | 4 | B | white | 18.6 | 8.8 | disclosure: Odysseus, Polyphemus, crewman in a row; Polyphemus waves |
| s007 | 5 | A | NBG01.png | 27.3 | 5.2 | cave exterior; cheese wheel pops beside the cave on "cheese" |
| s008 | 6 | D | map_med_west.png | 32.5 | 7.6 | map: ship icon beside an unlabelled coast, ? pin |
| s009 | 7 | A | NBG01.png | 40.1 | 5.0 | cave exterior; Odysseus + 12 crew walking toward the mouth |
| s010 | 8 | A | NBG02.png | 45.2 | 4.1 | cave interior held still; cheese wheels pop one at a time |
| s011 | 9 | B | white | 49.3 | 3.0 | crew sprite points at the exit |
| s012 | 10 | B | white | 52.3 | 4.6 | Odysseus confident; bubble pops whole |
| s013 | 11 | A | NBG02.png | 56.9 | 4.9 | cave; Odysseus arms crossed; gift basket pops on the floor |
| s014 | 12 | A | NBG02_mouth.png | 61.8 | 5.5 | cave mouth from inside; Polyphemus cutout enters as a dark shape |
| s015 | 13 | A | RC11.png | 67.3 | 7.2 | Cyclops pushes boulder (cy_v4_s11); counter "22 WAGONS" pops |
| s016 | 14 | B | white | 74.5 | 4.5 | Polyphemus leaning down, one big eye |
| s017 | 15 | B | white | 79.0 | 6.5 | Odysseus hands open |
| s018 | 16 | B | white | 85.4 | 4.9 | Polyphemus scornful; lightning icon pops and is cut away |
| s019 | 17 | A | NB05.png | 90.3 | 5.9 | giant back against the fire, cowering silhouettes (NB05); counter 12 MEN in the corner ticks to 10 on "supper" |
| s021 | 18 | B | white | 96.2 | 3.7 | Odysseus alone, sword half drawn |
| s022 | 19,20 | B | white | 99.9 | 2.7 | beats 19-20 share: Odysseus thinking; 22 WAGONS pops back; sword lowered on Ah., hold 1.5 s |
| s024 | 21 | E | NB05.png | 102.6 | 2.5 | counter ticks 10 to 8 on the hard cut; hold on 8 |
| s025 | 21 | A | NB04.png | 105.1 | 3.2 | Odysseus, hand on sword hilt, eyes on the dark ("we will spare you") |
| s026 | 22 | A | NB06.png | 108.3 | 5.4 | Odysseus small beside the olive club (scale) |
| s027 | 22 | B | white | 113.8 | 4.7 | prop cutaways: club, sharpened length, flames |
| s028 | 23 | B | white | 118.5 | 4.0 | five sprites in a huddle, four hands drawing straws |
| s029 | 24 | B | white | 122.5 | 2.4 | crew sprite, sweat mark |
| s030 | 25 | B | white | 124.9 | 2.1 | Odysseus, flat expression |
| s031 | 26 | A | NBG02.png | 127.0 | 5.6 | cave; stake prop then dung heap pops over it |
| s033 | 27 | A | NB05.png | 132.5 | 3.6 | giant back against the fire (evening); counter ticks 8 to 6 on "Six"; hold 1 s |
| s034 | 28 | B | white | 136.2 | 6.1 | Odysseus holds out a bowl, deadpan |
| s035 | 29 | A | NB08.png | 142.3 | 6.1 | wine offer two-shot (NB08); counter 20 : 1 pops with a row of water-drop icons |
| s036 | 29 | A | NB09.png | 148.4 | 3.2 | Cyclops drinks wine, profile (NB09); three bowls stack in the corner, one pop per word (stop-motion, no extra  |
| s039 | 30 | B | white | 151.6 | 5.1 | Polyphemus flushed and wobbling |
| s040 | 31 | B | white | 156.7 | 2.3 | Odysseus pops in on "Nobody"; NOBODY label |
| s041 | 32,33 | B | white | 159.0 | 7.9 | beats 32-33 share: Polyphemus beams; Odysseus swaps to flat/unamused; hold 0.4 s after "friends first" |
| s043 | 34,35 | A | NB10.png | 167.0 | 5.5 | beats 34-35a share: giant asleep, dark (NB10); LAST label over Odysseus; stake prop pops on "fire" |
| s044 | 35 | A | NB11.png | 172.5 | 1.4 | "Then he puts it in the eye": glowing stake, giant a dark mass (NB11) |
| s045 | 35 | G | black | 173.8 | 1.2 | hard cut to black for half a second |
| s046 | 36 | F | white | 175.1 | 5.0 | axe head in a trough with steam (NP03), one hiss |
| s048 | 37 | A | NBG03.png | 180.0 | 5.2 | night hills; three dark Cyclops silhouettes against the moon; one bubble |
| s049 | 38 | A | NB12.png | 185.3 | 5.6 | Cyclops at cave mouth, hand over eye, shouting; smug Odysseus inset pops in and out |
| s050 | 39 | A | NBG03.png | 190.8 | 8.1 | silhouettes turn and leave; hold 0.4 s after "you" |
| s051 | 40 | B | white | 199.0 | 4.9 | three Cyclops sprites, one shrugs |
| s052 | 41 | A | NB13.png | 203.9 | 7.0 | rams bound in threes leaving at dawn |
| s053 | 42 | A | NB14_crop_left55.png | 210.9 | 2.4 | Odysseus under the ram; giant hand on the back |
| s054 | 42 | A | NB15.png | 213.3 | 3.1 | giant hands on wool, face out of frame |
| s055 | 43 | F | white | 216.4 | 2.2 | the belly, untouched: ram prop with Odysseus feet showing |
| s056 | 44,45 | B | white | 218.6 | 11.8 | beats 44-45 share: Polyphemus softened face, patting a ram sprite; hold 0.4 s on "last today"; inset of the ra |
| s058 | 46 | A | NBG04.png | 230.4 | 3.8 | calm dawn sea, ship cutout (NP04) |
| s059 | 47 | A | RS10.png | 234.2 | 3.3 | Odysseus shouting on ship (s10) as the jeer |
| s060 | 47 | A | NB17.png | 237.5 | 3.6 | Cyclops from behind on the cliff top, arm raised |
| s061 | 48 | A | NB18.png | 241.1 | 3.5 | boulder splash beside the stern (splash frame) |
| s062 | 48 | A | NBG04.png | 244.6 | 3.2 | ship cutout swaps to the listing pose |
| s063 | 49 | B | white | 247.8 | 5.0 | two small crew sprites, hands clasped |
| s064 | 50,51 | B | white | 252.7 | 9.4 | beats 50-51 share: Odysseus on tiptoe, chin up; ODYSSEUS label pops; hold 0.5 s after "Of Ithaca."; NOBODY ret |
| s066 | 52 | B | white | 262.1 | 10.7 | Polyphemus arms wide; gift-box prop pops |
| s067 | 53 | B | white | 272.8 | 6.1 | Odysseus arms folded |
| s068 | 54 | A | NB_prayer.png | 278.9 | 11.4 | NEW plate: Polyphemus dark silhouette on the shore at dusk, hands raised; the one grave moment |
| s069 | 55 | G | black | 290.3 | 1.5 | hard cut to black; wave sound |
| s070 | 55 | D | map_med_loop.png | 291.8 | 3.5 | sea map; route loops back on itself; small Odysseus sprite on the map |
| s071 | 56 | F | white | 295.3 | 6.6 | magnifier over a real Greek line (Perseus, public domain); eye word enlarged |
| s071b | 56 | A | NB01.png | 301.9 | 1.9 | "He says the eye": Cyclops close-up (NB01), ring on the eye, chip |
| s072 | 57,58 | E | board_base.png | 303.7 | 9.1 | beats 57-58 share: board pops, four frames with ?; elephant sprite beside it; CASE OPEN stamp on 58 |
| s075 | 59,60 | C | white | 312.8 | 9.2 | TEXT-CHIP 59 + beat 60 share: frame 1 opens to white with the dwarf elephant sprite; SUSPECT 1 title rides 2.5 |
| s076a | 61 | D | map_sicily.png | 322.1 | 3.9 | Sicily and Malta map; bone pins pop; dwarf elephant sprite on the map (character) |
| s076 | 61 | F | skull_front_pd.png | 325.9 | 7.4 | public-domain skull plate (not generated); two small circles then one large |
| s077 | 62 | A | NB20.png | 333.3 | 7.3 | anonymous sailor sheltering in a beach cave with a fire (NB20) |
| s078 | 62,63 | A | NBG02.png | 340.6 | 7.3 | beats 62b-63 share: hard cut to the cave interior, held still; sailor sprite pops in at the mouth with a torch |
| s080 | 64 | B | white | 347.9 | 1.9 | sailor sprite, one hand up, torch |
| s081 | 65 | F | skull_front_pd.png | 349.7 | 4.5 | front-view skull plate; ring pops around the nasal opening on "eye" |
| s082 | 66 | A | NBG02.png | 354.2 | 0.8 | cave plate: sailor swaps to alarmed, slides out left, dust puff |
| s083 | 67 | A | NB20.png | 355.0 | 3.5 | beach cave (NB20): IMAGINED stamp lands on the sailor; skull plate pops beside him |
| s084 | 68 | B | white | 358.5 | 1.4 | sailor squints at the skull plate, head tipped |
| s085a | 69 | B | white | 359.9 | 4.0 | sailor points at the skull plate beside him; NASAL CAVITY label |
| s085 | 69 | F | skull_front_pd.png | 363.9 | 5.7 | skull plate full; eye icon pops over the hole on "eye" |
| s086 | 70 | C | white | 369.6 | 8.9 | elephant sprite with a crossed-out ship icon; chip Discover |
| s087 | 71 | C | white | 378.5 | 7.4 | book prop with title text only (no cover art); chip Mayor, Stanford; Odysseus listens |
| s088 | 72 | C | white | 385.9 | 6.7 | only WE JUST CAN'T PROVE THAT in large lettering; chip for the line; Odysseus stays |
| s089 | 73 | E | board_base.png | 392.6 | 9.7 | board; the elephant portrait jitters two frames on "friend"; fossil-bone prop pops on "giants"; Odysseus sprit |
| s091 | 74 | B | white | 402.4 | 9.4 | Empedocles sprite (NEW) with bone bubble; tag THE FAMOUS STORY |
| s092 | 75 | B | white | 411.8 | 2.8 | sailor with magnifier opens drawer ANCIENT SOURCES; empty |
| s093 | 76 | C | white | 414.5 | 7.9 | empty SOURCE: slip; A MODERN MYTH lettered; chip Colavito; sailor stays |
| s094 | 80 | E | board_base.png | 422.4 | 3.1 | UNPROVEN stamp on the elephant frame (0.6 s beat before "Possible") |
| s096 | 81,82 | A | NB_forge.png | 425.5 | 3.8 | TEXT-CHIP 81 + beat 82 share: frame 2 opens to the NEW forge plate (anvil in plate); SUSPECT 2 title rides 2.5 |
| s097 | 83 | A | NB_forge.png | 429.3 | 6.5 | three smith sprites pop in turn on Thunder, Lightning, Bright; chip with the three names for 2 s |
| s098 | 84 | A | NB23.png | 435.8 | 1.9 | tongs, hammer, thunderbolt on the anvil (NB23) |
| s099 | 84 | B | white | 437.6 | 3.0 | Book Nine Cyclopes shrug Zeus off: lightning icon returns and is cut away |
| s100 | 85 | A | NB_forge.png | 440.7 | 3.2 | Polyphemus in the doorway with a lamb, awkward half wave; smiths stare |
| s101 | 86 | B | white | 443.8 | 0.7 | one smith sprite, flat, hammer lowered |
| s102 | 87 | A | NB_forge.png | 444.6 | 2.9 | forge plate: three smith sprites hold up three hammers |
| s103 | 88 | A | NB22.png | 447.4 | 7.6 | Cyclops as smith (NB22), one eye ringed on "eye"; chip Hesiod |
| s104 | 90 | D | map_sicily.png | 455.0 | 8.6 | map with an Etna icon and smoke; small Polyphemus sprite at the address; chip Euripides |
| s105 | 92 | B | white | 463.5 | 9.0 | Thucydides sprite (NEW), palms up; the quote lettered 2.5 s; chip 6.2 |
| s106 | 93 | A | NBG06.png | 472.5 | 7.1 | Aeolian crater with glowing vent (night); small Thucydides sprite in the corner for "he records" |
| s107 | 93 | A | NBG06_day.png | 479.7 | 1.4 | day cut with a smoke plume (NEW day variant) |
| s108 | 94 | A | NBG06_day.png | 481.0 | 5.7 | hold on the volcano; smith sprite pops in at the base and tips his hat |
| s109 | 95 | A | NB24.png | 486.7 | 6.5 | seated Cyclops singing on a cliff (NB24) |
| s110 | 95 | B | white | 493.2 | 5.0 | lovesick Polyphemus with heart prop; ONE EYEBROW across the forehead |
| s111 | 96 | E | board_base.png | 498.2 | 3.6 | PLAUSIBLE stamp on the smiths frame |
| s113 | 97,98 | A | NBG07.png | 501.8 | 4.5 | TEXT-CHIP 97 + beat 98 share: frame 3 opens to the cyclopean wall (NBG07); SUSPECT 3 title rides 2.5 s; Odysse |
| s114 | 99 | A | NBG07.png | 506.3 | 6.4 | wall of huge blocks, Odysseus tiny at the foot |
| s115 | 100 | B | white | 512.7 | 2.4 | one small crew sprite at the foot of a block, head tipped back |
| s116 | 101 | A | NB25.png | 515.0 | 8.0 | two mules straining at a huge stone (NB25); counter 2 MULES; chips |
| s117 | 102 | A | NBG08.png | 523.0 | 7.6 | Mycenae Lion Gate (NBG08); crew sprite small at the gate; chip Pausanias 2.16 |
| s118 | 103 | E | white | 530.6 | 6.4 | split counter: 22 WAGONS pops left on "twenty-two", 2 MULES pops right on "two" |
| s120 | 103 | C | white | 537.0 | 3.4 | Odysseus beside the two counters: GIANTS IN WAGONS AND MULES |
| s121 | 104 | A | NBG08.png | 540.4 | 10.4 | Lion Gate; c. 1250 BC counter; crowd of workers pops; CYCLOPEAN MASONRY on the wall |
| s122 | 105 | E | board_base.png | 550.8 | 2.1 | REAL stamp on the walls frame (0.6 s beat before "The wall") |
| s122b | 105 | A | NBG07.png | 552.9 | 6.1 | wall plate with Odysseus tiny at the foot for the two hedge sentences |
| s124 | 106,107 | D | board_base.png | 559.0 | 6.7 | TEXT-CHIP 106 + beat 107 share: frame 4 fills the screen (world map); SUSPECT 4 title rides 2.5 s; the three e |
| s126 | 108 | A | NB05.png | 565.7 | 4.5 | montage 1 of 3: cave with the giant silhouette (Act 1 art) |
| s127 | 108 | A | NB11.png | 570.3 | 3.1 | montage 2: the stake in the fire |
| s128 | 108 | A | NB13.png | 573.4 | 1.4 | montage 3: the sheep escape |
| s129 | 109 | D | map_world.png | 574.7 | 8.0 | world map; counter to 200+; pins on each place; chip Hackman; small Odysseus sprite in the corner |
| s130 | 110 | F | white | 582.7 | 3.0 | small Homer plate with the folktale marker to its left and an OLDER arrow |
| s131 | 111 | B | white | 585.7 | 3.2 | Odysseus pops in on "first", flat expression, same pop as beat 31 |
| s132 | 112,113 | E | board_base.png | 588.9 | 11.4 | beats 112-113 share: board with Odysseus sprite beside it; elephant frame dims on "skull"; PROBABLY OLDER stam |
| s134 | 114 | E | board_base.png | 600.3 | 1.4 | the full board |
| s135 | 114 | A | NB22.png | 601.7 | 1.9 | frame 2 full: Cyclops as smith (NB22); PLAUSIBLE stamp re-lands on "Hesiod" |
| s136 | 114 | A | NBG07.png | 603.5 | 2.0 | frame 3 full: the wall (NBG07) with Odysseus tiny; REAL stamp on "Pausanias" |
| s137 | 114 | D | map_world.png | 605.5 | 2.6 | frame 4 full: world map with pins and the 200+ counter; PROBABLY OLDER stamp |
| s138 | 114 | B | white | 608.1 | 3.8 | frame 1: the skull beside the sailor sprite; UNPROVEN stamp; holds into 115 |
| s139 | 115,116 | B | white | 611.9 | 5.5 | beats 115-116 share: Cyclops sprite shrugs on "no"; swaps to wounded on "Rude." |
| s141 | 117 | B | white | 617.4 | 7.4 | four props pop in a row: anvil, wall block, scroll, skull |
| s142 | 118,119 | B | white | 624.8 | 4.1 | beats 118-119 share: empty stage; ? pops on "from?"; hold 0.6 s; Odysseus pops in on "Nobody." (same pop as be |
| s144 | 120 | A | NBG04.png | 628.9 | 5.4 | ship leaves a calm sea; bag, wand, whirlpool icons pop on their words |
| s145 | 121 | A | RS08.png | 634.4 | 6.0 | Odysseus on the night beach (s08), calm |
| s146 | 121 | G | black | 640.4 | 1.4 | hard cut to black on "father"; sea sound; end card |
