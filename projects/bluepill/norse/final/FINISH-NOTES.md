# Norse v1 finish (Stages 8-9)
## Done
- Audio mix in `audio-mix/` (chain `src/chain.txt`, `src/build.sh`): voice-only narration + room tone + 3 stingers + 5 SFX, all synthesised with ffmpeg; loudnorm two-pass linear. See `audio-mix/MIX-REPORT.md`, `CREDITS.md`.
- Render script `remotion/render_final.sh` (silent 1080p CRF 16 and 540p CRF 18 of `scenes/full/cuts.json`, unchanged, 18505 frames, 616.833 s). Muxed with `audio-mix/final_mix.wav` (AAC 192k / 160k, 0.5 s end fade, faststart): 1080p at CRF 18, 540p at CRF 20.
- Times (wall): 1080p render about 7.5 min, 540p render about 4.5 min (no stall), 1080p re-encode/mux about 5 min. A first nohup launch from a short foreground command never started; rerun as a background exec worked.
## Outputs
- `final/norse_v1_1080p_final.mp4`: 1920x1080 30 fps h264 High + AAC 48 kHz mono, 616.83 s, 190 MB (above the 140-170 MB guess; CRF 18 is the ceiling of the brief range).
- `final/norse_v1_540p_final.mp4`: 960x540, 74 MB. `final/norse_v1_1080p_stills.jpg`: 12 evenly spaced frames (taken from the 540p file).
## Checks
- blackdetect (d=0.1): 0 segments. Muxed audio: -16.0 LUFS, LRA 1.9, true peak -1.3 dBFS (AAC). 
- Sync (speech onset after -40 dB silence vs beat start): N-001 0.4 -> 0.51, N-060 199.20 -> 199.27, N-100 324.90 -> 324.98, N-146 493.29 -> 493.30, N-178: no silence before the beat in the window (speech runs on from N-177), so aligned.
## MIX
| Item | Beat | Time (s) |
|---|---|---|
| Drone swell 5 s | N-001 | 0.40 |
| Low hit 3 s | N-146 | 493.29 |
| Outro swell 7 s, 1 s final fade | N-177/178 | 608.00 |
| Wolves swallow sun rumble | N-137 | 456.15 |
| Chain snap | N-064 | 210.86 |
| Ship of fingernails creak | N-141 | 472.53 |
| Heimdall horn | N-143 | 482.41 |
| Boat splintering | N-092 | 300.62 |
## Soft crops (plate width / crop width, plates 1536 px; over 3.0x)
N-045, N-053, N-054, N-170, N-172 (3.20x); N-056, N-082, N-097 (3.07x). Over 3.7x: **N-037 (3.84x)**, a slice crop approved earlier. Also high: N-031/N-032 (3.66x). 2.95x: N-007, 067, 068, 077, 088, 098, 104, 120, 123, 168.
## For William to check
- Listen to the synthesised SFX/outro (horn and splinter are crude, they sit about 10 dB under the voice); say which to drop.
- N-037 at 3.84x for softness at 1080; N-031/032 at 3.66x.
- File size 190 MB; re-mux at CRF 20 gives about 150 MB if needed.
