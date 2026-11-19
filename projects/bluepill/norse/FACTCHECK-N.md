# FACTCHECK-N.md: fact-check of SCRIPT-N-draft1 (Norse, The Myth Ledger video 2)

Checked 2026-11-14 by a Sonnet subagent against `norse/BRIEF-FACTCHECK.md`. Read: SCRIPT-N-draft1.md, SCRIPT-N-NOTES.md, video2/FACTCHECK-V5.md (format). Nothing outside `norse/` changed; no spend, no images. Output: this file and `SCRIPT-N-draft2.md` (all FIXes applied; scratch scripts `norse/src/apply_fixes.py`, `gen2.py`, `factcheck_gen.py`; beat file `norse/src/beats2.txt`).

## Counts

- **PASS 157** (of which 19 had a wrong locator corrected, 33 carry a caveat, 14 are colour/framing with no claim, 91 clean), **FIX 18**, **CUT 0**; 175 beats checked. One further change: beat 122's shot/state moved with beat 121 (spoken line unchanged, counted PASS).
- Draft 2 spoken words: **1,507** (draft 1: 1,495; brief 1,450-1,650). 139 sentences, 175 beats, beat ids unchanged. Raw voice time 10:03 at 150 wpm (3 s over the 10:00 note target; trim one line if it matters).
- Where the Poetic and Prose Eddas disagree, the script follows Snorri (Gylfaginning) and states the other only once, as a disagreement (beats 170-172). See section 3.

## 1. Sources and how they were read

- **Bellows 1923, The Poetic Edda** (archive.org `poeticedda00belluoft`, OCR): Voluspa read in full with Bellows's notes; Grimnismol 32, 40-41, 46-48; Vafthrudnismol 21; Lokasenna 38-39, 49-50 and notes; Bellows general introduction (Codex Regius, AM 748, Hauksbok). Hymiskvitha and Baldrs draumar located, not relied on.
- **Brodeur 1916, The Prose Edda** (archive.org `proseedda00snor`, OCR): Gylfaginning chapters IV-IX, XIII-XVI, XXI-XXII, XXVII, XXXIII-XXXIV, XLVII-LIII read in full; Prologue opening; Brodeur's introduction (Snorri's death, Prologue authorship). Anderson's Gutenberg texts were fetched but not used.
- **Modern sources (Wikipedia, via web_fetch/curl):** Codex Regius (written 1270s, sole source for most of its poems), Snorri Sturluson (1179 - 23 September 1241), Prose Edda (c. 1220), Christianization of Iceland (legally Christian in 1000). sacred-texts.com is blocked by Cloudflare from this host; Wikisource not needed. Web content treated as untrusted data; downloads kept in `/tmp/norse`, not the workspace.
- **Locator convention.** Brodeur numbers Gylfaginning by Roman chapter, so `Gylf 34` = Brodeur XXXIV (the Faulkes numbering used elsewhere agrees for 34 and 49-51 but not for the early chapters). Bellows numbers stanzas inside each poem. Draft 1's Gylf locators were almost all right; the wrong ones are listed in section 2.

## 2. Locators corrected (draft 1 `trace:` lines written from memory)

| Beat(s) | Draft 1 said | Correct | Why |
|---|---|---|---|
| 002 | Voluspa 45-66 | Voluspa 45-57 (destruction); 59-66 is the new world | Whole stanza range included the rebirth |
| 004 | Voluspa 1 | Voluspa 1, 28-30 | Stanza 1 is the seeress asking a hearing; Odin consults her at 28-30 |
| 005, 047 | Voluspa 28 | Voluspa 28-29 | Eye in Mimir's well is stanza 29 |
| 010 | Voluspa 47-52 | Voluspa 45-57 | Fuller span |
| 031 | Grimnismal 41 | Grimnismal 40 (skull as sky); Gylf VIII (four dwarfs) | 41 is the brows and the brain; the dwarfs are prose only |
| 035 | Voluspa 17 'trees without fate' | Gylf IX for the trees; Voluspa 17 has no trees | Bellows 17: 'Two without fate on the land they found' |
| 048 | Voluspa 28 (one eye) | Voluspa 29; hat = Grimnismal 48 (Sidhottr) | Hat now sourced |
| 081-093 | Gylf 47 | Gylf 48 | Gylf XLVII ends the Utgard-Loki story; the fishing trip is XLVIII |
| 120 | Voluspa 31-33 | Voluspa 32-33 | 31 is the Valkyries |
| all others | Gylf 4-9, 13, 15, 16, 21, 22, 33, 34, 49, 50, 51, 53; Voluspa 2, 3, 17, 18, 19, 59, 62; Grimnismal 40 | correct as written | checked against the text |

## 3. Poetic vs Prose disagreements and the pick (brief rule)

| Point | Poetic Edda (Bellows) | Prose Edda (Brodeur) | Script |
|---|---|---|---|
| Who made the first people | Voluspa 17-18: Odin, Hoenir, Lothur give soul, sense, heat and hue; two 'without fate', not trees | Gylf IX: sons of Borr (Odin, Vili, Ve) shape two trees; spirit and life / wit and feeling / form, speech, hearing, sight | Snorri; beat 38 'Odin gives them breath' is true of both; beats 171-172 name the difference once, as a difference |
| Loki's binding | Voluspa 35: bound 'in the wet woods', Sigyn by him; Lokasenna prose: bowels of son Vali, Narfi made a wolf | Gylf L: cave, three stones, Narfi's entrails, serpent from Skadi, Sigyn's bowl; Vali the wolf | Snorri. Beats 128-133 use stones, serpent, Sigyn, earthquake and none of the sons. (Correction to NOTES: the Lokasenna prose is the Vali-bowels version, not Snorri's Narfi version.) |
| Fenrir's killer | Voluspa 54: Vidar thrusts a sword to the heart | Gylf LI: one foot on the lower jaw, tears the gullet | Snorri (beats 145-146) |
| Ship at Ragnarok | Voluspa 50: Hrym steers Naglfar from the east; 51: Loki steers a ship of Hel's people | Gylf LI: Hrym steers Naglfar; the verse quotes both | Neither named (beat 140) |
| Who swallows the sun/Odin | Voluspa 40-41, 57: wolf steals the sun, it turns black; Odin fights the wolf (53) | Gylf LI: wolf swallows the sun and Odin | Snorri (beats 136, 144) |
| Thor and the serpent | Hymiskvitha (not read in full): quest for a cauldron, Tyr as Hymir's son | Gylf XLVIII: Thor alone, disguised, Hymir cuts the line; serpent lives | Snorri; cauldron and Tyr-as-son not used. Beat 99 does not say the head was struck off |
| After the fire | Voluspa 62-64: Baldr and Hoth return; Gimle hall of gold | Gylf LII: Gimle, Brimir, Sindri halls; LIII: earth green, Vidar, Vali, Modi, Magni, Baldr, Hod, Lif and Lifthrasir | Consistent; beat 2 changed so 'every world doomed' no longer contradicts it |

## 4. Specific checks you asked for

- **Codex Regius c. 1270s: PASS.** Wikipedia: 'thought to have been written during the 1270s', GKS 2365 4to. Bellows (1923) is vaguer ('a copy made a hundred years or so later' than a mid/late-12th-century collection). 'About twelve seventy' stands. The line wrongly said 'one great book' (beat 165, FIX).
- **Snorri b. 1179, d. 1241: PASS.** Wikipedia 1179 - 23 September 1241; Brodeur intro 1241. The script only voices 1241. Killed by Gizurr Thorvaldsson, 'at the express order of the King' Hakon Hakonarson (Brodeur); Wikipedia: Hakon sent a secret letter ordering him killed or captured. 'On the orders of a Norwegian king' holds.
- **Prose Edda c. 1220: PASS (hedged).** Wikipedia: 'to some extent written, or at least compiled, by Snorri c. 1220'. Beat 167 reworded to 'put together'. Not checkable more exactly: no precise year is fixed.
- **Oral tradition (beats 163-164): FIX.** Bellows supports a gap between composition and writing for Voluspa (about 200 years) and for a written 12th-century collection; nothing in the two Eddas says 'the people who first told it' never wrote. Reworded to a safe claim. 'Winter nights' dropped. The oral-tradition account is standard scholarship, not an Edda statement.
- **Tyr and Fenrir (7, 8, 61-79): PASS.** Gylf XXXIV: only Tyr dared feed him; Laedingr, Dromi, Gleipnir (six things); Tyr's right hand in the mouth; 'all laughed except Tyr: he lost his hand'; sword gag; bound till the Weird of the Gods. FIX only for 'weave' (67) and the cat's step (68).
- **Thor and Jormungandr (80-101, 147-148): PASS after FIX 80.** Gylf XLVIII fully matches (disguise as a lad, Hymir, Himinbrjotr's head, rowing further, feet through the boat, Hymir cuts the line, Hymir knocked overboard). Ragnarok: Thor kills the serpent, nine paces, dies of venom (Gylf LI, Voluspa 55-56).
- **Baldr and the mistletoe (102-126): PASS after FIX 121.** Oaths from all things but the sprout west of Valhall; Loki as a woman at Fensalir; Hod blind and weaponless at the edge; Loki directs; shaft goes through Baldr (Gylf XLIX). Thokk may be Loki.
- **Loki's punishment (127-133): PASS.** Salmon at Franangr Falls, net, Thor holds the tail, cave, three stones, serpent, Sigyn's basin, earthquakes, bound till the Weird of the Gods (Gylf L).
- **Ragnarok (134-153): PASS after FIX 141, 144, 146, 151 (and 2).** Three winters with no summer; wolves; stars vanish; all fetters break; Naglfar of dead men's nails; Surt; Heimdall's horn; Odin v. wolf, Vidar, Thor and serpent, Tyr and Garm, Heimdall and Loki (Gylf LI). Freyr and Surt omitted, fine.
- **'Sources disagree' (170-172): PASS.** Voluspa 17-18 vs Gylf IX is a real disagreement and is the only one voiced.
- **Numbers:** nine worlds (Voluspa 2) PASS; three days Buri (Gylf VI) PASS; three sons of Borr PASS; four dwarfs PASS; six things Gleipnir PASS; three roots PASS; three children PASS; three stones PASS; three winters PASS; nine steps (Voluspa 56, Gylf LI) PASS. Dates: twelve seventy, twelve twenty, twelve forty-one PASS (see above).

## 5. Beat table (all 175)

Verdict key: PASS; PASS (note) supported with a caveat; PASS (colour) no factual claim; PASS (locator fixed) claim right, `trace:` corrected; FIX spoken line rewritten in draft 2; CUT none. Source/locator column is the corrected draft 2 `trace:` (V = read in the text).

| Beat | Verdict | Spoken (draft 2) | Source / locator | Note |
|---|---|---|---|---|
| N-001 | PASS (note) | Nine worlds hang from one tree, | Voluspa 2 (nine worlds); Gylf 15 (Yggdrasil) V | Voluspa 2: 'the nine in the tree'. Gylf does not say the nine worlds hang from the tree (Poetic only, no conflict). |
| N-002 | FIX | and every one of them is doomed. -> **and all of it will burn.** | Voluspa 45-57 (the destruction); Gylf 4 and 51 ('burn all the world') V | Overreach: 'every one of them is doomed' is contradicted by Gylf LII (Gimle, Brimir and Sindri halls stand after the fire) and by the script's own rebirth chapter. Sourced replacement: Surt 'burn[s] all the world' (Gylf IV, LI), Voluspa 57 fire against heaven. |
| N-003 | FIX | The gods know it, -> **Odin knows it,** | (ours) framing; basis Voluspa 28-30 (Odin consults the seeress) | The gods as a group are not told the prophecy in the poem; the seeress speaks to Odin (Voluspa 1 addresses Valfather, 28-30 Odin consults her). Shot already shows Odin alone. |
| N-004 | FIX | because they have heard their own ending. -> **because a seeress told him his own ending.** | Voluspa 1, 28-30 V | As beat 3. |
| N-005 | PASS (locator fixed) | Odin gave an eye for wisdom, | Voluspa 28-29 V; Gylf 15 V | Voluspa 28 is Odin sought by the seeress; the eye is in 29. |
| N-006 | PASS (colour) | and still could not change the ending. | (ours) restates Voluspa | Colour: the gods do not avert the end (Gylf XXXIV chain Fenrir; Voluspa 45-57). |
| N-007 | PASS | The gods chain a wolf to stop it. | Gylf 34 V |  |
| N-008 | PASS | One of them loses a hand doing it. | Gylf 34 V |  |
| N-009 | PASS (colour) | It makes no difference. | (ours) | Colour, no claim. |
| N-010 | PASS (locator fixed) | The end comes anyway, | Voluspa 45-57 V | Voluspa 47-52 was too narrow; the destruction is 45-57. |
| N-011 | PASS | and almost every god dies. | Gylf 51 V |  |
| N-012 | PASS (colour) | So how does a world begin, and how does it end? | (ours; the video's one question) | Colour, no claim. |
| N-013 | PASS (colour) | Let us start at the beginning. | Gylf 4-5 V | Colour. |
| N-014 | PASS | In the beginning there is no sand, no sea, and no sky. | Voluspa 3 V; Gylf 4 V |  |
| N-015 | PASS | Only a great gap, with ice on one side | Gylf 4 V |  |
| N-016 | PASS | and fire on the other. | Gylf 4 V |  |
| N-017 | PASS | Where the cold meets the heat, the ice begins to melt, | Gylf 5 V |  |
| N-018 | PASS | and out of the drops comes a giant named Ymir. | Gylf 5 V |  |
| N-019 | PASS | Beside him, a cow named Audhumla comes out of the same melting ice. | Gylf 6 V |  |
| N-020 | PASS | Ymir lives on her milk, and she lives on salty ice. | Gylf 6 V |  |
| N-021 | PASS | By the third day, she has licked a whole man out of the ice. | Gylf 6 V (Buri on the third day) |  |
| N-022 | PASS | That man's grandsons are Odin and two brothers, Vili and Ve. | Gylf 6 V |  |
| N-023 | PASS | So they kill Ymir. | Gylf 7 V |  |
| N-024 | PASS | His blood pours out in such a flood that nearly every frost giant drowns. | Gylf 7 V |  |
| N-025 | PASS (note) | The brothers drag the body into the middle of the gap, | Gylf 8 V | Gylf VIII 'bore him into the middle of the Yawning Void'; 'drag' is the shot's rope image only. |
| N-026 | PASS (note) | and build a world out of it. | Gylf 8 V | As 25. |
| N-027 | PASS | His flesh becomes the land, | Grimnismal 40 V; Gylf 8 V |  |
| N-028 | PASS | his blood becomes the sea, | Grimnismal 40 V |  |
| N-029 | PASS | his bones become the mountains, | Grimnismal 40 V |  |
| N-030 | PASS | and his hair becomes the trees. | Grimnismal 40 V |  |
| N-031 | PASS (locator fixed) | His skull becomes the sky, held up by four dwarfs. | Grimnismal 40 (skull as sky) V; Gylf 8 (four dwarfs, East, West, North, South) V | Grimnismal 41 is Midgard from the brows and the clouds. Skull as sky is Grimnismal 40; the four dwarfs are Gylf VIII only. |
| N-032 | PASS (note) | Sparks from the fire land are thrown up there as stars. | Gylf 8 V | Gylf VIII sparks and embers from Muspellheim set in the sky; sun and moon are made from them in Gylf XI. 'Stars' is the poem's list (Voluspa 5). |
| N-033 | FIX | Not bad for a day's work. -> **Not bad for three brothers.** | (ours) dry beat; the three brothers are Gylf 6-8 | 'A day's work' implies a duration no source gives. Three brothers made the world (Gylf VI-VIII). |
| N-034 | PASS (colour) | The brothers need someone to live in it. | (ours) glue; basis Gylf 9 | Glue line, no claim. |
| N-035 | PASS (locator fixed) | Along the shore they find two fallen trees. | Gylf 9 V (the two trees); Voluspa 17 has 'two without fate' and no trees | Voluspa 17 says 'two without fate', no trees; the trees are Gylf IX only. |
| N-036 | PASS | They shape them into the first man and woman, | Gylf 9 V |  |
| N-037 | PASS | Ask and Embla. | Gylf 9 V; Voluspa 17 V |  |
| N-038 | PASS | Odin gives them breath, | Gylf 9 V (Voluspa 18 differs; see NOTES) |  |
| N-039 | PASS | and their world is called Midgard, the middle world. | Gylf 8 V |  |
| N-040 | PASS (note) | Above it, the gods build their own home, Asgard, | Gylf 9 V | Gylf IX: Asgard 'in the middle of the world'; Gylf XV: the gods ride 'up over Bifrost'. 'Above' is fair. |
| N-041 | PASS | and join the two with a rainbow bridge. | Gylf 13 V |  |
| N-042 | PASS | Holding everything together is an enormous ash tree, Yggdrasil. | Gylf 15 V; Voluspa 19 V |  |
| N-043 | PASS (note) | Its roots run down to the gods, the frost giants, and the dead. | Gylf 15 V | Gylf XV: roots among the Aesir (in heaven), among the Rime-Giants, over Niflheim; Hel's realm is the land of the dead. |
| N-044 | PASS (note) | An eagle sits at the top. | Gylf 16 V | Gylf XVI: the eagle 'sits in the limbs of the Ash'; 'at the top' is the picture, Grimnismal 32 has the eagle above. |
| N-045 | PASS | A dragon gnaws at the bottom. | Gylf 16 V |  |
| N-046 | PASS (note) | And a squirrel runs between them, carrying insults. | Gylf 16 V | Gylf XVI: Ratatosk bears 'envious words' between eagle and Nidhogg; 'insults' fair. |
| N-047 | FIX | At the well of the giant Mimir, Odin trades one eye for a drink. -> **At the well of Mimir, Odin trades one eye for a drink.** | Voluspa 28-29 V; Gylf 15 V (Mimir keeps the well; Brodeur does not call him a giant) | Brodeur does not call Mimir a giant; he 'keeps the well' under the root toward the Rime-Giants (Gylf XV). Eye laid in pledge for one drink: Gylf XV, Voluspa 29. |
| N-048 | PASS (locator fixed) | That is why Odin has one eye, a wide hat, and a lot of secrets. | (ours) one eye Voluspa 29 and Gylf 15 V; wide hat = Odin's name Sidhottr 'With Broad Hat', Grimnismal 48 V; 'a lot of secrets' is our joke | One eye is Voluspa 29, not 28. Broad hat: Sidhottr 'With Broad Hat', Odin's name in Grimnismal 48. |
| N-049 | PASS | Then Loki walks in. | Gylf 33 V (Loki among the Aesir) |  |
| N-050 | PASS | Loki is a giant's son who lives among the gods. | Gylf 33 V (son of the giant Farbauti) |  |
| N-051 | PASS (note) | He is handsome, charming, and impossible to trust. | Gylf 33 V | Gylf XXXIII: 'beautiful and comely to look upon, evil in spirit, very fickle'. 'Charming' is colour on 'sleight' and 'artifices'. |
| N-052 | PASS | In the land of the giants, he has three children. | Gylf 34 V |  |
| N-053 | PASS | The first is a wolf named Fenrir. | Gylf 34 V |  |
| N-054 | PASS | The second is a serpent named Jormungandr. | Gylf 34 V |  |
| N-055 | PASS | The third is a girl named Hel, half dark and half pale. | Gylf 34 V |  |
| N-056 | PASS | The gods hear a prophecy that these three will bring them harm, | Gylf 34 V |  |
| N-057 | PASS | and Odin acts. | Gylf 34 V |  |
| N-058 | PASS | He throws the serpent into the deep sea, | Gylf 34 V |  |
| N-059 | PASS | and it grows until it circles the whole world, biting its own tail. | Gylf 34 V |  |
| N-060 | PASS (note) | He sends Hel to the land of the dead, and gives her charge of it. | Gylf 34 V | Gylf XXXIV: Hel gets Niflheim and 'power over nine worlds' over those who die of sickness or old age. 'Land of the dead' is a fair compression. |
| N-061 | PASS | The gods keep the wolf close, | Gylf 34 V |  |
| N-062 | PASS | and only Tyr dares to feed him. | Gylf 34 V |  |
| N-063 | PASS | Fenrir grows fast, so the gods decide to chain him. | Gylf 34 V |  |
| N-064 | PASS (note) | They offer him a chain as a game of strength, | Gylf 34 V | Gylf XXXIV names 'the Aesir' only. Odin and Thor in the shot are our casting; the spoken line is safe. |
| N-065 | PASS (note) | and he snaps it like thread. | Gylf 34 V | Gylf XXXIV: the first fetter Laedingr 'broke'; 'thread' is a simile. Dromi: 'stronger by half'. |
| N-066 | PASS | A heavier chain breaks too. | Gylf 34 V |  |
| N-067 | FIX | So the gods send to the dwarfs, who weave a ribbon called Gleipnir. -> **So the gods send to the dwarfs, who make a cord called Gleipnir.** | Gylf 34 V (Brodeur: 'fetter named Gleipnir', 'soft and smooth as a silken ribbon'; Skirnir is sent) | 'Weave' is not in the text: Gylf XXXIV says dwarves made the fetter Gleipnir, 'soft and smooth as a silken ribbon' (so beat 70 stands). |
| N-068 | FIX | It is made of six things: a cat's footstep, a woman's beard, -> **It is made of six things: the sound of a cat's step, a woman's beard,** | Gylf 34 V (noise a cat makes in foot-fall; beard of a woman) | Source is the 'noise a cat makes in foot-fall', a sound, not a print. Shot changed from a paw print to sound-lines. |
| N-069 | PASS (note) | a mountain's roots, a bear's sinews, a fish's breath, and a bird's spit. | Gylf 34 V (Brodeur: roots of a rock; Bellows note on Voluspa 39 quotes 'roots of mountains') | Brodeur: 'roots of a rock'; Bellows note on Voluspa 39 quotes 'roots of mountains'. Either is acceptable. |
| N-070 | PASS | It looks like a silk ribbon. | Gylf 34 V |  |
| N-071 | PASS | Fenrir smells a trick, and agrees on one condition: | Gylf 34 V |  |
| N-072 | PASS | one of the gods must put a hand in his mouth. | Gylf 34 V |  |
| N-073 | PASS (note) | The gods look at one another. Who will risk it? | Gylf 34 V | Gylf XXXIV: 'Each of the Aesir looked at his neighbor'. The question is our beat. |
| N-074 | PASS | Tyr steps forward, | Gylf 34 V |  |
| N-075 | PASS | and puts his right hand between the wolf's jaws. | Gylf 34 V |  |
| N-076 | PASS | The ribbon goes on, and the harder Fenrir pulls, the tighter it holds. | Gylf 34 V |  |
| N-077 | PASS | The gods laugh, all except Tyr. | Gylf 34 V |  |
| N-078 | PASS (note) | Fenrir bites the hand off, | Gylf 34 V | Gylf XXXIV says only 'he lost his hand'; the wolf biting it off is the plain reading and Lokasenna 38 has Tyr 'lost my hand' to Hrothvitnir (Fenrir). |
| N-079 | PASS | and stays chained until the end of the world. | Gylf 34 V |  |
| N-080 | FIX | Thor is the god of thunder, with a red beard and a hammer named Mjolnir. -> **Thor is the god of thunder, strongest of them all, with a hammer named Mjolnir.** | Gylf 21 V (strongest of all gods and men; Mjollnir). 'God of thunder' is the standard description, not a word in Gylf 21. Red beard not in Brodeur or Bellows: visual design only, never narrated | Red beard is in neither Brodeur nor Bellows (searched both texts: the only beard is Thrymskvitha 'he shook his beard'). Dropped from the narration; kept as a visual design choice only. |
| N-081 | PASS (locator fixed) | One day he sets out to find the serpent, | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-082 | PASS (locator fixed) | disguised as a young man. | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-083 | PASS (locator fixed) | He comes to a giant named Hymir, | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-084 | PASS (locator fixed) | who does not think the stranger will be much use on a boat. | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-085 | PASS (locator fixed) | Thor takes the head of the biggest ox on the farm for bait. | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-086 | PASS (locator fixed) | They row out, and Hymir says they are far enough, | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-087 | PASS (locator fixed) | but Thor says row further. | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-088 | PASS (locator fixed) | Hymir grows pale. | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-089 | PASS (locator fixed) | Thor ties the ox head to a hook, | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-090 | PASS (locator fixed) | and throws it into the deep, | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-091 | PASS (locator fixed) | and the serpent bites. | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-092 | PASS (locator fixed) | Thor pulls so hard his feet go through the bottom of the boat, | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-093 | PASS (locator fixed) | and he braces himself on the sea floor. | Gylf 48 V | Locator: the whole fishing trip is Gylf XLVIII (Brodeur); XLVII is the end of the Utgard-Loki tale. Claim supported. |
| N-094 | PASS | The serpent rises, and the two of them stare at each other. | Gylf 48 V |  |
| N-095 | PASS | Water pours in, Hymir panics, | Gylf 48 V |  |
| N-096 | PASS | and Thor lifts his hammer. | Gylf 48 V |  |
| N-097 | PASS | Hymir cuts the line. | Gylf 48 V |  |
| N-098 | PASS | The serpent sinks back into the sea, | Gylf 48 V |  |
| N-099 | PASS (note) | and Thor throws the hammer after it. | Gylf 48 V | Gylf XLVIII: 'men say he struck off its head... I think the Midgard Serpent yet lives'. Script follows Snorri's own view (needed for Ragnarok) and does not state the other. |
| N-100 | PASS | Thor knocks Hymir overboard, and wades ashore. | Gylf 48 V |  |
| N-101 | PASS (colour) | Round one is a draw, but they will meet again. | (ours) foreshadowing Gylf 51 | Colour/foreshadow: Gylf XLVII ends with Thor resolving to seek the serpent; kill at Ragnarok Gylf LI, Voluspa 55-56. |
| N-102 | PASS | Baldr is the best loved of the gods, | Gylf 22 V |  |
| N-103 | PASS | so fair and bright that light seems to shine from him. | Gylf 22 V |  |
| N-104 | PASS | Then he begins to dream about his own death. | Gylf 49 V; Baldrs draumar V |  |
| N-105 | PASS (note) | His mother, Frigg, goes to everything in the world | Gylf 49 V | Gylf XLIX: 'the Aesir took counsel' then 'Frigg took oaths'. Frigg as Baldr's mother is standard; Voluspa 53 'joy of Frigg' is Odin, not used. |
| N-106 | PASS | and asks for a promise. | Gylf 49 V |  |
| N-107 | PASS (note) | Fire, water, iron, stone, trees, sickness, poison, beasts, birds. | Gylf 49 V | Gylf XLIX list: fire, water, iron and metal, stones, earth, trees, sicknesses, beasts, birds, venom, serpents. The spoken list is a true selection. |
| N-108 | PASS | Every one swears not to harm Baldr. | Gylf 49 V |  |
| N-109 | PASS (note) | The gods are so relieved that they turn it into a game. | Gylf 49 V | Gylf XLIX: 'a diversion of Baldr's and the Aesir'. 'So relieved' is colour. Loki is not at the game in the text until he sees it; shot ok. |
| N-110 | PASS | Nothing touches him. | Gylf 49 V |  |
| N-111 | PASS | Everyone cheers, except Loki. | Gylf 49 V |  |
| N-112 | PASS | Loki puts on the shape of a woman and visits Frigg. | Gylf 49 V |  |
| N-113 | PASS | He asks if truly everything promised. | Gylf 49 V |  |
| N-114 | PASS | Frigg says only one plant, a little mistletoe, was too young to ask. | Gylf 49 V |  |
| N-115 | PASS | Loki goes straight out and pulls it up. | Gylf 49 V |  |
| N-116 | PASS (colour) | How do you hurt a god that nothing can hurt? | (ours; question) | Question beat, no claim. |
| N-117 | PASS | At the edge of the game stands the blind god Hod, with nothing to throw. | Gylf 49 V |  |
| N-118 | PASS (note) | Loki puts the mistletoe in his hand, and points him at Baldr. | Gylf 49 V | Gylf XLIX: Loki says 'I will direct thee where he stands; shoot at him with this wand'. 'Puts it in his hand' is the plain action. |
| N-119 | PASS | Hod throws. | Gylf 49 V |  |
| N-120 | PASS (locator fixed) | The mistletoe goes straight through Baldr, and he falls dead. | Gylf 49 V; Voluspa 32-33 V | Voluspa 31 is the Valkyries; Baldr and the mistletoe are 32, Hod's shaft 33. |
| N-121 | FIX | The gods beg Hel to give him back. -> **Odin's son rides to Hel, and begs her to give him back.** | Gylf 49 V (Hermod, Odin's son, rides to Hel; he is not named in the narration) | The gods do not go to Hel's gate. Hermod, Odin's son, rides Sleipnir to Hel and begs; Hel sets the condition (Gylf XLIX). Odin and Thor kneeling was invented. State and shot changed (a hooded rider; Hermod unnamed so no new card). |
| N-122 | PASS | She says yes, if every living thing weeps for him. | Gylf 49 V |  |
| N-123 | PASS | Everything weeps, even the rocks and the iron, | Gylf 49 V |  |
| N-124 | PASS | except one giantess, who says she will not. | Gylf 49 V |  |
| N-125 | PASS (note) | Some say it was Loki in disguise. | Gylf 49 V | Gylf XLIX: 'men deem that she who was there was Loki'. |
| N-126 | PASS (note) | Baldr stays dead. | Gylf 49 V | Gylf XLIX has the burning (ship Hringhorni, Nanna dies) before Hermod's ride; shot is a flash-forward, line is safe. |
| N-127 | PASS | The gods catch Loki at last, hiding as a salmon. | Gylf 50 V |  |
| N-128 | PASS | They bind him to three rocks, | Gylf 50 V |  |
| N-129 | PASS | and hang a serpent above his face, dripping venom. | Gylf 50 V |  |
| N-130 | PASS | His wife, Sigyn, holds a bowl to catch the drops. | Gylf 50 V |  |
| N-131 | PASS | When the bowl is full, she has to empty it, | Gylf 50 V |  |
| N-132 | PASS | and the venom lands on him, and the earth shakes. | Gylf 50 V |  |
| N-133 | PASS | He lies there until the end of the world. | Gylf 50 V |  |
| N-134 | PASS (note) | The end begins with a winter. | Gylf 51 V | Gylf LI: three winters of battles come first, then the Awful Winter. 'Begins with a winter' fair. |
| N-135 | PASS | It lasts three winters, with no summer between. | Gylf 51 V |  |
| N-136 | PASS (note) | Then wolves swallow the sun and the moon. | Gylf 51 V | Gylf LI: one wolf 'shall swallow the sun', the other 'seize the moon'. Voluspa 57: the sun turns black. Script follows Snorri. |
| N-137 | PASS | The stars go out, the earth shakes, and every chain breaks. | Gylf 51 V |  |
| N-138 | PASS | Fenrir runs free, his jaws open from the earth to the sky. | Gylf 51 V |  |
| N-139 | PASS | The serpent twists out of the sea, and the waves flood the land. | Gylf 51 V |  |
| N-140 | PASS (note) | A ship built of dead men's fingernails sails in. | Gylf 51 V | Gylf LI: Naglfar steered by Hrym. Voluspa 51: Loki at the helm of a ship. Script names neither (no conflict stated). |
| N-141 | FIX | Fire giants ride from the south, led by Surt, with a flaming sword. -> **The sons of Muspell ride from the south, led by Surt, with a flaming sword.** | Gylf 51 V; Voluspa 52 V (Brodeur: 'Sons of Muspell'; they are not called giants) | Brodeur: 'the Sons of Muspell ride'; Surt leads, sword brighter than the sun. They are not called giants in Gylf LI or Voluspa 52. |
| N-142 | PASS | The watchman of the gods, Heimdall, blows his horn. | Gylf 51 V |  |
| N-143 | PASS | The gods arm themselves and ride out to the plain. | Gylf 51 V |  |
| N-144 | FIX | The wolf goes for Odin and swallows him whole. -> **The wolf goes for Odin and swallows him.** | Gylf 51 V ('The Wolf shall swallow Odin') | 'Whole' is not in the text: 'The Wolf shall swallow Odin' (Gylf LI). |
| N-145 | PASS (note) | Odin's son Vidar puts one boot on the wolf's jaw, | Gylf 51 V (Vidar sets one foot on the lower jaw) | Gylf LI: one foot on the lower jaw, the shoe made of leather scraps. Voluspa 54: sword to the heart (not stated). |
| N-146 | FIX | and tears it apart. -> **and tears the wolf's throat apart.** | Gylf 51 V (Prose Edda: tears the gullet asunder; Voluspa 54 has a sword to the heart, not used) | Gylf LI: Vidar seizes the upper jaw and 'tears his gullet asunder'. 'It' was ambiguous (jaw or wolf). Voluspa 54 differs (sword to the heart): the script follows Snorri and does not state the other. |
| N-147 | PASS | Thor meets the serpent at last, and kills it. | Gylf 51 V |  |
| N-148 | PASS | Then he walks nine steps, and falls dead from the venom. | Gylf 51 V |  |
| N-149 | PASS | Tyr and a hound named Garm kill each other. | Gylf 51 V |  |
| N-150 | PASS (note) | So do Heimdall and Loki, free at last. | Gylf 51 V | Gylf LI: Loki and Heimdall each the other's slayer. 'Free at last' is colour on 'all fetters... broken' (Gylf LI). |
| N-151 | FIX | Then Surt flings fire across every world. -> **Then Surt flings fire across the earth.** | Gylf 51 V ('burn all the world'); Voluspa 52, 57 V | Gylf LI: Surt 'cast fire over the earth and burn all the world'. 'Every world' overreaches (Gimle survives, Gylf LII). |
| N-152 | PASS | The earth sinks into the sea. | Gylf 51 V |  |
| N-153 | PASS (colour) | And then, silence. | (ours) | Colour, no claim. |
| N-154 | PASS (colour) | But the story does not end there. | Gylf 53 V | Colour/transition; earth emerges: Gylf LIII, Voluspa 59. |
| N-155 | PASS | The earth rises again from the sea, green and new. | Voluspa 59 V; Gylf 53 V |  |
| N-156 | PASS | Fields grow without anyone sowing them. | Voluspa 62 V |  |
| N-157 | PASS (note) | A few gods survive, and Thor's sons carry his hammer. | Gylf 53 V | Gylf LIII: Vidar and Vali live; Modi and Magni 'shall have Mjollnir'. 'Carry' is the picture of 'have'. |
| N-158 | PASS | Baldr and Hod come back from the dead. | Voluspa 62 V; Gylf 53 V |  |
| N-159 | PASS (note) | One man and one woman step out of a forest, | Gylf 53 V | Gylf LIII: Lif and Lifthrasir hidden in Hoddmimir's Holt (a wood); 'step out' is implied by the repeopling. |
| N-160 | PASS | where they hid and lived on morning dew. | Gylf 53 V |  |
| N-161 | PASS | They begin again. | Gylf 53 V |  |
| N-162 | PASS (colour) | So how do we know any of this? | (ours; question) | Question beat, no claim. |
| N-163 | FIX | None of this was written down by the people who first told it. -> **None of this was written down when the poems were first made.** | (ours) basis: Bellows, Voluspa introductory note ('two hundred years between its composition and its first being committed to writing') V; Bellows general introduction (collections written by the 12th century) | Overstates: Bellows (Voluspa introductory note) puts about 200 years between composition and first writing for that poem, but the claim about 'the people who first told it' is not sourced for the whole corpus. Reworded to the safe claim. |
| N-164 | FIX | For centuries it was spoken, from memory, on long winter nights. -> **For generations it was recited from memory by poets.** | (ours) basis: Bellows (as above); 'winter nights' dropped, no source | 'Long winter nights' unsourced, dropped. 'Recited from memory' is the standard account; supported only in general terms (Bellows intro). Marked unverifiable detail in section 4. |
| N-165 | FIX | The poems survive in one great book, the Codex Regius, from about twelve seventy. -> **Most of the poems survive in one great book, the Codex Regius, from about twelve seventy.** | Codex Regius (GKS 2365 4to), 1270s (Wikipedia, Codex Regius; sole source for most of its poems) V; Bellows intro: other poems survive elsewhere (AM 748, Hauksbok) | 'The poems survive in one great book' is wrong: Bellows intro lists AM 748 (six poems plus Baldrs draumar), the Hauksbok Voluspa and others elsewhere. Wikipedia: Regius is 'the sole source for most of the poems it contains'. Date: 'thought to have been written during the 1270s' (Wikipedia, Codex Regius); Bellows gives only 'a hundred years or so' after a mid/late-12th-century collection. |
| N-166 | PASS (note) | It was written in Iceland, by Christians, about gods nobody worshipped anymore. | (ours) Iceland legally Christian in 1000 (Wikipedia, Christianization of Iceland) V; Bellows intro: Regius is a copy made about a hundred years after the 12th-century collections | Iceland legally Christian in 1000 (Wikipedia). 'By Christians': the 13th-century scribe is unnamed, but the whole context is Christian Iceland. |
| N-167 | FIX | Around twelve twenty, a chieftain named Snorri Sturluson wrote a handbook for poets. -> **Around twelve twenty, an Icelandic chieftain named Snorri Sturluson put together a handbook for poets.** | Prose Edda c. 1220 (Wikipedia, Prose Edda: 'to some extent written, or at least compiled, by Snorri c. 1220'); Brodeur intro: a book for apprentice poets V | Wikipedia, Prose Edda: 'to some extent written, or at least compiled, by Snorri c. 1220'; attribution is the standard one (Brodeur treats it as Snorri's) but hedged by modern sources. 'Icelandic' added so the reader places him. |
| N-168 | PASS (note) | Snorri was a Christian too, | (ours) basis: Brodeur intro (Snorri's address to beginners: the tales are 'neither to be believed nor to be tampered with'); Prologue opens with the Christian creation V | No single sentence in the texts read says 'Snorri was a Christian'; Brodeur's intro and the Prologue (Adam and Eve) establish it. |
| N-169 | FIX | and he begins by saying the gods were once men from Asia. -> **and his book opens with Adam and Eve, then says the gods were once men from Asia.** | Prose Edda Prologue (Brodeur p. 1-9: Adam and Eve, then the Aesir as men of Asia, from Troy) V; Brodeur intro: many scholars consider the Prologue spurious | Brodeur's Prologue opens 'In the beginning God created heaven and earth... Adam and Eve'; the Asia/Troy passage follows. Brodeur's intro: many scholars consider the Prologue spurious (not Snorri's). 'He begins by saying' was wrong. |
| N-170 | PASS (colour) | Not every source agrees. | (ours) | Framing: two real disagreements are named in beat 171 only. |
| N-171 | PASS (note) | In one poem, the makers of the first people have different names. | Voluspa 17-18 V | Voluspa 18: Odin, Hoenir, Lothur give soul, sense, heat and hue. Gylf IX: Odin, Vili, Ve. True as worded; the script then picks Snorri (beat 172). |
| N-172 | PASS (colour) | When they disagree, we follow Snorri. | (ours) | Editorial rule, no claim. |
| N-173 | PASS (note) | He was killed in twelve forty-one, on the orders of a Norwegian king. | Brodeur intro (Gizurr Thorvaldsson, 1241, 'at the express order of the King', Hakon Hakonarson) V; Wikipedia, Snorri: 23 Sept 1241, Reykholt, killed in the cellar | Date, king and order confirmed (Brodeur intro; Wikipedia: Hakon's secret letter ordered him killed or captured; he was killed in the cellar at Reykholt). Shot is a dramatisation (study doorway, not the cellar): visual only. |
| N-174 | PASS (colour) | A world made from a giant, ended by a wolf, and begun again. | (ours) recap | Recap, no claim. |
| N-175 | PASS (colour) | We only know it because somebody wrote it down. | (ours) | Closing line, true of the Eddic texts. |

## 6. Beats I am unsure about

- **N-040 'Above it, the gods build their own home, Asgard'**: Gylf IX puts Asgard 'in the middle of the world'; Gylf XV has the gods ride 'up over Bifrost' to the well in heaven, and Gylf XXII puts Breidablik 'in heaven'. 'Above' is the common reading; left PASS (note).
- **N-044 'An eagle sits at the top'**: Gylf XVI says 'in the limbs of the Ash'. Grimnismal 32 not re-read for 'above'. Harmless, left.
- **N-165/N-167 exact dates**: Codex Regius c. 1270 and the Prose Edda c. 1220 rest on modern reference (Wikipedia), not on a second scholarly source; Bellows (1923) does not give 1270. Unverified beyond one reference source each.
- **N-168 'Snorri was a Christian too'**: no sentence says it in the texts read; inferred from Brodeur's intro and the Christian Prologue. Near certain, not quotable.
- **N-173 shot**: Snorri was killed in the cellar at Reykholt (Wikipedia: 'He fled to the cellar'); the shot shows a study doorway. Visual only; change if the shot is regenerated.
- **N-064, N-073 shots**: Thor is not named in the Fenrir binding (Gylf says 'the Aesir'); Odin and Thor in the shot are our casting, not a source claim.
- **N-080 'god of thunder'**: standard description; Gylf XXI uses Oku-Thor ('chariot Thor') and 'strongest of all gods and men'. Brodeur's Skaldskaparmal has 'Thunderer' as a kenning. Kept.
- **Hymiskvitha, Baldrs draumar, Vafthrudnismol 44**: located in Bellows, not read in full; no beat depends on them (traces cite Baldrs draumar for N-104 only as the dream source).

## 7. Unverifiable items

- 'On long winter nights' (N-164): no source; dropped.
- The exact scribe, place and Christian status of the Codex Regius copyist: unknown; N-166 relies on the general Christian context of 13th-century Iceland.
- Red beard of Thor: not in either text; visual only.
- Exact year 1220 for the Prose Edda: a convention, not a recorded date.