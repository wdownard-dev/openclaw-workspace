"""Word-level transcript of the clip -> words.json. Usage: transcribe.py clip.mp4 out.json"""
import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=12,
                 download_root="/home/williamdownard/openclaw-sites/models")
segs, _ = m.transcribe(sys.argv[1], word_timestamps=True, vad_filter=True)
words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in s.words]
json.dump(words, open(sys.argv[2], "w"), indent=1)
print(" ".join(f"{w['w']}[{w['s']}]" for w in words))
