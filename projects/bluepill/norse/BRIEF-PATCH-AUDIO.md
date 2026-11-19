# BRIEF-PATCH-AUDIO: two script additions (William, 2026-11-14), verify claims, re-record two passages

Worker: Sonnet, context cap 60k. No images. Do not read session history. Work in `projects/bluepill/norse/` (audio-n/ and FACTCHECK-N2.md). ElevenLabs spend cap: 2,400 characters total.

## What changed in `norse/SCRIPT-N-LOCKED.md` (backup: `SCRIPT-N-LOCKED.pre-teaser.md`)
1. New beat **N-047a**: "And one of those secrets is his own ending, which a seeress has told him." (chapter 2, after N-047).
2. Old closing beat N-174 replaced by **N-174 to N-178**, a teaser: "Some of the gods barely got a mention here. / Freyja and Freyr. Idunn and her apples. / A giant who stole Thor's hammer, / and a war between two families of gods. / Follow the channel for part two. [CTA]". Egypt is still not named.
Title is now "The Story of Norse Mythology, Creation to Ragnarok, in 10 Minutes" (no "ENTIRE").

## Tasks
1. **Fact-check the new claims** against Bellows 1923 (Poetic Edda) and Brodeur 1916 (Prose Edda) on archive.org (`poeticedda00belluoft`, `proseedda00snor`; sacred-texts.com is blocked): Voluspa 1 and 28-30 (seeress speaks to Odin); Freyja and Freyr are Vanir (Gylfaginning, Njord/Frey/Freyja); Idunn keeps the apples that keep the gods young (Gylfaginning 26 / Skaldskaparmal); Thrym steals Thor's hammer (Thrymskvitha 1-2); the Aesir-Vanir war (Voluspa 21-24, Ynglinga saga is not needed). For each: PASS or FIX with the locator and the quoted words. If a line needs a FIX, rewrite the spoken line minimally in SCRIPT-N-LOCKED.md (keep word count under 1,650) and tell me which words changed. Write `norse/FACTCHECK-N2.md`.
2. **Re-record** only the passage that contains N-047a and the final passage (N-162 to N-178), using the same settings and respellings as before (`audio-n/SPOKEN-TEXT.md`, `audio-n/scripts/`). Do not re-record any other passage. Add respellings for Freyja ("Fraya"), Freyr ("Fray"), Idunn ("Eedoon"), Thor's hammer is spelled "hammer" so no respelling; keep the existing Mjolnir respelling if it appears.
3. Re-run `assemble.py` and `quality.py` on all passages: update `narration_voice_only.wav/.mp3`, `words.json`, `beats_timing.json`, `quality.json`, `SPOKEN-TEXT.md`, `plan.json`. If the two abrupt events from before (passages P2 and P4) are locatable with `quality.json`, give their timestamps. Keep the previous files as `audio-n/previous/` before overwriting.
4. Report the new runtime, wpm, chapter start times, characters used, and the verify results.

## Final message (max 8 lines)
Verify result per claim (PASS/FIX), words changed if any, new runtime and chapter starts, characters used, quality result, abrupt-event timestamps if found.
