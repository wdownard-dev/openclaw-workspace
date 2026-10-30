import os, sys
os.environ["PATH"] = os.path.expanduser("~/openclaw-sites/bin") + os.pathsep + os.environ["PATH"]
from faster_whisper import WhisperModel
m = WhisperModel("base.en", device="cpu", compute_type="int8", download_root=os.path.expanduser("~/openclaw-sites/models"))
for part, a, b in [(5,28,40)]:
    segs,_ = m.transcribe(f"source/fg-p{part}.mp4", beam_size=1, word_timestamps=True, vad_filter=False, clip_timestamps=[a,b], condition_on_previous_text=False)
    print(f"=== p{part} {a}-{b}")
    print(" ".join(f"{w.word.strip()}[{w.start:.1f}]" for s in segs for w in s.words))
