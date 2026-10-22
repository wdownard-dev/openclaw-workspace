#!/usr/bin/env python3
"""Transcribe a clip locally (CPU, faster-whisper base.en) to JSON with timestamps.

Usage (run with the project venv):
  ~/openclaw-sites/clips-venv/bin/python transcribe.py CLIP.mp4 OUT.json

Output: {"duration": s, "language": "en", "text": "...", "segments": [{"start","end","text"}]}
Everything runs on this machine; no audio leaves it. The ffmpeg binary at
~/openclaw-sites/bin/ffmpeg is put on PATH so faster-whisper can decode mp4/mkv.
"""
import json, os, sys, time

os.environ["PATH"] = os.path.expanduser("~/openclaw-sites/bin") + os.pathsep + os.environ.get("PATH", "")
from faster_whisper import WhisperModel

MODEL_DIR = os.path.expanduser("~/openclaw-sites/models")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    t0 = time.time()
    model = WhisperModel("base.en", device="cpu", compute_type="int8", download_root=MODEL_DIR)
    segments, info = model.transcribe(src, beam_size=1, vad_filter=True, condition_on_previous_text=False)
    segs = [{"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()} for s in segments]
    data = {"duration": round(info.duration, 2), "language": info.language,
            "text": " ".join(s["text"] for s in segs), "segments": segs}
    json.dump(data, open(out, "w"), indent=2)
    print(f"{info.duration:.1f}s of audio transcribed in {time.time() - t0:.1f}s -> {out}")
    print("TEXT:", data["text"][:300] or "(no speech detected)")


if __name__ == "__main__":
    main()
