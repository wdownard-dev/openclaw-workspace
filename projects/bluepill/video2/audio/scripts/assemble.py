"""Assemble video-1 narration from passages (method A2 smooth join recipe of round 3).
Usage: assemble.py [--tight|--raw]    (tight = default deliverable; raw = same passages, model gaps untouched, for comparison)
Steps per passage: decode -> slow gain ride (+-4 dB, linear in dB between beat midpoints, no splice) -> beat-gap editing (cut the quietest stretch out of a long gap with a 20 ms
equal-power crossfade, or insert silence where the script asks for a longer beat) -> soft trim and 15 ms fade-in / 25 ms fade-out -> placed on the timeline with 0.40 s (0.50 s before a section) gaps.
Whole timeline: continuous -62 dBFS pink room tone, per-passage level match, two-pass loudnorm to -19 LUFS, alimiter (TP <= -1.5), wav + mp3 192k.
Outputs: narration_voice_only.wav/.mp3, words.json, beats_timing.json (+ _work/*.json for quality.py)."""
import os, sys, json, re, subprocess
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import *
from asm import fade, trim_soft, line_lufs, room_tone, artefact_stats
import words as Wd

MODE = "raw" if "--raw" in sys.argv else "tight"
LEAD, TAIL = 0.40, 1.0
JOIN, JOIN_SECTION = 0.15, 0.25           # silence between passages on top of the 0.05 s lead and 0.20 s tail pads, so word-to-word is 0.40 s (0.50 s before a section)
XF = 0.020                                # crossfade used where silence is cut out of a gap
# beat gaps (seconds between the last word of a beat and the first word of the next, inside a passage)
GAP_NN, GAP_NC, GAP_CC = 0.40, 0.32, 0.28
# caps on the model's own pauses INSIDE a beat (William approved the "tight2b" setting, 2026-11-13): after a sentence end / after a comma or colon / between other words
CAP_S, CAP_C, CAP_O = 0.35, 0.25, 0.20
HOLD = {(32, "first,"): 0.45, (39, "you."): 0.45, (44, "today?"): 0.45}   # holds the script asks for mid-beat: never cut below this
def cap_for(tok):
    if tok.endswith(('.', '!', '?', '."', '!"', '?"')): return CAP_S
    if tok.endswith((',', ':', ';', ',"')): return CAP_C
    return CAP_O
BEFORE = {80: 0.70, 96: 0.70, 105: 0.70, 113: 0.70,   # verdict stamp lines: 0.6-0.8 s beat before (SCRIPT-V3 (b), (e))
          119: 0.75,                                 # "Nobody."
          20: 0.55}                                  # "Ah." recorded after a 0.5 s beat (beat 20 note)
SECTION_START = {"P09", "P12", "P14", "P15"}          # passages that follow a TEXT-CHIP beat (59, 81, 97, 106)
CHIP_BEFORE = {"P09": 59, "P12": 81, "P14": 97, "P15": 106}

def ride(x, spans, limit=4.0):
    L = {b: line_lufs(x[int(max(0, t0 - 0.05) * SR):int((t1 + 0.1) * SR)]) for b, (t0, t1) in spans.items()}
    return L

def edit_gaps(x, ws, mode):
    """returns y, edits[(orig_t_a, orig_t_b, delta)] where delta = new length of the region minus old (neg = cut, pos = inserted silence)"""
    if mode == "raw": return x, []
    spk = {}
    for w in ws: spk[w["beat"]] = "N" if (w["speaker"] == "NARR") else "C"
    for w in ws:
        if w["added"]: pass
    # a beat is "C" if its script speaker is a character (attribution words are tagged NARR, so use the first word)
    first = {}
    for w in ws: first.setdefault(w["beat"], w["speaker"])
    kind = {b: ("N" if s == "NARR" else "C") for b, s in first.items()}
    # boundaries between beats
    # last word of each beat includes attribution words, so the gap is measured to whatever is spoken last
    last = {}
    for w in ws: last[w["beat"]] = w
    n = int(XF * SR); y = x.copy(); shift = 0; edits = []; info = []
    for a, b in zip(ws, ws[1:]):
        same = a["beat"] == b["beat"]
        if same: target = HOLD.get((a["beat"], a["word"].strip('"')), cap_for(a["word"]))
        else: target = BEFORE.get(b["beat"], GAP_NN if (kind[a["beat"]] == "N" and kind[b["beat"]] == "N") else (GAP_CC if (kind[a["beat"]] == "C" and kind[b["beat"]] == "C") else GAP_NC))
        gap = b["start"] - a["end"]; d = gap - target
        s0 = int(a["end"] * SR) + shift; s1 = int(b["start"] * SR) + shift
        if d > 0.04:                              # cut d seconds out of the quietest stretch of the gap
            m = 0.06 if same else 0.08
            R = int(d * SR); lo = s0 + int(m * SR); hi = s1 - int(m * SR) - n
            if hi - lo < R + n: R = max(0, hi - lo - n)
            if R <= 0: info.append((b["beat"], round(gap, 2), "skipped")); continue
            seg = np.abs(y[lo:hi + n]); win = R + n
            # quietest window of length win (sliding peak over 5 ms hops)
            hop = int(0.005 * SR); best = None
            for k in range(0, len(seg) - win + 1, hop):
                v = float(seg[k:k + win].max())
                if best is None or v < best[0]: best = (v, k)
            if best is None or db(best[0]) > (-40 if same else -45): info.append((b["beat"], round(gap, 2), "not quiet %.0f dB" % db(best[0] if best else 1))); continue
            a0 = lo + best[1]; b0 = a0 + R
            left = y[:a0 + n]; right = y[b0:]; t = np.linspace(0, np.pi / 2, n)
            y = np.concatenate([left[:-n], left[-n:] * np.cos(t) + right[:n] * np.sin(t), right[n:]])
            edits.append((a0 / SR - shift / SR, b0 / SR - shift / SR, -R / SR)); shift -= R
            info.append((b["beat"], round(gap, 2), round(gap - R / SR, 2)))
        elif d < -0.04 and not same:              # insert silence in the middle of the gap (between beats only)
            R = int(-d * SR); mid = (s0 + s1) // 2; f = int(0.008 * SR)
            left = y[:mid].copy(); right = y[mid:].copy(); left[-f:] *= np.cos(np.linspace(0, np.pi / 2, f)) ** 2; right[:f] *= np.sin(np.linspace(0, np.pi / 2, f)) ** 2
            y = np.concatenate([left, np.zeros(R, np.float32), right]); edits.append((mid / SR - shift / SR, mid / SR - shift / SR, R / SR)); shift += R
            info.append((b["beat"], round(gap, 2), round(gap + R / SR, 2)))
    return y, edits, info

def remap(t, edits):
    """map an original passage time to the edited passage time"""
    d = 0.0
    for a, b, delta in edits:
        if delta < 0:
            if t >= b: d += delta
            elif t > a: d += (t - a) * (delta / (b - a)) if b > a else 0.0
        else:
            if t >= a: d += delta
    return t + d

def main():
    plan = Wd.plan(); P = plan["passages"]; chips = {int(k): v for k, v in plan["chips"].items()}
    segs = []; allwords = []; beats = {}; passinfo = []; markers = []
    t = LEAD; parts = []
    for i, p in enumerate(P):
        x = load(os.path.join(OUT, "passages", p["id"] + ".mp3")); ws = Wd.words_of(p)
        spans = {}
        for w in ws:
            if w["added"]: continue
            s = spans.setdefault(w["beat"], [w["start"], w["end"]]); s[1] = w["end"]
        L = ride(x, spans); tgt = float(np.median(list(L.values())))
        ks = []; g = []
        for b, (t0, t1) in sorted(spans.items(), key=lambda kv: kv[1][0]): ks.append((t0 + t1) / 2); g.append(float(np.clip(tgt - L[b], -4, 4)))
        gt = np.interp(np.arange(len(x)) / SR, ks, g); x = (x * 10 ** (gt / 20)).astype(np.float32)
        y, edits, ginfo = edit_gaps(x, ws, MODE) if MODE != "raw" else (x, [], [])
        w0 = remap(ws[0]["start"], edits); w1 = remap(ws[-1]["end"], edits)
        a0 = max(0.0, w0 - 0.05); a1 = w1 + 0.20
        seg = y[int(a0 * SR):min(len(y), int(a1 * SR))]
        pl = line_lufs(seg); gain = float(np.clip(TARGET - pl, -6, 6)); seg = seg * 10 ** (gain / 20)
        seg = fade(seg, 0.015, 0.025)
        if i > 0:
            gap = JOIN_SECTION if p["id"] in SECTION_START else JOIN
            if p["id"] in CHIP_BEFORE: markers.append(dict(chip_beat=CHIP_BEFORE[p["id"]], text=chips[CHIP_BEFORE[p["id"]]], at=round(t + gap / 2, 3), note="TEXT-CHIP is on screen only; no audio of its own"))
            t += gap
        off = t - a0       # final time = edited passage time + off
        parts.append((int(round(t * SR)), seg))
        pw = []
        for w in ws:
            s = remap(w["start"], edits) + off; e = remap(w["end"], edits) + off
            d = dict(w); d["start"] = round(s, 3); d["end"] = round(e, 3); pw.append(d)
        allwords += pw
        passinfo.append(dict(id=p["id"], label=p["label"], start=round(t, 3), end=round(t + len(seg) / SR, 3), loudness_before_gain=round(pl, 1), gain_db=round(gain, 1),
                             gap_edits=ginfo, chars=p["chars"]))
        t += len(seg) / SR
    total = t + TAIL
    bus = np.zeros(int(total * SR) + SR // 2, np.float32)
    for s, y in parts: bus[s:s + len(y)] += y
    return bus, allwords, passinfo, markers, P

def finalize(bus, stem):
    x = bus + room_tone(len(bus) / SR, -62)[:len(bus)]
    tmp = f"{W}/_fin_{stem}.wav"; write_wav(tmp, x)
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", tmp, "-af", f"loudnorm=I={TARGET}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    af = (f"loudnorm=I={TARGET}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,alimiter=limit=0.89:level=false")
    wav = os.path.join(OUT, stem + ".wav"); mp3 = os.path.join(OUT, stem + ".mp3")
    subprocess.run([FF, "-y", "-v", "error", "-i", tmp, "-af", af, "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", wav], check=True)
    subprocess.run([FF, "-y", "-v", "error", "-i", wav, "-c:a", "libmp3lame", "-b:a", "192k", mp3], check=True)
    return wav, mp3, metrics.ebur(wav), metrics.ebur(mp3), j

if __name__ == "__main__":
    bus, words, passinfo, markers, P = main()
    stem = "narration_voice_only" if MODE == "tight" else "narration_voice_only_untightened"
    wav, mp3, Iw, Im, j = finalize(bus, stem)
    out = dict(mode=MODE, stem=stem, loudnorm_in=j, wav_I_LRA_TP=Iw, mp3_I_LRA_TP=Im, passages=passinfo, markers=markers)
    json.dump(out, open(os.path.join(W, f"assembled_{MODE}.json"), "w"), indent=1)
    json.dump(words, open(os.path.join(W, f"words_{MODE}.json"), "w"))
    print(MODE, "wav LUFS/LRA/TP", Iw, "mp3", Im, "duration", round(len(bus) / SR, 2))
