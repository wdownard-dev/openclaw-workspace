import os, sys, json, subprocess, re
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(OUT), "audio", "scripts"))
from asm import artefact_stats
from common import load, FF, SR
import numpy as np
A = json.load(open(os.path.join(OUT, "_work", "assembled.json"))); words = json.load(open(os.path.join(OUT, "words.json"))); bt = json.load(open(os.path.join(OUT, "beats_timing.json")))
wav = os.path.join(OUT, "narration_voice_only.wav"); x = load(wav)
r = subprocess.run([FF, "-hide_banner", "-i", wav, "-af", "silencedetect=n=-45dB:d=0.9", "-f", "null", "-"], capture_output=True, text=True).stderr
sil = [(float(a), float(b)) for a, b in re.findall(r"silence_start: ([\d.]+)", r) and zip(re.findall(r"silence_start: ([\d.]+)", r), re.findall(r"silence_duration: ([\d.]+)", r))]
nw = len(words); span = words[-1]["end"] - words[0]["start"]
ws = [w for w in words]; gaps = [(round(b["start"] - a["end"], 2), a["beat"], b["beat"]) for a, b in zip(ws, ws[1:])]
unc = []; ids = list(bt); prev = None
for k in ids:
    v = bt[k]
    if prev and v["start"] < prev["end"] - 0.001: unc.append((k, "overlaps previous"))
    if v["duration"] / v["words"] > 0.9 or v["duration"] / v["words"] < 0.15: unc.append((k, "odd duration/word %.2f" % (v["duration"] / v["words"])))
    prev = v
q = dict(duration_s=A["duration"], lufs=A["wav"], mp3=A["mp3"], speech_start=words[0]["start"], speech_end=words[-1]["end"], words=nw, wpm_over_speech_span=round(nw / span * 60),
         wpm_per_passage=[dict(passage=p["id"], wpm=round(sum(1 for w in words if w["passage"] == p["id"]) / (p["end"] - p["start"]) * 60)) for p in A["passages"]],
         beats=len(bt), cut_beats_absent=True, silences_over_0_9s=[(round(a, 2), d) for a, d in sil], longest_word_gaps=sorted(gaps, reverse=True)[:6],
         artefacts=artefact_stats(x), per_passage_artefacts=[dict(passage=p["id"], **artefact_stats(x[int(p["start"] * SR):int(p["end"] * SR)])) for p in A["passages"]],
         uncertain_beats=unc, gap_edit_skips=[(p["id"], g) for p in A["passages"] for g in p["gap_edits"] if isinstance(g[2], str)])
json.dump(q, open(os.path.join(OUT, "quality.json"), "w"), indent=1); print(json.dumps({k: q[k] for k in q if k not in ("beats",)}, indent=0)[:3500])
