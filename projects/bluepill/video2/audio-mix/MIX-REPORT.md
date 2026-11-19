# Cyclops final mix
Chain: narration_voice_only.wav + pink room tone (-50 dB, lowpass 4 kHz) + synthesised stingers/SFX via amix (normalize=0) -> loudnorm two-pass (linear) I=-16 TP=-1.5 -> alimiter -> 48 kHz.
Measured final_mix.wav: **-16.0 LUFS, peak -1.5 dBFS (ebur128 peak=true), LRA 1.9 LU**. m4a (AAC 192k): LRA 1.9, peak -1.4 dBFS. No digital silence (silencedetect -70 dB: 0 hits).
LRA 1.9 is below the 3-5 target: it is inherited from the voice track (draft was 1.7); raising it needs performance changes, not mix tricks.
Voice peak -1.5 dBFS pre-mix; SFX peaks -12 dBFS (10.5 dB under), stingers -10/-9/-10.

| Item | Beat | Time (s) |
|---|---|---|
| Stinger 1 drone swell 5 s | V5-001 | 0.40 |
| Stinger 2 low hit 3 s | V5-092 | 265.94 |
| Stinger 3 outro swell 5.5 s | V5-184 | 567.64 (final 1 s fade) |
| Stone scrape | V5-033, V5-056 | 89.66, 160.35 |
| Wave | V5-134 | 400.06 |
| Soft thud (minority of cuts) | V5-020, 075, 150 | per beats_timing |

Files: final_mix.wav/.m4a, preview_cold_open.mp3 (0-20 s), preview_blinding.mp3 (V5-088..095, 254.8-278.4 s). Chain script: src/chain.txt, placements: src/placements.json.
