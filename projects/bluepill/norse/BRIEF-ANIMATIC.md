# BRIEF-ANIMATIC: Norse slice animatic (S01-S20, 0:00-2:35) with the narration, 540p. No model calls, no image spend.

Worker: Sonnet, context cap 80k. Mechanical: reuse video 1's Remotion tooling with path changes. Do not read session history. Never modify `video2/` (copy). Write inside `projects/bluepill/norse/remotion/` (copy of `video2/remotion-v3/` WITHOUT node_modules: symlink `node_modules` to `../../video2/remotion-v3/node_modules`; skip `out/`), `norse/scenes/slice/cuts.json`, and outputs in `norse/remotion/out/`.

## Read
- `video2/remotion-v3/render.sh` (the `slice` mode), `slice.js`, `src/` (the `Slice` composition and `slice_timeline.json`), `full_sheets.py`; `video2/scenes/full/build_cuts.py` and `cut.py` and `cuts.json` (schema: beat, scene, image, move, crop_rect; start/end come from beats_timing at render).
- `norse/scenes/scene_plan.json` (camera moves per scene), `norse/scenes/slice/manifest.json` and `img/` (plates), `norse/audio-n/beats_timing.json` and `narration_voice_only.wav`.

## Do
1. Write `norse/scenes/build_cuts.py` producing `norse/scenes/slice/cuts.json` for beats N-001..N-047a from the scene plan: one cut per beat, plate = the scene's base or variant for that beat, move from the plan (hold, push_in on every 4th beat, pull_out, pan, crop_close with a crop rect fitted to the 1536x1024 plate). Hard cuts only; no text, bands, stamps or chips; hero plate S01 held with a slow push-in. Pans on at most about 1 in 4 shots. Where a plan move needs a character position you cannot see, use a plain push_in.
2. Adapt `slice.js`/`render.sh` paths to Norse: narration `norse/audio-n/narration_voice_only.wav` trimmed to 0-155.0 s (atrim) with a 0.5 s fade out; timings from `norse/audio-n/beats_timing.json` (beat ids are `N-001`, `N-047a`); plates from `norse/scenes/slice/img/`. Keep the 30 fps, 540p (scale 0.5), CRF 20, muted video then mux.
3. Render `norse/remotion/out/norse_slice_540p.mp4` and a contact sheet `norse_slice_sheet.jpg` (a render-time frame per beat, as `full_sheets.py` does). Check: duration about 155 s, audio present, no missing plates, no black frames (spot-check 10 frames via the sheet), voice and picture in sync at three beats you verify by their timestamps.
4. Write `norse/remotion/SLICE-NOTES.md`: what was changed in the copied tooling, render time, anything William should know, and how to run the FULL cut later (`render.sh full` equivalent with the full cuts file) so the next step is one command.

## Final message (max 8 lines)
Output paths, duration, render time, any beat whose plate/move you had to improvise, issues.
