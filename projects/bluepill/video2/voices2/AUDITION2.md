# AUDITION2.md: voice round 2 for video 1 (The Myth Ledger), 2026-11-13

**I cannot hear any of these clips.** Every pick below comes from voice metadata, the prompts and the measurements. William's ears decide. Nothing was uploaded, posted or sent; only audition lines were generated (no full script).

**Listen in this order:**
1. `reel2_daniel.mp3` (2:17): slate, then clip, six Daniel variants numbered 1-6.
2. `reel2_characters.mp3` (4:54): per role (Odysseus, Polyphemus, the Cyclopes, the crew): the best preview of each of the three designed prompts, then the best-scoring library or OpenAI voice.
3. `reel2_extra.mp3` (3:22): the next candidates (extra library and OpenAI voices, the pitched-down Polyphemus, the ram and prayer lines).
Every reel clip is edge-trimmed, long gaps shortened to 0.7 s and level-matched to -19 LUFS so loudness does not bias you; slates are spoken by one fixed voice, River. Files in `narrator_daniel/` and `characters/` are raw. The slate number is the # in the table below.

**Reference traits** (REVIEW-ref-vs-draft section 4): 178 wpm overall, pitch spread 4.7 semitones, loudness range 3.6 LU, 1.9 pauses of 0.3 s or more per minute, performed voices for characters. Round-1 Daniel (N02, 143-character clip): 158 wpm, 3.43 st, 1.4 LU. Caveat: 12-27 second clips, one take each. Pitch spread and LRA wobble by a semitone or a couple of LU between takes of the same voice; read the numbers as hints.

**What the finisher did** (the first worker was cut off by the usage limit before writing this file): measured every clip again from the metric files it left (`_work/metrics_*.json`, `_work/words.json`; 6 + 73 clips, all present, none zero-length or corrupt), checked both reels, rebuilt `reel2_characters.mp3` and added `reel2_extra.mp3` (see section 6), backfilled one missing log row, and wrote this file. No audio was generated.

## 1. All clips, numbered

Number = the number spoken on the slate in the reels (reel column: D = `reel2_daniel.mp3`, C = `reel2_characters.mp3`, X = `reel2_extra.mp3`, blank = only the raw file exists). F0 mean is the wide-range tracker (40-400 Hz) in Hz; spread = std of voiced F0 in semitones with the reference teardown's own definition (autocorrelation 70-300 Hz, corr > 0.5). wpm is words / speech span (first to last sound); the bracket is an articulation pace with every gap of 0.3 s or more removed. It runs high because it also removes normal sentence stops, so use it only to compare clips of the same line, and read the plain wpm as the pace you would actually get. Voice Design previews also carry a few seconds of silence between lines, which lowers their plain wpm. Pauses/min counts gaps of 0.3 s or more (reference definition).

### Daniel narrator variants (`narrator_daniel/`, 266-310 characters, SCRIPT-V3 beats 01, 02, 08, 11)

| # | reel | file | engine / model | voice | settings / tags | s | wpm | F0 mean Hz (spread st) | LUFS / LRA | pauses/min | hint |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | D | `narrator_daniel/D1_multilingual_v2_speed1.1_style0.25.mp3` | ElevenLabs eleven_multilingual_v2 | Daniel (premade, onwK4e9ZLuTAKqWW03F9) | eleven_multilingual_v2; stability 0.5, style 0.25, speed 1.1, similarity 0.75, boost on; | 20.57 | 157 | 131 (3.32) | -23.1 / 1.9 | 29.7 |  |
| 2 | D | `narrator_daniel/D2a_v4_tagA_speed1.0.mp3` | ElevenLabs eleven_v4 | Daniel (premade, onwK4e9ZLuTAKqWW03F9) | eleven_v4; stability 0.5, style 0.2, speed 1.0, similarity 0.75, boost on; tag [dry, deadpan, amused documentary narrator] | 19.36 | 166 | 131 (4.6) | -22.2 / 4.1 | 18.7 |  |
| 3 | D | `narrator_daniel/D2b_v4_tagB_speed1.0.mp3` | ElevenLabs eleven_v4 | Daniel (premade, onwK4e9ZLuTAKqWW03F9) | eleven_v4; stability 0.5, style 0.2, speed 1.0, similarity 0.75, boost on; tag [wry, unhurried, quietly amused] | 20.4 | 158 | 121 (5.13) | -23.0 / 4.9 | 20.9 |  |
| 4 | D | `narrator_daniel/D3_v4_tagA_speed1.1.mp3` | ElevenLabs eleven_v4 | Daniel (premade, onwK4e9ZLuTAKqWW03F9) | eleven_v4; stability 0.5, style 0.2, speed 1.1, similarity 0.75, boost on; tag [dry, deadpan, amused documentary narrator] | 19.68 | 163 | 129 (4.34) | -22.0 / 4.3 | 21.5 |  |
| 5 | D | `narrator_daniel/D4_control_r1_multilingual_v2.mp3` | ElevenLabs eleven_multilingual_v2 | Daniel (premade, onwK4e9ZLuTAKqWW03F9) | eleven_multilingual_v2; stability 0.5, style 0.2, speed 1.0, similarity 0.75, boost on; | 21.69 | 149 | 137 (3.77) | -23.2 / 1.6 | 28.2 |  |
| 6 | D | `narrator_daniel/D5_v4_tagA_speed1.2.mp3` | ElevenLabs eleven_v4 | Daniel (premade, onwK4e9ZLuTAKqWW03F9) | eleven_v4; stability 0.5, style 0.2, speed 1.2, similarity 0.75, boost on; tag [dry, deadpan, amused documentary narrator] | 19.76 | 162 | 125 (4.34) | -22.5 / 4.1 | 21.4 |  |

### Odysseus (`characters/ODY/`)

| # | reel | file | engine / model | voice or prompt id | settings / tags | s | wpm (art.) | F0 mean Hz (spread st) | LUFS / LRA | pauses/min | hint |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 7 |  | `characters/ODY/design/ODY_designA_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design ODY A** (prompt ODY-A, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 16.12 | 146 (217) | 99 (3.11) | -18.4 / 4.4 | 22.4 | very deep |
| 8 |  | `characters/ODY/design/ODY_designA_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design ODY A** (prompt ODY-A, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 16.51 | 143 (210) | 93 (2.82) | -18.4 / 3.1 | 22.0 | very deep |
| 9 | C | `characters/ODY/design/ODY_designA_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design ODY A** (prompt ODY-A, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 15.57 | 153 (214) | 98 (3.29) | -18.7 / 4.2 | 23.5 | very deep |
| 10 |  | `characters/ODY/design/ODY_designB_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design ODY B** (prompt ODY-B, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 12.59 | 190 (259) | 112 (4.3) | -18.7 / 3.7 | 29.3 |  |
| 11 | C | `characters/ODY/design/ODY_designB_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design ODY B** (prompt ODY-B, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 14.52 | 162 (235) | 107 (3.4) | -18.4 / 3.2 | 24.9 |  |
| 12 |  | `characters/ODY/design/ODY_designB_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design ODY B** (prompt ODY-B, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 13.79 | 175 (244) | 103 (3.76) | -18.9 / 3.8 | 22.5 |  |
| 13 |  | `characters/ODY/design/ODY_designC_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design ODY C** (prompt ODY-C, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 17.16 | 138 (203) | 111 (2.75) | -17.3 / 5.4 | 21.2 |  |
| 14 | C | `characters/ODY/design/ODY_designC_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design ODY C** (prompt ODY-C, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 17.87 | 132 (194) | 101 (3.2) | -18.3 / 3.5 | 20.3 | very deep |
| 15 |  | `characters/ODY/design/ODY_designC_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design ODY C** (prompt ODY-C, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 20.85 | 114 (199) | 100 (3.75) | -18.8 / 5.8 | 20.5 |  |
| 16 |  | `characters/ODY/eleven_lib/C02_JustinTrustingCalm_ODY_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **JustinTrustingCalm** (library voice 'BP Justin (audition)'), line ODY | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [dry, amused, controlled] | 12.8 | 184 (233) | 122 (5.72) | -23.4 / 2.4 | 28.3 | very wide pitch |
| 17 | C | `characters/ODY/eleven_lib/C01_DanielWarmBaritone_ODY_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **DanielWarmBaritone** (library voice 'BP Daniel (audition)'), line ODY | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [dry, amused, controlled] | 13.36 | 180 (227) | 117 (4.02) | -23.9 / 3.7 | 27.7 |  |
| 18 | X | `characters/ODY/eleven_lib/C03_RyanUnhurried_ODY_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **RyanUnhurried** (library voice 'BP Ryan (audition)'), line ODY | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [dry, amused, controlled] | 14.0 | 169 (211) | 161 (4.17) | -21.8 / 3.5 | 26.0 |  |
| 19 | X | `characters/ODY/openai/ash_ODY.mp3` | OpenAI gpt-4o-mini-tts | **ash**, line ODY | gpt-4o-mini-tts; instructions: Voice: warm, dry mid-baritone, wry and controlled, intelligent and quietly amused. Delivery: unhurried, understated, a faint smile in the voice, deadpan on 'My name is Nobody.' and 'I am honoured.' Never heroic, never trailer-like. | 16.8 | 150 (193) | 109 (2.89) | -22.9 / 2.1 | 23.0 |  |
| 20 |  | `characters/ODY/openai/onyx_ODY.mp3` | OpenAI gpt-4o-mini-tts | **onyx**, line ODY | gpt-4o-mini-tts; instructions: Voice: a calm low baritone, dry and amused. Delivery: measured and precise, light irony, composed, like a clever man hiding a joke. No dramatic emphasis. | 12.77 | 186 (235) | 89 (1.64) | -23.6 / 2.6 | 28.7 | very deep; flat pitch |
| 21 |  | `characters/ODY/openai/echo_ODY.mp3` | OpenAI gpt-4o-mini-tts | **echo**, line ODY | gpt-4o-mini-tts; instructions: Voice: easy mid-range male, sardonic and relaxed. Delivery: conversational, controlled, dry humour, not heroic. | 13.46 | 182 (229) | 107 (3.0) | -20.4 / 5.0 | 28.0 |  |

### Polyphemus (`characters/POLY/`)

| # | reel | file | engine / model | voice or prompt id | settings / tags | s | wpm (art.) | F0 mean Hz (spread st) | LUFS / LRA | pauses/min | hint |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 22 |  | `characters/POLY/design/POLY_designA_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design POLY A** (prompt POLY-A, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 17.08 | 102 (153) | 95 (2.64) | -21.4 / 4.7 | 21.2 | very deep |
| 23 | C | `characters/POLY/design/POLY_designA_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design POLY A** (prompt POLY-A, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 18.05 | 97 (153) | 98 (2.74) | -19.6 / 3.3 | 26.8 | very deep |
| 24 |  | `characters/POLY/design/POLY_designA_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design POLY A** (prompt POLY-A, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 20.27 | 86 (157) | 101 (2.99) | -18.8 / 6.7 | 20.8 |  |
| 25 |  | `characters/POLY/design/POLY_designB_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design POLY B** (prompt POLY-B, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 24.19 | 72 (111) | 120 (4.32) | -18.2 / 11.9 | 22.4 | big loudness swings |
| 26 | C | `characters/POLY/design/POLY_designB_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design POLY B** (prompt POLY-B, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 21.97 | 80 (124) | 106 (2.94) | -18.8 / 5.0 | 24.8 |  |
| 27 |  | `characters/POLY/design/POLY_designB_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design POLY B** (prompt POLY-B, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 27.17 | 64 (110) | 105 (2.77) | -19.6 / 6.0 | 19.9 |  |
| 28 |  | `characters/POLY/design/POLY_designC_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design POLY C** (prompt POLY-C, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 16.12 | 109 (149) | 155 (3.61) | -14.6 / 17.5 | 15.0 | big loudness swings |
| 29 | C | `characters/POLY/design/POLY_designC_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design POLY C** (prompt POLY-C, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 12.83 | 138 (166) | 119 (2.72) | -18.4 / 2.1 | 19.0 |  |
| 30 |  | `characters/POLY/design/POLY_designC_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design POLY C** (prompt POLY-C, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 16.35 | 107 (180) | 150 (4.06) | -18.0 / 7.4 | 22.2 |  |
| 31 | X | `characters/POLY/post/POLY_designA_p2_pitchdown4st.mp3` | local pitch shift | design POLY A preview 2, local pitch shift down 4 semitones, duration unchanged (method not recorded in the scripts; no API call) | n/a (local post-processing) | 18.05 | 97 (153) | 80 (3.96) | -20.3 / 3.5 | 26.7 | very deep |
| 32 |  | `characters/POLY/eleven_lib/C06_UjjalSleepy_POLY_NOBODY_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **UjjalSleepy** (library voice 'BP UjjalSleepy (audition)'), line POLY_NOBODY | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [gentle, slow, enormous] | 12.96 | 139 (173) | 159 (5.48) | -25.8 / 10.2 | 19.1 | very wide pitch; big loudness swings |
| 33 |  | `characters/POLY/eleven_lib/C06_UjjalSleepy_POLY_RAM_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **UjjalSleepy** (library voice 'BP UjjalSleepy (audition)'), line POLY_RAM | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [gentle, slow, enormous] | 9.2 | 136 (185) | 168 (4.68) | -29.7 / 5.5 | 27.1 |  |
| 34 |  | `characters/POLY/eleven_lib/C06_UjjalSleepy_POLY_PRAYER_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **UjjalSleepy** (library voice 'BP UjjalSleepy (audition)'), line POLY_PRAYER | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [gentle, slow, enormous, solemn] | 11.52 | 139 (177) | 136 (3.62) | -23.4 / 4.2 | 26.7 |  |
| 35 |  | `characters/POLY/eleven_lib/C04_MichaelMoody_POLY_NOBODY_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **MichaelMoody** (library voice 'BP MichaelMoody (audition)'), line POLY_NOBODY | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [gentle, slow, enormous] | 13.84 | 127 (156) | 144 (5.01) | -19.3 / 8.6 | 17.6 | very wide pitch; big loudness swings |
| 36 |  | `characters/POLY/eleven_lib/C04_MichaelMoody_POLY_RAM_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **MichaelMoody** (library voice 'BP MichaelMoody (audition)'), line POLY_RAM | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [gentle, slow, enormous] | 9.44 | 131 (167) | 137 (4.37) | -23.4 / 3.0 | 19.7 |  |
| 37 |  | `characters/POLY/eleven_lib/C04_MichaelMoody_POLY_PRAYER_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **MichaelMoody** (library voice 'BP MichaelMoody (audition)'), line POLY_PRAYER | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [gentle, slow, enormous, solemn] | 12.4 | 129 (145) | 139 (4.22) | -17.7 / 3.7 | 14.9 |  |
| 38 | X | `characters/POLY/eleven_lib/C05_PhilipQuietAuthority_POLY_NOBODY_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **PhilipQuietAuthority** (library voice 'BP PhilipQuietAuthority (audition)'), line POLY_NOBODY | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [gentle, slow, enormous] | 12.64 | 141 (181) | 121 (3.6) | -20.8 / 6.4 | 19.4 |  |
| 39 | X | `characters/POLY/eleven_lib/C05_PhilipQuietAuthority_POLY_RAM_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **PhilipQuietAuthority** (library voice 'BP PhilipQuietAuthority (audition)'), line POLY_RAM | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [gentle, slow, enormous] | 8.32 | 151 (200) | 124 (3.58) | -23.8 / 2.7 | 22.6 |  |
| 40 | X | `characters/POLY/eleven_lib/C05_PhilipQuietAuthority_POLY_PRAYER_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **PhilipQuietAuthority** (library voice 'BP PhilipQuietAuthority (audition)'), line POLY_PRAYER | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [gentle, slow, enormous, solemn] | 10.8 | 148 (205) | 109 (2.5) | -20.9 / 2.8 | 34.1 |  |
| 41 | X | `characters/POLY/openai/onyx_POLY_NOBODY.mp3` | OpenAI gpt-4o-mini-tts | **onyx**, line POLY_NOBODY | gpt-4o-mini-tts; instructions: Voice: enormous, very deep, slow. Delivery: gentle, simple sincerity with childlike literalness, gravelly but not a villain, no growl, warm and trusting. | 11.76 | 151 (207) | 92 (1.81) | -22.1 / 2.0 | 31.2 | very deep; flat pitch |
| 42 |  | `characters/POLY/openai/onyx_POLY_RAM.mp3` | OpenAI gpt-4o-mini-tts | **onyx**, line POLY_RAM | gpt-4o-mini-tts; instructions: Voice: enormous, very deep, slow. Delivery: gentle, simple sincerity with childlike literalness, gravelly but not a villain, no growl, warm and trusting. | 7.75 | 161 (214) | 89 (1.25) | -23.1 / 2.2 | 24.2 | very deep; flat pitch |
| 43 |  | `characters/POLY/openai/onyx_POLY_PRAYER.mp3` | OpenAI gpt-4o-mini-tts | **onyx**, line POLY_PRAYER | gpt-4o-mini-tts; instructions: Voice: enormous, very deep, slow. Delivery: gentle, simple sincerity with childlike literalness, gravelly but not a villain, no growl, warm and trusting. | 11.52 | 139 (193) | 91 (1.31) | -22.9 / 2.4 | 32.1 | very deep; flat pitch |
| 44 | C | `characters/POLY/openai/ash_POLY_NOBODY.mp3` | OpenAI gpt-4o-mini-tts | **ash**, line POLY_NOBODY | gpt-4o-mini-tts; instructions: Voice: very deep and gravelly, huge and soft-spoken. Delivery: slow, deliberate, sincere, almost tender, innocent and literal, never menacing. | 13.7 | 130 (185) | 100 (2.57) | -23.5 / 2.1 | 31.5 | very deep |
| 45 | X | `characters/POLY/openai/ash_POLY_RAM.mp3` | OpenAI gpt-4o-mini-tts | **ash**, line POLY_RAM | gpt-4o-mini-tts; instructions: Voice: very deep and gravelly, huge and soft-spoken. Delivery: slow, deliberate, sincere, almost tender, innocent and literal, never menacing. | 10.75 | 115 (175) | 114 (3.16) | -20.9 / 3.1 | 23.1 |  |
| 46 | X | `characters/POLY/openai/ash_POLY_PRAYER.mp3` | OpenAI gpt-4o-mini-tts | **ash**, line POLY_PRAYER | gpt-4o-mini-tts; instructions: Voice: very deep and gravelly, huge and soft-spoken. Delivery: slow, deliberate, sincere, almost tender, innocent and literal, never menacing. | 11.86 | 136 (177) | 98 (2.62) | -23.2 / 5.0 | 31.4 | very deep |
| 47 |  | `characters/POLY/openai/ballad_POLY_NOBODY.mp3` | OpenAI gpt-4o-mini-tts | **ballad**, line POLY_NOBODY | gpt-4o-mini-tts; instructions: Voice: low, rumbling, slow and wounded. Delivery: gentle sincerity, simple and childlike, heavy with feeling but not theatrical, no villain growl. | 12.72 | 146 (187) | 154 (3.17) | -24.9 / 4.0 | 20.2 |  |
| 48 |  | `characters/POLY/openai/ballad_POLY_RAM.mp3` | OpenAI gpt-4o-mini-tts | **ballad**, line POLY_RAM | gpt-4o-mini-tts; instructions: Voice: low, rumbling, slow and wounded. Delivery: gentle sincerity, simple and childlike, heavy with feeling but not theatrical, no villain growl. | 7.51 | 166 (207) | 153 (2.81) | -26.9 / 3.8 | 24.8 | quiet file |
| 49 |  | `characters/POLY/openai/ballad_POLY_PRAYER.mp3` | OpenAI gpt-4o-mini-tts | **ballad**, line POLY_PRAYER | gpt-4o-mini-tts; instructions: Voice: low, rumbling, slow and wounded. Delivery: gentle sincerity, simple and childlike, heavy with feeling but not theatrical, no villain growl. | 13.7 | 122 (158) | 144 (3.84) | -26.8 / 4.2 | 23.5 |  |

### The Cyclopes (`characters/CYC2/`)

| # | reel | file | engine / model | voice or prompt id | settings / tags | s | wpm (art.) | F0 mean Hz (spread st) | LUFS / LRA | pauses/min | hint |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 |  | `characters/CYC2/design/CYC2_designA_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CYC2 A** (prompt CYC2-A, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 18.29 | 112 (148) | 190 (4.91) | -21.3 / 3.8 | 19.4 |  |
| 51 | C | `characters/CYC2/design/CYC2_designA_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CYC2 A** (prompt CYC2-A, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 17.48 | 104 (162) | 128 (4.03) | -16.0 / 5.0 | 21.6 |  |
| 52 |  | `characters/CYC2/design/CYC2_designA_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CYC2 A** (prompt CYC2-A, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 19.64 | 99 (155) | 136 (5.05) | -19.2 / 4.8 | 23.8 | very wide pitch |
| 53 |  | `characters/CYC2/design/CYC2_designB_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CYC2 B** (prompt CYC2-B, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 18.76 | 103 (164) | 147 (5.67) | -15.3 / 5.9 | 21.3 | very wide pitch |
| 54 | C | `characters/CYC2/design/CYC2_designB_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CYC2 B** (prompt CYC2-B, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 19.07 | 94 (146) | 106 (3.4) | -17.9 / 5.1 | 25.9 | very deep |
| 55 |  | `characters/CYC2/design/CYC2_designB_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CYC2 B** (prompt CYC2-B, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 21.0 | 83 (141) | 109 (4.24) | -18.9 / 4.1 | 20.0 |  |
| 56 |  | `characters/CYC2/design/CYC2_designC_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CYC2 C** (prompt CYC2-C, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 14.03 | 131 (206) | 203 (3.96) | -19.2 / 6.3 | 27.2 | high; 'Sheep' unmeasurable |
| 57 | C | `characters/CYC2/design/CYC2_designC_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CYC2 C** (prompt CYC2-C, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 15.73 | 112 (184) | 158 (2.19) | -18.4 / 2.8 | 27.0 | flat pitch |
| 58 |  | `characters/CYC2/design/CYC2_designC_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CYC2 C** (prompt CYC2-C, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 16.12 | 109 (163) | 175 (2.37) | -19.8 / 6.4 | 22.6 | flat pitch |
| 59 | C | `characters/CYC2/eleven_lib/C07_DrewDeadpan_CYC2_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **DrewDeadpan** (library voice 'BP DrewDeadpan (audition)'), line CYC2 | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [bored, flat, deadpan] | 12.16 | 146 (186) | 130 (3.8) | -19.3 / 1.6 | 25.2 | 'Sheep' unmeasurable; name misheard 'Olafemus' |
| 60 | X | `characters/CYC2/eleven_lib/C09_DeadpanCynic_CYC2_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **DeadpanCynic** (library voice 'BP DeadpanCynic (audition)'), line CYC2 | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [bored, flat, deadpan] | 11.92 | 150 (182) | 141 (4.16) | -22.6 / 4.0 | 25.9 | 'Sheep' unmeasurable |
| 61 |  | `characters/CYC2/eleven_lib/C08_DannyMonotone_CYC2_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **DannyMonotone** (library voice 'BP DannyMonotone (audition)'), line CYC2 | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [bored, flat, deadpan] | 11.76 | 151 (189) | 119 (5.5) | -21.7 / 7.9 | 26.0 | very wide pitch; 'Sheep' unmeasurable |
| 62 | X | `characters/CYC2/openai/echo_CYC2.mp3` | OpenAI gpt-4o-mini-tts | **echo**, line CYC2 | gpt-4o-mini-tts; instructions: Voice: bored, flat, tired working-class neighbour woken at night. Delivery: monotone, irritated, sighing, mid-low register, no energy, zero enthusiasm, the one word 'Sheep.' dead and flat. | 10.8 | 173 (210) | 118 (3.01) | -20.2 / 1.7 | 23.9 |  |
| 63 |  | `characters/CYC2/openai/sage_CYC2.mp3` | OpenAI gpt-4o-mini-tts | **sage**, line CYC2 | gpt-4o-mini-tts; instructions: Voice: weary, flat, gruff. Delivery: deadpan, bored, put-upon, slow, as if woken at three in the morning and unimpressed. | 14.62 | 128 (188) | 180 (2.73) | -32.8 / 5.2 | 26.6 | quiet file; name misheard 'Paul of Venus' |
| 64 |  | `characters/CYC2/openai/fable_CYC2.mp3` | OpenAI gpt-4o-mini-tts | **fable**, line CYC2 | gpt-4o-mini-tts; instructions: Voice: low-energy, nasal and fed up. Delivery: flat, irritated, sleepy, working-class, monotone with weary sighs. | 14.3 | 130 (207) | 134 (3.53) | -21.5 / 3.4 | 31.3 | 'Sheep' FLAT (1.3 st); name misheard 'Polyfamous' |

### The crew (`characters/CREW/`)

| # | reel | file | engine / model | voice or prompt id | settings / tags | s | wpm (art.) | F0 mean Hz (spread st) | LUFS / LRA | pauses/min | hint |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 65 |  | `characters/CREW/design/CREW_designA_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CREW A** (prompt CREW-A, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 14.52 | 88 (242) | 122 (1.63) | -20.7 / 9.0 | 25.3 | flat pitch; big loudness swings; 'Nope' FLAT (1.74 st) |
| 66 |  | `characters/CREW/design/CREW_designA_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CREW A** (prompt CREW-A, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 14.21 | 97 (245) | 116 (1.36) | -18.0 / 4.7 | 32.4 | flat pitch; 'Nope' FLAT (1.79 st) |
| 67 | C | `characters/CREW/design/CREW_designA_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CREW A** (prompt CREW-A, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 18.91 | 68 (231) | 121 (2.69) | -19.7 / 10.8 | 22.5 | big loudness swings |
| 68 | C | `characters/CREW/design/CREW_designB_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CREW B** (prompt CREW-B, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 13.01 | 99 (215) | 177 (3.82) | -19.1 / 7.6 | 23.5 |  |
| 69 |  | `characters/CREW/design/CREW_designB_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CREW B** (prompt CREW-B, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 13.09 | 97 (236) | 159 (4.08) | -17.5 / 7.2 | 32.2 |  |
| 70 |  | `characters/CREW/design/CREW_designB_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CREW B** (prompt CREW-B, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 15.31 | 83 (217) | 145 (3.6) | -20.1 / 6.1 | 27.8 | 'Hello' FLAT (0.42 st) |
| 71 |  | `characters/CREW/design/CREW_designC_p1.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CREW C** (prompt CREW-C, §Voice Design); preview 1 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 13.48 | 95 (255) | 126 (2.2) | -18.7 / 9.3 | 27.2 | flat pitch; big loudness swings |
| 72 | C | `characters/CREW/design/CREW_designC_p2.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CREW C** (prompt CREW-C, §Voice Design); preview 2 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 12.59 | 102 (212) | 126 (2.55) | -18.3 / 3.6 | 34.0 |  |
| 73 |  | `characters/CREW/design/CREW_designC_p3.mp3` | ElevenLabs Voice Design (eleven_ttv_v3) | **Voice Design CREW C** (prompt CREW-C, §Voice Design); preview 3 of 3 | eleven_ttv_v3, guidance 4, loudness 0.5; line text only (no tag) | 15.65 | 82 (210) | 128 (2.32) | -19.5 / 6.7 | 23.4 | flat pitch; 'Hello' FLAT (0.26 st); 'Nope' FLAT (1.54 st) |
| 74 | X | `characters/CREW/eleven_lib/C11_LukasExcitedYouth_CREW_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **LukasExcitedYouth** (library voice 'BP LukasExcitedYouth (audition)'), line CREW | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [earnest, nervous] | 9.36 | 138 (183) | 210 (5.18) | -20.0 / 2.7 | 32.8 | high; very wide pitch; 'Hello' FLAT (0.84 st) |
| 75 | X | `characters/CREW/eleven_lib/C10_HarryAnxiousFighter_CREW_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **HarryAnxiousFighter** (library voice 'BP HarryAnxiousFighter (audition)'), line CREW | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [earnest, nervous] | 9.12 | 142 (197) | 238 (3.6) | -19.6 / 2.5 | 40.4 | high |
| 76 | C | `characters/CREW/eleven_lib/C12_TimmyAnxiousNerd_CREW_v4.mp3` | ElevenLabs eleven_v4 (library voice) | **TimmyAnxiousNerd** (library voice 'BP TimmyAnxiousNerd (audition)'), line CREW | eleven_v4; stability 0.5, style 0.3, speed 1.0, similarity 0.75, boost on; tag [earnest, nervous] | 9.12 | 142 (179) | 227 (3.95) | -23.3 / 1.8 | 27.0 | high; 'Hello' unmeasurable |
| 77 |  | `characters/CREW/openai/verse_CREW.mp3` | OpenAI gpt-4o-mini-tts | **verse**, line CREW | gpt-4o-mini-tts; instructions: Voice: young, earnest everyman sailor, mid-high, a little frightened. Delivery: breathless, quick, nervous, sincere; 'Nope.' short and scared, 'Where's the nose?' puzzled. | 9.5 | 135 (210) | 163 (3.1) | -24.1 / 1.7 | 45.2 |  |
| 78 |  | `characters/CREW/openai/alloy_CREW.mp3` | OpenAI gpt-4o-mini-tts | **alloy**, line CREW | gpt-4o-mini-tts; instructions: Voice: young man, nervous and honest. Delivery: shaky, breathy, earnest, worried, not comedic. | 10.46 | 137 (250) | 140 (3.06) | -18.9 / 1.7 | 45.7 | 'Hello' unmeasurable; 'Nope' unmeasurable |
| 79 |  | `characters/CREW/openai/coral_CREW.mp3` | OpenAI gpt-4o-mini-tts | **coral**, line CREW | gpt-4o-mini-tts; instructions: Voice: young, bright and anxious. Delivery: fast, breathless, earnest, a little scared, plain and sincere. | 6.58 | 203 (323) | 222 (3.99) | -26.3 / 2.7 | 48.4 | high; 'Hello' FLAT (1.68 st) |


## 2. Voice Design: what it offered and what it cost

- **Offered:** `POST /v1/text-to-voice/design`, model `eleven_ttv_v3`, `guidance_scale` 4, `loudness` 0.5, a text description (native language, gender, age, quality, persona, emotion, timbre and pacing) plus the audition line. Each call returned **3 previews** (3 different voices from one prompt). 12 calls (4 roles x 3 prompts) = **36 previews**, 8-12 s per call, all HTTP 200 on this Creator plan, so the feature is available without a plan change.
- **Cost:** per the log, 1,911 characters (the audition text once per call: 201 x 3 Odysseus, 153 x 3 Polyphemus, 160 x 3 Cyclopes, 123 x 3 crew); the two other previews of a call were logged at 0. That is a reading of the account counter behaviour in round 1, not a verified invoice line: the subscription counter lags (see section 7), so I could not confirm the per-call charge.
- **Slots:** previews are temporary (their ids are not in My Voices). Nothing was saved, so no designed voice occupies a slot. To use a designed voice for a full script it must be saved (create voice from preview) and takes **one slot each** (8 free of 30, see section 8); saving does not cost characters by itself. Previews cannot be re-rendered with other lines until saved.
- **Limits seen:** the voice is fixed by the preview, so the first line decides; previews carry 1-4 s of silence between lines (lowers plain wpm); three previews have loudness range above 10 LU (Polyphemus B p1 11.9, Polyphemus C p1 17.5, crew A p3 10.8; outliers, flagged in the table).

### Design prompts (full text, as sent)

Audition line (same for all three prompts of a role): ODY = the 4-line Odysseus text; POLY = 'More. Now tell me your name... Nobody last.'; CYC2 = the 3-line Cyclopes text incl. 'Sheep.'; CREW = the 6-line crew text incl. 'Hello?' and 'Nope.'

- **ODY-A** (clips 7, 8, 9): Native English, light Mediterranean-tinged speech, a faint Greek-Cypriot lilt without caricature. Male, 40-45. Studio quality. Persona: wry ship captain, clever and controlled. Emotion: amused, dry, composed. Warm mid-baritone with a smooth, slightly husky timbre; unhurried, precise pacing with the faintest smile in the voice, intelligent understatement, never heroic or trailer-like.
- **ODY-B** (clips 10, 11, 12): Native English, neutral American, general Midwest, mild and unforced. Male, 35-40. Studio quality. Persona: dry-witted engineer who has seen everything. Emotion: amused, calm, mildly sardonic. Warm, medium-low baritone with a relaxed, conversational timbre; moderate pace, light ironic emphasis, controlled and a little tired, not dramatic.
- **ODY-C** (clips 13, 14, 15): Native English, soft Scottish lowland intonation, understated. Male, 50-55. Very good quality. Persona: seasoned, sharp-eyed negotiator. Emotion: wry, patient, quietly confident. Rich lower-mid baritone with a dry, slightly gravelly texture; measured pace with small deadpan pauses, intelligent and amused, never booming.
- **POLY-A** (clips 22, 23, 24): Native English, deep rural American South, slow and soft. Male, 45-55. Studio quality. Persona: enormous gentle shepherd, simple and sincere. Emotion: gentle, earnest, puzzled. Very deep, low-pitched, gravelly bass with a warm, rumbling timbre; slow, deliberate pacing, childlike literalness, no villain growl.
- **POLY-B** (clips 25, 26, 27): Native English, rural West Country England, thick and warm. Male, 55-65. Good quality. Persona: huge, lonely farmer who talks to his sheep. Emotion: tender, sincere, a little sad. Extremely deep, resonant bass-baritone with a rough, breathy texture; very slow pace with long soft vowels, simple and trusting, never menacing.
- **POLY-C** (clips 28, 29, 30): Native English, heavy Newfoundland-style rural intonation, unhurried. Male, 60-65. Good quality. Persona: gentle giant, big-hearted and slow of thought. Emotion: kind, earnest, innocent. Deep, booming yet soft bass with a gravelly, worn timbre; slow, steady pacing, sincere and literal-minded, warm rather than threatening.
- **CYC2-A** (clips 50, 51, 52): Native English, gruff Northern English, thick Yorkshire-style intonation. Male, 45-50. Good quality. Persona: grumpy neighbour woken in the middle of the night. Emotion: bored, irritated, flat. Mid-low, rough, nasal timbre; slow, sighing, monotone delivery with weary emphasis, working-class and unimpressed.
- **CYC2-B** (clips 53, 54, 55): Native English, Midlands (Black Country style) intonation, plain and flat. Male, 55-60. Good quality. Persona: tired pub regular who has heard every excuse. Emotion: deadpan, weary, put-upon. Low-mid, dry and slightly raspy; slow pace, very little pitch variation, mumbling a little, bored.
- **CYC2-C** (clips 56, 57, 58): Native English, Northern Irish-tinged working-class speech, blunt and sleepy. Female, 40-50. Good quality. Persona: irritated neighbour in a dressing gown. Emotion: flat, annoyed, tired. Low-mid, gravelly, a little hoarse from sleep; unhurried, monotone with sharp tired sighs, unimpressed.
- **CREW-A** (clips 65, 66, 67): Native English, soft Irish lilt, light and natural. Male, 20-25. Good quality. Persona: nervous young sailor, an everyman. Emotion: earnest, frightened, breathless. Mid-high, slightly thin and boyish timbre; quick, breathy pacing with small catches in the voice, sincere and a little out of breath.
- **CREW-B** (clips 68, 69, 70): Native English, West Country England, mild rural intonation. Male, 20-25. Good quality. Persona: honest young deckhand out of his depth. Emotion: anxious, earnest, worried. Mid-high, bright and slightly nasal; fast, breathless delivery, rising worried inflection, plain and sincere.
- **CREW-C** (clips 71, 72, 73): Native English, neutral American with a hint of Appalachian twang. Male, 18-22. Good quality. Persona: scared young crewman trying to stay brave. Emotion: nervous, earnest, shaky. High-mid, light and slightly cracked timbre; rapid breathless speech, tense and sincere, not comedic.

## 3. Character distinctness (F0 mean, semitones re 100 Hz)

**Set 1 (widest separation, all gaps at least 2 st)**

| | Daniel (D2a, #2) | ODY #14 | POLY #31 | CYC2 #57 | CREW #76 |
|---|---|---|---|---|---|
| **Daniel (D2a, #2)** (131 Hz, +4.7 st) | - | 4.6 | 8.6 | 3.2 | 9.5 |
| **ODY #14** (101 Hz, +0.1 st) | 4.6 | - | 4.0 | 7.8 | 14.1 |
| **POLY #31** (80 Hz, -3.9 st) | 8.6 | 4.0 | - | 11.8 | 18.1 |
| **CYC2 #57** (158 Hz, +7.9 st) | 3.2 | 7.8 | 11.8 | - | 6.3 |
| **CREW #76** (227 Hz, +14.2 st) | 9.5 | 14.1 | 18.1 | 6.3 | - |

Smallest gap: **3.21 st** (meets the 2 st rule).

**Set 2 (best total score from the selection script, gap 2.03 st; Odysseus is a library voice named Daniel, a different voice from the narrator)**

| | Daniel (D2a, #2) | ODY #17 | POLY #23 | CYC2 #57 | CREW #76 |
|---|---|---|---|---|---|
| **Daniel (D2a, #2)** (131 Hz, +4.7 st) | - | 2.0 | 5.0 | 3.2 | 9.5 |
| **ODY #17** (117 Hz, +2.7 st) | 2.0 | - | 3.0 | 5.2 | 11.5 |
| **POLY #23** (98 Hz, -0.3 st) | 5.0 | 3.0 | - | 8.3 | 14.5 |
| **CYC2 #57** (158 Hz, +7.9 st) | 3.2 | 5.2 | 8.3 | - | 6.3 |
| **CREW #76** (227 Hz, +14.2 st) | 9.5 | 11.5 | 14.5 | 6.3 | - |

Smallest gap: **2.03 st** (meets the 2 st rule).

**Set 3 (best-scoring clip per role, no gap rule; shows the problem)**

| | Daniel (D2a, #2) | ODY #14 | POLY #23 | CYC2 #54 | CREW #76 |
|---|---|---|---|---|---|
| **Daniel (D2a, #2)** (131 Hz, +4.7 st) | - | 4.6 | 5.0 | 3.6 | 9.5 |
| **ODY #14** (101 Hz, +0.1 st) | 4.6 | - | 0.4 | 1.0 | 14.1 |
| **POLY #23** (98 Hz, -0.3 st) | 5.0 | 0.4 | - | 1.4 | 14.5 |
| **CYC2 #54** (106 Hz, +1.1 st) | 3.6 | 1.0 | 1.4 | - | 13.1 |
| **CREW #76** (227 Hz, +14.2 st) | 9.5 | 14.1 | 14.5 | 13.1 | - |

Smallest gap: **0.45 st** (fails the 2 st rule).

Notes: F0 mean is a proxy for the voice's register; two voices 2 st apart can still sound alike if the accent and delivery match, and two voices closer than 2 st can still be told apart by accent. The set-1 Cyclopes is a designed *female* voice (prompt CYC2-C); that is a casting decision for William. Crew is much higher than everyone else (210-230 Hz library voices), which is intended for a young, frightened crewman. Designed Odysseus, Polyphemus and Cyclopes-B all sit within 1.5 st of each other (98-106 Hz) when taken as the top-scoring preview, so the design prompts did not separate those three by register; accent, pace and delivery would have to.

## 4. Suggested picks per role (by measurement; I cannot hear them)

Scores come from `scripts/select2.py`: lower = closer to explicit targets that are my reading of the brief, not facts about taste. Targets: **Odysseus** warm dry mid-baritone, 90-125 Hz, spread about 4.5 st, 185 wpm, LRA about 3.6. **Polyphemus** enormous, very deep and slow, 60-95 Hz, 150 wpm, not flat. **Cyclopes** bored and flat, 105-150 Hz, spread about 3 st. **Crew** young and breathless, 150-240 Hz, spread about 4.5 st, 'Nope.' and 'Hello?' not flat. Designed voices use the best of their three previews.

**Odysseus**
1. **#14** `ODY_designC_p2.mp3`: 101 Hz mean, 3.2 st spread, 132 wpm, -18.3 LUFS / 3.5 LU. Best score (1.28). Scottish-lowland negotiator prompt; deep (98-101 Hz), a little slow (132 wpm); preview 1 and 3 of the same prompt are slower still (138, 114 wpm).
2. **#17** `C01_DanielWarmBaritone_ODY_v4.mp3`: 117 Hz mean, 4.02 st spread, 180 wpm, -23.9 LUFS / 3.7 LU. Library voice 'Daniel (warm baritone)', a different voice from the narrator but the same name: say so when you listen, so the two are not confused. Closest to the reference pace and spread, but its mean F0 is only 2.0 st from the narrator.
3. **#19** `ash_ODY.mp3`: 109 Hz mean, 2.89 st spread, 150 wpm, -22.9 LUFS / 2.1 LU. OpenAI ash with acting instructions; flatter (2.9 st) and slowish (150 wpm), peaks at -5.6 dB. Also on the list: designed A p3 (#9) and B p2 (#11).

**Polyphemus**
1. **#23** `POLY_designA_p2.mp3`: 98 Hz mean, 2.74 st spread, 97 wpm, -19.6 LUFS / 3.3 LU. Best score (0.75): deep (98 Hz), slow (97 wpm), not flat (2.7 st). The slowest-sounding of the picks; 'Nobody.' ok (2.5 st).
2. **#31** `POLY_designA_p2_pitchdown4st.mp3`: 80 Hz mean, 3.96 st spread, 97 wpm, -20.3 LUFS / 3.5 LU. The same take pitched down 4 st locally: 80 Hz, 'enormous' on paper, spread 3.96 st. Pitch shifting can add a processed sound; I cannot hear whether it does.
3. **#44** `ash_POLY_NOBODY.mp3`: 100 Hz mean, 2.57 st spread, 130 wpm, -23.5 LUFS / 2.1 LU. OpenAI ash, 97-100 Hz, 130 wpm, flat-ish (2.6 st). Rams and prayer lines #45, #46.
Library voices are poor fits by measurement (113-157 Hz and loudness range 6-10 LU on the Nobody line); OpenAI onyx is the deepest (89-93 Hz) but the flattest (1.3-1.8 st).

**Cyclopes chorus**
1. **#54** `CYC2_designB_p2.mp3`: 106 Hz mean, 3.4 st spread, 94 wpm, -17.9 LUFS / 5.1 LU. Best score (2.18): Midlands 'tired pub regular', slow (94 wpm), 98 Hz median, 3.4 st; loudness range 5.1 LU is wider than flat; 'Sheep.' ok.
2. **#59** `C07_DrewDeadpan_CYC2_v4.mp3`: 130 Hz mean, 3.8 st spread, 146 wpm, -19.3 LUFS / 1.6 LU. Library Drew with [bored, flat, deadpan]: steadiest levels (LRA 1.6), 146 wpm. 'Sheep.' could not be measured; the speech check heard the name as 'Olafemus', so the name spelling may need a respell.
3. **#57** `CYC2_designC_p2.mp3`: 158 Hz mean, 2.19 st spread, 112 wpm, -18.4 LUFS / 2.8 LU. Female, irritated neighbour: flattest designed take (2.2 st), 158 Hz; this is the one that clears the 2 st rule against Daniel and Odysseus (section 3).

**Crew / sailor**
1. **#76** `C12_TimmyAnxiousNerd_CREW_v4.mp3`: 227 Hz mean, 3.95 st spread, 142 wpm, -23.3 LUFS / 1.8 LU. Best score (1.22): 227 Hz, 142 wpm, 'Nope.' not flat (3.3 st); 'Hello?' could not be measured (too few voiced frames).
2. **#74** `C11_LukasExcitedYouth_CREW_v4.mp3`: 210 Hz mean, 5.18 st spread, 138 wpm, -20.0 LUFS / 2.7 LU. Widest pitch (5.2 st) and 'Nope.' lively (12 st range); but 'Hello?' is FLAT (0.8 st).
3. **#68** `CREW_designB_p1.mp3`: 177 Hz mean, 3.82 st spread, 99 wpm, -19.1 LUFS / 7.6 LU. Only designed take with a wide pitch (3.8 st) and a lively 'Hello?' (16 st) and 'Nope.' (3.4 st); slow (99 wpm) and big loudness swings (7.6 LU). Designed A and C crew voices sit at 114-125 Hz median, which is low for a young sailor.

**One-word and short lines (flatness check).** F0 range (10th-90th percentile, semitones) inside the word, found with a local speech aligner; FLAT = under 2.0 st with at least 6 voiced frames. A 0.2-0.3 s word gives only 6-20 voiced frames, so this is a rough flag. 'Ah.' is not in the round-2 text set.

- FLAT: C11_LukasExcitedYouth_CREW_v4 Hello? 0.84 st; coral_CREW Hello? 1.68 st; fable_CYC2 Sheep. 1.3 st; CREW_designA_p1 Nope. 1.74 st; CREW_designA_p2 Nope. 1.79 st; CREW_designB_p3 Hello? 0.42 st; CREW_designC_p3 Hello? 0.26 st; CREW_designC_p3 Nope. 1.54 st.
- Not measurable (word too short, or aligner heard a different word): 16 cases, mostly 'Hello?' and 'Sheep.'; listen to these first. Clips: C10_HarryAnxiousFighter_CREW_v4 Hello?; C12_TimmyAnxiousNerd_CREW_v4 Hello?; alloy_CREW Hello?; alloy_CREW Nope.; verse_CREW Hello?; C07_DrewDeadpan_CYC2_v4 Sheep.; C08_DannyMonotone_CYC2_v4 Sheep.; C09_DeadpanCynic_CYC2_v4 Sheep.; echo_CYC2 Sheep.; sage_CYC2 Sheep.; CYC2_designC_p1 Sheep.; CREW_designA_p1 Hello?; CREW_designA_p2 Hello?; CREW_designB_p2 Hello?; CREW_designC_p1 Hello?; CREW_designC_p2 Hello?.
- 'Nobody.' (Polyphemus): no clip is flat. Narrowest: OpenAI onyx 2.1 st, library Philip 2.2 st. 'Sheep.' (Cyclopes): the only measured flat one is OpenAI fable (1.3 st); the library and OpenAI echo/sage clips could not be measured.

## 5. Daniel: best variant against the reference

| trait | reference | D1 (#1) | D2a (#2) | D2b (#3) | D3 (#4) | D4 control (#5) | D5 (#6) |
|---|---|---|---|---|---|---|---|
| pace, wpm | 178 (target 170-178) | 157 | 166 | 158 | 163 | 149 | 162 |
| pitch spread, st | 4.7 | 3.32 | 4.6 | 5.13 | 4.34 | 3.77 | 4.34 |
| loudness range, LU | 3.6 | 1.9 | 4.1 | 4.9 | 4.3 | 1.6 | 4.1 |
| pauses per minute (0.3 s or more) | 1.9 | 29.7 | 18.7 | 20.9 | 21.5 | 28.2 | 21.4 |
| F0 mean, Hz | - | 131 | 131 | 121 | 129 | 137 | 125 |

- **Best by closeness: D2a (#2): eleven_v4, tag `[dry, deadpan, amused documentary narrator]`, stability 0.5, style 0.2, similarity 0.75, speaker boost on, speed 1.0.** 166 wpm (12 under the reference), 4.6 st (reference 4.7), LRA 4.1 LU (0.5 over). Score 1.4 against 2.1-5.4 for the others.
- **Tag A against tag B:** D2b (tag `[wry, unhurried, quietly amused]`) is deeper (121 Hz) and wider (5.1 st, 4.9 LU) but slower (158 wpm).
- **Speed does not buy pace in v4:** 1.0, 1.1 and 1.2 give 166, 163 and 162 wpm. The extra 'speed' setting is not the lever; if William wants 174 wpm, a 5% time-stretch in post on D2a (166 x 1.05 = 174, pitch kept) is the cleaner route (not done here).
- **v4 against multilingual_v2 (what round 1 used):** the v4 clips more than double the loudness range (4.1-4.9 against 1.6-1.9 LU) and widen the pitch spread by about 1 st, matching the reference far better than the control (D4: 149 wpm, 3.8 st, 1.6 LU) or D1 (157 wpm, 3.3 st, 1.9 LU).
- **Pauses:** every variant sits at 19-30 pauses per minute against the reference's 1.9. Same rule as the reference script (gaps 18 dB under the median, 0.3 s or more); the v4 takes have the fewest (19-22) against 28-30 for multilingual_v2. This is largely something editing can tighten (gap trimming), not a voice property.
- **Tags:** a speech check of all six clips shows the tag text is not spoken aloud (all start 'Twelve men follow Odysseus into a cave...'); D2a heard 'a one-eyed kind' for 'the one-eyed kind', a small drift worth checking by ear.
- Loudness is -22 to -23 LUFS raw (peaks -2.5 to -6 dB), no clipping.

## 6. Reels: checks

| reel | duration | integrated | LRA | true peak | contents (slate numbers, in order) |
|---|---|---|---|---|---|
| `reel2_daniel.mp3` | 2:16.8 | -19.5 LUFS | 3.9 LU | -1.3 dBFS | intro 'Daniel, narrator variants', then 1, 2, 3, 4, 5 (control), 6 (bonus) |
| `reel2_characters.mp3` | 4:53.7 | -19.6 LUFS | 4.6 LU | -1.3 dBFS | intro; Odysseus 9, 11, 14, 17; Polyphemus 23, 26, 29, 44; Cyclopes 51, 54, 57, 59; crew 67, 68, 72, 76 |
| `reel2_extra.mp3` | 3:22.0 | -19.5 LUFS | 4.2 LU | -1.3 dBFS | Odysseus 19, 18; Polyphemus 31, 41, 38, 39 (ram), 40 (prayer), 45 (ram), 46 (prayer); Cyclopes 62, 60; crew 74, 75 |
- **Slate mapping:** slate number = the # of the clip (numbering from `scripts/plan.py`, the same one the table uses), verified by transcribing the slates in the rebuilt reels and by building each reel from a manifest (`_work/reel_manifest.json`). The Daniel reel was already correct (slates one to six at the expected offsets, six clips in the right order, 'control' on 5, 'bonus' on 6) and was left as it was.
- **Characters reel rebuilt:** the first worker's `reel2_characters.mp3` (6:41) had been built before `plan.py` and `slates2.py` were last edited, so it did not match the current plan (extras mixed in, none of the main/extra split). It is kept as `_work/reel2_characters_OLD_prePlanEdit.mp3`. The new main reel and the extras reel use only existing slate audio (no new TTS).
- **No clipping, level-matched:** every clip is brought to -19 LUFS (alimiter at 0.89, true peak -1.3 dBFS in all three reels, nothing above 0 dBFS); reel-level -19.5 to -19.6 LUFS. Slates are spoken at the same level as the clips.
- **Not in a reel:** the two unselected previews of each of the 12 design prompts (24 of the 36 design previews) and the other library/OpenAI voices for the ram and prayer lines. They exist as raw files and in the table.

## 7. Spend

| item | characters |
|---|---|
| multilingual_v2 Daniel (D1, D4) | 532 |
| eleven_v4 (4 Daniel + 18 library clips) | 4,286 |
| Voice Design (12 calls) | 1,911 |
| slates (River, multilingual_v2) | 797 |
| OpenAI | 2,604 |
| **ElevenLabs total** | **7,526** (plan credits, about $1.37 of plan value at $0.182 per 1,000; no extra charge) |
| OpenAI gpt-4o-mini-tts | 2,604 characters, 3.5 minutes of audio, about $0.05 (at about $0.015/min) |

- Log: `voice_log.csv` has 119 rows from the first worker; one row (OA-coral-CREW, 123 characters) was missing though the file exists and was backfilled with a marked note; no new call. The log also contains one slate (n77) not used by any reel.
- **Quota (ElevenLabs subscription endpoint, Creator, limit 131,000):** before round 2: not recorded by the first worker; the round-1 report predicted about 16,660 used once all its calls were counted (counter then showed 12,931). **Read now (10:0x ET): 17,404 used, 113,596 left.** The counter lags the calls (round-1 note in TOOLS.md), so this reading does not yet include all of round 2. Expected true figure once it catches up: about 16,660 + 7,526 = **about 24,200 used, about 106,800 left** (an estimate; Voice Design may bill differently from 1 character per text character). Re-read the endpoint later to confirm.
- No tier change, no overage, nothing deleted.

## 8. My Voices slot usage

- Voices named 'BP ... (audition)': **22** (the 22 added in round 1). With the 21 premade voices the account lists 43 voices. Slots: **22 of 30 used, 8 free** (the API field `voice_slots_used` reads 0, so I am counting the library voices myself, as the round-1 note did).
- **Designed voices created this round: 0** (previews only; see section 2). Nothing was deleted or added.
- Audition voices: Alex, Daniel, Danny, Deadpan Cynic with a Slight Li, Drew, Hey Its Brad, Jarnathan Cross, Justin, Kurt, Liam Callahan, Lukas, Michael Dan, Michael Moody, Nathaniel C, Oliver Silk, Philip, Russell, Ryan, Spuds Oxley, Stephen Davis, Timmy, Ujjal.

## 9. What to tell me (so round 3 is targeted)

Answer any of these in a word per voice or per role, using the slate number:
- **Narrator (Daniel, clips 1-6):** closest to what you want? Too slow, too flat, too dry or too lively? Does the tag version (2, 3, 4, 6) sound better than the plain version (1, 5)? Fast enough, or should I speed it up in post (about 5%)?
- **Too deep / too high:** say 'deeper' or 'lighter' by number (Polyphemus is the usual one: 3 of the designed bass takes are 95-100 Hz, #31 is the pitched-down one at 80 Hz).
- **Too young / too old:** most useful for Odysseus (designs A 40-45, B 35-40, C 50-55) and the crew (18-25).
- **Too cartoonish / too theatrical:** especially Polyphemus and the Cyclopes; say if you want 'plain' instead.
- **Wrong accent:** Odysseus tried Greek-Cypriot (A), neutral American (B) and Scottish (C); Polyphemus Southern US (A), West Country (B), Newfoundland (C); Cyclopes Yorkshire (A), Black Country (B), Northern Irish female (C); crew Irish (A), West Country (B), Appalachian American (C). Say which accent family to keep or drop.
- **Too much energy / too flat:** the crew's 'Nope.' and 'Hello?', the Cyclopes' 'Sheep.' and Polyphemus' 'Nobody.' (the flagged lines in section 4).
- **Name:** 'Polyphemus' (written 'Pollifeemus' for the TTS) was misheard by the speech check in the Cyclopes line for Drew, sage and fable; tell me if any sound wrong.
- **Casting:** is a female Cyclopes chorus (#57) acceptable? Should Odysseus avoid the library 'Daniel' name?
- **Keep / drop:** name up to 3 numbers per role to keep; I will use those as the base and save them as designed voices (1 slot each, 8 free).
- **Round-3 candidate moves:** re-prompt the winner of each role with the adjectives you give me, make a second Voice Design batch from the best prompt, try speed 1.0 plus a 5% post stretch on Daniel, and test the full cast on a 20-second scene.
