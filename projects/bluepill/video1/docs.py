import sys, re, collections, math
sys.argv=['x']
exec(open('render.py').read().split("if __name__=='__main__':")[0])
OUT='/home/williamdownard/.openclaw/workspace/projects/bluepill/'
def cell(x): return str(x).replace('|','/').replace('\n',' ')
# ---------- SCRIPT ----------
paras=[]; cur=[]; curch=None; blocks=[]
for r in R:
    if r['ch']!=curch:
        if cur: blocks.append((curch,cur)); cur=[]
        curch=r['ch']; cur=[[]]
    if r['para'] and cur[-1]: cur.append([])
    cur[-1].append(r['text'])
blocks.append((curch,cur))
# chapter word counts and timestamps (VO time only + cards)
chw=collections.Counter()
for r in R: chw[r['ch']]+=len(r['text'].split())
narr=""
for ch,pl in blocks:
    title=CH[ch][0]
    narr+=f"\n### {title}  (est. {fmt(ch_start[ch])}, {chw[ch]} words)\n\n"
    for p in pl: narr+=' '.join(p)+"\n\n"
def findt(sub):
    for s in shots:
        if sub in s['text']: return s['start']
T=dict(trap=findt('That stone is the real trap'),eye=findt('Now the stake goes into the eye'),ch2=ch_start[3],mayor=findt('Mayor herself is careful'),emp=findt('Then there is a problem'),hes=findt('Meanwhile, the Cyclops'),walls=findt('There is a third strand'),solid=findt('So where does that leave'),folk=findt('The blinding story itself'),stakes=ch_start[1],verdict=ch_start[6])
hes_len=findt('Later poets merged')-T['hes']
nover=sum(1 for s in shots if s['kind']=='bakedX' and ('quote' in s['asset'] or 'overlay' in s['asset']))
cut_bgs=sorted({m for s in shots if s['kind']=='cutout' for m in re.findall(r'\bNBG\d+\b',s['asset'])})
yt=[("Cold open",0)]
names={2:"The poem as Homer tells it",3:"The skull",4:"The other Cyclopes",5:"What we can and cannot say",6:"Verdict, and what's next"}
for c in (2,3,4,5,6): yt.append((names[c],ch_start[c]))
script=f"""# SCRIPT-V1.md: "The Cyclops Was Real? What the Myth Is Hiding" (Project Blue Pill, video 1, draft 1)

Nothing generated, uploaded or sent. Written 2026-11-12 for The Myth Ledger. Every claim in the narration is tied to a source and a confidence label in `RESEARCH-V1.md`. The shot list is in `SHOTLIST-V1.md`; both are generated from `video1/beats.py`, so narration and shots stay in step.

## Numbers
- **Narration: {words:,} words.** At 150 wpm that is {words/150:.1f} min of voice ({fmt(words/2.5)}); with the 5 silent chapter cards and a 3.2 s floor on very short lines the cut runs about {fmt(total)} [E]. The trim candidates at the end save about 80 words (roughly 30 s) and bring it to about 10:30; for exactly 10:00 also cut the two-line folktale pair in chapter 4.
- Cold-open hook (first three lines, 33 words) ends at about 0:13. The stakes line starts at {fmt(T['stakes'])}.
- Re-hook beats, with estimated start times (from word counts): {fmt(T['trap'])} the stone is the trap; {fmt(T['eye'])} Homer never writes "one eye"; {fmt(T['ch2'])} "is there anything solid underneath it?" (chapter 2); {fmt(T['mayor'])} even Mayor is careful; {fmt(T['emp'])} the Empedocles story has no source; {fmt(T['hes'])} Hesiod's smiths; {fmt(T['walls'])} the walls are real; {fmt(T['solid'])} what is solid and what is not; {fmt(T['folk'])} the folktale has two hundred versions. The longest gap between beats is about 1:40.
- Tone: adult, restrained, dry. No exclamations, no all-caps words, no impact-word moments. Source attribution is spoken inline.

## Voice direction (ElevenLabs, George)
Slower and flatter than the v2 test: calm storyteller, let sentences land, dry on the asides ("We will leave it out", "Even cannibals get a love life"). Short pause after each chapter card. Keep the hedges as written ("may", "one theory", "unproven"); do not stress them or the claims will sound unsure.
Pronunciations: Polyphemus (pol-ih-FEE-mus), Palaeoloxodon (not spoken), Othenio Abel (oh-TEN-ee-oh AH-bel), Empedocles (em-PED-oh-kleez), Theocritus (thee-OCK-rih-tus), Thucydides (thoo-SID-ih-deez), Tiryns (TIE-rinz), Pausanias (paw-SAY-nee-us), Brontes (BRON-teez), Steropes (STAIR-oh-peez), Arges (AR-geez), Aci Trezza (AH-chee TRET-sah), Aguirre (ah-GHEE-reh), Buxton (BUCK-stun), Burkert (BOOR-kert), Witton (WIT-un).

## Narration
{narr}
## Title options
Patterns from `OUTLIER-CHECK.md` (round 2): "turned out to be true / real" has the highest ceiling, "Every ___ explained" is the pattern small channels crack, "real story / the truth" is mid. None of the options below claims more than the video delivers.

1. **The Cyclops Was Real? What the Myth Is Hiding** (William's approved working title). Pattern: "turned out to be real", posed as a question. Defence: the video answers it, "not as a one-eyed giant; maybe a skull; and the walls and smiths are real". The one soft spot is "is hiding", which implies a secret the video does not claim to uncover. Safer variant that costs little: **"The Cyclops Was Real? What the Myth May Be Hiding"**.
2. **Did a Tiny Elephant Invent the Cyclops? What the Evidence Actually Says** Pattern: specific curiosity plus an evidence promise. Defence: it is the exact question chapter 2 tests, and the answer given ("plausible, unproven") matches "what the evidence actually says".
3. **Every Kind of Cyclops, Explained: Which Parts Are Real?** Pattern: "Every ___ explained", the small-channel pattern. Defence: chapters 1 and 3 cover the Homeric, Hesiodic and wall-building traditions plus the Sicilian and folktale strands, and the verdict names which parts are real (the walls, the elephants) and which are not. "Every kind" means every Greek tradition, not every one-eyed monster on earth.

## Description (draft)
Was the Cyclops a real creature? Not as Homer describes him. But the question leads somewhere stranger: an elephant on Sicily under a metre tall, a 1914 theory about its skull, and an argument that nobody has ever managed to prove.

This video goes through the Odyssey's cave scene as Homer tells it, the dwarf-elephant skull theory (Othenio Abel, Adrienne Mayor) and its critics, Hesiod's thunderbolt-forging Cyclopes, the Sicilian and Etna tradition, and the "cyclopean" walls of Mycenae and Tiryns. Every claim is labelled with its source, and we say where the evidence stops.

Chapters
{chr(10).join(f"{fmt(t)} {n}" for n,t in yt)}

Sources
Primary texts
- Homer, Odyssey 9 and 1.68-75 (Butler prose translation): https://www.gutenberg.org/ebooks/1727
- Homer, Odyssey 9 (A.T. Murray, Loeb 1919; Greek text): https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0136:book=9 and https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0135:book=9
- Hesiod, Theogony 139-146 (Evelyn-White): https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0130:card=139
- Euripides, Cyclops (Shelley translation): https://en.wikisource.org/wiki/Cyclops_(Shelley_1824)
- Theocritus, Idyll 11 (Andrew Lang): https://www.gutenberg.org/ebooks/4775
- Thucydides 6.2 and 3.88 (Crawley): https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0200:book=6:chapter=2
- Virgil, Aeneid 3 and 8 (Williams): https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.02.0054:book=3
- Pausanias 2.16 and 2.25 (W.H.S. Jones): https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.01.0160:book=2:chapter=25
Modern scholarship
- Othenio Abel, Die Tiere der Vorwelt (1914), pp. 31-33, translated by Jason Colavito: https://www.jasoncolavito.com/fossil-origin-of-the-cyclops.html
- Adrienne Mayor, The First Fossil Hunters (Princeton University Press, 2000; rev. 2011), and her comments in Discover Magazine: https://www.discovermagazine.com/one-eyed-looking-mammoth-fossils-may-have-inspired-origins-of-the-cyclops-45824
- Mercedes Aguirre and Richard Buxton, "Seven Ways to Approach a Cyclops", in Cyclops (Oxford University Press, 2020): https://doi.org/10.1093/oso/9780198713777.003.0002
- Mark P. Witton and Richard A. Hing, Interdisciplinary Science Reviews 49 (2024): https://doi.org/10.1177/03080188241255543
- Background reference articles: https://en.wikipedia.org/wiki/Cyclopes, https://en.wikipedia.org/wiki/Palaeoloxodon_falconeri, https://en.wikipedia.org/wiki/Dwarf_elephant, https://en.wikipedia.org/wiki/Cyclopean_masonry, https://en.wikipedia.org/wiki/Polyphemus

Translations quoted on screen are credited in the video. [Artwork disclosure line: William to decide the wording on how the illustrations were made; see PLAN.md section 5.]

## Thumbnail concept
Cast: **Odysseus** (style A, laurel wreath, blue sash) and the **Cyclops cy_v4** (olive-brown skin, plain rope belt, no bells). No text on the characters, no emoji, no arrows.
- **Primary:** a close, low-angle Cyclops face fills the right two thirds, single eye large and sharp, cool cave light with one warm rim from a fire. Odysseus small in the lower-left foreground, looking up, face lit, wreath and sash readable. The eye sits on a rule-of-thirds point and survives at 120 px wide.
- **Text (max 3 words):** **WAS HE REAL?** in a condensed serif, cream on a dark block at the upper left (inside the mobile-safe zone, clear of the eye and of Odysseus). One accent colour at most.
- **Alternate B (curiosity gap):** split frame, skull plate (nasal opening ringed) on the left, Cyclops eye on the right. Text: **SAME HOLE?** The skull must be the real plate, not a generated one.
- Source image: shot NB01 (Cyclops close-up) plus a Cyclops-and-Odysseus scene such as RC02; generate a dedicated thumbnail frame only if neither crops well (1 extra image, counted in the shot list margin).
- Defensibility: "WAS HE REAL?" matches title option 1 and the video answers it.

## Chapter timestamps (estimates from word counts; re-time to the real voice track)
{chr(10).join(f"- {fmt(t)} {n}" for n,t in yt)}

## Pre-publish verification (do these before the voice track is locked)
1. Read Witton and Hing (2024) and Aguirre and Buxton (2020). I could not open either (publisher bot check; see RESEARCH-V1.md). The lines attributed to them are paraphrases of what a secondary article quotes. Confirm the paraphrases or soften them.
2. Re-run the "one eye" search on the Greek of Odyssey 9 in the Perseus search tool (steps in RESEARCH-V1.md). It found no "forehead" and no "one eye" in the Greek or in the Butler and Murray translations; a different modern translation may add the word "one", which is a translator's choice, not Homer's.
3. Confirm any on-screen photograph or plate is public domain or licensed (skull plate, Abel title page).

## Trim candidates if the cut runs long
Cut in this order: "It is not much of a gift, but it buys time" (NB10 then drops as well), the Burkert line, "Even cannibals get a love life", the Euripides line, "Homer gives the detail. We will leave it out.", "Beside them, even a hero looks small", "Archaeologists still call the style cyclopean masonry", the Aguirre and Buxton verdict in chapter 4. Together about 80 words.
"""
open(OUT+'SCRIPT-V1.md','w').write(script)
# ---------- SHOTLIST ----------
def row(s):
    return f"| {s['n']} | {fmt(s['start'])} | {s['d']:.1f} | {cell(s['text']) if s['text'] else '(silent chapter card)'} | {s['kind']} | {cell(s['chars'])} | {cell(s['light'])} | {cell(s['cam'])} | {cell(s['asset'])} | {cell(s['note'])} |"
camdef={'push-in':'push-in 1.00 to 1.06 over the shot, ease-in-out','pull-out':'pull-out 1.06 to 1.00','hold':'hold, no move','pan L-R slow':'pan left to right, fixed zoom, 0.5 px/frame max','pan R-L slow':'pan right to left, fixed zoom, 0.5 px/frame max'}
head="| # | start | sec | narration | type | characters | setting and light | camera | asset | notes, new art, drift risk |\n|---|---|---|---|---|---|---|---|---|---|\n"
body=""
lastch=None
for s in shots:
    if s['ch']!=lastch:
        lastch=s['ch']; body+=f"\n### {CH[s['ch']][0]}\n\n"+head
    body+=row(s)+"\n"
mixrows=[("Baked scenes (new, cropped from a new scene, or an existing accepted slot)",kc['baked']),("Cutouts on inked empty-stage backgrounds",kc['cutout']),("Maps, cards, diagrams, white cutaways (incl. 5 chapter cards)",kc['card'])]
tot=N
mix="\n".join(f"| {a} | {b} | {100*b/tot:.0f}% |" for a,b in mixrows)
OV={'NBG01':'Cave on a sea cliff with laurels, a stone-and-timber yard wall, sheep and goats; overcast daylight; no characters. Cutout background for shot 17',
'NBG02':'Cave interior: cheese racks, lamb pens, daylight from the entrance; no characters. Cutout background',
'NBG03':'Night hillside under a low moon, a glowing cave mouth, clear ground band; no characters. Cutout background (dark silhouettes)',
'NBG04':'Calm clear dawn sea, low horizon, empty; no characters. Cutout background for the ship and Odysseus cutouts',
'NBG05':'Etna smoking at night, caves at its foot, volcanic glow; no characters. Also a cutout background',
'NBG06':'Aeolian island crater with a glowing vent and smoke plume (graded again for a daylight version); no characters',
'NBG07':'Massive cyclopean wall of unworked boulders, raking dawn sun; no characters. Also a cutout background (Odysseus for scale)',
'NBG08':'Mycenae Lion Gate with the two-lion relief, cool morning; no characters',
'NBG09':'Basalt sea stacks off a coast, bright overcast; no characters',
'NP01':'Flat-ink dwarf elephant, side view, on white, cutout-ready; proportions simplified (also scaled to 4 m for the scale chart)',
'NP02':'Flat-ink shipwright auger boring a plank; prop on white',
'NP03':'Flat-ink axe head quenched in a water trough with steam; prop on white',
'NP04':'Flat-ink Greek ship, side view, oars, plain hull with no eye symbol; transparent cutout'}
spec_rows=lambda lst: "\n".join(f"| {i} | {RISK[i]} | {', '.join(str(x) for x in ids[i])} | {cell(OV.get(i) or short_spec(i))} |" for i in lst)
reuse_rows="\n".join(f"| {k} | {', '.join(str(x) for x in v)} |" for k,v in sorted(reuse.items()))
costlo=flat_calls*0.10; costhi=flat_calls*0.15
rwlo=rw_calls*0.10; rwhi=rw_calls*0.15
shotlist=f"""# SHOTLIST-V1.md: video 1, "The Cyclops Was Real? What the Myth Is Hiding"

Nothing generated, uploaded or sent. Generated from `video1/beats.py` (same table as SCRIPT-V1.md). Labels: **[E]** my estimate, **[M]** measured from the stress-test files.

## Summary
- **{N} shots** ({N-5} narrated plus 5 silent chapter cards), narration {words:,} words, cut about {fmt(total)} [E]. Average narrated shot {(total-12.5)/(N-5):.1f} s; lines of 16 words or more are split into an A/B pair (second crop or state of the same image, hard cut at the phrase break). Shots under 3.5 s are deliberate short beats (one-line sentences); the rhythm matters more than a flat average.
- **Mix actually used versus the recommended mix** (`PIPELINE-RECOMMENDATION.md`: about 45% baked, 20% cutouts, 5% crew as extras, 30% maps and cards):

| Shot type | Shots | Share |
|---|---|---|
{mix}

  - Baked is a little above target because crops of one baked scene are free and look better than cutouts (William's blind pick), so I used crops instead of cutouts wherever there was no crew or group moment. Cutouts are 7%, below the 20% target, and kept for crew, group and ship moments, where baked scenes are weakest. Cards and maps are above target (44% vs 30%) because this is an evidence video: every sourced claim gets a ledger card or a quote overlay. {nover} of the baked shots carry a quote or label overlay (counted as baked), so there is picture under the text. If the Editor finds the cards too dense, the cheapest fix is to turn the ledger rows in chapter 2 into cutout beats, not to add generation.
  - Crew appear as small extras or cutouts in about {sum(1 for s in shots if 'extras' in s['chars'] or 'crew' in s['chars'].lower())} shots (about {100*sum(1 for s in shots if 'extras' in s['chars'] or 'crew' in s['chars'].lower())/N:.0f}%). No baked crew-centred scene is requested. The six crew-centred first attempts that failed (stress and crew tests) are why.
- **Motion rules (Editor's v2 review):** push-in 1.00 to 1.06 on baked shots, hold on cards, one move per shot (never zoom plus pan), same zoom for background and characters, no shake (one optional 1.03 zoom punch on the boulder splash, shot with NB18), no bounce, no entrance overshoot, hard cuts with an 8-12 frame dissolve only where noted. One serif or condensed type family, thin stroke, no impact words, no reaction marks. Real recorded foley for stone and sea, no pops or dings.
- **Violence handling (ad suitability):** the eating is a silhouette and a tally card, the blinding is a glowing stake in the dark with the giant a dark mass, and the eye is never shown injured in close-up. The similes (shipwright's auger, smith's axe) are white prop cutaways.
- **Poseidon:** named in narration, not shown. One optional shot is flagged at shot with "prays to Poseidon" (`pos_v2a`, never tested in scenes).

## Shot list
{body}

## New art needed
{new_total} new images are needed in total: **{len(nb)} baked scenes (NB), {len(nbg)} empty-stage backgrounds (NBG, {len(cut_bgs)} double as cutout backgrounds: {', '.join(cut_bgs)}) and {len(npp)} props or sprites (NP)**. Drift risk H, M, L is my judgement from the stress-test failure modes (eye count on tilted or occluded faces, style drift in groups and dark close-ups, prop leakage, skull anatomy).

### Baked scenes (NB)
| id | risk | used in shots | cast, light, spec |
|---|---|---|---|
{spec_rows(nb)}

### Empty-stage backgrounds (NBG)
| id | risk | used in shots | spec |
|---|---|---|---|
{spec_rows(nbg)}

### Props and sprites (NP)
| id | risk | used in shots | spec |
|---|---|---|---|
{spec_rows(npp)}

## Cost estimate
- **Generation calls needed: {flat_calls}** with the brief's flat 30% reject allowance ({new_total} accepted images / 0.7). At $0.10-0.15 per call that is **${costlo:.2f}-${costhi:.2f}**.
- **Risk-weighted check:** {cnt['H']} high-risk images at 2.0 attempts each, {cnt['M']} medium at 1.43, {cnt['L']} low at 1.18 gives **{rw_calls:.0f} calls, ${rwlo:.2f}-${rwhi:.2f}**. The two methods agree.
- {flat_calls} sits at the bottom of the 55-70 target because the list counts only shots that truly need generation: {sum(1 for s in shots if s['kind']=='bakedX')} shots are crops or overlays of an existing image and {sum(1 for s in shots if s['kind']=='bakedR')} reuse an accepted slot. Budget: expected {flat_calls} calls (${flat_calls*0.10:.2f}-${flat_calls*0.15:.2f}); with a margin of 8 for the thumbnail frame and a second pass on the hardest images, {flat_calls+8} calls (${(flat_calls+8)*0.10:.2f}-${(flat_calls+8)*0.15:.2f}); hard cap 70 calls ($7.00-$10.50).
- Not counted: review time (the real cost; unmeasured) and the code-built items below.

## Reuse from `tests/stress_test/` (accepted slots)
| existing image | used in shots |
|---|---|
{reuse_rows}

- **Reused as is: slots 07, 08, 09, 10** (Odysseus-only, all passed; face large and readable in 07, 09, 10; slot 08 is a wide where the face is not needed) **and the cy_v4 validation scenes `cy_v4_s02` (RC02) and `cy_v4_s11` (RC11)**, which replace old slots 02 and 11.
- **Not reused although they passed: slots 01, 02, 04, 05b, 11, 13.** They were drawn with `cy_v2b` (orange-tan skin, brass bells on the belt in 01, 02, 04, 05, 11; a pouch in 13). Mixed with cy_v4 scenes the Cyclops would visibly change skin tone and belt between shots [M, seen in `cyclops_v4_check.jpg`]. NB08, NB10, NB14 and NB16 regenerate their moments with cy_v4. Slot 13 (milking) is not needed in this script.
- **Not reused, failed:** 03, 06, 12b, 14c, 15, 16.
- Slot 07 is used once (an A/B pair of crops, {', '.join(str(x) for x in reuse['RS07'])}); slot 08 appears twice ({', '.join(str(x) for x in reuse['RS08'])}); cy_v4 scene RC02 appears {len(reuse['RC02'])} times as full frame, crop or panel. If the Editor finds that repetitive, swap the second slot 08 use for a cutout.

## Built in code (no image cost)
- **Maps (6):** Mediterranean base (Natural Earth, public domain), dwarf-elephant islands, Etna and the Aeolian islands, Argolid (Mycenae, Tiryns, Argos), east Sicily with Aci Trezza, world folktale markers (regions only).
- **Diagrams (about 12):** the skull plate (DG-01, used 7 times), skull-versus-eye split, 22-wagon count, six-mark tally, wine-to-water 1:20, elephant scale chart, the two "which came first" arrows, world pair, three-row ledger, shepherd-versus-smith split, three-column and four-panel montages.
- **Ledger and typographic cards (about 25):** one parchment ledger component (ruled columns, ticks, stamp: UNVERIFIED, HYPOTHESIS, SUSPECT) reused with different rows, plus name cards, quote cards and the 5 chapter cards.
- **Overlays:** lower-third quote component (Hesiod, Thucydides x2, Pausanias, Mayor, Abel paraphrase), Greek-word overlay (Οὖτις, ὀφθαλμῷ), measuring rod.
- **Non-generated pictures to source:** the skull plate and the Abel title page. Candidates: Abel's own figure from the 1914 book (published before 1930, so probably public domain in the US [E]) or a licensed museum photograph of a *Palaeoloxodon falconeri* skull. I have not fetched or checked either scan or licence. **Do not generate the skull plate**: image models draw skull anatomy loosely and this plate carries the argument.

## Assets with drift risk (flag list)
1. **Cyclops eye count** on tilted, occluded or hand-covered faces: NB09 (drinking), NB12 (shouting, hand over the eye), NB16 (head to the ram), NB24 (face crop). Prompt must say "exactly one eye; no other eye visible". Old slot 03 and 12 failed this way [M].
2. **Style drift to painterly** in dark close-ups and groups: NB05, NB10, NB11, NB12, NB18, NB22. Always include the flat-ink clause and use an accepted flat-ink scene as the style anchor [M].
3. **Group scenes** (NB02 listeners, NB05 cowering men, NB18 crew, NBG03 silhouette Cyclopes): keep every extra as a silhouette or tiny figure. The crew method is unproven (0/7) [M].
4. **cy_v4 specifics:** skin reads khaki-to-green and the eye is smaller than cy_v2b's [M, 2 scenes]; the ref has no club, so NB06 needs the club described in the prompt. The smith (NB22) intentionally shows the same face in a new job; the Editor should confirm that is not read as an error.
5. **Skull anatomy** (NB19, and any generated skull): models add two sockets or distort the nasal opening. Keep it small and partial in NB19 and use the real plate for every explanatory shot.
6. **Ship (NP04, NB18):** the earlier hull drew an eye symbol that read as Eye of Horus, and cutout ships had matte residue [M, Editor]. Write "plain hull, no symbol"; clean the matte.
7. **Stake that looks like a sword** (NB07, NB11; slot 09 already does) [M]: describe "a long pole, sharpened and charred, taller than the man".
8. **Odysseus too small in wide shots:** only RS08 and NB18 are wide; neither needs his face.
9. **Cutout pose availability:** the refusing/explaining pose, small crew cutouts and a standing cy_v4 are assumed to exist in the pose sheets; confirm before building. Any missing pose is a new generation.
10. **Lion Gate relief** (NBG08) and **cyclopean wall** (NBG07): models tend to neaten the stonework; the point is unworked boulders.
11. **Poseidon** (optional): `pos_v2a` untested in scenes.

## Open decisions for William
1. Show Poseidon on screen (one silhouette shot) or keep him as a name only (current plan)?
2. Keep the Hesiod smith strand (about {hes_len:.0f} s of narration, two baked scenes) or cut it to a single line? It carries the "same name, different job" point and the "one eye, plainly stated" source.
3. Accept cards at 44%, or ask for more cutout beats in chapter 2?
4. Is 10:30-11:00 acceptable, or trim to 10:00 using the list at the end of the script?
"""
open(OUT+'SHOTLIST-V1.md','w').write(shotlist)
print('ok',len(script.split()),len(shotlist.split()))
