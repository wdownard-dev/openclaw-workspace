# BRIEF-FINISH: Norse 1080p render + audio mix (Stages 8-9). No model calls, no image spend.

Worker: Sonnet, context cap 80k. Mechanical. Do not read session history. Never modify `video2/` or `norse/library/`. Work in `norse/remotion/`, `norse/audio-mix/` (create), `norse/final/` (create).

## Read
- `norse/remotion/CUT-NOTES.md` and `SLICE-NOTES.md` (render commands), `video2/remotion-v3/render.sh` (the `full1080` mode: 1080p CRF 16/18, AAC 192k), `video2/audio-mix/MIX-REPORT.md`, `CREDITS.md` and `video2/audio-mix/src/` (how the Cyclops mix was synthesised), `PROCESS.md` Stages 8 and 9.

## Do
1. **Audio mix** (`norse/audio-mix/`): copy and adapt the Cyclops mix chain: `norse/audio-n/narration_voice_only.wav` + pink room tone (-50 dB, lowpass 4 kHz) + 3-4 SYNTHESISED stingers/light SFX (no third-party audio at all) -> amix (normalize=0) -> loudnorm two-pass linear I=-16 TP=-1.5 -> alimiter -> 48 kHz. Stingers: drone swell at N-001 (the skull sky), a low hit at N-146 (the wolf swallows Odin) or N-153 (Surt flings fire), and a short outro swell under the teaser at N-174 to N-178 with a 1 s fade at the end. Light SFX only where a beat names a sound: N-137 (wolves swallow the sun), N-064 (the chain snaps), N-141 (ship of fingernails), N-143 (Heimdall's horn), N-092 (boat bottom splintering). Keep them 10 dB under the voice. Write `norse/audio-mix/MIX-REPORT.md` (LUFS, peak, LRA, silencedetect) and `CREDITS.md` ("all audio synthesised in house; narration by ElevenLabs Daniel"). Outputs `final_mix.wav` and `final_mix.m4a`.
2. **Final render:** 1080p of the CURRENT cut (`scenes/full/cuts.json`; do not change cuts) using the full1080 route adapted for Norse, muxed with the NEW mix instead of the voice-only wav: output `norse/final/norse_v1_1080p_final.mp4` (CRF 16-18, AAC 192k, faststart) plus a 540p copy `norse_v1_540p_final.mp4`. Duration about 617 s. If the first render stalls (it did once on the 540p run; re-run as a background job with RESUME=1) recover and continue.
3. **Checks:** ffprobe streams/duration, blackdetect (0), LUFS of the muxed audio (-16 +/- 0.5), sync at N-001, N-060, N-100, N-146, N-178, soft crops at 1080 (list beats whose crop zoom exceeds 3.0x; none may exceed 3.7x), file size (expect about 140-170 MB), stills at 12 points to `norse/final/norse_v1_1080p_stills.jpg`.
4. Write `norse/final/FINISH-NOTES.md`: what was done, render times, MIX table (stinger/SFX, beat, time), the soft-crop list, anything William should check.

## Final message (max 8 lines)
Paths, duration, size, LUFS/peak, soft crops, issues.
