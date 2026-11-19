# BRIEF-DRAFT3: make the Norse script a story strangers will watch (hook + CTAs + pull)

Worker: Sonnet. Context cap 150k. Read only the files named here. Do not read session history. Write only inside `projects/bluepill/norse/`. Do not touch `library/`, do not generate images or audio, do not send messages.

## Read first
- `norse/SCRIPT-N-draft2.md` (current script, 175 beats, fact-checked)
- `norse/FACTCHECK-N.md` (what is verified; your new claims need the same standard)
- `norse/BRIEF-SCRIPT.md` (original format rules: beat id, spoken text, `shot:`, `state:`, `trace:`)
- `video2/RECIPE-SCRIPT.md` and `refs/RECIPE-2026-11-13.md` section 4 and 7 (grammar, sentence length)
- `projects/bluepill/PROCESS.md` Stage 2 (shape, rules)

## William's feedback (2026-11-14, verbatim intent)
1. The opening has no hook. Right now only people who already want "the whole story of Norse mythology" would stay. We want the opposite: someone who never heard of this and was not looking for it should see the first 20 seconds and be hooked.
2. First 20 seconds must be extremely engaging.
3. Make the script great first, then edit.
4. We want people to follow the channel, so add a call to action a couple of times.

## Job
A. HOOK. Write THREE alternative cold opens, each 45-60 spoken words (about 20 s), each built on a different angle. Rules:
   - Open on a concrete, strange, human moment or a startling fact a stranger can feel in one sentence. No "nine worlds hang from one tree" encyclopedia opening, no "welcome", no "in this video".
   - Curiosity gap: raise a question the viewer cannot answer, and promise the payoff inside the video (the ending of the gods, a prophecy that cannot be dodged, a god who knows how he dies). Specific beats vague.
   - Stakes within 10 s, an escalation within 15 s, an open loop closed only later in the script (name which beat closes it).
   - Short sentences (mean 8-11 words), no filler, no questions stacked more than one. Calm, dry voice stays (Daniel). No hype words ("epic", "insane").
   - Only cast already in draft 2 (28 cards). No new characters or places. Every shot line must be filmable and obey the state ledger (only named figures appear).
   - Every factual claim must trace to the Eddas the way draft 2 does; mark anything new with `trace:` and add it to a "NEW CLAIMS FOR FACT-CHECK" list.
   Then the existing "Let us start at the beginning." bridge must still work after each option; adjust the bridge sentence if needed.
B. MID-VIDEO PULL. Without changing facts, add at most 4 spoken open-loop lines at chapter ends or starts (a line that promises what is coming: "That is the last time anyone trusts the wolf." style). Keep each under 12 words. Do not add more than 60 words total to the script.
C. CALL TO ACTION, spoken by Daniel, natural voice, no on-screen text (PROCESS rule 8), no begging. Three placements:
   1. Soft, about 0:35-0:50, right after the hook payoff or first chapter beat: one line (example register: "If you want every myth told straight, follow the channel.").
   2. Mid-video, at a natural story beat just before a cliffhanger (about 5:00-6:00): one line tied to the story ("Follow if you want to see how this ends.").
   3. Final 20 s: one clear line plus a pointer to the next video's lane (Egyptian gods) without a date promise.
   Each CTA is 8-18 words, different wording each time, as narrator asides in the same shot, not new shots. List placements and beat ids.
D. Produce `norse/HOOK-OPTIONS.md`: the three hooks in full beat format (new ids N-H1a-01 ... etc.), a one-line strategic note on each (what a stranger feels, what loop it opens, where it closes), and your recommendation of which to use and why in three sentences.
E. Produce `norse/SCRIPT-N-draft3.md`: draft 2 with your RECOMMENDED hook swapped in for the cold open, the pull lines and CTAs inserted, beat ids renumbered cleanly (document the old-to-new mapping in a table at the bottom), header updated (word count, sentence count, estimated runtime at 150 wpm; target total at most 1,600 words so the video stays near 10:30 raw, tell William if you exceed it). The rest of the story stays as draft 2 except lines you change to close the hook loop.
F. Produce `norse/DRAFT3-CHANGES.md`: bullet list of every change (beat ids), the NEW CLAIMS FOR FACT-CHECK list, and any shot lines that need a new library entity (there should be none).

## Quality bar
- A stranger scrolling past must have a reason to stay at second 5, second 20 and second 45. Read your own hook aloud (count syllables) before you finish.
- No claims beyond the sources; if a dramatic framing needs a stretch, cut it.
- Beat formats identical to draft 2 so `build` scripts keep working.

## Output
Final message: files written, word and runtime totals, recommended hook with the full spoken text of the three hooks (so William can read them in chat), the CTA lines with beat ids, and any claim you could not source.
