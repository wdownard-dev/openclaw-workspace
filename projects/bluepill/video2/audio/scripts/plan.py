"""Spoken-text plan for SCRIPT-V4 (video 1; V3 with the approved cuts), method A2 (Daniel, eleven_multilingual_v2, no tags, quotes + short attribution, continuous passages).
Builds audio/plan.json: passages -> segments (char spans of each beat's script text inside the text sent to TTS) and SPOKEN-TEXT.md.
Run: /home/williamdownard/openclaw-sites/clips-venv/bin/python -I plan.py [show]"""
import os, sys, re, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import *

B = parse_script()          # beat -> (speaker, text); TEXT-CHIP beats are not matched by the regex (their speaker is TEXT-CHIP, '-' not \w)
CHIPS = {59: "SUSPECT 1: THE DWARF ELEPHANT", 81: "SUSPECT 2: THE SMITHS", 97: "SUSPECT 3: THE WALLS", 106: "SUSPECT 4: THE FOLKTALE"}

# TTS-only respellings (video1/voice.py RESPELL, applied only to what is sent). Othenio Abel: plain (not spoken in V3 anyway: beat 62 says "Abel" only).
RESPELL = [("Polyphemus", "Pollifeemus"), ("Empedocles", "Em-peddokleez"), ("Theocritus", "Thee-ockritus"), ("Thucydides", "Thoo-sididdeez"),
           ("Tiryns", "Tie-rinz"), ("Pausanias", "Paw-sayneeus"), ("Brontes", "Bron-teez"), ("Steropes", "Stair-oh-peez"), ("Arges", "Ar-geez"),
           ("Aci", "Ah-chee"), ("Trezza", "Tret-sah"), ("Aguirre", "Ah-gheereh"), ("Burkert", "Boor-kert"),
           ("BC", "B.C.")]   # BC -> B.C.: FORMAT per SCRIPT-V3 (b) "twelve fifty B.C." / "seven hundred B.C."
def tts(t):
    for a, b in RESPELL: t = re.sub(r"\b" + a + r"\b", b, t)
    return t.replace("B.C..", "B.C.")   # "BC." at a sentence end must not become "B.C.." (it produced a 0.92 s pause in the V3 take, beat 104)

# A2 attribution (method A2 of round 3: character lines in double quotes, short attribution after on some lines; no bracket tags).
# Beats listed here are EXACTLY as in round-3 A2 (scene_texts.ATTR); the rest follow the same pattern for the same reason (a speaker change right after narration).
ATTR = {
    # --- as rendered in round-3 A2 ---
    28: "said Odysseus, quite calmly", 30: "the giant rumbled", 31: "said Odysseus", 37: "a Cyclops asked, bored", 38: "the giant bellowed",
    39: "the Cyclops said flatly", 64: "the sailor asked",
    # --- same technique, new lines (first line of an exchange / a new speaker straight after narration) ---
    9: "the crew urged", 10: "said Odysseus", 14: "the giant asked", 18: "Odysseus thought", 23: "said Odysseus", 24: "a crewman asked",
    44: "the giant said softly", 49: "the crew begged", 52: "the giant called", 54: "the giant prayed", 75: "the sailor asked",
    85: "the giant said awkwardly", 100: "a crewman asked", 111: "Odysseus muttered",
}
# bare quotes (no attribution), as in A2's 32, 33, 66, 68: replies inside an exchange and the one-word gags
BARE = [15, 16, 19, 20, 25, 32, 33, 50, 53, 66, 68, 86, 116, 119]

def line_text(b):
    """text sent for one beat (before TTS respelling): narrator lines verbatim; character lines in quotes, with attribution on those in ATTR"""
    s, t = B[b]
    if s == "NARR": return t
    a = ATTR.get(b)
    if not a: return '"%s"' % t
    end = t[-1]
    body = t[:-1] + ("," if end == "." else end)
    return ('"%s" %s.' % (body, a)).replace("?,", "?").replace("!,", "!")

PASSAGES = [   # id, label, beats (chip beats are markers, not in the list)
    ("P01", "cold open", [1, 2, 3, 4, 5]),
    ("P02", "act 1: arrival", [6, 7, 8, 9, 10, 11, 12, 13]),
    ("P03", "act 1: the owner", [14, 15, 16, 17, 18, 19, 20, 21]),
    ("P04", "act 1: the stake, the wine, Nobody", [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]),
    ("P05", "act 1: the eye", [35, 36, 37, 38, 39, 40]),
    ("P06", "act 1: the sheep", [41, 42, 43, 44, 45, 46, 47, 48]),
    ("P07", "act 1: departure", [49, 50, 51, 52, 53, 54]),
    ("P08", "act 1 close and the turn", [55, 56, 57, 58]),
    ("P09", "suspect 1 a: the dwarf elephant", [60, 61, 62, 63, 64, 65, 66, 67]),
    ("P10", "suspect 1 b: nasal cavity, Mayor", [68, 69, 70, 71, 72, 73]),
    ("P11", "suspect 1 c: Empedocles", [74, 75, 76, 80]),                 # V4: 77, 78, 79 cut
    ("P12", "suspect 2 a: the smiths", [82, 83, 84, 85, 86, 87, 88]),      # V4: 89 cut
    ("P13", "suspect 2 b: addresses", [90, 92, 93, 94, 95, 96]),           # V4: 91 cut
    ("P14", "suspect 3: the walls", [98, 99, 100, 101, 102, 103, 104, 105]),
    ("P15", "suspect 4: the folktale", [107, 108, 109, 110, 111, 112, 113]),
    ("P16", "verdict and tease", [114, 115, 116, 117, 118, 119, 120, 121]),
]
SEP = "\n\n"   # as A2

def build():
    out = []
    for pid, label, beats in PASSAGES:
        text = ""; segs = []
        for b in beats:
            if text: text += SEP
            s, t = B[b]; lt = line_text(b); sent = tts(lt)
            start = len(text); text += sent
            # script words are the quoted/narrated text; attribution words (if any) are the tail after the closing quote
            attr = tts(ATTR[b]) if b in ATTR else None
            segs.append(dict(beat=b, speaker=s, script=t, line_orig=lt, sent=sent, attr=ATTR.get(b), start=start, end=len(text)))
        out.append(dict(id=pid, label=label, beats=beats, text=text, chars=len(text), segs=segs))
    return out

if __name__ == "__main__":
    P = build()
    for i, p in enumerate(P):
        p["prev"] = P[i - 1]["text"][-300:] if i else ""
        p["next"] = P[i + 1]["text"][:300] if i + 1 < len(P) else ""
    json.dump(dict(passages=P, chips=CHIPS), open(os.path.join(OUT, "plan.json"), "w"), indent=1)
    tot = 0; words = 0
    for p in P:
        w = sum(len(B[b][1].split()) for b in p["beats"]); words += w; tot += p["chars"]
        print(p["id"], p["label"], "beats", p["beats"][0], "-", p["beats"][-1], "chars", p["chars"], "script words", w)
    print("total chars", tot, "script words", words, "spoken beats", sum(len(p["beats"]) for p in P))
    if len(sys.argv) > 1:
        for p in P[:2]: print(p["text"]); print()
