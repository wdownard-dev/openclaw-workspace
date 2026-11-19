# QA-ANIMATIC.md: measurable QA on the animatic (FORMAT-BIBLE section 8)

File: `out/animatic_540p.mp4`, 19253 frames at 30 fps = 641.8 s (10.7 min). Detectors: `analysis_teardown_scripts/` (frames_to_bin, cuts, events, seg2, audio) on 320x180 frames, same settings as the UF teardown. Generated 2026-11-13T17:42:41.972Z by `qa/run_qa.sh`.

Caveat: 0 assets are placeholders (grey cards), so luminance, white share and some event counts will shift when the art lands; pacing numbers come from the storyboard timing and are already representative.

## Numbers vs targets

| Measure | Animatic | Target | |
|---|---|---|---|
| Picture changes per minute (events.js, >= 30% px, 0.45 s apart) | 9.5 | 9.5-12 | pass |
| Pops, swaps, label appearances per minute (10-30% px) | 6.5 | 6-8 | pass |
| All visible change moments per minute (>= 10% px) | 16 | 16-19 | MISS |
| Changes under 10% px (chips, small labels, small props; not counted above) | 16/min | info | info |
| Scheduled changes in the storyboard (shot starts + visual events) | 34.6/min; median gap 1.32 s, p90 4.23 s, longest 11.38 s | what the detector should see once the art lands | info |
| Picture changes per minute, windowed detector (seg2 K=6, >= 30% px) | 9.8 (133 visible at K=4, >= 10%) | cross-check | info |
| Median gap between visible changes (s) | 3.4 | <= 2.5 | MISS |
| p90 gap (s) | 7.97 | <= 7 | MISS |
| Longest gap (s) | 11.6 | <= 15 (one held beat <= 24) | pass |
| Gaps over 8 s (count, per minute) | 16 (1.5/min) | <= 1 per minute | MISS |
| Hard cuts (cuts.js) | 135 | cuts are hard | info |
| Crossfades / dissolve clusters (cuts.js) | 0 | 0 | pass |
| Frozen frames (frame diff < 0.05) | 91.5% | >= 85% | pass |
| Frames in motion (0.05 <= diff < 2.5, pop and tick frames included) | 5.7% | info | info |
| Frames in constant slow motion (moving, not within 8 frames after an event) | 3.1% | <= 5% | pass |
| Mean luminance (/255) | 153.1 | >= 105 | pass |
| White-dominant frames (> 40% px near white) | 41.9% (storyboard white=true shots: 39.2% of runtime) | 15-25% | MISS |
| Near-black frames (> 50% px < 25) | 0.7% | <= 8% | pass |
| Text, map or diagram only (classes D+E+F+G, from storyboard) | 21.6% | <= 19% (cap 22%) | MISS |
| Pure text cards (class G, from storyboard) | 0.6% | <= 2% | pass |
| Longest run of non-character shots (s, from storyboard) | 7.6 (0 runs over 8 s) | none over 8 s | pass |
| Shots with text on them (from storyboard) | 53.1% | 40-45% | info |
| Integrated loudness (ebur128) | -19 LUFS | -16 +-1 at final mix; animatic is voice as delivered (-19) | info |
| True peak (ebur128) | -1.5 dBTP | <= -1.5 | pass |
| Loudness range (ebur128) | 1.5 LU | 3-5 | MISS |
| Pauses >= 0.3 s per minute (audio.js) | 22.34 | <= 2 | MISS |
| Pauses >= 0.6 s (audio.js) | 7 | 0 (bar the held beat) | MISS |
| Pitch spread, semitone std over 20 s windows (audio.js) | 3.65 | >= 4 | MISS |

11 pass, 10 miss, 7 informational.

## Storyboard timing (resolved from words.json)

- Shots: 128; median shot 4.89 s, p90 8.8 s, longest 11.81 s (target median 4-4.5 s, p90 <= 12 s).
- Class shares of runtime: A 42.8%, B 28.8%, C 6.8%, D 6.4%, E 9.2%, F 5.4%, G 0.6% (targets A 53, B 23, C 5, D 11, E 4, F 3, G <= 1).
- Events: 332 (sprite 158, counter 18, sfx 37, label 63, stamp 14, chip 18, swap 16, route 2, bubble 6); 27.6 visual events per minute scheduled.

## Detector detail

- events.js: 342 local maxima; 171 at >= 10% px (visible changes), 102 picture changes at >= 30% px. seg2 windowed: 105 picture boundaries (65 hard, 40 gradual). Hard cuts by cuts.js: 135.
- Gap list over 8 s (s): 10.2-18.4, 190.8-199, 218.8-230.4, 252.7-262.1, 278.9-290.3, 303.7-312.8, 313-322.1, 369.8-378.5, 392.6-402.4, 402.4-411.8, 425.5-435.8, 455-463.5, 463.5-472.5, 501.8-512.7, 540.4-550.8, 589-600.3.
- Non-character runs over 8 s (storyboard): none.
- Audio (audio.js on 16 kHz mono): overall RMS -18.7 dBFS, floor mean -62.5 dBFS, pauses >= 0.3 s 239, >= 0.6 s 7, >= 1.0 s 0; F0 median 137 Hz.
- Contact sheet every 30 s: `qa/work/contact_30s.jpg`.

## Missing assets (0; rendered as labelled grey placeholders)

By role: .



Resolved from existing art (reuse table) or drawn in code: see `out/assets_report.json`.
