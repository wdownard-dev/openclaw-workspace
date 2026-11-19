# Blue Pill v2 upgrade test (Cyclops), notes, 2026-11-12

Built to the Editor's critique (REVIEW-2026-11-12.md). Old proof in pipeline/remotion-proof/ is untouched. Nothing uploaded or posted.

## Where things are
- Render: `pipeline/remotion-v2/out.mp4` (1920x1080, 30 fps, 76.5 s, h264 + aac, 36 MB). Render time 77 s, no errors.
- Stills: `tests/v2/v2_01..08_*.jpg` (extracted from out.mp4 with ffmpeg), `tests/v2/compare.jpg` (old proof row vs v2 row), `tests/v2/work/final8.jpg`, `tests/v2/work/sheet_b0..4.jpg` (3 frames per shot, every shot), `tests/v2/gen/` (the 4 new images).
- Sounds and cue list: `pipeline/remotion-v2/SOUNDS.md`.
- Rebuild: `cd pipeline/remotion-v2 && node prep_assets.js && node synth.js && python3 make_audio.py && npx remotion render src/index.ts MythLedgerCyclopsV2 out.mp4`. `make_audio.py` reuses the cached ElevenLabs alignments in data/vo_*.json, so rerunning costs nothing unless a cache file is deleted. `node stills.js <dir> shots|even|list ...` renders review stills.

## Reusable pieces (src/lib/)
- `Scene.tsx`: `Scene` (bg layer with overscan, parallax bg/char/fg, camera, grade, vignette, dim keys, flashes, impact words, cue list, screen-space `extras` and camera-space `world` slots). `Cutout` (bottom-anchored placement by feet x/y and height fraction, spring entrances left/right/drop/pop/rise/fade with overshoot, walk hop, idle bob + breathing, reactions hop/shake/wobble/recoil/squash, rotateTo with lift, moveTo travel, spin for rolling props, emotion marks `! ? sweat shh zzz sparks x`, ground shadow that shrinks with lift, multiply colour tint with darker feet clipped to the cutout shape). `Impact` (hand-lettered word, spring slam, decaying shake, line boil, sfx).
- `camera.ts`: presets `pushIn`, `pullOut`, `pan`, `hold` (with shake keys), `tilt`.
- `Cards.tsx`: `TitleCard` (chapter card with sting), `EndCard` (tease + channel lockup + lightning), `MapShot` (painting, dotted route revealed by a mask, arrowhead on the tip, pins, years counter), `NamePlate`, `CountCard`.
- `Captions.tsx`: phrase chunker (breaks at punctuation, balanced split of long clauses, never ends a chunk on a weak word, no one-word orphans, never crosses a shot boundary) and the caption renderer (58 px vs 88 px in the proof, positioned per shot, fixed chunk with a short fade, one static gold keyword at most, no per-word colour change).
- Head safety: the cover-crop only ever applies to the background; characters are placed by coordinates, and every shot was checked in stills at start/40%/85% (no clipped heads seen after fixes). The check is visual, not automated.
- `src/shots.tsx` is the shot table (20 shots), `src/Video.tsx` does sequencing, transitions (cut, whip, fade, flash), voice sequences, music ducking.

## What changed vs the proof
- Script: same Cyclops story, narration kept as in the proof except these additions: stakes hook ("Twelve men walk into this cave. Six never walk out."), a map-setup line ("Ten years after Troy, Odysseus is still sailing home."), a re-hook ("Now the giant is blind. But the boulder is still there, and he is waiting at the door."), and a tease ("Next: the god who heard that name, and what he did to the sea."). One reworded line: "Odysseus and his crew are starving, so they walk into..." became "His crew is starving, so they walk into..." because the map line now introduces Odysseus. Everything else is the proof's text. The stakes line is the standard retelling (Odysseus takes 12 men into the cave, Polyphemus eats 6); the Editor or William should fact-check it before any real video.
- 20 shots in 76.5 s: mean 3.8 s, range 1.35 s (punchline) to 6.8 s (end card). Cuts per minute: 19 transitions / 76.5 s = 14.9 (15.7 shots/min) vs about 6.5 in the proof. The Editor's target was 11-13, so this is slightly fast; the short punchline shots (1.35 to 2.4 s) pull the mean down. Not 4-5 s everywhere: 10 of 20 shots are under 3.8 s and only 4 reach 5 s or more.
- Shot types: character scenes (16), storm atmosphere shot (1), map with animated route (1), chapter card (1), end card (1). Hard cuts on punchlines (SIX, MISTAKE, Cyclops landing, boulder, NOBODY, BLIND, plan works, shout); whip, fade or flash only where time or place jumps.
- Impact words: SIX, MISTAKE, NOBODY, BLIND!, ODYSSEUS!, PRIDE, plus "22 WAGONS" counter and POLYPHEMUS name plate.
- Captions never cover characters: feet kept at or above y 0.88 of frame, captions sit in the bottom band; shot 1's silhouette giant is intentionally dark under the caption.

## Images generated
4 images, gpt-image-2.6-sunburst, medium, 1536x1024, all kept: island at dusk with cave path, sea at sunrise, cave mouth at dawn, props sheet (sheep, cup, stake, boulder, ship, amphora; amphora unused). Each is about 1,132 output tokens like round 1. Exact dollar cost not measured; estimate about 0.04-0.08 USD each, so roughly 0.15-0.30 USD in total [E]. Plus 9 ElevenLabs TTS calls (about 1,050 characters in total, new narration), which cost plan credits.

## Known weaknesses and decisions for William
1. Acting is thin. Every character has one front-facing pose (hero, Cyclops), so expression comes only from motion, marks (!, ?, sweat, X over the eye) and camera. The proof's baked scenes had real poses (arm up, asleep, peeking under a sheep). This is the biggest remaining gap. Fix: commission 4-6 poses per main character (point, cheer, scared, arms out, sleeping, back view) via the reference-edit method, then they drop straight into Scene.
2. Cutouts sit on the backgrounds better (shadow, tint, darker feet) but are still flat-on-painting; scale and perspective are by eye. The hook shot crew (hero art shaded lavender) reads as ghostly background men; fine for a test.
3. Backgrounds are reused across shots (cave bg in 8 shots with flips and crops); that matches the Editor's "80-100 unique images for 10-12 min" plan, but in a 76 s test it is noticeable.
4. The chapter card and end card are plain (blurred painting plus type). No chapter numerals beyond a faint "I".
5. Audio is synthesised and unheard by me (see SOUNDS.md). Whether to keep synthesis or use licensed tracks is a call for William after listening. Final mix peaks at -0.6 dBFS.
6. Voice: one ElevenLabs call per paragraph with previous_text/next_text for continuity; prosody may vary slightly between paragraphs. Not heard.
7. Map: route and pins are placed by eye on a stock round-2 map; Ithaca is approximate and the route is illustrative.
8. Cut rate is 14.9 cuts/min, above the 11-13 target; easy to slow by merging the 2 s punchline shots, a decision for the Editor.
9. Renders from a symlinked node_modules (-> ../remotion-proof/node_modules) to avoid a 742 MB copy; if the old proof folder is deleted, run `npm i` in remotion-v2.
10. Remotion licence for commercial use remains unconfirmed (PLAN.md [U]).
