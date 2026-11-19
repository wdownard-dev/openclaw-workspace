# ROUND3.md: smoother character approach, video 1 (The Myth Ledger), 2026-11-13

**I cannot hear any of these clips.** Everything below is measurement: F0, spectra, loudness, edge and join indicators, whisper alignment. William's ears decide. Nothing was posted, sent or uploaded; no full script was recorded. No voices were created or deleted (4 BP generated voices + 22 audition voices still in the account, 26 of 30 slots).

Narration stays Daniel, `eleven_multilingual_v2`, stability 0.5 / style 0.2 / speed 1.0 / similarity 0.75 / boost on, unchanged, wherever that model is used.

## Files (all in `video2/voices4/`, all -19.2 LUFS integrated, true peak -1.6 to -1.8 dBFS, 192 kbps mono)

| File | What it is | Length |
|---|---|---|
| `diag_bp_voices_smooth.mp3` | **Listen first.** The round-2 proof scene, same voices and the same per-line renders as `voices3/proof_scene.mp3` (William's BP picks, speeds 0.8-0.9), only the joins rebuilt. 0 new characters. | 1:52 |
| `methodA_scene.mp3` (= `methodA_v4_scene.mp3`) | Method A, eleven_v4: Daniel does everything, tags on character lines, one call per passage | 1:39 |
| `methodA_v2_scene.mp3` | Method A, multilingual_v2: Daniel, no tags, quotes plus short attribution | 1:50 |
| `methodB_scene.mp3` | Method B, Text to Dialogue (eleven_v4), Daniel + library voices (Justin / Philip / Drew / Lukas) | 1:41 |
| `methodB_bp_scene.mp3` | Method B, Text to Dialogue (eleven_v4), Daniel + the saved BP voices | 1:45 |
| `methodB_libRyan_scene.mp3` | First library attempt (Ryan as Odysseus). Kept for the record: line 28 came out noise-like (see below). Not in the reel. | 1:41 |
| `methodC_scene.mp3` | Method C: Daniel for every line, characters differentiated by pitch/formant/tempo/EQ | 1:46 |
| `reel_methods.mp3` | 7:20. River slates: "Method A, one" (v4 tags), "Method A, two" (v2), "Method B" (library voices), "Method C", each followed by its scene. Offsets: A1 0:00, A2 1:45, B 3:42, C 5:29. (About 2 minutes over the 5 you asked for because A needed two versions.) | 7:20 |

Scripts in `scripts/`, per-call log (voice id, characters, model, settings, quota before and after) in `voice_log.csv`, raw measurements in `_work/*.json` (`diagnosis.json`, `comparison.json`, `c_processing.json`, `align_*.json`).

## 1. Diagnosis: why round 2 sounded cut up (measured on `voices3/proof_scene.mp3` and `voices3/proof_lines/`)

Scene indicators: **10 abrupt events** (adjacent 5 ms frames more than 35 dB apart at audible level; 5.5 per minute), **4 of them click-level** (sample step more than 8x the median speech step), and **every one of the 20 gaps is digital silence** (-159 to -180 dB, no room tone). Every new scene below reads 0 abrupt events except one inside a library render (see B).

| Likely cause | Evidence | Verdict |
|---|---|---|
| **Truncated line ends and starts, no fades** | Raw line files end at audible amplitude: beat 29 narrator last sample -12 dBFS, beat 37 chorus -12, beat 28 Odysseus -24, beat 65 narrator -30, beat 32 Poly -35. Starts: beat 32 Poly first sample -14 dBFS, beat 38 Poly -26, beat 39 chorus -33. The assembler trimmed at -50 dB and cut with no fade, then butted the result against digital zero. Joins 29→30, 32→33, 37→38 have sample steps 51x, 11x, 5x the median step (clicks). | **Main cause.** Fixed by 15 ms fade-in, 25 ms fade-out on every line. |
| **Digital silence between lines** | Gap RMS -159 to -180 dB in all 20 gaps; Daniel's files have -88 dB padding, the designed voices have no quiet frames at all (5th percentile frame -36 to -41 dB for Odysseus, chorus) so the cut goes from speech straight to nothing. | **Major.** Fixed by a continuous -62 dBFS room tone under everything. |
| **Uniform mechanical gaps** | Only three gap lengths (0.25 / 0.32 / 0.40 s) at every join. The speakers' own inline pauses are 0.25-0.98 s (narrator median about 0.45 s, Polyphemus 0.35-0.98 s) so the gaps are shorter and more regular than the performers' own rhythm. | Moderate. Methods A and B let the model place pauses (median 0.5-1.0 s, up to 3.5 s). C keeps 0.25-0.4 s. |
| **Timbre jump at every narrator/character join** | Energy above 4 kHz: Daniel 4.0%, Odysseus 2.1%, chorus 1.3%, crew 1.5%, **Polyphemus 0.5%** (8x less than Daniel). Spectral centroid 590 Hz Daniel vs 764 Poly, 1038 chorus, 804 crew. Each cut also swaps the apparent microphone and room. | **Real, and cuts make it audible.** A single continuous render or a shared bed hides it. |
| **Level steps** | Per-speaker integrated loudness was matched, but short-term level at the join (RMS of the last 400 ms vs the next 400 ms) differs by 6.5 dB on average, more than 6 dB at 8 of 20 joins, 22.7 dB at 32→33 (Poly line trails off, then Odysseus is 3x louder). Per-line LUFS after the speaker gain ranged -16.9 to -20.6. | Moderate. Partly natural falling intonation; per-line matching and the ride fix the rest. |
| **Inconsistent attack** | 10-90% onset rise: narrator 14 ms, Poly 7 ms, chorus 28 ms, **Odysseus 63 ms, crew 60 ms**. Hard attack next to soft attack makes every cut sound different. | Minor-moderate. 15 ms fade-in evens the worst. |
| **Speed settings 0.8/0.85/0.9** | F0 jump rate (share of adjacent voiced frames jumping more than 2 st) is 3.8% Poly (0.8), 7.4% chorus (0.85), **17% crew (0.9)** vs 3.6% Daniel and 2.7% Odysseus (1.0). Not proof of artefact, but the three slowed voices are the three with the least stable pitch track. | Possible contributor. Method C avoids the speed parameter; A and B never use it. |
| **Saved designed voices are not the previews** | CAST.md: at speed 1.0 the saved voices ran 0.61-0.71x the previews' length (Poly 4.09 s vs 6.66 s). Today's v4 renders move them further: Poly median F0 102 Hz (v2, round 2) → 119 Hz (v4, dialogue), crew 170 → 239 Hz (+6 st). | **Probable root of "the voices just don't sound good".** Voice Design voices are preview-tuned (ttv_v3); v2 and v4 renders of the saved id are different performances. The diag clip separates this from the cuts. |
| Pitch-shift artefacts | The only shifted variant in round 2 was the optional chorus +3 st file; the main proof scene (the one William heard) had no pitch shifting. | Not a cause for the proof scene. |

Net: the scene William heard had hard clicks and digital-silence holes at about 1 in 2 joins, plus 5 voices with 5 different spectral balances. Both complaints are plausible; the diag clip lets you tell which one it is.

## 2. Methods

All passages are two continuous calls per method: beats 27-40 (Nobody exchange, narrator, neighbours) and beats 63-69 (sailor). The script text is SCRIPT-V3.md verbatim, Polyphemus respelled "Pollifeemus" in speech as in round 2. Tag text never got spoken (whisper check for tag words on the A and B renders: none heard).

**Method A (Daniel only).**
- **A v4** (`eleven_v4`, stability 0.5, similarity 0.75; v4 has no style or speed). Character lines carry tags and quotes: Odysseus `[dry, controlled]`, Polyphemus `[slow, enormous, gentle]` (the pain bellow `[enormous, bellowing in pain]`), chorus `[bored, flat]`, sailor `[earnest, nervous]` variants. Narrator untagged. 1,510 characters.
- **v4 changes the narrator.** Against the D4 control (Daniel v2, round 2 narrator lines): F0 mean 123 vs 135 Hz (-1.7 st), median 125 vs 139, spectral centroid 900 vs 590 Hz, energy above 4 kHz 5.9% vs 3.8%, pace 151 vs 128 wpm. Spread is the same (3.9 vs 4.0 st). That is a different, brighter, lower, faster Daniel, so per your rule I also rendered:
- **A v2** (`eleven_multilingual_v2`, Daniel settings): no tags, character lines in quotes with short attribution on seven of eleven ("said Odysseus, quite calmly", "the giant rumbled", "a Cyclops asked, bored" ...). Narrator measures as the control (F0 133 vs 135, spread 3.8 vs 4.0, centroid 577 vs 590). 1,424 characters. The attribution words are part of the audio, so this is a test of the method, not final copy.
- Assembly: no cuts inside a passage; a slow gain ride (linear in dB between beat midpoints, at most +-4 dB) levels beats toward the median; passages joined with fade-out 60 ms / fade-in 30 ms into the room tone.

**Method B (Text to Dialogue).** `POST /v1/text-to-dialogue`, `eleven_v4`, stability 0.5, similarity 0.75, one call per passage, tags on character turns only. **The endpoint works on this plan (Creator).** No errors, one audio file per passage, and the model list says only v3 and v4 are accepted. The docs recommend at most 2,000 characters per request (ours: 1,058 and 392), at most 10 voices, 100 characters of previous_text/future_text, previous_request_ids for continuity (used for passage 2), and an `audio_effects` field (reverb environments, phone/radio filters) that I did not use.
- **B BP:** Daniel + the saved BP voices (ODY, POLY, CYC2, CREW). 1,450 characters.
- **B library:** Daniel + four of the 22 audition voices, chosen by metadata: Odysseus (dry, level) **BP Justin**, "deep, warm baritone, calm, dry understated humour"; Polyphemus (gruff giant) **BP Philip**, "deep, commanding baritone, slow, deliberate"; neighbours **BP Drew**, "deadpan, sarcasm, vocal fry"; sailor **BP Lukas**, "young, passion, hopeful, confident" (earnest). That is four character voices, not three, because the two exchanges need Odysseus, Polyphemus, a chorus voice and a sailor. 1,450 characters.
- **First library attempt (Ryan as Odysseus) was discarded:** line 28 measured spectral centroid 4,312 Hz with 46% of energy above 4 kHz and a flat spectrum to 16 kHz, i.e. a noise-like/whispered render. Re-rendered passage 1 with Justin (centroid 648 Hz, 1.5% above 4 kHz); 1,058 extra characters. The Ryan version is kept as `methodB_libRyan_scene.mp3`.
- **Narrator caveat:** the dialogue endpoint cannot use multilingual_v2, so Daniel in B is the v4-Daniel described above (F0 mean 123-125 Hz, centroid 914-927 Hz), not the Daniel you loved.
- Assembly: same as A.

**Method C (Daniel plus processing).** Daniel (v2, narrator settings, no speed change, previous/next text for context) renders the 11 character lines individually (493 characters); the 10 narrator lines are the round-2 files (Daniel, identical settings, no new characters). ffmpeg build at `/home/williamdownard/openclaw-sites/bin/ffmpeg` has rubberband, asetrate, atempo, equalizer, acompressor; used rubberband with `formant=shifted`, `pitchq=quality`, `transients=smooth`, `window=long`:

| Role | Processing | Raw → processed (same lines) |
|---|---|---|
| Odysseus | -1 st, +1 dB at 250 Hz | F0 median 143 → 139 Hz; centroid 582 → 594 Hz (barely changed) |
| Polyphemus | -3.5 st, tempo 0.88 (time-stretch), +2.5 dB at 130 Hz, -2.5 dB shelf above 4.5 kHz | median 140 → 119 Hz (-3.2 st); centroid 481 → 290 Hz; energy above 8 kHz 0.78% → 0.17%; 13% longer |
| Chorus | -1 st, tempo 0.94, high-pass 110 Hz, low-pass 5.2 kHz, -2 dB at 2.5 kHz, 3:1 compressor | median 144 → 138 Hz; pitch spread 4.0 → 3.5 st; centroid 647 → 530 Hz; above 8 kHz 1.1% → 0.09% |
| Sailor | +2.5 st, tempo 1.04, high-pass 90 Hz, +2 dB shelf at 4 kHz | median 145 → 170 Hz (+2.7 st); centroid 388 → 558 Hz |

Artefact indicators after processing: F0 jump rate 3.2/3.3/4.2/1.9% → 4.1/3.5/4.8/4.2% (Odysseus/Poly/chorus/sailor; the sailor's rise is the only visible one and is small); 0 abrupt edges after fades. Whether the giant now sounds muffled rather than large is an ear question: his centroid is half of Daniel's.
- Assembly: per-line gain to -19 LUFS (at most +-9 dB), 15/25 ms fades, gaps 0.25-0.40 s, room tone.

**Diagnostic clip.** Because the v4 dialogue render moves the saved voices (Poly +3 st, crew +6 st), a dialogue render is not the same voices. So `diag_bp_voices_smooth.mp3` re-stitches the exact round-2 per-line renders with the new join recipe (room tone, fades, per-line level match, 0.25-0.4 s gaps). Its F0 and spectra equal round 2 (Poly 102 Hz, crew 168 Hz), only the joins change: 10 abrupt events and 4 clicks → 0 and 0. The dialogue-endpoint rendering of the same BP voices is `methodB_bp_scene.mp3`.

## 3. Measured comparison

Join and edge indicators (same recipe for all; "quietest 100 ms" reads about -60 dB when a room tone is under the whole scene and -180 when there are digital-silence gaps):

| Scene | Duration s | LUFS / LRA | Abrupt events (per min) | Click events | Quietest 100 ms | Gaps between beats, min / median / max s |
|---|---|---|---|---|---|---|
| Round 2 (voices3) | 108.1 | -19.2 / 2.5 | 10 (5.5) | 4 | -180 dB | 0.25 / 0.32 / 0.40 |
| DIAG re-stitch | 111.7 | -19.2 / 2.4 | 0 | 0 | -64 dB | 0.25 / 0.32 / 0.40 |
| A v4 tags | 98.9 | -19.2 / 3.2 | 0 | 0 | -61 dB | 0.0 / 0.6 / 2.0 |
| A v2 attribution | 110.1 | -19.2 / 2.4 | 0 | 0 | -60 dB | 0.46 / 1.0 / 3.5 |
| B BP voices | 105.4 | -19.3 / 5.0 | 0 | 0 | -64 dB | 0.4 / 0.58 / 2.2 |
| B library | 101.1 | -19.3 / 3.4 | 1 (0.6) | 0 | -61 dB | 0.0 / 0.52 / 2.0 |
| C processed | 106.0 | -19.2 / 1.9 | 0 | 0 | -64 dB | 0.25 / 0.32 / 0.40 |

B library's one abrupt event is at 65.8 s, inside a model render (a word onset from near silence), not a join. Gap 0.0 in A v4 and B library means two beats ran straight into each other in the model's own performance (beats 32→33 "Nobody last" / "I am honoured").

F0 per role in each scene, mean / median Hz / spread st (wide tracker 40-400 Hz, same as round 2; medians are more trustworthy than means for the chorus and the crew):

| Scene | Narrator | Odysseus | Polyphemus | Chorus | Sailor |
|---|---|---|---|---|---|
| Round 2 | 135 / 139 / 4.0 | 97 / 101 / 3.1 | 103 / 102 / 2.3 | 116 / 105 / 4.2 | 173 / 170 / 3.2 |
| DIAG | 135 / 139 / 4.0 | 97 / 101 / 3.0 | 103 / 102 / 2.7 | 118 / 106 / 4.5 | 175 / 168 / 3.6 |
| A v4 | 123 / 125 / 3.9 | 129 / 127 / 4.3 | 132 / 123 / 6.1 | 136 / 142 / 3.8 | 160 / 167 / 4.6 |
| A v2 | 133 / 136 / 3.8 | 133 / 133 / 3.9 | 137 / 138 / 4.2 | 136 / 137 / 4.3 | 176 / 193 / 3.8 |
| B BP | 123 / 126 / 3.9 | 102 / 98 / 3.6 | 136 / 119 / 6.0 | 123 / 119 / 4.4 | 243 / 239 / 3.3 |
| B library | 125 / 127 / 4.0 | 99 / 89 / 4.5 | 155 / 140 / 6.3 | 124 / 122 / 4.0 | 172 / 177 / 5.5 |
| C | 135 / 139 / 4.0 | 132 / 139 / 3.6 | 118 / 118 / 3.3 | 133 / 138 / 3.6 | 174 / 182 / 4.0 |

Separation between the voices that share an exchange, median F0 in semitones, and pace (words per minute):

| Scene | Odysseus vs Poly (Nobody) | Poly vs chorus (neighbours) | Narrator vs Poly | Pace N / ODY / POLY / CYC / CREW |
|---|---|---|---|---|
| Round 2 / DIAG | -0.2 | -0.5 | +5.4 | 139 / 162 / 98 / 133 / 143 |
| A v4 | +0.6 | -2.5 | +0.3 | 151 / 156 / 131 / 190 / 122 |
| A v2 | -0.6 | +0.1 | -0.3 | 150 / 145 / 150 / 185 / 130 |
| B BP | -3.4 | 0.0 | +1.0 | 149 / 146 / 115 / 153 / 160 |
| B library | -7.8 | +2.4 | -1.7 | 148 / 141 / 135 / 170 / 130 |
| C | +2.8 | -2.7 | +2.8 | 135 / 147 / 135 / 123 / 113 |

Spectral centroid Hz / share of energy above 4 kHz %:

| Scene | Narrator | Odysseus | Polyphemus | Chorus | Sailor |
|---|---|---|---|---|---|
| Round 2 | 590 / 3.8 | 593 / 3.4 | 764 / 0.5 | 1038 / 1.3 | 804 / 1.5 |
| A v4 | 900 / 5.9 | 748 / 4.5 | 929 / 3.2 | 979 / 6.8 | 451 / 2.0 |
| A v2 | 577 / 3.5 | 522 / 2.7 | 465 / 2.3 | 616 / 4.0 | 486 / 1.9 |
| B BP | 927 / 6.3 | 474 / 2.3 | 1013 / 1.2 | 1148 / 2.5 | 857 / 5.4 |
| B library | 914 / 6.2 | 481 / 0.9 | 688 / 2.9 | 1033 / 6.0 | 282 / 0.2 |
| C | 585 / 3.8 | 606 / 3.7 | 289 / 0.9 | 536 / 3.7 | 636 / 3.5 |

Loudness per speaker: round 2, DIAG and C land every role within 0.7 LU of -19 (per-line matched). In A and B the one-call renders cannot be cut for per-line gain; the ride moved roles to within about 1 LU of each other in A v4 (-22.4 to -22.0 before the final -19 normalisation), A v2 (-23.1 to -22.5) and B library (-21.5 to -21.3), and within about 2.5 LU in B BP (narrator -19.9 vs sailor -21.4).

Cost (characters submitted; 24 logged calls, 7,558 in total): A v4 1,510; A v2 1,424; B BP 1,450; B library 1,450 plus the discarded Ryan attempt 1,058; C 493; slates 173; diag and reel 0. That is about 1,550 more than the 6,000 target, because A needed two versions (the v4 timbre shift) and B library needed a re-render. **Billing per character is not settled:** the account's counter went 18,132 → 21,457 (+3,325) across these calls and increments arrive late and in lumps (the log's per-call before/after columns mostly read +0 until a later call picks the change up), so the counter has not caught up or v4 and dialogue bill below 1 credit per character. A later reading is the way to check; docs bill dialogue by `inputs[].text` characters. The Creator plan accepted every call.

## 4. Recommendation by measurement (I cannot hear; William's ears decide)

1. **The cuts were bad, measurably.** Round 2 had 10 abrupt events and 4 clicks and digital-silence gaps; every rebuilt scene has 0 clicks. So "harsh cuts" is confirmed as a real defect with a mechanical fix, independent of the voices. Whether the voices are also bad is the diag clip's job.
2. **Pitch and pace separation of characters on paper:** C is the most even (Odysseus vs Poly 2.8 st, Poly vs chorus 2.7 st, narrator vs Poly 2.8 st) and keeps Daniel's timbre family and narrator spectrum (centroid 585 Hz). Its weak points: Odysseus and the chorus sit at the narrator's pitch (139 / 138 vs 139 Hz), and the giant is dark (centroid 290 Hz) where it could read as muffled.
3. **A v2 is the only one-call method that keeps the narrator exactly as loved,** but its characters sit within 0.6 st of the narrator (and of each other), so on these numbers they differ only by attribution words and by the chorus's pace (185 wpm vs about 150).
4. **A v4 and B change the narrator** (-1.7 st, +310 Hz centroid, faster). A v4's tags do create contrast in delivery (Poly's pitch spread 6.1 st vs 3.9, pace 131 vs 151 wpm, chorus 190 wpm) but not in pitch (Poly 123 vs narrator 125 Hz).
5. **B works technically and has the widest voice separation** (library: Odysseus 89 Hz, chorus 122, sailor 177), but in the library set Polyphemus (Philip, 140 Hz median) is *higher* than Odysseus (Justin, 89 Hz): the "enormous" tag did not make the deep voice deeper, which is the opposite of what the giant needs. B BP moves the saved voices (Poly +3 st, crew +6 st), so it is not the voices you picked.
6. **If you want the narrator untouched and the cuts gone, my measured order is C, then A v2 + a processed character layer, then B for character-to-character exchanges only.** (A hybrid is possible: dialogue-endpoint calls for the narrator-free exchanges, v2 Daniel for narration, joined with the same fades and room tone; not built.)

## 5. What to tell me

Listen in this order and reply in one line each:

1. **`diag_bp_voices_smooth.mp3`**: same voices as round 2, cuts rebuilt. Say one of: *"cuts fixed, voices still bad"* (then the problem is the designed voices and Methods A/B/C are the way forward), *"cuts fixed, voices fine now"* (then keep the BP cast and use this join recipe, no new voices), or *"still harsh"* with a timestamp (then I look at the line, not the joins).
2. **`reel_methods.mp3`** (7:20, River slates "Method A, one / two", "Method B", "Method C"; or the separate files). Per method tell me: can you tell who is speaking without the sprites (yes / mostly / no), does it still sound like the Daniel you love in the narration (yes / slightly off / no), and any single moment that sounds wrong with the timestamp.
3. **A one vs A two:** if A one (tags) sounds more alive but the narrator is different, say "keep v4 feel, want v2 narrator", and I try v4 on narration-free character lines with v2 narration spliced by crossfade.
4. **C:** is the giant big, or muffled? (my knob is the 4.5 kHz shelf and the -3.5 st). Are Odysseus and the chorus too close to the narrator? (my knob is pitch and the chorus's band-limiting).
5. **B:** does the dialogue-style overlap and pacing feel more natural than C even though the narrator is v4-Daniel? Is the giant Philip deep enough, or is he too light for a giant?
6. Anything you want carried forward unchanged (a voice, a method, the room tone), and anything to drop.

## Settings and methods quick reference

- Round-3 join recipe (`scripts/asm.py`, `assemble_all.py`): 15 ms fade-in, 20-25 ms fade-out (60 ms at passage tails) on every segment; continuous -62 dBFS pink room tone (70 Hz-5 kHz, +-1 dB 0.15 Hz drift) under everything; per-line gain to -19 LUFS (max +-9 dB) for separate renders, slow gain ride (+-4 dB) for one-call renders; final two-pass loudnorm to -19 LUFS, true peak -1.5, 192 kbps. A true 40 ms equal-power crossfade function exists (`asm.xfade`) but no join needed it: every join sits in a room-tone gap with fades on both sides. A shared reverb was left out on purpose (the narrator should stay as dry as he was).
- Tooling: run with `/home/williamdownard/openclaw-sites/clips-venv/bin/python -I` (numpy only); key from `ELEVENLABS_API_KEY` env; ffmpeg `/home/williamdownard/openclaw-sites/bin/ffmpeg`.
