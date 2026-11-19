# MUSIC.md: ambient bed and audio mix for the video 1 draft

Nothing third-party is used anywhere in the audio. Narration is the ElevenLabs track already approved ("sounds good"), the five chapter stings are the existing synthesised stings (`video1/audio/stings/`), and the bed below is generated in code. Licence: own work, no samples, no libraries of sound, nothing to clear.

## How the bed was made
Script: `pipeline/remotion-v1/make_audio.js` (plain Node, no audio libraries; sample loop over 612.8 s at 44.1 kHz, stereo).
- **Pad:** for each chord root, four sine partials (root, fifth, octave, a very soft ninth at 14 % level), each with a second harmonic at 18 %, detuned about -0.24 % in the left channel and +0.24 % in the right (slow beating = width, no chorus effect needed). Each partial has its own slow level LFO (periods 17, 23, 29 and 35 s), so the bed breathes without any rhythm.
- **Air:** brown-ish noise through two one-pole lowpass filters, level slowly modulated (29 s period), summed under the pad.
- **No melody, no drums, no plucks.** Nothing moves faster than the LFOs.
- **Roots follow the chapters** and match the roots of the stings so the two never clash: D2 (73.4 Hz) for cold open, stakes and chapter I; C2 (65.4 Hz) for chapter II; E2 (82.4 Hz) for chapter III; A2 (110 Hz) for chapter IV; D2 for the verdict. Changes are 10 s smoothstep crossfades centred 5 s before each chapter card.
- **Fades:** 4 s in at the start, 6 s out at the end.
- **Ducking:** the bed is ducked 6.5 dB whenever the narration is active (50 ms RMS window, attack 0.12 s, release 0.9 s) and comes back up during the 2.0 s chapter-card pauses and at the end card.

## Levels in the final mix (measured with the bundled ffmpeg `loudnorm` measurement pass; the build has no `ebur128`, so these are loudnorm figures: integrated LUFS and true peak)
| Component | Integrated loudness |
|---|---|
| Narration alone (processed) | -16.15 LUFS |
| Bed alone, un-ducked reference | -29.5 LUFS (brief: under -28) |
| Bed alone as it plays (ducked) | -35.2 LUFS |
| Stings alone (as played) | -25.1 LUFS (9.0 dB under the narration) |
| **Final mix** | **-16.15 LUFS, true peak -1.06 dBFS** (see `draft/QA-REPORT.md` for the figures measured on the encoded mp4) |

## Voice processing
The narration (-22 LUFS raw, peaks near -1 dBFS) was lifted by 10.35 dB with light dynamics control: 65 Hz high-pass, a soft-knee compressor (threshold -27 dB, ratio 2.6:1, attack 6 ms, release 160 ms), then a 4 ms look-ahead peak limiter at -1.9 dBFS sample peak; a second look-ahead limiter on the mix bus at -1.7 dBFS. All dynamics are plain DSP in `make_audio.js` because the bundled ffmpeg build has no compressor or limiter filters. I cannot judge it by ear: listen for pumping on the loudest sentences and for the bed audibility under the voice (it is meant to be felt rather than heard).

## Regenerate
`cd pipeline/remotion-v1 && node make_audio.js` writes `public/audio/mix.wav` and `audio_report.json`. Environment overrides: `TARGET_LUFS`, `MUSIC_LUFS`, `ST_REL` (sting level relative to the voice gain), `VOICE_GAIN`.
