# SCRIPT-N-NOTES.md (Norse, video 2 of The Myth Ledger, draft 1)

Measured on the spoken beat text of `SCRIPT-N-draft1.md` with a throwaway script (`norse/src/measure.py`; word = letters/digits token; sentence = split on . ? !; time = words at 150 wpm, raw voice, no pauses added). Source files for the script are `norse/src/beats.txt` (edit there, then run `measure.py` and `gen.py`).

## Metrics vs targets
| Metric | Draft 1 | Target |
|---|---|---|
| Spoken words | 1495 | 1,450-1,650 |
| Raw voice time at 150 wpm | 9:58 | 9:30-10:00 |
| Sentences | 139 (13.9 a minute) | 12-14 a minute |
| Words a sentence | mean 10.8, median 10, longest 25, 19% are 6 words or fewer | mean 10-12 |
| Questions | 4 (0.4 a minute): hook, Fenrir's "Who will risk it?", "How do you hurt a god that nothing can hurt?", "So how do we know any of this?" | 0.3-0.5 a minute |
| Beats (shots) | 175 (17.6 a minute; median beat 9 words, about 3.6 s) | V5 had 176 |
| Named chapters | 7 plus the cold open | 6-8 |
| Text cards, bands, chips, on-screen text | 0 | none (PROCESS rule 8) |
| Voiced dialogue, Edda quotations | 0, 0 | no invented quotes |

Hook is 83 words, about 33 s (3 s over the 30 s target; N-013 "Let us start at the beginning" can go if it must be 30 s flat).

## Chapters and timestamps (raw voice, 150 wpm; they will drift with Daniel's pauses and are re-timed at packaging)
| # | Chapter (story-claim title) | Start | Words | Beats | Beat ids |
|---|---|---|---|---|---|
| 0 | Cold open | 0:00 | 83 | 13 | N-001 to N-013 |
| 1 | A Giant Became the World | 0:33 | 180 | 20 | N-014 to N-033 |
| 2 | The Tree That Held Nine Worlds | 1:45 | 133 | 16 | N-034 to N-049 |
| 3 | The Wolf Everyone Agreed to Chain | 2:38 | 268 | 30 | N-050 to N-079 |
| 4 | The Day Thor Went Fishing for a Serpent | 4:26 | 176 | 22 | N-080 to N-101 |
| 5 | The God Nothing Could Hurt | 5:36 | 272 | 32 | N-102 to N-133 |
| 6 | Everyone Dies, Then the World Begins Again | 7:25 | 237 | 28 | N-134 to N-161 |
| 7 | The Christian Who Saved the Gods | 9:00 | 146 | 14 | N-162 to N-175 |

Story spine as briefed: Ymir and Audhumla, the world made from Ymir's body, Odin and his two brothers (chapter 1); Ask and Embla, Yggdrasil, the nine worlds kept light, Odin's eye (chapter 2); Loki and his three children, the binding of Fenrir and Tyr's hand (chapter 3); Thor and the Midgard serpent (chapter 4); Baldr's death and Loki's punishment (chapter 5); Ragnarok and the world reborn (chapter 6); where the myth comes from (chapter 7).

## Source key (every trace tag in the script)
**Locator caveat.** Stanza and section numbers were written from memory of Bellows 1923 (Poetic Edda) and Brodeur 1916 (Prose Edda) and are NOT yet checked against the texts; no web read was done in this pass. The fact-check pass (Stage 2 step 3) must confirm each one and correct the number where it is off. The facts themselves are standard to those texts. Brodeur's section numbering is approximate below; where unsure the poem or section is named by its content.

| Tag | Source | Used for |
|---|---|---|
| Voluspa 1 | Voluspa (Bellows), the seeress addresses Odin and the gods | the gods hearing the prophecy (N-004) |
| Voluspa 2 | Voluspa, the seeress remembers nine worlds and the tree | nine worlds (N-001) |
| Voluspa 3 | Voluspa, no sand, no sea, no cool waves in the time of Ymir | the opening of chapter 1 |
| Voluspa 17-18 | Voluspa, Ask and Embla found as trees; Odin, Hoenir and Lodur give them life | Ask and Embla; the one disagreement the script names |
| Voluspa 19 | Voluspa, the ash Yggdrasil and the well at its foot | Yggdrasil |
| Voluspa 28 | Voluspa, Odin's eye hidden in Mimir's well | Odin's eye (hook and chapter 2) |
| Voluspa 31-33 | Voluspa, the mistletoe, Hod's throw, Baldr's death | Baldr's death |
| Voluspa 45-66 | Voluspa, the whole Ragnarok section and the rebirth | Ragnarok and rebirth (the more exact stanzas are cited per beat) |
| Voluspa 59, 62 | Voluspa, earth rises green from the sea; unsown fields bear; Baldr returns | rebirth beats |
| Grimnismal 40-41 | Grimnismal (Bellows), earth from Ymir's flesh, sea from blood, hills from bones, trees from hair, heavens from the skull | N-027 to N-031 |
| Baldrs draumar | Baldrs draumar (Bellows), Baldr's evil dreams | N-104 |
| Gylf 4-5 | Gylfaginning (Brodeur): Ginnungagap, Niflheim and Muspellheim, the thaw, Ymir | N-014 onward |
| Gylf 6 | Gylfaginning: Audhumla, her milk, the licked ice, Buri on the third day, Bor's sons Odin, Vili, Ve | N-019 to N-022 |
| Gylf 7 | Gylfaginning: the brothers kill Ymir, the flood of blood | N-023, N-024 |
| Gylf 8 | Gylfaginning: the earth made of Ymir, the four dwarfs, sparks as stars | N-025 to N-033 |
| Gylf 9 | Gylfaginning: Bor's sons find two trees, Ask and Embla; Asgard | N-035 to N-039 |
| Gylf 13 | Gylfaginning: Bifrost, the rainbow bridge | N-040, N-041 |
| Gylf 15-16 | Gylfaginning: Yggdrasil's three roots, Mimir's well, Odin's eye; eagle, Nidhogg, Ratatosk | chapter 2 |
| Gylf 21-22 | Gylfaginning: Thor and Mjolnir; Baldr the fair | N-080, N-102 |
| Gylf 33 | Gylfaginning: Loki, son of Farbauti, fair of face and evil of mind | N-050, N-051 |
| Gylf 34 | Gylfaginning: Loki's three children, Odin throws the serpent in the sea, Hel in Niflheim, Tyr feeds the wolf, Laeding, Dromi, Gleipnir (six ingredients), Tyr's hand | N-052 to N-079 (Loki's children through Tyr's hand) |
| Gylf 47-48 | Gylfaginning: Thor disguised as a youth, Hymir, the ox head, the serpent, the line cut, Hymir knocked overboard | chapter 4 |
| Gylf 49 | Gylfaginning: Baldr's dreams, Frigg's oaths, the game, Loki as a woman, mistletoe, Hod, Hel's condition, all things weep but Thokk | chapter 5 |
| Gylf 50 | Gylfaginning: Loki as a salmon, bound with Narfi's entrails, the serpent, Sigyn's bowl, the earthquakes | end of chapter 5 |
| Gylf 51 | Gylfaginning: Fimbulwinter, the wolves, the chains break, Surt, the fight on Vigrid, who kills whom | chapter 6 |
| Gylf 53 | Gylfaginning: the new earth, Vidar and Vali, Modi and Magni with the hammer, Baldr and Hod, Lif and Lifthrasir on morning dew | rebirth beats |
| Prose Edda Prologue | Prose Edda Prologue (Brodeur): the Aesir as men from Asia | N-169 |
| Codex Regius, Prose Edda c. 1220, Snorri 1241 | Not Edda text: standard dating of the manuscript (about 1270), the Prose Edda (about 1220) and Snorri's killing in 1241. Cite a PD or reference source in the fact-check (Brodeur's introduction, or a reference work); flag if only a modern source is found. | chapter 7 |

## The source for EVERY (ours) claim
(ours) beats carry no factual claim beyond what is shown; where there is one, the basis is named. 19 beats.

| Beat | Text | Basis |
|---|---|---|
| N-003 | The gods know it, | Framing line. Basis: Voluspa 1 and the seeress's prophecy, which the gods hear (the next beat carries the V trace). |
| N-006 | and still could not change the ending. | Restates the prophecy of Ragnarok (Voluspa 45-66); the gods do not avert it. |
| N-009 | It makes no difference. | Collapse line of the hook; no factual claim. |
| N-012 | So how does a world begin, and how does it end? | The video's one question; no claim. |
| N-033 | Not bad for a day's work. | Dry button after the creation; no claim. |
| N-034 | The brothers need someone to live in it. | Glue; matches Gylf 9 (the brothers make the first people). |
| N-048 | That is why Odin has one eye, a wide hat, and a lot of secrets. | One eye is Voluspa 28 and Gylf 15. The wide hat and the 'secrets' are our character description; the lot-of-secrets joke is ours. |
| N-101 | Round one is a draw, but they will meet again. | Foreshadow: Thor and the serpent meet at Ragnarok (Gylf 51, Voluspa 55-56). The fishing trip being a 'draw' is our reading of Gylf 48. |
| N-116 | How do you hurt a god that nothing can hurt? | Question beat; no claim. |
| N-153 | And then, silence. | Transition beat; Gylf 51/Voluspa 57 say the earth sinks into the sea. No claim. |
| N-162 | So how do we know any of this? | Question beat; no claim. |
| N-163 | None of this was written down by the people who first told it. | Oral transmission before writing is the standard account of the Eddic poems; no Edda text says it. Needs a reference source in the fact-check (or soften). |
| N-164 | For centuries it was spoken, from memory, on long winter nights. | Oral transmission before writing is the standard account of the Eddic poems; no Edda text says it. Needs a reference source in the fact-check (or soften). |
| N-166 | It was written in Iceland, by Christians, about gods nobody worshipped anymore. | Iceland's conversion about the year 1000 and a Christian scribal context for Codex Regius; reference source needed in the fact-check. |
| N-168 | Snorri was a Christian too, | Snorri was a Christian; his Prologue frames the gods as men (Prose Edda Prologue), which is how a Christian could write them down. |
| N-170 | Not every source agrees. | Framing for the one source disagreement (see the next beat); the disagreements are listed below. |
| N-172 | When they disagree, we follow Snorri. | States our editorial rule: where the Eddas differ we follow Snorri (Gylfaginning) as the spine. |
| N-174 | A world made from a giant, ended by a wolf, and begun again. | Recap of the story just told; no new claim. |
| N-175 | We only know it because somebody wrote it down. | Closing line; our claim that the survival of the myths depends on writing it down (true of the Eddic texts). No claim beyond that. |

## Where the sources disagree (the script picks one version)
1. **Who made the first people, and what each gave.** Voluspa 17-18: Odin, Hoenir and Lodur give breath, spirit, and blood with fair colour. Gylfaginning 9: Odin, Vili and Ve give breath and life, wit and feeling, hearing and sight. Script follows Snorri (Odin gives breath; Vili and Ve are in the cast); N-171 says once, in chapter 7, that the makers differ in one poem. This is the only disagreement named in the narration.
2. **Thor's fishing trip.** Gylfaginning 47-48 has Thor travel alone, disguised as a youth, to Hymir's, and Hymir cuts the line; Snorri adds that some say Thor killed the serpent, but he thinks it still lives. Hymiskvida (Poetic Edda) tells the trip as part of a quest for a cauldron, with Tyr as guide (and Tyr as Hymir's son, which clashes with Gylfaginning 34's Tyr as one of the Aesir). Script follows Snorri's version; the quest, the cauldron and Hymir-as-Tyr's-father are not used. The serpent's survival matters because Thor kills it at Ragnarok.
3. **Where and how Loki is bound.** Gylfaginning 50: a cave, three rocks, the entrails of his son Narfi, a serpent from Skadi, Sigyn's bowl. Voluspa 34-35 puts a bound Loki in a grove of hot springs with Sigyn and no mention of the serpent or rocks (stanza detail to verify). Lokasenna's closing prose has the Narfi version. Script follows Snorri.
4. **Who steers the ship at Ragnarok.** Voluspa 50 puts Loki at the helm of a ship from the east; Gylfaginning 51 says Hrym steers Naglfar. The script says only that a ship built of dead men's fingernails sails in, so it does not need to choose; the Naglfar name is not spoken.
5. **Hermod's ride to Hel.** Gylfaginning 49 has Hermod ride Sleipnir to Hel to ask for Baldr back. The script says "the gods beg Hel" and shows Odin and Thor kneeling at her gate; this compresses the story and leaves Hermod out (cast kept small). Flag for review: it is a simplification, not a contradiction.
6. **Odin and the eye in the early beats.** Odin is shown with one eye throughout, including in chapter 1 before he pays for it at Mimir's well in chapter 2, following the video 1 decision to keep one clean look. The narration never says he is one-eyed in chapter 1. Open question 2 below.
7. **Baldr's killing, other versions.** Saxo's Gesta Danorum (Elton 1894, public domain) tells it differently, with Hotherus as a rival. Not used; the script follows the Eddas as briefed.

## Cast list with a proposed one-line bold identity each
Scale line: Odin, Thor, Loki, Tyr, Baldr, Frigg, Hod, Vidar 1.0; dwarfs 0.5; giants (Ymir, Hymir, giantess, Surt) 3.0-4.0; Fenrir 0.5 as a cub, 1.5 as a growing wolf, 2.0 grown; Jormungandr 0.1 as a cub, ring around the world later (shot as a huge green coil, head 3.0); Hel (child) 0.8.

| # | Character | Bold identity (5-6 tells at most) |
|---|---|---|
| 1 | Odin | one eye (the other a dark socket), wide blue-grey hat, long grey beard, dark blue cloak |
| 2 | Vili and Ve (one card, two cloak colours) | bare-headed, brown beards, matching build, green cloak (Vili), yellow cloak (Ve) |
| 3 | Ymir | huge pale-blue giant, white beard, ice on his shoulders, bare chest |
| 4 | Audhumla | white cow with large brown patches, ice crystals on her muzzle |
| 5 | Dwarf (four copies, one card) | small, long white beard, pointed brown hood, leather apron |
| 6 | Ask and Embla (also reused as Lif and Lifthrasir) | man and woman, leaf-green tunics, plain, wide-eyed, no weapons |
| 7 | Loki | spiky jet-black hair, bright green cloak, wide grin, thin build |
| 8 | Giantess (Angrboda; reused as Thokk) | blue skin, dark-brown braids, ragged brown dress |
| 9 | Fenrir | grey wolf, white teeth, a pale ribbon or chain when bound |
| 10 | Jormungandr | green serpent with dark ring bands, yellow eyes |
| 11 | Hel | child, face split down the middle, left half black and right half white, black dress |
| 12 | Tyr | blue tunic, short brown hair, right arm ends in a bandaged stump after the binding (two-handed in earlier beats: needs a variant sheet or a note that all his beats come at or after the binding; see open question 3) |
| 13 | Thor | red beard, red cape, short hammer, broad build; hooded brown cloak variant for the disguise |
| 14 | Hymir | giant, brown beard, fisherman's brown smock, net over one shoulder |
| 15 | Baldr | white hair, glowing gold tunic, soft gold halo |
| 16 | Frigg | long blue dress, white headdress, brown braid |
| 17 | Hod | plain grey cloak, blank white eyes, hands often empty or reaching |
| 18 | Sigyn | brown dress, white headscarf, a wooden bowl always in her hands |
| 19 | Eagle | huge brown eagle with a white head |
| 20 | Dragon (Nidhogg) | dark brown wingless dragon, red eyes |
| 21 | Squirrel | red-brown squirrel, big tail, tiny scroll |
| 22 | Surt | giant, black body, orange flame sword, flame hair |
| 23 | Heimdall | white cloak, golden horn, pale blond hair |
| 24 | Vidar | stone-faced young god, one huge iron boot, dark red cloak |
| 25 | Garm | black hound, red eyes, bloody chest |
| 26 | Modi and Magni (one card) | two young boys in red capes copying Thor, one hammer between them |
| 27 | Skald or scribe (one card) | plain brown tunic, round head, beard, a lyre or a quill by scene |
| 28 | Snorri Sturluson | long dark-blue robe, holds a quill, small wooden cross on a cord, shaved top of head |

That is 28 cards (31 figures on screen counting Vili and Ve, Modi and Magni, and the dwarf copies). Frost giants swept away by the flood are an unnamed crowd (composite, or draw as tiny blue figures in the distance only). Odin's seeress and Hermod are not in the cast.

## NEW places (all new; Greek library does not carry over). One master each, variants derived by edit.
1. Yggdrasil in empty space (dusk, derives to the root and branch crops for chapter 2)
2. Odin's hall (night, firelit, high seat; also used for dawn doorway and the Asgard feast shot)
3. Cliff above a dark sea (twilight)
4. Fenrir's rock: a flat grey rock on a hill (dusk, night)
5. Ginnungagap: pale-blue empty gap with a white ice land on the left and a red fire land on the right (dawn)
6. The ice field with a melt pool (dawn; Ymir, Audhumla, flood variants)
7. Ymir's body as land: brown hills, blue sea, grey peaks, green forest (dawn to night; the skull sky with four corner dwarfs is a variant)
8. Midgard shore (morning; two driftwood trunks)
9. Asgard: golden hall on a green hill, rainbow bridge, grassy ring for Baldr's game and Fenrir (day; the grounds are a crop)
10. Mimir's well beneath a root of Yggdrasil (dusk)
11. Jotunheim hut (night, firelit, cradle)
12. Dwarf forge (night, firelit, bench and pot)
13. Open sea with the world-ring serpent (day; also night for the Ragnarok wolf and ship beats)
14. Hymir's farm (day)
15. Hill road to the sea and the beach (day, evening)
16. Hymir's boat on open sea (a place master with the boat prop; morning, midday)
17. Baldr's bedroom (night)
18. Meadow (day)
19. Fensalir: a wooden door in a hall wall (dusk)
20. Oak tree with a mistletoe sprig (dusk)
21. Hel's gate: a black stone gate (dusk)
22. Giantess's cave (day)
23. Burning funeral ship at sea (dusk)
24. Waterfall (day)
25. Loki's prison cave: three rocks, dripping serpent (night)
26. Snowy world, three winter views (dusk, day)
27. Night sky with wolves, sun and moon discs
28. Heimdall's wall on Asgard's edge (night)
29. Vigrid plain: dark plain, red sky (night; the opening hook's burnt-plain beats use the same master)
30. Empty black sea, then a green hill rising (night to dawn)
31. Hoddmimir's forest (dawn)
32. Icelandic turf hall (night, firelit)
33. Scriptorium (day)
34. Snorri's study at Reykholt (day, dusk)

34 place masters. Several are crops or time-of-day variants of one master (for example 2 and 17, 9 and 18, 13 and 27, 29 and 30), so a realistic count is about 26 generated masters plus derived variants.

## NEW props (each needs a master card, with a scale note)
1. Mjolnir: short-handled hammer (Thor)
2. Gleipnir: thin pale ribbon (the same prop doubles as a chain)
3. Iron chains, thick and thicker (Fenrir, Laeding and Dromi)
4. Sword (propped in Fenrir's jaws)
5. Ox head (Hymir's biggest ox, Thor's bait; scale 1.0, huge horns)
6. Fishing hook and heavy rope
7. Hymir's boat (small wooden rowboat, scale note: seats two)
8. Mistletoe sprig (a green sprig with white berries, tiny; needs a big visual in close-ups)
9. Wooden cradle (Loki's children)
10. Sigyn's wooden bowl
11. Surt's flame sword
12. Gjallarhorn: golden horn
13. Naglfar: pale ship made of fingernails, ragged sail
14. Rainbow bridge (place-prop, Bifrost)
15. Skald's lyre, scribe's quill and desk, a calfskin page, the Codex Regius (a thick book), Snorri's hanging cross (one "book and writing" prop set)
16. Cross on the scriptorium wall (simple wooden cross)

16 props listed (counted as 15 plus the cross as part of the book-and-writing set if William prefers). Places and props together: 34 places (about 26 real masters) and 16 props.

## What I am least sure of
1. **Locators (stanza and section numbers).** From memory, not verified. Every one needs the fact-check pass.
2. **The 1241 death and "Norwegian king" line (N-173), the Codex Regius date (N-165) and the oral-tradition lines (N-163, N-164)** rest on standard accounts, not on the Eddas; the fact-check must find a public-domain or reference source or soften them.
3. **Dwarfs weaving Gleipnir**: Gylfaginning 34 says the dwarfs "made" it; "weave" is our verb. Change to "make" if the fact-check wants it exact.
4. **Hel as a child.** Gylfaginning 34 says only that she is thrown into Niflheim and given power; showing her as a child in Odin's hand is ours. The brief wanted bold simple designs, and a child stays small-feature simple.
5. **"The brothers need someone to live in it" (N-034) and "Not bad for a day's work" (N-033)** are dry humour with no source.
6. **Hymir's reluctance.** Gylf 47 has Hymir doubt the stranger and fear the far water; the script keeps the doubt (N-084) and a bare "Hymir grows pale" (N-088).
7. **"Heimdall and Loki ... free at last"**: Gylf 51 does say all fetters break; "free at last" is our colour on the earthquake that releases Loki.

## Open questions for William
1. Hook is 33 s, 3 s over target. Cut N-013 ("Let us start at the beginning") or keep?
2. Odin has one eye in chapter 1, before the narration says he lost it. Keep one eye throughout (simplest, same as video 1), or draw two eyes until Mimir's well (needs a second face on the card)?
3. Tyr's hand. Cards and plates before the binding should show two hands; after, a stump. Do we want one Tyr card with a plain note, or two variants?
4. Hermod is cut and Odin and Thor kneel at Hel's gate instead: accept the simplification?
5. Chapter 7 mentions Snorri's killing by a Norwegian king. Keep as a short sombre beat, or cut for tone and runtime?
