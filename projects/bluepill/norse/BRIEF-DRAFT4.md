# BRIEF-DRAFT4: Norse draft 4 = draft 3 with hook C4, no Egypt mention, voice-file pass

Worker: Sonnet. Context cap 150k. Work only inside `projects/bluepill/norse/`. No images, no audio, no spend, no messages. Do not read session history.

## Read first
- `projects/bluepill/VOICE.md` (new; binding. Read every section, especially hooks, tone registers, "you", structural tells, CTAs)
- `norse/SCRIPT-N-draft3.md`, `norse/HOOK-OPTIONS.md` (hook C), `norse/DRAFT3-CHANGES.md`, `norse/FACTCHECK-N.md`
- `norse/BRIEF-SCRIPT.md` (beat format: id, spoken text, `shot:`, `state:`, `trace:`)

## What William decided (2026-11-14)
- He chose hook C ("The sky is a skull") over A and B. A painted nothing and confused him; B told him exactly what would happen. C made him want more.
- A vague, exciting glimpse of the ending is fine in the hook ("it ends in fire and almost every god dies"). Narrating the sequence is not.
- Tone: calm baseline, with dry humour and warmth on top. The narrator may address the viewer ("look up").
- Do NOT mention Egypt in the voice-over. Egypt is not committed yet.

## The hook to use (William's final pick, about 25 s). Replace the cold open of draft 3 (all hook beats and the old bridge) with exactly this spoken text, split into beats the way draft 3 splits them:
"The sky is a skull. The clouds are its brain. The sea is blood, and the mountains are bones. In Norse myth, the world was a giant once, until three brothers took him apart. One of them was Odin. He built everything from a corpse, and then he was told how it would end. But first, there was nothing at all."
- Word for word. If a line breaks a VOICE.md rule, do NOT change it; flag it in DRAFT4-CHANGES.md and let William decide.
- "But first, there was nothing at all." is the bridge into chapter 1. Make sure chapter 1's first story beat works right after it and still pulls forward (re-hook, no meta line).
- Shots: reuse existing chapter 1 places and figures (sky-as-skull, Ymir's body, the three brothers, Odin, empty void/Ginnungagap). No new library entities. Every `state:` names only the figures in the shot. Beats must be filmable. The viewer must SEE the picture from the narration alone (William's test).
- Sources for new claims: clouds from his brain, Grimnismal 41; sky from skull, sea from blood, mountains from bones, Grimnismal 40; three brothers took him apart, Gylfaginning; Odin told the ending, Voluspa 28-30 (seeress); "nothing at all", Voluspa 3 (earth not found nor heaven above). Re-verify Grimnismal 41 and Voluspa 3 against Bellows 1923 (archive.org `poeticedda00belluoft`) and quote the stanza text in your note; sacred-texts.com is blocked from this host. "Built everything from a corpse" must be defensible: say how in the note.

## Variant cards (William, binding)
- In every `state:` line, name variant characters explicitly: "Tyr (hand)" before the binding of Fenrir, "Tyr (stump)" from the moment the hand is bitten off onward. Odin keeps ONE eye throughout the whole video (no two-eyed Odin anywhere). Add a short "Variants" table to the header listing each variant and the beat id where it changes. Plate generation reads the card named in `state:`, so never leave a variant implicit.
- Keep the Snorri 1241 beat.

## Other changes
1. CTA 3 (closing) must not name Egypt (William: Egypt is not committed). Rewrite it in the same register, 8-18 words, different wording from CTA 1 and 2, e.g. an invitation to follow for the next myth. CTAs 1 and 2 stay unless VOICE.md says they break a rule (CTA 1 currently says "These myths come straight from the sources, so follow the channel for the rest." Keep if it passes the structural-tell check; otherwise fix).
2. Make sure no beat anywhere says "Let us start at the beginning" or any meta line banned in VOICE.md. Run `python3 -I scripts/voicecheck.py norse/SCRIPT-N-draft4.md`; zero flags except harmless ones you justify.
3. Apply VOICE.md section 8/structural tells to the whole draft: list any beat that is a one-line closer restating the previous beat, a not-X-but-Y, an inflated-significance line (check the Snorri chapter and the origin material), or a shallow -ing tail. FIX only those; leave the rest. Give each change a one-line reason with the VOICE.md rule number.
4. Warmth and humour: find at most 3 places where a single dry line or one warm human beat can be added or sharpened without a new claim (suggested places: Tyr stepping forward, Baldr and Frigg, Thor and the serpent). Each must be sourced or clearly framing. Keep the total under 1,650 words.
5. Add re-hook: the first story beat after the hook (chapter 1, first 30-60 s) must pull forward without a meta line.

## Deliver
- `norse/SCRIPT-N-draft4.md` (same format and header style; renumbered; old-to-new id table at the bottom; header with word count, sentences, runtime at 150 wpm)
- `norse/DRAFT4-CHANGES.md`: every change with beat ids and the VOICE.md rule it serves; a NEW CLAIMS table with source locators and PASS/FIX for each (you verified Grimnismal 41 and Voluspa 3); the three VOICE.md tests applied to the hook with a one-line verdict each; voicecheck output
- Final message: files, word count and runtime, the hook as spoken, CTA lines with ids, anything you could not verify.
