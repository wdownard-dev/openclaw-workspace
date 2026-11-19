import json,re
chs=json.load(open('/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/src/parsed2.json'))
w=lambda t: len(re.findall(r"[A-Za-z0-9']+",t))
tot=sum(w(b['text']) for c in chs for b in c['beats'])
allt=' '.join(b['text'] for c in chs for b in c['beats'])
sents=[x for x in re.split(r'(?<=[.?!])\s+',allt) if x.strip()]
def ts(words):
    sec=round(words/150*60); return f"{sec//60}:{sec%60:02d}"
out=[]
out.append('# SCRIPT-N-draft2.md: "The ENTIRE Story of Norse Mythology, Creation to Ragnarok in 10 Minutes" (The Myth Ledger, video 2)\n')
out.append("Draft 2, 2026-11-14: draft 1 with every FIX from `norse/FACTCHECK-N.md` applied (18 spoken lines rewritten, locators corrected, shot/state changed only on N-068 and N-121/N-122). Beat ids are unchanged. Calm lane, one straight chronological story from the Eddas, Snorri as the closing chapter. Format as draft 1 and `video2/SCRIPT-V5.md`: beat id, spoken text, `shot:`, `trace:`, plus a `state:` line per beat (the SCENE STATE: location; time of day; who is present and how many; action direction). Nothing recorded, generated, uploaded or sent; `library/` untouched.\n")
out.append("## Header")
out.append(f"- **Spoken words: {tot}** in {len(sents)} sentences (mean {tot/len(sents):.1f}); {allt.count('?')} questions. At 150 wpm: **{ts(tot)}** raw voice time. {sum(len(c['beats']) for c in chs)} beats, {len(chs)-1} named chapters plus the cold open. No text cards, no on-screen text, no chapter bands (PROCESS rule 8).")
out.append("- Beat = one spoken fragment; a beat that starts lower-case continues the previous one. `shot:` is the single painted image for the beat. `state:` carries forward and changes only when the narration changes it; only the figures named in `state:` appear in the shot. `trace:` gives the source (Voluspa and the other Poetic Edda poems = Bellows 1923; Gylf = Gylfaginning, Prose Edda = Brodeur 1916; Gylf N = Brodeur chapter N in Roman numerals; locators checked in the fact-check pass) with V (read in a text) or E (inference). `(ours)` = sentence with no source, or a pure framing/glue line; the basis is stated after it.")
out.append("- No Edda quote appears anywhere in the narration. There is no voiced dialogue, so nothing needs flagging as invented speech.")
out.append("- Hook: number first (nine worlds), escalating facts, collapse line (\"It makes no difference.\"), the question, then \"Let us start at the beginning.\"\n")
out.append("Chapter plan: "+"; ".join(f"{c['title']} {ts(sum(w(b['text']) for cc in chs[:i] for b in cc['beats']))}" for i,c in enumerate(chs))+"\n")
n=0; t=0
for c in chs:
    cw=sum(w(b['text']) for b in c['beats'])
    head = "## COLD OPEN" if c['title']=='COLD OPEN' else "## CHAPTER: "+c['title'].upper()
    out.append(f"{head}  ({ts(t)}, {cw} words)\n")
    t+=cw
    for b in c['beats']:
        n+=1
        out.append(f"**N-{n:03d}** {b['text']}")
        out.append(f"- shot: {b['shot']}")
        out.append(f"- state: {b['state']}")
        out.append(f"- trace: {b['trace']}\n")
open('/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/SCRIPT-N-draft2.md','w').write('\n'.join(out))
# beat table for notes
rows=[]
n=0
for c in chs:
    for b in c['beats']:
        n+=1; rows.append((f"N-{n:03d}",c['title'],b['text'],b['trace']))
json.dump(rows,open('/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/src/rows2.json','w'))
ours=[r for r in rows if '(ours' in r[3]]
print(len(ours),'ours beats')
for r in ours: print(r[0],r[2][:60],'|',r[3])
