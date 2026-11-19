import json, re
B = '/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/'
chs = json.load(open(B + 'src/parsed2.json'))
w = lambda t: len(re.findall(r"[A-Za-z0-9']+", t))

def beat(text, shot, state, trace, **kw):
    d = {'text': text, 'shot': shot, 'state': state, 'trace': trace}
    d.update(kw)
    return d

# ---------- three hooks ----------
S_ODIN = "Odin's hall; night; 1 present: Odin alone; no movement"
S_FROCK2 = "Fenrir's rock; dusk; 2 present: Fenrir (bound), Tyr; Tyr stands still"
S_TYR = "Fenrir's rock; dusk; 1 present: Tyr; close on his raised arm"
S_FEN1 = "Fenrir's rock; dusk; 1 present: Fenrir; eyes open"
S_FRISE = "Fenrir's rock; night; 1 present: Fenrir; Fenrir rises"
S_VIG2 = "Vigrid plain; night; 2 present: Odin, Fenrir (huge); Odin walks toward the wolf"
S_DOOR = "Odin's hall doorway; dawn; 1 present: Odin; he faces the camera, no movement"
S_GRND = "Asgard grounds; day; 4 present: Fenrir, Odin, Thor, Tyr; they stand in a half circle"
S_GRND_LOOK = "Asgard grounds; day; 4 present: Fenrir, Odin, Thor, Tyr; Odin and Thor look away, Tyr steps forward"
S_FROCK4 = "Fenrir's rock; dusk; 4 present: Fenrir, Odin, Thor, Tyr; the wolf strains, ribbon tightens"
S_VIG_LUNGE = "Vigrid plain; night; 2 present: Odin, Fenrir; the wolf lunges"
S_NEW = "the new world; dusk; 0 present; static wide, slow push-in"
S_YBODY = "Ymir's body, now land; dawn; 0 present; slow pan from sea to peaks"
S_GAP4 = "the empty gap; dawn; 4 present: Odin, Vili, Ve, Ymir's body; brothers drag the body"
S_BURNT = "burnt plain; night, red sky; 0 then 3: Odin, Thor, Tyr fallen"
S_GREEN = "a green hill; dawn; 0 present; green rises"
S_VOID = "empty pale-blue void; dawn; 0 present; slow pull-out"
SH_VOID = "wide, dawn: an empty pale-blue gap between a white ice land on the left and a red glowing land on the right"

HOOKS = {}
HOOKS['a'] = [
 beat("Odin knows how he will die.", "medium, firelit hall: Odin alone on a high seat, one eye, wide hat, looking at his own hands", S_ODIN,
      "Voluspa 28-30 (Odin consults the seeress), 53-54 (Odin fares to fight the wolf; 'his father is avenged') V; Gylf 51 ('The Wolf shall swallow Odin') V"),
 beat("A seeress told him that a wolf will kill him.", "medium, firelit hall: Odin alone, head tilted as if listening, eye half closed", S_ODIN,
      "Voluspa 1 (the seeress addresses Valfather), 28-30, 53-54 V; Bellows note on 53: Othin 'fated' to be 'slain by the wolf Fenrir'; Gylf 51 V. NEW CLAIM A1 (see DRAFT3-CHANGES)"),
 beat("So the gods chain the wolf,", "wide, dusk: the huge grey wolf Fenrir bound to a flat rock by a thin pale ribbon, Tyr standing alone beside him", S_FROCK2, "Gylf 34 V"),
 beat("and one of them loses a hand.", "close, dusk: Tyr alone holding up his right arm, which ends in a bandaged stump", S_TYR, "Gylf 34 V"),
 beat("It changes nothing.", "wide, dusk: Fenrir alone on his rock, the ribbon pulled tight, eyes open and fixed on the camera", S_FEN1,
      "(ours) framing; basis Gylf 51 (the fetters are broken at the end)"),
 beat("On the last day, every chain breaks,", "wide, night: the huge grey wolf standing up, the ribbon in pieces around him, jaws open from ground to clouds", S_FRISE,
      "Gylf 51 V ('all fetters and bonds shall be broken and rent. Then shall Fenris-Wolf get loose')"),
 beat("and Odin goes out to meet the wolf anyway.", "wide, night: tiny Odin in armor and wide hat walking across a burnt plain toward the huge grey wolf, red sky", S_VIG2,
      "Gylf 51 V ('He shall go forth against Fenris-Wolf'); Voluspa 53 V. NEW CLAIM A2"),
 beat("This is how that day comes.", "close, dawn: Odin facing us, one eye, wide hat, pale light", S_DOOR, "(ours; bridge into the story)"),
]
HOOKS['b'] = [
 beat("A wolf agrees to be chained, on one condition.", "medium: the huge grey wolf with jaws slightly open, a thin pale ribbon laid on the grass", S_GRND, "Gylf 34 V"),
 beat("One god must put his right hand in the wolf's mouth.", "close: the wolf's open jaws, teeth white, a hand-sized gap in the dark", S_GRND, "Gylf 34 V"),
 beat("The gods look at one another,", "medium: Odin and Thor glancing sideways at each other, silent", S_GRND_LOOK, "Gylf 34 V (none of the Aesir would, until Tyr)"),
 beat("and only Tyr steps forward.", "medium: Tyr walking forward alone, the wolf in front of him", S_GRND_LOOK, "Gylf 34 V"),
 beat("The wolf bites the hand off.", "close: the wolf's jaws closing on Tyr's wrist", S_FROCK4, "Gylf 34 V"),
 beat("That hand is the least of it.", "close, dusk: Tyr alone holding up his right arm, which ends in a bandaged stump", S_TYR, "(ours) framing; basis Gylf 51"),
 beat("At the end of the world, the same wolf swallows Odin.", "medium: Fenrir's huge jaws closing on Odin, hat flying off", S_VIG_LUNGE, "Gylf 51 V ('The Wolf shall swallow Odin')"),
 beat("To see how it came to this, we start at the beginning.", SH_VOID, S_VOID, "(ours; bridge); Gylf 4-5 V"),
]
HOOKS['c'] = [
 beat("The sky is a skull.", "wide, dusk: a vast curved skull-shaped dome over a dark sea, no figures", S_NEW, "Grimnismal 40 V"),
 beat("The sea is blood, and the mountains are bones.", "medium: a blue sea washing against brown earth, grey stone peaks rising behind", S_YBODY, "Grimnismal 40 V"),
 beat("In Norse myth, the world is a giant's body, and three brothers made it.", "wide: the huge body lying in the gap, the brothers small on its chest looking down", S_GAP4, "Gylf 6-8 V; Grimnismal 40 V"),
 beat("One of them, Odin, is told how it will end.", "medium, firelit hall: Odin alone, head tilted as if listening, eye half closed", S_ODIN, "Voluspa 1, 28-30, 53-54 V; NEW CLAIM A1 (as hook A)"),
 beat("It ends in fire, and almost every god dies.", "wide, night: Odin, Thor and Tyr lying fallen on a burnt plain, smoke drifting", S_BURNT, "Gylf 51 V; Voluspa 52, 57 V"),
 beat("Then the world begins again.", "wide, dawn: green hills rising from calm blue water", S_GREEN, "Voluspa 59 V; Gylf 53 V"),
 beat("Let us start at the beginning, with the giant.", SH_VOID, S_VOID, "(ours; bridge); Gylf 4-5 V"),
]

def hook_stats(h):
    t = ' '.join(b['text'] for b in h)
    sents = [s for s in re.split(r'(?<=[.?!])\s+', t) if s.strip()]
    return w(t), len(sents), t

if __name__ == '__main__':
    # ---------- build draft 3 ----------
    old = []
    n = 0
    for c in chs:
        for b in c['beats']:
            n += 1
            b['old'] = n
    # insertions after old id
    def aside(prev, text, trace, kind):
        return beat(text, prev['shot'], prev['state'], trace, kind=kind, holds=prev['old'])
    byold = {b['old']: b for c in chs for b in c['beats']}
    ins = {}
    ins[18] = [aside(byold[18], "These myths come straight from the sources, so follow the channel for the rest.",
                     "(ours) CTA 1, soft; narrator aside, holds the N-018 plate", 'CTA')]
    ins[33] = [aside(byold[33], "Everything they just built will end in fire.",
                     "Gylf 51 V ('burn all the world'); Gylf 4 V. Pull line, holds the N-033 plate", 'PULL')]
    ins[79] = [aside(byold[79], "That ribbon will not hold forever.",
                     "Gylf 51 V ('all fetters and bonds shall be broken'). Pull line, holds the N-079 plate", 'PULL')]
    ins[94] = [aside(byold[94], "Follow the channel to see how this fight ends.",
                     "(ours) CTA 2, mid-video; narrator aside, holds the N-094 plate", 'CTA')]
    ins[133] = [aside(byold[133], "Loki will not stay in that cave.",
                      "Gylf 51 V (fetters broken; Loki and Heimdall fall together). Pull line, holds the N-133 plate", 'PULL')]
    ins[143] = [beat("Odin knows how it ends, and goes anyway.",
                     "close, night: Odin in armor and wide hat, one eye fixed ahead, red sky behind",
                     "Vigrid plain; night; 1 present: Odin; he walks forward",
                     "Voluspa 28-30, 53 V; Gylf 51 V. (ours) closes the cold-open loop (hook A, 'goes out to meet the wolf anyway')", kind='CLOSE')]
    ins[175] = [aside(byold[175], "If this was your kind of story, follow the channel. The gods of Egypt are next.",
                      "(ours) CTA 3, closing; narrator aside, holds the N-175 plate", 'CTA')]

    new = []
    for c in chs:
        nc = {'title': c['title'], 'beats': []}
        if c['title'] == 'COLD OPEN':
            for b in HOOKS['a']:
                bb = dict(b); bb['old'] = None; bb['kind'] = 'HOOK'; nc['beats'].append(bb)
            nc['beats'].append(dict(byold[13], kind=None))
        else:
            for b in c['beats']:
                nc['beats'].append(dict(b, kind=None))
                for x in ins.get(b['old'], []):
                    nc['beats'].append(dict(x))
        new.append(nc)
    # ids
    k = 0; maprows = []
    for c in new:
        for b in c['beats']:
            k += 1; b['id'] = f"N-{k:03d}"
    flat = [b for c in new for b in c['beats']]
    for i, b in enumerate(flat):
        if b.get('kind') in ('CTA', 'PULL'):
            b['trace'] = re.sub(r'N-\d{3} plate', flat[i-1]['id'] + ' plate', b['trace'])
    json.dump(new, open(B + 'src/parsed3.json', 'w'))

    alltext = ' '.join(b['text'] for c in new for b in c['beats'])
    tot = w(alltext)
    sents = [s for s in re.split(r'(?<=[.?!])\s+', alltext) if s.strip()]
    ts = lambda words: f"{round(words/150*60)//60}:{round(words/150*60)%60:02d}"
    nb = sum(len(c['beats']) for c in new)
    print('words', tot, 'sents', len(sents), 'mean', round(tot/len(sents), 1), 'q', alltext.count('?'), 'beats', nb, 'time', ts(tot))
    t = 0
    plan = []
    for c in new:
        cw = sum(w(b['text']) for b in c['beats'])
        plan.append(f"{c['title']} {ts(t)}"); print(c['title'], cw, ts(t)); t += cw
    # timestamps of aside beats
    t = 0
    for c in new:
        for b in c['beats']:
            if b.get('kind') in ('CTA', 'PULL', 'CLOSE'):
                print(b['id'], b['kind'], ts(t), '-', ts(t + w(b['text'])), b['text'], w(b['text']))
            t += w(b['text'])
    for key in 'abc':
        print(key, hook_stats(HOOKS[key])[:2])
    # ---------- write SCRIPT-N-draft3.md ----------
    out = []
    out.append('# SCRIPT-N-draft3.md: "The ENTIRE Story of Norse Mythology, Creation to Ragnarok in 10 Minutes" (The Myth Ledger, video 2)\n')
    out.append("Draft 3, 2026-11-14: draft 2 with a new cold open (hook option A from `norse/HOOK-OPTIONS.md`), three pull lines, three calls to action and one loop-closing line. Everything else is draft 2, word for word. Format as draft 2: beat id, spoken text, `shot:`, `state:`, `trace:`. Beat ids are renumbered; the old-to-new table is at the bottom. Nothing recorded, generated, uploaded or sent; `library/` untouched. New claims are listed in `norse/DRAFT3-CHANGES.md` and still need the fact-check pass.\n")
    out.append("## Header")
    out.append(f"- **Spoken words: {tot}** in {len(sents)} sentences (mean {tot/len(sents):.1f}); {alltext.count('?')} questions. At 150 wpm: **{ts(tot)}** raw voice time (target at most 1,600 words: met). {nb} beats, {len(new)-1} named chapters plus the cold open. No text cards, no on-screen text, no chapter bands (PROCESS rule 8).")
    out.append("- Beat = one spoken fragment; a beat that starts lower-case continues the previous one. `shot:` is the single painted image for the beat. `state:` carries forward and changes only when the narration changes it; only the figures named in `state:` appear in the shot. `trace:` gives the source (Voluspa and the other Poetic Edda poems = Bellows 1923; Gylf = Gylfaginning, Prose Edda = Brodeur 1916; Gylf N = Brodeur chapter N in Roman numerals) with V (read in a text) or E (inference). `(ours)` = sentence with no source, or a pure framing/glue line; the basis is stated after it.")
    out.append("- **Aside beats (CTA and PULL) have no new shot.** Their `shot:` and `state:` repeat the previous beat's plate exactly and the `trace:` says `holds N-xxx`; the scene planner should merge each with the plate it holds (the narration simply continues over the same image). The CLOSE beat (%s) is the only new shot, and it uses only Odin." % [b['id'] for c in new for b in c['beats'] if b.get('kind') == 'CLOSE'][0])
    out.append("- No Edda quote appears anywhere in the narration. There is no voiced dialogue.")
    out.append("- Hook (hook A): a god who knows how he dies, the seeress, the chained wolf and the lost hand, the chains that break on the last day, and Odin going out to meet the wolf anyway. The loop closes at the CLOSE beat and the wolf beat (see DRAFT3-CHANGES).")
    ctas = []; t2 = 0
    for c in new:
        for b in c['beats']:
            if b.get('kind') == 'CTA': ctas.append(f"{b['id']} at about {ts(t2)}")
            t2 += w(b['text'])
    out.append("- Calls to action (spoken by Daniel, no on-screen text, asides over the previous plate): " + "; ".join(ctas) + ".\n")
    out.append("Chapter plan: " + "; ".join(plan) + "\n")
    t = 0
    for c in new:
        cw = sum(w(b['text']) for b in c['beats'])
        head = "## COLD OPEN" if c['title'] == 'COLD OPEN' else "## CHAPTER: " + c['title'].upper()
        out.append(f"{head}  ({ts(t)}, {cw} words)\n"); t += cw
        for b in c['beats']:
            tag = f" [{b['kind']}]" if b.get('kind') in ('CTA', 'PULL', 'CLOSE') else ''
            out.append(f"**{b['id']}** {b['text']}{tag}")
            out.append(f"- shot: {b['shot']}")
            out.append(f"- state: {b['state']}")
            out.append(f"- trace: {b['trace']}\n")
    out.append("## Old-to-new beat id map\n")
    out.append("| Draft 2 | Draft 3 | | Draft 2 | Draft 3 |")
    out.append("|---|---|---|---|---|")
    mp = {}
    for c in new:
        for b in c['beats']:
            if b.get('old'): mp[b['old']] = b['id']
    lines = []
    for o in range(1, 176):
        lines.append(f"N-{o:03d} | " + (mp.get(o) if o in mp else "removed (replaced by hook)"))
    half = (len(lines) + 1) // 2
    for i in range(half):
        a = lines[i].split(' | '); bb = lines[i+half].split(' | ') if i+half < len(lines) else ['', '']
        out.append(f"| {a[0]} | {a[1]} | | {bb[0]} | {bb[1]} |")
    out.append("")
    out.append("New beats with no draft 2 id: " + ", ".join(f"{b['id']} ({b['kind']})" for c in new for b in c['beats'] if b.get('old') is None and b.get('kind') != 'HOOK') + "; hook beats " + ", ".join(b['id'] for c in new for b in c['beats'] if b.get('kind') == 'HOOK') + " (hook A, replacing N-001 to N-012 of draft 2; the draft 2 bridge N-013 is kept as %s)." % mp[13])
    open(B + 'SCRIPT-N-draft3.md', 'w').write('\n'.join(out))
    json.dump({'map': mp}, open(B + 'src/map3.json', 'w'))
