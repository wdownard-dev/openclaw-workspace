#!/usr/bin/env python3
"""voicecheck: flag VOICE.md ban-list words and structural AI tells in the SPOKEN lines of a beat script.
usage: python3 -I scripts/voicecheck.py projects/bluepill/norse/SCRIPT-N-draft2.md
Spoken line = text after **ID** at the start of a beat line. Flags are prompts for a human or worker decision, not auto-fixes."""
import re, sys, collections

WORDS = r"delve|testament|tapestry|beacon|unlock(?:ed|s)?|realm|pivotal|crucial|enduring|landscape|intricate|meticulous(?:ly)?|vibrant|showcas\w+|underscor\w+|epic|insane|legendary|mind-blowing|shocking"
PHRASES = [
 ("meta-opener", r"in today's|here's the thing|the thing is|let us start|let's start|let's dive|let's explore|first, the story|in this video|welcome to|without further ado|buckle up|little did (?:he|she|they) know"),
 ("not-X-but-Y", r"\bnot (?:just|only|merely)\b|\bit(?:'s| is) not [^,.;]{1,40}[,;] it(?:'s| is)\b|\bisn't (?:just|about)\b|\bnot [a-z ]{1,25}, but\b"),
 ("deep-saying", r"the real question|at its core|what really matters|the heart of the matter|fundamentally|the deeper (?:issue|truth)|in reality"),
 ("inflated-significance", r"marking (?:a|the)|set(?:ting)? the stage|lasting legacy|enduring legacy|indelible|stood as|stands as|plays? a (?:key|crucial|pivotal) role|the stakes (?:could not|couldn't) be higher|changed everything"),
 ("shallow-ing", r",\s+(?:showing|highlighting|underscoring|reflecting|symbolizing|revealing|demonstrating)\b"),
 ("moral-platitude", r"the lesson is|teaches us|reminds us that|goes to show|sometimes,? the (?:best|smartest)"),
 ("dash", r"[—–]| -- "),
]
def beats(path):
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        m = re.match(r"\*\*([A-Za-z0-9-]+)\*\*\s+(.+)$", line.rstrip())
        if m: yield ln, m.group(1), m.group(2)
def main(path):
    rows = list(beats(path)); hits = collections.defaultdict(list)
    for ln, bid, txt in rows:
        low = txt.lower()
        for m in re.finditer(WORDS, low): hits["ban-word"].append((bid, txt, m.group(0)))
        for name, pat in PHRASES:
            m = re.search(pat, low)
            if m: hits[name].append((bid, txt, m.group(0)))
    # structural: runs of 3+ consecutive beats of 4 words or fewer (fragment rows); triads "a, b, and c" of equal-length words
    run = []
    for ln, bid, txt in rows:
        if len(txt.split()) <= 4: run.append((bid, txt))
        else:
            if len(run) >= 3: hits["fragment-row"].append((run[0][0], " / ".join(t for _, t in run), f"{len(run)} short beats"))
            run = []
    for ln, bid, txt in rows:
        if re.search(r"\b\w+, \w+,? and \w+\b", txt) and len(txt.split()) <= 9:
            hits["short-triad"].append((bid, txt, "triad"))
    words = sum(len(t.split()) for _, _, t in rows)
    print(f"{path}: {len(rows)} beats, {words} spoken words, {sum(len(v) for v in hits.values())} flags")
    for k in sorted(hits):
        print(f"\n## {k} ({len(hits[k])})")
        for bid, txt, why in hits[k]: print(f"- {bid} [{why}] {txt}")
if __name__ == "__main__": main(sys.argv[1])
