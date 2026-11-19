#!/usr/bin/env python3
"""gen5.py: build norse/SCRIPT-N-draft4.md from SCRIPT-N-draft3.md (run from projects/bluepill/norse).
Draft 4 = draft 3 with William's exact hook C ("The sky is a skull"), a re-hook, voice-file fixes,
three warmth/humour edits, CTA 3 without Egypt, and explicit variant cards in every state line.
Replaces the earlier gen4.py output (that run used a hook that was not word for word)."""
import re, json

SRC = "SCRIPT-N-draft3.md"
OUT = "SCRIPT-N-draft4.md"

beats, order, cur = {}, [], None
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
    if line.startswith("## Old-to-new"):
        break

def B(text, shot, state, trace, tag=None, old="new (hook C)"):
    return {"text": text, "shot": shot, "state": state, "trace": trace, "tag": tag, "old": old}

GAP_SHOT = "wide, dawn: a bare empty gap, grey and pale blue, nothing in it"
GAP_STATE = "Ginnungagap, the empty gap; dawn; 0 present; static wide"
DOME_STATE = "the new world; dusk; 0 present; {mv}"

hook = [
    B("The sky is a skull.",
      "wide, dusk: a vast curved skull-shaped dome filling the sky over a dark sea, seen from below, no figures",
      DOME_STATE.format(mv="slow push-in"),
      "Grimnismal 40 ('Of his skull the heavens high') V; Vafthruthnismol 21 ('The sky from the frost-cold giant's skull') V"),
    B("The clouds are its brain.",
      "medium, dusk: grey clouds swirling inside the open hollow of the skull dome",
      DOME_STATE.format(mv="clouds turn"),
      "Grimnismal 41 ('And out of his brain the baleful clouds They made to move on high') V. NEW CLAIM H1"),
    B("The sea is blood,",
      "medium, dusk: a dark blue sea with a red tinge washing against brown earth",
      DOME_STATE.format(mv="slow pan"),
      "Grimnismal 40 ('the ocean out of his blood') V; Vafthruthnismol 21 V"),
    B("and the mountains are bones.",
      "medium, dusk: grey stone peaks standing against the dark sky, pale and ridged like bone",
      DOME_STATE.format(mv="slow pan up"),
      "Vafthruthnismol 21 ('the mountains were made of his bones') V; Grimnismal 40 says 'the hills' V. NEW CLAIM H2"),
    B("In Norse myth, the world was a giant once,",
      "wide, dawn: green hills, brown earth and a blue sea laid out as one vast pale giant lying on his back, hill-shoulders, ridge-knees",
      "Ymir's body, now land; dawn; 1 present: Ymir's body; static wide",
      "Voluspa 3 ('Of old was the age when Ymir lived') V; Gylf 8 (the earth made from Ymir's body) V; Grimnismal 40 V"),
    B("until three brothers took him apart.",
      "wide: three small brothers hauling the enormous pale blue body across the pale gap on ropes",
      "the empty gap; dawn; 4 present: Odin, Vili, Ve, Ymir's body; brothers drag the body",
      "Gylf 6-8 V (Odin, Vili and Ve kill Ymir, carry the body to the middle of the gap and make the world of it)"),
    B("One of them was Odin.",
      "close, dawn: Odin facing us, one eye, wide hat, pale light",
      "the empty gap; dawn; 1 present: Odin; he faces the camera, no movement",
      "Gylf 6 V (Odin, Vili and Ve)"),
    B("He built everything from a corpse,",
      "wide: the huge body lying in the gap, the three brothers small on its chest looking down",
      "the empty gap; dawn; 4 present: Odin, Vili, Ve, Ymir's body; the brothers stand on the body",
      "Gylf 8 V; Grimnismal 40-41 V (earth, sea, hills, trees, sky, clouds, and Mithgarth from the eyebrows). 'Everything' = the whole physical world; see DRAFT4-CHANGES NEW CLAIMS H4. NEW CLAIM H4"),
    B("and then he was told how it would end.",
      "medium, firelit hall: Odin alone, head tilted as if listening, eye half closed",
      "Odin's hall; night; 1 present: Odin alone; no movement",
      "Voluspa 1 (the seeress speaks to Valfather), 28-30 (the seeress and Othin; 'Widely I saw over all the worlds'), 31-66 (her prophecy, incl. 53 Othin fares to fight the wolf) V; Bellows note on 28 ('the fate in store for you'). NEW CLAIM H3"),
    B("But first, there was nothing at all.",
      GAP_SHOT, GAP_STATE,
      "Voluspa 3 ('Earth had not been, nor heaven above, But a yawning gap') V; Gylf 4 V. NEW CLAIM H5 (hyperbole: Ymir, ice and the gap exist; corrected by the next beat)"),
]

DELETE = {
    **{f"N-{i:03d}": "removed (draft 3 hook A)" for i in range(1, 9)},
    "N-009": "removed ('Let us start at the beginning' is a banned meta line; VOICE 2, 9)",
    "N-010": "removed (restated the hook's 'nothing at all'; VOICE 9.2)",
    "N-133": "removed (restated the chapter's 'until the end of the world' that the pull line N-134 now carries; VOICE 9.2)",
    "N-156": "removed ('But the story does not end there' is a staged run-up and a meta line; VOICE 9.4, 2)",
    "N-163": "removed ('They begin again' restated the chapter title and the beats before it; VOICE 9.2, 9.7)",
    "N-176": "removed (recap triad that restates the chapter; VOICE 9.2, 9.7)",
    "N-177": "removed (moral-as-platitude closer; VOICE 9, 9.2)",
}

EDIT = {
    "N-011": ("Well, almost nothing. Only a great gap, with ice on one side", None, None,
              "Gylf 4 V ('Ginnunga-gap'; Niflheim and Muspellsheim either side). 'Well, almost nothing' is (ours): a dry correction of the hook's 'nothing at all', accurate to Voluspa 3 (a gap, and Ymir). It is also the first story beat after the bridge, so the viewer gets a question ('what is in the gap?') and no meta line"),
    "N-049": ("He is handsome and charming, and impossible to trust.", None, None,
              "Gylf 33 V (Loki 'fair and comely', 'evil in disposition', 'very capricious'); VOICE 9.6: breaks the forced triad that voicecheck flagged"),
    "N-071": ("The gods look at one another, and then at the grass.", None, None,
              "Gylf 34 V (each of the Aesir refuses until Tyr; Brodeur); 'and then at the grass' is (ours) dry framing of that refusal. HUMOUR EDIT 1"),
    "N-077": ("and the wolf stays chained.", None, None,
              "Gylf 34 V ('until the end of the world' now lives in the pull line N-078 instead of being said twice)"),
    "N-105": ("His mother, Frigg, will not take the chance.", None, None,
              "Gylf 49 V (the Aesir took counsel; Frigg took oaths); 'will not take the chance' is (ours) framing of that. WARMTH EDIT 2"),
    "N-106": ("She goes to everything in the world and asks for a promise.", None, None, "Gylf 49 V"),
    "N-130": ("His wife, Sigyn, sits by his side with a bowl to catch the drops.", None, None,
              "Voluspa 35 ('By his side does Sigyn sit') V; Gylf 50 V (Sigyn holds a basin under the drops). WARMTH EDIT 3"),
    "N-145": (None, None, None,
              "Voluspa 28-30, 53 V; Gylf 51 V. (ours) pays the master promise of the hook ('he was told how it would end'); 'knows' is the inference of draft 3 claims A1/A5"),
}

# shot edits that make the variant visible
SHOT_EXTRA = {
    "N-077": "wide, dusk: the wolf bound on a flat rock, a sword propped in his jaws, the gods small beside him, Tyr's right arm ending in a stump",
    "N-144": "wide, night: three tiny armored figures marching across a dark plain, red sky, the left one with an empty right sleeve",
    "N-151": "medium: Tyr, his right arm ending in a stump, and a black hound locked together, both falling",
}

REHOOK = B("The skull in the sky is still on his shoulders, for now.",
           "close: Ymir's huge pale blue head and white beard, ice melting off his brow",
           "the gap, where ice meets fire; dawn; 1 present: Ymir (scale 4.0); static close",
           "Grimnismal 40, Vafthruthnismol 21 (the sky is the giant's skull) V; Gylf 8 V. (ours) re-hook: ties the hook's picture to the giant now on screen and pulls forward ('for now'). No meta line",
           tag="REHOOK", old="new (re-hook)")

new_seq = list(hook)
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
    if oid in SHOT_EXTRA:
        b["shot"] = SHOT_EXTRA[oid]
    if oid == "N-011":
        b["shot"] = beats["N-011"]["shot"]
    new_seq.append(b)
    if oid == "N-014":
        new_seq.append(REHOOK)

# ---- variant cards in state lines
def onum(b):
    m = re.match(r"N-(\d+)", b["old"] or "")
    return int(m.group(1)) if m else None

def split_state(st):
    """split 'place; time; N present: names; action' into (head+present, action)"""
    parts = st.split("; ")
    if len(parts) >= 4:
        return "; ".join(parts[:3]), "; " + "; ".join(parts[3:])
    return st, ""

for b in new_seq:
    head, act = split_state(b["state"])
    n = onum(b)
    head = re.sub(r"\bOdin\b(?!'s)(?! gone)(?! \(one eye\))", "Odin (one eye)", head)
    if n is not None and re.search(r"\bTyr\b(?! \()", head):
        head = re.sub(r"\bTyr\b(?! \()", "Tyr (hand)" if n <= 76 else "Tyr (stump)", head)
    if n is not None and re.search(r"\bFenrir\b(?! \()", head):
        card = None
        if 61 <= n <= 73: card = "Fenrir (huge, 2.0)"
        elif 74 <= n <= 78: card = "Fenrir (bound)"
        elif 137 <= n <= 148: card = "Fenrir (huge)"
        if card:
            head = re.sub(r"\bFenrir\b(?! \()", card, head)
    head = head.replace("Loki, tied across three rocks", "Loki (bound)")
    b["state"] = head + act

# chain the new Tyr stump line into N-076's shot? no: the bite beat keeps the hand (jaws closing); stump starts the next beat.

# CTA 3 and aside beats hold the previous plate
for i, b in enumerate(new_seq):
    prev = new_seq[i - 1]
    if b["tag"] == "CTA" and b["old"] == "N-015":
        b["shot"], b["state"] = prev["shot"], prev["state"]
        b["trace"] = "(ours) CTA 1, soft; narrator aside, holds the re-hook plate (Ymir's head)"
    elif b["old"] == "N-031" or b["old"] == "N-078" or b["old"] == "N-094" or b["old"] == "N-134":
        b["shot"], b["state"] = prev["shot"], prev["state"]
    elif b["old"] == "N-178":
        b["text"] = "If this was your kind of story, come back for the next myth."
        b["shot"], b["state"] = prev["shot"], prev["state"]
        b["tag"] = "CTA"

for i, b in enumerate(new_seq, 1):
    b["id"] = f"N-{i:03d}"
newid = {b["old"]: b["id"] for b in new_seq if b["old"] and b["old"].startswith("N-")}
prevof = {}
for i, b in enumerate(new_seq):
    prevof[b["old"]] = new_seq[i - 1]["id"] if i else None
for b in new_seq:
    o = b["old"]
    if o == "N-031":
        b["trace"] = "Gylf 51 V ('burn all the world'); Gylf 4 V. Pull line, holds %s; callback to the hook's 'how it would end'" % prevof[o]
    elif o == "N-078":
        b["trace"] = "Gylf 51 V ('all fetters and bonds shall be broken'). Pull line, holds %s; carries the 'will break' fact that N-077 no longer repeats" % prevof[o]
    elif o == "N-094":
        b["trace"] = "(ours) CTA 2, story-tied, mid-video; narrator aside, holds the %s plate" % prevof[o]
    elif o == "N-134":
        b["trace"] = "Gylf 51 V (fetters broken; Loki and Heimdall fall together); Gylf 50 V ('until Ragnarok'). Pull line, holds %s" % prevof[o]
    elif o == "N-178":
        b["trace"] = "(ours) CTA 3, closing; narrator aside, holds the %s plate (Snorri and the spearman's shadow); points to the next myth without naming it" % prevof[o]

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
for ci, (title, first) in enumerate(chapters):
    if first:
        for i, b in enumerate(new_seq):
            if b["old"] == first:
                start_idx[ci] = i
                break

def wc(b): return len(b["text"].split())
idxs = sorted(start_idx.items(), key=lambda kv: kv[1])
spans = []
for k, (ci, si) in enumerate(idxs):
    ei = idxs[k + 1][1] if k + 1 < len(idxs) else len(new_seq)
    spans.append((ci, si, ei, sum(wc(b) for b in new_seq[si:ei])))

total_words = sum(wc(b) for b in new_seq)
full = " ".join(b["text"] for b in new_seq)
sent_clean = len([s for s in re.split(r"(?<=[.!?])\s+", full) if s.strip()])
questions = full.count("?")
def mmss(w):
    s = round(w / 150 * 60); return f"{s // 60}:{s % 60:02d}"
cum = 0; chap_start = {}
for ci, si, ei, words in spans:
    chap_start[ci] = cum; cum += words
beat_time = {}; cum = 0
for b in new_seq:
    beat_time[b["id"]] = cum; cum += wc(b)
cta_ids = [b["id"] for b in new_seq if b["tag"] == "CTA"]
pull_ids = [b["id"] for b in new_seq if b["tag"] == "PULL"]
rehook_id = [b["id"] for b in new_seq if b["tag"] == "REHOOK"][0]
close_id = [b["id"] for b in new_seq if b["tag"] == "CLOSE"][0]
hook_words = sum(wc(b) for b in new_seq[:len(hook)])
raw = mmss(total_words)

# ---- variants table (auto from state lines)
vlabels = ["Odin (one eye)", "Tyr (hand)", "Tyr (stump)", "Fenrir (cub)", "Fenrir (young)", "Fenrir (huge, 2.0)", "Fenrir (bound)", "Fenrir (huge)",
           "Jormungandr (small serpent)", "Hel (child)", "Hymir (scale 3.0)", "Ymir (scale 4.0)", "Surt (scale 4.0)", "Loki as an old woman", "Loki as a salmon", "Loki (bound)", "Baldr (dead)"]
vrows = []
for v in vlabels:
    ids = [b["id"] for b in new_seq if v in b["state"]]
    if ids:
        vrows.append((v, ids[0], ids[-1], len(ids)))
tyr_hand_last = [b["id"] for b in new_seq if "Tyr (hand)" in b["state"]][-1]
tyr_stump_first = [b["id"] for b in new_seq if "Tyr (stump)" in b["state"]][0]
bite_id = newid["N-076"]
odin_ids = [b["id"] for b in new_seq if re.search(r"\bOdin\b(?!'s)(?! gone)", b["state"])]
assert all("Odin (one eye)" in split_state(b["state"])[0] for b in new_seq if re.search(r"\bOdin\b(?!'s)(?! gone)", split_state(b["state"])[0]))
assert not any(re.search(r"\bTyr\b(?! \()", split_state(b["state"])[0]) for b in new_seq)
loki_old_names = ("Loki as an old woman", "Loki as a salmon")

out = []
out.append('# SCRIPT-N-draft4.md: "The ENTIRE Story of Norse Mythology, Creation to Ragnarok in 10 Minutes" (The Myth Ledger, video 2)\n')
out.append("Draft 4, 2026-11-14: draft 3 with William's hook C ('The sky is a skull', word for word) in place of hook A and the old bridge, a re-hook after Ymir, no Egypt in the voice-over, a pass against `VOICE.md` (structural tells, warmth and humour), and explicit variant cards in every `state:` line. Everything else is draft 3. Format as draft 3: beat id, spoken text, `shot:`, `state:`, `trace:`. Beat ids are renumbered; the old-to-new table is at the bottom. Nothing recorded, generated, uploaded or sent; `library/` untouched. Every change, the new claims and the voicecheck output are in `norse/DRAFT4-CHANGES.md`.\n")
out.append("## Header")
out.append(f"- **Spoken words: {total_words}** in {sent_clean} sentences (mean {total_words/sent_clean:.1f}); {questions} questions. At 150 wpm: **{raw}** raw voice time (target at most 1,650 words: {'met' if total_words <= 1650 else 'NOT met'}). {len(new_seq)} beats, 7 named chapters plus the cold open. No text cards, no on-screen text, no chapter bands (PROCESS rule 8).")
out.append("- Beat = one spoken fragment; a beat that starts lower-case continues the previous one. `shot:` is the single painted image for the beat. `state:` carries forward and changes only when the narration changes it; only the figures named in `state:` appear in the shot, and every variant character is named with its card, e.g. `Tyr (hand)`. `trace:` gives the source (Voluspa and the other Poetic Edda poems = Bellows 1923; Gylf = Gylfaginning, Prose Edda = Brodeur 1916; Gylf N = Brodeur chapter N in Roman numerals) with V (read in a text) or E (inference). `(ours)` = sentence with no source, or a pure framing/glue line; the basis is stated after it.")
out.append(f"- **Aside beats (CTA and PULL) have no new shot.** Their `shot:` and `state:` repeat the previous beat's plate exactly and the `trace:` says `holds N-xxx`; the scene planner should merge each with the plate it holds. The re-hook ({rehook_id}) is a normal beat with its own shot (Ymir's head).")
out.append("- No Edda quote appears anywhere in the narration. There is no voiced dialogue. Egypt is not mentioned anywhere in the voice-over.")
out.append(f"- Hook (hook C, N-001 to {hook and new_seq[len(hook)-1]['id']}, {hook_words} words, about {round(hook_words/150*60)} s, William's wording unchanged): the sky is a skull, the clouds its brain, the sea its blood, the mountains its bones; the world was a giant once and three brothers took him apart; Odin built everything from the corpse and was told how it would end; 'But first, there was nothing at all' is the bridge. {new_seq[len(hook)]['id']} ('Well, almost nothing. Only a great gap...') is the first story beat. **Master promise:** how a world made like that ends, paid at the Ragnarok chapter (from {mmss(chap_start[6])}) and at the CLOSE beat {close_id} (about {mmss(beat_time[close_id])}, about {beat_time[close_id]/total_words*100:.0f}% of the runtime).")
ctas = "; ".join(f"{i} at about {mmss(beat_time[i])}" for i in cta_ids)
out.append(f"- Re-hook: {rehook_id} 'The skull in the sky is still on his shoulders, for now.' at about {mmss(beat_time[rehook_id])}. Calls to action (spoken by Daniel, no on-screen text, asides over the previous plate): {ctas}.")
out.append("- **Variants (binding; plate generation reads the card named in `state:`).** Odin keeps ONE eye in every beat, including the brothers and the Ymir beats before he gives the eye at the well (accepted by William). Tyr is `Tyr (hand)` until the bite and `Tyr (stump)` from the beat after it.\n")
out.append("| Variant card | First beat | Last beat | Beats | Where it changes |")
out.append("|---|---|---|---|---|")
change = {
    "Odin (one eye)": "never changes; no two-eyed Odin anywhere",
    "Tyr (hand)": f"changes to Tyr (stump) at {tyr_stump_first}, the beat after the bite ({bite_id} 'Fenrir bites the hand off' shows the jaws closing on the wrist, so the hand is still on the arm)",
    "Tyr (stump)": f"from {tyr_stump_first} to the end of the video",
    "Fenrir (cub)": f"to Fenrir (young) at {newid['N-059']}",
    "Fenrir (young)": f"to Fenrir (huge, 2.0) at {newid['N-061']}",
    "Fenrir (huge, 2.0)": f"to Fenrir (bound) at {newid['N-074']}",
    "Fenrir (bound)": f"to Fenrir (huge) at {newid['N-139']} (the chains break)",
    "Fenrir (huge)": "free at Ragnarok; killed by Vidar",
    "Loki as an old woman": "one scene only",
    "Loki as a salmon": "one scene only",
    "Jormungandr (small serpent)": f"to the world-ring serpent at {newid['N-057']}",
    "Hel (child)": "stays a child throughout",
    "Hymir (scale 3.0)": "none",
    "Ymir (scale 4.0)": "none; body only from the killing on",
    "Surt (scale 4.0)": "none",
    "Loki (bound)": f"bound from {newid['N-128']} until the chains break (N-152 shows him free)",
    "Baldr (dead)": f"alive until he falls dead at {newid['N-120']}; next shown at {newid['N-126']} (dead, burning ship); alive again at {newid['N-160']}",
}
for v, a, z, n in vrows:
    out.append(f"| {v} | {a} | {z} | {n} | {change.get(v, '')} |")
out.append("")
plan = "; ".join(f"{('COLD OPEN' if ci == 0 else chapters[ci][0].title())} {mmss(chap_start[ci])}" for ci, si, ei, w in spans)
out.append("Chapter plan: " + plan + "\n")

span_by_start = {si: (ci, w) for ci, si, ei, w in spans}
for i, b in enumerate(new_seq):
    if i in span_by_start:
        ci, w = span_by_start[i]
        out.append(f"## COLD OPEN  (0:00, {w} words)\n" if ci == 0 else f"## CHAPTER: {chapters[ci][0]}  ({mmss(chap_start[ci])}, {w} words)\n")
    tag = f" [{b['tag']}]" if b["tag"] in ("CTA", "PULL", "CLOSE") else ""
    out.append(f"**{b['id']}** {b['text']}{tag}")
    out.append(f"- shot: {b['shot']}")
    out.append(f"- state: {b['state']}")
    out.append(f"- trace: {b['trace']}\n")

out.append("## Old-to-new beat id map (draft 3 to draft 4)\n")
rows = [(oid, DELETE[oid] if oid in DELETE else newid[oid]) for oid in order]
out.append("| Draft 3 | Draft 4 | | Draft 3 | Draft 4 |")
out.append("|---|---|---|---|---|")
half = (len(rows) + 1) // 2
for i in range(half):
    a = rows[i]; c = rows[i + half] if i + half < len(rows) else ("", "")
    out.append(f"| {a[0]} | {a[1]} | | {c[0]} | {c[1]} |")
newonly = [b["id"] for b in new_seq if (b["old"] or "").startswith("new")]
out.append("")
out.append("New beats with no draft 3 id: " + ", ".join(newonly) + f" (hook C {new_seq[0]['id']} to {new_seq[len(hook)-1]['id']}; re-hook {rehook_id}).")

open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
stats = {"words": total_words, "sentences": sent_clean, "questions": questions, "beats": len(new_seq),
         "raw": raw, "hook_words": hook_words, "cta": {i: mmss(beat_time[i]) for i in cta_ids},
         "pull": {i: mmss(beat_time[i]) for i in pull_ids}, "rehook": mmss(beat_time[rehook_id]),
         "close": [close_id, mmss(beat_time[close_id])],
         "chapters": {chapters[ci][0]: (mmss(chap_start[ci]), w) for ci, si, ei, w in spans},
         "map": {k: v for k, v in rows}, "newid": newid}
json.dump(stats, open("src/gen5_stats.json", "w"), indent=1)
print(total_words, sent_clean, questions, len(new_seq), raw, "hook", hook_words, "cta", stats["cta"], "rehook", stats["rehook"], "close", stats["close"])
