"""Word-level timestamps via local faster-whisper. Usage: words.py SRC.mp4 OUT.json"""
import json, os, sys
os.environ["PATH"] = os.path.expanduser("~/openclaw-sites/bin") + os.pathsep + os.environ.get("PATH", "")
from faster_whisper import WhisperModel
m = WhisperModel("base.en", device="cpu", compute_type="int8", download_root=os.path.expanduser("~/openclaw-sites/models"))
segs, _ = m.transcribe(sys.argv[1], beam_size=1, vad_filter=True, word_timestamps=True, condition_on_previous_text=False)
w = [{"s": round(x.start, 2), "e": round(x.end, 2), "w": x.word.strip()} for s in segs for x in s.words]
json.dump(w, open(sys.argv[2], "w")); print(len(w), "words")
