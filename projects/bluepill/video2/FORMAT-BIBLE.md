# FORMAT-BIBLE.md: the Unknown Frequencies (UF) recipe, tool-agnostic, with our ingredients (The Myth Ledger)

Date 2026-11-12. Nothing generated, uploaded or sent. Reference: UF, "The ENTIRE Story of The Odyssey Explained" (mJS-QVw8lzY, 13:08).
Sources: `REVIEW-ref-vs-draft-2026-11-12.md` (the Editor's measurements, called "Editor" below), `REF-unknown-frequencies.md`, `CHARACTER-STYLE-REF.md`, `PIPELINE-RECOMMENDATION.md`, `tests/stress_test/SCORES.md`, `tests/crew_test/SCORES.md`, `video2/RECIPE-SCRIPT.md` (script grammar, written by another worker), and my own viewing of the 142-shot sheets `analysis_teardown_out/refshots_0-3.jpg`.
Labels: **[V]** measured on files, **[E]** estimate or hand count from viewing, **[U]** unknown or untested.
Scope: this document says *what the video is*, not *how it is rendered*. Any tool that can place images at word times and cut hard can build it. Tool decision: `video2/TOOLING-EVAL.md` (Remotion stays; audio is mixed in full ffmpeg).

---

## 1. Script grammar (pointer only)

The full grammar, with exact UF lines and our matching ingredients, is in **`video2/RECIPE-SCRIPT.md`**; do not duplicate it here. The numbers the visual layer depends on:

| Script property | UF [V, Editor] | Target for us |
|---|---|---|
| Pace | 178 wpm | 165-175 wpm |
| Sentences per minute | 18.5 | 18-21 |
| Words per sentence, mean / median | 9.6 / 8 | 8-10 / 6-8 |
| Sentences of 6 words or fewer | 39.5% | 40-50% |
| Questions per minute | 1.22 | 1-1.5 |
| Voiced dialogue exchanges per 13 min | 16 | 12-16 per 10 min |
| Action verbs per 100 words | 6.3 | 5-6.5 |
| Hedges per 100 words | 0.38 | 0.5-1.0 (hedges become stamps and short verdict lines) |
| Gags per minute / stakes lines per minute [E] | 1.1 / 1.5 | 1 / 1.5 |

One cause per beat, a number that measures the damage, a button line, a hard cut. Each sentence is one *beat* in the sense of section 2: the script is the source of the storyboard, never the other way round.

---

## 2. Beat grammar: what appears on screen per sentence

**Unit.** One spoken sentence (or one dialogue line) = one beat. The storyboard assigns every beat a shot, zero or more timed events, and optional SFX. Every beat gets at least one visible change (cut, pop, pose swap, counter tick); two consecutive beats may share a picture if the second adds a pop.

**Measured UF cadence [V, Editor]**

| Measure | UF | Our target | Draft v1 (what we must leave) |
|---|---|---|---|
| Picture changes per minute (new picture, ≥30% of pixels) | 10.7 | 9.5-12 | 8.5 |
| Pop-ins, sprite swaps and label appearances per minute | 7.4 | 6-8 | 2.8 |
| All visible change moments per minute | 18.1 | 16-19 | 11.4 |
| Median gap between visible changes | 2.2 s | ≤ 2.5 s | 4.6 s |
| p90 gap | 6.7 s | ≤ 7 s | 8.0 s |
| Longest gap | 24 s (one held beat) | ≤ 15 s; one 20-24 s held beat per episode allowed | 31 s |
| Gaps over 8 s | 17 in 13.1 min (1.3 per min) | ≤ 1 per min | 10 |
| Median shot / p90 shot | 4.2 s / 12.3 s | 4-4.5 s / ≤ 12 s | 4.8 s / 13.2 s |
| Frozen frames (no movement) | 91% | ≥ 85% | 8% |
| Frames in constant slow motion | 4% | ≤ 5% | 72% |

For a 10:00 episode that is about 105 picture changes, about 70 pops or swaps, about 180 visible events.

**Beat types and what each shows** (the storyboarder picks one per sentence; events anchor to the word that earns them)

| Beat type | Trigger in the script | Screen | Event timing |
|---|---|---|---|
| **Place or time shift** | "The next stop was...", "Ten years later" | Hard cut to a painted plate or map | Cut on the first word of the sentence, minus 0.05 s. A 1-3 word place label pops 0.0-0.15 s after the place name |
| **Speaker change / dialogue** | A quoted line, a name before a line | White cutaway with two sprites, or pose swap on the speaker | Sprite enters or swaps on the first word of the line. Optional bubble text pops on the same word |
| **Number or count** | Any numeral | Counter or number label | Pops on the numeral's onset; later changes tick in 15-per-second steps (stop-motion) |
| **Reaction or gag** | The punchline | White cutaway, sprite swapped to the reaction pose | Cut on the last word before the punchline; hold 1.5-3 s |
| **Stakes tally** | "12 ships became one" | Counter shot or crossed-out icons | Each decrement on its word; ends the scene |
| **Source claim** | "Mayor writes...", "Hesiod says..." | Source chip in a fixed corner, 2.5 s, over whatever picture is on | Appears on the attribution phrase, no new shot, no card |
| **Verdict** | "As a one-eyed giant who eats sailors, no" | Stamp pops on the case board or on the plate | On the verdict word |
| **Time passing** | "weeks of this" | Rapid hard cuts, 0.6-1.0 s each (UF's loom run at 625-631 s [V]) | Allowed at most twice per episode |

**Density rules**
1. No sentence without a visible change; no gap over 8 s more than once a minute; none over 15 s except the one held beat.
2. A run of non-character shots (map, counter, card, inset) lasts at most 8 s, and at most two such shots in a row. (UF's longest non-character run is a few seconds; our draft had 32 s, 27 s and 17 s [V, Editor].)
3. A new picture at least every 12 s; a new event at least every 7 s.
4. Pops land 0-0.15 s after the word onset, using word-level timestamps from the voice provider. UF's own lag is not measured [U].
5. One idea per pop: one noun, one number, one stamp. Never two competing labels within 0.5 s.

---

## 3. Shot taxonomy and target shares

| Class | What it is | UF share of runtime [V durations, E labels] (shots) | Target for us, 10:00 | Min / typical / max |
|---|---|---|---|---|
| **A. Painted scene, character-led** | A painted plate with one or two principals (and tiny extras) | 63.2% (81 of 142) | **53%** (5:18) | 2 s / 4-6 s / 12 s |
| **B. White cutaway** | Pure white, 1-3 sprites, posed, with labels or bubbles | 17.1% (30) | **23%** (2:18) | 1 s / 3-5 s / 8 s |
| **C. Text beside a character** | Sprite plus one big lettered phrase or number | 4.5% (8) | **5%** (0:30) | 1.5 s / 2-4 s / 6 s |
| **D. Map** | Painted map plate with route arrows, labels, a counter, sometimes a sprite on it | 12.3% (14; 8 with route arrows, 2 with a character) | **11%** (1:06) | 3 s / 5-8 s / 12 s |
| **E. Counter or prop card** | A number from the story, a crossed-out grid, the case board with stamps | 0.8% (4, all numbers) | **4%** (0:24) | 1 s / 2-3 s / 5 s |
| **F. Inset or diagram** | Picture-in-picture, a labelled prop, our skull-style plates | 2.1% (5) | **3%** (0:18) | 2 s / 3 s / 6 s |
| **G. Title or chapter card** | Lettered title on a plain background | within E | **≤ 1%** (0:06, the episode title only; no chapter cards) | 2 s |

Text, map and diagram only (D+E+F+G): UF 15.2%, draft v1 39.5% [V], **target ≤ 19%, hard cap 22%**. Pure text cards: UF 0.8%, draft v1 20.0%, **cap 2%**; no card carries a claim or a citation (that is the source chip's job).

Notes on mapping to our assets:
- **A** is the baked flat-ink scene from `PIPELINE-RECOMMENDATION.md`: Odysseus-only, Odysseus + Cyclops, Cyclops-only, plus empty scenes. **Crew-centred baked scenes are 0%** until a method passes (0 of 7 first attempts did [V]); crew appear as extras, as a group sprite in class B, or as small figures in wide plates.
- **B** carries the shift of runtime from A to B (UF has 17%, we plan 23%) because cutaways cost no plates and are where our crew and jokes live.
- Colour balance [V, Editor]: UF has 25.6% white-dominant frames, mean luminance 135/255, near-black frames 2.8%. Our draft: 0%, 59/255, 40.1%. Target **white-dominant 15-25%, mean luminance ≥ 105, near-black ≤ 8%.**

---

## 4. Edit grammar

1. **Hard cuts only.** Between pictures: cut. UF has 127 hard cuts in 141 picture changes and 0 dissolves [V]; our draft had 53 crossfades in 146 boundaries [V]. No crossfade, dip, whip, slide or flash exists as an option in the build.
2. **Hold still.** 91% of UF frames are frozen [V]. No Ken Burns, no blanket push-in, no pan. Allowed motion, each by exception: a sprite sliding in (UF 659 s), letterbox bars closing (671.5 s), a stop-motion zoom through an object (695-698 s), a route drawing. At most 5% of frames in motion.
3. **Pops.** A sprite or label appears at once at word onset and scales 0 to about 1.06 and back to 1.0 over 0.2 s (6 frames at 30 fps; the spike's `popScale`, easeOutBack, overshoot constant 1.4). UF pops with no easing at all [V, Editor]; we keep the short ease as our own touch. Pose changes are **swaps**, never tweens. Entrances may slide 120-200 px over 0.15 s. Positions of sprites on white are bottom-anchored (feet), labels centre-anchored.
4. **Counters and routes** step at 15 updates per second (stop-motion feel, same as the spike).
5. **Label styles** (one hand-lettered all-caps display face for all of them; face and accent colour must differ from UF's, see section 9):
   - *Impact word*: 1-3 words, large; cream with dark outline on paintings, solid accent on white.
   - *Counter*: big number, optional unit word ("SHIPS"); decrements tick.
   - *Stamp*: rubber stamp, rotated 3-6 degrees, one verdict word (UNPROVEN, PLAUSIBLE, REAL, SUSPECT). Our signature; pops with a 0.2 s scale ease and a soft thud.
   - *Source chip*: small, fixed corner, 2.5 s ("HOMER, ODYSSEY 9", "MAYOR, 2000"). Same position in every video.
   - *Bubble*: hand-lettered text with a thin curved tail line, no box. Used for dialogue on class B shots.
   - *Place label* on maps, *arrow* or *pointer* on plates.
   Text on 40-45% of shots (UF 44% [E]); 1-3 words (bubbles may run to 8); never over a face; keep to the plate's negative space.
6. **No burned-in captions.** UF shows none in 142 sampled frames [V]; our draft put a serif caption on nearly every picture [V]. Captions ship as an uploaded SRT (YouTube auto-captions as backup). A word-synced caption render is an optional variant for Shorts only, never in the main video.
7. **Cards are props, not slides.** If a number or fact appears, it appears because the story says it: ships left, men lost, wagons. Claims and citations are chips and stamps, not cards.
8. **Frame rate and size.** Master at 1920x1080, 30 fps (UF's file is 60 fps [V]; 30 is fine because nothing moves continuously). 4K only when plates are generated at 3840 px; today's 1536 px plates would only be upscaled.
9. **Montage flicker** (time passing) uses 3-6 frame hard cuts, at most twice per episode.

---

## 5. Sprite system

### 5.1 How many poses? Derivation from the reference

I hand-counted recurring figures in the 142 shot frames (one frame per shot, so this undercounts: a shot can hold poses I did not see) [E]:

| Figure in UF | Shots seen | Distinct drawings seen (poses, expressions, group arrangements) |
|---|---|---|
| Host (skull face, helmet; their identity, we do not copy) | about 28 | 12 or more (talking, pointing up, shrug, dizzy, worried, shouting, arms wide, thinking...) |
| Odysseus (curly hair, beard) | about 45 | 14 or more (neutral, pointing, scheming with light bulb, tired at the helm, hands on rope, shouting, sad on the beach, aiming the bow...) |
| Penelope | about 10 | 6 or more |
| Circe | about 6 | 4 or more |
| Athena, Zeus, Aeolus, Tiresias | 2-3 each | 1-3 each |
| Crew (identical soldiers, groups of 3-6) | about 12 | 6 or more group arrangements |
| Monsters, gods and big figures | painted into plates, not sprites | n/a |

Estimate for UF: **about 75-90 distinct sprite drawings in 13 minutes**, concentrated in four recurring figures, of which about 14 drawings belong to the lead. [E]

**Our requirement for a 10-minute episode** (we have no host sprite; William chose story characters only, voice narrates [V, TOOLS.md]):

| Asset set | Drawings | Notes |
|---|---|---|
| Lead (e.g. Odysseus) | **14** | Core grammar below; mirrored copies count once |
| Antagonist or key supporting (e.g. Polyphemus, monster tier) | **8** | Mostly in plates; sprites for cutaway reaction shots |
| Two more speaking characters | **5 each = 10** | Enough for dialogue pairs |
| Group sprite sets (crew, neighbours, suitors) | **6** | Line-up, huddle, scared, cheering, rowing pose, fallen |
| Prop sprites (cheese wheel, wine cup, sack, stake, ship icon, skull, scroll) | **~10** | Single objects; counters use them |
| **Total episode 1** | **~48** | **Reuse across a mythology series is high: recurring cast about 60% [E], so new sprites per later episode about 20-25** |

**Core pose grammar for a principal** (14): neutral, talk (open mouth, gesture), point (left-right by mirroring), shrug, worried, scared, shouting, smug or proud, thinking (finger or chin), sad or crying, angry, surprised, back view, lying or asleep. Hold-object variants are prop sprites, not new poses. A sprite always faces right; the player mirrors it.

### 5.2 Asset specification

- **File:** PNG with alpha, one figure per file, tight bounding box plus 8 px pad.
- **Size:** master height at least 1,000 px for 1080p (our current cutouts are 1,004 px tall: Odysseus 448x1004, Cyclops 646x1004 [V]; a 780 px figure at 1080p downsamples 0.78x). For 4K we need at least 1,800 px; the image API sizes that allow it are not tested [U].
- **Generation on pure white (#FFFFFF),** flat ink outline, then cutout by flood fill: `pipeline/cutout.js` works because the dark outline stops the fill and leaves no halo [V, TOOLS.md]. Check every sprite on a dark and a mid-grey background for fringes.
- **Anchor:** feet-centre pixel stored in a sidecar JSON; `height_px_at_1080` stored too, so layout code places by feet.
- **Naming:** `<char>__<pose>__<variant>.png`, lowercase, e.g. `odysseus__shrug__a.png`, `crew__huddle__a.png`, `prop__cheese__a.png`. One `<char>.cast.json` per character: palette hexes, immutable features, pose list with tags (emotion, facing, hands, props), accepted date, source call id.
- **Immutable features** (from the stress test, Odysseus: wreath, blue sash, beard 11 of 11 held [V]; Cyclops: exactly one eye, no bells, plain rope belt [V]). They are checked on every pose.

### 5.3 Generating poses consistently with our image pipeline

What the tests say [V]: two locked refs flattened onto white per call; fixed identity paragraph per ref plus "do not copy the white background, layout or pose"; always the flat-ink clause; chain from an accepted flat-ink image when a setting is needed; do not list individual crewmen, describe the group in the plural and lead with the action. Odysseus-only scenes 4 of 4 passed, Odysseus + Cyclops 4 of 6, Cyclops-only 2 of 3, crew-centred 0 of 7. Style drift to painterly (5 of 16) is the largest failure. Two poses per character (neutral and a shouting pointing pose) held across four style options in `tests/chars_v3/sheet_poses.jpg`; style A (flat ink, leftmost column) held both for Odysseus and for the Cyclops [V, viewed today]. **Fourteen poses for one character in one session has not been tested [U].**

Procedure per character (agent: Art Director):
1. **Master.** One neutral full-body pose, flat ink, white background, approved by William (gate G2) before any pose is made. Lock it as `<char>_master`.
2. **Pose batch.** One call per pose: refs = master + the previous accepted pose; identity paragraph; "same character, pose: <pose text>, full body, feet visible, facing right, plain white background, nothing else in the frame"; flat-ink clause. Never name another character in the same call.
3. **Check** per pose with the stress-test attributes: identity features, style (flat ink, same palette and line weight), pose delivered, face readable at 280 px, no text or limb errors, clean white. Reject, adjust one thing, retry once; a second reject means rewrite the pose text, not a third retry.
4. **Cutout and verify** on dark and light; store sprite, anchor, cast.json.
5. **Budget and caps.** Expect about 30% first-attempt rejects [V, non-crew shots] so about 1.5 calls per accepted pose; at $0.05-0.10 per sprite call [E] the 48 sprites of episode 1 cost **about $4-7**; later episodes $1-3. Group sets are the risk (crew-centred 0 of 7): build them from the single approved crewman sprite placed several times with small offsets and swapped poses, which UF itself does (identical soldiers, each with a different expression [V, CHARACTER-STYLE-REF]), rather than generating a group in one call.

---

## 6. Background system: painted scene plates

- **Plate spec:** 1536x864 (16:9 accepted natively by the image API [V]), flat-ink clause, no text in the image, bright palette. Upscaled 1.25x to fill 1080p; **no crop-in beyond 1.1x** (our draft's B-shot crops at 1.3-1.6x were soft [V, QA-REPORT]); if a close-up is needed, generate a close-up plate.
- **Negative space:** every plate leaves a clear area (upper third or one side) for labels; the prompt asks for it.
- **Count per 10-minute episode:** class A is 53% of runtime = 318 s; at a typical 5.5 s per shot that is about 58 shot slots; about a quarter reuse a plate with a different overlay (UF reuses one plate across 8 consecutive shots for the loom sequence, shots 117-124 [V]); so about **44 generated plates**, plus **4-5 map bases** (routes, arrows and labels are code overlays) and **0 plates for cutaways** (white). UF has about 127 distinct compositions in 142 shots including cutaways [V, Editor], i.e. roughly 65-70 painted plates in 13 minutes [E].
- **Cost [E]:** 44 plates x 1.5 attempts x $0.10-0.15 = **$7-10**; maps at about $0.06 each [V, cheap test]; episode 1 total with sprites about **$12-20**, later episodes about $8-13. UF-style estimate in `REF-unknown-frequencies.md` was $5-12.
- **Mix by subject** (from the pipeline evidence): Odysseus-only, Odysseus + Cyclops, Cyclops-only and empty scenes are the proven core; wide shots carry the Cyclops or the crew, not Odysseus' face (190 px tall is unreadable [V]).
- **Light and colour:** day or lit scenes by default; night and cave plates are allowed but near-black frames stay under 8% of the episode. Avoid the slop tells: sunset glow, symmetric muscle men, stock Poseidon, ship-hull eye [V, Editor and TOOLS].

---

## 7. Audio grammar

| Element | UF [V, Editor] | Our rule |
|---|---|---|
| Voice | one narrator who performs character voices; pitch spread 4.7 semitones; pace 178 wpm | Narrator George (chosen by William [V]) plus **one fixed ElevenLabs voice per speaking character** (cast by blind test on one paragraph, about 6 candidates from the 21 premade voices); narrator never doubles as a character. Aim pitch spread ≥ 4 semitones by lowering stability and raising style, to be tested [U] |
| Pace | 178 wpm | 165-175 wpm; sentence gap 0.15-0.25 s |
| Pauses | pauses ≥ 0.3 s: 1.9 per min; none ≥ 0.6 s | ≤ 2 per min ≥ 0.3 s; none ≥ 0.6 s except the one held beat |
| Loudness | -19.4 LUFS, LRA 3.6 LU | **-16 ± 1 LUFS integrated, true peak ≤ -1.5 dBTP, LRA 3-5 LU** from performance, not compression (draft: -16.2 LUFS, LRA 1.7) |
| Floor between words | -50.8 dBFS broadband room tone, no tonal bed; dual mono | Same: low broadband room tone about -50 dBFS, no pad, no drone. Digital silence reads as dead air |
| Music | none detectable in gaps (cannot rule out music masked under speech [U]) | **No continuous bed.** Music only as 2-4 stingers per episode (cold open, big reveal, outro), each under 6 s |
| SFX | cut-synchronised transients on a minority of cuts at most [U, test cannot separate effects from sibilants] | Light tick or thud on at most half of the pops and on every stamp; one stinger on the verdict; nothing on ordinary hard cuts. Peak 10 dB under the voice |
| Dialogue | 16 voiced exchanges | Per-character takes with word timestamps (ElevenLabs `/with-timestamps`), each line placed by `adelay`; no overlap longer than 0.1 s |

Mix is done in full ffmpeg, not in the picture renderer: `amix` voices, `sidechaincompress` only if a stinger bed is present, `loudnorm=I=-16:TP=-1.5`, `alimiter`. A test of that exact chain ran in 0.54 s for 20 s and measured -15.5 LUFS, -1.0 dBTP (`video2/spike/out/mix_test.wav`) [V]. Voice budget: a 10-minute script is about 10,000 characters; three takes is about 30,000 of the 131,000-character Creator allowance [E from TOOLS.md].

---

## 8. QA checklist before any upload

Run on the **final mp4**, using the Editor's detectors in `analysis_teardown_scripts/` (cut, event, luminance, loudness) and a contact sheet every 30 s. Every item has a number or a yes/no.

**Pacing and edit**
- [ ] Picture changes per minute 9.5-12; pops and swaps per minute 6-8; all visible events per minute 16-19.
- [ ] Median gap ≤ 2.5 s, p90 ≤ 7 s, longest ≤ 15 s (one held beat up to 24 s); gaps over 8 s ≤ 1 per minute.
- [ ] Frozen frames ≥ 85%; frames in constant motion ≤ 5%.
- [ ] Crossfades 0, dissolve clusters 0, burned-in captions 0.
- [ ] Text, map or diagram only ≤ 19% of runtime (cap 22%); pure text cards ≤ 2%; no run of non-character shots over 8 s.
- [ ] White-dominant frames 15-25%; mean luminance ≥ 105/255; near-black frames ≤ 8%.

**Accuracy chips and sources**
- [ ] Every claim attributed to a scholar, ancient author or institution has a source chip within 1 s of the claim, 2.5 s long, same corner.
- [ ] Every number on screen traces to the fact-check table; every stamp matches the verdict in the script (UNPROVEN, PLAUSIBLE, REAL...).
- [ ] Dramatised dialogue is flagged once, early; no invented line is put in the mouth of a named scholar; Homer quotes stay close to the cited translation.
- [ ] Description carries the full source list, chapter timestamps and the pinned comment text.

**Characters and art**
- [ ] Identity attributes pass in every shot (Odysseus: wreath, sash, beard; Cyclops: exactly one eye, no bells); flat-ink style consistent (no painterly drift); no text, limb or prop-leak errors.
- [ ] No sprite fringe on white; no head cropped; labels stay in safe areas.

**Audio**
- [ ] -16 ± 1 LUFS, true peak ≤ -1.5 dBTP, LRA 3-5 LU; pauses ≥ 0.3 s ≤ 2 per min, none ≥ 0.6 s (bar the held beat); each speaker's voice id constant; no continuous bed; room tone present.

**Thumbnail and packaging**
- [ ] Three candidates; chosen one reads at 168 px wide on a phone; at most 4 words; own layout (section 9); no UF-style "IN N MINUTES" tag or two-characters-over-a-map template.
- [ ] Title promises the story first and the real-world check second; no claim the video does not prove.
- [ ] Compliance note recorded for this episode: YouTube's synthetic-content disclosure and inauthentic-content policy reviewed and the decision logged (William's current decision is no disclosure line; policy details not re-verified here [U]).

**Process**
- [ ] Private upload first; William's gate G4 passed; spend log updated; run recorded in the episode folder.

---

## 9. What is deliberately different from UF (originality guardrails)

Do not copy: UF's characters, fonts or thumbnails. We copy the *recipe* (grammar, cadence, shot mix), not the surface.

| UF element | Our rule |
|---|---|
| Skull-faced, gold-helmeted host sprite with red crest and cape | **No host.** Story characters only, voice narrates [William, 2026-11-12]. No skull face, no crested helmet figure as a recurring mascot |
| Odysseus as a bearded man with a large curly dark hair mass and grey cuirass; round blank faces with eyebrow acting | Our own Style A: flat-ink adult proportions, laurel wreath, blue sash, beard, readable faces (`CHARACTER-STYLE-REF.md`); different silhouettes, palette and costume; our heads are not UF's blank discs |
| Rust-red Greek-key hand lettering | **Different face and accent colour.** Note: our draft theme already uses rust `#b8472a`, which is UF's accent. Pick a new accent and display font before building v3 (William approves, gate G2); suggestion to test: ink-blue or verdigris with a gold stamp colour, and a free-for-commercial-use hand-lettered face from Google Fonts. The spike labels use rust only because they reuse the draft theme |
| "THE END OF" / "10 YEARS" plain-white typed cards, parchment-scroll moral card | Our cards are the case board, stamps and source chips; no scroll |
| Title family "The ENTIRE Story of ___ Explained"; "IN 13 MINUTES" label | Own title formula: a story promise plus the real-world check (e.g. "The Cyclops Story, and Which Parts Were Real"); no minutes tag |
| Thumbnails: two or three characters facing off over a map or setting with big title | Own layout built from our cast and the case-board motif; reviewed against UF's last 24 thumbnails before use |
| Jokes and lines (the "Nobody" exchange as they play it, "Yeah, the meat mooed") | Scripts written from primary sources (Butler's Book 9, Hesiod, Mayor, etc.); jokes are ours; the Nobody punchline is Homer's, not UF's phrasing |
| No sources cited | We cite by chip and phrase; accuracy and sources are the series promise (`PLAN.md`) |
| Music-free, no hedging | We hedge, compressed into stamps and short verdict lines |
| Painterly backgrounds that look AI-made | We keep plates flat-ink and consistent with sprites; we use no UF frame, map or plate as a reference image |

Also: each episode needs its own story (YouTube inauthentic-content policy, `REF-unknown-frequencies.md`); do not reuse UF's episode order or structure beyond the recipe.

---

## 10. Per-episode production workflow, owners and gates

Agent roles are subagent or session roles, not people. William appears only at the five gates.

| Step | Output (in `videoN/`) | Owner | Done when |
|---|---|---|---|
| 0. Topic and angle | 3 options with a story promise and a real-world twist | **Researcher** + **Producer** | **G0, William picks one** |
| 1. Research and fact table | `FACTS.md`: claims, sources, verdicts, quote-verbatim list | **Researcher** | Every claim has a source and a verdict word |
| 2. Script | `SCRIPT.md` in the beat format (`RECIPE-SCRIPT.md`), speaker tags, 1,700-1,800 words | **Scriptwriter** | `metrics.py` within the section 1 targets |
| 3. Accuracy pass | `ACCURACY.md`: each factual line checked, dramatised dialogue flagged | **Fact-checker** (separate agent from the writer) | Zero unresolved lines |
| **Gate G1** | Script plus accuracy report | **Producer** | **William approves the script** (reads it; hears a 60-90 s sample if asked) |
| 4. Casting and voice | Voice per speaker, 3 takes of one paragraph each; final takes; word timestamps (`words.json`) | **Voice director** | Pace, pause and loudness targets met on the raw VO |
| 5. Storyboard | `storyboard.json` (section 11): shot, class, plate or sprite, events anchored to word indices, SFX | **Storyboarder** | Class shares within section 3; density rules pass on the *plan* before any art |
| 6. Asset list and budget | Plate prompts (about 44), sprite and pose list, map bases, call plan and cost estimate | **Art director** | Within the call cap; reuse maximised |
| **Gate G2** | New characters only: master pose, accent colour and font (first episode), voice cast | **Producer** | **William approves masters, voices and the look** |
| 7. Assets | Plates, sprites, cutouts, `cast.json`, contact sheets, reject log | **Art director** | Attribute checks pass; spend logged |
| 8. Assemble | Resolve storyboard to `timeline.json`; render the animatic at half resolution; mix audio in full ffmpeg; mux | **Assembler** | Animatic plays through; `--frames` stills for every class checked |
| **Gate G3** | Animatic (540p) plus 8 stills plus the QA numbers so far | **Producer** | **William reviews the animatic** before the final render |
| 9. Final render and QA | Final 1080p mp4; `QA-REPORT.md` against section 8 | **Assembler**, then **Editor** (independent measurement) | Every item in section 8 passes or has a recorded exception |
| 10. Packaging | Title, description with sources and chapters, SRT, 3 thumbnails, pinned comment | **Publisher** | Section 8 packaging items pass |
| **Gate G4** | Private upload link plus QA report plus thumbnail pick | **Producer** | **William watches and approves** |
| 11. Publish and log | Schedule or publish after G4; cost, render time and call counts appended to the CSV log | **Publisher** | Public link verified; nothing published without G4 |

Standing rules: no spend above the pre-agreed cap without William; no upload at all before G4; a change to script, voice or timing re-runs steps 5, 8, 9 only (retiming is one command, measured in the spike); art is regenerated only for shots whose content changed.

Estimated agent effort per episode once the system exists [E]: research and script about 1 day, storyboard half a day, assets about 1 day of calls and checks, assembly and QA about half a day. Render time about 6 min for the final (spike extrapolation, TOOLING-EVAL section 3) [E].

---

## 11. Appendix: tool-agnostic storyboard record

One JSON record per beat or event; every time is an index into `words.json`, converted to seconds at build time. The spike's `video2/spike/common/storyboard.json` is the working example.

```json
{
  "fps": 30,
  "shots": [
    {"id": "s1_map", "class": "D", "start": {"word": 0}, "bg": {"type": "map", "src": "map_med.png"}},
    {"id": "s2_white", "class": "B", "start": {"word": 11, "off": -0.05}, "bg": {"type": "white"}}
  ],
  "events": [
    {"shot": "s1_map", "kind": "route", "at": {"word": 7}, "dur": 1.0, "from": [16.1, 40.2], "via": [15.9, 38.2], "to": [14.2, 37.6]},
    {"shot": "s2_white", "kind": "sprite", "at": {"word": 12}, "src": "elephant__neutral__a.png", "x": 640, "y": 960, "h": 420},
    {"shot": "s2_white", "kind": "label", "at": {"word": 16}, "text": "UNDER 1 m", "style": "impact", "x": 960, "y": 180},
    {"shot": "s4_count", "kind": "counter", "at": {"word": 34}, "dur": 0.95, "from": 1900, "to": 1914},
    {"shot": "s3_paint", "kind": "chip", "at": {"word": 40}, "text": "MAYOR, 2000", "corner": "bottom-left", "dur": 2.5},
    {"shot": "s3_paint", "kind": "stamp", "at": {"word": 52}, "text": "UNPROVEN"}
  ]
}
```

Event kinds: `sprite`, `label`, `counter`, `route`, `chip`, `stamp`, `bubble`, `swap` (pose change on an existing sprite), `sfx`. Any renderer that implements these kinds can build the format. The spike implements four (`sprite`, `label`, `counter`, `route`) in two renderers; `chip`, `stamp`, `bubble`, `swap` and `sfx` follow the same pattern but are untested [U].
