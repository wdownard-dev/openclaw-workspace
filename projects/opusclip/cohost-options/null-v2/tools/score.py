import sys, glob, os, re, json
from faster_whisper import WhisperModel
LINE = "Oh, that was the play? Sure. I've seen smoother moves from a loading screen, but fine, I'll allow it."
norm = lambda s: re.sub(r"[^a-z' ]", "", s.lower().replace("-", " ")).split()
def wer(ref, hyp):
    r, h = norm(ref), norm(hyp); d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (r[i - 1] != h[j - 1]))
    return d[-1] / len(r)
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=12, download_root="/home/williamdownard/openclaw-sites/models")
out = {}
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "voices", "*.wav"))):
    segs, _ = m.transcribe(f, language="en")
    t = " ".join(s.text for s in segs)
    out[os.path.basename(f)] = round(wer(LINE, t), 3); print(os.path.basename(f), out[os.path.basename(f)], "|", t.strip())
json.dump(out, open(os.path.join(os.path.dirname(__file__), "..", "voices", "wer.json"), "w"), indent=1)
