# Norse v1 full cut (N-001..N-178)
Output: `out/norse_v1_540p.mp4` (960x540, 30 fps, 616.83 s, H.264 + AAC mono, ~74 MB), same file as `out/norse_full_540p.mp4`.
Sheets: `out/norse_v1_sheet_a/b/c.jpg` (one render-time frame per beat, labelled beat / move / plate / text), `out/norse_v1_stills.jpg` (24 frames spread across the runtime).
No model calls, no image spend, no text/bands/stamps/chips. Hard cuts only.

## What it is
- Cut list: `../scenes/full/cuts.json`, built by `../scenes/build_cuts.py` (slice section unchanged, FULL section appended at the bottom). 177 cuts, 17.2 cuts/min.
- First 46 cuts = the approved slice cuts, verbatim. N-048+ come from scene_plan.json moves and halfA/halfB manifests (plate per beat; crop beats use their parent plate).
- Slice plates were copied into `../scenes/full/img/` so slice.js finds every plate in one dir (names do not collide).
- Moves for N-048+: plan moves, plus push_in on every 4th beat that would have been a hold, the three hero plates (S33, S40, S49) held with a slow push-in, and 4 extra pan_right on holds. Totals over all 177 beats: 65 crop_close, 54 hold, 49 push_in, 4 pull_out, 4 pan_right, 1 pan_up (5 pans, about 3%).
- Audio: `../audio-n/narration_voice_only.wav`, atrim end=615.344, 0.5 s fade out at 614.84, video holds 1.5 s past the last beat end (total 616.833 s, about 1 frame short of 616.844 because of frame rounding).
- Render: `FULL_END=615.344 CONC=8 bash render.sh full`, then copy to the v1 name, then `~/.venvs/refwatch/bin/python full_sheets3.py` (thirds + stills). Render ~190 s wall on 12 cores. Run it as a background exec; a backgrounded job tied to a short foreground command stalled once at frame 411.

## Crops improvised (49 new, N-048+; all fitted by eye from gridded plate sheets)
All rects checked inside 1536x1024 and 16:9. No crop over 3.7x. Crops between 3.0x and 3.2x zoom, expect slight softness at 1080: N-053, N-054, N-056, N-082, N-097, N-170, N-172 (soft-crop list).
Fix-ups after the first render: N-109 (S45_comp, Frigg was out of frame), N-126 (S52, plate shows the giantess from behind/side, there is no face with a raised eyebrow, so the crop is the seated figure and cave mouth).

## Things William should check
- N-109: plan note says "Frigg and the flame, the flame bowing"; the flame icons sit about 450 px below Frigg on the plate, so the crop is Frigg only.
- N-126: no face on the plate (see above).
- N-161 "dew on a leaf": no leaf on the plate, crop is the two people.
- N-096 "Hymir with a knife, water at his ankles": crop keeps head and knife, ankles/water are cut.
- N-136 (S57_v1): the plate itself is a triptych-looking frame; unchanged by the cut.
- Last cut (N-178): N-178 speech runs into the 0.5 s fade, same as slice.

## Checks run
- blackdetect (d=0.1): 0 black segments. All 177 plates present (assert in build_cuts.py).
- Sync: speech onset (silencedetect -40 dB) vs beats_timing start: N-001 +0.11 s, N-060 +0.06, N-100 +0.08, N-146 +0.06, N-178 -0.02 (onset sits slightly after the beat marker because of the breath before the word; same as slice).
- Loudness: integrated -19.0 LUFS, LRA 1.8, identical to narration_voice_only.wav over the same span.
- Streams: video h264 960x540 30 fps, audio aac mono 44.1 kHz, duration 10:16.83.

## Re-rendering a fix pass
1. Edit `FCROP` / moves in `../scenes/build_cuts.py` (or edit `../scenes/full/cuts.json` directly), `python3 ../scenes/build_cuts.py`.
2. `cd remotion && FULL_END=615.344 CONC=8 bash render.sh full` (about 190 s), `cp out/norse_full_540p.mp4 out/norse_v1_540p.mp4`, `~/.venvs/refwatch/bin/python full_sheets3.py`.
3. Plates are staged into `public/s/` by `slice.js prep` on every render; no cache to clear.
