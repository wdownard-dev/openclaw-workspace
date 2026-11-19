"""Alignment -> words with beat/speaker/passage tags. words_of(pid) returns list of dict(word, start, end, beat, speaker, passage, added, quote_open_close).
Character alignment is mapped to the plan's char spans: script words = the beat's own text; attribution words (A2 technique) are flagged added=True and tagged speaker NARR."""
import os, sys, json, re
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)

def plan(): return json.load(open(os.path.join(OUT, "plan.json")))
def align(pid): return json.load(open(os.path.join(OUT, "passages", pid + ".json")))["alignment"]

def words_of(p, al=None):
    al = al or align(p["id"]); ch = al["characters"]; ts = al["character_start_times_seconds"]; te = al["character_end_times_seconds"]
    text = p["text"]; out = []
    for sg in p["segs"]:
        seg = text[sg["start"]:sg["end"]]; base = sg["start"]
        # attribution tail = text after the closing quote of a character line
        cut = len(seg)
        if sg["speaker"] != "NARR":
            q = seg.rfind('"'); cut = q + 1
        for m in re.finditer(r"\S+", seg):
            s, e = base + m.start(), base + m.end()
            idx = [i for i in range(s, e) if ch[i].isalnum()]
            if not idx: continue          # pure punctuation token
            added = sg["speaker"] != "NARR" and m.start() >= cut
            out.append(dict(word=m.group(), start=ts[idx[0]], end=te[idx[-1]], beat=sg["beat"], speaker=("NARR" if added else sg["speaker"]),
                            passage=p["id"], added=added))
    return out
