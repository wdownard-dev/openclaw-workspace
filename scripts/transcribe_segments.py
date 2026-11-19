import sys, json
from faster_whisper import WhisperModel
wav, out = sys.argv[1], sys.argv[2]
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(wav, language="en", vad_filter=True)
rows = [{"start": round(s.start,2), "end": round(s.end,2), "text": s.text.strip()} for s in segs]
json.dump(rows, open(out, "w"), indent=1)
for r in rows: print(r["start"], r["end"], r["text"])
