"""Generate the same snarky line with several Kokoro voices, score clarity (faster-whisper WER) and pitch (autocorr F0)."""
import sys, os, json, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "voices")
LINE = "Oh, that was the play? Sure. I've seen smoother moves from a loading screen, but fine, I'll allow it."
VOICES = ["am_onyx", "bm_lewis", "am_fenrir", "bm_george", "am_michael", "bm_fable", "am_puck", "bm_daniel"]
SPEEDS = [0.92]
from kokoro import KPipeline
pipes = {}
res = {}
for v in VOICES:
    for sp in SPEEDS:
        lc = "b" if v.startswith("b") else "a"
        pipes.setdefault(lc, KPipeline(lang_code=lc, repo_id="hexgrad/Kokoro-82M"))
        try:
            w = np.concatenate([r[2].numpy() for r in pipes[lc](LINE, voice=v, speed=sp)])
        except Exception as e:
            print("fail", v, e); continue
        p = os.path.join(OUT, f"{v}_{sp}.wav"); sf.write(p, w, 24000)
        # F0 via autocorrelation on voiced frames
        f0s = []
        hop, win = 480, 960
        for i in range(0, len(w) - win, hop):
            x = w[i:i + win]
            if np.sqrt((x ** 2).mean()) < 0.03: continue
            x = x - x.mean(); ac = np.correlate(x, x, "full")[win - 1:]
            lo, hi = 24000 // 300, 24000 // 70
            k = lo + np.argmax(ac[lo:hi])
            if ac[k] / (ac[0] + 1e-9) > 0.45: f0s.append(24000 / k)
        res[f"{v}_{sp}"] = dict(dur=round(len(w) / 24000, 2), f0=round(float(np.median(f0s)), 1) if f0s else None,
                                f0_sd=round(float(np.std(f0s)), 1) if f0s else None)
        print(v, sp, res[f"{v}_{sp}"], flush=True)
json.dump(res, open(os.path.join(OUT, "audition.json"), "w"), indent=1)
