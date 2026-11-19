# SPOKEN-TEXT.md: exactly what was sent to the voice, video 1 (SCRIPT-V3, method A2)

Voice Daniel (`onwK4e9ZLuTAKqWW03F9`), `eleven_multilingual_v2`, stability 0.5, style 0.2, speed 1.0, similarity 0.75, speaker boost on. No audio tags. One continuous call per passage (16 passages), `previous_text` / `next_text` = the neighbouring passages' text. Beats are separated by a blank line inside a passage (as in round-3 A2). TEXT-CHIP beats 59, 81, 97, 106 are on screen only and are not in the text.

## What the A2 technique adds or changes (nothing else was altered)

1. **Quotation marks** around every character line (never spoken, but they set the voice up as a quotation). A final full stop becomes a comma when an attribution follows (`...Have some wine," said Odysseus`); `?` and `!` stay.
2. **Attribution words** after 21 of the 35 character lines (listed below). These words are **spoken**: 62 words in all, tagged `added: true` and `speaker: NARR` in `words.json`, kept out of `beats_timing.json` `start`/`end` (they get their own `attribution` span). Seven are exactly as in round-3 A2 (28, 30, 31, 37, 38, 39, 64); fourteen are new, same pattern.
3. **No attribution** on the 14 remaining character lines: replies inside an exchange (15, 16, 19, 25, 32, 33, 50, 53, 86) and the one-word gags / punchlines (20 `Ah.`, 66 `Nope.`, 68, 116 `Rude.`, 119 `Nobody.`) as in A2's 32, 33, 66, 68.
4. **TTS-only respellings** (the saved script is never altered; each is one token for one token so words map back 1:1): Polyphemus → Pollifeemus, Empedocles → Em-peddokleez, Theocritus → Thee-ockritus, Thucydides → Thoo-sididdeez, Tiryns → Tie-rinz, Pausanias → Paw-sayneeus, Brontes → Bron-teez, Steropes → Stair-oh-peez, Arges → Ar-geez, Aci → Ah-chee, Trezza → Tret-sah, Aguirre → Ah-gheereh, Burkert → Boor-kert, BC → B.C.. `Othenio Abel` is never spoken in V3 (beat 62 says "Abel"); William's approved plain-text handling is kept, with no respelling. Not respelled: Odysseus, Hesiod, Callimachus, Laertes, Ithaca, Poseidon, Euripides, Mycenae, Etna, Colavito, Buxton, Hackman, Mayor, Aeolian.
5. Numbers are as written in the script (words, e.g. "Twenty-two", "twelve fifty"). `BC` was sent as `B.C.` (beats 83, 90, 91, 95, 104).

### Attribution words added (spoken, not in the script)

| beat | speaker | words added | time |
|---|---|---|---|
| 9 | CREW | the crew urged. | 0:55.61 |
| 10 | ODY | said Odysseus. | 1:00.67 |
| 14 | POLY | the giant asked. | 1:25.03 |
| 18 | ODY | Odysseus thought. | 1:48.41 |
| 23 | ODY | said Odysseus. | 2:12.57 |
| 24 | CREW | a crewman asked. | 2:14.94 |
| 28 | ODY | said Odysseus, quite calmly. | 2:32.29 |
| 30 | POLY | the giant rumbled. | 2:47.79 |
| 31 | ODY | said Odysseus. | 2:50.31 |
| 37 | CYC2 | a Cyclops asked, bored. | 3:17.12 |
| 38 | POLY | the giant bellowed. | 3:23.33 |
| 39 | CYC2 | the Cyclops said flatly. | 3:31.31 |
| 44 | POLY | the giant said softly. | 4:01.50 |
| 49 | CREW | the crew begged. | 4:28.88 |
| 52 | POLY | the giant called. | 4:50.88 |
| 54 | POLY | the giant prayed. | 5:09.82 |
| 64 | CREW | the sailor asked. | 6:14.37 |
| 75 | CREW | the sailor asked. | 7:24.92 |
| 85 | POLY | the giant said awkwardly. | 8:14.07 |
| 100 | CREW | a crewman asked. | 9:41.51 |
| 111 | ODY | Odysseus muttered. | 10:59.68 |

Total added words: 63.

## Per beat

`script` = SCRIPT-V3.md wording; `sent` = the exact text in the TTS call (quotes, attribution and respellings included). Identical except where shown.

### P01 · cold open · beats 1-5 · 480 characters

- **01 · NARR** (0:00.40-0:04.32)
  - script: Twelve men follow Odysseus into a cave. Six of them get out.
- **02 · NARR** (0:04.72-0:09.86)
  - script: A giant ate the other six, the one-eyed kind. So where did he come from?
- **03 · NARR** (0:10.26-0:18.82)
  - script: We have four suspects, and a verdict on each. One is an elephant skull. Another, you can still walk up to and touch.
- **04 · NARR** (0:19.22-0:30.73)
  - script: One note before we start. Where Homer gives these characters lines, we have tidied them up. Where he doesn't, we have made a few up. Everything else comes from sources.
- **05 · NARR** (0:31.13-0:35.84)
  - script: But first, a poem. And a very bad decision about cheese.

### P02 · act 1: arrival · beats 6-13 · 619 characters

- **06 · NARR** (0:36.19-0:43.72)
  - script: Sailing home from Troy, Odysseus lands in the country of the Cyclopes. Book Nine never says where.
- **07 · NARR** (0:44.12-0:48.87)
  - script: He picks twelve men, takes a goatskin of wine, and walks up to a cave.
- **08 · NARR** (0:49.25-0:53.31)
  - script: Racks of cheese. Pens full of lambs. Nobody home.
- **09 · CREW** (0:53.63-0:55.29)
  - script: Take the cheese. Let's go.
  - sent: "Take the cheese. Let's go," the crew urged.
- **10 · ODY** (0:56.73-1:00.42)
  - script: No. I want to meet the owner. He might give us a present.
  - sent: "No. I want to meet the owner. He might give us a present," said Odysseus.
- **11 · NARR** (1:01.76-1:06.54)
  - script: The cleverest man in the poem is waiting for a gift basket from a stranger's cave.
- **12 · NARR** (1:06.94-1:12.43)
  - script: The owner comes home. He looks less like a man than a wooded peak, standing alone.
- **13 · NARR** (1:12.83-1:20.61)
  - script: He drives his flock inside, then rolls a stone across the door. Twenty-two wagons could not have moved it.

### P03 · act 1: the owner · beats 14-21 · 514 characters

- **14 · POLY** (1:21.01-1:24.72)
  - script: Strangers, who are you? Traders, or pirates?
  - sent: "Strangers, who are you? Traders, or pirates?" the giant asked.
- **15 · ODY** (1:26.12-1:33.33)
  - script: We are Greeks, heading home from Troy. We ask for hospitality. Remember: Zeus protects guests.
  - sent: "We are Greeks, heading home from Troy. We ask for hospitality. Remember: Zeus protects guests."
- **16 · POLY** (1:33.61-1:38.48)
  - script: Zeus? We Cyclopes don't care about Zeus. We are stronger than the gods.
  - sent: "Zeus? We Cyclopes don't care about Zeus. We are stronger than the gods."
- **17 · NARR** (1:38.81-1:45.07)
  - script: That is not a good answer. He grabs two of the men for supper, then falls asleep among his sheep.
- **18 · ODY** (1:45.39-1:47.98)
  - script: He is asleep. I could kill him right now.
  - sent: "He is asleep. I could kill him right now," Odysseus thought.
- **19 · ODY** (1:49.50-1:50.98)
  - script: And then who moves the stone?
  - sent: "And then who moves the stone?"
- **20 · ODY** (1:51.53-1:51.89)
  - script: Ah.
  - sent: "Ah."
- **21 · NARR** (1:52.21-1:58.70)
  - script: At breakfast, two more men go. Homer gives the details. We will spare you.

### P04 · act 1: the stake, the wine, Nobody · beats 22-34 · 891 characters

- **22 · NARR** (1:59.05-2:09.29)
  - script: Odysseus finds the giant's own club, an olive trunk as big as a ship's mast. He cuts off a length, sharpens it, and hardens the point in the fire.
- **23 · ODY** (2:09.61-2:12.28)
  - script: Who helps me carry the stake? Draw lots.
  - sent: "Who helps me carry the stake? Draw lots," said Odysseus.
- **24 · CREW** (2:13.66-2:14.62)
  - script: And if he wakes up?
  - sent: "And if he wakes up?" a crewman asked.
- **25 · ODY** (2:16.06-2:17.80)
  - script: Then it was a short plan.
  - sent: "Then it was a short plan."
- **26 · NARR** (2:18.12-2:23.68)
  - script: He hides the stake under dung, the one thing a cave full of sheep has plenty of.
- **27 · NARR** (2:24.08-2:27.72)
  - script: That evening, two more. Six men gone.
- **28 · ODY** (2:28.04-2:32.22)
  - script: You have eaten a great deal of man's flesh, Cyclops. Have some wine.
  - sent: "You have eaten a great deal of man's flesh, Cyclops. Have some wine," said Odysseus, quite calmly.
- **29 · NARR** (2:34.18-2:43.57)
  - script: The wine comes from a priest of Apollo, whose household drank it mixed twenty parts water to one. The giant drinks three bowls. Homer counts.
- **30 · POLY** (2:43.89-2:47.55)
  - script: More. Now tell me your name, and I will give you a present.
  - sent: "More. Now tell me your name, and I will give you a present," the giant rumbled.
- **31 · ODY** (2:49.03-2:50.08)
  - script: My name is Nobody.
  - sent: "My name is Nobody," said Odysseus.
- **32 · POLY** (2:51.33-2:58.64)
  - script: Nobody. Then here is my present, Nobody. I will eat Nobody's friends first, and Nobody last.
  - sent: "Nobody. Then here is my present, Nobody. I will eat Nobody's friends first, and Nobody last."
- **33 · ODY** (2:58.92-2:59.56)
  - script: I am honoured.
  - sent: "I am honoured."
- **34 · NARR** (2:59.88-3:01.03)
  - script: It does buy time.

### P05 · act 1: the eye · beats 35-40 · 535 characters

- **35 · NARR** (3:01.38-3:07.28)
  - script: The giant passes out. Odysseus puts the stake in the fire. Then he puts it in the eye.
- **36 · NARR** (3:07.68-3:13.37)
  - script: Homer reaches for a blacksmith's simile: an axe plunged into cold water, hissing.
- **37 · CYC2** (3:13.69-3:16.77)
  - script: Polyphemus, what is wrong? Is someone killing you?
  - sent: "Pollifeemus, what is wrong? Is someone killing you?" a Cyclops asked, bored.
- **38 · POLY** (3:19.04-3:23.04)
  - script: Nobody is killing me by trickery! Nobody is killing me by force!
  - sent: "Nobody is killing me by trickery! Nobody is killing me by force!" the giant bellowed.
- **39 · CYC2** (3:24.62-3:30.81)
  - script: Then nobody is hurting you. It must be a sickness from Zeus. Pray to your father, and let us sleep.
  - sent: "Then nobody is hurting you. It must be a sickness from Zeus. Pray to your father, and let us sleep," the Cyclops said flatly.
- **40 · NARR** (3:33.12-3:37.69)
  - script: The Cyclopes have no laws, no assemblies, and no follow-up questions.

### P06 · act 1: the sheep · beats 41-48 · 649 characters

- **41 · NARR** (3:38.04-3:45.37)
  - script: At dawn the sheep file out. Odysseus has tied them in threes, with a man hanging under each middle one.
- **42 · NARR** (3:45.77-3:51.34)
  - script: He hangs under the best ram himself. The blinded giant feels along their backs.
- **43 · NARR** (3:51.74-3:53.87)
  - script: Their backs. Not their bellies.
- **44 · POLY** (3:54.19-4:01.01)
  - script: My good ram. You are always first out. Why are you last today? Are you sorry for your master's eye?
  - sent: "My good ram. You are always first out. Why are you last today? Are you sorry for your master's eye?" the giant said softly.
- **45 · NARR** (4:03.29-4:06.14)
  - script: The most sincere conversation in the poem.
- **46 · NARR** (4:06.54-4:10.08)
  - script: Odysseus should sail away quietly. He has won.
- **47 · NARR** (4:10.48-4:17.35)
  - script: Instead, he jeers at the giant from the deck. The giant tears the top off a mountain and throws it.
- **48 · NARR** (4:17.75-4:24.27)
  - script: It lands just in front of the ship, a whisker from the rudder, and the wave carries the ship back toward shore.

### P07 · act 1: departure · beats 49-54 · 622 characters

- **49 · CREW** (4:24.67-4:28.56)
  - script: Please stop. He already threw one rock. He can throw another.
  - sent: "Please stop. He already threw one rock. He can throw another," the crew begged.
- **50 · ODY** (4:29.96-4:38.27)
  - script: Cyclops. If anyone asks who blinded you, tell them it was Odysseus. Son of Laertes. Of Ithaca.
  - sent: "Cyclops. If anyone asks who blinded you, tell them it was Odysseus. Son of Laertes. Of Ithaca."
- **51 · NARR** (4:38.59-4:40.03)
  - script: Nobody lasted one night.
- **52 · POLY** (4:40.35-4:50.44)
  - script: A prophet told me Odysseus would take my eye. I expected a warrior. I got a weakling who got me drunk. Come back, and I will give you presents.
  - sent: "A prophet told me Odysseus would take my eye. I expected a warrior. I got a weakling who got me drunk. Come back, and I will give you presents," the giant called.
- **53 · ODY** (4:52.05-4:58.13)
  - script: Keep your presents. I would send you to Hades if I could. Not even Poseidon will heal that eye.
  - sent: "Keep your presents. I would send you to Hades if I could. Not even Poseidon will heal that eye."
- **54 · POLY** (4:58.42-5:09.20)
  - script: Father Poseidon, hear me. Never let Odysseus reach his home. Or if he must, let him come late, in misery, and with all his men lost.
  - sent: "Father Poseidon, hear me. Never let Odysseus reach his home. Or if he must, let him come late, in misery, and with all his men lost," the giant prayed.

### P08 · act 1 close and the turn · beats 55-58 · 338 characters

- **55 · NARR** (5:11.13-5:15.83)
  - script: Poseidon listens. It will be years before Odysseus sees Ithaca again.
- **56 · NARR** (5:16.23-5:25.01)
  - script: Now search Book Nine for the words "one eye". Homer never writes them, and he never mentions a forehead. He says "the eye".
- **57 · NARR** (5:25.44-5:33.05)
  - script: Homer takes it for granted. If you want it spelled out, you need a different poet. So where did the Cyclops come from?
- **58 · NARR** (5:33.45-5:35.18)
  - script: Time to open the case.

### P09 · suspect 1 a: the dwarf elephant · beats 60-67 · 644 characters

- **60 · NARR** (5:35.63-5:45.32)
  - script: Ice Age Sicily had elephants, and island life shrank them until the smallest stood under a metre. You could have looked one in the eye.
- **61 · NARR** (5:45.72-5:57.41)
  - script: Their bones have turned up in caves on Sicily and Malta. Head-on, the skull shows two small eye sockets at the sides, and in the middle, one enormous hole.
- **62 · NARR** (5:57.81-6:08.14)
  - script: In 1914, a palaeontologist named Abel imagined sailors finding a skull like this in a beach cave. He thought it might be where the Cyclops came from.
- **63 · NARR** (6:08.54-6:13.10)
  - script: Here is our version. A sailor ducks in to light a fire.
- **64 · CREW** (6:13.42-6:13.82)
  - script: Hello?
  - sent: "Hello?" the sailor asked.
- **65 · NARR** (6:15.51-6:20.25)
  - script: In the clay, something looks back at him. One enormous eye.
- **66 · CREW** (6:20.57-6:21.04)
  - script: Nope.
  - sent: "Nope."
- **67 · NARR** (6:21.36-6:24.68)
  - script: The sailor is imagined. The skulls are real.

### P10 · suspect 1 b: nasal cavity, Mayor · beats 68-73 · 670 characters

- **68 · CREW** (6:25.08-6:26.18)
  - script: Where's the nose?
  - sent: "Where's the nose?"
- **69 · NARR** (6:26.50-6:36.64)
  - script: You are looking at it. That hole is a nasal cavity. To someone who had never seen an elephant, it could pass for one very large eye.
- **70 · NARR** (6:37.04-6:46.29)
  - script: Discover magazine adds that before Alexander the Great, most Greeks had never seen a live elephant. A skull could easily have baffled them.
- **71 · NARR** (6:46.69-6:54.60)
  - script: The folklorist Adrienne Mayor is the theory's best-known champion. Asked about the Cyclops, she is careful.
- **72 · NARR** (6:55.00-7:01.70)
  - script: "I don't like to say that the fossils inspired, or were the source of the story, because we just can't prove that."
- **73 · NARR** (7:02.10-7:12.04)
  - script: That is the theory's best friend, on the record. She does think fossils shaped how Greeks pictured giants. She just won't say they started this one.

### P11 · suspect 1 c: Empedocles · beats 74-80 · 577 characters

- **74 · NARR** (7:12.39-7:22.74)
  - script: Then there is the famous version. In Abel's telling, the philosopher Empedocles reported such bones on Sicily and took them for giants.
  - sent: Then there is the famous version. In Abel's telling, the philosopher Em-peddokleez reported such bones on Sicily and took them for giants.
- **75 · CREW** (7:23.06-7:24.65)
  - script: Which ancient book says that?
  - sent: "Which ancient book says that?" the sailor asked.
- **76 · NARR** (7:26.18-7:35.06)
  - script: None that survives. The translator Jason Colavito calls it "a modern myth invented, apparently, by Abel himself."
- **77 · NARR** (7:35.46-7:40.31)
  - script: Without that story, critics say, Abel's case is very thin.
- **78 · NARR** (7:40.71-7:45.35)
  - script: Abel hedged his sailors with "perhaps". His Empedocles, he told straight.
  - sent: Abel hedged his sailors with "perhaps". His Em-peddokleez, he told straight.
- **79 · NARR** (7:45.75-7:52.90)
  - script: Two scholars of Greek myth, Aguirre and Buxton, have serious doubts about the dwarf-elephant explanation.
  - sent: Two scholars of Greek myth, Ah-gheereh and Buxton, have serious doubts about the dwarf-elephant explanation.
- **80 · NARR** (7:53.60-7:56.30)
  - script: Possible. Provable? No.

### P12 · suspect 2 a: the smiths · beats 82-89 · 503 characters

- **82 · NARR** (7:56.75-8:00.28)
  - script: Suspect two lives in a different poem, with a different job.
- **83 · NARR** (8:00.68-8:06.87)
  - script: Hesiod, around seven hundred BC, has three Cyclopes: Thunder, Lightning and Bright.
  - sent: Hesiod, around seven hundred B.C., has three Cyclopes: Thunder, Lightning and Bright.
- **84 · NARR** (8:07.27-8:12.60)
  - script: They make the thunderbolt for Zeus. The Cyclopes of Book Nine shrug Zeus off.
- **85 · POLY** (8:12.92-8:13.75)
  - script: I keep sheep.
  - sent: "I keep sheep," the giant said awkwardly.
- **86 · CYC2** (8:15.58-8:16.02)
  - script: Sheep.
  - sent: "Sheep."
- **87 · NARR** (8:16.34-8:18.50)
  - script: Hesiod's Cyclopes have careers.
- **88 · NARR** (8:18.90-8:25.33)
  - script: And there it is, the line Book Nine never gave us: one eye only, in the middle of the forehead.
- **89 · NARR** (8:25.73-8:31.64)
  - script: The scholar Walter Burkert suggested that real guilds of metalworkers may lie behind them.
  - sent: The scholar Walter Boor-kert suggested that real guilds of metalworkers may lie behind them.

### P13 · suspect 2 b: addresses · beats 90-96 · 733 characters

- **90 · NARR** (8:31.99-8:41.03)
  - script: By the fifth century BC, the Cyclopes have a Sicilian address, next to Mount Etna. Euripides sets a comic play there.
  - sent: By the fifth century B.C., the Cyclopes have a Sicilian address, next to Mount Etna. Euripides sets a comic play there.
- **91 · NARR** (8:41.43-8:48.50)
  - script: Later, the poet Callimachus sends the smiths to the same neighbourhood, to work for the smith god.
- **92 · NARR** (8:48.90-8:58.13)
  - script: Thucydides lists the Cyclopes among the earliest people spoken of in Sicily. Then he admits, "I cannot tell of what race they were."
  - sent: Thoo-sididdeez lists the Cyclopes among the earliest people spoken of in Sicily. Then he admits, "I cannot tell of what race they were."
- **93 · NARR** (8:58.53-9:07.32)
  - script: Locals, he records, believed the smith god kept a forge on one of the Aeolian islands. Flame by night. Smoke by day.
- **94 · NARR** (9:07.72-9:12.91)
  - script: Forges need fire. Sicily had volcanoes. You can see how the two met.
- **95 · NARR** (9:13.31-9:25.00)
  - script: In the third century BC, Theocritus has Polyphemus sing a love song to a sea nymph. He frets about his looks: one long unbroken eyebrow, and one eye.
  - sent: In the third century B.C., Thee-ockritus has Pollifeemus sing a love song to a sea nymph. He frets about his looks: one long unbroken eyebrow, and one eye.
- **96 · NARR** (9:25.70-9:28.92)
  - script: Plausible. Provable? Also no.

### P14 · suspect 3: the walls · beats 98-105 · 829 characters

- **98 · NARR** (9:29.37-9:33.03)
  - script: Suspect three is not a story. You can go and stand next to it.
- **99 · NARR** (9:33.43-9:39.85)
  - script: At Tiryns and Mycenae, Bronze Age walls rise from boulders so big you wonder who lifted them.
  - sent: At Tie-rinz and Mycenae, Bronze Age walls rise from boulders so big you wonder who lifted them.
- **100 · CREW** (9:40.17-9:41.20)
  - script: Who lifted those?
  - sent: "Who lifted those?" a crewman asked.
- **101 · NARR** (9:42.65-9:51.09)
  - script: At Tiryns, the travel writer Pausanias finds stones so big that a pair of mules could not move even the smallest.
  - sent: At Tie-rinz, the travel writer Paw-sayneeus finds stones so big that a pair of mules could not move even the smallest.
- **102 · NARR** (9:51.49-9:58.53)
  - script: He reports that the Cyclopes built that wall, and that Mycenae's wall and Lion Gate are said to be theirs too.
- **103 · NARR** (9:58.93-10:09.56)
  - script: Homer: twenty-two wagons for one door. Pausanias: two mules, and the stone wins. The Greeks measured giants in wagons and mules.
  - sent: Homer: twenty-two wagons for one door. Paw-sayneeus: two mules, and the stone wins. The Greeks measured giants in wagons and mules.
- **104 · NARR** (10:09.96-10:20.49)
  - script: The Lion Gate is about twelve fifty BC. People built it, and later Greeks credited the Cyclopes. Archaeologists still call the style cyclopean masonry.
  - sent: The Lion Gate is about twelve fifty B.C.. People built it, and later Greeks credited the Cyclopes. Archaeologists still call the style cyclopean masonry.
- **105 · NARR** (10:21.19-10:29.01)
  - script: The wall is real. The giants were the Greeks' explanation for it. It cannot tell us where Homer's giant began.

### P15 · suspect 4: the folktale · beats 107-113 · 586 characters

- **107 · NARR** (10:29.46-10:36.10)
  - script: Suspect four does not need an elephant, a smith, or a wall. It does not even need Sicily.
- **108 · NARR** (10:36.50-10:45.80)
  - script: Strip off the names, and you have a story you have already watched. A man is trapped by a giant, blinds him, and gets away.
- **109 · NARR** (10:46.20-10:54.27)
  - script: Scholars have recorded more than two hundred versions. Iceland. Portugal. Russia. Even the Arabian Nights.
- **110 · NARR** (10:54.67-10:57.35)
  - script: Most scholars think the tale is older than Homer.
- **111 · ODY** (10:57.67-10:59.48)
  - script: So I was not the first.
  - sent: "So I was not the first," Odysseus muttered.
- **112 · NARR** (11:00.91-11:06.07)
  - script: That does not rule out the skull. It does mean the story does not need one.
- **113 · NARR** (11:06.77-11:12.88)
  - script: On that view, Homer did not invent the Cyclops story. He gave us the best-known version.

### P16 · verdict and tease · beats 114-121 · 587 characters

- **114 · NARR** (11:13.23-11:25.05)
  - script: Four suspects. The smiths have Hesiod. The walls have Pausanias. The folktale has two hundred versions. The elephant has real skulls, and an imaginary sailor.
  - sent: Four suspects. The smiths have Hesiod. The walls have Paw-sayneeus. The folktale has two hundred versions. The elephant has real skulls, and an imaginary sailor.
- **115 · NARR** (11:25.45-11:30.22)
  - script: So was the Cyclops real? As a one-eyed giant who eats sailors, no.
- **116 · POLY** (11:30.54-11:31.12)
  - script: Rude.
  - sent: "Rude."
- **117 · NARR** (11:31.44-11:38.85)
  - script: But the name is real. It was wrapped around a forge, a wall, a story, and perhaps a skull.
- **118 · NARR** (11:39.25-11:41.77)
  - script: Who can prove where the Cyclops came from?
- **119 · ODY** (11:42.52-11:43.04)
  - script: Nobody.
  - sent: "Nobody."
- **120 · NARR** (11:43.36-11:48.75)
  - script: Next time: the wind in the bag, the witch with the wand, and the other monsters of the Odyssey.
- **121 · NARR** (11:49.15-11:55.94)
  - script: Odysseus thinks the worst is behind him. He has just told a giant his name, and the giant has a father.
