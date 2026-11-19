# SPOKEN-TEXT.md: exactly what was sent to the voice, video 1 (SCRIPT-V4 = V3 with the approved cuts, method A2)

Voice Daniel (`onwK4e9ZLuTAKqWW03F9`), `eleven_multilingual_v2`, stability 0.5, style 0.2, speed 1.0, similarity 0.75, speaker boost on. No audio tags. One continuous call per passage (16 passages), `previous_text` / `next_text` = the neighbouring passages' text. Beats are separated by a blank line inside a passage (as in round-3 A2). TEXT-CHIP beats 59, 81, 97, 106 are on screen only and are not in the text.

## What the A2 technique adds or changes (nothing else was altered)

1. **Quotation marks** around every character line (never spoken, but they set the voice up as a quotation). A final full stop becomes a comma when an attribution follows (`...Have some wine," said Odysseus`); `?` and `!` stay.
2. **Attribution words** after 21 of the 35 character lines (listed below). These words are **spoken**: 63 words in all, tagged `added: true` and `speaker: NARR` in `words.json`, kept out of `beats_timing.json` `start`/`end` (they get their own `attribution` span). Seven are exactly as in round-3 A2 (28, 30, 31, 37, 38, 39, 64); fourteen are new, same pattern.
3. **No attribution** on the 14 remaining character lines: replies inside an exchange (15, 16, 19, 25, 32, 33, 50, 53, 86) and the one-word gags / punchlines (20 `Ah.`, 66 `Nope.`, 68, 116 `Rude.`, 119 `Nobody.`) as in A2's 32, 33, 66, 68.
4. **TTS-only respellings** (the saved script is never altered; each is one token for one token so words map back 1:1): Polyphemus → Pollifeemus, Empedocles → Em-peddokleez, Theocritus → Thee-ockritus, Thucydides → Thoo-sididdeez, Tiryns → Tie-rinz, Pausanias → Paw-sayneeus, Brontes → Bron-teez, Steropes → Stair-oh-peez, Arges → Ar-geez, Aci → Ah-chee, Trezza → Tret-sah, Aguirre → Ah-gheereh, Burkert → Boor-kert, BC → B.C.. `Othenio Abel` is never spoken in V3 (beat 62 says "Abel"); William's approved plain-text handling is kept, with no respelling. Not respelled: Odysseus, Hesiod, Callimachus, Laertes, Ithaca, Poseidon, Euripides, Mycenae, Etna, Colavito, Buxton, Hackman, Mayor, Aeolian.
5. Numbers are as written in the script (words, e.g. "Twenty-two", "twelve fifty"). `BC` was sent as `B.C.` (beats 83, 90, 91, 95, 104).

### Attribution words added (spoken, not in the script)

| beat | speaker | words added | time |
|---|---|---|---|
| 9 | CREW | the crew urged. | 0:51.24 |
| 10 | ODY | said Odysseus. | 0:55.88 |
| 14 | POLY | the giant asked. | 1:17.92 |
| 18 | ODY | Odysseus thought. | 1:38.86 |
| 23 | ODY | said Odysseus. | 2:01.47 |
| 24 | CREW | a crewman asked. | 2:03.84 |
| 28 | ODY | said Odysseus, quite calmly. | 2:20.45 |
| 30 | POLY | the giant rumbled. | 2:35.54 |
| 31 | ODY | said Odysseus. | 2:38.06 |
| 37 | CYC2 | a Cyclops asked, bored. | 3:03.39 |
| 38 | POLY | the giant bellowed. | 3:09.60 |
| 39 | CYC2 | the Cyclops said flatly. | 3:17.20 |
| 44 | POLY | the giant said softly. | 3:45.66 |
| 49 | CREW | the crew begged. | 4:11.70 |
| 52 | POLY | the giant called. | 4:31.71 |
| 54 | POLY | the giant prayed. | 4:49.01 |
| 64 | CREW | the sailor asked. | 5:48.65 |
| 75 | CREW | the sailor asked. | 6:53.41 |
| 85 | POLY | the giant said awkwardly. | 7:22.19 |
| 100 | CREW | a crewman asked. | 8:33.89 |
| 111 | ODY | Odysseus muttered. | 9:47.71 |

Total added words: 63.

## Per beat

`script` = SCRIPT-V4.md wording; `sent` = the exact text in the TTS call (quotes, attribution and respellings included). Identical except where shown.

### P01 · cold open · beats 1-5 · 444 characters

- **01 · NARR** (0:00.40-0:04.80)
  - script: Twelve men follow Odysseus into a cave. Six of them get out.
- **02 · NARR** (0:05.20-0:09.81)
  - script: A giant ate the other six, the one-eyed kind. So where did he come from?
- **03 · NARR** (0:10.21-0:18.20)
  - script: We have four suspects, and a verdict on each. One is an elephant skull. Another, you can still walk up to and touch.
- **04 · NARR** (0:18.60-0:27.00)
  - script: One note before we start. Where Homer gives these characters lines, we have tidied them up. Where he doesn't, we have made a few up.
- **05 · NARR** (0:27.40-0:32.24)
  - script: But first, a poem. And a very bad decision about cheese.

### P02 · act 1: arrival · beats 6-13 · 619 characters

- **06 · NARR** (0:32.59-0:39.78)
  - script: Sailing home from Troy, Odysseus lands in the country of the Cyclopes. Book Nine never says where.
- **07 · NARR** (0:40.18-0:44.83)
  - script: He picks twelve men, takes a goatskin of wine, and walks up to a cave.
- **08 · NARR** (0:45.22-0:49.02)
  - script: Racks of cheese. Pens full of lambs. Nobody home.
- **09 · CREW** (0:49.34-0:50.99)
  - script: Take the cheese. Let's go.
  - sent: "Take the cheese. Let's go," the crew urged.
- **10 · ODY** (0:52.37-0:55.64)
  - script: No. I want to meet the owner. He might give us a present.
  - sent: "No. I want to meet the owner. He might give us a present," said Odysseus.
- **11 · NARR** (0:56.97-1:01.44)
  - script: The cleverest man in the poem is waiting for a gift basket from a stranger's cave.
- **12 · NARR** (1:01.84-1:06.94)
  - script: The owner comes home. He looks less like a man than a wooded peak, standing alone.
- **13 · NARR** (1:07.34-1:14.12)
  - script: He drives his flock inside, then rolls a stone across the door. Twenty-two wagons could not have moved it.

### P03 · act 1: the owner · beats 14-21 · 514 characters

- **14 · POLY** (1:14.52-1:17.62)
  - script: Strangers, who are you? Traders, or pirates?
  - sent: "Strangers, who are you? Traders, or pirates?" the giant asked.
- **15 · ODY** (1:19.01-1:25.21)
  - script: We are Greeks, heading home from Troy. We ask for hospitality. Remember: Zeus protects guests.
  - sent: "We are Greeks, heading home from Troy. We ask for hospitality. Remember: Zeus protects guests."
- **16 · POLY** (1:25.49-1:30.06)
  - script: Zeus? We Cyclopes don't care about Zeus. We are stronger than the gods.
  - sent: "Zeus? We Cyclopes don't care about Zeus. We are stronger than the gods."
- **17 · NARR** (1:30.38-1:35.96)
  - script: That is not a good answer. He grabs two of the men for supper, then falls asleep among his sheep.
- **18 · ODY** (1:36.28-1:38.61)
  - script: He is asleep. I could kill him right now.
  - sent: "He is asleep. I could kill him right now," Odysseus thought.
- **19 · ODY** (1:39.95-1:41.42)
  - script: And then who moves the stone?
  - sent: "And then who moves the stone?"
- **20 · ODY** (1:41.97-1:42.33)
  - script: Ah.
  - sent: "Ah."
- **21 · NARR** (1:42.65-1:48.04)
  - script: At breakfast, two more men go. Homer gives the details. We will spare you.

### P04 · act 1: the stake, the wine, Nobody · beats 22-34 · 891 characters

- **22 · NARR** (1:48.39-1:58.23)
  - script: Odysseus finds the giant's own club, an olive trunk as big as a ship's mast. He cuts off a length, sharpens it, and hardens the point in the fire.
- **23 · ODY** (1:58.55-2:01.22)
  - script: Who helps me carry the stake? Draw lots.
  - sent: "Who helps me carry the stake? Draw lots," said Odysseus.
- **24 · CREW** (2:02.56-2:03.51)
  - script: And if he wakes up?
  - sent: "And if he wakes up?" a crewman asked.
- **25 · ODY** (2:04.95-2:06.69)
  - script: Then it was a short plan.
  - sent: "Then it was a short plan."
- **26 · NARR** (2:07.02-2:12.19)
  - script: He hides the stake under dung, the one thing a cave full of sheep has plenty of.
- **27 · NARR** (2:12.59-2:15.88)
  - script: That evening, two more. Six men gone.
- **28 · ODY** (2:16.21-2:20.38)
  - script: You have eaten a great deal of man's flesh, Cyclops. Have some wine.
  - sent: "You have eaten a great deal of man's flesh, Cyclops. Have some wine," said Odysseus, quite calmly.
- **29 · NARR** (2:22.34-2:31.37)
  - script: The wine comes from a priest of Apollo, whose household drank it mixed twenty parts water to one. The giant drinks three bowls. Homer counts.
- **30 · POLY** (2:31.69-2:35.30)
  - script: More. Now tell me your name, and I will give you a present.
  - sent: "More. Now tell me your name, and I will give you a present," the giant rumbled.
- **31 · ODY** (2:36.77-2:37.83)
  - script: My name is Nobody.
  - sent: "My name is Nobody," said Odysseus.
- **32 · POLY** (2:39.07-2:45.77)
  - script: Nobody. Then here is my present, Nobody. I will eat Nobody's friends first, and Nobody last.
  - sent: "Nobody. Then here is my present, Nobody. I will eat Nobody's friends first, and Nobody last."
- **33 · ODY** (2:46.05-2:46.69)
  - script: I am honoured.
  - sent: "I am honoured."
- **34 · NARR** (2:47.01-2:48.16)
  - script: It does buy time.

### P05 · act 1: the eye · beats 35-40 · 535 characters

- **35 · NARR** (2:48.51-2:53.92)
  - script: The giant passes out. Odysseus puts the stake in the fire. Then he puts it in the eye.
- **36 · NARR** (2:54.32-2:59.76)
  - script: Homer reaches for a blacksmith's simile: an axe plunged into cold water, hissing.
- **37 · CYC2** (3:00.08-3:03.04)
  - script: Polyphemus, what is wrong? Is someone killing you?
  - sent: "Pollifeemus, what is wrong? Is someone killing you?" a Cyclops asked, bored.
- **38 · POLY** (3:05.30-3:09.31)
  - script: Nobody is killing me by trickery! Nobody is killing me by force!
  - sent: "Nobody is killing me by trickery! Nobody is killing me by force!" the giant bellowed.
- **39 · CYC2** (3:10.89-3:16.95)
  - script: Then nobody is hurting you. It must be a sickness from Zeus. Pray to your father, and let us sleep.
  - sent: "Then nobody is hurting you. It must be a sickness from Zeus. Pray to your father, and let us sleep," the Cyclops said flatly.
- **40 · NARR** (3:19.01-3:23.58)
  - script: The Cyclopes have no laws, no assemblies, and no follow-up questions.

### P06 · act 1: the sheep · beats 41-48 · 649 characters

- **41 · NARR** (3:23.93-3:30.57)
  - script: At dawn the sheep file out. Odysseus has tied them in threes, with a man hanging under each middle one.
- **42 · NARR** (3:30.97-3:36.05)
  - script: He hangs under the best ram himself. The blinded giant feels along their backs.
- **43 · NARR** (3:36.45-3:38.33)
  - script: Their backs. Not their bellies.
- **44 · POLY** (3:38.65-3:45.31)
  - script: My good ram. You are always first out. Why are you last today? Are you sorry for your master's eye?
  - sent: "My good ram. You are always first out. Why are you last today? Are you sorry for your master's eye?" the giant said softly.
- **45 · NARR** (3:47.45-3:50.07)
  - script: The most sincere conversation in the poem.
- **46 · NARR** (3:50.47-3:53.86)
  - script: Odysseus should sail away quietly. He has won.
- **47 · NARR** (3:54.26-4:00.73)
  - script: Instead, he jeers at the giant from the deck. The giant tears the top off a mountain and throws it.
- **48 · NARR** (4:01.13-4:07.41)
  - script: It lands just in front of the ship, a whisker from the rudder, and the wave carries the ship back toward shore.

### P07 · act 1: departure · beats 49-54 · 622 characters

- **49 · CREW** (4:07.81-4:11.45)
  - script: Please stop. He already threw one rock. He can throw another.
  - sent: "Please stop. He already threw one rock. He can throw another," the crew begged.
- **50 · ODY** (4:12.78-4:20.08)
  - script: Cyclops. If anyone asks who blinded you, tell them it was Odysseus. Son of Laertes. Of Ithaca.
  - sent: "Cyclops. If anyone asks who blinded you, tell them it was Odysseus. Son of Laertes. Of Ithaca."
- **51 · NARR** (4:20.40-4:21.84)
  - script: Nobody lasted one night.
- **52 · POLY** (4:22.16-4:31.46)
  - script: A prophet told me Odysseus would take my eye. I expected a warrior. I got a weakling who got me drunk. Come back, and I will give you presents.
  - sent: "A prophet told me Odysseus would take my eye. I expected a warrior. I got a weakling who got me drunk. Come back, and I will give you presents," the giant called.
- **53 · ODY** (4:32.89-4:38.66)
  - script: Keep your presents. I would send you to Hades if I could. Not even Poseidon will heal that eye.
  - sent: "Keep your presents. I would send you to Hades if I could. Not even Poseidon will heal that eye."
- **54 · POLY** (4:38.94-4:48.76)
  - script: Father Poseidon, hear me. Never let Odysseus reach his home. Or if he must, let him come late, in misery, and with all his men lost.
  - sent: "Father Poseidon, hear me. Never let Odysseus reach his home. Or if he must, let him come late, in misery, and with all his men lost," the giant prayed.

### P08 · act 1 close and the turn · beats 55-58 · 338 characters

- **55 · NARR** (4:50.32-4:54.92)
  - script: Poseidon listens. It will be years before Odysseus sees Ithaca again.
- **56 · NARR** (4:55.32-5:03.36)
  - script: Now search Book Nine for the words "one eye". Homer never writes them, and he never mentions a forehead. He says "the eye".
- **57 · NARR** (5:03.79-5:10.44)
  - script: Homer takes it for granted. If you want it spelled out, you need a different poet. So where did the Cyclops come from?
- **58 · NARR** (5:10.84-5:12.57)
  - script: Time to open the case.

### P09 · suspect 1 a: the dwarf elephant · beats 60-67 · 644 characters

- **60 · NARR** (5:13.02-5:21.74)
  - script: Ice Age Sicily had elephants, and island life shrank them until the smallest stood under a metre. You could have looked one in the eye.
- **61 · NARR** (5:22.14-5:32.96)
  - script: Their bones have turned up in caves on Sicily and Malta. Head-on, the skull shows two small eye sockets at the sides, and in the middle, one enormous hole.
- **62 · NARR** (5:33.36-5:43.04)
  - script: In 1914, a palaeontologist named Abel imagined sailors finding a skull like this in a beach cave. He thought it might be where the Cyclops came from.
- **63 · NARR** (5:43.44-5:47.58)
  - script: Here is our version. A sailor ducks in to light a fire.
- **64 · CREW** (5:47.90-5:48.30)
  - script: Hello?
  - sent: "Hello?" the sailor asked.
- **65 · NARR** (5:49.78-5:53.97)
  - script: In the clay, something looks back at him. One enormous eye.
- **66 · CREW** (5:54.29-5:54.75)
  - script: Nope.
  - sent: "Nope."
- **67 · NARR** (5:55.07-5:58.16)
  - script: The sailor is imagined. The skulls are real.

### P10 · suspect 1 b: nasal cavity, Mayor · beats 68-73 · 670 characters

- **68 · CREW** (5:58.56-5:59.67)
  - script: Where's the nose?
  - sent: "Where's the nose?"
- **69 · NARR** (5:59.99-6:09.29)
  - script: You are looking at it. That hole is a nasal cavity. To someone who had never seen an elephant, it could pass for one very large eye.
- **70 · NARR** (6:09.69-6:18.15)
  - script: Discover magazine adds that before Alexander the Great, most Greeks had never seen a live elephant. A skull could easily have baffled them.
- **71 · NARR** (6:18.55-6:25.56)
  - script: The folklorist Adrienne Mayor is the theory's best-known champion. Asked about the Cyclops, she is careful.
- **72 · NARR** (6:25.96-6:32.30)
  - script: "I don't like to say that the fossils inspired, or were the source of the story, because we just can't prove that."
- **73 · NARR** (6:32.70-6:42.06)
  - script: That is the theory's best friend, on the record. She does think fossils shaped how Greeks pictured giants. She just won't say they started this one.

### P11 · suspect 1 c: Empedocles · beats 74-80 · 329 characters

- **74 · NARR** (6:42.41-6:51.48)
  - script: Then there is the famous version. In Abel's telling, the philosopher Empedocles reported such bones on Sicily and took them for giants.
  - sent: Then there is the famous version. In Abel's telling, the philosopher Em-peddokleez reported such bones on Sicily and took them for giants.
- **75 · CREW** (6:51.80-6:53.16)
  - script: Which ancient book says that?
  - sent: "Which ancient book says that?" the sailor asked.
- **76 · NARR** (6:54.58-7:02.29)
  - script: None that survives. The translator Jason Colavito calls it "a modern myth invented, apparently, by Abel himself."
- **80 · NARR** (7:02.99-7:05.24)
  - script: Possible. Provable? No.

### P12 · suspect 2 a: the smiths · beats 82-88 · 409 characters

- **82 · NARR** (7:05.69-7:08.94)
  - script: Suspect two lives in a different poem, with a different job.
- **83 · NARR** (7:09.35-7:15.42)
  - script: Hesiod, around seven hundred BC, has three Cyclopes: Thunder, Lightning and Bright.
  - sent: Hesiod, around seven hundred B.C., has three Cyclopes: Thunder, Lightning and Bright.
- **84 · NARR** (7:15.82-7:20.40)
  - script: They make the thunderbolt for Zeus. The Cyclopes of Book Nine shrug Zeus off.
- **85 · POLY** (7:20.73-7:21.94)
  - script: I keep sheep.
  - sent: "I keep sheep," the giant said awkwardly.
- **86 · CYC2** (7:23.88-7:24.29)
  - script: Sheep.
  - sent: "Sheep."
- **87 · NARR** (7:24.61-7:27.07)
  - script: Hesiod's Cyclopes have careers.
- **88 · NARR** (7:27.47-7:34.68)
  - script: And there it is, the line Book Nine never gave us: one eye only, in the middle of the forehead.

### P13 · suspect 2 b: addresses · beats 90-96 · 633 characters

- **90 · NARR** (7:35.03-7:43.19)
  - script: By the fifth century BC, the Cyclopes have a Sicilian address, next to Mount Etna. Euripides sets a comic play there.
  - sent: By the fifth century B.C., the Cyclopes have a Sicilian address, next to Mount Etna. Euripides sets a comic play there.
- **92 · NARR** (7:43.59-7:52.19)
  - script: Thucydides lists the Cyclopes among the earliest people spoken of in Sicily. Then he admits, "I cannot tell of what race they were."
  - sent: Thoo-sididdeez lists the Cyclopes among the earliest people spoken of in Sicily. Then he admits, "I cannot tell of what race they were."
- **93 · NARR** (7:52.59-8:00.69)
  - script: Locals, he records, believed the smith god kept a forge on one of the Aeolian islands. Flame by night. Smoke by day.
- **94 · NARR** (8:01.09-8:06.36)
  - script: Forges need fire. Sicily had volcanoes. You can see how the two met.
- **95 · NARR** (8:06.75-8:18.12)
  - script: In the third century BC, Theocritus has Polyphemus sing a love song to a sea nymph. He frets about his looks: one long unbroken eyebrow, and one eye.
  - sent: In the third century B.C., Thee-ockritus has Pollifeemus sing a love song to a sea nymph. He frets about his looks: one long unbroken eyebrow, and one eye.
- **96 · NARR** (8:18.81-8:21.52)
  - script: Plausible. Provable? Also no.

### P14 · suspect 3: the walls · beats 98-105 · 828 characters

- **98 · NARR** (8:21.97-8:25.92)
  - script: Suspect three is not a story. You can go and stand next to it.
- **99 · NARR** (8:26.32-8:32.40)
  - script: At Tiryns and Mycenae, Bronze Age walls rise from boulders so big you wonder who lifted them.
  - sent: At Tie-rinz and Mycenae, Bronze Age walls rise from boulders so big you wonder who lifted them.
- **100 · CREW** (8:32.72-8:33.76)
  - script: Who lifted those?
  - sent: "Who lifted those?" a crewman asked.
- **101 · NARR** (8:35.08-8:42.68)
  - script: At Tiryns, the travel writer Pausanias finds stones so big that a pair of mules could not move even the smallest.
  - sent: At Tie-rinz, the travel writer Paw-sayneeus finds stones so big that a pair of mules could not move even the smallest.
- **102 · NARR** (8:43.08-8:50.24)
  - script: He reports that the Cyclopes built that wall, and that Mycenae's wall and Lion Gate are said to be theirs too.
- **103 · NARR** (8:50.64-9:00.01)
  - script: Homer: twenty-two wagons for one door. Pausanias: two mules, and the stone wins. The Greeks measured giants in wagons and mules.
  - sent: Homer: twenty-two wagons for one door. Paw-sayneeus: two mules, and the stone wins. The Greeks measured giants in wagons and mules.
- **104 · NARR** (9:00.41-9:10.66)
  - script: The Lion Gate is about twelve fifty BC. People built it, and later Greeks credited the Cyclopes. Archaeologists still call the style cyclopean masonry.
  - sent: The Lion Gate is about twelve fifty B.C. People built it, and later Greeks credited the Cyclopes. Archaeologists still call the style cyclopean masonry.
- **105 · NARR** (9:11.36-9:18.77)
  - script: The wall is real. The giants were the Greeks' explanation for it. It cannot tell us where Homer's giant began.

### P15 · suspect 4: the folktale · beats 107-113 · 586 characters

- **107 · NARR** (9:19.22-9:25.39)
  - script: Suspect four does not need an elephant, a smith, or a wall. It does not even need Sicily.
- **108 · NARR** (9:25.79-9:34.39)
  - script: Strip off the names, and you have a story you have already watched. A man is trapped by a giant, blinds him, and gets away.
- **109 · NARR** (9:34.79-9:42.34)
  - script: Scholars have recorded more than two hundred versions. Iceland. Portugal. Russia. Even the Arabian Nights.
- **110 · NARR** (9:42.74-9:45.42)
  - script: Most scholars think the tale is older than Homer.
- **111 · ODY** (9:45.75-9:47.51)
  - script: So I was not the first.
  - sent: "So I was not the first," Odysseus muttered.
- **112 · NARR** (9:48.93-9:53.62)
  - script: That does not rule out the skull. It does mean the story does not need one.
- **113 · NARR** (9:54.32-9:59.96)
  - script: On that view, Homer did not invent the Cyclops story. He gave us the best-known version.

### P16 · verdict and tease · beats 114-121 · 587 characters

- **114 · NARR** (10:00.31-10:11.58)
  - script: Four suspects. The smiths have Hesiod. The walls have Pausanias. The folktale has two hundred versions. The elephant has real skulls, and an imaginary sailor.
  - sent: Four suspects. The smiths have Hesiod. The walls have Paw-sayneeus. The folktale has two hundred versions. The elephant has real skulls, and an imaginary sailor.
- **115 · NARR** (10:11.98-10:16.25)
  - script: So was the Cyclops real? As a one-eyed giant who eats sailors, no.
- **116 · POLY** (10:16.57-10:17.15)
  - script: Rude.
  - sent: "Rude."
- **117 · NARR** (10:17.47-10:24.48)
  - script: But the name is real. It was wrapped around a forge, a wall, a story, and perhaps a skull.
- **118 · NARR** (10:24.88-10:27.40)
  - script: Who can prove where the Cyclops came from?
- **119 · ODY** (10:28.15-10:28.67)
  - script: Nobody.
  - sent: "Nobody."
- **120 · NARR** (10:28.99-10:34.01)
  - script: Next time: the wind in the bag, the witch with the wand, and the other monsters of the Odyssey.
- **121 · NARR** (10:34.41-10:40.86)
  - script: Odysseus thinks the worst is behind him. He has just told a giant his name, and the giant has a father.
