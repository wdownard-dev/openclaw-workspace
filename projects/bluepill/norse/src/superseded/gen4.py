#!/usr/bin/env python3
"""gen4.py: build norse/SCRIPT-N-draft4.md from SCRIPT-N-draft3.md (run from projects/bluepill/norse).
Draft 4 = draft 3 with hook C4, re-hook, voice-file fixes, three warmth/humour edits, CTA 3 without Egypt."""
import re, json

SRC = "SCRIPT-N-draft3.md"
OUT = "SCRIPT-N-draft4.md"

# ---- parse draft 3 beats ------------------------------------------------
beats = {}
order = []
cur = None
for line in open(SRC, encoding="utf-8"):
    line = line.rstrip("\n")
    m = re.match(r"\*\*(N-\d+)\*\*\s+(.+)$", line)
    if m:
        cur = m.group(1)
        beats[cur] = {"text": m.group(2), "shot": "", "state": "", "trace": ""}
        order.append(cur)
        continue
    m = re.match(r"- (shot|state|trace): (.*)$", line)
    if m and cur:
        beats[cur][m.group(1)] = m.group(2)

def B(text, shot, state, trace, tag=None):
    return {"text": text, "shot": shot, "state": state, "trace": trace, "tag": tag, "old": None}

GAP_SHOT = "wide, dawn: a bare empty gap, grey and pale blue, nothing in it"
GAP_STATE = "Ginnungagap, the empty gap; dawn; 0 present; static wide"

hook = [
    B("Look up.",
      "wide, dusk: a vast curved skull-shaped dome filling the sky over a dark sea, seen from below, no figures",
      "the new world; dusk; 0 present; slow tilt up",
      "(ours) direct address; the picture is Grimnismal 40 and Vafthruthnismol 21 (sky from the skull of the giant) V"),
    B("That is a skull.",
      "medium, dusk: the same dome closer, a pale bone curve with a heavy brow ridge, stars in its hollow",
      "the new world; dusk; 0 present; slow push-in",
      "Grimnismal 40 ('Of his skull the heavens high'), Vafthruthnismol 21 ('The sky from the frost-cold giant's skull') V"),
    B("The clouds are its brain,",
      "medium, dusk: grey clouds swirling inside the open hollow of the skull dome",
      "the new world; dusk; 0 present; clouds turn",
      "Grimnismal 41 ('And out of his brain the baleful clouds They made to move on high') V. NEW CLAIM H1"),
    B("the sea is its blood,",
      "medium, dusk: a dark blue sea with a red tinge washing against brown earth",
      "the new world; dusk; 0 present; slow pan",
      "Grimnismal 40 ('the ocean out of his blood') V"),
    B("the mountains its bones.",
      "medium, dusk: grey stone peaks standing against the dark sky",
      "the new world; dusk; 0 present; slow pan up",
      "Vafthruthnismol 21 ('the mountains were made of his bones') V; Grimnismal 40 says 'hills'. NEW CLAIM H2"),
    B("Norse myth says the world was a giant once,",
      "wide, dawn: the vast pale blue giant Ymir lying on his back in the empty pale gap, ice around his shoulders",
      "the empty gap; dawn; 1 present: Ymir's body; static wide",
      "Gylf 8 V (the earth made from Ymir's body); Grimnismal 40 V"),
    B("until three brothers took him apart.",
      "wide: the huge body lying in the gap, the brothers small on its chest looking down",
      "the empty gap; dawn; 4 present: Odin, Vili, Ve, Ymir's body; the brothers stand on the body",
      "Gylf 6-8 V (Odin, Vili and Ve kill Ymir, carry the body to the middle of the gap and make the world of it)"),
    B("One of them was Odin.",
      "close, dawn: Odin facing us, one eye, wide hat, pale light",
      "the empty gap; dawn; 1 present: Odin; he faces the camera, no movement",
      "Gylf 6 V (Odin, Vili and Ve)"),
    B("He was told how it all ends:",
      "medium, firelit hall: Odin alone, head tilted as if listening, eye half closed",
      "Odin's hall; night; 1 present: Odin alone; no movement",
      "Voluspa 1 (the seeress speaks to Valfather), 28-30 (Odin seeks her out: 'Widely I saw over all the worlds') V. NEW CLAIM H3"),
    B("in fire, with almost every god dead.",
      "wide, night: a plain burning to the horizon, Odin, Thor and Tyr lying fallen in the smoke, red sky",
      "burnt plain; night, red sky; 3 present: Odin, Thor, Tyr fallen; smoke drifts",
      "Gylf 51 V ('cast fire over the earth and burn all the world'; Odin, Thor, Tyr, Heimdall fall); Gylf 53 V (a few survive); Voluspa 52, 57 V. NEW CLAIM H4"),
    B("Before any of that, there was nothing.",
      GAP_SHOT, GAP_STATE,
      "Voluspa 3 V ('Earth had not been, nor heaven above, But a yawning gap'); Gylf 4 V. NEW CLAIM H5"),
    B("Not even a sky to hang a skull on.",
      "wide, dawn: the same empty gap, the camera tilting up to a blank grey sky",
      GAP_STATE,
      "Voluspa 3 V ('nor heaven above'); (ours) the joke is the callback to the opening picture. NEW CLAIM H5"),
]
for h in hook:
    h["old"] = "new (hook C4)"

new_seq = list(hook)

DELETE = {
    # draft 3 id: reason
    **{f"N-{i:03d}": "removed (draft 3 hook A)" for i in range(1, 10)},
    "N-010": "removed (hook now says there was nothing; 'Only a great gap' follows it)",
    "N-134": "removed (restated N-133 'until the end of the world'; VOICE 9.2)",
    "N-156": "removed ('But the story does not end there' is a staged run-up; VOICE 9.4)",
    "N-176": "removed (recap closer; VOICE 9.2)",
    "N-177": "removed (restating closer; VOICE 9.2)",
}

EDIT = {
    "N-071": ("The gods look at one another, and then at the grass.",
              "medium: Odin and Thor glancing sideways at each other, then down at the ground",
              None,
              "Gylf 34 V ('Each of the Aesir looked at his neighbor', Brodeur per FACTCHECK-N); 'and then at the grass' is (ours) dry framing"),
    "N-077": ("and the wolf stays chained.", None, None, "Gylf 34 V ('until the end of the world' moves to N-078)"),
    "N-105": ("His mother, Frigg, takes the dream seriously.", None, None,
              "Gylf 49 V ('the Aesir took counsel', then 'Frigg took oaths'); 'takes the dream seriously' is (ours) framing on that"),
    "N-106": ("She goes to everything in the world and asks for a promise.", None, None, "Gylf 49 V"),
    "N-130": ("His wife, Sigyn, sits beside him with a bowl to catch the drops.", None, None,
              "Voluspa 35 ('By his side does Sigyn sit'), Gylf 50 V (Sigyn sat by him with a basin)"),
    "N-145": (None, None, None,
              "Voluspa 28-30, 53 V; Gylf 51 V. (ours) callback to the hook's 'he was told how it all ends'; 'knows' is the inference of draft 3 claim A1/A5"),
    "N-031": (None, None, None,
              "Gylf 51 V ('burn all the world'); Gylf 4 V. Pull line, holds the N-030 plate; callback to the hook's 'in fire'"),
    "N-078": (None, None, None,
              "Gylf 51 V ('all fetters and bonds shall be broken'); (ours) now carries the 'will break' fact that N-077 used to state. Pull line, holds the N-077 plate"),
}
# N-078 must now also say what N-077 used to say? No: N-078 keeps 'will not hold forever'; 'end of the world' lives in the chapter's own pull.

ASIDES = {"N-015", "N-031", "N-078", "N-094"}  # aside beats whose shot/state hold the previous plate

REHOOK = B("Remember the skull? It is his.",
           "close: Ymir's huge pale blue head and white beard, ice melting off his brow",
           "the gap, where ice meets fire; dawn; 1 present: Ymir; static close",
           "Grimnismal 40, Vafthruthnismol 21 (the sky is the skull of the giant) V; Gylf 8 V. (ours) re-hook: restates why the giant matters and pulls forward",
           tag="REHOOK")
REHOOK["old"] = "new (re-hook)"

CTA1_TRACE = "(ours) CTA 1, soft; narrator aside, holds the re-hook plate (Ymir's head)"

for oid in order:
    if oid in DELETE:
        continue
    b = dict(beats[oid])
    b["old"] = oid
    tag = None
    m = re.match(r"^(.*?)\s*\[(CTA|PULL|CLOSE)\]\s*$", b["text"])
    if m:
        b["text"], tag = m.group(1), m.group(2)
    b["tag"] = tag
    if oid in EDIT:
        t, sh, st, tr = EDIT[oid]
        if t: b["text"] = t
        if sh: b["shot"] = sh
        if st: b["state"] = st
        if tr: b["trace"] = tr
    new_seq.append(b)
    if oid == "N-014":
        new_seq.append(REHOOK)

# fix the aside beats' shot/state so they hold the immediately preceding plate
for i, b in enumerate(new_seq):
    if b["tag"] == "CTA" and b["old"] == "N-015":
        prev = new_seq[i - 1]
        b["shot"], b["state"] = prev["shot"], prev["state"]
        b["trace"] = CTA1_TRACE
    if b["old"] == "N-094":
        pass
    if b["old"] == "N-178":
        b["text"] = "If this was your kind of story, come back for the next myth."
        prev = new_seq[i - 1]
        b["shot"], b["state"] = prev["shot"], prev["state"]
        b["trace"] = "(ours) CTA 3, closing; narrator aside, holds the N-175-draft-3 plate (Snorri and the spearman's shadow); points at the next myth without naming it"
        b["tag"] = "CTA"

# renumber
for i, b in enumerate(new_seq, 1):
    b["id"] = f"N-{i:03d}"

# trace "holds N-xxx" strings: rewrite aside traces with new ids
newid = {b["old"]: b["id"] for b in new_seq if b["old"] and b["old"].startswith("N-")}
def holds(prev_old):
    return newid.get(prev_old, "?")
for b in new_seq:
    if b["old"] == "N-031":
        b["trace"] = b["trace"].replace("N-030", holds("N-030"))
    if b["old"] == "N-078":
        b["trace"] = b["trace"].replace("N-077", holds("N-077"))
    if b["old"] == "N-094":
        b["trace"] = "(ours) CTA 2, mid-video; narrator aside, holds the %s plate" % holds("N-093")
    if b["old"] == "N-178":
        b["trace"] = b["trace"].replace("N-175-draft-3", holds("N-175"))

# chapter headers from draft 3 (title text); first beat of each chapter by draft 3 id
chapters = [
    ("COLD OPEN", None),
    ("A GIANT BECAME THE WORLD", "N-011"),
    ("THE TREE THAT HELD NINE WORLDS", "N-032"),
    ("THE WOLF EVERYONE AGREED TO CHAIN", "N-048"),
    ("THE DAY THOR WENT FISHING FOR A SERPENT", "N-079"),
    ("THE GOD NOTHING COULD HURT", "N-102"),
    ("EVERYONE DIES, THEN THE WORLD BEGINS AGAIN", "N-135"),
    ("THE CHRISTIAN WHO SAVED THE GODS", "N-164"),
]
start_idx = {0: 0}
for title, first in chapters[1:]:
    for i, b in enumerate(new_seq):
        if b["old"] == first:
            start_idx[chapters.index((title, first))] = i
            break

def wc(b):
    return len(b["text"].split())

# chapter spans
idxs = sorted(start_idx.items())
spans = []
for k, (ci, si) in enumerate(idxs):
    ei = idxs[k + 1][1] if k + 1 < len(idxs) else len(new_seq)
    words = sum(wc(b) for b in new_seq[si:ei])
    spans.append((ci, si, ei, words))

total_words = sum(wc(b) for b in new_seq)
sentences = sum(len(re.findall(r"[.!?]+(?=\s|$)", b["text"])) or 0 for b in new_seq)
# a beat that ends with ',' or has no terminal punctuation continues; count sentences by terminal punctuation overall
full = " ".join(b["text"] for b in new_seq)
sent = len(re.findall(r"[.!?:]+(?=\s|$)", full))
sent_clean = len([s for s in re.split(r"(?<=[.!?])\s+", full) if s.strip()])
questions = full.count("?")

def mmss(w):
    s = round(w / 150 * 60)
    return f"{s // 60}:{s % 60:02d}"

cum = 0
chap_start = {}
for ci, si, ei, words in spans:
    chap_start[ci] = cum
    cum += words
beat_time = {}
cum = 0
for b in new_seq:
    beat_time[b["id"]] = cum
    cum += wc(b)

cta_ids = [b["id"] for b in new_seq if b["tag"] == "CTA"]
pull_ids = [b["id"] for b in new_seq if b["tag"] == "PULL"]
close_ids = [b["id"] for b in new_seq if b["tag"] == "CLOSE"]
rehook_id = [b["id"] for b in new_seq if b["tag"] == "REHOOK"][0]

hook_words = sum(wc(b) for b in new_seq[:12])
raw = mmss(total_words)

out = []
out.append('# SCRIPT-N-draft4.md: "The ENTIRE Story of Norse Mythology, Creation to Ragnarok in 10 Minutes" (The Myth Ledger, video 2)\n')
out.append("Draft 4, 2026-11-14: draft 3 with hook C4 (\"The sky is a skull\", William's pick) in place of hook A, a re-hook beat after Ymir, no Egypt mention in the voice-over, and a pass against `VOICE.md` (structural tells, warmth and humour). Everything else is draft 3, word for word. Format as draft 3: beat id, spoken text, `shot:`, `state:`, `trace:`. Beat ids are renumbered; the old-to-new table is at the bottom. Nothing recorded, generated, uploaded or sent; `library/` untouched. Every change and the new claims are in `norse/DRAFT4-CHANGES.md`.\n")
out.append("## Header")
out.append(f"- **Spoken words: {total_words}** in {sent_clean} sentences (mean {total_words/sent_clean:.1f}); {questions} questions. At 150 wpm: **{raw}** raw voice time (target at most 1,650 words: met). {len(new_seq)} beats, 7 named chapters plus the cold open. No text cards, no on-screen text, no chapter bands (PROCESS rule 8).")
out.append("- Beat = one spoken fragment; a beat that starts lower-case continues the previous one. `shot:` is the single painted image for the beat. `state:` carries forward and changes only when the narration changes it; only the figures named in `state:` appear in the shot. `trace:` gives the source (Voluspa and the other Poetic Edda poems = Bellows 1923; Gylf = Gylfaginning, Prose Edda = Brodeur 1916; Gylf N = Brodeur chapter N in Roman numerals) with V (read in a text) or E (inference). `(ours)` = sentence with no source, or a pure framing/glue line; the basis is stated after it.")
out.append(f"- **Aside beats (CTA and PULL) have no new shot.** Their `shot:` and `state:` repeat the previous beat's plate exactly and the `trace:` says `holds N-xxx`; the scene planner should merge each with the plate it holds. The re-hook ({rehook_id}) is a normal beat with its own shot (Ymir's head).")
out.append("- No Edda quote appears anywhere in the narration. There is no voiced dialogue. Egypt is not mentioned anywhere in the voice-over.")
out.append(f"- Hook (hook C4, N-001 to N-012, {hook_words} words, about {round(hook_words/150*60)} s): the sky is a skull (clouds its brain, sea its blood, mountains its bones); the world was a giant once and three brothers took him apart; one of them, Odin, was told how it all ends, in fire with almost every god dead; before any of it there was nothing, not even a sky to hang a skull on. The bridge into chapter 1 is the last hook beat, then 'Only a great gap'. Master promise: how a world made like that ends. Paid at the Ragnarok chapter ({beat_time[[b['id'] for b in new_seq if b['old']=='N-135'][0]]/150:.0f}-ish min in) and at the CLOSE beat.")
ctas = "; ".join(f"{i} at about {mmss(beat_time[i])}" for i in cta_ids)
out.append(f"- Re-hook: {rehook_id} 'Remember the skull? It is his.' at about {mmss(beat_time[rehook_id])}. Calls to action (spoken by Daniel, no on-screen text, asides over the previous plate): {ctas}.\n")
plan = "; ".join(f"{('COLD OPEN' if ci == 0 else chapters[ci][0].title())} {mmss(chap_start[ci])}" for ci, si, ei, w in spans)
out.append("Chapter plan: " + plan + "\n")

def chap_header(ci, words):
    if ci == 0:
        return f"## COLD OPEN  (0:00, {words} words)\n"
    return f"## CHAPTER: {chapters[ci][0]}  ({mmss(chap_start[ci])}, {words} words)\n"

span_by_start = {si: (ci, w) for ci, si, ei, w in spans}
for i, b in enumerate(new_seq):
    if i in span_by_start:
        ci, w = span_by_start[i]
        out.append(chap_header(ci, w))
    tag = f" [{b['tag']}]" if b["tag"] in ("CTA", "PULL", "CLOSE") else ""
    out.append(f"**{b['id']}** {b['text']}{tag}")
    out.append(f"- shot: {b['shot']}")
    out.append(f"- state: {b['state']}")
    out.append(f"- trace: {b['trace']}\n")

# old-to-new table
out.append("## Old-to-new beat id map (draft 3 to draft 4)\n")
rows = []
for oid in order:
    if oid in DELETE:
        rows.append((oid, DELETE[oid]))
    else:
        rows.append((oid, newid[oid]))
out.append("| Draft 3 | Draft 4 | | Draft 3 | Draft 4 |")
out.append("|---|---|---|---|---|")
half = (len(rows) + 1) // 2
for i in range(half):
    a = rows[i]
    c = rows[i + half] if i + half < len(rows) else ("", "")
    out.append(f"| {a[0]} | {a[1]} | | {c[0]} | {c[1]} |")
newonly = [b["id"] for b in new_seq if (b["old"] or "").startswith("new")]
out.append("")
out.append("New beats with no draft 3 id: " + ", ".join(newonly) + " (hook C4 N-001 to N-012; re-hook %s)." % rehook_id)

open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")

json.dump({"words": total_words, "sentences": sent_clean, "questions": questions, "beats": len(new_seq),
           "raw": raw, "hook_words": hook_words, "cta": {i: mmss(beat_time[i]) for i in cta_ids},
           "pull": {i: mmss(beat_time[i]) for i in pull_ids}, "rehook": mmss(beat_time[rehook_id]),
           "chapters": {chapters[ci][0]: (mmss(chap_start[ci]), w) for ci, si, ei, w in spans},
           "map": {k: v for k, v in rows}}, open("src/gen4_stats.json", "w"), indent=1)
print(total_words, sent_clean, questions, len(new_seq), raw)
