"""tighten2.py: same assembly as assemble.py --tight, plus caps on the model's own pauses INSIDE beats.
Does not touch narration_voice_only.*; writes narration_voice_only_<stem>.wav/.mp3 and _work/words_<stem>.json.
Usage: tighten2.py <stem> <sentence_cap> <comma_cap> <other_cap>
Holds the script asks for are kept: beat 32 after "first," / beat 39 after "you." / beat 44 after "today?" stay >= 0.45 s; inter-beat targets unchanged (assemble.BEFORE etc.)."""
import os, sys, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import assemble as A
from common import *

stem = sys.argv[1]; CAP_S, CAP_C, CAP_O = (float(v) for v in sys.argv[2:5])
HOLD = {(32, "first,"): 0.45, (39, "you."): 0.45, (44, "today?"): 0.45}

def cls(tok):
    if tok.endswith(('.', '!', '?', '."', '!"', '?"')): return CAP_S
    if tok.endswith((',', ':', ';', ',"')): return CAP_C
    return CAP_O

def edit_gaps2(x, ws, mode):
    first = {}
    for w in ws: first.setdefault(w["beat"], w["speaker"])
    kind = {b: ("N" if s == "NARR" else "C") for b, s in first.items()}
    n = int(A.XF * SR); y = x.copy(); shift = 0; edits = []; info = []
    for a, b in zip(ws, ws[1:]):
        if a["beat"] != b["beat"]:
            target = A.BEFORE.get(b["beat"], A.GAP_NN if (kind[a["beat"]] == "N" and kind[b["beat"]] == "N") else (A.GAP_CC if (kind[a["beat"]] == "C" and kind[b["beat"]] == "C") else A.GAP_NC))
        else:
            target = HOLD.get((a["beat"], a["word"].strip('"')), cls(a["word"]))
        gap = b["start"] - a["end"]; d = gap - target
        s0 = int(a["end"] * SR) + shift; s1 = int(b["start"] * SR) + shift
        if d > 0.04:
            R = int(d * SR); lo = s0 + int(0.06 * SR); hi = s1 - int(0.06 * SR) - n
            if hi - lo < R + n: R = max(0, hi - lo - n)
            if R <= 0: info.append((b["beat"], a["word"], round(gap, 2), "skipped")); continue
            seg = np.abs(y[lo:hi + n]); win = R + n; hop = int(0.005 * SR); best = None
            for k in range(0, len(seg) - win + 1, hop):
                v = float(seg[k:k + win].max())
                if best is None or v < best[0]: best = (v, k)
            if best is None or db(best[0]) > -40: info.append((b["beat"], a["word"], round(gap, 2), "not quiet %.0f dB" % db(best[0] if best else 1))); continue
            a0 = lo + best[1]; b0 = a0 + R
            left = y[:a0 + n]; right = y[b0:]; t = np.linspace(0, np.pi / 2, n)
            y = np.concatenate([left[:-n], left[-n:] * np.cos(t) + right[:n] * np.sin(t), right[n:]])
            edits.append((a0 / SR - shift / SR, b0 / SR - shift / SR, -R / SR)); shift -= R
            info.append((b["beat"], a["word"], round(gap, 2), round(gap - R / SR, 2)))
        elif d < -0.04 and a["beat"] != b["beat"]:
            R = int(-d * SR); mid = (s0 + s1) // 2; f = int(0.008 * SR)
            left = y[:mid].copy(); right = y[mid:].copy(); left[-f:] *= np.cos(np.linspace(0, np.pi / 2, f)) ** 2; right[:f] *= np.sin(np.linspace(0, np.pi / 2, f)) ** 2
            y = np.concatenate([left, np.zeros(R, np.float32), right]); edits.append((mid / SR - shift / SR, mid / SR - shift / SR, R / SR)); shift += R
            info.append((b["beat"], a["word"], round(gap, 2), round(gap + R / SR, 2)))
    return y, edits, info

A.edit_gaps = edit_gaps2
bus, words, passinfo, markers, P = A.main()
wav, mp3, Iw, Im, j = A.finalize(bus, "narration_voice_only_" + stem)
json.dump(words, open(os.path.join(W, f"words_{stem}.json"), "w"))
json.dump(dict(stem=stem, caps=[CAP_S, CAP_C, CAP_O], wav_I_LRA_TP=Iw, mp3_I_LRA_TP=Im, passages=passinfo, markers=markers), open(os.path.join(W, f"assembled_{stem}.json"), "w"), indent=1)
x = load(wav); st = A.artefact_stats(x)
gaps = [b["start"] - a["end"] for a, b in zip(words, words[1:])]
span = words[-1]["end"] - words[0]["start"]
skipped = sum(1 for p in passinfo for e in p["gap_edits"] if isinstance(e[-1], str))
print(json.dumps(dict(stem=stem, caps=[CAP_S, CAP_C, CAP_O], file_s=round(len(x) / SR, 2), mmss="%d:%02d" % divmod(int(len(x) / SR), 60), speech_span_s=round(span, 2),
                      pauses_ge_0_3_per_min=round(sum(g >= 0.3 for g in gaps) / span * 60, 1), gaps_ge_0_6=sum(g >= 0.6 for g in gaps), longest_gap=round(max(gaps), 2),
                      lufs=Iw, artefacts=st, edits_skipped=skipped)))
