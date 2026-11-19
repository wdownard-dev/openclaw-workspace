# BRIEF-CUT: Norse full 540p cut with narration. No model calls, no image spend.

Worker: Sonnet, context cap 80k. Mechanical. Do not read session history. Never modify `video2/` or `norse/library/`. Work in `norse/scenes/`, `norse/remotion/`.

## Read
- `norse/remotion/SLICE-NOTES.md` (how the slice cut was built; the full command), `norse/scenes/build_cuts.py`, `norse/scenes/slice/cuts.json`, `norse/scenes/scene_plan.json`, `norse/audio-n/beats_timing.json` (177 beats, last beat N-178 ends about 615.3 s, total 616.84 s).
- Plates: slice plates in `norse/scenes/slice/img/` (S01-S20) and full plates in `norse/scenes/full/img/` (S21-S81); manifests `scenes/slice/manifest.json`, `scenes/full/halfA/manifest.json`, `scenes/full/halfB/manifest.json` map every beat to a plate. Crop beats map to their parent plate; crop rects are NOT fitted yet.

## Do
1. Extend `build_cuts.py` to write `norse/scenes/full/cuts.json` for ALL 177 beats: plate per beat from the manifests, move per the scene plan (hard cuts only; push_in on every 4th beat; pans on at most about 1 in 4 shots; crop_close with a crop rect you FIT per beat by viewing the plate; hero plates held with a slow push-in). No text, bands, stamps or chips. Fit crops by viewing plates at low resolution in contact sheets, not one by one; check every crop rect lies inside the 1536x1024 plate and keeps the speaking subject (head not clipped; crops over 3.7x zoom flagged, they look soft at 1080).
2. Render the full 540p cut with the narration: `norse/remotion/out/norse_v1_540p.mp4`, duration = last beat end + 1.5 s hold + 0.5 s fade (total about 617 s). Audio: `norse/audio-n/narration_voice_only.wav`. Use the full command in SLICE-NOTES.md.
3. Contact sheets: `norse_v1_sheet_a/b/c.jpg` (render-time frame per beat, labelled with beat id and text) and `norse_v1_stills.jpg` (about 24 frames spread across the video).
4. Checks: no black frames, no missing plates, sync spot-check at 5 beats across the runtime (N-001, N-060, N-100, N-146, N-178) against beats_timing, loudness unchanged, file plays (ffprobe duration and streams).
5. `norse/remotion/CUT-NOTES.md`: what the cut is, render time, crops improvised, soft-crop list, anything William should check, and how to re-render a fix pass.

## Final message (max 8 lines)
Paths, duration, render time, cuts per minute, soft crops, issues.
