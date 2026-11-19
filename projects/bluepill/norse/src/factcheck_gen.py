import json
P='/home/williamdownard/.openclaw/workspace/projects/bluepill/norse/'
c1=json.load(open(P+'src/parsed.json')); c2=json.load(open(P+'src/parsed2.json'))
b1=[b for c in c1 for b in c['beats']]; b2=[b for c in c2 for b in c['beats']]
chap=[]; 
for c in c2: chap+= [c['title']]*len(c['beats'])
N=len(b1)
LOC=set([5,10,31,35,48,120]+list(range(81,94)))
FIX=set()
V={i:'PASS' for i in range(1,N+1)}
note={}
def n(i,t,v=None):
    note[i]=t
    if v: V[i]=v
# FIX beats: (note)
fx={
2:"Overreach: 'every one of them is doomed' is contradicted by Gylf LII (Gimle, Brimir and Sindri halls stand after the fire) and by the script's own rebirth chapter. Sourced replacement: Surt 'burn[s] all the world' (Gylf IV, LI), Voluspa 57 fire against heaven.",
3:"The gods as a group are not told the prophecy in the poem; the seeress speaks to Odin (Voluspa 1 addresses Valfather, 28-30 Odin consults her). Shot already shows Odin alone.",
4:"As beat 3.",
33:"'A day's work' implies a duration no source gives. Three brothers made the world (Gylf VI-VIII).",
47:"Brodeur does not call Mimir a giant; he 'keeps the well' under the root toward the Rime-Giants (Gylf XV). Eye laid in pledge for one drink: Gylf XV, Voluspa 29.",
67:"'Weave' is not in the text: Gylf XXXIV says dwarves made the fetter Gleipnir, 'soft and smooth as a silken ribbon' (so beat 70 stands).",
68:"Source is the 'noise a cat makes in foot-fall', a sound, not a print. Shot changed from a paw print to sound-lines.",
80:"Red beard is in neither Brodeur nor Bellows (searched both texts: the only beard is Thrymskvitha 'he shook his beard'). Dropped from the narration; kept as a visual design choice only.",
121:"The gods do not go to Hel's gate. Hermod, Odin's son, rides Sleipnir to Hel and begs; Hel sets the condition (Gylf XLIX). Odin and Thor kneeling was invented. State and shot changed (a hooded rider; Hermod unnamed so no new card).",
141:"Brodeur: 'the Sons of Muspell ride'; Surt leads, sword brighter than the sun. They are not called giants in Gylf LI or Voluspa 52.",
144:"'Whole' is not in the text: 'The Wolf shall swallow Odin' (Gylf LI).",
146:"Gylf LI: Vidar seizes the upper jaw and 'tears his gullet asunder'. 'It' was ambiguous (jaw or wolf). Voluspa 54 differs (sword to the heart): the script follows Snorri and does not state the other.",
151:"Gylf LI: Surt 'cast fire over the earth and burn all the world'. 'Every world' overreaches (Gimle survives, Gylf LII).",
163:"Overstates: Bellows (Voluspa introductory note) puts about 200 years between composition and first writing for that poem, but the claim about 'the people who first told it' is not sourced for the whole corpus. Reworded to the safe claim.",
164:"'Long winter nights' unsourced, dropped. 'Recited from memory' is the standard account; supported only in general terms (Bellows intro). Marked unverifiable detail in section 4.",
165:"'The poems survive in one great book' is wrong: Bellows intro lists AM 748 (six poems plus Baldrs draumar), the Hauksbok Voluspa and others elsewhere. Wikipedia: Regius is 'the sole source for most of the poems it contains'. Date: 'thought to have been written during the 1270s' (Wikipedia, Codex Regius); Bellows gives only 'a hundred years or so' after a mid/late-12th-century collection.",
167:"Wikipedia, Prose Edda: 'to some extent written, or at least compiled, by Snorri c. 1220'; attribution is the standard one (Brodeur treats it as Snorri's) but hedged by modern sources. 'Icelandic' added so the reader places him.",
169:"Brodeur's Prologue opens 'In the beginning God created heaven and earth... Adam and Eve'; the Asia/Troy passage follows. Brodeur's intro: many scholars consider the Prologue spurious (not Snorri's). 'He begins by saying' was wrong.",
}
for i,t in fx.items(): FIX.add(i); V[i]='FIX'; note[i]=t
for i in LOC: V[i]='PASS (locator fixed)'
loc_notes={5:"Voluspa 28 is Odin sought by the seeress; the eye is in 29.",10:"Voluspa 47-52 was too narrow; the destruction is 45-57.",31:"Grimnismal 41 is Midgard from the brows and the clouds. Skull as sky is Grimnismal 40; the four dwarfs are Gylf VIII only.",35:"Voluspa 17 says 'two without fate', no trees; the trees are Gylf IX only.",48:"One eye is Voluspa 29, not 28. Broad hat: Sidhottr 'With Broad Hat', Odin's name in Grimnismal 48.",120:"Voluspa 31 is the Valkyries; Baldr and the mistletoe are 32, Hod's shaft 33."}
for i,t in loc_notes.items(): note[i]=t
for i in range(81,94): note[i]="Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported."
pn={1:"Voluspa 2: 'the nine in the tree'. Gylf does not say the nine worlds hang from the tree (Poetic only, no conflict).",
6:"Colour: the gods do not avert the end (Gylf XXXIV chain Fenrir; Voluspa 45-57).",
9:"Colour, no claim.",12:"Colour, no claim.",
25:"Gylf VIII 'bore him into the middle of the Yawning Void'; 'drag' is the shot's rope image only.",
26:"As 25.",
32:"Gylf VIII sparks and embers from Muspellheim set in the sky; sun and moon are made from them in Gylf XI. 'Stars' is the poem's list (Voluspa 5).",
34:"Glue line, no claim.",
40:"Gylf IX: Asgard 'in the middle of the world'; Gylf XV: the gods ride 'up over Bifrost'. 'Above' is fair.",
43:"Gylf XV: roots among the Aesir (in heaven), among the Rime-Giants, over Niflheim; Hel's realm is the land of the dead.",
44:"Gylf XVI: the eagle 'sits in the limbs of the Ash'; 'at the top' is the picture, Grimnismal 32 has the eagle above.",
46:"Gylf XVI: Ratatosk bears 'envious words' between eagle and Nidhogg; 'insults' fair.",
51:"Gylf XXXIII: 'beautiful and comely to look upon, evil in spirit, very fickle'. 'Charming' is colour on 'sleight' and 'artifices'.",
60:"Gylf XXXIV: Hel gets Niflheim and 'power over nine worlds' over those who die of sickness or old age. 'Land of the dead' is a fair compression.",
64:"Gylf XXXIV names 'the Aesir' only. Odin and Thor in the shot are our casting; the spoken line is safe.",
65:"Gylf XXXIV: the first fetter Laedingr 'broke'; 'thread' is a simile. Dromi: 'stronger by half'.",
69:"Brodeur: 'roots of a rock'; Bellows note on Voluspa 39 quotes 'roots of mountains'. Either is acceptable.",
73:"Gylf XXXIV: 'Each of the Aesir looked at his neighbor'. The question is our beat.",
78:"Gylf XXXIV says only 'he lost his hand'; the wolf biting it off is the plain reading and Lokasenna 38 has Tyr 'lost my hand' to Hrothvitnir (Fenrir).",
88:"Gylf XLVIII: Hymir 'sore afraid' at the far rowing; he 'grew pale, became yellow' only on seeing the serpent. Order is a compression, claim stands.",
99:"Gylf XLVIII: 'men say he struck off its head... I think the Midgard Serpent yet lives'. Script follows Snorri's own view (needed for Ragnarok) and does not state the other.",
101:"Colour/foreshadow: Gylf XLVII ends with Thor resolving to seek the serpent; kill at Ragnarok Gylf LI, Voluspa 55-56.",
105:"Gylf XLIX: 'the Aesir took counsel' then 'Frigg took oaths'. Frigg as Baldr's mother is standard; Voluspa 53 'joy of Frigg' is Odin, not used.",
107:"Gylf XLIX list: fire, water, iron and metal, stones, earth, trees, sicknesses, beasts, birds, venom, serpents. The spoken list is a true selection.",
109:"Gylf XLIX: 'a diversion of Baldr's and the Aesir'. 'So relieved' is colour. Loki is not at the game in the text until he sees it; shot ok.",
118:"Gylf XLIX: Loki says 'I will direct thee where he stands; shoot at him with this wand'. 'Puts it in his hand' is the plain action.",
125:"Gylf XLIX: 'men deem that she who was there was Loki'.",
126:"Gylf XLIX has the burning (ship Hringhorni, Nanna dies) before Hermod's ride; shot is a flash-forward, line is safe.",
134:"Gylf LI: three winters of battles come first, then the Awful Winter. 'Begins with a winter' fair.",
136:"Gylf LI: one wolf 'shall swallow the sun', the other 'seize the moon'. Voluspa 57: the sun turns black. Script follows Snorri.",
140:"Gylf LI: Naglfar steered by Hrym. Voluspa 51: Loki at the helm of a ship. Script names neither (no conflict stated).",
145:"Gylf LI: one foot on the lower jaw, the shoe made of leather scraps. Voluspa 54: sword to the heart (not stated).",
150:"Gylf LI: Loki and Heimdall each the other's slayer. 'Free at last' is colour on 'all fetters... broken' (Gylf LI).",
154:"Colour/transition; earth emerges: Gylf LIII, Voluspa 59.",
157:"Gylf LIII: Vidar and Vali live; Modi and Magni 'shall have Mjollnir'. 'Carry' is the picture of 'have'.",
159:"Gylf LIII: Lif and Lifthrasir hidden in Hoddmimir's Holt (a wood); 'step out' is implied by the repeopling.",
153:"Colour, no claim.",116:"Question beat, no claim.",162:"Question beat, no claim.",
170:"Framing: two real disagreements are named in beat 171 only.",
171:"Voluspa 18: Odin, Hoenir, Lothur give soul, sense, heat and hue. Gylf IX: Odin, Vili, Ve. True as worded; the script then picks Snorri (beat 172).",
172:"Editorial rule, no claim.",
174:"Recap, no claim.",175:"Closing line, true of the Eddic texts.",
166:"Iceland legally Christian in 1000 (Wikipedia). 'By Christians': the 13th-century scribe is unnamed, but the whole context is Christian Iceland.",
168:"No single sentence in the texts read says 'Snorri was a Christian'; Brodeur's intro and the Prologue (Adam and Eve) establish it.",
173:"Date, king and order confirmed (Brodeur intro; Wikipedia: Hakon's secret letter ordered him killed or captured; he was killed in the cellar at Reykholt). Shot is a dramatisation (study doorway, not the cellar): visual only.",
13:"Colour.",
}
for i,t in pn.items():
    if V[i]=='PASS':
        V[i]='PASS (colour)' if t.startswith(('Colour','Question','Glue','Recap','Closing','Editorial','Framing')) else 'PASS (note)'
    note.setdefault(i,t)
for i in (2,3,4): pass
cnt={}
for v in V.values():
    k=v.split(' (')[0]; cnt[k]=cnt.get(k,0)+1
sub={}
for v in V.values(): sub[v]=sub.get(v,0)+1
out=[]
out.append("# FACTCHECK-N.md: fact-check of SCRIPT-N-draft1 (Norse, The Myth Ledger video 2)\n")
out.append("Checked 2026-11-14 by a Sonnet subagent against `norse/BRIEF-FACTCHECK.md`. Read: SCRIPT-N-draft1.md, SCRIPT-N-NOTES.md, video2/FACTCHECK-V5.md (format). Nothing outside `norse/` changed; no spend, no images. Output: this file and `SCRIPT-N-draft2.md` (all FIXes applied; scratch scripts `norse/src/apply_fixes.py`, `gen2.py`, `factcheck_gen.py`; beat file `norse/src/beats2.txt`).\n")
out.append("## Counts\n")
out.append(f"- **PASS {cnt['PASS']}** (of which {sub.get('PASS (locator fixed)',0)} had a wrong locator corrected, {sub.get('PASS (note)',0)} carry a caveat, {sub.get('PASS (colour)',0)} are colour/framing with no claim, {sub.get('PASS',0)} clean), **FIX {cnt['FIX']}**, **CUT {cnt.get('CUT',0)}**; {N} beats checked. One further change: beat 122's shot/state moved with beat 121 (spoken line unchanged, counted PASS).")
out.append("- Draft 2 spoken words: **1,507** (draft 1: 1,495; brief 1,450-1,650). 139 sentences, 175 beats, beat ids unchanged. Raw voice time 10:03 at 150 wpm (3 s over the 10:00 note target; trim one line if it matters).")
out.append("- Where the Poetic and Prose Eddas disagree, the script follows Snorri (Gylfaginning) and states the other only once, as a disagreement (beats 170-172). See section 3.\n")
out.append("## 1. Sources and how they were read\n")
out.append("- **Bellows 1923, The Poetic Edda** (archive.org `poeticedda00belluoft`, OCR): Voluspa read in full with Bellows's notes; Grimnismol 32, 40-41, 46-48; Vafthrudnismol 21; Lokasenna 38-39, 49-50 and notes; Bellows general introduction (Codex Regius, AM 748, Hauksbok). Hymiskvitha and Baldrs draumar located, not relied on.")
out.append("- **Brodeur 1916, The Prose Edda** (archive.org `proseedda00snor`, OCR): Gylfaginning chapters IV-IX, XIII-XVI, XXI-XXII, XXVII, XXXIII-XXXIV, XLVII-LIII read in full; Prologue opening; Brodeur's introduction (Snorri's death, Prologue authorship). Anderson's Gutenberg texts were fetched but not used.")
out.append("- **Modern sources (Wikipedia, via web_fetch/curl):** Codex Regius (written 1270s, sole source for most of its poems), Snorri Sturluson (1179 - 23 September 1241), Prose Edda (c. 1220), Christianization of Iceland (legally Christian in 1000). sacred-texts.com is blocked by Cloudflare from this host; Wikisource not needed. Web content treated as untrusted data; downloads kept in `/tmp/norse`, not the workspace.")
out.append("- **Locator convention.** Brodeur numbers Gylfaginning by Roman chapter, so `Gylf 34` = Brodeur XXXIV (the Faulkes numbering used elsewhere agrees for 34 and 49-51 but not for the early chapters). Bellows numbers stanzas inside each poem. Draft 1's Gylf locators were almost all right; the wrong ones are listed in section 2.\n")
out.append("## 2. Locators corrected (draft 1 `trace:` lines written from memory)\n")
out.append("| Beat(s) | Draft 1 said | Correct | Why |\n|---|---|---|---|")
rows=[("002","Voluspa 45-66","Voluspa 45-57 (destruction); 59-66 is the new world","Whole stanza range included the rebirth"),
("004","Voluspa 1","Voluspa 1, 28-30","Stanza 1 is the seeress asking a hearing; Odin consults her at 28-30"),
("005, 047","Voluspa 28","Voluspa 28-29","Eye in Mimir's well is stanza 29"),
("010","Voluspa 47-52","Voluspa 45-57","Fuller span"),
("031","Grimnismal 41","Grimnismal 40 (skull as sky); Gylf VIII (four dwarfs)","41 is the brows and the brain; the dwarfs are prose only"),
("035","Voluspa 17 'trees without fate'","Gylf IX for the trees; Voluspa 17 has no trees","Bellows 17: 'Two without fate on the land they found'"),
("048","Voluspa 28 (one eye)","Voluspa 29; hat = Grimnismal 48 (Sidhottr)","Hat now sourced"),
("081-093","Gylf 47","Gylf 48","Gylf XLVII ends the Utgard-Loki story; the fishing trip is XLVIII"),
("120","Voluspa 31-33","Voluspa 32-33","31 is the Valkyries"),
("all others","Gylf 4-9, 13, 15, 16, 21, 22, 33, 34, 49, 50, 51, 53; Voluspa 2, 3, 17, 18, 19, 59, 62; Grimnismal 40","correct as written","checked against the text")]
for r in rows: out.append("| "+" | ".join(r)+" |")
out.append("\n## 3. Poetic vs Prose disagreements and the pick (brief rule)\n")
out.append("| Point | Poetic Edda (Bellows) | Prose Edda (Brodeur) | Script |\n|---|---|---|---|")
for r in [
("Who made the first people","Voluspa 17-18: Odin, Hoenir, Lothur give soul, sense, heat and hue; two 'without fate', not trees","Gylf IX: sons of Borr (Odin, Vili, Ve) shape two trees; spirit and life / wit and feeling / form, speech, hearing, sight","Snorri; beat 38 'Odin gives them breath' is true of both; beats 171-172 name the difference once, as a difference"),
("Loki's binding","Voluspa 35: bound 'in the wet woods', Sigyn by him; Lokasenna prose: bowels of son Vali, Narfi made a wolf","Gylf L: cave, three stones, Narfi's entrails, serpent from Skadi, Sigyn's bowl; Vali the wolf","Snorri. Beats 128-133 use stones, serpent, Sigyn, earthquake and none of the sons. (Correction to NOTES: the Lokasenna prose is the Vali-bowels version, not Snorri's Narfi version.)"),
("Fenrir's killer","Voluspa 54: Vidar thrusts a sword to the heart","Gylf LI: one foot on the lower jaw, tears the gullet","Snorri (beats 145-146)"),
("Ship at Ragnarok","Voluspa 50: Hrym steers Naglfar from the east; 51: Loki steers a ship of Hel's people","Gylf LI: Hrym steers Naglfar; the verse quotes both","Neither named (beat 140)"),
("Who swallows the sun/Odin","Voluspa 40-41, 57: wolf steals the sun, it turns black; Odin fights the wolf (53)","Gylf LI: wolf swallows the sun and Odin","Snorri (beats 136, 144)"),
("Thor and the serpent","Hymiskvitha (not read in full): quest for a cauldron, Tyr as Hymir's son","Gylf XLVIII: Thor alone, disguised, Hymir cuts the line; serpent lives","Snorri; cauldron and Tyr-as-son not used. Beat 99 does not say the head was struck off"),
("After the fire","Voluspa 62-64: Baldr and Hoth return; Gimle hall of gold","Gylf LII: Gimle, Brimir, Sindri halls; LIII: earth green, Vidar, Vali, Modi, Magni, Baldr, Hod, Lif and Lifthrasir","Consistent; beat 2 changed so 'every world doomed' no longer contradicts it")]:
    out.append("| "+" | ".join(r)+" |")
out.append("\n## 4. Specific checks you asked for\n")
for t in [
"**Codex Regius c. 1270s: PASS.** Wikipedia: 'thought to have been written during the 1270s', GKS 2365 4to. Bellows (1923) is vaguer ('a copy made a hundred years or so later' than a mid/late-12th-century collection). 'About twelve seventy' stands. The line wrongly said 'one great book' (beat 165, FIX).",
"**Snorri b. 1179, d. 1241: PASS.** Wikipedia 1179 - 23 September 1241; Brodeur intro 1241. The script only voices 1241. Killed by Gizurr Thorvaldsson, 'at the express order of the King' Hakon Hakonarson (Brodeur); Wikipedia: Hakon sent a secret letter ordering him killed or captured. 'On the orders of a Norwegian king' holds.",
"**Prose Edda c. 1220: PASS (hedged).** Wikipedia: 'to some extent written, or at least compiled, by Snorri c. 1220'. Beat 167 reworded to 'put together'. Not checkable more exactly: no precise year is fixed.",
"**Oral tradition (beats 163-164): FIX.** Bellows supports a gap between composition and writing for Voluspa (about 200 years) and for a written 12th-century collection; nothing in the two Eddas says 'the people who first told it' never wrote. Reworded to a safe claim. 'Winter nights' dropped. The oral-tradition account is standard scholarship, not an Edda statement.",
"**Tyr and Fenrir (7, 8, 61-79): PASS.** Gylf XXXIV: only Tyr dared feed him; Laedingr, Dromi, Gleipnir (six things); Tyr's right hand in the mouth; 'all laughed except Tyr: he lost his hand'; sword gag; bound till the Weird of the Gods. FIX only for 'weave' (67) and the cat's step (68).",
"**Thor and Jormungandr (80-101, 147-148): PASS after FIX 80.** Gylf XLVIII fully matches (disguise as a lad, Hymir, Himinbrjotr's head, rowing further, feet through the boat, Hymir cuts the line, Hymir knocked overboard). Ragnarok: Thor kills the serpent, nine paces, dies of venom (Gylf LI, Voluspa 55-56).",
"**Baldr and the mistletoe (102-126): PASS after FIX 121.** Oaths from all things but the sprout west of Valhall; Loki as a woman at Fensalir; Hod blind and weaponless at the edge; Loki directs; shaft goes through Baldr (Gylf XLIX). Thokk may be Loki.",
"**Loki's punishment (127-133): PASS.** Salmon at Franangr Falls, net, Thor holds the tail, cave, three stones, serpent, Sigyn's basin, earthquakes, bound till the Weird of the Gods (Gylf L).",
"**Ragnarok (134-153): PASS after FIX 141, 144, 146, 151 (and 2).** Three winters with no summer; wolves; stars vanish; all fetters break; Naglfar of dead men's nails; Surt; Heimdall's horn; Odin v. wolf, Vidar, Thor and serpent, Tyr and Garm, Heimdall and Loki (Gylf LI). Freyr and Surt omitted, fine.",
"**'Sources disagree' (170-172): PASS.** Voluspa 17-18 vs Gylf IX is a real disagreement and is the only one voiced.",
"**Numbers:** nine worlds (Voluspa 2) PASS; three days Buri (Gylf VI) PASS; three sons of Borr PASS; four dwarfs PASS; six things Gleipnir PASS; three roots PASS; three children PASS; three stones PASS; three winters PASS; nine steps (Voluspa 56, Gylf LI) PASS. Dates: twelve seventy, twelve twenty, twelve forty-one PASS (see above)."]:
    out.append("- "+t)
out.append("\n## 5. Beat table (all 175)\n")
out.append("Verdict key: PASS; PASS (note) supported with a caveat; PASS (colour) no factual claim; PASS (locator fixed) claim right, `trace:` corrected; FIX spoken line rewritten in draft 2; CUT none. Source/locator column is the corrected draft 2 `trace:` (V = read in the text).\n")
out.append("| Beat | Verdict | Spoken (draft 2) | Source / locator | Note |\n|---|---|---|---|---|")
for i in range(1,N+1):
    t2=b2[i-1]['text']; tr=b2[i-1]['trace']
    if V[i]=='FIX': sp=f"{b1[i-1]['text']} -> **{t2}**"
    else: sp=t2
    out.append(f"| N-{i:03d} | {V[i]} | {sp.replace('|','/')} | {tr.replace('|','/')} | {note.get(i,'')} |")
out.append("\n## 6. Beats I am unsure about\n")
for t in [
"**N-040 'Above it, the gods build their own home, Asgard'**: Gylf IX puts Asgard 'in the middle of the world'; Gylf XV has the gods ride 'up over Bifrost' to the well in heaven, and Gylf XXII puts Breidablik 'in heaven'. 'Above' is the common reading; left PASS (note).",
"**N-044 'An eagle sits at the top'**: Gylf XVI says 'in the limbs of the Ash'. Grimnismal 32 not re-read for 'above'. Harmless, left.",
"**N-165/N-167 exact dates**: Codex Regius c. 1270 and the Prose Edda c. 1220 rest on modern reference (Wikipedia), not on a second scholarly source; Bellows (1923) does not give 1270. Unverified beyond one reference source each.",
"**N-168 'Snorri was a Christian too'**: no sentence says it in the texts read; inferred from Brodeur's intro and the Christian Prologue. Near certain, not quotable.",
"**N-173 shot**: Snorri was killed in the cellar at Reykholt (Wikipedia: 'He fled to the cellar'); the shot shows a study doorway. Visual only; change if the shot is regenerated.",
"**N-064, N-073 shots**: Thor is not named in the Fenrir binding (Gylf says 'the Aesir'); Odin and Thor in the shot are our casting, not a source claim.",
"**N-080 'god of thunder'**: standard description; Gylf XXI uses Oku-Thor ('chariot Thor') and 'strongest of all gods and men'. Brodeur's Skaldskaparmal has 'Thunderer' as a kenning. Kept.",
"**Hymiskvitha, Baldrs draumar, Vafthrudnismol 44**: located in Bellows, not read in full; no beat depends on them (traces cite Baldrs draumar for N-104 only as the dream source)."]:
    out.append("- "+t)
out.append("\n## 7. Unverifiable items\n")
out.append("- 'On long winter nights' (N-164): no source; dropped.\n- The exact scribe, place and Christian status of the Codex Regius copyist: unknown; N-166 relies on the general Christian context of 13th-century Iceland.\n- Red beard of Thor: not in either text; visual only.\n- Exact year 1220 for the Prose Edda: a convention, not a recorded date.")
open(P+'FACTCHECK-N.md','w').write('\n'.join(out))
print(cnt,sub)
