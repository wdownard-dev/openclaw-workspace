# Chapter-card stings (video 1)

Five 2.0 s mono 44.1 kHz WAV stings, one per chapter card. **Licence: none needed.** They are synthesised from scratch by `video1/make_stings.py` in pure Python (sine oscillators plus low-passed random noise). No samples, loops, presets or third-party audio files were used, so there is no licensing question.

| File | Chapter | Root | Colour |
|---|---|---|---|
| `sting_ch2_poem.wav` | 1. The poem as Homer tells it | D2 (73.4 Hz) | plain fifth |
| `sting_ch3_skull.wav` | 2. The skull | C2 (65.4 Hz) | minor third, darker |
| `sting_ch4_cyclopes.wav` | 3. The other Cyclopes | E2 (82.4 Hz) | fifth |
| `sting_ch5_limits.wav` | 4. What we can and cannot say | A1 (55 Hz) | minor third, sober |
| `sting_ch6_verdict.wav` | Verdict and next | D2 (73.4 Hz) | major third, slightly resolved |

## How each is built
- Low pad: root and a 0.45% detuned copy, a soft octave (plus detuned copy), and a fifth or third (plus detuned copy) with a slow 0.45 Hz tremolo of about 6%.
- Noise swell: white noise through two one-pole low-pass filters (about 350 Hz), shaped by a raised-cosine swell that peaks mid-sting. Seeded RNG, so renders are reproducible.
- Envelope: raised-cosine attack to the peak at 0.8 s, cosine decay to silence at 1.75 s, then 0.25 s of true silence. 5 ms fade-in at the start. No transient, so no ding or whoosh.
- Level: calibrated to **-29.0 LUFS integrated** (ffmpeg loudnorm measurement, three-pass gain trim); true peaks are -14 to -17 dBFS. The voice track is at -22 LUFS.

## Placement
Each sting starts at the first sample of its 2.0 s card window (the end of the previous paragraph's audio) and ends exactly at the card end, so it is silent for its last 0.25 s plus the 0.05 s pre-roll before the next first word. `assemble.py` writes them to `audio/stings_track.wav` (same length as the narration) so the final mix can set their level; `narration.wav` is voice plus stings, `narration_voice_only.wav` is the voice alone.

Regenerate: `python3 video1/make_stings.py`, then `python3 video1/assemble.py` and `python3 video1/gen_retimed_md.py`.
