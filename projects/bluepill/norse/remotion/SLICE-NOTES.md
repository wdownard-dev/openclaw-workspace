# Norse slice animatic (N-001..N-047a, 0:00-2:35)
Output: out/norse_slice_540p.mp4 (960x540, 30 fps, 155.000 s, AAC mono), out/norse_slice_sheet.jpg (46 render-time frames + narration line).
Render: ~51-58 s wall (12 cores, CONC=8). No model calls.

## Changes vs video2/remotion-v3 (copied, video2 untouched; node_modules symlinked)
- render.sh: rewritten, modes `slice` and `full`. Narration = ../audio-n/narration_voice_only.wav, atrim end=155.0, 0.5 s fade out. Muted video then mux, CRF 20, scale 0.5.
- slice.js: timings from audio-n/beats_timing.json (ids N-xxx, N-047a); sheet text from scene_plan.json narration_line; END default 155.0, TAIL 0. Plates from <cuts dir>/img.
- src/Slice.tsx: added `pan_up` (plan move for N-041). Everything else identical.
- full_sheets.py: rewritten as one contact sheet for any NAME.
- ../scenes/build_cuts.py -> ../scenes/slice/cuts.json (46 cuts, hard cuts, no overlays).

## Notes
- Plates: scene base, or the variant listed in the manifest for that beat (S03_v1, S06_v1, S08_v1, S09_v1, S12_v1, S14_v1, S11_n023/n024, *_lib). N-026/N-027 do not exist in the plan.
- Moves from the plan; crop rects fitted by eye (N-004, N-028, N-034 re-fitted after first render). Pans: N-012 (pan_right), N-041 (pan_up) only.
- N-032 "holds N-031": same crop as N-031, no motion (so no visible cut). N-019 variant: crop to Audhumla + ice block (Ymir out of frame).
- Sync: speech onsets (silencedetect) match beats_timing within ~0.05 s at N-001, N-002, N-003. No black frames (blackdetect: 0).
- Last cut ends at 155.0; N-047a speech ends 155.046, so the final syllable is under the 0.5 s fade.

## FULL cut later
1. Build ../scenes/full/cuts.json (same schema; plates in ../scenes/full/img, copy build_cuts.py and extend over N-048+).
2. `FULL_END=<last beat end s> bash render.sh full` (optionally pass a cuts path; defaults ../scenes/full/cuts.json; SLICE_TAIL default 1.5 s hold). Output out/norse_full_540p.mp4 + out/norse_full_sheet.jpg. Contact sheet is one image: 6 cols, ~177 beats would exceed 3000 px, so split full_sheets.py into thirds as video2 did.
