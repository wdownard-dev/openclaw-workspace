# SHOTLIST-V1-RETIMED.md: video 1, "The Cyclops Was Real? What the Myth Is Hiding"

Nothing uploaded or sent. Shot structure, numbering and art notes are unchanged from `SHOTLIST-V1.md` (see it for characters, light, camera and drift notes). Only the timing changed: every narrated shot now starts on the first word of its line in the real ElevenLabs track (`audio/narration.wav`, word times in `audio/words.json`); the first shot after a chapter card starts when the card ends and absorbs the pause before the voice; each shot ends where the next begins. Machine-readable version: `shots_timed.json`.

## Summary

- **Runtime 10:19 (619.1 s)**, down from the 11:01 estimate and 11 s under William's accepted 10:30. Voice only: 605 s of speech across 13 paragraph takes, 154.1 wpm from first to last word including pauses and cards (153.6 wpm over the whole runtime).
- **147 shots** (142 narrated plus 5 silent chapter cards of 2.0 s, each with a synthesised ambient sting). **14.25 cuts per minute** (mean narrated shot 4.3 s, median 4.4 s, shortest 1.4 s, longest 7.9 s).
- **Flags:** 14 shots under 2.5 s, 0 over 8 s. Every short one is a one-line or half-line beat that the old estimate padded to a 3.2 s floor; the voice does not.
- Inserted silence: 0.40 s lead-in, 0.35 s between paragraphs (0.40 s between cold open and stakes), and at each chapter a single 2.0 s card window (was 3.3 s of silence) that carries the sting (`audio/stings/`, `audio/stings_track.wav`); the card shot is exactly that window and the next voice starts 0.05 s after it ends. End card holds at least 4 s (narration plus tail).
- **Cut placement:** cuts sit exactly on word onsets. Editors usually pull a cut 2 to 4 frames early (0.07 to 0.13 s) so the picture lands just before the word; do that in the assembly, not here.

## Chapters (real times; replace the estimates in SCRIPT-V1.md and the description)

| Chapter | Card/start (real) | Old estimate |
|---|---|---|
| Cold open | 0:00.0 | 0:00 |
| Stakes | 0:22.4 | 0:23 |
| 1. The poem as Homer tells it | 0:39.7 | 0:42 |
| 2. The skull | 3:59.0 | 4:16 |
| 3. The other Cyclopes | 6:14.4 | 6:39 |
| 4. What we can and cannot say | 8:32.0 | 9:04 |
| Verdict and next | 9:38.4 | 10:18 |

YouTube chapter list (card start = chapter timestamp; paste after William listens): 0:00 Cold open; 0:39 The poem as Homer tells it; 3:59 The skull; 6:14 The other Cyclopes; 8:32 What we can and cannot say; 9:38 Verdict and next

## Flagged shots

**Over 8 s: none.** Longest narrated shot is 7.9 s.

**Under 2.5 s:**

| # | start | sec | narration | suggestion |
|---|---|---|---|---|
| 13 | 0:47.1 | 2.2 | So this is the hero's own account. | same image as the previous shot (12); fold into one hold of 4.9 s |
| 15 | 0:54.0 | 1.8 | On a cliff stands a cave, | same image as the next shot (16); fold into one hold of 6.7 s |
| 17 | 1:00.7 | 1.4 | The owner is out. | same image as the previous shot (16); fold into one hold of 6.3 s |
| 29 | 1:50.4 | 2.1 | He finds the giant's own club, | same image as the next shot (30); fold into one hold of 5.6 s |
| 62 | 4:25.2 | 2.1 | and island life shrank them. | same image as the previous shot (61); fold into one hold of 6.0 s |
| 64 | 4:30.3 | 2.2 | Now look at the skull from the front. | same image as the next shot (65); fold into one hold of 5.6 s |
| 92 | 6:32.2 | 2.4 | And Hesiod is the one who says it plainly: | same image as the next shot (93); fold into one hold of 5.9 s |
| 106 | 7:36.6 | 1.5 | There is a third strand, | same image as the next shot (107); fold into one hold of 4.4 s |
| 124 | 8:49.0 | 2.5 | Dwarf elephants really lived on those islands, | same image as the next shot (125); fold into one hold of 5.4 s |
| 128 | 9:04.2 | 2.0 | That does not rule out the skull. | same image as the next shot (129); fold into one hold of 4.8 s |
| 130 | 9:09.0 | 2.1 | Now, what we cannot say. | same image as the next shot (131); fold into one hold of 7.0 s |
| 135 | 9:31.4 | 1.7 | and none has proof. | same image as the previous shot (134); fold into one hold of 5.8 s |
| 138 | 9:40.4 | 2.0 | So, was the Cyclops real? | no same-image neighbour: keep as a deliberate short beat, or hold the previous frame through this line |
| 142 | 9:54.4 | 2.1 | and walls you can still touch. | no same-image neighbour: keep as a deliberate short beat, or hold the previous frame through this line |

## Listen first (I cannot judge a voice by ear; these are the spots most likely to be wrong)

Names are sent to the TTS as phonetic respellings (the saved script is untouched). Timestamps are on the final timeline. `rel` is seconds per syllable relative to the narration average (1.0 = normal; below 0.6 is hurried, above 1.5 is drawn out).

| time | name | sent to TTS as | dur | rel |
|---|---|---|---|---|
| 1:12.8 | Polyphemus. | Pollifeemus. | 1.02 s | 1.01 |
| 4:07.6 | Othenio | Oh-TAY-nee-oh | 1.02 s | 1.01 |
| 4:08.7 | Abel | AH-bel | 0.67 s | 1.33 |
| 5:37.8 | Empedocles | Em-peddokleez | 0.88 s | 0.87 |
| 6:04.7 | Aguirre | Ah-gheereh | 0.60 s | 0.79 |
| 6:24.5 | Brontes, | Bron-teez, | 0.79 s | 1.55 |
| 6:25.4 | Steropes, | Stair-oh-peez, | 1.00 s | 1.31 |
| 6:26.7 | Arges. | Ar-geez. | 0.71 s | 1.39 |
| 6:47.3 | Burkert | Boor-kert | 0.67 s | 1.33 |
| 7:08.5 | Thucydides | Thoo-sididdeez | 0.82 s | 0.81 |
| 7:27.7 | Theocritus | Thee-ockritus | 0.79 s | 0.78 |
| 7:42.2 | Tiryns, | Tie-rinz, | 0.70 s | 1.37 |
| 7:49.9 | Pausanias, | Paw-sayneeus, | 1.03 s | 1.36 |
| 8:21.9 | Aci | Ah-chee | 0.32 s | 0.64 |
| 8:22.3 | Trezza | Tret-sah | 0.59 s | 1.17 |

Names left as written (the model usually handles them): Buxton, Witton, Mayor, Hesiod, Euripides, Mycenae, Virgil, Etna, Aeolian, Cyclopes, Odysseus, Poseidon, cyclopia. Check Cyclopes (sy-KLOH-peez) at 0:50.4 and Buxton at 6:06.1.

**Othenio Abel (4:07.6) was re-recorded** (chunk 6 only): the first take was heard as "oh-ten-e-o"; the name is Austrian/German, now sent as `Oh-TAY-nee-oh AH-bel`. Alignment only confirms the syllables are spread plausibly (1.02 s for four syllables, stress on the second); the second Abel in that paragraph and the one in the Aeolian-bones paragraph (chunk 8, still `Ah-bel`) should be checked for consistency. If it still sounds wrong, the fallback respelling is `Oh-TAY-nyo AH-bel` (one more call on chunk 6).

**Chapter-card transitions (new, 2.0 s each with a synthesised low-pad sting at about -29 LUFS):** 0:39.7; 3:59.0; 6:14.4; 8:32.0; 9:38.4. Check that the sting is restrained, fades out before the first word, and that the first word is not clipped.

Hedge phrases (should be flat, not stressed): presumably 2:39.2; may 5:12.7; Perhaps 5:27.8; bluntly 5:48.8; baseless 5:52.7; plausible 6:09.6; may 6:49.8; implies 8:48.0; hypothesis 9:34.3; plausible 9:35.7; unproven 9:37.1; may 9:57.1; suspect 9:59.1.

Paragraph takes generated at a speed above 1.0 to even out the pace (the voice slowed on its own in the later chapters): chunk 8 (speed 1.05, 5:32.5 to 6:14.4), chunk 9 (1.06, 6:16.4 to 7:36.3). If either sounds hurried, re-take it at 0.97 and accept a few seconds more runtime.

## Shot list (real times)


### Cold open

| # | start | end | sec | flag | narration | type | asset | old start / sec |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:00.0 | 0:04.5 | 4.5 |  | Hundreds of thousands of years ago, an elephant lived on Sicily. | map | CODE:map-med | 0:00.0 / 4.4 |
| 2 | 0:04.5 | 0:07.6 | 3.1 |  | It stood less than a metre tall at the shoulder. | white | NP01 + odysseus_A cutout | 0:04.4 / 4.0 |
| 3 | 0:07.6 | 0:11.5 | 3.9 |  | Its skull has one enormous hole in the middle of its face. | diagram | CODE:skull-front (DG-01) | 0:08.4 / 4.8 |
| 4 | 0:11.5 | 0:17.3 | 5.8 |  | In 1914, a palaeontologist argued that hole is where the Cyclops came from. | card | CODE:card-abel-year | 0:13.2 / 5.2 |
| 5 | 0:17.3 | 0:22.3 | 5.0 |  | The idea is now everywhere. Today, we check what is under it. | baked | NB01 | 0:18.4 / 4.8 |

### Stakes

| # | start | end | sec | flag | narration | type | asset | old start / sec |
|---|---|---|---|---|---|---|---|---|
| 6 | 0:22.3 | 0:28.1 | 5.8 |  | If it is right, one of literature's most famous monsters began as an honest mistake. | diagram | CODE:split-skull-eye (DG-02) | 0:23.2 / 6.0 |
| 7 | 0:28.1 | 0:32.8 | 4.7 |  | If it is wrong, we have been passing on a good story with nothing underneath. | bakedX | X:NB01 + CODE:overlay-evidence | 0:29.2 / 6.0 |
| 8 | 0:32.8 | 0:36.0 | 3.2 |  | So we will go slowly: the poem first, | card | CODE:ledger-roadmap | 0:35.2 / 3.2 |
| 9 | 0:36.0 | 0:39.7 | 3.6 |  | then the bones, then the people who disagree. | card | CODE:ledger-roadmap | 0:38.4 / 3.2 |

### 1. The poem as Homer tells it

| # | start | end | sec | flag | narration | type | asset | old start / sec |
|---|---|---|---|---|---|---|---|---|
| 10 | 0:39.7 | 0:41.7 | 2.0 |  | (silent chapter card) | title card | CODE:chapter-card | 0:41.6 / 2.5 |
| 11 | 0:41.7 | 0:44.4 | 2.7 |  | Homer tells it in Book Nine of the Odyssey, | baked | NB02 | 0:44.1 / 3.6 |
| 12 | 0:44.4 | 0:47.1 | 2.7 |  | and he lets Odysseus tell it himself. | bakedX | X:NB02 | 0:47.7 / 3.2 |
| 13 | 0:47.1 | 0:49.3 | 2.2 | short | So this is the hero's own account. | bakedX | X:NB02 | 0:50.9 / 3.2 |
| 14 | 0:49.3 | 0:54.0 | 4.7 |  | They reach the land of the Cyclopes, a place Homer never locates. | bakedR | RS08 | 0:54.1 / 4.8 |
| 15 | 0:54.0 | 0:55.8 | 1.8 | short | On a cliff stands a cave, | baked | NBG01 | 0:58.9 / 3.2 |
| 16 | 0:55.8 | 1:00.7 | 4.9 |  | full of sheep and goats. Odysseus takes twelve men to look. | bakedX | X:NBG01 | 1:02.1 / 4.4 |
| 17 | 1:00.7 | 1:02.1 | 1.4 | short | The owner is out. | cutout | NBG01 + cutouts | 1:06.5 / 3.2 |
| 18 | 1:02.1 | 1:07.1 | 5.0 |  | His men find racks of cheese, and suggest taking some and leaving. | cutout | NBG02 + cutouts | 1:09.7 / 4.8 |
| 19 | 1:07.1 | 1:12.0 | 4.9 |  | Odysseus refuses. He wants to meet the owner, in case there is a gift. | cutout | NBG02 + cutout | 1:14.5 / 5.6 |
| 20 | 1:12.0 | 1:17.0 | 5.0 |  | The owner is Polyphemus. Homer says he looks less like a man who eats bread, | bakedR | RC02 | 1:20.1 / 6.0 |
| 21 | 1:17.0 | 1:20.9 | 3.9 |  | than like a wooded peak, standing alone above the others. | baked | NB03 | 1:26.1 / 4.0 |
| 22 | 1:20.9 | 1:25.7 | 4.7 |  | He drives his flock inside, and rolls a stone across the entrance. | bakedR | RC11 | 1:30.1 / 4.8 |
| 23 | 1:25.7 | 1:30.0 | 4.4 |  | Homer says twenty-two four-wheeled wagons could not have moved it. | diagram | CODE:wagon-count (DG-03) | 1:34.9 / 4.0 |
| 24 | 1:30.0 | 1:34.8 | 4.7 |  | That stone is the real trap. Odysseus thinks of drawing his sword, | baked | NB04 | 1:38.9 / 4.8 |
| 25 | 1:34.8 | 1:40.0 | 5.2 |  | then realises that if he kills the giant, no one can ever open the door. | bakedR | RS09 | 1:43.7 / 6.0 |
| 26 | 1:40.0 | 1:43.2 | 3.2 |  | So he waits. Across three meals, | baked | NB05 | 1:49.7 / 3.2 |
| 27 | 1:43.2 | 1:46.9 | 3.7 |  | Polyphemus eats six of his men, two at a time. | bakedX | X:NB05 | 1:52.9 / 4.0 |
| 28 | 1:46.9 | 1:50.4 | 3.5 |  | Homer gives the detail. We will leave it out. | diagram | CODE:tally-six | 1:56.9 / 3.6 |
| 29 | 1:50.4 | 1:52.5 | 2.1 | short | He finds the giant's own club, | baked | NB06 | 2:00.5 / 3.2 |
| 30 | 1:52.5 | 1:56.0 | 3.5 |  | a green olive trunk the size of a ship's mast. | bakedX | X:NB06 | 2:03.7 / 4.0 |
| 31 | 1:56.0 | 2:00.9 | 4.9 |  | He cuts off a length, sharpens it, and hardens the point in the fire. | baked | NB07 | 2:07.7 / 5.6 |
| 32 | 2:00.9 | 2:05.6 | 4.7 |  | Then he offers Polyphemus wine, a gift from a priest of Apollo. | baked | NB08 | 2:13.3 / 4.8 |
| 33 | 2:05.6 | 2:10.3 | 4.6 |  | It is so strong that its owners mixed it with twenty measures of water. | diagram | CODE:mix-1-to-20 | 2:18.1 / 5.6 |
| 34 | 2:10.3 | 2:15.5 | 5.2 |  | The giant drinks three bowls, and asks for a name, promising a present. | baked | NB09 | 2:23.7 / 5.2 |
| 35 | 2:15.5 | 2:21.6 | 6.1 |  | Odysseus says his name is Nobody. The present is that Polyphemus will eat him last. | bakedX | X:NB08 + CODE:outis-overlay | 2:28.9 / 6.0 |
| 36 | 2:21.6 | 2:25.5 | 3.9 |  | It is not much of a gift, but it buys time. | baked | NB10 | 2:34.9 / 4.4 |
| 37 | 2:25.5 | 2:31.1 | 5.7 |  | Now the stake goes into the eye. And here is something people rarely notice. | baked | NB11 | 2:39.3 / 5.6 |
| 38 | 2:31.1 | 2:35.9 | 4.8 |  | Search the whole of Book Nine, and Homer never writes the words 'one eye'. | card | CODE:ledger-search | 2:44.9 / 5.6 |
| 39 | 2:35.9 | 2:41.5 | 5.7 |  | He never mentions a forehead. He says 'the eye', and presumably his audience knew. | bakedX | X:NB11 + CODE:overlay-greek | 2:50.5 / 5.6 |
| 40 | 2:41.5 | 2:46.8 | 5.3 |  | For a plain statement, one eye in the forehead, we need a different poet. | card | CODE:card-hesiod-teaser | 2:56.1 / 5.6 |
| 41 | 2:46.8 | 2:52.0 | 5.2 |  | As for the blinding itself, Homer compares it to a shipwright boring a plank, | white | NP02 | 3:01.7 / 5.6 |
| 42 | 2:52.0 | 2:57.6 | 5.6 |  | and to a smith quenching an axe in water. That is all we need. | white | NP03 | 3:07.3 / 5.6 |
| 43 | 2:57.6 | 3:02.3 | 4.8 |  | The other Cyclopes hear the screaming and come to ask what is wrong. | cutout | NBG03 + cutouts | 3:12.9 / 5.2 |
| 44 | 3:02.3 | 3:08.6 | 6.2 |  | Polyphemus shouts that Nobody is killing him. The others conclude that nobody is. | baked | NB12 | 3:18.1 / 5.2 |
| 45 | 3:08.6 | 3:13.3 | 4.8 |  | They suggest he pray to Poseidon, and go back to bed. | cutout | NBG03 + cutouts | 3:23.3 / 4.4 |
| 46 | 3:13.3 | 3:17.8 | 4.5 |  | At dawn, the sheep leave the cave. Odysseus has tied them in threes, | baked | NB13 | 3:27.7 / 5.2 |
| 47 | 3:17.8 | 3:23.8 | 5.9 |  | with a man hidden under each middle sheep. He himself hangs beneath the finest ram. | baked | NB14 | 3:32.9 / 6.0 |
| 48 | 3:23.8 | 3:28.1 | 4.4 |  | The blinded giant feels along their backs, never their bellies. | baked | NB15 | 3:38.9 / 4.0 |
| 49 | 3:28.1 | 3:33.7 | 5.5 |  | Homer even lets Polyphemus talk to his ram, almost tenderly, as it leaves last. | baked | NB16 | 3:42.9 / 5.6 |
| 50 | 3:33.7 | 3:37.5 | 3.9 |  | Then Odysseus, safely aboard his ship, cannot resist. | cutout | NBG04 + NP04 | 3:48.5 / 3.2 |
| 51 | 3:37.5 | 3:41.9 | 4.3 |  | His crew begs him to stop. He shouts his real name anyway. | cutout | NBG04 + NP04 + cutouts | 3:51.7 / 4.8 |
| 52 | 3:41.9 | 3:46.7 | 4.8 |  | Polyphemus remembers a prophecy that a man named Odysseus would take his sight. | baked | NB17 | 3:56.5 / 5.2 |
| 53 | 3:46.7 | 3:50.0 | 3.3 |  | He tears the top off a hill and hurls it at the ship, | baked | NB18 | 4:01.7 / 5.2 |
| 54 | 3:50.0 | 3:53.8 | 3.9 |  | and prays to Poseidon that Odysseus never reaches home. | bakedX | X:NB17 | 4:06.9 / 3.6 |
| 55 | 3:53.8 | 3:59.0 | 5.2 |  | Poseidon listens. For much of the rest of the poem, he keeps Odysseus from home. | bakedR | RS10 | 4:10.5 / 6.0 |

### 2. The skull

| # | start | end | sec | flag | narration | type | asset | old start / sec |
|---|---|---|---|---|---|---|---|---|
| 56 | 3:59.0 | 4:01.0 | 2.0 |  | (silent chapter card) | title card | CODE:chapter-card | 4:16.5 / 2.5 |
| 57 | 4:01.0 | 4:05.3 | 4.3 |  | So that is the myth. Is there anything solid underneath it? | white | existing cy_v4 cutout | 4:19.0 / 4.4 |
| 58 | 4:05.3 | 4:11.3 | 5.9 |  | In 1914, the palaeontologist Othenio Abel thought there might be. | card | CODE:card-abel-book | 4:23.4 / 4.0 |
| 59 | 4:11.3 | 4:16.0 | 4.8 |  | During the Ice Age, dwarf elephants lived on islands across the Mediterranean: | map | CODE:map-dwarf-islands | 4:27.4 / 4.8 |
| 60 | 4:16.0 | 4:21.3 | 5.2 |  | Sicily, Malta, Crete, Cyprus, and a scattering of Aegean islands. | map | CODE:map-dwarf-islands | 4:32.2 / 4.0 |
| 61 | 4:21.3 | 4:25.2 | 3.9 |  | They descended from a straight-tusked elephant about four metres tall, | white | X:NP01 + CODE:scale-chart | 4:36.2 / 4.0 |
| 62 | 4:25.2 | 4:27.2 | 2.1 | short | and island life shrank them. | white | X:NP01 + odysseus_A cutout | 4:40.2 / 3.2 |
| 63 | 4:27.2 | 4:30.3 | 3.1 |  | Their bones turn up in caves, and still do. | baked | NB19 | 4:43.4 / 3.6 |
| 64 | 4:30.3 | 4:32.5 | 2.2 | short | Now look at the skull from the front. | diagram | CODE:skull-front (DG-01) | 4:47.0 / 3.2 |
| 65 | 4:32.5 | 4:35.9 | 3.4 |  | The eye sockets are small, and set low at the sides. | diagram | CODE:skull-front (DG-01) | 4:50.2 / 4.4 |
| 66 | 4:35.9 | 4:40.8 | 4.8 |  | What dominates is a huge hole in the middle: the opening for the trunk. | diagram | CODE:skull-front (DG-01) | 4:54.6 / 5.6 |
| 67 | 4:40.8 | 4:45.1 | 4.3 |  | Abel pictured a sailor, sheltering in a cave and lighting a fire, | baked | NB20 | 5:00.2 / 4.8 |
| 68 | 4:45.1 | 4:49.1 | 4.0 |  | who sees a skull sticking out of the clay, with one great eye. | bakedX | X:NB19 | 5:05.0 / 5.2 |
| 69 | 4:49.1 | 4:54.8 | 5.8 |  | Everything else, he wrote, was added later. It is imagination, not evidence. | bakedX | X:NB20 + CODE:overlay-abel | 5:10.2 / 4.8 |
| 70 | 4:54.8 | 5:01.1 | 6.3 |  | The idea found a champion in Adrienne Mayor, a Stanford folklorist and historian of science. | card | CODE:card-mayor | 5:15.0 / 6.0 |
| 71 | 5:01.1 | 5:06.9 | 5.8 |  | In The First Fossil Hunters, she argues that Greeks and Romans noticed big fossil bones, | baked | NB21 | 5:21.0 / 6.0 |
| 72 | 5:06.9 | 5:10.6 | 3.7 |  | collected them, measured them, and tried to explain them. | bakedX | X:NB21 + CODE:measuring-rod | 5:27.0 / 3.6 |
| 73 | 5:10.6 | 5:15.3 | 4.7 |  | Giants, and one-eyed monsters, may owe something to those finds. | bakedX | X:NB21 + CODE:overlay-may | 5:30.6 / 4.0 |
| 74 | 5:15.3 | 5:18.6 | 3.3 |  | On the Cyclops, though, Mayor herself is careful. | card | CODE:ledger-mayor-careful | 5:34.6 / 3.2 |
| 75 | 5:18.6 | 5:22.3 | 3.7 |  | She does not like to say the fossils were the source of the story, | bakedX | X:NB19 + CODE:quote-mayor | 5:37.8 / 5.6 |
| 76 | 5:22.3 | 5:27.8 | 5.5 |  | 'because we just can't prove that.' We do not know, she says, which came first. | diagram | CODE:arrows-which-first (DG-07) | 5:43.4 / 6.0 |
| 77 | 5:27.8 | 5:32.5 | 4.7 |  | Perhaps the myth came first, and the bones merely seemed to confirm it. | diagram | CODE:arrows-which-first (DG-07) | 5:49.4 / 5.2 |
| 78 | 5:32.5 | 5:36.0 | 3.5 |  | Then there is a problem with the most famous version of this theory. | card | CODE:ledger-problem | 5:54.6 / 5.2 |
| 79 | 5:36.0 | 5:41.7 | 5.7 |  | Abel claimed that the philosopher Empedocles reported finding such bones on Sicily. | card | CODE:card-empedocles | 5:59.8 / 4.8 |
| 80 | 5:41.7 | 5:45.8 | 4.1 |  | Later researchers have found no surviving ancient source that says so. | card | CODE:ledger-source-none | 6:04.6 / 4.4 |
| 81 | 5:45.8 | 5:49.8 | 4.0 |  | The palaeontologist Mark Witton and Richard Hing put it bluntly: | card | CODE:card-witton-hing | 6:09.0 / 4.0 |
| 82 | 5:49.8 | 5:53.8 | 3.9 |  | without that story, they argue, the idea becomes baseless. | bakedX | X:NB19 + CODE:overlay-paraphrase | 6:13.0 / 3.6 |
| 83 | 5:53.8 | 5:57.8 | 4.1 |  | Elephant fossils and one-eyed monsters turn up all over the world, | diagram | CODE:world-pair | 6:16.6 / 4.4 |
| 84 | 5:57.8 | 6:02.6 | 4.8 |  | and no ancient text or artwork makes the Sicilian link stand out. | map | CODE:map-med | 6:21.0 / 4.8 |
| 85 | 6:02.6 | 6:08.3 | 5.7 |  | The scholars of Greek myth Mercedes Aguirre and Richard Buxton make a similar point. | card | CODE:card-aguirre-buxton | 6:25.8 / 5.6 |
| 86 | 6:08.3 | 6:10.9 | 2.5 |  | Theories like this sound plausible, they say, | card | CODE:ledger-plausible | 6:31.4 / 3.2 |
| 87 | 6:10.9 | 6:14.4 | 3.5 |  | but lack a chain of argument linking origin to myth. | bakedX | X:NB19 | 6:34.6 / 4.0 |

### 3. The other Cyclopes

| # | start | end | sec | flag | narration | type | asset | old start / sec |
|---|---|---|---|---|---|---|---|---|
| 88 | 6:14.4 | 6:16.4 | 2.0 |  | (silent chapter card) | title card | CODE:chapter-card | 6:38.6 / 2.5 |
| 89 | 6:16.4 | 6:19.9 | 3.6 |  | Meanwhile, the Cyclops had a different life in a different poem. | baked | NB22 | 6:41.1 / 4.4 |
| 90 | 6:19.9 | 6:27.8 | 7.9 |  | Hesiod, writing around 700 BC, names three Cyclopes: Brontes, Steropes, and Arges. | card | CODE:ledger-names | 6:45.5 / 4.8 |
| 91 | 6:27.8 | 6:32.2 | 4.4 |  | Thunder, Lightning, and Bright. They forge the thunderbolt for Zeus. | baked | NB23 | 6:50.3 / 4.0 |
| 92 | 6:32.2 | 6:34.6 | 2.4 | short | And Hesiod is the one who says it plainly: | bakedX | X:NB22 | 6:54.3 / 3.6 |
| 93 | 6:34.6 | 6:38.1 | 3.5 |  | 'one eye only was set in the midst of their foreheads.' | bakedX | X:NB22 + CODE:quote-hesiod | 6:57.9 / 4.4 |
| 94 | 6:38.1 | 6:43.1 | 5.1 |  | These are not cannibal shepherds. They are craftsmen, working for the king of the gods. | bakedX | X:NB23 | 7:02.3 / 6.0 |
| 95 | 6:43.1 | 6:46.3 | 3.2 |  | Same name, same eye, completely different job. | diagram | CODE:split (RC02 / NB22) | 7:08.3 / 3.2 |
| 96 | 6:46.3 | 6:52.6 | 6.3 |  | The scholar Walter Burkert suggested the smith Cyclopes may reflect real guilds of metalworkers. | card | CODE:card-burkert | 7:11.5 / 5.6 |
| 97 | 6:52.6 | 6:59.2 | 6.6 |  | Later poets merged the two. Virgil puts Brontes and Steropes in a forge under Etna. | map | CODE:map-etna-aeolian | 7:17.1 / 6.0 |
| 98 | 6:59.2 | 7:03.1 | 3.8 |  | By the fifth century BC, the Cyclopes are living on Sicily. | cutout | NBG05 + cy_v4 cutout | 7:23.1 / 4.4 |
| 99 | 7:03.1 | 7:07.7 | 4.6 |  | Euripides sets a comic satyr play about Polyphemus beside Mount Etna. | baked | NBG05 | 7:27.5 / 4.4 |
| 100 | 7:07.7 | 7:13.1 | 5.5 |  | The historian Thucydides lists the Cyclopes among Sicily's earliest inhabitants, | bakedX | X:NBG05 + CODE:quote-thucydides-1 | 7:31.9 / 4.0 |
| 101 | 7:13.1 | 7:17.5 | 4.4 |  | then adds that he cannot say what race they were, or where they came from. | bakedX | X:NBG05 + CODE:quote-thucydides-2 | 7:35.9 / 6.0 |
| 102 | 7:17.5 | 7:20.9 | 3.4 |  | He also reports that locals believed the smith-god had a forge | baked | NBG06 | 7:41.9 / 4.4 |
| 103 | 7:20.9 | 7:25.9 | 5.0 |  | in the Aeolian islands, judging by the flame at night and the smoke by day. | bakedX | X:NBG06 | 7:46.3 / 6.0 |
| 104 | 7:25.9 | 7:31.4 | 5.5 |  | By the third century BC, Theocritus has Polyphemus singing love songs to a sea nymph, | baked | NB24 | 7:52.3 / 6.0 |
| 105 | 7:31.4 | 7:36.6 | 5.2 |  | and worrying about his one long eyebrow. Even cannibals get a love life. | bakedX | X:NB24 | 7:58.3 / 5.2 |
| 106 | 7:36.6 | 7:38.1 | 1.5 | short | There is a third strand, | map | CODE:map-argolid | 8:03.5 / 3.2 |
| 107 | 7:38.1 | 7:41.0 | 2.9 |  | and it is real in a way the others are not. | map | CODE:map-argolid | 8:06.7 / 4.4 |
| 108 | 7:41.0 | 7:46.9 | 5.9 |  | Visit Mycenae or Tiryns, and you can walk beside walls of enormous unworked stones. | baked | NBG07 | 8:11.1 / 5.6 |
| 109 | 7:46.9 | 7:49.9 | 3.0 |  | Beside them, even a hero looks small. | cutout | NBG07 + odysseus_A cutout | 8:16.7 / 3.2 |
| 110 | 7:49.9 | 7:53.2 | 3.4 |  | Pausanias, writing in the second century AD, | bakedX | X:NBG07 + CODE:quote-pausanias | 8:19.9 / 3.2 |
| 111 | 7:53.2 | 7:56.9 | 3.7 |  | says the walls of Tiryns are the work of the Cyclopes, | bakedX | X:NBG07 | 8:23.1 / 4.4 |
| 112 | 7:56.9 | 8:01.1 | 4.2 |  | with stones so big that a pair of mules could not move the smallest. | baked | NB25 | 8:27.5 / 5.6 |
| 113 | 8:01.1 | 8:06.5 | 5.4 |  | The walls date to the Bronze Age, centuries before Homer, and people built them. | baked | NBG08 | 8:33.1 / 5.6 |
| 114 | 8:06.5 | 8:10.6 | 4.0 |  | Archaeologists still call the style cyclopean masonry. | bakedX | X:NBG08 + CODE:overlay-definition | 8:38.7 / 3.2 |
| 115 | 8:10.6 | 8:15.1 | 4.5 |  | The wall is real. The Cyclopes were the Greeks' explanation for it. | bakedX | X:NBG07 | 8:41.9 / 4.8 |
| 116 | 8:15.1 | 8:18.9 | 3.8 |  | The Greeks did attach giants to things they could not explain. | diagram | CODE:ledger-three-rows (DG-08) | 8:46.7 / 4.4 |
| 117 | 8:18.9 | 8:21.7 | 2.9 |  | In Sicily, local tradition says the sea stacks | baked | NBG09 | 8:51.1 / 3.2 |
| 118 | 8:21.7 | 8:25.5 | 3.7 |  | at Aci Trezza are the boulders thrown at Odysseus. | bakedX | X:NBG09 | 8:54.3 / 3.6 |
| 119 | 8:25.5 | 8:32.0 | 6.6 |  | They are volcanic basalt, about half a million years old. That is legend, not archaeology. | bakedX | X:NBG09 + CODE:map-sicily-east (inset) | 8:57.9 / 6.0 |

### 4. What we can and cannot say

| # | start | end | sec | flag | narration | type | asset | old start / sec |
|---|---|---|---|---|---|---|---|---|
| 120 | 8:32.0 | 8:34.0 | 2.0 |  | (silent chapter card) | title card | CODE:chapter-card | 9:03.9 / 2.5 |
| 121 | 8:34.0 | 8:37.7 | 3.7 |  | So where does that leave us? Start with what is solid. | card | CODE:ledger-solid-not | 9:06.4 / 4.4 |
| 122 | 8:37.7 | 8:42.6 | 4.8 |  | The Greeks told at least three different Cyclops stories, and kept them apart. | diagram | CODE:three-columns (RC02 / NB22 / NBG07) | 9:10.8 / 5.2 |
| 123 | 8:42.6 | 8:49.0 | 6.5 |  | A single eye is stated by Hesiod, Euripides, and Theocritus. Homer implies it. | card | CODE:ledger-attested | 9:16.0 / 5.2 |
| 124 | 8:49.0 | 8:51.5 | 2.5 | short | Dwarf elephants really lived on those islands, | diagram | CODE:skull-front (DG-01) | 9:21.2 / 3.2 |
| 125 | 8:51.5 | 8:54.4 | 2.9 |  | and their skulls really do have a hole in the middle. | diagram | CODE:skull-front (DG-01) | 9:24.4 / 4.4 |
| 126 | 8:54.4 | 9:00.0 | 5.6 |  | The blinding story itself is a folktale. Scholars have counted over two hundred versions, | map | CODE:map-world-folktale | 9:28.8 / 5.6 |
| 127 | 9:00.0 | 9:04.2 | 4.2 |  | from Iceland to Korea, and most think the tale is older than Homer. | map | CODE:map-world-folktale | 9:34.4 / 5.2 |
| 128 | 9:04.2 | 9:06.2 | 2.0 | short | That does not rule out the skull. | bakedX | X:RS07 | 9:39.6 / 3.2 |
| 129 | 9:06.2 | 9:09.0 | 2.8 |  | It does mean the story does not need one. | bakedX | X:RS07 | 9:42.8 / 3.6 |
| 130 | 9:09.0 | 9:11.1 | 2.1 | short | Now, what we cannot say. | bakedX | X:NB19 + CODE:overlay-not-stated | 9:46.4 / 3.2 |
| 131 | 9:11.1 | 9:16.0 | 4.8 |  | No surviving ancient text says anyone mistook a skull for a Cyclops. | bakedX | X:NB19 | 9:49.6 / 4.8 |
| 132 | 9:16.0 | 9:23.1 | 7.1 |  | Other explanations compete: volcanic craters, smith guilds, even a birth defect called cyclopia, | bakedX | X:NBG06 | 9:54.4 / 5.2 |
| 133 | 9:23.1 | 9:27.3 | 4.2 |  | though in that condition the eye sits below the nose, not above it. | card | CODE:card-cyclopia | 9:59.6 / 5.2 |
| 134 | 9:27.3 | 9:31.4 | 4.1 |  | Aguirre and Buxton's verdict is that each has an air of plausibility, | card | CODE:ledger-verdict | 10:04.8 / 4.8 |
| 135 | 9:31.4 | 9:33.1 | 1.7 | short | and none has proof. | card | CODE:ledger-verdict | 10:09.6 / 3.2 |
| 136 | 9:33.1 | 9:38.4 | 5.3 |  | The skull theory is a hypothesis. A plausible one, and still unproven. | diagram | CODE:skull-front (DG-01) + stamp | 10:12.8 / 4.8 |

### Verdict and next

| # | start | end | sec | flag | narration | type | asset | old start / sec |
|---|---|---|---|---|---|---|---|---|
| 137 | 9:38.4 | 9:40.4 | 2.0 |  | (silent chapter card) | title card | CODE:chapter-card | 10:17.6 / 2.5 |
| 138 | 9:40.4 | 9:42.4 | 2.0 | short | So, was the Cyclops real? | bakedX | X:NB01 | 10:20.1 / 3.2 |
| 139 | 9:42.4 | 9:45.7 | 3.3 |  | As a one-eyed giant who eats sailors, no. | bakedR | RS08 | 10:23.3 / 3.2 |
| 140 | 9:45.7 | 9:48.7 | 3.0 |  | But the name covers at least four different things: | card | CODE:ledger-four | 10:26.5 / 3.6 |
| 141 | 9:48.7 | 9:54.4 | 5.7 |  | Hesiod's thunderbolt smiths, Homer's shepherd, a volcano's worth of Sicilian tradition, | diagram | CODE:four-panel (NB22 / RC02 / NBG05 / NBG07) | 10:30.1 / 4.4 |
| 142 | 9:54.4 | 9:56.5 | 2.1 | short | and walls you can still touch. | bakedX | X:NBG07 | 10:34.5 / 3.2 |
| 143 | 9:56.5 | 10:01.4 | 4.9 |  | The skull may be one more thread. It is a suspect, not a conviction. | diagram | CODE:skull-front (DG-01) + stamp | 10:37.7 / 5.6 |
| 144 | 10:01.4 | 10:05.8 | 4.4 |  | Odysseus leaves that island six men short, with a god's grudge. | cutout | NBG04 + odysseus_A cutout | 10:43.3 / 4.4 |
| 145 | 10:05.8 | 10:10.4 | 4.6 |  | Next time: the winds, the witch, and the other monsters of the Odyssey. | card | CODE:card-next | 10:47.7 / 5.2 |
| 146 | 10:10.4 | 10:15.1 | 4.7 |  | Some of them have real-world suspects too. We will see which survive. | card | CODE:ledger-next | 10:52.9 / 4.8 |
| 147 | 10:15.1 | 10:19.1 | 4.0 |  | Subscribe if you would like us to keep checking. | card | CODE:end-card | 10:57.7 / 3.6 |
