"""Write words.json, beats_timing.json, quality.json, risky.json from the tight assembly (assembled_tight.json + words_tight.json) and the final wav.
Run: finalize_outputs.py"""
import os, sys, json, re, csv, statistics as S
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import *
from asm import artefact_stats
from tools import role_measure
import words as Wd

plan = Wd.plan(); P = plan["passages"]; chips = {int(k): v for k, v in plan["chips"].items()}
asm = json.load(open(os.path.join(W, "assembled_tight.json"))); raw = json.load(open(os.path.join(W, "assembled_raw.json")))
ws = json.load(open(os.path.join(W, "words_tight.json")))
Bs = parse_script()
# ---- words.json: video1 format + speaker/passage/added; text = the script word, spoken = word as sent to TTS (quotes stripped)
by_beat = {}
for w in ws: by_beat.setdefault(w["beat"], []).append(w)
out = []; i = 0
for b, L in sorted(by_beat.items()):
    toks = Bs[b][1].split(); sc = [w for w in L if not w["added"]]
    assert len(sc) == len(toks), (b, len(sc), len(toks))
    for w in L:
        if w["added"]: text = None
        else: text = toks[[x for x in L if not x["added"]].index(w)]
        spoken = w["word"].strip('"')
        out.append(dict(i=None, text=text if text is not None else spoken, spoken=spoken, start=w["start"], end=w["end"], beat=b, speaker=w["speaker"], passage=w["passage"],
                        added=w["added"], respelled=(text is not None and re.sub(r'^"|"$|[,.]$', "", spoken) != re.sub(r'^"|"$|[,.]$', "", text) if text else False)))
out.sort(key=lambda d: d["start"])
for k, d in enumerate(out): d["i"] = k
json.dump(out, open(os.path.join(OUT, "words.json"), "w"), indent=0)

# ---- beats_timing.json
bt = []; prev_end = None
idx_of = {}
for k, d in enumerate(out): idx_of.setdefault(d["beat"], []).append(k)
beats_all = sorted(set(list(Bs.keys()) + list(chips.keys())))
pass_of = {b: p["id"] for p in P for b in p["beats"]}
for b in beats_all:
    if b in chips:
        mk = next(m for m in asm["markers"] if m["chip_beat"] == b)
        bt.append(dict(beat=b, type="text-chip", spoken=False, text=chips[b], start=mk["at"], end=mk["at"], duration=0.0, words=0, speaker="TEXT-CHIP",
                       note="on-screen only, zero audio duration; `at` is the middle of the passage join"))
        continue
    if b not in idx_of: continue
    L = [out[k] for k in idx_of[b]]; sc = [d for d in L if not d["added"]]; ad = [d for d in L if d["added"]]
    seg = next(sg for p in P for sg in p["segs"] if sg["beat"] == b)
    e = dict(beat=b, type="line", spoken=True, speaker=seg["speaker"], passage=pass_of[b], text=Bs[b][1], words=len(sc), first_word=sc[0]["i"], last_word=sc[-1]["i"],
             start=sc[0]["start"], end=sc[-1]["end"], duration=round(sc[-1]["end"] - sc[0]["start"], 3))
    if ad:
        e["attribution"] = dict(text=" ".join(d["spoken"] for d in ad), start=ad[0]["start"], end=ad[-1]["end"], first_word=ad[0]["i"], last_word=ad[-1]["i"])
        e["end_with_attribution"] = ad[-1]["end"]
    last_end = e.get("end_with_attribution", e["end"])
    e["gap_before"] = None if prev_end is None else round(e["start"] - prev_end, 3)
    prev_end = last_end; bt.append(e)
json.dump(bt, open(os.path.join(OUT, "beats_timing.json"), "w"), indent=1)

# ---- quality
x = load(os.path.join(OUT, "narration_voice_only.wav")); xr = load(os.path.join(OUT, "narration_voice_only_untightened.wav"))
dur = len(x) / SR; first = out[0]["start"]; last = out[-1]["end"]
sw = [d for d in out if not d["added"]]; nadd = sum(1 for d in out if d["added"])
per = []
for p in asm["passages"]:
    pw = [d for d in out if d["passage"] == p["id"]]; ps = [d for d in pw if not d["added"]]; span = pw[-1]["end"] - pw[0]["start"]
    per.append(dict(passage=p["id"], label=p["label"], beats=f'{P[[q["id"] for q in P].index(p["id"])]["beats"][0]}-{P[[q["id"] for q in P].index(p["id"])]["beats"][-1]}', start=round(pw[0]["start"], 2), end=round(pw[-1]["end"], 2),
                    script_words=len(ps), spoken_words=len(pw), seconds=round(span, 2), wpm_script_words=round(len(ps) / span * 60), wpm_all_spoken=round(len(pw) / span * 60), chars=p["chars"]))
gaps = [(b["start"] - a["end"], a, b) for a, b in zip(out, out[1:])]
pauses = [g for g, a, b in gaps]
lg = max(gaps, key=lambda t: t[0])
runtime_speech = last - first
# longest RMS silence (20 ms frames below -45 dBFS) between first and last word
r, H = rms_db_frames(x, 20); a0 = int(first / 0.02); a1 = int(last / 0.02); run = 0; best = 0; best_at = 0
for k in range(a0, a1):
    if r[k] < -45: run += 1
    else:
        if run > best: best = run; best_at = k - run
        run = 0
# per-role measures (final timeline, script words only, quoted lines only); narrator vs D4 control
roles = {}
for spk in ("NARR", "ODY", "POLY", "CREW", "CYC2"):
    segs = []; txt = []
    for e in bt:
        if e.get("type") == "line" and e["speaker"] == spk:
            segs.append(x[int(max(0, e["start"] - 0.05) * SR):int((e["end"] + 0.12) * SR)]); txt.append(e["text"])
    roles[spk] = role_measure(segs, " ".join(txt), "q_" + spk); roles[spk]["lines"] = len(segs)
allseg = x[int(first * SR):int((last + 0.1) * SR)]; whole = role_measure([allseg], " ".join(d["text"] for d in sw), "q_all")
ctrl = {"note": "Daniel D4 control (voices2 AUDITION2): 149 wpm, F0 mean 137 Hz, spread 3.77 st, LRA 1.6 LU, centroid 590 Hz; round-3 A2 narrator: 150 wpm, 133/136 Hz, 3.76 st, 577 Hz"}
art = artefact_stats(x); art_raw = artefact_stats(xr)
# join artefacts: detector events within 60 ms of a passage join or gap edit
join_t = [p["start"] for p in asm["passages"][1:]]
edit_ts = []
q = dict(
    files=dict(wav="narration_voice_only.wav", mp3="narration_voice_only.mp3", comparison_wav="narration_voice_only_untightened.wav (same passages, model gaps untouched)"),
    runtime=dict(file_seconds=round(dur, 2), file_mmss="%d:%02d" % (dur // 60, round(dur % 60)), first_word_s=round(first, 2), last_word_s=round(last, 2),
                 speech_seconds=round(runtime_speech, 2), speech_mmss="%d:%02d" % (runtime_speech // 60, round(runtime_speech % 60)),
                 untightened_file_seconds=round(len(xr) / SR, 2), untightened_mmss="%d:%02d" % (len(xr) / SR // 60, round(len(xr) / SR % 60)),
                 target="about 10:20-10:40", script_estimate="10:49 at 155 wpm raw"),
    words=dict(script_words=len(sw), added_by_A2_attribution=nadd, spoken_words=len(out)),
    wpm=dict(overall_script_words_over_speech_span=round(len(sw) / runtime_speech * 60), overall_all_spoken_words=round(len(out) / runtime_speech * 60),
             narrator_speech_only_measure2=roles["NARR"]["wpm"], whole_measure2=whole["wpm"], per_passage=per),
    loudness=dict(wav_I_LRA_TP=asm["wav_I_LRA_TP"], mp3_I_LRA_TP=asm["mp3_I_LRA_TP"], loudnorm_input=asm["loudnorm_in"], target="-19 LUFS integrated, TP <= -1 dBFS",
                  per_passage_gain_db=[dict(p=p["id"], before=p["loudness_before_gain"], gain=p["gain_db"]) for p in asm["passages"]]),
    silence=dict(longest_gap_between_words_s=round(lg[0], 2), at_s=round(lg[1]["end"], 2), between=f'beat {lg[1]["beat"]} -> {lg[2]["beat"]}', longest_rms_silence_below_minus45dBFS_s=round(best * 0.02, 2),
                 gaps_ge_0_3_per_min=round(sum(1 for g in pauses if g >= 0.3) / (runtime_speech / 60), 1), gaps_ge_0_6_count=sum(1 for g in pauses if g >= 0.6),
                 gaps_ge_0_6_per_min=round(sum(1 for g in pauses if g >= 0.6) / (runtime_speech / 60), 1), gaps_ge_0_9_count=sum(1 for g in pauses if g >= 0.9),
                 beat_gap_edits_made=sum(len(p["gap_edits"]) for p in asm["passages"])),
    joins=dict(detector="same as round 3 asm.artefact_stats: adjacent 5 ms RMS frames >35 dB apart with the louder above -45 dBFS; click = step >8x median speech step", tight=art, untightened=art_raw,
               passage_joins=len(join_t), crossfades="20 ms equal-power where silence was cut out of a gap; passage joins sit in room-tone gaps with 15 ms fade-in / 25 ms fade-out"),
    pitch_and_timbre=dict(whole=whole, per_role=roles, daniel_control=ctrl),
    calls=dict(note="see voice_log.csv; characters and calls added below by the report script"),
)
with open(os.path.join(OUT, "voice_log.csv")) as f: rows = list(csv.DictReader(f))
q["calls"] = dict(calls=len(rows), retakes=sum(1 for r in rows if r["note"] == "retake"), characters_sent=sum(int(r["characters"]) for r in rows))
json.dump(q, open(os.path.join(OUT, "quality.json"), "w"), indent=1)
print(json.dumps({k: q[k] for k in ("runtime", "words", "loudness", "silence", "joins", "calls")}, indent=1)[:3500])
print("roles", json.dumps(roles)); print("whole", whole); print("overall wpm", q["wpm"]["overall_script_words_over_speech_span"], q["wpm"]["overall_all_spoken_words"])
