"""V5 assemble: decode passages, tighten pauses (inside-beat caps 0.35/0.25/0.20 as V4 tight2b; beat gaps: sentence 0.40 cut/insert, continuation cap 0.30), place on a timeline,
room tone -62 dB, two-pass loudnorm -19 LUFS, wav+mp3, words.json, beats_timing.json. Run: clips-venv/bin/python -I assemble.py"""
import os, sys, json, re, subprocess
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); W = os.path.join(OUT, "_work")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(OUT)), "video2", "audio", "scripts"))
from asm import fade, line_lufs, room_tone, artefact_stats
from common import load, write_wav, FF, SR, TARGET, db
import metrics
CAP_S, CAP_C, CAP_O = 0.35, 0.25, 0.20
GAP_SENT, GAP_CONT = 0.40, 0.30
BEFORE = {174: 0.75}
LEAD, JOIN, TAIL, XF = 0.40, 0.55, 1.0, 0.020
plan = json.load(open(os.path.join(OUT, "plan.json")))["passages"]
def cap_for(tok):
    if re.search(r'[.!?]["”]?$|…$', tok): return CAP_S
    if re.search(r'[,:;]["”]?$', tok): return CAP_C
    return CAP_O
def words_of(p):
    al = json.load(open(os.path.join(OUT, "passages", p["id"] + ".json")))["alignment"]
    ch, ts, te = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    ws = []; i = 0
    for m in re.finditer(r"\S+", p["text"]):
        a, b = m.start(), m.end()
        beat = next(s["beat"] for s in p["segs"] if s["start"] <= a < s["end"])
        ws.append(dict(text=m.group(), start=ts[a], end=te[b-1], beat=beat, passage=p["id"], c0=a))
    return ws
def edit(x, ws):
    n = int(XF * SR); y = x.copy(); shift = 0.0; edits = []; log = []
    sent_end = {}
    for a, b in zip(ws, ws[1:]):
        same = a["beat"] == b["beat"]
        if same: tgt = cap_for(a["text"]); mode = "cut"
        else:
            endsent = bool(re.search(r'[.!?]["”]?$', a["text"])) and not re.match(r'[a-z]', b["text"])
            if b["beat"] in BEFORE: tgt = BEFORE[b["beat"]]; mode = "both"
            elif endsent: tgt = GAP_SENT; mode = "both"
            else: tgt = GAP_CONT; mode = "cut"
        gap = b["start"] - a["end"]; d = gap - tgt
        a_end = a["end"]; s0 = int(round((a_end + shift) * SR)); s1 = int(round((b["start"] + shift) * SR))
        if d > 0.04:
            R = int(d * SR); head = int((tgt / 2) * SR) if tgt > 0.1 else int(0.05 * SR)
            a0 = s0 + head; b0 = a0 + R
            if b0 > s1 - int(0.03 * SR): log.append((b["beat"], round(gap, 2), "skipped")); continue
            peak = db(float(np_abs(y[a0:b0 + n]).max()))
            if peak > -38: log.append((b["beat"], round(gap, 2), "not quiet %.0f dB" % peak)); continue
            t = np_lin(n); left = y[:a0 + n]; right = y[b0:]
            y = np_cat([left[:-n], left[-n:] * np_cos(t) + right[:n] * np_sin(t), right[n:]])
            edits.append((a0 / SR - shift, b0 / SR - shift, -R / SR)); shift -= R / SR; log.append((b["beat"], round(gap, 2), round(gap - R / SR, 2)))
        elif d < -0.04 and mode == "both":
            R = int(-d * SR); mid = (s0 + s1) // 2
            y = np_cat([y[:mid], np_zeros(R), y[mid:]]); edits.append((mid / SR - shift, mid / SR - shift, R / SR)); shift += R / SR
            log.append((b["beat"], round(gap, 2), round(gap + R / SR, 2)))
    return y, edits, log
import numpy as np
np_abs, np_lin, np_cat, np_cos, np_sin = np.abs, (lambda n: np.linspace(0, np.pi / 2, n)), np.concatenate, np.cos, np.sin
np_zeros = lambda R: np.zeros(R, np.float32)
def remap(t, edits):
    d = 0.0
    for a, b, delta in edits:
        if delta < 0:
            if t >= b: d += delta
            elif t > a: d += (t - a) * (delta / (b - a))
        elif t >= a: d += delta
    return t + d
t = LEAD; parts = []; allw = []; pinfo = []
for i, p in enumerate(plan):
    x = load(os.path.join(OUT, "passages", p["id"] + ".mp3")); ws = words_of(p)
    y, edits, log = edit(x, ws)
    w0 = remap(ws[0]["start"], edits); w1 = remap(ws[-1]["end"], edits)
    a0 = max(0.0, w0 - 0.05); seg = y[int(a0 * SR):min(len(y), int((w1 + 0.20) * SR))]
    pl = line_lufs(seg); seg = fade(seg * 10 ** (float(np.clip(TARGET - pl, -6, 6)) / 20), 0.015, 0.025)
    if i: t += JOIN
    off = t - a0; parts.append((int(round(t * SR)), seg))
    for w in ws:
        d = dict(w); d["start"] = round(remap(w["start"], edits) + off, 3); d["end"] = round(remap(w["end"], edits) + off, 3); allw.append(d)
    pinfo.append(dict(id=p["id"], label=p["label"], start=round(t, 3), end=round(t + len(seg) / SR, 3), chars=p["chars"], gap_edits=log)); t += len(seg) / SR
total = t + TAIL; bus = np.zeros(int(total * SR) + SR // 2, np.float32)
for s, y in parts: bus[s:s + len(y)] += y
x = bus + room_tone(len(bus) / SR, -62)[:len(bus)]; tmp = os.path.join(W, "_fin.wav"); write_wav(tmp, x)
r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", tmp, "-af", f"loudnorm=I={TARGET}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
j = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
af = (f"loudnorm=I={TARGET}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,alimiter=limit=0.89:level=false")
wav = os.path.join(OUT, "narration_voice_only.wav"); mp3 = os.path.join(OUT, "narration_voice_only.mp3")
subprocess.run([FF, "-y", "-v", "error", "-i", tmp, "-af", af, "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", wav], check=True)
subprocess.run([FF, "-y", "-v", "error", "-i", wav, "-c:a", "libmp3lame", "-b:a", "192k", mp3], check=True)
json.dump(allw, open(os.path.join(OUT, "words.json"), "w"))
bt = {}
for w in allw:
    s = bt.setdefault(w["beat"], dict(start=w["start"], end=w["end"], passage=w["passage"], words=0)); s["end"] = w["end"]; s["words"] += 1
bt = {(f"N-{int(k):03d}a" if k != int(k) else f"N-{int(k):03d}"): dict(start=v["start"], end=v["end"], duration=round(v["end"] - v["start"], 3), passage=v["passage"], words=v["words"]) for k, v in sorted(bt.items())}
json.dump(bt, open(os.path.join(OUT, "beats_timing.json"), "w"), indent=1)
json.dump(dict(passages=pinfo, loudnorm_in=j, wav=metrics.ebur(wav), mp3=metrics.ebur(mp3), duration=round(len(bus) / SR, 2)), open(os.path.join(W, "assembled.json"), "w"), indent=1)
print("done", metrics.ebur(wav), round(len(bus) / SR, 2), [len(p["gap_edits"]) for p in pinfo])
