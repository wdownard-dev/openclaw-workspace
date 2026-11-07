"""Run with clips-venv python: transcribe.py CLIP.mp4 OUT.json  -> words with timestamps (faster-whisper, CPU)."""
import json, sys
from faster_whisper import WhisperModel
clip, out, model, root = sys.argv[1:5]
m = WhisperModel(model, device="cpu", compute_type="int8", download_root=root)
segs, info = m.transcribe(clip, word_timestamps=True, vad_filter=False)
res = {"duration": info.duration, "segments": []}
for s in segs:
    res["segments"].append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
                            "words": [{"w": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)} for w in s.words]})
json.dump(res, open(out, "w"), indent=1)
print(f"{len(res['segments'])} segments")
