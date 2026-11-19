"""Write SHOTLIST-V1-RETIMED.md from shots_timed.json + audio/quality.json + audio/words.json (run after assemble.py)."""
import json, os, re
HERE=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(f"{HERE}/shots_timed.json")); Q=json.load(open(f"{HERE}/audio/quality.json")); W=json.load(open(f"{HERE}/audio/words.json"))
SL=D['shot_list']
def ts(x): m=int(x//60); return f"{m}:{x-60*m:04.1f}"
def cell(x): return str(x).replace('|','/').replace('\n',' ')
def base(a): return re.sub(r'^X:','',a.split(' + ')[0]).strip()
shorts=[s for s in SL if s['flag']=='short']; longs=[s for s in SL if s['flag']=='long']
by={s['shot']:s for s in SL}
def hint(s):
    for nb,lab in ((s['shot']-1,'previous'),(s['shot']+1,'next')):
        o=by.get(nb)
        if o and o['type']!='title card' and base(o['asset'])==base(s['asset']):
            tot=s['sec']+o['sec']; return f"same image as the {lab} shot ({nb}); fold into one hold of {tot:.1f} s"
    return "no same-image neighbour: keep as a deliberate short beat, or hold the previous frame through this line"
nar=[s for s in SL if s['type']!='title card']
avg=sum(s['sec'] for s in nar)/len(nar)
L=[]
L.append('# SHOTLIST-V1-RETIMED.md: video 1, "The Cyclops Was Real? What the Myth Is Hiding"\n')
L.append("Nothing uploaded or sent. Shot structure, numbering and art notes are unchanged from `SHOTLIST-V1.md` (see it for characters, light, camera and drift notes). Only the timing changed: every narrated shot now starts on the first word of its line in the real ElevenLabs track (`audio/narration.wav`, word times in `audio/words.json`); the first shot after a chapter card starts when the card ends and absorbs the pause before the voice; each shot ends where the next begins. Machine-readable version: `shots_timed.json`.\n")
L.append("## Summary\n")
L.append(f"- **Runtime {D['total_label'][:-3]} ({D['total_sec']:.1f} s)**, down from the 11:01 estimate and 5 s under William's accepted 10:30. Voice only: {sum(c['dur'] for c in Q['per_chunk']):.0f} s of speech across 13 paragraph takes, {Q['speech_span_wpm']} wpm from first to last word including pauses and cards ({Q['wpm_all_in']} wpm over the whole runtime).")
L.append(f"- **{D['shots']} shots** ({D['shots']-5} narrated plus 5 silent chapter cards of 2.5 s). **{D['cuts_per_min']} cuts per minute** (mean narrated shot {avg:.1f} s, median {sorted(s['sec'] for s in nar)[len(nar)//2]:.1f} s, shortest {min(s['sec'] for s in nar):.1f} s, longest {max(s['sec'] for s in nar):.1f} s).")
L.append(f"- **Flags:** {len(shorts)} shots under 2.5 s, {len(longs)} over 8 s. Every short one is a one-line or half-line beat that the old estimate padded to a 3.2 s floor; the voice does not.")
L.append("- Inserted silence: 0.40 s lead-in, 0.35 s between paragraphs (0.40 s between cold open and stakes), 0.35 s before each chapter card, 2.5 s card, 0.45 s after the card, then the voice. End card holds at least 4 s (narration plus tail).")
L.append("- **Cut placement:** cuts sit exactly on word onsets. Editors usually pull a cut 2 to 4 frames early (0.07 to 0.13 s) so the picture lands just before the word; do that in the assembly, not here.\n")
L.append("## Chapters (real times; replace the estimates in SCRIPT-V1.md and the description)\n")
L.append("| Chapter | Card/start (real) | Old estimate |\n|---|---|---|")
old={"Cold open":"0:00","Stakes":"0:23","1. The poem as Homer tells it":"0:42","2. The skull":"4:16","3. The other Cyclopes":"6:39","4. What we can and cannot say":"9:04","Verdict and next":"10:18"}
for k,v in Q['chapter_starts'].items():
    cardn=Q['cards'].get(str([i for i,c in enumerate(old) if c==k][0]),None)
    L.append(f"| {k} | {ts(v)} | {old[k]} |")
L.append("\nYouTube chapter list (card start = chapter timestamp; paste after William listens): "+"; ".join(f"{int(v//60)}:{int(v%60):02d} {k.split('. ',1)[-1]}" for k,v in Q['chapter_starts'].items() if k!='Stakes')+"\n")
L.append("## Flagged shots\n")
L.append("**Over 8 s: none.** Longest narrated shot is %.1f s.\n"%max(s['sec'] for s in nar))
L.append("**Under 2.5 s:**\n\n| # | start | sec | narration | suggestion |\n|---|---|---|---|---|")
for s in shorts: L.append(f"| {s['shot']} | {ts(s['start'])} | {s['sec']:.1f} | {cell(s['narration'])} | {hint(s)} |")
L.append("")

L.append("## Listen first (I cannot judge a voice by ear; these are the spots most likely to be wrong)\n")
L.append("Names are sent to the TTS as phonetic respellings (the saved script is untouched). Timestamps are on the final timeline. `rel` is seconds per syllable relative to the narration average (1.0 = normal; below 0.6 is hurried, above 1.5 is drawn out).\n")
seen=set(); rows=[]
for r in Q['risky']:
    if r['kind']!='name' or not r['respelled']: continue
    key=re.sub(r"[^A-Za-z]","",r['word']).lower()
    if key in seen: continue
    seen.add(key); rows.append(r)
L.append("| time | name | sent to TTS as | dur | rel |\n|---|---|---|---|---|")
for r in sorted(rows,key=lambda r:r['t']): L.append(f"| {ts(r['t'])} | {r['word']} | {r['spoken']} | {r['dur']:.2f} s | {r['rel_per_syllable']} |")
L.append("\nNames left as written (the model usually handles them): Buxton, Witton, Mayor, Hesiod, Euripides, Mycenae, Virgil, Etna, Aeolian, Cyclopes, Odysseus, Poseidon, cyclopia. Check Cyclopes (sy-KLOH-peez) at 0:51.7 and Buxton at 6:08.\n")
L.append("Hedge phrases (should be flat, not stressed): "+"; ".join(f"{r['word'].strip('.,:')} {ts(r['t'])}" for r in Q['risky'] if r['kind']=='hedge' and r['word'].strip('.,:').lower() in ('presumably','may','perhaps','plausible','implies','unproven','suspect','hypothesis','bluntly','baseless'))+".\n")
L.append("Paragraph takes generated at a speed above 1.0 to even out the pace (the voice slowed on its own in the later chapters): chunk 8 (speed 1.05, 5:34 to 6:16), chunk 9 (1.06, 6:19 to 7:39). If either sounds hurried, re-take it at 0.97 and accept a few seconds more runtime.\n")
L.append("## Shot list (real times)\n")
cur=None
for s in SL:
    if s['chapter']!=cur:
        cur=s['chapter']; L.append(f"\n### {cur}\n\n| # | start | end | sec | flag | narration | type | asset | old start / sec |\n|---|---|---|---|---|---|---|---|---|")
    nr=s['narration'] if s['narration'] else "(silent chapter card)"
    L.append(f"| {s['shot']} | {ts(s['start'])} | {ts(s['end'])} | {s['sec']:.1f} | {s['flag'] or ''} | {cell(nr)} | {s['type']} | {cell(s['asset'])} | {ts(s['old_start'])} / {s['old_sec']:.1f} |")
L.append("")
open(f"{os.path.dirname(HERE)}/video1/SHOTLIST-V1-RETIMED.md","w").write("\n".join(L))
print("ok",len(L))
