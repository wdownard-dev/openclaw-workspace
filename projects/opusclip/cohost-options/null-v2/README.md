# NULL v2 "NULL//SMIRK" (NULL + a little RASCAL)

Tagline: "No face. All takes. Mild contempt." Original character, code-drawn, free/local (Pillow + numpy, Kokoro TTS, ffmpeg, CPU only).

## Files
| File | What |
|---|---|
| `contact-sheet-null-v2.png` | A (subtle) vs B (raccoon-hooded), 4 expressions each |
| `null-v2-demo.mp4` | ~35 s, 1080x1920 demo, same structure as `../../cohost-demo/` (corner reactions over a sample clip, then full-screen outro) |
| `null-v2-A.mp4`, `null-v2-B.mp4` | ~13 s each: one reaction + 3-part outro, each in its own variant and voice |
| `frames_A/`, `frames_B/` | transparent 600x600 PNGs, `nullv2<A|B>_<expr>_<mouth>.png` |
| `null_v2.py` | the rig (layers, expressions, `compose()`) |
| `build_video.py` + `configs/*.json` | video builder (TTS, captions, mouth sync, expression timeline) |
| `make_sheet.py`, `tools/audition.py`, `tools/score.py` | contact sheet, voice audition, clarity scoring |
| `voices/` | audition wavs + `audition.json` (pitch) + `wer.json` (clarity) |
| `script-sample.md` | micro-sample of the snarky script style |

The sample background footage is a third-party clip (`clips-work/cut/mw4-01-cut.mp4`): demo only, NOT for posting.

## The two variants
- **A Subtle**: NULL silhouette/hood/headphones unchanged. Personality only through the glowing features: angled brow bars (right brow raised for smug), heavy half-lidded eyes with a dark pupil that can glance or roll, squint state, and an equalizer mouth with a built-in smirk (bars on the right side lift and run taller).
- **B Raccoon-hooded**: A plus small glowing raccoon ears behind the headphone band (band sits a bit lower), a faint neon bandit-mask band around the eyes, a thin forehead stripe, and a smaller mouth (7 bars; closed state is a thin hooked smirk line).
- Both: expressions `smug, laugh, squint, raised, glance, glanceL, blink`, plus an animated eye-roll (`roll_pose(t)`, exported as `roll1..3`); 4 mouth states `closed/small/open/wide`; head tilt and idle bob are applied at video time. The old faint rim-light streak at the lower left is fixed: rim lights now fade out vertically (`vramp`) before they reach the hood/body bottom corners.

## Voices (picked without listening: the machine has no audio output)
All 8 auditioned voices transcribed back with 0% word error (faster-whisper small.en), so clarity did not separate them; pitch and intonation did (`voices/audition.json`).
- A: `am_onyx`, speed 0.97. Lowest pitch (about 87 Hz) and flattest intonation = deadpan delivery. Same family as the first NULL.
- B: `am_fenrir`, speed 0.97. Livelier intonation (pitch spread about 3x onyx) = mischievous. Not `bm_lewis`, so B does not sound like RASCAL.
- Plain stock Kokoro voices, clearly synthetic, no impersonation. Listen and swap `voice`/`speed` in `configs/*.json` (candidates in `voices/`).

## Swap NULL v2 into the existing pipeline
Quick path (3-state `../../cohost-demo/build.py`): copy a variant's frames over the demo mascot and set the voice.
```
V=B   # A or B
D=/home/williamdownard/.openclaw/workspace/projects/opusclip
for m in closed:closed small:half open:open; do a=${m%%:*}; b=${m##*:}
  cp $D/cohost-options/null-v2/frames_$V/nullv2${V}_smug_$a.png $D/cohost-demo/frames/mascot_$b.png
  cp $D/cohost-options/null-v2/frames_$V/nullv2${V}_blink_$a.png $D/cohost-demo/frames/mascot_${b}_blink.png; done
```
Set `"voice": "am_fenrir"` (B) or `"am_onyx"` (A) in `cohost-demo/config.json`, then `build.py` as usual. You get the smug face with mouth swaps only.

Full path (expressions, head tilt, eye-roll): use `build_video.py` here. It is `cohost-demo/build.py` with the mascot stream replaced by `null_v2.compose(variant, mouth, pose)`.
```
PY=/home/williamdownard/openclaw-sites/tts-venv/bin/python
cd .../cohost-options/null-v2
$PY build_video.py configs/demo.json            # add --skip-tts to reuse work/<name>/voice.wav
```
Config = the demo's `config.json` plus `variant`, and per-line `expr` cues: `"expr": [["0","squint"],["1.6","roll",1.9]]` = offsets in seconds from the line start; names `smug laugh squint raised glance glanceL blink roll`; `roll` takes a duration. `reactions` are silent cues at video time. Sizes/positions: `mascot_small`, `small_xy`, `mascot_big`, `big_xy`. Output goes to `out`.

To use the rig directly: `import null_v2 as N; N.RES = 800; N.compose("B", "open", N.EXPR["raised"])` returns an RGBA PIL image (mouth: closed/small/open/wide). Blend poses with `N.lerp_pose`; `build_video.py` low-passes the pose per frame so changes ease in over ~4 frames. Regenerate PNGs: `$PY null_v2.py A B; $PY make_sheet.py`.

## Known flaws
- Expressions are pose swaps with easing, not real animation; the eye-roll is a pupil sweep, not a head move.
- The dark pupils soften the "faceless" look a little; the raised-brow state with a wide right eye reads slightly cyclops.
- Mouth sync is loudness-based (4 levels), not phonemes. Captions are timed proportionally, not by word alignment.
- B's bandit-mask outline can read as glasses at small sizes; the corner mascot is small, so fine detail (pupils, brow angle) is mostly lost there.
- Voices chosen from pitch statistics and fit, not by ear. Ears/mask of B are simple geometry, not illustrated.
- Generic archetypes (hooded figure, raccoon): do a reverse-image search before using as a brand identity.
