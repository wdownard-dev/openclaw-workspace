# remotion-v2: Blue Pill video 1 renderer (2026-11-13)

Storyboard-driven Remotion build implementing every FORMAT-BIBLE section 11 event kind. Nothing here edits `storyboard.json`, the audio or `video2/assets/`.

## One command

```
cd video2/remotion-v2 && bash render.sh animatic      # -> out/animatic_540p.mp4 (960x540, narration muxed), about 4 min on 12 cores
bash render.sh final                                   # -> out/video1_1080p.mp4 (same chain at 1920x1080, crf 19)
node stills.js out/stills                              # 8 full-1080p stills, one per shot class present (+ one bubble shot)
bash qa/run_qa.sh                                      # section 8 numbers -> QA-ANIMATIC.md, contact sheet qa/work/contact_30s.jpg
```

`render.sh` runs `node resolve.js` first (re-resolves timing and assets), renders the picture silent with Remotion, then muxes `../audio/narration_voice_only.wav` with the full ffmpeg at `/home/williamdownard/openclaw-sites/bin/ffmpeg` (voice as delivered, no loudnorm, no bed). `CONC=n` sets Remotion concurrency (default 11).

Versions are pinned in `package.json` (remotion, @remotion/* 4.0.543; react 19.3.1); `node_modules` is a symlink to `../../pipeline/remotion-proof/node_modules`, which holds exactly those versions, so no install is needed. Fonts: Permanent Marker and Special Elite (Apache 2.0) in `public/fonts/`, loaded with `FontFace` behind `delayRender`.

## Files

- `resolve.js`: `../storyboard.json` + `../audio/words.json` -> `src/timeline.json`. Every shot start and event time is re-derived from word onsets (`{word, off}`) or `{t}`; the storyboard's convenience `t` fields are ignored. Stages assets into `public/a/` and writes `out/assets_report.json` (resolved / code / missing). Also computes swap targets (`targetIndex`) and board memory (`shot.earned`: verdict stamps earned on earlier board shots).
- `src/Video.tsx`: one `<Sequence>` per shot, hard cuts only. Ground by `bg.type`: `img` plate (cover, no camera), `white` (class B gets the tinted ground `#f6f1e8`, C/F stay white), `board`, `map`, `black`.
- `src/lib/Text.tsx`: `Label` (impact / place / title / crossout / chip_title), `Counter` (15 updates per second, unit under or inline), `Chip` (Special Elite 48 px, verdigris pill, fixed bottom-left 60 px margins, 2.5 s, wraps over 40 chars), `Stamp` (deep gold `#a8841c`, double border, rotated, 0.2 s slam from 1.35x, 85% cream halo over paint; stamps under 700 px apart on one line drop to 64 px), `Bubble` (64 px hand lettering, no box, 4 words per line, thin curved tail to the nearest non-prop sprite's head).
- `src/lib/Sprite.tsx`: bottom-anchored sprites, pop 0 -> 1.06 -> 1 over 0.2 s (easeOutBack, overshoot 1.3), `mirror`, `inset` (framed picture-in-picture, centre-anchored), optional `enter:'slide'` (160 px over 0.15 s). `swap`: hard src replacement; `none` removes; `slide_out_left` slides 200 px over 0.15 s then removes. Swap targets resolve by name prefix (`polyphemus` -> `polyphemus__*`, `prop_club` -> `prop__club*`, `cyc2_2` -> second `cyc2__*` sprite in the shot).
- `src/lib/Board.tsx`: the case board (cork, wood frame, four pinned cream cards at (560,420) (1360,420) (560,820) (1360,820), 640x340). Label style `board` with `state` drives it (`empty`, `frame1_skull`, `frame3_wall_flicker`, `four_questions`, `four_questions_skull`, `frame1_skull_jitter`, `four_frames_skull[_anvil[_wall]]`, `frame1_dim`, `frame4_full_world`, `frame4_blank`, `four_stamped`). Verdict stamps earned on earlier boards persist (`shot.earned`). `ping_*` states on non-board shots draw a 480x270 corner inset with the named frame glowing 0.5 s, held 1.5 s, no stamp.
- `src/lib/Maps.tsx`: code maps from Natural Earth rings (`med.json`, `world.json`, copied from remotion-v1) with a bbox per map id; `Route` draws from->via->to in 15 fps steps with an arrow head; `loop:true` closes the curve back to the start.
- `src/lib/CodeProps.tsx`: ASSET-PLAN 3.2 code-drawn icons (rings, eye, ship icon from the NP04 cutout, height line, person silhouette, drops, pins, book, arrows, heart, glow, dust, slip, Etna, whirlpool), silhouettes (base sprite filtered to black), crew group sets built from `crew__neutral__a`, `NP04_listing` (12 deg). `Placeholder`: grey dashed card with the asset name.
- `src/lib/anim.ts`: popScale, stampScale, step15, counterValue, routeProgress, slide helpers, tiltOf.
- `stills.js`, `render.sh`, `qa/run_qa.sh`, `qa/metrics.js`, `qa/contact.js`.

## Asset resolution order (never fails a render)

1. `video2/assets/{,plates,sprites,props,maps,sourced}/<name>` (delivery folders only; `gen/`, `rejects/`, `masters/`, `checks/` are ignored on purpose).
2. Reuse table from ASSET-PLAN.md: `video1/images/` for NB*, NBG*, NB14_crop_left55, RC11, RS08, RS10, NP01/NP03/NP04 (the NP props are white-keyed into cutouts at stage time); `pipeline/remotion-v3a/public/img3/` for `odysseus__neutral__a` (ody), `odysseus__point__a` (ody_shout), `odysseus__tired_helm__a` (ody at 260 px), `prop__boulder__a` (boulder3), `prop__ram__a` (sheep).
3. Code-drawn (maps, board, icons, groups, silhouettes).
4. Labelled grey placeholder; listed in `out/assets_report.json` and QA-ANIMATIC.md.

Re-run `bash render.sh animatic` after the asset worker delivers: resolve picks up new files automatically.

## SFX hook

`sfx` events are collected into `timeline.sfx` with `file` set when `assets/sfx/<src>` exists; the picture renderer ignores them and nothing is mixed yet (no music bed by design). Wiring: add `-i` inputs and `adelay` per entry to the mux in `render.sh` once files exist.

## QA (qa/run_qa.sh)

Extracts every frame at 320x180, runs the Editor's `frames_to_bin`, `cuts`, `events`, `seg2` (K=6/0.30 and K=4/0.10) and `audio` detectors, measures loudness with `ebur128`, and writes `QA-ANIMATIC.md` plus `qa/work/contact_30s.jpg`. Pacing rows follow the UF teardown method (events.js local maxima: picture change = >= 30% of pixels at least 0.45 s apart, visible change = >= 10%, pops = the difference). Changes under 10% of the frame (chips, 48-100 px labels, small props) are listed separately because the detector cannot see them; the storyboard's own scheduled cadence is reported next to the detected one. `qa/work/frames/` (about 1 GB) is deleted after a run; re-run the script to regenerate.

## Known renderer gaps

- Routes and place labels use the storyboard's pixel positions, which were set without a real map; the code map bbox per id is a guess (`MAP_BBOX`). When painted map plates arrive, pins and labels may need re-placing.
- Bubble tails aim at the nearest non-prop sprite's head by x; a storyboard `tail: [x, y]` override is not implemented.
- `hold` and `beats` shot fields and the shot notes (e.g. "crop 1.1x") are informational only; no crop is applied.
- `frame3_wall_flicker` and `frame1_skull_jitter` are 15 fps stop-motion for 0.6 s / 0.5 s; tune by eye at G3.
- Counters with `from === to` pop; ticking counters hold 1.0 scale while stepping.
- The title card (class G) uses cream Permanent Marker on near-black; no end-card layout beyond the one label.
- No burned-in captions (by rule); SRT export is not part of this build.
