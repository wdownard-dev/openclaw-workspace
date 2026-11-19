"""Norse plan: parse SCRIPT-N-LOCKED.md beats -> 8 passages -> audio-n/plan.json + SPOKEN-TEXT.md. Run: clips-venv/bin/python -I plan.py"""
import os, re, json, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
SCRIPT = os.path.join(os.path.dirname(OUT), "SCRIPT-N-LOCKED.md")
import json as _j
RESPELL = [tuple(x) for x in _j.load(open(os.path.join(HERE, "respell.json")))]
CH = [("P1", "Cold open", 1, 10), ("P2", "A Giant Became The World", 11, 32), ("P3", "The Tree That Held Nine Worlds", 33, 48),
      ("P4", "The Wolf Everyone Agreed To Chain", 49, 79), ("P5", "The Day Thor Went Fishing For A Serpent", 80, 102),
      ("P6", "The God Nothing Could Hurt", 103, 134), ("P7", "Everyone Dies, Then The World Begins Again", 135, 161),
      ("P8", "The Christian Who Saved The Gods", 162, 178)]
def tts(t):
    for a, b in RESPELL: t = t.replace(a, b)
    return t
B = {(int(m.group(1)) if not m.group(2) else int(m.group(1))+0.5): re.sub(r"\s*\[(CTA|PULL|CLOSE)\]\s*$", "", m.group(3).strip()) for m in re.finditer(r"^\*\*N-(\d+)(a?)\*\* (.+)$", open(SCRIPT).read(), re.M)}
passages = []
for pid, label, a, b in CH:
    ids = [i for i in sorted(B) if a <= i <= b]; text = ""; segs = []
    for k, i in enumerate(ids):
        t = tts(B[i])
        if k:
            cont = B[i][0].islower() or B[i][0] == '"' and False
            text += " " if (B[i][0].islower() or not re.search(r'[.?!]"?$', B[ids[k-1]])) else "\n\n"
        s = len(text); text += t; segs.append(dict(beat=i, start=s, end=len(text), script=B[i]))
    passages.append(dict(id=pid, label=label, beats=ids, text=text, segs=segs, chars=len(text)))
for k, p in enumerate(passages):
    p["prev"] = passages[k-1]["text"][-400:] if k else ""; p["next"] = passages[k+1]["text"][:400] if k < len(passages)-1 else ""
json.dump(dict(passages=passages), open(os.path.join(OUT, "plan.json"), "w"), indent=1)
md = ["# SPOKEN-TEXT (Norse, video 2)\n", "Exactly what was sent to ElevenLabs (Daniel, eleven_multilingual_v2, stability 0.5, style 0.2, speed 1.0, similarity 0.75, boost on, no tags). TTS-only respellings: " + ", ".join(f"{a}->{b}" for a, b in RESPELL) + ". Blank line = sentence break between beats; single space = continuation.\n"]
for p in passages: md.append(f"## {p['id']} {p['label']} (beats {p['beats'][0]}-{p['beats'][-1]}, {p['chars']} chars)\n\n{p['text']}\n")
open(os.path.join(OUT, "SPOKEN-TEXT.md"), "w").write("\n".join(md))
print([(p["id"], p["chars"]) for p in passages], "total", sum(p["chars"] for p in passages), "beats", len(B))
