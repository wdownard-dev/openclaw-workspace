# REVIEW-ref-vs-draft-2026-11-12.md: why the reference holds 13 minutes and our draft does not

Author: Editor (subagent), 2026-11-12. Read-only on project assets; nothing generated, uploaded or sent. Reference: Unknown Frequencies, "The ENTIRE Story of The Odyssey Explained" (mJS-QVw8lzY, 13:08). Ours: `video1/draft/video1_draft.mp4` (10:12.8).

William's note: "it was the transitions and the cards. It felt like a school lesson and easy to tune out." The measurements below agree with him, and add three things he did not name: the **script** is an essay, the **palette** is dark, and the **voice** is flat.

Confidence labels: **[V]** measured on the files, **[E]** estimate or hand-count from viewing, **[U]** unverified or not judgeable by me.

---

## 0. Verdict in six lines

1. **Cut rate is not the gap.** Picture changes per minute: reference 10.7, ours 8.5 detected (14.4 planned in our shot list, but 43% of those planned shots are the same image or a card re-cut). Median shot 4.2 s vs 4.2 s planned. What differs is *what* is on screen and *what happens inside* each shot. [V]
2. **Cards.** Text/map/diagram-only shots take **15.2% of the reference's runtime and 0.8% is a pure text card**; in ours they take **39.5% and 20.0%** (ledger and source cards). The reference's cards are story props (a counter ticking 12→7 SHIPS, a map with the hero's route, "22 WAGONS" popping beside the boulder). Ours are claim and source tables. [V counts from our shot list; E for the reference's categories, hand-labelled from 142 frames]
3. **Transitions.** Reference: 0 crossfades, 127 hard cuts of 141 picture changes, the other 14 are in-shot animations. Ours: 53 of 146 boundaries (36%) are 9- or 12-frame crossfades by code, and our dissolve detector finds 36 clusters vs 0. Crossfades read as slides. [V]
4. **Script.** The reference tells a story: 16 voiced dialogue exchanges, 6.3 action verbs per 100 words, hedging 0.38 per 100. Ours is an essay: 0 dialogue, 3.0 action verbs, hedging 1.7 per 100, attribution verbs 7× more frequent. [V lexicon counts, E for dialogue and jokes (hand-counted)]
5. **Look and sound.** 66.5% of our frames have mean luminance under 60/255 and 40% are near black; the reference is 5.6% and 2.8%, with 25.6% of frames white-dominant (cutaways) vs our 0%. Ours has a continuous drone bed 12 dB above the reference's gap floor, a flatter voice (pitch spread 2.9 vs 4.7 semitones, LRA 1.7 vs 3.6 LU), and 3× more pauses. [V]
6. **Share of the "school lesson" feel (my judgement, [E]):** about 55% script and structure, 30% visuals (cards, dark palette, no acting, captions on every shot), 15% edit and sound (crossfades, constant push-ins, drone, flat voice). The visual fixes alone would help but cannot rescue the middle six minutes, because those cards exist to carry claims.

---

## 1. Method and what is and is not covered

| Item | How |
|---|---|
| Reference transcript | YouTube auto-captions (English, ASR, punctuated) via the existing yt-dlp (`/home/williamdownard/tools/ytdlp-venv/bin/yt-dlp --skip-download --write-auto-subs --sub-format json3`) into new directory `tests/ref_mJS_captions/`. 2,341 words, word-level start times. ASR may mis-hear names ("suiters", "Banded up"). [V] |
| Our transcript | `video1/audio/words.json` (1,585 words, word start and end) and `SCRIPT-V1.md` |
| Reference video | already at `tests/ref_mJS/ref.mp4` (AV1, 720p, 60 fps). No new download. |
| Frames | bundled ffmpeg to PNG sequence at 320x180, 30 fps (reference halved from 60 fps): 23,659 and 18,384 frames. The bundled ffmpeg has no `fps`, `ebur128` or `rawvideo`, so I used `-r 30` and PNGs, then Node + sharp. No numpy on this machine; all pixel maths in Node. |
| Cut and event detection | per-frame mean absolute difference; picture change = ≥30% of 80x45 gray pixels differing by >25 levels between frames t-6 and t+6 (catches hard cuts and dissolves); "any visible change" = ≥10% over ±4 frames. Calibrated on our own draft: against our 146 known boundaries it finds 87 (the rest are same-image re-crops and card-to-card changes under the threshold), with 0 false extras. |
| Shot types | **Ours:** from `shots_timed.json` (ground truth). **Reference:** I viewed one frame per shot (142 shots, 4 sheets) and hand-labelled each; counts below are [E] for the label, [V] for the durations. |
| Audio | 16 kHz mono and 44.1 kHz stereo extracts; Node for RMS, floor, pauses, F0 (autocorrelation), stereo width; `loudnorm` pass for LUFS/LRA. |
| Scratch files | scripts in `analysis_teardown_scripts/`, outputs in `analysis_teardown_out/` (sheets and JSON kept; bulk PNG frames and WAVs deleted at the end). |

Not judged: the sound of either voice, the music, real-time motion feel, hand-drawn animation quality at 60 fps, and any retention data (we have view counts only, not watch-time curves). [U]

---

## 2. Writing (script teardown)

### 2.1 Numbers [V unless noted]

| Measure | Reference (788 s) | Ours (611 s of narration) |
|---|---|---|
| Words | 2,341 | 1,585 |
| Overall pace | 178 wpm | 155 wpm |
| Sentences (ASR punctuation / script punctuation) | 243 | 141 |
| Words per sentence, mean / median | 9.6 / 8 | 11.2 / 11 |
| Sentences of ≤6 words | 39.5% | 24.1% |
| Sentences per minute | 18.5 | 13.8 |
| Questions per minute | 1.22 (16) | 0.29 (3) |
| Action verbs per 100 words (physical plot verbs: grab, smash, drive, burn, run...) | 6.3 | 3.0 |
| Sentences that contain an action verb | 41.6% (≈7.7 per min) | 25.5% (≈3.5 per min) |
| Claim/mental verbs per 100 words (say, argue, know, call, name...) | 1.7 | 4.2 |
| Hedge words per 100 (may, might, perhaps, theory, plausible, unproven...) | 0.38 | 1.70 |
| Attribution verbs per 100 (says, writes, argues, according...) | 0.26 | 1.83 |
| Sentences naming a scholar or ancient author, or using an attribution verb | n/a (the reference cites no one) | 32% (45 of 141) |
| Sentences containing a number | 17.3% | 12.8% |
| Proper nouns per 100 words | 4.7 (characters and places) | 7.5 (scholars, authors, places) |
| Voiced dialogue exchanges (hand count) [E] | 16 | 0 (quotes are read as sourced quotations) |
| Jokes, deadpan asides and gags per minute (hand count) [E] | ≈15 in 13.1 min = 1.1 | ≈5 in 10.2 min = 0.5 |
| Stakes lines and forward-pull lines per minute (hand count) [E] | ≈20 = 1.5 | ≈9 = 0.9 |

**Correction to the brief's "second-person address":** the reference's 28 "you" tokens are almost all inside character dialogue ("Who's hurting you?", "You thought your king was dead?"). Direct narrator-to-viewer address is about 4 lines in 13 minutes ("Let's start...", "Brilliant, right?", the moral, the Spotify line). We use it 3 times. Neither video talks to the viewer; the reference talks *through characters*. [V from grep]

**Reference shape:** 11 episodes (Troy, Ismarus, Lotus Eaters, Cyclops, Aeolus, Laestrygonians, Circe, underworld, Sirens/Scylla, Thrinacia, Calypso, Ithaca) at about 70 s each, no commentary until the last 30 s moral. Even the Cyclops, the longest, is 143 s (2:22-4:45), with 14 shots, about 4 gags and 4-5 dialogue passages. Ours spends 198 s on the same story with no dialogue (chapter 1), then 6 minutes arguing about sources.

### 2.2 How each beat ends

**Reference** (12 episode endings, hand-read): 10 end on a forward pull or escalation, 2 on a punchline. [E]
- "Day one of the trip home and he's already burying soldiers." (joke plus stakes)
- "Not the worst stop on the trip. That honor goes to the next one." (teaser)
- "Poseidon heard every word, and he granted every part of that prayer. From this point on, the sea itself was Odysseus' enemy."
- "But the worst was still coming."
- "12 ships became one. Over 500 men became a few dozen. And they hadn't even reached the halfway point."
- "Every man drowned. Every single one."

**Ours** (12 paragraph and chapter endings, hand-read): 3 forward pull, 4 jokes, 5 summary or hedge. [E]
- Ch 2: "It is imagination, not evidence." / "...lack a chain of argument linking origin to myth."
- Ch 3: "That is legend, not archaeology."
- Ch 4: "The skull theory is a hypothesis. A plausible one, and still unproven."
- End: "Subscribe if you would like us to keep checking."

Fairness: our script *does* re-hook ("So that is the myth. Is there anything solid underneath it?", "There is a third strand, and it is real in a way the others are not"). Re-hook density is not the weakness; the re-hooks are epistemic ("is it true?") where theirs are physical and emotional ("will they survive?").

### 2.3 Side by side (exact lines)

| Moment | Reference | Ours |
|---|---|---|
| Opening stakes | [0:04] "But the entire 10-year nightmare happened because one man couldn't keep his mouth shut after winning a fight." [0:11] "Yeah, seriously." | [0:11] "In 1914, a palaeontologist argued that hole is where the Cyclops came from." [0:21] "If it is right, one of literature's most famous monsters began as an honest mistake." |
| The loss | [0:30] "He left Troy with 12 ships and more than 600 men. Not one of them made it home." | [0:27] "If it is wrong, we have been passing on a good story with nothing underneath." |
| Same beat, the "Nobody" gag | [3:11] "Cyclops, what's your name?" "Polyphemus. What's yours?" "My name is Nobody." "Nobody? Well, Nobody, I like you. I'll eat you last. That's my gift." "Thanks. Very generous." | [2:14] "Odysseus says his name is Nobody." [2:16] "The present is that Polyphemus will eat him last." [2:20] "It is not much of a gift, but it buys time." |
| Violence | [2:55] "The Cyclops grabbed two of Odysseus' men, smashed their heads on the ground, and ate them raw." | [1:40] "Across three meals, Polyphemus eats six of his men, two at a time." [1:47] "Homer gives the detail. We will leave it out." |
| A reversal | [8:53] "The hides of the dead cattle crawled on the ground. The meat on the spits mooed. Yeah, the meat mooed." | [5:39] "The palaeontologist Mark Witton and Richard Hing put it bluntly: without that story, they argue, the idea becomes baseless." |
| Escalation | [5:41] "But the worst was still coming." | [5:21] "Perhaps the myth came first, and the bones merely seemed to confirm it." |
| Chapter close | [8:59] "Every man drowned. Every single one." | [9:26] "The skull theory is a hypothesis. A plausible one, and still unproven." |
| Hedge | (none; the story is simply told) | [5:12] "She does not like to say the fossils were the source of the story, 'because we just can't prove that.'" |

The "Nobody" row is the clearest: identical event, theirs is a scene with a punchline, ours is a report of the scene with a dry aside. Ours is the better prose and the worse television.

### 2.4 Device: told story vs essay

| | Reference | Ours |
|---|---|---|
| Narrative device | A story told in scenes, always in the moment, one cause per beat ("because he turned around and shouted his name") | A case file: poem, then bones, then dissenters, then ledger. Past events are reported by Homer, claims by named scholars |
| Who speaks | Characters, the narrator mostly stays out | The narrator and cited scholars |
| Where the surprise sits | Inside the plot (bag of winds, mooing meat) | Inside the argument ("that story has no source") |
| Share of runtime that is "the story" | ~97% | 32% (chapter 1) plus the cold open |
| Reader's task | Follow what happens next | Weigh evidence |

### 2.5 How much is script and how much is visuals and edit [E]

The cards, source plates and diagrams exist because the script has 45 claim-and-source sentences; a visual-only pass cannot remove them. 24 of our 30 cards are in chapters 2-4 and the verdict, where 51% of runtime is cards, maps or diagrams (21.5% before 3:56). Chapter 1, which *is* a story, is the part of our video closest to the reference, and it still lacks dialogue, expression changes and any bright cutaways. That points to the script as the root cause and the visuals as the amplifier. My split: **55% script and structure, 30% cards and look, 15% edit and sound**. That is judgement; it is not something I can measure.

---

## 3. Visuals and edit

### 3.1 Summary table [V unless noted]

| Measure | Reference | Ours |
|---|---|---|
| Picture changes per min (≥30% of pixels, detector) | 10.7 (141) | 8.5 (87); planned shot list 14.4 (147) |
| All visible change moments per min (≥10% of pixels) | 18.1 (238) | 11.4 (116) |
| Pop-ins, sprite swaps, label appearances per min (≥10% but not a new picture) | 7.4 | 2.8 |
| Median gap between visible changes | 2.2 s (p90 6.7 s) | 4.6 s (p90 8.0 s) |
| Longest gap without a visible change | 24 s (a held beat) | 31 s |
| Gaps over 8 s | 17 | 10 |
| Shot length, median / p90 | 4.2 s / 12.3 s | 4.8 s / 13.2 s (detector); 4.2 s / 5.7 s (planned) |
| Share of runtime in shots ≥8 s | 44% (static image plus pop-ins) | 52% (detector) |
| Frozen frames (mean frame diff <0.05) | **91%** | **8%** |
| Frames in constant slow motion | 4% | 72% |
| Planned camera moves | none visible | 55 push-ins, 7 pans, 1 pull-out, 84 holds |
| Distinct compositions | ≈127 of 142 shots (89%), clustering at diff <12 | 42 generated pictures reused across 147 shots (26 of 42 used more than once; most-used picture 8 times), plus 74 code shots (dark card template) |
| Mean luminance | 135/255 | 59/255 |
| White-dominant frames (>40% of pixels near white) | 25.6% | 0.0% |
| Near-black frames (>50% of pixels <25) | 2.8% | 40.1% |
| Burned-in captions | none in 142 sampled frames and 2 full-size stills [V] | small serif caption at the bottom of nearly every picture shot, plus plates like "PARAPHRASE: Witton and Hing (2024), as reported..." [V from sheets and stills] |
| Share of shots with on-screen text or a label | ≈44% (63 of 142; 1-3 words, large, hand-lettered) [E] | ≈50%+ (cards, plates, quotes, lower-thirds, 4-18 words) [E] |

**Surprise for the brief:** the reference does *not* move. Between events its frames are exactly frozen (91%), with no camera push, pan or zoom. It is "eventful but static"; ours is "constantly drifting but uneventful". Our blanket slow push-in on every picture is the standard documentary slideshow signature and, with the crossfades, probably adds to the lecture feel. [E on the effect, V on the measurement]

### 3.2 What a beat looks like

- **Reference:** a new picture, then within 1-2 s something pops on a key word with no easing: "12 SHIPS" appears at 31.8 s as the narration says "12 ships" (30.3 s); "22 WAGONS" at 168 s on "22 wagons" (167 s); the counter ticks 12→11→10→...→7 SHIPS over 6 frames. Characters change by *swapping to a new drawing* (worried, shouting, shrug, crying), not by tweening. About 15 counters or number labels, 6+ speech bubbles or lettered quotes in the 142 shots. [V for timing, E for the counts]
- **Ours:** a new picture or card per sentence in chapter 1 (good cadence), then slow push-in, caption at the bottom. Cards animate their reveal (our QA found text-card reveals 0.25-0.3 s after the card starts). Characters never change pose within a shot. Odysseus and the Cyclops appear in 59 of 147 shots, all baked into a painted scene or cut out and scaled. [V from shot list and QA]

### 3.3 Character-led vs everything else (hand labels for the reference, [E]; durations [V])

| Category | Reference shots | Share of runtime | Ours (shot list) | Share of runtime |
|---|---|---|---|---|
| Character(s) in a painted scene or monster scene | 81 (66 S, 10 monster, 5 empty scene) | 63.2% | 73 baked + 10 cutout = 83 pictures; only 59 contain a character | 39.6% for character shots; 56.6% for all pictures |
| Characters on plain white (cutaway) | 30 | 17.1% | 6 (props only, no characters) | 3.9% |
| Text with a character beside it | 8 | 4.5% | 0 | 0% |
| Pure text or number card | 4 | 0.8% | 30 (25 ledger/claim cards + 5 chapter cards) | 20.0% |
| Map | 14 (8 with route arrows, 2 with a character on it) | 12.3% | 9 (information maps, 1 route, 0 characters) | 6.6% |
| Diagram or inset | 5 | 2.1% | 19 (skull plate, scale chart, three-column tables; 9 shots use the skull) | 12.9% |
| **Text, map or diagram only** | **23 (16%)** | **15.2%** | **58 (39%)** | **39.5%** |

Ours also has 26 runs of consecutive card, map or diagram shots; the longest are 32 s, 27 s and 17 s. The reference's longest run without a character is a few seconds.

### 3.4 Palette

Reference: bright, white-heavy, saturated cartoon (rust-red lettering, cream, light blue). Ours: near-black cards, brown caves, night scenes. On a phone or TV a 10-minute run of dark frames feels like a documentary; a bright one feels like a cartoon. [E on the effect]

---

## 4. Audio [V; I cannot hear either track]

| Measure | Reference | Ours |
|---|---|---|
| Integrated loudness | -19.4 LUFS | -16.2 LUFS |
| Loudness range | 3.6 LU | 1.7 LU |
| Pace overall / per 30 s window | 178 wpm / 173 ± 26 (162-202 apart from the last window) | 155 wpm / 151 ± 22 (136-172) |
| Pauses ≥0.3 s (relative to median level -18 dB) | 25 (1.9 per min), 8.7 s total (1.1%) | 59 (5.8 per min), 28.1 s total (4.6%) |
| Pauses ≥0.6 s | 0 | 15 (and 36 pauses >0.5 s by word timings) |
| Voice pitch spread (F0, mean of 20 s windows) | 4.7 semitones, median 160 Hz | 2.9 semitones, median 127 Hz |
| Level steadiness of the voice (p90 across 30 s windows) | ±0.5 dB | ±0.2 dB |
| Gap floor (5th percentile of 50 ms RMS) | -50.8 dBFS (range -45 to -60) | -41.8 dBFS (range -40 to -54) |
| Floor spectrum | broadband, 40% at 50-150 Hz, 22% at 300-600 Hz, no tonal structure | 97% below 300 Hz: the synthesised drone |
| Stereo | dual mono (side channel -86 to -105 dBFS = digital silence) | genuine stereo (side -39 dBFS), detuned pad |

Readings:
- **Reference music:** there is no detectable bed in the gaps between words: the floor is about 30 dB under the speech and shows no pad or tonal content, and the channels are identical. I cannot rule out music masked under the speech. The reference is, in effect, a voice on a quiet room tone. [V for the floor, U for hidden music]
- **Ours:** a continuous low drone sits 12 dB above the reference's floor from first to last second (floor stays at -40 to -43 dBFS in every window). MUSIC.md calls it "felt rather than heard" at -35 LUFS ducked; the measurement says it is a constant presence in every gap. A held low pad with no melody or rhythm is the classic documentary-lecture bed. [V for the level, E for the effect]
- **Voice:** theirs is 15% faster overall, with almost no air between sentences, a wider pitch spread (consistent with a performer doing character voices; the crude tracker can have octave errors, but both files were measured the same way), and 2× the loudness range. Ours was directed "slower and flatter... let sentences land" (SCRIPT-V1.md), which is what measured. [V]
- **Sound effects:** I tested for cut-synchronised high-frequency transients. At a strict threshold 15.6% of reference cuts have one against 8.4% for random times (ratio 1.85), but our own draft, which has no cut-synchronised effects, shows 1.39 on the same test. The test cannot separate light effects from speech sibilants. At most the reference has light sounds on a minority of cuts. [U]

---

## 5. Transitions (the first thing William named)

| | Reference | Ours |
|---|---|---|
| Scene-to-scene | **Hard cut, every time** (127 of 141 picture changes by detector; 0 dissolve clusters; the other 14 are in-shot animations; 12 gradual events from the wider list of 37 were viewed and are the same kind: counter ticks, sprite entrances, label pop-ins) | **Hard cut 93, 9-frame crossfade 43, 12-frame crossfade 10** (from `Video.tsx`: `fadeLen` = 12 into and out of every chapter card, 9 whenever a picture meets a card, map or diagram) |
| Dissolves detected | 0 | 36 clusters |
| Time under a crossfade | 0 s | 16.9 s (2.8% of runtime, 36% of boundaries) |
| Dip to black or white | none | none |
| Whip, shake, slide | none | one 8 px x-kick (shot 37) |
| Time passing | rapid hard-cut montage (loom shots 625-631 s, sun to moon flashes 580-581 s) | none |
| Scene reveal inside a shot | pop-in with no easing; sprite slides in (659 s); letterbox bars close (671.5 s); stop-motion zoom through the axe heads (695-698 s) | card text reveals ~0.3 s after start; map and skull diagram animations; caption chunks |
| Camera | none; image is frozen between events | slow push or pan on 63 shots (43%) |

**Effect on flow [E]:** every crossfade is placed at the exact moment the video switches from a story picture to an information card or back, so the transition itself announces "slide change". The reference never softens a cut; it keeps energy by cutting on the beat and letting the new picture pop. The chapter cards add 10 more 0.4 s fades plus a 2.0 s silent card window each, which stops the voice at five points in ten minutes.

---

## 6. Cards, quantified

**Reference: 23 non-character shots in 142 (16%).** All of them are story props, not claims:
- **4 pure text cards (0.8% of runtime):** "10 YEARS", "9 DAYS", "DAY 1 OF THE TRIP HOME", the "72 MEN KILLED: 6" counter with ship icons. Each shows a *number from the story*.
- **8 text beside a character (4.5%):** "THE END OF" with the host, "WAR OVER", "HUNDREDS OF MEN KILLED", "1 SHIPS 500 MEN", "GO SAIL TO THE LAND OF THE DEAD / the prophet / TIRESIAS" with an arrow to him.
- **14 maps (12.3%):** 8 have route arrows, labelled islands ("ISMARUS", "THE ISLAND OF AEOLUS", "ITHACA"), and in 2 a character stands on the map (Penelope on the Greek map at 82 s, the host beside the route at 121 s). One closing map (753 s) draws the whole route as a recap.
- **5 diagram or inset:** a picture-in-picture of the Cyclops, the grid of crossed-out ships (11 of 12), the stop-motion zoom through the axes.

**Ours: 58 non-character shots in 147 (39%), 39.5% of runtime.** Examples: `ledger-roadmap`, `ledger-problem`, `ledger-source-n`, `ledger-plausible`, `ledger-names`, `ledger-attested`, `ledger-verdict`, `ledger-four`; name plates ("Walter Burkert", "Mark Witton & Richard Hing", "Mercedes Aguirre & Richard Buxton", "Hesiod, Theogony line 145, c. 700 BC"); a CANDIDATE | PROOF table; the skull plate with labels (9 shots use the skull); 5 chapter cards.

| | Reference | Ours | Ratio |
|---|---|---|---|
| Pure text card, share of runtime | 0.8% | 20.0% | 25× |
| Text, map, diagram only, share of runtime | 15.2% | 39.5% | 2.6× |
| Cards that carry a claim or a citation (hand-read ids) | 0 | ≈19 of 30 cards | n/a |
| Number or counter from the plot shown as an overlay | ≈15 | ≈3 (1914, 22 wagons, 200+ versions) [E] | n/a |
| Maps with a hero's route | 8 of 14 | ≈1 of 9 | n/a |

---

## 7. Is the topic or the execution the problem?

**Mostly execution, with a structural cause that a re-script fixes.** Evidence:
- The *idea* (a dwarf-elephant skull may have inspired the Cyclops; the walls are real; the folktale is older than Homer) is a good hook and we measured nothing that says the topic itself repels viewers. The hook in our own cold open ("Its skull has one enormous hole in the middle of its face") is strong. [E]
- The *structure* is what makes it a lesson: "the poem first, then the bones, then the people who disagree" promises homework in the first minute, spends the first third on a retelling that the reference does with jokes in 143 s, and then runs 6 minutes of claims. Even our best chapter (the poem) is a report of a scene, not the scene.
- A told story with the real-world origin as the final-third twist would fix the largest part of the problem: it moves the evidence into the second half as a *reveal* after the audience is already invested, turns scholar quotes into short punch lines, and lets the cards become story props. It will not remove the need for hedges; it changes how they are delivered.

**Risk to flag:** the reference's pattern works because the story is already known and fun (a heist-comedy retelling). Our payoff is "plausible, unproven", which is a weaker ending than "Every man drowned." The twist has to be dramatised as a suspect line-up with a real verdict (the walls are real; the skull is a suspect), not as a shrug. Also: 1.67M views for the reference proves the format works for the *Odyssey*; it does not prove an investigative-twist format works for us. We have no retention data on either. [U]

---

## 8. Recommendations (ranked by impact per effort)

Costs: images at about $0.10-0.18 per accepted image (our own run: 37 accepted from 64 calls, 1.73 calls per accept); code time in working hours; "Layer" = script / edit / visuals / sound.

| # | Change | Layer | Effort and cost | Expected effect |
|---|---|---|---|---|
| 1 | **Re-script video 1 as a told story**: Act 1 (the cave) in scenes with performed dialogue, including the Nobody exchange; evidence moves to a "four suspects" second half, ending on a verdict. Keep every claim sourced (see integrity rules below). | Script | 1-2 days writing plus the existing accuracy pass; new voice take; 0 images for the script itself | Largest single change. Fixes the essay feel; addresses the 55% share |
| 2 | **Replace ledger, claim and source cards with story props**: case-file board with suspect portraits, rubber stamps (UNVERIFIED, HYPOTHESIS and SUSPECT already exist), counters, 1-3 word labels, a chip like "HESIOD, THEOGONY" in a corner for 2.5 s. Cap pure text cards at ≤4% of runtime. | Visuals and edit | ~1 day Remotion (components exist: stamps, plates, counters); 0 images | Brings cards from 39.5% to about 15% of runtime |
| 3 | **Remove the crossfades**: set `fadeLen` to 0 in `Video.tsx`; chapter cards become a hard cut plus a sting, or disappear in favour of a lettered title pop. | Edit | 30 minutes; re-render ~21 min; 0 images | Removes the "slide change" signal on 53 boundaries |
| 4 | **Add bright white cutaways and lighter cards**: sprite shots of Odysseus, the Cyclops and a host on white for dialogue, jokes and counters; raise card backgrounds off black. Target 15-25% white-dominant frames. | Visuals | ~40 sprites (3 heroes x 8 expressions, host x 8, 8 extras) plus ~12 new scenes = about 50-60 accepted images, **$5-11** [E]; cutout code exists (`pipeline/cutout.js`) | Gives the story-scene look and the palette contrast |
| 5 | **Act through swaps and pop-ins**: a new expression or pose per sentence, key nouns and numbers pop in with no easing ("22 WAGONS", "6 MEN", "1 EYE"), time-passing montage by rapid hard cuts. | Edit | ~1 day code, sprites from #4 | Raises pop-ins from 2.8 to about 7 per minute |
| 6 | **Voice performance**: second voice (or a pitch-shifted take) for Odysseus and Polyphemus, tighten the pauses (target 1-2 pauses ≥0.3 s per minute, pace about 170 wpm), keep dry humour in the narrator voice. | Sound | Re-render of about 10 minutes; ElevenLabs cost for a second voice and retakes [U, not priced] | Brings pitch spread toward 4-5 semitones, LRA toward 3 LU |
| 7 | **Captions**: drop the burned-in bottom captions on story shots (YouTube auto-captions plus an uploaded SRT stay); keep on-screen text only for quotes. | Edit | 1 hour; 0 images | Removes the subtitle-over-slide look; frees the lower third |
| 8 | **Audio bed**: delete the continuous drone or drop it by 12 dB so the gaps are quiet; add small tick or pop sounds on label appearances and a stinger on reveals (keep them light, the evidence for effects in the reference is weak [U]). | Sound | ½ day; 0 images | Removes the lecture bed |
| 9 | **Make a recurring host sprite our own** (not a copy of their skull-faced helmet figure: it is their identity and the channel notes say not to copy characters, fonts or thumbnails) that points, shrugs and doubts. A "ledger keeper" character could carry the hedges as a deadpan reaction instead of a sentence. | Visuals and script | Included in #4 (8 expressions) | Gives hedges personality and a reaction shot |
| 10 | **Series format**: every episode = a told story (about 70% of runtime) plus the real-world check as the twist (about 30%). Re-test the title as a story promise, for example "The Cyclops Story, and Which Parts Were Real". | Format | Planning only | Makes the first minute a story promise, not homework |

**Quick wins with no new image cost** (an edit-only "v4", about 1.5 days, estimated to remove perhaps a quarter of the problem [E]): #3, #7, #8, partial #2 (convert the 12 most text-heavy ledger cards into stamped or counter props using existing art), shave the pauses, drop the blanket push-ins to holds on the cards and keep them only on pictures.

### Keeping integrity (accuracy-first, source-attributed, but a story)

- **Sources in the description plus a consistent on-screen source chip.** A small chip ("HOMER, ODYSSEY 9", "MAYOR, 2000") shown for 2-3 s when a claim is made, always in the same corner and style, reads as a footnote and not a slide. The full source list and chapter timestamps stay in the description, with a pinned comment.
- **Dramatised dialogue must be honest.** For Homer's scene, speak lines that are in or close to the text ("Nobody is my name"); mark invented banter once ("dramatised") the first time it appears; never put invented lines in the mouth of a named scholar, whose quotes stay verbatim with a name chip.
- **Hedges delivered with personality.** "Even its biggest fan says: 'we just can't prove that.'" The stamp UNPROVEN lands on the skull; the host sprite raises an eyebrow. The hedge stays; the lecture tone goes. Our own word counts say the script uses 1.7 hedges per 100 words against 0.38; in the story version, expect about 1 per 100 because the Act 1 story is plain statement.
- **The verdict stays a verdict.** The twist is "walls: real; smiths: plausible; skull: suspect; folktale: older than the skull" with stamps, not a shrug.

---

## 9. One concrete alternative structure for video 1 (target about 10:20)

Pace target 165-175 wpm, about 1,700 words. All timings are targets.

| Time | Beat | Content | Visuals |
|---|---|---|---|
| 0:00-0:25 | **Cold open (hook)** | A skull on Sicily with one huge hole in its face. A Greek sailor could have found it. Did he? "By the end: four suspects, and one thing nobody can prove." | Skull plate pop, Odysseus on white, map push to Sicily |
| 0:25-0:45 | **Promise** | "The Cyclops is not one monster. Let's start with the one Homer gave us." | Host sprite, 4 empty suspect frames on a board |
| 0:45-1:30 | **Act 1a: the cave** | Odysseus takes 12 men; cheese, lambs, "let's wait for the owner"; Polyphemus returns, the stone (22 wagons) | Painted cave, counters, dialogue bubbles |
| 1:30-2:20 | **Act 1b: trapped** | Two men eaten (tone kept restrained, no gore; "We will leave out the detail"), why he cannot kill him (the stone), a plan | Cutaways on white, Polyphemus portrait |
| 2:20-3:10 | **Act 1c: "Nobody"** | Wine, the name exchange as performed dialogue, the stake | Two-sprite dialogue on white, then painted cave |
| 3:10-3:50 | **Act 1d: the neighbours and the sheep** | "Nobody is hurting me." "Then go back to sleep." Sheep escape | Gag shot, sheep escape scene |
| 3:50-4:20 | **Act 1e: the shout** | He shouts his name; the curse; "Poseidon listens" | Ship, Poseidon silhouette, hard cut to black |
| 4:20-4:40 | **Turn** | "Here is what Homer never says: he never writes 'one eye'. So where did the one-eyed giant come from?" Suspect board lights up | Board, magnifier pop on "the eye" |
| 4:40-6:25 | **Suspect 1: the elephant skull** | 1914, Abel's sailor-in-a-cave scene told as a scene; the dwarf elephant is smaller than a man (scale gag); Mayor, verbatim with chip: "we just can't prove that"; the Empedocles story has no source; UNVERIFIED stamp | Skull plate, scale gag, Abel sailor scene, stamp |
| 6:25-7:40 | **Suspect 2: the smiths** | Hesiod's three, Brontes, Steropes, Arges (thunder, lightning, bright), working for Zeus; Etna's forge; Theocritus's lovesick Polyphemus worrying about his one eyebrow | Forge scene, Etna map, lovesick gag |
| 7:40-8:40 | **Suspect 3: the walls (real)** | Tiryns and Mycenae, stones that two mules could not move; "the wall is real; the Cyclops were the Greeks' explanation for it" | Hero beside the wall for scale, Argolid map with route |
| 8:40-9:20 | **Suspect 4: the folktale** | 200+ versions from Iceland to Korea; older than Homer; the story does not need a skull | World map with ticking counter |
| 9:20-10:00 | **Verdict** | Four stamps on the board; "As a one-eyed giant who eats sailors, no" | Board, stamps pop on each line |
| 10:00-10:20 | **Next** | "Next time: the winds, the witch, and the other monsters. Some have suspects of their own." | Host sprite, tease image |

Text cards: at most 5 (title, one per suspect). The ledger tables go away; every claim has a name chip.

---

## 10. Confidence summary

| Claim | Label |
|---|---|
| Cut rates, shot lengths, frozen share, palette, change-event rates | [V] |
| Our shot types and crossfade counts | [V] (from `shots_timed.json` and `Video.tsx`) |
| Reference shot categories (S, W, M, T, TW, D) | [E] hand-labelled from 142 frames; durations [V] |
| Reference has 0 crossfades | [V] detector (0 clusters) plus 12 viewed samples; a rare slow dissolve under the threshold is [U] |
| Text metrics (sentence length, verbs, hedges) | [V], lexicon-based and approximate; ASR captions are noisy |
| Dialogue, jokes, stakes counts | [E] hand counts |
| Loudness, floor, pauses, pace, stereo | [V] |
| Pitch spread | [V] with a crude tracker; absolute values uncertain, comparison fair |
| No audible bed in the reference | [V] for gap floor, [U] under speech |
| Sound effects at cuts | [U] |
| Script 55% / visuals 30% / edit and sound 15% | [E] judgement |
| Cost estimates | [E] |
| How either voice and music sounds, real-time motion feel, hand-drawn quality | [U] not judged |
| That the story format would raise watch time | [U]: we have no retention data, only the reference's view counts and William's reaction |

Files: this report; scripts in `analysis_teardown_scripts/`; outputs (JSON, shot sheets `refshots_0-3.jpg`, `ourshots_0-3.jpg`, `pairs_ref_*.jpg`, `seq_ref.jpg`, `stills/`) in `analysis_teardown_out/`; captions in `tests/ref_mJS_captions/`.
