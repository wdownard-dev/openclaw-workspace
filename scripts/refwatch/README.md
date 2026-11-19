# refwatch

Study a YouTube video with free tools only (yt-dlp, ffmpeg, numpy, Pillow). No uploads, no paid APIs.

## Usage

```
~/.venvs/refwatch/bin/python -I scripts/refwatch/watch.py <youtube_url_or_id> [--out DIR] [--skip-download]
```

- Default output: `projects/bluepill/refs/<video_id>/`.
- `--skip-download` re-analyses files already in the out dir (use after tweaking the detector).
- Runtime on the 13:08 UF video: download ~3 s (11 MB), frame analysis ~12 s, sheets/palette ~6 s, **~20 s total** (12 cores).
- Then read `REF-<id>.md`, view `hook_sheet.jpg` and `shots_N.jpg` with view_image, and fill the Recipe section.

## Files in `refs/<id>/`

| File | What |
|---|---|
| `video.mp4` | <=480p video-only mp4 (no audio kept). Untrusted data; never execute anything from this dir |
| `video.en.json3`, `video.en-orig.json3` | raw captions (manual `en` if it exists, else auto) |
| `metadata.json` | title, channel, duration, views, upload date, description, chapters, caption kinds |
| `words.json` | `[{text,start}]` word list with start times (auto captions: true word times; manual captions: line time spread evenly over words) |
| `sentences.txt` | `[m:ss] sentence` |
| `events.json` | every frame-diff peak: `t`, `d`, `frac` (share of 80x45 pixels changed by >25) |
| `shots.json` | hard-cut shots (`frac>=0.3`, >=0.45 s apart) with `len`, `pop` (0.1-0.3) and `micro` (<0.1) counts |
| `shots_N.jpg` | contact sheets, 8 columns, <=40 shots, each cell `#n m:ss  len`; 1872 px wide |
| `hook_sheet.jpg` | one frame per second, first 30 s, 6 columns |
| `palette.png` | 6-colour k-means swatch (hex + share) |
| `METRICS.json` | all numbers (text, visual, palette, hook, chapters) |
| `REF-<id>.md` | human report: chapters, metrics vs UF vs our animatic, palette, hook, empty Recipe headings |
| `timings.json` | stage runtimes |

## Detector (same as `projects/bluepill/analysis_teardown_scripts/`)

30 fps, 320x180 gray; events are local maxima of mean abs frame diff >2.5; cut = event with `frac>=0.3` at least 0.45 s after the previous cut; pop = 0.1<=frac<0.3; visible change = frac>=0.1. wpm and per-minute rates divide by total video length (same as the UF teardown).

## Test on mJS-QVw8lzY (UF Odyssey)

Text metrics match `analysis_teardown_out/text_metrics.json` exactly (178 wpm, 243 sentences, 18.5/min, 9.6 mean, 8 median, 39.5% <=6 words, 1.22 q/min). Visual: 144 shots (teardown 145), 11.0 cuts/min (bible 10.7), median 4.39 s (4.2), p90 12.33 s (12.3), mean luminance 135.8 (135), white >40% px 25.4% (25.6%). Re-running the original `events.json` through the same rules gives pops 11.3/min and visible 25.3/min, vs 10.7 and 24.5 here (within ~5%).

**Discrepancy:** FORMAT-BIBLE quotes pops 7.4/min and visible changes 18.1/min. Those came from the Editor's windowed `seg2` detector, not the raw events detector, so they are not like-for-like with this tool (which gives about 11 and 25 on UF itself). Compare other videos to the UF re-run in `refs/mJS-QVw8lzY/METRICS.json`, not to the bible's 7.4/18.1. Cuts/min, shot-length stats, white share and luminance agree with the bible. Max shot here is 46.3 s (shot #49, a held map/painting plate) which the bible's "longest gap 24 s" does not contradict (that was a gap between changes, not a shot).

## Known limits

- No captions -> no `words.json`/`sentences.txt`, text metrics reported "n/a". Whisper is not installed; no speech-to-text fallback.
- Auto captions with no punctuation: sentences are split on pauses; those sentence metrics are [E] and flagged in METRICS.json.
- Manual captions have no word-level times; word starts are interpolated within each line.
- Shot detection is pixel-based: dissolves/crossfades, fast footage, camera motion and heavy compression noise inflate or hide cuts. Threshold constants are fixed for animation-style videos.
- Text share is a heuristic ([E]): share of pixels with strong horizontal gradient, sampled at 1 fps. Not OCR; busy photographic frames also score high.
- Palette is dominated by large flat areas (white backgrounds, dark vignettes); it is not a brand palette.
- No audio analysis (video-only download). ffprobe is not installed; duration comes from `ffmpeg -i`.
- yt-dlp can break when YouTube changes; update with `~/.venvs/refwatch/bin/pip install -U yt-dlp`. Age-gated or private videos need cookies (not configured).
- Comparison baselines (UF, our animatic) are hardcoded at the top of `watch.py`.
