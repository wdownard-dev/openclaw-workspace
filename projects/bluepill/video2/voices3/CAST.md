# CAST.md: locked cast for video 1 (The Myth Ledger), proof scene, 2026-11-13

**I cannot hear any of these clips.** Everything below is voice ids, settings and measurements. William's ears decide. Nothing was uploaded, posted or sent; no full script was recorded.

## Cast

All lines use model `eleven_multilingual_v2` (Daniel is the same model as pick #5). Voice Design previews were made with `eleven_ttv_v3`; I rendered each saved voice through both `eleven_multilingual_v2` and `eleven_v3` (see Verification) and v2 was the closer match, so v2 is the one used. `previous_text`/`next_text` (free, not billed) gave each line its neighbours for continuity.

| Role | Voice name | Voice id | Source (William's pick) | Settings used in the proof scene | F0 mean / median Hz, spread st (proof lines) | Chosen clip F0 mean (round 2) |
|---|---|---|---|---|---|---|
| Narrator | Daniel (premade) | `onwK4e9ZLuTAKqWW03F9` | #5 `D4_control_r1_multilingual_v2` | stability 0.5, style 0.2, speed 1.0, similarity 0.75, boost on (unchanged) | 135 / 139, 3.95 | 137 |
| Odysseus | **BP Odysseus** | `VjxhlwVjjBpI2LsBesOS` | #9 Voice Design ODY A, preview 3 of 3 | stability 0.45, style 0.25, speed 1.0, similarity 0.75, boost on | 98 / 101, 3.1 | 98 |
| Polyphemus | **BP Polyphemus** | `uM5YTm59xrfl2vmPc47V` | #26 Voice Design POLY B, preview 2 of 3 | stability 0.45, style 0.25, speed 0.8, similarity 0.75, boost on | 104 / 102, 2.4 | 106 |
| Cyclops chorus | **BP Cyclops chorus** | `5yjDNqcqMzshLpW5Xc91` | #54 Voice Design CYC2 B, preview 2 of 3 | stability 0.45, style 0.25, speed 0.85, similarity 0.75, boost on | 118 / 106, 4.4 | 106 |
| Crew / sailor | **BP Crew** | `F8If4viPI1f5VSMBsTfa` | #68 Voice Design CREW B, preview 1 of 3 | stability 0.45, style 0.25, speed 0.9, similarity 0.75, boost on | 177 / 172, 3.8 | 177 |

- The four saved voices keep the id of the preview they came from (the previews were still valid, so no regeneration and no different take). Saved in My Voices as category `generated`; each description stores the prompt id (`ODY-A`, `POLY-B`, `CYC2-B`, `CREW-B`), the slate number and the design prompt.
- Slots: 22 audition voices + 4 = **26 of 30** used. Nothing deleted.
- The speeds below 1.0 for POLY, CYC2 and CREW are mine, not William's: the saved voices read faster than the previews (see Verification), and the previews' slow cadence is what William picked. Change the numbers in `scripts/proof_gen.py` (`SETTINGS`) if the pace is wrong.
- F0 = wide-range tracker (40-400 Hz) over all of that speaker's proof lines. The CYC2 mean (118) is pulled up by tracker jumps; its median (106) is the better number and matches the chosen clip.

## Verification (step 2)

One short line per saved voice, same text as the first line of the chosen clip, speed 1.0, stability 0.5, style 0.2. The chosen clip's first line was cut at whisper word times. Raw numbers: `_work/verify_metrics.json`, audio in `verify/`.

| Voice | Line | Duration chosen / v2 / v3 (s) | F0 mean chosen / v2 / v3 (Hz) | Spread chosen / v2 / v3 (st) |
|---|---|---|---|---|
| ODY | "You have eaten ... Have some wine." | 4.60 / 4.55 / 3.76 | 103 / 99 / 101 | 3.15 / 3.09 / 3.60 |
| POLY | "More. Now tell me your name ..." | 6.66 / 4.09 / 4.72 | 105 / 107 / 105 | 2.13 / 2.55 / 1.91 |
| CYC2 | "Pollifeemus, what is wrong? ..." | 4.94 / 3.53 / 4.80 | 108 / 104 / **138** | 1.64 / 4.06 / 5.56 |
| CREW | "Take the cheese. Let's go." | 1.84 / 1.21 / 1.28 | 177 / 148 / 189 (medians 145 / 145 / 143) | 5.95 / 2.17 / 4.50 |

- Pitch matches within 0.7 st for ODY, POLY and CYC2 on v2. CREW's mean is 3 st low on v2 but the median is identical (145 Hz); a 1.5 s clip is too short for the mean to mean much.
- `eleven_v3` pulls CYC2 up 4 st, so it was rejected. v2 was used for everyone.
- **Pace differs**: at speed 1.0 the saved voices run 0.61-0.71 of the chosen clips' duration for POLY, CYC2 and CREW (the previews are slow, with long pauses). ODY matches (0.99). That is why the proof scene uses speeds 0.8, 0.85 and 0.9. Voice Design voices vary between takes, so spread differences of 1-2 st are within normal wobble.

## Pitch distinctness (step 3)

Median F0 from the proof lines (chosen-clip tracker means in brackets): Daniel 139 (137), ODY 101 (98), POLY 102 (106), CYC2 106 (106), CREW 172 (177).

| Pair | Distance on medians (means) |
|---|---|
| ODY vs POLY | 0.2 st (1.0) |
| POLY vs CYC2 | 0.7 st (2.2, mean skewed by tracker jumps) |
| ODY vs CYC2 | 0.8 st (3.2, same skew) |
| CREW vs everyone | 9 st above POLY, about 5 st above Daniel's median: safe |

**Risk: real.** ODY, POLY and the chorus all sit at about 100-106 Hz. Pitch will not tell them apart; what remains is accent and timbre (Greek-Cypriot-leaning baritone, West Country bass, Midlands flat), pace (POLY about 98 wpm, CYC2 133, ODY 162) and pitch spread (POLY 2.4 st, ODY 3.1, CYC2 4.4). Those differences are real on paper, but I cannot confirm by ear that they carry. The two direct exchanges are the worry: POLY versus the other Cyclopes (beats 37-39) is the tighter pair, 0.7 st apart. The Nobody exchange (ODY versus POLY) is about 0.2 st apart, but ODY is about 1.6x faster and the lines alternate on shots that show the speaker, so it is the lesser risk. The neighbours are also meant to be a group of different Cyclopes, so a similar-sounding chorus is a story risk as well as a clarity risk.

**Mitigation, no change to any pick: shift only the chorus up in post.** `rubberband` pitch shift with formants shifted (so it sounds like a smaller or younger speaker, not a sped-up one). Measured chorus median: unshifted 106 Hz, +2 st 119 Hz, +3 st 126 Hz.

- +3 st puts the chorus 3.7 st above POLY and 3.8 above ODY, but only 1.7 st below Daniel (139). It trades one collision for another: the neighbours and Daniel never share a line, but the chorus would be the closest voice to the narrator in pitch.
- +2 st (119 Hz) is 2.7 st above POLY and 2.7 st below Daniel. This is my recommendation if the A/B sounds like a different person and not a processed one.
- If neither sounds right, the zero-cost fallbacks are acting direction in v3-style text and delivery pace (already different), and leaning on the on-screen sprites.

**A/B for William** (neighbours exchange, beats 37-39, POLY unshifted in all):
- `ab/neighbours_ABC.mp3` (1:06): A unshifted, 1.5 s silence, B +2 st, 1.5 s silence, C +3 st.
- Separate files: `ab/neighbours_A_unshifted.mp3`, `ab/neighbours_B_chorus_plus2st.mp3`, `ab/neighbours_C_chorus_plus3st.mp3`.
- Full scene with the chorus at +3 st: `proof_scene_chorus_plus3st.mp3` (the main `proof_scene.mp3` is the unshifted cast, William's picks as is).

## Proof scene (step 4)

`proof_scene.mp3`: 1:48, 192 kbps mono, **-19.2 LUFS integrated, true peak -1.8 dBFS, LRA 2.5**. Beats 27-40 and 63-69 of SCRIPT-V3.md (the Nobody exchange 28-33, the neighbours 37-39, the sailor 64-68) with the narrator lines between them (27, 29, 34, 35, 36, 40, 63, 65, 67, 69); 1,253 characters including two extra flatness lines (the Polyphemus name in line 37 is respelled "Pollifeemus" as in video 1).

- Loudness: each speaker's lines got one common gain to -19 LUFS integrated for that speaker (Daniel +4.3 dB, ODY -0.6, POLY -1.5, CYC2 -3.5, CREW -3.8), then a two-pass linear loudnorm of the whole scene to -19 LUFS, peak limited below -1.5 dBFS. The final reading is 0.2 LU off the -19 target.
- Gaps: 0.25 s between two characters, 0.4 s between two narrator lines, 0.32 s otherwise. Edge silence trimmed with a -50 dB gate.
- Timeline: `_work/assemble.json`; line-by-line log (time, clip, file, voice id, characters, model, settings, duration): `voice_log.csv`.

## One-word-line flatness (p10-p90 F0 range inside the word; FLAT = under 2.0 st)

| Word | File | F0 median Hz | p10-p90 st | Result |
|---|---|---|---|---|
| "Nope." (CREW) | `proof_lines/beat66_CREW.mp3` | 177 | 7.5 | ok, rising |
| "Hello?" (CREW) | `beat64_CREW.mp3` | 208 | 12.6 | ok (a question; the tracker has a few jumps) |
| "Ah." (ODY, rendered inside "And then who moves the stone? Ah.", beats 19-20) | `extra_ODY_Ah_ctx.mp3` (2.38-2.85 s) | 81 | 2.3 | borderline, just over the flat line; sits low and mostly falling, 74-86 Hz |
| "Sheep." (CYC2, rendered alone with previous text "I keep sheep.") | `extra_CYC2_Sheep.mp3` | n/a | n/a | **unmeasurable**: the tracker jumps between about 100 and 280 Hz (the "sh" and the "ee" confuse it), the same limit round 2 hit on this word. Not flat by the numbers, but I do not trust them. Listen to it. |
| "Nobody." as ODY's last word of "My name is Nobody." | `beat31_ODY.mp3` | 98 | 1.7 | **FLAT**. The script asks for "Nobody." with a perfectly straight face, so flat may be right; check by ear. |
| "Nobody." as POLY's first word of line 32 | `beat32_POLY.mp3` | 110 | 4.0 | ok |
| "I am honoured." (ODY, three words) | `beat33_ODY.mp3` | not measured (the aligner heard "honored") | n/a | listen; the script wants it flat |

Words under 0.7 s are short for the tracker. Flatness numbers are hints; listening is the check.

## Spend

ElevenLabs characters requested by my calls: 408 (verification, four lines through two models) + 1,253 (proof scene, including 39 for the "Ah." and "Sheep." extras) = **1,661** (sum of `voice_log.csv`). No Voice Design preview was regenerated (no preview expired). The account counter went from 17,404 to 18,132 (+728), less than the 1,661 requested, so the counter lags or counts these calls differently; treat 1,661 as the upper figure. Remaining by the counter: 112,868 of 131,000.

## Files

- `proof_scene.mp3`, `proof_scene_chorus_plus3st.mp3`, `ab/`, `proof_lines/` (raw per-line), `verify/`, `voice_log.csv`, `CAST.md`
- `scripts/`: `save_voices.py`, `verify_gen.py`, `verify_cmp.py`, `proof_gen.py`, `assemble.py`, `analyze.py` (run with `/home/williamdownard/openclaw-sites/clips-venv/bin/python -I`; the key comes only from `ELEVENLABS_API_KEY`)
- `_work/`: `saved_voices.json`, `verify_metrics.json`, `analysis.json`, `assemble.json`
