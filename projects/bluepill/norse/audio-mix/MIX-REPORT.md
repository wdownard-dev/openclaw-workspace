# Norse final mix
Chain (src/chain.txt, src/build.sh): narration_voice_only.wav + pink room tone (-50 dB, lowpass 4 kHz) + 3 synthesised stingers + 5 light SFX via amix (normalize=0) -> loudnorm two-pass linear I=-16 TP=-1.5 (pass 1 in src/pass1.json) -> alimiter -> 48 kHz mono. Padded/trimmed to 616.833 s, 1 s fade-out at the end.
Measured final_mix.wav: **-16.0 LUFS, true peak -1.5 dBFS, LRA 1.9 LU** (LRA is inherited from the voice track). m4a (AAC 192k): LRA 1.9, peak -1.3 dBFS. silencedetect (-70 dB, 0.5 s): 0 hits.
Stinger peaks about -10 dBFS pre-norm, SFX peaks about -13 dBFS, voice peak -1.5 dBFS (SFX roughly 10+ dB under voice).

| Item | Beat | Time (s) |
|---|---|---|
| Stinger 1 drone swell 5 s | N-001 | 0.40 |
| Stinger 2 low hit 3 s | N-146 | 493.29 |
| Stinger 3 outro swell 7 s (under teaser, ends in 1 s fade) | N-177/N-178 | 608.00 |
| SFX wolves swallow the sun (brown-noise rumble) | N-137 | 456.15 |
| SFX chain snaps | N-064 | 210.86 |
| SFX ship of fingernails (creak) | N-141 | 472.53 |
| SFX Heimdall's horn | N-143 | 482.41 |
| SFX boat bottom splintering | N-092 | 300.62 |
