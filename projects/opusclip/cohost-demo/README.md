# AI co-host outro demo (local, free tools only)

Output: `cohost-demo.mp4` (1080x1920, 30 fps, H.264/AAC, 32.4 s, about 7 MB). Demo script text is placeholder, generic, and makes no game claims.

## Regenerate
```
cd /home/williamdownard/.openclaw/workspace/projects/opusclip/cohost-demo
/home/williamdownard/openclaw-sites/tts-venv/bin/python mascot.py                 # redraw mascot PNGs -> frames/
/home/williamdownard/openclaw-sites/clips-venv/bin/python transcribe.py CLIP.mp4 words.json   # optional: word timestamps to choose interjection moments
/home/williamdownard/openclaw-sites/tts-venv/bin/python build.py                  # TTS + captions + render
/home/williamdownard/openclaw-sites/tts-venv/bin/python build.py --skip-tts       # re-render only, reuse voice.wav/timeline.json
```
Setup (done once): `python3 -m venv tts-venv; tts-venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu; tts-venv/bin/pip install kokoro soundfile numpy pillow` (installs the CPU torch wheel to avoid multi-GB CUDA downloads). Kokoro-82M weights download from HuggingFace on first run; espeak data comes via pip.

## What the pipeline does per clip
1. Whisper word timestamps find gaps/moments in the clip; the agent writes 1-2 short interjections tied to those moments plus a 3-part outro (takeaway, opinion, question).
2. Kokoro-82M (CPU) voices each line; lines are placed on a timeline into `voice.wav`.
3. Mouth state per video frame (30 fps) from the RMS loudness of the voice: closed / half / open, with 3-frame median smoothing, idle bob, speech bounce, periodic blink.
4. ffmpeg: clip fit over blurred copy of itself, crossfade to gradient outro, mascot RGBA frames piped in (small corner, then grows to centre at the outro), ASS captions + "AI CO-HOST" tag, clip audio ducked by `sidechaincompress` keyed on the voice.

## Timing (12 CPU threads, no GPU)
- Kokoro: about 0.3x real time (5.1 s of speech in 1.6 s) after about 10 s model load.
- Full build: about 47 s (TTS+prep 9 s, render 37 s) for a 32 s video. Re-render only: about 39 s.

## Swap things
- Script, voice, timing, clip, positions: edit `config.json` (`interjections[].at` is seconds into the clip segment; `outro[]` lines follow each other; `voice` e.g. `am_puck`, `af_heart`, `am_adam`; `speed`; `clip_start`/`clip_len` pick the source segment).
- Mascot: edit the drawing code in `mascot.py` (any PNG set named `mascot_{closed,half,open}[_blink].png` in `frames/` works; 600x600 transparent).
- Captions style/positions: styles at the top of `write_ass()` in `build.py`.

## Known flaws
- Sample footage is a third-party clip from local `clips-work/cut/mw4-01-cut.mp4`; demo only, not for posting.
- Voice is stock Kokoro (`am_puck`), clearly synthetic; interjections are generic.
- Captions are timed proportionally to text length, not from true word alignment.
- Mascot is flat/2D with 3 mouth shapes; no body gestures.
