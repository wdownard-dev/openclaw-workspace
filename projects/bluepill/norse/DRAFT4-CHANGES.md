# DRAFT4-CHANGES.md: draft 3 to draft 4 (Norse, The Myth Ledger video 2)

2026-11-14. Source: `norse/BRIEF-DRAFT4.md`. Output: `norse/SCRIPT-N-draft4.md` (built by `norse/src/gen5.py` from `SCRIPT-N-draft3.md`; stats in `src/gen5_stats.json`). Ids below are draft 4 ids unless marked "d3". The old-to-new table is at the bottom of the script. Nothing recorded, generated, uploaded or sent; `library/` untouched.

Note on a stale file: a `SCRIPT-N-draft4.md` already sat in the folder when this run started (written 16:38, before the brief). It used "Look up. That is a skull." and other wording that is not William's final hook, so it was replaced. The old file and its generator are kept in `norse/src/superseded/`.

## Totals

| | Draft 3 | Draft 4 |
|---|---|---|
| Spoken words | 1,553 | **1,520** (-33; cap 1,650, met) |
| Sentences (mean words) | 145 (10.7) | 140 (10.9) |
| Questions | 3 | 2 (0.2 a minute) |
| Beats | 178 | 174 |
| Raw voice time at 150 wpm | 10:21 | **10:08** |
| Cold open | 60 words | 61 words, about 24 s |

voicecheck counts 1,527 because it counts the seven `[CTA]`, `[PULL]` and `[CLOSE]` tags as words; the spoken count is 1,520.

## 1. The hook (William's final pick, word for word)

Spoken as written in the brief, split into beats the way draft 3 splits:

| Beat | Spoken text | Shot (reused entity) |
|---|---|---|
| N-001 | The sky is a skull. | sky-as-skull dome over a dark sea |
| N-002 | The clouds are its brain. | clouds inside the skull dome |
| N-003 | The sea is blood, | blue sea with a red tinge |
| N-004 | and the mountains are bones. | grey peaks, ridged like bone |
| N-005 | In Norse myth, the world was a giant once, | land and sea laid out as Ymir's body |
| N-006 | until three brothers took him apart. | Odin, Vili, Ve hauling Ymir's body |
| N-007 | One of them was Odin. | Odin, one eye, facing us |
| N-008 | He built everything from a corpse, | brothers small on the body |
| N-009 | and then he was told how it would end. | Odin alone, listening, in his hall |
| N-010 | But first, there was nothing at all. | empty Ginnungagap |

- Removed: d3 N-001 to N-008 (hook A), d3 N-009 "Let us start at the beginning." (banned meta line, VOICE.md §2 and §9) and d3 N-010 "In the beginning there is no sand, no sea, and no sky." (restated the bridge, §9 tell 2).
- **First story beat after the bridge, N-011:** "Well, almost nothing. Only a great gap, with ice on one side" / N-012 "and fire on the other." The edit is ours: it corrects "nothing at all" in four words (Voluspa 3 has a gap, and Ymir lives), gives the viewer a question ("what is in the gap?") and carries no meta line. The shot is d3's gap with the ice land on the left.
- **Re-hook, N-015 (about 0:40):** "The skull in the sky is still on his shoulders, for now." It lands on the beat after Ymir rises (N-014), shows his head, and pulls forward ("for now": how does a skull get to the sky?). No meta line. Shot: close on Ymir's head and beard.
- **Master promise:** how a world made like that ends. The hook raises it ("told how it would end"); it is paid at the Ragnarok chapter (from 7:36) and at the CLOSE beat **N-145** "Odin knows how it ends, and goes anyway." (about 8:16). That is about 82% of the runtime, not the 90% VOICE.md §2 asks for, because the Snorri origin chapter (about 1:50) closes the video after it. Left as is; the origin chapter has to close the video (VOICE.md §5).
- **Hook flags for William** (hook text was NOT changed; these are for you to decide):
  1. N-010 "nothing at all" is hyperbole. Voluspa 3 has Ymir alive and a yawning gap; Gylf 4 has the ice and fire lands already there. N-011 softens it on the next beat. Cheap alternative if you want it exact: "But first, there was almost nothing."
  2. N-008 "He built everything from a corpse": the source credits three brothers (Odin, Vili, Ve), and "everything" is the physical world only (earth, sea, hills, trees, sky, clouds, the wall of Mithgarth). Asgard, the first humans (from trees), the sun and the stars (sparks from Muspellsheim) and Yggdrasil are not made from the corpse. Defensible as a hook, loose as a claim. See NEW CLAIMS H4.
  3. N-005 "In Norse myth," is a topic label at the front of a sentence (VOICE.md §2: not on the topic label; §4: facts as plot). Mild, because the hook has already opened on the image.
  4. N-001 to N-003 open three sentences with "The" in a row (VOICE.md §9 tell 6). It reads as deliberate, and it is your pick, so left.
  5. N-006/N-008 together retell "three brothers took him apart, he built everything from a corpse", and chapter 1 then retells it (N-021 to N-029) with the same list (flesh, blood, bones, skull). This is the cost HOOK-OPTIONS.md predicted for hook C. I did not trim N-025 to N-029 (not on the brief's list), but if you want, cutting N-026 and N-027 ("his blood becomes the sea," "his bones become the mountains,") removes the repeats and saves 10 words.

### The three VOICE.md tests applied to the hook

| Test | Verdict |
|---|---|
| 1. Would a smart friend say this over a drink to someone who has never heard the story? | PASS. "The sky is a skull. The clouds are its brain." is a thing you would say to start the story. "He built everything from a corpse, and then he was told how it would end" is plain talk. |
| 2. Does a stranger stay past 5 s, 20 s, 45 s? | PASS. 5 s: a skull for a sky. 20 s: Odin is told the ending. 45 s: "almost nothing", the gap, a giant rising, "the skull is still on his shoulders, for now". The viewer has more questions than answers at each point. |
| 3. Could any model have guessed this sentence? | PASS for N-001 to N-004 (Grimnismal 41's clouds from the brain is the unguessable detail), PARTIAL for N-010 ("there was nothing at all" is the generic line; N-011's "almost nothing" and the gap carry the specific). |

## 2. Variant cards (binding)

- Every `state:` that names Odin now reads `Odin (one eye)`; no beat shows a two-eyed Odin, including the creation and brother beats that come before the well (N-046). N-046 "Odin trades one eye for a drink" stays as the story of how he lost it; the figure is one-eyed in the plate regardless.
- Tyr: `Tyr (hand)` from N-061 (feeding the wolf) through N-077; `Tyr (stump)` from N-078 on (N-079 pull, N-144, N-151). The bite beat N-077 "Fenrir bites the hand off" keeps `Tyr (hand)`, because its shot is the jaws closing on the wrist; the stump starts the very next beat. If you want the stump on the bite beat itself, change that one state and shot.
- Shots that must show the stump were edited: N-078 (the bound wolf, "Tyr's right arm ending in a stump"), N-144 (the left figure with an empty right sleeve), N-151 (Tyr's stump).
- Also made explicit so plate generation never guesses: Fenrir (cub / young / huge, 2.0 / bound / huge), Loki (bound), Loki as an old woman, Loki as a salmon, Baldr (dead). The Variants table is in the script header with first and last beats.
- Variant names appear in the figure list of each `state:`; action text such as "Tyr steps forward" is left as plain prose.

## 3. VOICE.md pass (structural tells and banned shapes)

Scan: every beat checked for tells 1 to 8 and the shape ban list. FIXed only these:

| d4 beat (d3 id) | Change | Reason |
|---|---|---|
| N-077/N-078 (d3 N-077) | "and stays chained until the end of the world." to "and the wolf stays chained." The "will break" fact stays in the pull N-079 "That ribbon will not hold forever." | §9 tell 2: two consecutive beats said the same fact. |
| d3 N-133 (removed; N-134 pull now holds N-133's plate, the Sigyn bowl) | Removed "He lies there until the end of the world." The pull "Loki will not stay in that cave." follows N-133 "and the venom lands on him, and the earth shakes." | §9 tell 2: duration line restated, and the pull flips it one beat later. |
| d3 N-156 (removed) | "But the story does not end there." removed. N-155 "And then, silence." now runs straight into N-156 "The earth rises again from the sea, green and new." | §9 tell 4 (staged run-up) and §2 (no meta lines about "the story"). |
| d3 N-163 (removed) | "They begin again." removed. | §9 tells 2 and 7: restates the chapter title and the two beats before it. |
| d3 N-176 (removed) | "A world made from a giant, ended by a wolf, and begun again." removed. | §9 tells 2 and 7: recap, in the Snorri chapter where significance inflates. |
| d3 N-177 (removed) | "We only know it because somebody wrote it down." removed. The video now ends on N-173 (Snorri killed in 1241, kept) and then CTA 3. | §9 ("an ending that states the moral as a platitude") and tell 2. |
| N-050 (d3 N-049) | "handsome, charming, and impossible to trust" to "handsome and charming, and impossible to trust". | §9 tell 6 (forced triad), flagged by voicecheck. |

Checked and left alone, with the reason:
- Tell 1 (not X but Y): none. The only "not" beats are plain negatives (N-079, N-084, N-106, N-109, N-125, N-134).
- Tell 3 (deep-sounding sayings), tell 5 (arguing with no one): none found.
- Tell 7 (inflated significance): the Snorri chapter and the origin beats read as facts after the fixes above. The chapter title "The Christian Who Saved the Gods" is a story claim, not an apparatus line, but "saved" is a strong word for a handbook author; decision for William.
- Tell 8 (shallow -ing tails): "carrying insults" (N-045) is the squirrel's joke and names what it does (Gylf 16); "biting its own tail" (N-058), "hiding as a salmon" (N-128) and "dripping venom" (N-130) are literal images. None is a "showing how..." tail.
- N-155 "And then, silence." stays: it is the pause between the end and the rebirth and the plate is the black sea; marginal under tell 2, so flagged here instead of fixed.
- N-031 "Not bad for three brothers." and N-047 "That is why Odin has one eye, a wide hat, and a lot of secrets." stay: both carry the gag or a new fact.
- Ban list words: none (voicecheck). No em dashes. No "Let us start at the beginning". No mention of Egypt anywhere in the script outside the header notes.

## 4. Warmth and humour (three edits, each framing, no new claim)

| Beat | New line | Basis | Register |
|---|---|---|---|
| N-072 (d3 N-071) | "The gods look at one another, and then at the grass." (was "...Who will risk it?") | Gylf 34: every god refuses to put a hand in the wolf's mouth until Tyr does. "At the grass" is our framing. Also removes the second question in the chapter. | dry |
| N-106 (d3 N-105) | "His mother, Frigg, will not take the chance." / N-107 "She goes to everything in the world and asks for a promise." | Gylf 49: after Baldr's dreams the gods take counsel and Frigg takes the oaths. "Will not take the chance" frames that. | warmth |
| N-131 (d3 N-130) | "His wife, Sigyn, sits by his side with a bowl to catch the drops." | Voluspa 35 (Bellows): "By his side does Sigyn sit, nor is glad to see her mate". Gylf 50: Sigyn holds a basin under the venom. | warmth |

Dry lines elsewhere (N-031, N-045, N-047, N-084, N-088) were not touched. The re-hook N-015 and N-011 "Well, almost nothing." are also dry but are counted under section 1.

## 5. Calls to action

| Id | Time | Words | Spoken line | Status |
|---|---|---|---|---|
| N-016 (CTA 1, soft) | 0:44 | 14 | "These myths come straight from the sources, so follow the channel for the rest." | Kept. Passes the tell check (no not-X-but-Y, no moral). Moved one beat later: it now holds the re-hook plate (Ymir's head) so the re-hook is not interrupted. |
| N-095 (CTA 2, story-tied) | 5:21 | 9 | "Follow the channel to see how this fight ends." | Kept. |
| N-174 (CTA 3, closing) | 10:03 | 12 | "If this was your kind of story, come back for the next myth." | **Rewritten.** d3 said "...follow the channel. The gods of Egypt are next." (Egypt not committed). Same register, different wording from CTA 1 and 2 ("come back", not "follow the channel"), points to the next lane without naming it. Holds the Snorri plate (N-173). |

## 6. NEW CLAIMS

Texts checked this run: Bellows 1923, archive.org `poeticedda00belluoft` (full text, fetched from the host; sacred-texts not used). Gylfaginning claims were checked in the earlier fact-check (FACTCHECK-N.md, Brodeur 1916) and were not changed; they are listed as PASS-by-prior-check.

| # | Claim (beat) | Source locator | Text read | Verdict |
|---|---|---|---|---|
| H1 | The clouds are its brain (N-002) | Grimnismal 41 (Bellows) | "Mithgarth the gods from his eyebrows made, And set for the sons of men; And out of his brain the baleful clouds They made to move on high." | **PASS.** Verified this run. |
| H2 | The sea is blood (N-003) | Grimnismal 40; Vafthruthnismol 21 | Grimnismal 40: "Out of Ymir's flesh was fashioned the earth, And the ocean out of his blood; Of his bones the hills, of his hair the trees. Of his skull the heavens high." Vafthruthnismol 21: "...the mountains were made of his bones; The sky from the frost-cold giant's skull, And the ocean out of his blood." | **PASS.** |
| H3 | The mountains are bones (N-004) | Vafthruthnismol 21 | as above ("the mountains were made of his bones") | **FIX locator only.** The brief cites Grimnismal 40, which says "the hills". The narration is accurate, but the trace now cites Vafthruthnismol 21 for "mountains" and notes Grimnismal 40's "hills". |
| H4 | The sky is a skull (N-001) | Grimnismal 40; Vafthruthnismol 21 | "Of his skull the heavens high" / "The sky from the frost-cold giant's skull" | **PASS.** |
| H5 | In Norse myth, the world was a giant once (N-005) | Voluspa 3; Gylf 8 | Voluspa 3: "Of old was the age when Ymir lived;" Gylf 8: the earth is made of Ymir's body | **PASS** (Gylf by prior check d3 N-024 to N-028). |
| H6 | Three brothers took him apart (N-006) | Gylf 6-8 | Odin, Vili and Ve slay Ymir and make the world from the body (Voluspa 4: "Bur's sons lifted the level land") | **PASS** (Gylf by prior check d3 N-019 to N-023). |
| H7 | He built everything from a corpse (N-008) | Gylf 8; Grimnismal 40-41 | Earth, sea, hills, trees, sky (40) and clouds, Mithgarth from the eyebrows (41), all from Ymir. Not from the corpse: Asgard (Gylf 9), Ask and Embla (trees, Gylf 9), sun and stars (sparks from Muspellsheim, Gylf 8), Yggdrasil. | **PASS, hedged.** "He" is Odin as one of three builders; "everything" means the physical world you stand under. Flagged for William in section 1. |
| H8 | And then he was told how it would end (N-009) | Voluspa 1, 28-30, 31-66 | Voluspa 1: "Thou wilt, Valfather, that well I relate Old tales I remember of men long ago." Voluspa 28: "Alone I sat when the Old One sought me, The terror of gods, and gazed in mine eyes: 'What hast thou to ask?...'" Voluspa 30: "Wise was my speech and my magic wisdom; Widely I saw over all the worlds." Bellows note 30: the seeress is "induced to proceed with her real prophecy (stanzas 31-66)"; note 28: "of the fate in store for you." Voluspa 53: "When Othin fares to fight with the wolf". | **PASS.** The Voluspa is the seeress's account to Odin, and its second half is his end. "And then" follows the order of the poem (past, then prophecy), not a timeline claim. |
| H9 | But first, there was nothing at all (N-010) | Voluspa 3; Gylf 4 | Voluspa 3: "Of old was the age when Ymir lived; Sea nor cool waves nor sand there were; Earth had not been, nor heaven above, But a yawning gap, and grass nowhere." | **FLAG (William's text, unchanged).** Verified this run. True of land, sea and sky; not true of "nothing at all" (a gap, Ymir, ice and fire already exist). N-011 "Well, almost nothing. Only a great gap..." makes it right on the next beat. |
| E1 | "Well, almost nothing." (N-011) | (ours) framing | Voluspa 3, Gylf 4 | **PASS** (framing that corrects H9). |
| E2 | "The skull in the sky is still on his shoulders, for now." (N-015) | (ours) framing | Grimnismal 40 (skull becomes the sky), Gylf 8 | **PASS** (framing; no new claim). |
| E3 | "...and then at the grass." (N-072) | (ours) framing | Gylf 34 | **PASS** (framing). |
| E4 | "Frigg will not take the chance." (N-106) | (ours) framing | Gylf 49 | **PASS** (framing). |
| E5 | Sigyn "sits by his side" (N-131) | Voluspa 35 (Bellows) | "By his side does Sigyn sit, nor is glad To see her mate: would you know yet more?"; Gylf 50: "Sigyn, Loki's wife, sat by him with a basin to catch the venom" | **PASS.** Verified this run. |
| E6 | Odin one eye in all plates, including before the well (variant rule) | n/a, a casting rule | William's rule | Not a text claim; the narration at N-046 still says the eye is given at the well. |

Could not verify this run: Gylfaginning (Brodeur 1916) was not re-read; its claims rest on the earlier FACTCHECK-N pass. The Bellows OCR text has line breaks inside stanzas; quotes above join them.

## 7. voicecheck output

`python3 -I scripts/voicecheck.py norse/SCRIPT-N-draft4.md` (run from `projects/bluepill/`):

```
norse/SCRIPT-N-draft4.md: 174 beats, 1527 spoken words, 0 flags
```

Zero flags. (First run found one: N-050's triad, fixed.)

## 8. Open items for William

1. Hook text choices listed in section 1 (N-010 "nothing at all", N-008 "everything", N-005 "In Norse myth,").
2. Trim N-026 and N-027 (hook repeats) or keep? Section 1, flag 5.
3. Bite beat N-077 keeps Tyr's hand; the stump starts at N-078. Change if you want the stump on the bite beat.
4. Chapter title "The Christian Who Saved the Gods": "saved" is a big word.
5. The master promise pays at about 82%, not 90%.
