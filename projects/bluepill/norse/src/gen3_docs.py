import re, json, sys
sys.path.insert(0, '/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/src')
from gen3 import HOOKS, hook_stats, w
B = '/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/'

notes = {
 'a': ("Hook A: the god who knows how he dies (prophecy that cannot be dodged)",
       "A stranger feels: a person who already knows the worst thing about his own future, then watches every precaution fail. Opens the loop 'what does a god do with a death he cannot dodge?' and the wolf-and-chain image promises a payoff. Closes in draft 3 ids: the chain-break promise at N-138 (draft 2 N-137); Odin going out at the CLOSE beat N-145 ('Odin knows how it ends, and goes anyway.'); the wolf killing him at N-146 (draft 2 N-144). The lost hand is retold in full at N-073 to N-076 (draft 2 N-075 to N-078)."),
 'b': ("Hook B: the hand in the wolf's mouth (one concrete human moment)",
       "A stranger feels: a held breath, a room of gods all looking away and one stepping up, a wolf's open jaws. Opens the loop 'what does the wolf take from the gods at the end of the world?' ('the least of it', 'swallows Odin'). Closes at draft 2 N-144 (Fenrir swallows Odin) and the scene itself is retold in full at draft 2 N-071 to N-079 (chapter 3). Cost: shows the chapter's set piece before the chapter, so chapter 3 starts with less surprise."),
 'c': ("Hook C: the sky is a skull (startling fact)",
       "A stranger feels: a jolt of strangeness from the first five words, then the scale of the thing (a whole world built from a corpse). Opens the loop 'how does a world made like that end?' (Odin is told). Closes across draft 2 N-134 to N-161 (the end and the rebirth), with Odin's fate at N-144. Cost: it names no scene or villain, and chapter 1 repeats the skull and the sea within 30 seconds (draft 2 N-027 to N-031), so it is the weakest of the three on curiosity."),
}

out = []
out.append('# HOOK-OPTIONS.md: three cold opens for the Norse video (The Myth Ledger, video 2)\n')
out.append("2026-11-14. Written to `norse/BRIEF-DRAFT3.md`. Each option is a full replacement for the draft 2 cold open (N-001 to N-012; the draft 2 bridge N-013 'Let us start at the beginning.' is kept only where it still works). Beat format identical to draft 2. Only the cast of draft 2 (28 cards); no new place, prop or character; every `state:` names only the figures in the shot. Calm, dry voice (Daniel); no hype words. Claims marked NEW CLAIM are listed in `norse/DRAFT3-CHANGES.md` for the fact-check pass.\n")
out.append("Nothing in this file was recorded, generated, uploaded or sent.\n")
for key in 'abc':
    h = HOOKS[key]
    title, note = notes[key]
    n_w, n_s, text = hook_stats(h)
    bridge = h[-1]['text']
    story_words = sum(w(b['text']) for b in h[:-1])
    ss = len(re.split(r'(?<=[.?!])\s+', ' '.join(b['text'] for b in h[:-1])))
    out.append(f"## {title}\n")
    out.append(f"- Hook words (without the bridge): **{story_words}** in {ss} sentences (mean {story_words/ss:.1f}); with the bridge {n_w}. Hook alone is about {story_words/150*60:.0f} s at 150 wpm. Stakes by 10 s, escalation by 15 s as marked in the note.")
    out.append(f"- Strategic note: {note}\n")
    for i, b in enumerate(h, 1):
        out.append(f"**N-H1{key}-{i:02d}** {b['text']}")
        out.append(f"- shot: {b['shot']}")
        out.append(f"- state: {b['state']}")
        out.append(f"- trace: {b['trace']}\n")
    out.append(f"Spoken in full: {' '.join(b['text'] for b in h)}\n")
out.append("## Bridge check\n")
out.append("- A: ends 'This is how that day comes.' then the unchanged 'Let us start at the beginning.' (draft 3 N-008, N-009).")
out.append("- B: the draft 2 bridge is replaced by 'To see how it came to this, we start at the beginning.' (it replaces N-013, one beat).")
out.append("- C: the draft 2 bridge is replaced by 'Let us start at the beginning, with the giant.' (it replaces N-013, one beat).\n")
out.append("## Recommendation\n")
out.append("Use **Hook A**. It is the only one that gives a stranger a person to care about (a god who knows how he dies), a threat (the wolf), a visible cost (the lost hand) and a date on the calendar (the last day), and it plants the exact image the video pays off at about 8:15, when Odin goes out to meet the wolf anyway. Hook B is a stronger single scene but spends chapter 3's best moment before the story starts, and Hook C has the best first sentence but is a fact list that chapter 1 repeats within 30 seconds. If William prefers a more tactile open, B is the fallback; it needs no other change to the script.\n")
open(B + 'HOOK-OPTIONS.md', 'w').write('\n'.join(out))
