# FACTCHECK-V2.md: line-by-line fact-check of SCRIPT-V2 (The Myth Ledger, video 1)

Checked 2026-11-12 (evening). SCRIPT-V2.md and RESEARCH-V1.md were read only, not edited. Nothing generated, uploaded or sent. All web content treated as untrusted data; Python run with `-I`; downloads kept in `/tmp/fc/` (not in the workspace).

**Tally (110 beats): 87 PASS, 18 FIX, 5 UNVERIFIED.** The 18 FIX are 10 small wording fixes (marked *minor*: 05, 29, 48, 61, 64, 70, 78, 86, 92, 93), 7 that change what the line claims (marked **material**: 11, 24, 55, 63, 81, 94, 104), and the beat 10 chip, which goes with 11.

**Two findings that change the research record (not just the script):**
1. **The Witton and Hing 2024 DOI in RESEARCH-V1 and section (f) is a paper about the griffin**: "Did the horned dinosaur *Protoceratops* inspire the griffin?", *Interdisciplinary Science Reviews* 49(3-4): 363-388. Its abstract (read in full via Crossref, OpenAlex and the Portsmouth repository page) never mentions Abel, Empedocles or the Cyclops. The Cyclops/Abel passage the script relies on is quoted only by Wikipedia (which cites this same DOI). Whether the passage is a section of that paper is **unconfirmed**; I could not open the paper (Cloudflare human check on every host; I did not click through a "verify you are human" box).
2. **Beat 63 misattributes a sentence.** In the Discover article, "prior to the time of Alexander the Great ... ancient Greeks would never have seen a live elephant" is the journalist's sentence, not Mayor's. RESEARCH-V1 C8 ("Mayor also notes") is wrong.

---

## 1. Summary table

Verdict key: PASS supported as worded (a note flags small caveats); FIX wording overstates, misattributes or is wrong; UNVERIFIED cannot be confirmed. "Primary" = Greek text plus Murray and Butler, read in full for the passage.

| Beat | Line (short) | Verdict | Reason |
|---|---|---|---|
| 01 | Picture a sailor, ducking into a beach cave to light a fire | PASS | Abel: sailors, "perhaps in a beach cave in Sicily", "in lighting a fire". Framed as imagining. |
| 02 | CREW: Hello? | PASS | Ours, inside the imagined scene. |
| 03 | In the clay at the back... one enormous eye | PASS | Abel: skull "projecting from the clay". "At the back", "looks back" are staging. Eye = layman's reading of the nostril. |
| 04 | CREW: Nope. | PASS | Gag. |
| 05 | That scene is from 1914... Abel imagined it | FIX (minor) | Abel imagines sailors (plural), hedged ("perhaps", "probably"); no reaction or dialogue. See 5-A. |
| 06 | The skulls are real... dwarf elephants on Sicily | PASS | Fossils real (Abel 1914; Discover). Label should read "SMALLEST: UNDER 1 M" (a 2 m Sicilian form existed). |
| 07 | The sailor is not. Abel made him up. | PASS | Defensible gag. "Imagined" is more exact than "made up"; optional. |
| 08 | Four suspects... elephant... touch | PASS | Tease; payoffs 59, 89. |
| 09 | A very bad decision about cheese | PASS | Odysseus refuses to take the cheeses and leave (Od. 9.224-229 sense; Butler). |
| 10 | Chip: DIALOGUE TIDIED FROM HOMER | FIX | Homer gives no speech at 24-26 and 30-31. See 11. |
| 11 | Homer gives these characters lines. Here they are, tidied up. | FIX **material** | Overstates: some lines are invented from thoughts or from nothing. |
| 12 | Book Nine never says where | PASS | No place-name in Greek Book 9; whole Odyssey never names a place for them (Od. 6.4-5 only "near" Phaeacians' old Hyperia). |
| 13 | Twelve men, goatskin of wine, cave | PASS | 9.195 δυοκαίδεκ' ἀρίστους; 9.196 ἀσκόν. |
| 14 | Racks of cheese. Pens full of lambs. Nobody home. | PASS | Butler; Greek sense. |
| 15 | CREW: Take the cheese. Let's go. | PASS | Men beg to steal cheeses and go (reported). Dramatised. |
| 16 | ODY: No. I want to meet the owner. | PASS | Odysseus's stated motive (reported). Dramatised. |
| 17 | Cleverest man... gift basket | PASS | Gag; the guest-gift (ξείνια) hope is Homer's. |
| 18 | Less like a man than a wooded peak | PASS | 9.190-192 ῥίῳ ὑλήεντι ("wooded peak"); Butler says "crag". Said before he arrives. |
| 19 | Drives his flock inside, rolls a stone. Twenty-two wagons | PASS | 9.241-242 δύω καὶ εἴκοσ' ἄμαξαι. Nit: night one the males stay outside. |
| 20 | POLY: Strangers, who are you? Traders, or pirates? | PASS | 9.252-255. |
| 21 | ODY: Greeks... home from Troy... Zeus protects guests | PASS | Dramatised; "Achaeans" simplified. |
| 22 | POLY: We Cyclopes don't care about Zeus | PASS | 9.275-276. |
| 23 | Grabs two of the men for supper, falls asleep | PASS | 9.288-298. |
| 24 | CREW: Kill him. He is asleep. | FIX **material** | The sword impulse is Odysseus's own thought (9.299-305), not the crew's. |
| 25 | ODY: And then who moves the stone? | PASS | Odysseus's own reasoning; right speaker. |
| 26 | CREW: Ah. | PASS | Gag (see 24 for the replacement option). |
| 27 | Two more at breakfast, two the next night, six in all | PASS | 9.289, 9.311, 9.344: three meals of two. Compresses the order (see Appendix A). |
| 28 | The giant's own club... olive trunk... mast | PASS | 9.319-328. |
| 29 | ODY: Four of you help me carry the stake. Draw lots. | FIX (minor) | Odysseus gives no number; "four" is the narrator's count after the lots (9.334-335). |
| 30 | CREW: And if he wakes up? | PASS | Invented, disclosed (after fix to 11). |
| 31 | ODY: Then it is a short plan. | PASS | Gag. |
| 32 | Stake hidden under dung | PASS | 9.329-330. |
| 33 | ODY: You have eaten a great deal of man's flesh, Cyclops. Have some wine. | PASS | 9.347 (Butler near-verbatim). |
| 34 | Priest of Apollo... twenty to one... unmixed... three bowls | PASS | Maron priest of Apollo; 9.209 one cup into twenty measures; 9.205 jars ἀκηράσιον (unmixed); skin filled from them (9.212); 9.361 τρὶς. Risk row resolved. |
| 35 | POLY: More. Now tell me your name | PASS | 9.355-356. Order compressed (he asks after bowl one). |
| 36 | ODY: My name is Nobody. Mother, father, friends | PASS | 9.366-367. |
| 37 | POLY: I will eat Nobody's friends first, Nobody last | PASS | 9.369-370. |
| 38 | Worst present in history | PASS | Gag. |
| 39 | Drunk... stake into the fire, then the eye | PASS | 9.371-383. |
| 40 | Blacksmith's simile: axe in cold water | PASS | 9.391-394 (axe or adze). |
| 41 | CYC2: Polyphemus, what is wrong? Is someone killing you? | PASS | 9.403-406. |
| 42 | POLY: Nobody is killing me. By trickery. Not by force. | PASS | 9.408 οὐδὲ βίηφιν. |
| 43 | CYC2: ...illness from Zeus. Pray to your father. Let the rest of us sleep. | PASS | 9.410-412; the "sleep" complaint is moved from their first question (9.404). All same speaker. |
| 44 | No laws and no assemblies | PASS | 9.112. |
| 45 | Sheep in threes; Odysseus under the best ram; backs not bellies | PASS | 9.425-433, 9.441-443. |
| 46 | POLY: My good ram... why are you last... your master's eye | PASS | 9.447-453. |
| 47 | Talking to the ram carrying the man who blinded him | PASS | Gag over 9.444-455. |
| 48 | Jeers... tears the top off a hill... just in front of the rudder | FIX (minor) | Greek: lands in front of the ship, just misses the tip of the steering-oar. |
| 49 | CREW: Please stop. He has thrown one rock already | PASS | 9.494-499. |
| 50 | ODY: If anyone asks who blinded you, tell them it was Odysseus | PASS | 9.502-505. |
| 51 | Nobody lasted one night | PASS | Gag. |
| 52 | POLY: ...prophecy was true... weakling... presents | PASS | 9.507-521 (Telemus). "Warrior" paraphrases "tall, handsome". |
| 53 | ODY: ...not even Poseidon can heal that eye | PASS | 9.523-525 (ἐνοσίχθων, Earth-shaker). |
| 54 | POLY: Father Poseidon... all his men gone | PASS | 9.528-535; "all his companions" (9.534) is in the Greek. "Father" is tidying of the vocative. |
| 55 | Poseidon listens. For most of the rest of the poem, Odysseus does not get home. | FIX **material** | Wrong for the poem: he is home from Book 13 (12 of 24 books). True for the story's years. |
| 56 | Search Book Nine for "one eye"... never a forehead | PASS | Greek: 0 hits μετωπ- for the Cyclops anywhere in the Odyssey; Iliad has no Cyclopes. |
| 57 | Homer assumes you were paying attention | PASS | Scholars say the same (West; Heubeck and Hoekstra, via Wikipedia). |
| 58 | Time to open the case | PASS | Structure. |
| 59 | Chip: SUSPECT 1 | PASS | Heading. |
| 60 | Ice Age Sicily had elephants... smallest stood under a metre | PASS | Larramendi and Palombo 2015 via Wikipedia (male 96.5 cm, female 80 cm); Herridge and Lister 2012 abstract. |
| 61 | Bones turn up in caves, and still do. Two small eye sockets... | FIX (minor) | "And still do" unsourced. Sockets: Abel "deep down on the sides"; Mayor "negligible". |
| 62 | That hole is the trunk opening... could pass for one very large eye | PASS | Discover: "nasal cavity... could easily have mistaken". Hedged. |
| 63 | Mayor notes that before Alexander... no live elephant | FIX **material** | Journalist's sentence in Discover, not Mayor's. |
| 64 | Abel pictured his sailor... looking back at him with one great eye | FIX (minor) | Abel: sailors, "perhaps", skull "projecting from the clay"; "looking back with one great eye" is ours. |
| 65 | CREW: Nope. | PASS | Callback gag. |
| 66 | Everything else, Abel wrote, was added later | PASS | Abel: "Everything else is a later addition". |
| 67 | Mayor is the theory's best-known champion... careful | PASS | Opinion, defensible. See Appendix B on the same article's other quotes. |
| 68 | "I don't like to say that the fossils inspired..." | PASS | Verbatim match to Discover. Context in 5-B. |
| 69 | The theory's best friend, on the record | PASS | Gag. |
| 70 | Empedocles found such bones on Sicily and took them for giants | FIX (minor) | Abel: "reported such discoveries", not "found". |
| 71 | No surviving ancient source has it. Colavito: modern myth, apparently invented by Abel | PASS | Colavito wording exact; "no surviving source" is Witton and Hing via Wikipedia (two secondary sources agree). |
| 72 | Witton and Hing argue the whole idea becomes baseless | UNVERIFIED | Paper not readable; DOI is the griffin paper. See 5-C. |
| 73 | Aguirre and Buxton call it unfalsifiable | UNVERIFIED | Only "serious doubts" verified (OUP abstract). See 5-D. |
| 74 | Possible. Provable? No. | PASS | Mayor's quote supports it. |
| 75 | Chip: SUSPECT 2 | PASS | Heading. |
| 76 | Different poem, different job | PASS | Hesiod's Cyclopes vs Homer's. |
| 77 | Hesiod, around 700 BC: Brontes, Steropes, Arges. Thunder, Lightning, Bright | PASS | Evelyn-White note: "Thunderer... Lightning Flash... Vivid One". |
| 78 | They hammer out the thunderbolt for Zeus | FIX (minor) | Hesiod: "made" (τεῦξαν). The smithing is later (Callimachus, Virgil). |
| 79 | One eye only, in the middle of the forehead | PASS | Theogony 142-143, Greek and Evelyn-White. |
| 80 | Burkert suggested smith Cyclopes may reflect guilds | PASS | Burkert, Greek Religion, p. 173: "It may be surmised that smith guilds lie behind... Cyclopes" (via Wikipedia's quotation). |
| 81 | By the fifth century BC the smiths have moved to Sicily, next to Etna. Euripides... | FIX **material** | Euripides' Cyclopes are Homeric shepherds; smiths on Etna begin with Callimachus (3rd c.). |
| 82 | Thucydides counts the Cyclopes among Sicily's first inhabitants... "I cannot tell of what race they were" | PASS | Crawley 6.2.1 verbatim. "The earliest inhabitants spoken of". |
| 83 | Locals believed the smith god kept a forge on an Aeolian island | PASS | Crawley 3.88.3. |
| 84 | A forge under a volcano. It helps explain... | PASS | Hedged; Hiera is the volcanic island. |
| 85 | Aci Trezza... basalt, about half a million years old | UNVERIFIED | Legend and basalt confirmed; the age only via Wikipedia. |
| 86 | Theocritus gives Polyphemus a love life... one long unbroken eyebrow, and one eye | FIX (minor) | Quote exact (Lang). Philoxenus (c. 400 BC) wrote the love story first. |
| 87 | Plausible. Though nobody has shown... | PASS | Hedged. |
| 88 | Chip: SUSPECT 3 | PASS | Heading. |
| 89 | You can go and stand next to it | PASS | True of Tiryns and Mycenae. |
| 90 | Bronze Age walls... boulders so big | PASS | General. |
| 91 | Pausanias, second century AD... pair of mules could not move even the smallest | PASS | Jones 2.25.8 matches; Pausanias is a 2nd-century AD writer (Wikipedia). |
| 92 | Homer: 22 wagons. Pausanias: two mules. Greeks measured giants in livestock | FIX (minor) | Wagons are not livestock; not like-for-like (a door vs the smallest block). |
| 93 | He credits the Cyclopes with that wall, and Mycenae's wall and Lion Gate | FIX (minor) | 2.25.8 states it; 2.16.5 says "are said to be". |
| 94 | Lion Gate about 1250 BC... later Greeks assumed only Cyclopes could move stones | FIX **material** | Date fine (Wikipedia). Second sentence is stronger than any source I read; Pliny is not about moving stones. |
| 95 | Archaeologists still call the style cyclopean masonry | PASS | Wikipedia; standard term. |
| 96 | The wall is real. The giants were the Greeks' explanation | PASS | Pausanias 2.16.5, 2.25.8. |
| 97 | Chip: SUSPECT 4 | PASS | Heading. |
| 98 | Doesn't need an elephant, a smith, a wall. Not even Sicily | PASS | Structure. |
| 99 | A man is trapped by a giant, blinds him, gets away | PASS | ATU 1137 core. |
| 100 | More than two hundred versions, about twenty-five nations. Iceland... Korea | UNVERIFIED | "Over 200" verified (Hackman 1904 numbers 221). Twenty-five nations, Ireland, Korea not verified. |
| 101 | Most scholars think the tale is older than Homer | PASS | Fowler 2013 p. 55; Heubeck and Hoekstra p. 19 (quoted by Wikipedia). Hedged. |
| 102 | That does not rule out the skull. It does mean the story does not need one. | PASS | Fair inference. |
| 103 | Homer did not invent the Cyclops story. Best-known version | PASS | "On that view". Heubeck and Hoekstra: the fusion is "surely the work of the poet himself". |
| 104 | Smiths have Hesiod. Walls have Pausanias... elephant has a sailor from 1914 | FIX **material** | The sailor is the one imagined part; the elephant case also has real skulls. |
| 105 | As a one-eyed giant who eats sailors, no | PASS | Judgement. |
| 106 | The name is real... forge, wall, story, perhaps a skull | PASS | Hedged. |
| 107 | Who can prove where the Cyclops came from? | PASS | Mayor's "we just can't prove that". |
| 108 | ODY: Nobody. | PASS | Callback. |
| 109 | Next time: wind in the bag, witch with the wand, other monsters. Some have suspects of their own | UNVERIFIED | Aeolus's bag (10.19-24), Circe's wand (10.238, 319) verified. "Suspects" not researched. |
| 110 | He has just told a giant his name, and the giant has a father | PASS | 9.519, 9.529; Od. 1.68-73. |

---

## 2. Details for every FIX and UNVERIFIED (corrected wording ready to paste)

### Beat 05 (FIX, minor)
Abel (Colavito translation): "Sailors of Homeric or pre-Homeric times were probably the first to bring these giant customers into their homes. They were perhaps in a beach cave in Sicily and sought shelter from bad weather. In lighting a fire, they saw an elephant skull projecting from the clay." Abel imagines the discovery only, and he hedges it ("perhaps", "probably"). He does not describe the sailors' reaction or any eye looking back.
**Paste:** "That scene is adapted from a book of 1914. A palaeontologist, Othenio Abel, imagined sailors finding a skull in a beach cave, and thought it might be where the Cyclops came from."
(Abel is more confident than "might" ("probably"); "might" is the safe side.)

### Beats 10 and 11 (FIX, material)
The script says "Homer gives these characters lines." Homer gives direct speech at 20-22, 33-37, 41-43, 46, 49-50, 52-54. He gives only reported speech or inner thought at 15-16 (men beg, Odysseus refuses), 24-25 (Odysseus's own plan, 9.299-305) and 29 (Odysseus orders lots). Beats 26, 30, 31 are invented. The disclosure should say so.
**Paste (11):** "One note before we start. Where Homer gives these characters lines, we have tidied them up. Where he doesn't, we have made a few up. Everything else comes from sources."
**Paste (10 chip):** "DIALOGUE ADAPTED FROM HOMER, ODYSSEY 9 (SOME LINES INVENTED)"
**Paste (description line):** "Dialogue in the cave scene is adapted from Homer, Odyssey 9; a few lines are invented. Everything else is sourced below."
(+2 words; runtime effect under 1 s.)

### Beat 24 (FIX, material) and 25-26
Greek 9.299-305: "τὸν μὲν ἐγὼ βούλευσα κατὰ μεγαλήτορα θυμὸν ἆσσον ἰών, ξίφος ὀξὺ ἐρυσσάμενος ... ἕτερος δέ με θυμὸς ἔρυκεν. αὐτοῦ γάρ κε καὶ ἄμμες ἀπωλόμεθ' αἰπὺν ὄλεθρον· οὐ γὰρ κεν δυνάμεσθα θυράων ὑψηλάων χερσὶν ἀπώσασθαι λίθον ὄβριμον" (Odysseus's own thought; the visual also gives the sword to a crew sprite).
**Option A (faithful, keeps the gag):**
- 24 ODY: "He is asleep. I could kill him right now."
- 25 ODY: "And then who moves the stone?"
- 26 ODY: "...Ah."
Visual: Odysseus alone, sword half-drawn; crew sprite absent. Moves 13 words from CREW to ODY; metrics change slightly (crew 35 → about 28 words).
**Option B (keep as written):** keep 24-26 and rely on the revised beat 11 ("where he doesn't, we have made a few up"). Acceptable, but Option A is better because it shows the "who moves the stone" logic as Odysseus's own.

### Beat 29 (FIX, minor)
Odysseus orders the lots with no number (9.331-333: "ὅς τις τολμήσειεν ἐμοὶ σὺν μοχλὸν ἀείρας"). The narrator reports afterwards: "four, and I was the fifth" (9.334-335).
**Paste:** "Who helps me carry the stake? Draw lots."
Optional gag, Homer's own: the lots "fell on the very four I would have chosen myself" (9.334).

### Beat 48 (FIX, minor)
Greek 9.482-483: it falls "in front of the dark-prowed ship, and just failed to reach the tip of the steering-oar." Butler's "just in front of my ship so that it was within a little of hitting the end of the rudder" is closer than the script's compression. Murray calls it "the peak of a high mountain" (hill acceptable).
**Paste:** "...and the giant tears the top off a mountain and throws it. It lands just in front of the ship, a whisker from the rudder, and the wave carries the ship back toward shore."

### Beat 55 (FIX, material)
Odysseus wakes on Ithaca in Book 13 (13.187). The poem has 24 books, so he is home for the second half. "Most of the rest of the poem" is false for the text. In story time it is true (he returns "in the twentieth year", 2.175, 17.327; Poseidon rages "until he reached his own land", 1.20-21; the prayer's "late", "all his men gone" come true).
**Paste:** "Poseidon listens. It will be years before Odysseus sees Ithaca again."
Alternative: "Poseidon listens. And he never forgets."
(Beat 110 "the worst is behind him" still works.)

### Beat 61 (FIX, minor)
"Their bones turn up in caves, and still do": the sources show finds in caves (Zebbug Cave, Malta; Spinagallo Cave, Sicily; Abel 1914 "one finds even today remains" in caves near Messina, Palermo, Trapani). No source shows new finds now.
**Paste:** "Their bones have turned up in caves on Sicily and Malta. From the front, the skull shows two small eye sockets, low at the sides, and in the middle, one enormous hole."

### Beat 63 (FIX, material)
Discover's text: "That hole is, of course, a nasal cavity. But prior to the time of Alexander the Great, in the mid-fourth century B.C.E., ancient Greeks would never have seen a live elephant, and thus could easily have mistaken it for a large, singular eye socket." This follows a quote from Mayor in the same article but is the article's own prose. Independent context: the first confrontation between Europeans and Persian war elephants was Gaugamela, 331 BC (Wikipedia citing Arrian via Chinnock). I found no Mayor statement of it (her book not read).
**Paste (no Mayor attribution):** "Before Alexander the Great, most Greeks had never seen a live elephant. So a skull could easily have baffled them."
**Chip:** replace "ADRIENNE MAYOR, STANFORD" with "SOURCE: DISCOVER MAGAZINE", and let beat 67 introduce Mayor ("The folklorist Adrienne Mayor..." is fine: Wikipedia calls her "a historian of ancient science and a classical folklorist"; Discover calls her "a research scholar in the Classics Department at Stanford").

### Beat 64 (FIX, minor)
"Looking back at him with one great eye" is ours, not Abel's.
**Paste:** "So Abel pictured his sailors. A beach cave. A fire. A skull sticking out of the clay."
(If the callback needs the eye: visual only, no line.)

### Beat 70 (FIX, minor)
Abel: "Empedocles (492-432 BC) reported such discoveries and believed them to be remnants of an extinct giant race."
**Paste:** "Then there is the famous version. In Abel's telling, the philosopher Empedocles reported such bones on Sicily and took them for giants."

### Beat 72 (UNVERIFIED)
What I have: Wikipedia quotes the paper as saying "without his literary evidence [of the Empedocles story], Abel's geomyth becomes baseless: elephant fossils and myths of one-eyed monsters exist all over the world, and there is no evidence from historic texts or artwork that makes their connection in Sicily particularly notable or important", and says the claim has "no basis in any surviving records". Wikipedia cites the griffin paper's DOI for these. The paper's abstract, which I read in full, covers only the griffin. So the Abel passage is probably a section of a griffin paper (examples of "ex post facto geomyths"), unconfirmed.
Also: the quote says "Abel's geomyth", not "the whole idea". The script's "the whole idea" is looser.
**Paste (keeps the point, no verbatim claim):** "Take that story away, and two palaeontologists, Witton and Hing, say Abel's case is left baseless."
**Safer paste (survives if the paper turns out not to say this):** "No ancient source backs the Empedocles story, and without it, critics say, Abel's case is very thin."
**Description fix:** write the DOI entry as "Witton and Hing 2024, 'Did the horned dinosaur Protoceratops inspire the griffin?', Interdisciplinary Science Reviews 49: 363-388 (the discussion of Abel's Cyclops claim is cited second-hand)", so viewers who click the DOI are not surprised.

### Beat 73 (UNVERIFIED)
Verified in the OUP/Crossref abstract of the chapter (2020, pp. 8-35): "5. The eye... how convincing are such explanations—in terms, for example, of the skull of a dwarf elephant, or the cone of a volcano? The authors have serious doubts." The word "unfalsifiable" appears only in Wikipedia's own sentence ("lacking evidence and being unfalsifiable"), which is not a quotation from them. The "robust chain of argument" quote (via Wikipedia) concerns the volcanic and mud explanations.
**Paste:** "Two scholars of Greek myth, Aguirre and Buxton, say they have serious doubts about it."
The armchair gag can stay as a narrator joke: it no longer carries the word "unfalsifiable", so it is not attributed to them. Chip: "AGUIRRE & BUXTON, 2020".

### Beat 78 (FIX, minor)
Theogony 140-141: "οἳ Ζηνὶ βροντήν τε δόσαν τεῦξάν τε κεραυνόν" (gave Zeus thunder and made the thunderbolt). "Hammer" is the later forge image.
**Paste:** "They make the thunderbolt for Zeus. Homer's Cyclops keeps sheep, but Hesiod's has a career."

### Beat 81 (FIX, material)
Euripides' *Cyclops* (Shelley): set on "Aetna, the loftiest peak in Sicily"; the Cyclopes are "the one-eyed children of the Ocean God", shepherds and hunters ("Absent on Aetna, hunting with his dogs"). They are the Homeric kind, not the smiths. Wikipedia (citing Hard pp. 66, 166, Fowler, Bremmer): "later poets, beginning with the third-century BC poet Callimachus" make the Hesiodic Cyclopes Hephaestus's assistants at a forge under Etna or the Aeolian Islands. What holds from the fifth century BC is: Cyclopes of the Homeric type are placed on Sicily and the Aeolian Islands.
**Paste:** "By the fifth century BC, the Cyclopes have a Sicilian address, next to Mount Etna. Euripides sets a comic play there. Two centuries later, the poet Callimachus puts the smiths in the same neighbourhood, working for the smith god."
Trim version (same words as before, ±): "By the fifth century BC, the Cyclopes have moved to Sicily, next to Mount Etna. Euripides sets a comic play there."
Visual: keep the Etna map; the smith sprite pops in on "smiths" (beat 81 new last sentence), not before. Beat 84 stays.

### Beat 85 (UNVERIFIED)
Verified: the legend (it.wikipedia Aci Trezza: eight basalt stacks "che, secondo la leggenda, furono lanciati da Polifemo ad Ulisse"); basalt. Not verified: the age. Wikipedia "Cyclopean Isles" says "formed about 500,000 years ago"; Wikipedia "Mount Etna" says Etna's first (submarine) eruptions were about 500,000 years ago, citing a USGS page whose URL now returns an error. I found no geology paper dating these particular stacks.
**Paste:** "At Aci Trezza, on Sicily's coast, locals will show you the boulders Polyphemus hurled at Odysseus. They are volcanic basalt, hundreds of thousands of years old. Local legend, not archaeology."
Counter: "HUNDREDS OF THOUSANDS OF YEARS" or cut the counter. (If "about half a million" is wanted, add "from Etna's earliest eruptions" only after reading Branca et al. 2011.)

### Beat 86 (FIX, minor)
Lang, Idyll 11: "one long unbroken eyebrow. And but one eye is on my forehead" (exact). But "gives Polyphemus a love life" implies he invented it. Philoxenus of Cythera (about 400 BC; Wikipedia "Polyphemus") wrote the Cyclops/Galatea dithyramb first; Theocritus is the best-preserved version.
**Paste:** "In the third century BC, Theocritus has Polyphemus sing a love song to a sea nymph. He frets about his looks: one long unbroken eyebrow, and one eye."

### Beat 92 (FIX, minor)
Wagons are not livestock, and a door and the smallest wall block are not like for like.
**Paste:** "Homer: twenty-two wagons for one door. Pausanias: two mules, and the stone wins. The Greeks measured giants in wagons and mules."

### Beat 93 (FIX, minor)
Jones 2.25.8 says it in Pausanias's own voice ("is a work of the Cyclopes"). 2.16.5: "These, too, are said to be the work of the Cyclopes."
**Paste:** "He reports that the Cyclopes built that wall, and, so locals say, Mycenae's wall and Lion Gate too."

### Beat 94 (FIX, material)
Lion Gate "built circa 1250 BC" (Wikipedia; fine). "Later Greeks assumed only Cyclopes could move stones like that" is a textbook gloss (Wikipedia: "the assumption of classical Greeks that only the mythical Cyclopes had the strength"); the Pliny cite attached to it (NH 7.195) concerns Aristotle's claim that Cyclopes invented towers. The solid source is Pausanias.
**Paste:** "The Lion Gate is about 1250 BC. People built it, and later Greeks credited the Cyclopes."

### Beat 100 (UNVERIFIED in part)
Verified from the primary (Hackman, *Die Polyphemsage in der Volksüberlieferung*, 1904, archive.org full-text OCR): the catalogue ends at "N:r 221"; it includes Icelandic (a faded version in Egil's saga, in his comparative section), Portuguese (Portugal/Galicia border), Arabic (*Thousand and One Nights*), Turkic (Oghuz; Altai), Russian, among many peoples named in its headings. NOT found in Hackman: Ireland (no Irish heading and zero hits for "Irland"; he has a "Galen" (Gaelic) heading, and the bibliography I saw lists Mac Innes, which I did not trace to Ireland or Scotland), Korea (zero hits). "Twenty-five nations" and the Ireland and Korea entries come only from Wikipedia citing Glenn 1971 p. 134 (not read).
**Paste:** "Scholars have recorded more than two hundred versions, from Iceland to Turkey and Arabia, Russia and Portugal."
(Drops "about twenty-five nations", Ireland and Korea. Add them back only after reading Glenn 1971, TAPA 102, p. 134. Visual: pins on Iceland, Portugal, Turkey, Arabia, Russia.)

### Beat 104 (FIX, material)
"The elephant has a sailor from 1914": the sailor is the imagined part, so the line shortchanges the case (real skulls, Mayor's fossil-hunter evidence) and could read as sneering. Truth: real skulls, imagined sailor.
**Paste:** "Four suspects. The smiths have Hesiod. The walls have Pausanias. The folktale has two hundred versions. The elephant has real skulls, and an imaginary sailor."

### Beat 109 (UNVERIFIED, second sentence)
Verified: Aeolus's bag (10.19-24), Circe's wand (10.238, 319). Not researched: that "some have suspects of their own" (Scylla, Charybdis, Sirens, Laestrygonians). Plausible but unsourced.
**Paste:** "Next time: the wind in the bag, the witch with the wand, and the other monsters of the Odyssey."

### Non-FIX notes worth knowing (all PASS)
- **34:** the script's "unmixed" is better supported than the risk row feared. Greek 9.204-205: jars of "ἡδὺν ἀκηράσιον" (sweet, unmixed wine); 9.212: Odysseus filled the skin from them. The 20:1 water is Maron's household mixing (9.208-210, "whenever they drank"), and one cup wine to twenty measures water. Homer never says Odysseus serves it neat, but nothing suggests he waters it. Butler's "unblended" qualifies the jars, as the Greek does. Keep.
- **54:** Greek 9.534 "ὀλέσας ἄπο πάντας ἑταίρους" ("having lost all his companions") is in the Greek and in Murray's text; only the following lines are bracketed in Butler. The risk row can be closed. "Father": Polyphemus says "πατὴρ δ' ἐμὸς εὔχεται εἶναι" (9.519) and "πατὴρ δ' ἐμὸς εὔχεαι εἶναι" (9.529). The opening "Father Poseidon, hear me" is tidying of "κλῦθι, Ποσείδαον γαιήοχε". The Cyclopes' "pray to your father" (9.412) is Butler's reading; Murray renders "our father".
- **56:** see Appendix A on scope; the claim can safely be broadened from "Book Nine" to "the Odyssey" if wanted. Pope's 1725 translation inserts "From all their dens the one-eyed race repair": a translator's word, not Homer's. Mention only if William wants a caveat.
- **43:** the Cyclopes' "let us sleep" is in their *first* question (9.404 "ἀύπνους ἄμμε τίθησθα"), not in their reply. It is compressed into one speech; same speaker, so nothing is misattributed.
- **19:** on night one only the ewes and she-goats go in; the rams and he-goats stay in the yard. On night two "all inside" (the reason the rams are there at dawn). Optional tightening: "drives his ewes and nanny goats inside".
- **27/28/33:** Homer's order is first supper (2), breakfast (2), the day of preparing the stake, second supper (2), then the wine. Beat 27 reports all six before the stake (28-32), so the counter at 6 is slightly early at beats 28-32 (eight men alive at the time). Visual only.

---

## 3. Sources newly accessed (what was readable)

| Source | URL | Accessed |
|---|---|---|
| Homer, Odyssey, Greek (Allen, Perseus) | https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml | **Full text, all 24 books**; searched for μετωπ-, μον-, ἕνα/εἷς ὀφθαλμ-, all ὀφθαλμ- forms; read 9.104-118, 186-215, 240-243, 287-298, 299-306, 309-316, 327-336, 342-371, 398-412, 424-460, 471-545; 1.19-21, 68-75; 6.4-6; 10.19-24, 238. |
| Homer, Odyssey, Murray (Loeb) | .../tlg0012.tlg002.perseus-eng3.xml | **Full text**; searched "one eye", "forehead" in all books. |
| Homer, Odyssey, Butler | https://www.gutenberg.org/cache/epub/1727/pg1727.txt | **Full text**; Book 9 read line by line. |
| Homer, Iliad, Greek | .../tlg0012.tlg001.perseus-grc2.xml | **Full text**; searched for Κύκλωπ- and μονοφθ-: none. |
| Pope's Odyssey; Chapman's Odyssey | https://www.gutenberg.org/cache/epub/3160/pg3160.txt ; .../48895/pg48895.txt | **Full text**, searched ("one eye", "forehead", "one-eyed"); Pope Book 9 read for eye wording. |
| Hesiod, Theogony (Evelyn-White; Greek) | .../tlg0020/tlg001/ (eng2, grc2) | **Full text**; 139-146 read. |
| Euripides, Cyclops (Shelley) | https://en.wikisource.org/wiki/Cyclops_(Shelley_1824) | **Full text**; searched Aetna, Sicily, forge, Vulcan, one eye. |
| Theocritus, Idylls (Lang) | https://www.gutenberg.org/cache/epub/4775/pg4775.txt | **Full text**; Idyll 11 read. |
| Thucydides 6.2, 3.88 (Crawley) | .../tlg0003/tlg001/tlg0003.tlg001.perseus-eng6.xml | **Full text**; both chapters read. |
| Pausanias 2.16, 2.25 (Jones; Greek) | .../tlg0525/tlg001/ (eng2, grc2) | **Full text**; both chapters read. |
| Abel 1914, tr. Colavito | https://www.jasoncolavito.com/fossil-origin-of-the-cyclops.html | **Full translated passage** (pp. 31-33 of the book) plus Colavito's introductory note. Original German not seen. |
| Discover Magazine (Mayor) | https://www.discovermagazine.com/one-eyed-looking-mammoth-fossils-may-have-inspired-origins-of-the-cyclops-45824 | **Full article** (via web_fetch; plain curl got a CloudFront 403). |
| Hackman, *Die Polyphemsage* (1904) | https://archive.org/download/diepolyphemsage00hackgoog/diepolyphemsage00hackgoog_djvu.txt | **Full text (OCR, German)**; catalogue headings, final number (221), Icelandic, Arabic, Portuguese, Turkic entries. |
| OUP abstract of Aguirre and Buxton ch. 2 | https://api.crossref.org/works/10.1093/oso/9780198713777.003.0002 | **Abstract in full** ("The authors have serious doubts"). Chapter not read. |
| BMCR review of Aguirre and Buxton (2021.07.10) | https://bmcr.brynmawr.edu/2021/2021.07.10/ | **Full review**; does not discuss the elephant claim or "unfalsifiable". |
| Witton and Hing 2024 | https://doi.org/10.1177/03080188241255543 | **Metadata and abstract only** (Crossref, OpenAlex, Portsmouth portal page). Full text: Cloudflare check on SAGE, T&F, the Portsmouth file host, ResearchGate, OUP, Europe PMC web. A managed-browser attempt ended at a "Verify you are human" tick-box; not clicked. |
| Wikipedia (raw): Cyclopes, Polyphemus, Cyclopean masonry, Lion Gate, Cyclopean Isles, Aci Trezza, Mount Etna, Palaeoloxodon falconeri, Pausanias, Galatea, War elephant, Adrienne Mayor; it.wikipedia Aci Trezza, Isola Lachea | en/it.wikipedia.org, `action=raw` | Full wikitext, for quotations and citation trails only (pointers, not authority). |
| Herridge and Lister 2012 abstract (Europe PMC) | https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1098/rspb.2012.0671 | Abstract only. Full text not retrievable. |
| Larramendi and Palombo 2015 (Spinagallo size figures) | via Wikipedia's account | Secondary only. |

Not reachable (blocked or rate-limited, not circumvented): Google Books (429), OUP Academic (Cloudflare), SAGE/T&F (Cloudflare), JSTOR (Glenn 1971), Semantic Scholar snippets (429), DuckDuckGo (bot challenge), Royal Society (Cloudflare), USGS Etna page (dead URL).

### Label changes (V/E/U)
| Item | Script label | New label | Why |
|---|---|---|---|
| Homer Book 9 facts used in Act 1 (A5-A16, N1-N6) | V | V (upgraded: now checked against the Greek) | Line references in Appendix A. |
| A13 "never writes one eye / forehead" | V (Book 9) | V for the whole Odyssey and Iliad (Greek) | Greek: no μετωπ- for the Cyclops; no ὀφθαλμ- plural for him; Iliad has no Cyclopes. |
| C3 Abel's imagined scene | V | V, with Abel's hedges ("perhaps", "probably") | Abel's text read in full. |
| C4 Abel claimed Empedocles | V | V (Abel: "reported such discoveries") | Same passage. |
| C4 Colavito's note | V | V, exact words | Same page. |
| C4 "no surviving source" and Witton and Hing quote | E | **U** for the paper itself; E via Wikipedia for the words | DOI is the griffin paper; Abel/Empedocles passage unconfirmed. |
| C5 Aguirre and Buxton "unfalsifiable" | V via Wikipedia | **U** for the word; V for "serious doubts" (OUP abstract) | Wikipedia's wording is its own. |
| C7 Mayor verbatim quote | V | V (exact) | Discover text read. |
| C8 Mayor on elephants before Alexander | V | **U as Mayor's claim** (journalist's sentence) | Misattributed in V1. |
| C13 "more than two hundred versions" | V via Wikipedia | V (Hackman 221, 1904, primary) | Catalogue ends at N:r 221. |
| C13 "about twenty-five nations", Ireland, Korea | V via Wikipedia | **U** | Not in Hackman; Glenn 1971 not read. |
| C13 "most scholars: older than Homer" | V via Wikipedia | E-strong | Quotes of Fowler p. 55 and Heubeck and Hoekstra p. 19 via Wikipedia; books not read. |
| D1, D2, D4 (Thucydides, Pausanias) | V | V (re-read) | Texts match the script. |
| D4 Pausanias date "second century AD" | E-low | V (Wikipedia: "2nd-century AD") | Standard. |
| D5 Lion Gate c. 1250 BC | V via Wikipedia | V via Wikipedia (still secondary) | No better source reached. |
| D5 "assumed only Cyclopes could move stones" | V via Wikipedia | **E (gloss)** | Pausanias gives the solid version. |
| D6 Aci Trezza age | V via Wikipedia | **U** (precision) | Only Wikipedia. |
| B9 Burkert | V (that he suggested it) | V via Wikipedia's quotation, Greek Religion p. 173 | Book not read. |
| D3 smiths on Sicily by 5th c. | V | **Wrong date**; 3rd c. (Callimachus) via Hard/Fowler/Bremmer on Wikipedia | Euripides' Cyclopes are shepherds. |
| C10 "under 1 m" | V via Wikipedia | V via Wikipedia (Larramendi and Palombo 2015); Herridge and Lister 2012 abstract corroborates "smallest" | Both secondary. |
| B5 Theocritus quote | V | V (exact) | Lang read. |

### Where the script is stricter or looser than the source
**Looser (needs fixing):** 63 (attributes a journalist's claim to Mayor); 72 ("whole idea" vs "Abel's geomyth"; paper unread); 73 ("unfalsifiable" not in any source I read); 81 (smiths on Sicily a century or two too early); 94 (assumption claim); 100 (nations list); 93 ("credits" vs "are said to be"); 55 (poem vs story time); 86 (implied invention); 78 ("hammer"); 11 (Homer "gives" all lines); 24 (speaker); 29 (number in Odysseus's mouth); 70 ("found" vs "reported").
**Stricter (safe):** 05 and 64 ("might" where Abel says "probably"); 56 (scoped to Book Nine when the Greek supports the whole Odyssey); 12 (scoped to Book Nine); 74 and the UNPROVEN stamp (Mayor says "distinct possibility"); 68 (quote verbatim, not paraphrase).

---

## 4. Remaining risks that cannot be resolved without reading X

1. **Witton and Hing 2024, *Interdisciplinary Science Reviews* 49(3-4): 363-388**, open access (CC BY-NC) at https://doi.org/10.1177/03080188241255543. Need: the passage on Abel's Cyclops claim (search the PDF for "Abel", "Empedocles", "baseless", "Cyclop"); confirm the exact words, whether it is a section or a footnote, and whether "the whole idea" vs "Abel's geomyth" is theirs. A human with a normal browser can open it in a minute. Beat 72 stays UNVERIFIED until then.
2. **Aguirre and Buxton, *Cyclops: The Myth and Its Cultural History* (OUP 2020), ch. 2 "Seven Ways to Approach a Cyclops", pp. 8-35**: the section headed "The eye" (item 5 in the abstract). Need: whether they use "unfalsifiable" or similar, and what they say about the dwarf elephant. The "air of plausibility" and "robust chain of argument" quotes (via Wikipedia) concern the volcano and mud theories, so confirm that too. Beat 73 needs this.
3. **Mayor, *The First Fossil Hunters* (Princeton 2000; revised 2011)**: the pages on the Cyclops and on elephants (look under "Cyclopes", "Polyphemus", "Abel", "Alexander the Great", "elephants" in the index). Need: whether she herself says Greeks had not seen live elephants before Alexander, and what she says of Abel's Empedocles claim (she may repeat it, which would sharpen beat 71's "no ancient source").
4. **Glenn, "The Polyphemus Folktale and Homer's Kyklôpeia", *TAPA* 102 (1971) 133-181, p. 134** (JSTOR 2935942): "about twenty-five nations", Ireland, Korea. And **Heubeck and Hoekstra, *A Commentary on Homer's Odyssey* vol. II (1989/1990), pp. 19-20** and **Fowler, *Early Greek Mythography* vol. II (2013), p. 55**, for the "older than Homer" quotes and the "fusion is the poet's own" nuance (relevant to beat 103).
5. **Burkert, *Greek Religion* (Harvard UP 1985; Blackwell 1991), p. 173**: confirm the "smith guilds" sentence and that it concerns the Hesiodic Cyclopes. (Pagination may differ between the 1985 and 1991 editions.)
6. **Callimachus, *Hymn to Artemis* (Hymn 3), about lines 46-61**, and **Hard, *The Routledge Handbook of Greek Mythology*, pp. 66 and 166**: for beat 81's "Callimachus puts the smiths there". Wikipedia's account is the only route I used.
7. **Branca et al. 2011, "Geological evolution of Etna volcano" (GSA/IAVCEI) or a local geology source (Univ. of Catania / CUTGANA) on the Aci Trezza stacks' age**: for beat 85 if William wants a number.
8. **Larramendi and Palombo 2015, *Hystrix* 26(2)**, for the 96.5 cm / 80 cm shoulder heights if the "under a metre" on-screen label is to cite a paper rather than Wikipedia.
9. **Abel's German original (*Die Tiere der Vorwelt*, 1914, pp. 31-33) and Fig. 5**: only the translation was read; the DG-01 plate source should be checked for its licence and that it shows a Sicilian dwarf elephant, not another species.
10. **Philoxenus's *Cyclops or Galatea*** (beat 86 note): date and priority over Theocritus rest on Wikipedia.

---

## Appendix A: Homer, Odyssey 9, beat-by-beat against the Greek (Act 1 and the turn)

| Check | Result |
|---|---|
| Six men eaten, three meals of two | 9.289 (first supper), 9.311 (breakfast), 9.344 (second evening). ✓ Order in the script: 23 first supper, 27 breakfast then "the next night". The wine scene follows the second supper (9.344-347), so at beat 33 six are gone. |
| Lots | 9.331-335: Odysseus orders the others to cast lots; "four, and I was the fifth". ✓ Four by lot plus Odysseus. |
| Twenty-two wagons | 9.241-242 δύω καὶ εἴκοσ' ἄμαξαι ἐσθλαὶ τετράκυκλοι. ✓ |
| Wine | 9.196-212: Maron, son of Euanthes, priest of Apollo; twelve jars ἀκηράσιον (unmixed); 9.209 one cup into twenty measures of water; skin filled from the jars. Butler "unblended" = jars. ✓ No line shows Odysseus pouring neat; none shows him mixing. |
| Three bowls | 9.360-361 τρὶς μὲν ἔδωκα, τρὶς δ' ἔκπιεν. ✓ The name is asked after bowl one (9.355-356), given after three (9.364-367). |
| Name exchange | 9.366-367 Οὖτις; "μήτηρ ἠδὲ πατὴρ ἠδ' ἄλλοι πάντες ἑταῖροι". 9.369-370 "I will eat Nobody last after his comrades... this will be your guest-gift". ✓ |
| Other Cyclopes | 9.399-412. Their first question mentions sleeplessness (9.404); reply: illness from Zeus, pray to your father Poseidon (9.410-412). ✓ |
| Sheep in threes | 9.425-433 (σύντρεις; man under the middle one; Odysseus under the best ram). 9.441-443 he feels the backs. ✓ |
| Ram speech | 9.447-460. ✓ He names "Nobody" (Οὖτις), not Odysseus. |
| Departure order | first jeer 9.474-479; rock 1 9.481-486 (wave to land); Odysseus poles off 9.487-490; crew plead 9.491-499; second shout with the name 9.502-505; Telemus and "weakling" 9.506-521; Odysseus's retort 9.523-525; prayer 9.528-535; Poseidon hears 9.536; rock 2 9.537-542 (behind the ship; wave drives it forward). Script order ✓. |
| Telemus | 9.508-512 Τήλεμος Εὐρυμίδης. "Weakling": ὀλίγος τε καὶ οὐτιδανὸς καὶ ἄκικυς (9.515). ✓ |
| Prayer | 9.528-535 as in beat 54. ✓ |
| "Father" | Polyphemus says it in 9.519 and 9.529 (and Od. 1.71-73 gives Poseidon as father). ✓ |
| "Never says where" (12) | 9.106 "land of the Cyclopes" only; the Odyssey elsewhere has Thrinacia (cattle of Helios), Sicels and Sicania (20.383, 24.307 etc.) but never links them to the Cyclopes. ✓ |
| "Never writes one eye / forehead" (56) | Greek, whole Odyssey: 0 hits for μετωπ- applied to the Cyclops (the 9 hits are cattle and men), 0 for μονοφθ-, μονωπ-, ἕνα/εἷς ὀφθαλμ-. Book 9 eye words: ὀφθαλμῷ (333, 383, 387), ὀφθαλμός (394), ὀφθαλμοῖο (397), ὀφθαλμόν (453), ὀφθαλμοῦ (503, 516), ὀφθαλμόν (525); 389 βλέφαρ' ... ὀφρύας is plural eyelids and brows (not "eyes"). 146 plural ὀφθαλμοῖσιν is the crew. Murray and Butler English, all books: no "one eye"; no Cyclops forehead. Iliad: no Cyclopes. Scholars via Wikipedia: West 1966 (on Theogony 139) "the story of [Polyphemus'] blinding presupposes that he is one-eyed ... though this is not explicitly stated"; Heubeck and Hoekstra p. 20 "the poet, surely intentionally ... omits any direct reference". Pope 1725 adds "one-eyed". ✓ |

## Appendix B: Mayor in Discover, full context (all words quoted)
- "Anyone who goes to a natural history museum and looks at the skull of an elephant can see that the eye sockets are negligible... What you notice is the gigantic hole in the middle of the skull that looks like a single eye."
- Journalist: "That hole is, of course, a nasal cavity. But prior to the time of Alexander the Great... ancient Greeks would never have seen a live elephant..."
- Journalist: "there's no evidence to confirm whether the remains of these animals predated the myths themselves — it could also be that these myths already existed, and the fossil discoveries simply confirmed them, Mayor notes." Then Mayor: "We don't know which comes first. I don't like to say that the fossils inspired, or were the source of the story, because we just can't prove that."
- Mayor: "I think there's no doubt that fossils influenced the way the ancient Greeks and Romans pictured mythological stories about giants, monsters, and fabulous creatures."
Beat 68 is verbatim and in context (about which came first), and beat 67 "careful" is fair. A fair-minded viewer note: the same article has her saying fossils clearly shaped how Greeks pictured monsters. If William wants balance, add to beat 69: "She does think fossils shaped how Greeks pictured giants. She just won't say they started this one."

## Appendix C: Internal consistency
- Counts reproduced with an independent parser (same tokenisation as `metrics.py`): 110 beats, ids 1-110 contiguous; **1,755 words**; NARR 1,435, ODY 120, POLY 134, CREW 35, CYC2 31 (sum 1,755); character lines 28; character share 320 words = 18.2%; 77 NARR beats, 5 chips. ✓ matches end matter (a).
- Runtime: 1,755/170 = 10.32 min = 10:19; /165 = 10:38; /175 = 10:02. ✓ Section words at 170 wpm: cold open 138 (49 s), Act 1 721 (254 s), turn 53 (19 s), suspect 1 274 (97 s), suspect 2 223 (79 s), suspect 3 137 (48 s), suspect 4 99 (35 s), verdict 110 (39 s); cumulative ends 0:49, 5:03, 5:22, 6:59, 8:17, 9:06, 9:41, 10:19. ✓ (suspect 2 ends 8:17 rather than the header's 8:18: rounding.) Cold open plus Act 1 = 303 s of 620 s = 48.9% ✓ "49%".
- Counters: "12 MEN" (13) → 10 (23) → 10, 8, 6 (27): the first cut at 27 shows 10 again; harmless but cut to "8, 6". "22 WAGONS" at 19, 25, 92 ✓; "2 MULES" at 91, 92 ✓; "500,000 YEARS" only at 85 (see fix); dates 1914 (05, 104), c. 1250 BC (94), 700 BC (77), 3rd c. (86), 5th c. (81), 2nd c. AD (91). Odysseus is the 13th person in the cave; "12 MEN" counts the comrades (correct). Six comrades survive, plus Odysseus.
- Order of the four suspects and stamps: board order elephant, smiths, walls, folktale (58-104); stamps UNPROVEN (74), PLAUSIBLE (87), REAL (96), PROBABLY OLDER (103) in that order; tease at 08 (elephant, touchable wall) matches. ✓ Beat 104 lists the suspects in the same order.
- Speakers: every spoken character line matches the speaker Homer gives it, except 24 (see fix). 41-43 CYC2 collective ✓; 20, 22, 35, 37, 42, 46, 52, 54 POLY ✓; 21, 33, 36, 50, 53 ODY ✓; 49 CREW ✓ (Homer: ἑταῖροι).
- "NOT to make" list (RESEARCH-V1 section 3): scanned all 110 beats. No beat says the Greeks identified the skulls; Empedocles appears only as "in Abel's telling" (and, after fix, "reported"); no "solved/proved"; "Homer says Sicily" nowhere (Sicily appears only for elephants, Thucydides, Euripides, Aci Trezza); no "Cyclops means one eye"; no skull size; no named cave; beat 54/110 keep Poseidon-as-father to Polyphemus only; no cyclopia; no total of men lost beyond the six; no Tilos; no "ten years after Troy"; no Strabo/Naples. ✓ One near miss: beat 81 ("the smiths have moved to Sicily") conflicts with RESEARCH-V1 D3/B4 as actually evidenced; FIX above.
- Section (d) risk rows now: **closed** 12, 34, 54, 56, 91; **upgraded to FIX** 63, 94, 104; **still open** 72, 73, 85, 100, 109; **resolved differently** 71 (no change), 68 (verbatim confirmed).
- Alt cold opens (section c): Alt B "Homer never says so... Search Book Nine for 'one eye'" ✓ (now safe even without "Book Nine"). Alt C "Twelve men follow Odysseus into a cave. Six of them walk out." ✓ (six of the twelve; Odysseus walks out too).
- Description (section f): add the full title to the Witton and Hing entry; Euripides entry should say "set on Etna; the Cyclopes are shepherds"; Hesiod entry fine.
