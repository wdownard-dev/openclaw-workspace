"""Write SPOKEN-TEXT.md and LISTEN-FIRST.md from plan.json, words.json, beats_timing.json, quality.json."""
import os, sys, json, re
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import *
import importlib.util as _iu
_s=_iu.spec_from_file_location("bp_plan",os.path.join(HERE,"plan.py")); PL=_iu.module_from_spec(_s); _s.loader.exec_module(PL)
OUTD = OUT
plan = json.load(open(os.path.join(OUT, "plan.json"))); P = plan["passages"]
words = json.load(open(os.path.join(OUT, "words.json"))); bt = {b["beat"]: b for b in json.load(open(os.path.join(OUT, "beats_timing.json"))) if b["type"] == "line"}
Q = json.load(open(os.path.join(OUT, "quality.json")))
Bs = parse_script()
def mmss(t): return "%d:%05.2f" % (t // 60, t % 60)

# ---------------- SPOKEN-TEXT.md
L = []
L.append("# SPOKEN-TEXT.md: exactly what was sent to the voice, video 1 (SCRIPT-V4 = V3 with the approved cuts, method A2)\n")
L.append("Voice Daniel (`onwK4e9ZLuTAKqWW03F9`), `eleven_multilingual_v2`, stability 0.5, style 0.2, speed 1.0, similarity 0.75, speaker boost on. No audio tags. One continuous call per passage (16 passages), `previous_text` / `next_text` = the neighbouring passages' text. Beats are separated by a blank line inside a passage (as in round-3 A2). TEXT-CHIP beats 59, 81, 97, 106 are on screen only and are not in the text.\n")
L.append("## What the A2 technique adds or changes (nothing else was altered)\n")
L.append("1. **Quotation marks** around every character line (never spoken, but they set the voice up as a quotation). A final full stop becomes a comma when an attribution follows (`...Have some wine,\" said Odysseus`); `?` and `!` stay.")
L.append("2. **Attribution words** after 21 of the 35 character lines (listed below). These words are **spoken**: 63 words in all, tagged `added: true` and `speaker: NARR` in `words.json`, kept out of `beats_timing.json` `start`/`end` (they get their own `attribution` span). Seven are exactly as in round-3 A2 (28, 30, 31, 37, 38, 39, 64); fourteen are new, same pattern.")
L.append("3. **No attribution** on the 14 remaining character lines: replies inside an exchange (15, 16, 19, 25, 32, 33, 50, 53, 86) and the one-word gags / punchlines (20 `Ah.`, 66 `Nope.`, 68, 116 `Rude.`, 119 `Nobody.`) as in A2's 32, 33, 66, 68.")
L.append("4. **TTS-only respellings** (the saved script is never altered; each is one token for one token so words map back 1:1): " + ", ".join(f"{a} → {b}" for a, b in PL.RESPELL) + ". `Othenio Abel` is never spoken in V3 (beat 62 says \"Abel\"); William's approved plain-text handling is kept, with no respelling. Not respelled: Odysseus, Hesiod, Callimachus, Laertes, Ithaca, Poseidon, Euripides, Mycenae, Etna, Colavito, Buxton, Hackman, Mayor, Aeolian.")
L.append("5. Numbers are as written in the script (words, e.g. \"Twenty-two\", \"twelve fifty\"). `BC` was sent as `B.C.` (beats 83, 90, 91, 95, 104).\n")
L.append("### Attribution words added (spoken, not in the script)\n")
L.append("| beat | speaker | words added | time |\n|---|---|---|---|")
for b, e in sorted(bt.items()):
    if "attribution" in e: L.append(f'| {b} | {e["speaker"]} | {e["attribution"]["text"]} | {mmss(e["attribution"]["start"])} |')
L.append("\nTotal added words: %d.\n" % sum(1 for w in words if w["added"]))
L.append("## Per beat\n")
L.append("`script` = SCRIPT-V4.md wording; `sent` = the exact text in the TTS call (quotes, attribution and respellings included). Identical except where shown.\n")
for p in P:
    L.append(f'### {p["id"]} · {p["label"]} · beats {p["beats"][0]}-{p["beats"][-1]} · {p["chars"]} characters\n')
    for sg in p["segs"]:
        b = sg["beat"]; e = bt[b]
        same = sg["sent"] == sg["script"]
        L.append(f'- **{b:02d} · {sg["speaker"]}** ({mmss(e["start"])}-{mmss(e["end"])})')
        L.append(f'  - script: {sg["script"]}')
        if not same: L.append(f'  - sent: {sg["sent"]}')
    L.append("")
open(os.path.join(OUT, "SPOKEN-TEXT.md"), "w").write("\n".join(L))

# ---------------- LISTEN-FIRST.md
def find(pat, beat=None):
    out = []
    for w in words:
        if w["added"]: continue
        if re.search(pat, w["spoken"].strip('",.?!:;'), re.I) and (beat is None or w["beat"] == beat): out.append(w)
    return out
risky = [("Abel", "Abel"), ("Empedocles", "Em-peddokleez"), ("Thucydides", "Thoo-sididdeez"), ("Pausanias", "Paw-sayneeus"), ("Hesiod", "Hesiod"),
         ("Tiryns", "Tie-rinz"), ("Callimachus", "Callimachus"), ("Theocritus", "Thee-ockritus"), ("Polyphemus", "Pollifeemus"), ("Laertes", "Laertes"), ("Ithaca", "Ithaca"),
         ("Aguirre", "Ah-gheereh"), ("Buxton", "Buxton"), ("Colavito", "Colavito"), ("Burkert", "Boor-kert"), ("Euripides", "Euripides"), ("Mycenae", "Mycenae"),
         ("Etna", "Etna"), ("Aeolian", "Aeolian"), ("Poseidon", "Poseidon"), ("Hackman", "Hackman"), ("Mayor", "Mayor"), ("Odysseus", "Odysseus"), ("Cyclopes", "Cyclopes"),
         ("palaeontologist", "palaeontologist"), ("Hades", "Hades"), ("Alexander", "Alexander")]
R = []
R.append("# LISTEN-FIRST.md: risky pronunciations and the one-word gags (video 1 narration, `narration_voice_only.wav`)\n")
R.append("Timestamps are on the final timeline (m:ss.ss, start of the word). I cannot hear audio; the check below is a local whisper (small.en) transcription of each passage against the script, plus the alignment. Whisper is not a pronunciation judge: 'heard' shows what it transcribed.\n")
R.append("Not spoken in V4 (chips only, cut, or not in the script): Othenio Abel (beat 62 says only \"Abel\"), Brontes, Steropes, Arges, Telemus, Maron, Aguirre, Buxton, Burkert, Callimachus.\n")
R.append("## Names\n\n| name (sent as) | beat | time | whisper heard |\n|---|---|---|---|")
qa = json.load(open(os.path.join(OUT, "_work", "qa_whisper.json")))
heard = {}
for pid, r in qa.items():
    for d in r["diffs"]:
        for (wd, b, t) in d["want"]: heard[(pid, b, wd)] = d["heard"]
pass_of = {b: p["id"] for p in P for b in p["beats"]}
for name, sent in risky:
    ws = find(r"^" + re.escape(sent) + r"(s|'s)?$")
    for w in ws:
        h = heard.get((pass_of[w["beat"]], w["beat"], w["spoken"]), None)
        if h is None:
            h = heard.get((pass_of[w["beat"]], w["beat"], w["spoken"].strip('"')), None)
        R.append(f'| {name} ({w["spoken"].strip(chr(34))}) | {w["beat"]} | {mmss(w["start"])} | {h if h else "= script"} |')
R.append("\n## One-word and short gags\n\n| line | beat | speaker | time | gap before | whisper |\n|---|---|---|---|---|---|")
for b, txt in ((20, "Ah."), (31, "My name is Nobody."), (33, "I am honoured."), (66, "Nope."), (68, "Where's the nose?"), (85, "I keep sheep."), (86, "Sheep."), (111, "So I was not the first."), (116, "Rude."), (119, "Nobody.")):
    e = bt[b]; R.append(f'| {txt} | {b} | {e["speaker"]} | {mmss(e["start"])}-{mmss(e["end"])} | {e["gap_before"]} s | per QA: {"ok" if not any(d for d in sum([r["diffs"] for r in qa.values()], []) if any(w[1]==b for w in d["want"]) and b not in (33,)) else "see diffs"} |')
R.append("\n## Also worth a listen\n")
R.append("- The cold open (0:00-0:36): it sets the voice and the pace.")
R.append(f'- Verdict stamp lines with the 0.70 s beat before them: beats 80 ({mmss(bt[80]["start"])}), 96 ({mmss(bt[96]["start"])}), 105 ({mmss(bt[105]["start"])}), 113 ({mmss(bt[113]["start"])}).')
R.append(f'- Beat 50 "Son of Laertes. Of Ithaca." ({mmss(bt[50]["start"])}) and beat 54 the prayer ({mmss(bt[54]["start"])}): the only places the script asks for a performance change; with no tags the model decides.')
R.append(f'- The sailor exchange, beats 64-68 ({mmss(bt[64]["start"])}-{mmss(bt[68]["end"])}) and the Nobody exchange, beats 28-34 ({mmss(bt[28]["start"])}-{mmss(bt[34]["end"])}).')
open(os.path.join(OUT, "LISTEN-FIRST.md"), "w").write("\n".join(R) + "\n")
print("wrote docs")
