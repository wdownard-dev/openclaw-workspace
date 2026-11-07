# AI co-host mascot options (6 original characters, all code-drawn, free/local)

Pick one: `contact-sheet.png` (3x2 grid), `montage.mp4` (45 s, 1080x1920, H.264/AAC, ~3 MB, each character says a short intro). Individual clips are in `clips/`, mid-clip stills in `stills/`.

| Folder | Name | Vibe | Palette | Kokoro voice |
|---|---|---|---|---|
| `volt/` | VOLT, "Fast takes. Faster foxes." | neon cyber-fox, glowing visor, LED brows | orange + cyan + magenta | `af_nova` (speed 1.08) |
| `quarter/` | QUARTER, "Insert coin. Receive opinions." | true pixel-art arcade cabinet, CRT face | purple + yellow + green | `am_fenrir` |
| `wisp/` | WISP, "Cozy vibes. Chaotic commentary." | friendly mint ghost, RGB headphones | mint + pink | `af_sky` |
| `null/` | NULL, "No face. All takes." | hooded esports silhouette, slit eyes, equalizer mouth | violet + acid green | `am_onyx` (0.97) |
| `rascal/` | RASCAL, "Zero chill. Maximum snark." | smug/grumpy raccoon, crimson headset | grey + crimson | `bm_lewis` |
| `orb/` | ORB-7, "Beep boop. Actually correct." | glossy 3D-look droid, LED-matrix face, halo ring | silver + electric blue | `af_kore` |

Each folder holds 8 transparent 600x600 PNGs: `<slug>_{closed,small,open,wide}.png` plus `<slug>_{...}_blink.png`. Intro lines and voices are in `chars/<slug>.py` (`LINE`, `VOICE`, `SPEED`). Voices were picked by character fit and not auditioned by ear, so listen to the montage and swap any that feel off. The Kokoro voice files were downloaded free from the Hugging Face repo into the HF cache.

## How they are made
- `lib.py`: small toolkit on Pillow + numpy. Everything is drawn at 3x and downscaled with LANCZOS (premultiplied alpha, so there are no dark fringes). Provides shape masks, Catmull-Rom smooth outlines, linear/radial gradients, soft glows, blurred shading clipped to a shape, and a bottom fade for bust characters.
- `chars/<slug>.py`: one `draw(mouth, blink)` function per character. Layers: rim glow, gradient body, shading/highlights, outline strokes, eyes with highlights, eyebrows that lift on louder mouth states, and mouth shapes. QUARTER is the exception: it is drawn on a 40x40 grid and upscaled with nearest-neighbour so the pixels stay crisp.
- `make_frames.py` renders the PNG sets; `build_clips.py <slug>` does Kokoro TTS, a mouth state per video frame from the voice loudness (4 levels, 3-frame median smoothing), idle bob and breathing (scale anchored at the bottom), speech bounce, scheduled blinks, captions, name/tag labels, and pipes raw frames into ffmpeg; `make_sheet.py` builds the contact sheet and concatenates the montage.
- Regenerate: `PY=/home/williamdownard/openclaw-sites/tts-venv/bin/python; $PY make_frames.py; for s in volt quarter wisp null rascal orb; do $PY build_clips.py $s; done; $PY make_sheet.py` (add `--skip-tts` to `build_clips.py` to reuse the saved voice).

## Swap one into the demo pipeline (`../cohost-demo/`)
The demo's `build.py` expects 3 mouth states named `mascot_{closed,half,open}[_blink].png` in `cohost-demo/frames/`. Mapping from these sets: `closed -> closed`, `small -> half`, `open -> open`; `wide` is the extra louder state. Quick swap:
```
S=rascal   # any slug
for m in closed:closed small:half open:open; do a=${m%%:*}; b=${m##*:}
  cp cohost-options/$S/${S}_$a.png cohost-demo/frames/mascot_$b.png
  cp cohost-options/$S/${S}_${a}_blink.png cohost-demo/frames/mascot_${b}_blink.png; done
```
Then set `"voice"` / `"speed"` in `cohost-demo/config.json` to the values above and run `build.py --skip-tts` (or without, to re-voice). To use all 4 states, change `names` in `stream_mascot()` to `["closed","small","open","wide"]` and the state thresholds in `mouth_states()` to `np.digitize(e, [0.12, 0.38, 0.70])` (as in `build_clips.py`). For QUARTER, resize with `Image.NEAREST` to keep pixels sharp. Bust characters (VOLT, NULL, RASCAL) fade out at the bottom so they sit on any background.

## Supplying your own art or using an image generator
Any transparent PNG set works: a closed mouth, a small, an open and (optionally) a wide mouth, same canvas size and same head position in every frame, plus blink versions (or skip blink and reuse the open-eyes frames). Name them `<slug>_closed.png`, `<slug>_small.png`, `<slug>_open.png`, `<slug>_wide.png` (+ `_blink`), drop them into a new folder, add a tiny `chars/<slug>.py` with `NAME, TAGLINE, VOICE, SPEED, LINE, ACCENT, BG, SLUG` (its `draw()` is not needed for rendering clips), and run `build_clips.py <slug>`. With an image generator: make one character on a plain background, then ask for edits of the same image changing only the mouth/eyes ("same character, mouth open wide", "eyes closed"). Remove the background (e.g. rembg, free) and align the frames. Keep the head fixed so the mouth swaps do not jitter. A layered PSD/SVG exported per mouth is better still. Alternatives that give true animation (not just mouth swaps): a Live2D or VTube-style rig, or Rive.

## Honest limitations of code-drawn characters
- Style ceiling: layered gradients and glows look clean and polished but not like a commissioned illustration. There is no hand-drawn line variation, painterly shading, or fur and cloth texture.
- Animation is only mouth swaps, blink, bob and breathing. There are no head turns, gestures, or lip-sync visemes beyond 4 openness levels. WISP and QUARTER wave an arm on the loudest state only.
- Mouth states follow loudness, not phonemes, so they read as "talking" but not as exact lip-sync.
- Characters are static drawings viewed front-on; changing pose or angle means redrawing code.
- QUARTER is the only one that is truly pixel-art. Scaling it by non-integer factors blurs it.
- Voices are stock Kokoro voices, clearly synthetic and not tuned per character; the intro lines are generic and make no game claims.
- Characters are original designs, but generic archetypes (fox, raccoon, ghost, hooded figure, droid). Run a quick reverse-image search before using any of them as a brand identity.
