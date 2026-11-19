# REPASS-FABLE.md: second pass on the SCRIPT-V3 narration (Fable, 2026-11-13)

Nothing re-rendered, uploaded or sent. `narration_voice_only.*` untouched. New files: `narration_voice_only_tight2a.*`, `narration_voice_only_tight2b.*`, `_work/words_tight2{a,b}.json`, `_work/assembled_tight2{a,b}.json`, `scripts/tighten2.py`. I cannot hear audio; everything below is measured from `words.json` and the wav.

## 1. Where the 11:58 comes from (measured)

| Quantity | Value |
|---|---|
| File | 717.6 s (11:58) |
| Articulated speech, script words only | 443.6 s = 226 wpm while actually speaking |
| Narrator in-beat rate (speech plus pauses inside the beat) | 154 wpm, on the script's 155 wpm estimate |
| Silence between words | 253 s (35% of the file) |
| of which inside beats | 210 s (1,622 gaps); sentence-end pauses avg 0.55 s (122), comma pauses avg 0.37 s (120) |
| of which between beats | 43.5 s, already tightened by the first pass |
| Attribution handover (21 "said X" lines) | 34.5 s against 8 s if unattributed: about 26 s net |
| Pauses >= 0.3 s | 28.3 per min; FORMAT-BIBLE target <= 2 per min, sentence gap 0.15-0.25 s |

So the voice is not slow. The overrun is the model's own pauses inside sentences, which the first pass left untouched by design, plus the A2 attributions.

## 2. Tightened variants (no API spend, no voice change)

`tighten2.py` caps the inside-beat pauses (sentence end / comma / other), keeps the inter-beat targets and the scripted holds (beats 20, 32, 39, 44, 50, 80, 96, 105, 113, 119), and cuts only in the quietest stretch with a 20 ms crossfade.

| Variant | Caps (s) | Runtime | Pauses >= 0.3/min | Gaps >= 0.6 | Joins |
|---|---|---|---|---|---|
| tight (first pass) | none inside beats | 11:58 | 28.3 | 50 | 0 abrupt, 0 clicks |
| tight2a | 0.45 / 0.32 / 0.25 | 11:30 | 26.7 | 6 (all scripted) | 0 abrupt, 0 clicks |
| tight2b | 0.35 / 0.25 / 0.20 | 11:11 | 20.0 | 6 (all scripted) | 0 abrupt, 0 clicks |

Both -19.0 LUFS, TP -1.5. Listen first in tight2b at the hardest-cut sentence ends: 0:07.6 (beat 2), 1:11.9 (13), 1:45.5 (21), 6:57.3 (76), 9:32.6 (104); and the kept holds at 2:44.9 (32 "friends first"), 3:13.0 (39), 3:43.9 (44). Stamp lines in tight2b: 7:21.7, 8:48.9, 9:40.7, 10:23.6; "Nobody." 10:57.5.

## 3. Getting from 11:11 to the 10:20-10:40 target

Estimated from the timing data; order is cheapest first.
1. **Drop the 15 bare attributions** ("said Odysseus", "the crew urged", "a crewman asked"...): about 26 s. Keep the six that carry a manner (28 quite calmly, 37 bored, 39 flatly, 44 softly, 85 awkwardly, 111 muttered). RECIPE-SCRIPT.md already says the reference uses no "he said" tags; sprites identify the speaker. Needs a re-render of the nine affected passages (about 5,500 characters). With tight2b: about 10:45.
2. **Cut beats 77 and 89** (unnamed "critics say"; Burkert via Wikipedia), the two weakest-sourced lines in the script's own trim list: about 10 s. With 1: about 10:35. Re-render P11 and P12 only.
3. Only if still long: speed 1.05 (about 30 s). Not recommended first; it is the one lever that touches the Daniel timbre William approved.
The first pass's full cut list (77, 36, 23-25, 89, 94) is the script's own section (g) list; 23-25 and 36 cost a character exchange and the axe simile for about 15 s, so take them last.

## 4. Text fixes for any re-render
- Beat 104 was sent as "twelve fifty B.C.." (double stop from the respell step on "BC."): it produced the longest gap in the file, 0.92 s. Fix the respell so a trailing stop is not doubled.
- Hyphenated respellings get split into tokens: "Thee-ockritus" came back from whisper as "the ocretus", "Paw-sayneeus" as "poor sineas" three times out of three, "Ah-gheereh" as "agiri". Phoneme tags are not available on `eleven_multilingual_v2` (ElevenLabs docs: flash_v2 only), so use unhyphenated respellings ("Pawsaynius", "Theeockritus", "Ageereh") or a pronunciation-dictionary alias rule, and test each word alone (about 100 characters each) before the passage render. Whisper is not a pronunciation judge; William's ear is.

## 5. Agreed with the first pass
Same Daniel as the control (pitch, spread, centroid within the control's range); no clicks or abrupt joins; loudness on target; the cut list exists in the script.

## 6. Outcome (2026-11-13, later)
William approved tight2b and the cuts (beats 77, 78, 79, 89, 91; beat 04 shortened). `SCRIPT-V4.md` written (V3 numbering kept, cut beats marked). `assemble.py` now applies the tight2b caps by default; `plan.py` fixes the "B.C.." double stop. P01, P11, P12, P13 and P14 re-rendered (2,643 characters, 5 calls, P14 only because the B.C. fix changed its text). The V3 take is archived in `v3-take1/`. New master `narration_voice_only.*`: 10:43, 1,604 script words, -19.0 LUFS, 0 abrupt joins, 0 clicks; the only gaps over 0.6 s are the scripted stamp beats and the "B.C.," commas.
