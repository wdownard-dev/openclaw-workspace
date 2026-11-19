# Spike: same 20 s UF-style sequence in Remotion and in a scripted sharp+ffmpeg state renderer (2026-11-12)
Shared: `common/storyboard.json` (shots and events anchored to word indices), `common/resolve.js` (storyboard + words.json -> timeline.json, absolute seconds), `common/anim.js` (pop easing, stop-motion route/counter steps, map projection), assets copied from video1/images and tests/chars_v3.
Run: `node common/resolve.js common/words.json common/timeline.json` then
- Remotion: `cp common/timeline.json remotion/tl.json && cd remotion && npx remotion render src/index.ts Spike ../out/remotion_20s.mp4 --codec=h264 --crf=20 --concurrency=11`
- State renderer: `cd sharpff && node render.js ../common/timeline.json ../out/sharpff_20s.mp4` (`S=2` for 4K, `S=0.5` for preview)
Retime: `node common/resolve.js common/words_retimed.json common/timeline_retimed.json` and render again (no code edits).
Outputs: `out/*.mp4` (20 s clips, 1080p and 4K, retimed), `out/compare_stills.jpg` (top two rows Remotion, bottom two sharp+ffmpeg), `out/mix_test.wav` (audio mix test). Numbers are in ../TOOLING-EVAL.md.
