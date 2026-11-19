# HOOKS-R3.md: Baba Yaga, third hook round (2026-11-18)

Why R2 missed: R1 ("a skull on a pole stops in front of a woman") is a scene with no anchor. The viewer does not know who the woman is, why anyone should care, or what is strange about it yet. William said it does not grasp him. His best hook so far is the Everglades cold open, so R3 copies its structure.

## The Everglades structure (William's wording, locked 11/15)
> A federal court says nearly 80 percent of the adult men in one Florida fishing community were arrested or indicted. In 1981, the county sheriff asked the federal government for help putting an end to an international drug smuggling operation that took over an entire city. Two years later, it came.

Three sentences, about 55 spoken words.
1. **The result, first, as a sourced fact with a number.** An authority (a federal court) states an outcome so extreme it sounds false. No scene, no setting, no adjectives. The viewer gets the stakes in sentence one.
2. **Rewind to a dated, human origin.** One small person asks one big power for help, and the problem is named at its real scale ("took over an entire city"). This is the cause of sentence one, told as a request.
3. **A four-word flat line that delays the answer.** "Two years later, it came." It does not say what came or what it cost. The viewer is left asking what help looked like, and why that outcome followed.

Mechanism in one line: extreme outcome stated flatly, then the plea that started it, then a short line that says help arrived without saying what help did. Nothing is described and nothing is explained. The facts carry it.

How it differs from our rules in VOICE.md: it is not a picture. It is a statistic and a plea. The "sky is a skull" pick and this one share one thing: both are strange, specific, true, and leave the next step open. William can read both, so the rule is "strange and specific", not "must be a picture".

## Applying it to Baba Yaga
Slot 1: the outcome nobody expects (three people burned to ashes, the witch touches none). Slot 2: the dated request (a stepmother sends an eight-year-old for fire). Slot 3: a short flat line that delivers the fire without saying what the fire does.

**A. RECOMMENDED (closest copy, about 50 words)**
"The most famous Baba Yaga story ends with three people burned to ashes, and the witch never touches any of them. It starts when a stepmother puts out every fire in the house and sends an eight-year-old girl into the forest to borrow a light. The girl brings one back."
- Slot 3 mirrors "Two years later, it came." It is flat, short, and open: what kind of light?
- Matches the title "Baba Yaga Never Touched Her".
- Gives away the three deaths, not who dies or how. Spine beat 10 stays the payoff (who burns, and why the lamp does it).
- Fact-check: "ends with three people burned to ashes" (A, ending (v)); "puts out every fire" (spine note 1, (v)); "eight-year-old" (spine note 2, (v)).

**B. Authority first (about 52 words)**
"In the 1850s, a Russian folklorist wrote down a story where a stepmother sends an eight-year-old girl to Baba Yaga to get fire. The witch lets the girl go home alive, with the fire. Within a day, the stepmother and both of her daughters were ash."
- Slot 1 is the sourced authority, slot 3 is the ash. Closer to the "federal court says" opening, but it spends the ending in the final line, so there is less left to wonder about.
- Fact-check: the date is Afanasyev, 1855-63 (use "1850s" only after the lock).

**C. Delayed answer (about 48 words)**
"A girl is sent into the forest at night to ask a witch for fire. The witch has a fence made of human bones and a rule about visitors. The girl follows the rule, gets the fire, and carries it home to the people who sent her."
- Slot 3 is the longer version of "it came": the fire arrives at the house that wanted her gone. Weakest on a number; no authority sentence.

## Pick
1. **A**. It has the number, the authority-free flat statement, the dated human request and the four-word-style close. The close is the strongest part: "The girl brings one back." tells the viewer help arrived and withholds what it did.
2. **B** as backup if William wants the authority line in.

## Open question for William
In Everglades the result is the number (80 percent). Here the number is three (people burned) or eight (her age). Is that strong enough, or does he want a second number in slot 1, for example how many tales or how old the story is? Any new number must come from a fact-checked source before it goes in.

Run `python3 -I scripts/voicecheck.py` on the winner before it goes into the script (VOICE.md).

## William's rewrite (11/18) and the working version
William: option A "reads weird". His shape: "The most famous Baba Yaga story ends with a family burned to ashes. It starts when a stepmother sends an eight-year-old girl into the forest to borrow fire. What the girl brings back...." Kept: "a family" (clearer than "three people"), "borrow fire" (stranger than "a light"), the dropped "puts out every fire" and the dropped "witch never touches any of them" (the title carries that). Changed: the trailing ellipsis cannot be narrated, so the last line becomes a flat sentence.

**A2 (working, pending William's pick), 40 words:**
"The most famous Baba Yaga story ends with a family burned to ashes. It starts when a stepmother sends an eight-year-old girl into the forest to borrow fire. What the girl brings back is exactly what she was sent for."

Alternate closers: "The girl comes back with it." / "The girl brings back the fire." (plainest, closest to "Two years later, it came.")
Fact-check: "family burned to ashes" (A, ending (v)); "eight-year-old" (W (v)); "most famous" (Afanasyev no. 104 / Vasilisa the Beautiful is the best-known Baba Yaga tale (v)). voicecheck.py returned 0 beats on a bare hook file, so the check has not actually run; run it on the full script.
