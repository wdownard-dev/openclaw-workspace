# PROCESS.md: The Myth Ledger video pipeline, topic to published (locked 2026-11-14 after video 1; revised 2026-11-14 after the process audit)

Canonical process reference. Written after video 1 ("The ENTIRE Story of the Cyclops in 10 Minutes", w5GKoqjc-n0, public 2026-11-14). Mirrored on the Miro board "Myth Ledger: video process". When the process changes, change this file first, then the board.

Legend: GATE = William decides before the next stage starts. $ = real spend. Paths are under `projects/bluepill/` unless absolute.

Model rule: tooling, scripting, generation and audit workers run on Sonnet (`claude-cli/claude-sonnet-5-5`). Judgment lanes (script review, look review, recipe writing) go to Fable only when William asks. Spawn workers with the model pinned. No worker runs past 150k context without William approving it first; split the job instead.

Lock order (audit 2026-11-14): references → script → fact-check → library → narration → plates. Narration is the LAST thing recorded before plates, after the library audit has patched every shot line, so re-records disappear. Auto-refill is on for OpenAI, Gemini and ElevenLabs, so there is no balance check stage.

---

## Stage 0. Standing setup (done once, reused every video)

| Item | Where / value |
|---|---|
| Channel | The Myth Ledger, @themythledgerofficial, channel id UCNSflpCKmwHr4bLpNTCbBqQ (separate Google account from wrdclipz) |
| Upload auth | secret `GOOGLE_OAUTH_REFRESH_TOKEN_MYTHLEDGER` (client morpheus-yt). Never `GOOGLE_OAUTH_REFRESH_TOKEN` (that is wrdclipz). OPEN ACTION before video 2 publish: re-auth once with `youtube.upload` + `youtube.force-ssl` so publish and schedule happen from chat, not a Studio click |
| Image models | Gemini 3.1 Flash Image (`GEMINI_API_KEY`, production plates, ~$0.07/img). OpenAI gpt-image-2.6 (`OPENAI_API_KEY`, library sheets and edits, ~$0.04/img) |
| Voice | ElevenLabs (`ELEVENLABS_API_KEY`, Creator plan). Narrator Daniel (premade), eleven_multilingual_v2, stability 0.5, similarity 0.75, style 0.2, speed 1.0. LOCKED: no auditions unless a video needs a voice Daniel cannot do |
| Edit | Remotion in `video2/remotion-v3/` (free licence for teams up to 3). ffmpeg at `openclaw-sites/bin` |
| Library | `library/` (characters, places, props, refs). LOCKED per `library/LOCKED.md`; additions in new folders, must pass AUDIT-LOCK checks A-F |
| Brand | `brand/` avatar_800.png, banner_2560x1440.jpg |
| Reference tool | `~/.openclaw/workspace/scripts/refwatch/watch.py` (venv `~/.venvs/refwatch`), skill `reference-watch` |
| Recipe docs | `refs/RECIPE-2026-11-13.md` (format recipe, sections 4, 6, 7), `video2/RECIPE-SCRIPT.md` (script grammar), `video2/FORMAT-BIBLE.md` |

---

## Stage 1. Topic and angle

1. Outlier check of the lane: `outlier_search.py` (YouTube Data API, views vs subscribers), results in `OUTLIER-CHECK.md`. Compilation and "ENTIRE story / every X explained" formats beat single-subject "who was".
2. Guardrails: public-domain subjects (myth, folklore, pre-1930 literature), cite the source tradition per claim, stylised violence, no living people, distinct research and twist per video (YouTube inauthentic-content policy).
3. Optional: William sends 3-5 reference videos that grabbed him. Run refwatch on each (`watch.py <url>` → `refs/<id>/METRICS.json`, shot sheets, palette) and update the recipe if the numbers move.
4. Output: one line, "topic + angle" (video 1: "The Cyclops: the whole Odyssey Book 9 story told straight, then where the giant came from").

**GATE 1: William approves topic + angle.**

---

## Stage 2. Script

Shape (calm lane, Genius History style; `refs/RECIPE-2026-11-13.md` section 4):
- Straight chronological story, 6-8 named chapters, origin/"where did it come from" material as the closing chapter, not as evidence apparatus mid-story.
- 1,450-1,650 words for 9:30-10:00 at 150 wpm. Mean 10-12 words per sentence, 12-14 sentences a minute, 0.3-0.5 questions a minute.
- Hook (first 30 s): bold claim with a number, two or three escalating facts, a collapse line, then the question the video answers.
- Every beat (sentence) carries a SHOT LINE and a SCENE STATE line: location, time of day, door sealed/open, who is present and how many, action direction. State carries forward and changes only when the narration changes it. Describe only who is present; never the full cast.
- Unfilmable shot lines are script bugs (sky through a sealed door, wrong head-count). Fix them in the script, not in the prompt.

Steps:
1. Sonnet writes `video2/SCRIPT-V<n>.md` + NOTES (drafts kept as draft1, draft2...).
2. Review pass (judgment lane): cut commentary beats, fix lines, check chapter rhythm. Video 1: 1,466 words, 115 sentences, 176 beats, 7 chapters.
3. Fact-check pass on every "(ours)" line against the sources → `video2/FACTCHECK-V<n>.md` with PASS / FIX / CUT per beat. FIX lines are rewritten in the script now, before anything is recorded. Video 1: 169 PASS, 7 FIX, 0 CUT.

**GATE 2: William reads the fact-checked script ("script is fine, move on").**

---

## Stage 3. Picture library (characters, places, props)

Only for new entities; the locked library carries over. ONE round: the worker gets the full checklist below up front and delivers everything in a single pass (video 1 took three rounds and $8.30; one round with the checklist is about $4).
1. Wardrobe options: 2-3 themed option sheets (`library/options-<date>/`) → William picks or mixes.
2. Model sheet per character on plain cream: front and three-quarter turnaround, one face close-up, wardrobe pieces broken out. Back view only as a separate sheet when the script has back shots. No expression rows, no silhouette sheet, no unused variants (helmet etc). Keep designs bold: beard-size features vanish in wide shots.
3. Places and props: ONE master per place/prop; every variant (dusk, night, door sealed, boulder aside) is DERIVED by edit from the master, never regenerated. Verify with an edge-correlation check (0.6-0.75 is a pass; pixel diff is useless under lighting change).
4. `cast_check.py` → `library/CAST-CHECK.md`: every entity named in any shot line maps to a folder. 0 MISSING is the bar.
5. Contradiction audit A-F → `library/AUDIT-LOCK.md` (crew style, helmet variants, boulder side, face vs body colour, band on blinded heads, etc.). Fix blockers, mark non-canonical variants NOT USED, patch script shot lines that contradict the library. These patches land BEFORE narration.
6. One labelled CARD per character (`library/refs/`), simplified spec: title, ONE identity line of at most 5-6 bold tells (e.g. laurel, blue tunic, red cloak one shoulder, no beard, dot eyes), front + three-quarter turnaround, one face close-up. No expressions, no back view, no details the plates never show (sandals, sword, gold hem). One card per crew variant, or one canonical crewman with B/C described in text only when a line names them. Scale note on every animal and prop card (sheep 0.35, ram 0.4, boulder 3x). Cards, not bare turnarounds, are what every generation call and every thumbnail uses. Smaller cards also mean fewer input tokens per Gemini call.
7. Write `library/LOCKED.md`.

**GATE 3: William says "locked". After that, nothing in `library/` changes without an explicit unlock (unlocks are logged in LOCKED.md).**

No rebuild of the video 1 cards (William, 2026-11-14: video 1 is done and posted). The simplified spec applies to new cards only; reuse a video 1 card as-is if a later video needs that character.

---

## Stage 4. Narration (last step before plates)

1. Voice is locked: Daniel reads everything, narration and character lines, no v4 tags (method A2; characters are told apart by picture and delivery). No auditions. Designed character voices, dialogue mode and processing were tested in video 1 and rejected.
2. Record only after fact-check FIXes and library shot-line patches are in the script, so the read is final. Record in scene-length passages with `/with-timestamps` → `video2/audio-v<n>/` (`narration_voice_only.wav`, `words.json`, `beats_timing.json`, `quality.json`, `SPOKEN-TEXT.md`). About 7,800 chars per 10-minute video.
3. `assemble.py` caps inside-beat pauses (0.35 / 0.25 / 0.20 s) so the read does not drag; target 150-155 wpm, 9:30 for a 10-minute title. Voice-only master at -19 LUFS, 0 artefacts.
4. Names the model mangles: use unhyphenated respellings (no phoneme tags on multilingual_v2). Watch for "B.C.." double stops.
5. A re-record after this point is a process failure; log why in `video<n>/NOTES.md`.

**GATE 4: William listens (MP3 in chat).**

---

## Stage 5. Scene plan and state ledger

1. `video2/scenes/scene_plan.json` + `SCENE-PLAN.md`: about 70 scenes per 10 minutes (7-8 cuts a minute). One base plate per scene held 4-20 s; every change inside a scene is a camera move (push_in, pull_out, pan, crop_close) or ONE derived variant ("edit image 1, change only ...").
2. Variant chaining: object additions chain forward; pose and expression variants derive from the BASE so drift cannot accumulate. Plates rendered 1.5x overscan so pulls and pans have room.
3. Scale line on every scene: Odysseus 1.0, crew 0.95, Polyphemus 4.0, neighbour giants 3.0, sheep 0.35, boulder 3x. Scale wrong = audit fail.
4. `state.json` from the script (location, time, door, cast with an explicit card id per character and variant, count, direction per beat; rule 21); `cards.json` only if any text cards survive (video 1: none; cards land on the subject, never on a chapter boundary).
5. Crowds above 5 cannot be counted by the model: plan exact-count crowd beats as COMPOSITES (figures cut from a cream row, placed on the plate).

Rule: build and show a TEST SLICE (first 2:30, ~22 scenes) before the full run.

---

## Stage 6. Plate generation

Production template (Gemini 3.1 Flash Image, "F1 edit framing"):
1. Image 1 = the place plate (library master or derived variant). Then one labelled card per character PRESENT in the beat. No cast sheet, no absent characters, no bare turnarounds.
2. Prompt = scene state line + shot line + identity lines copied verbatim from each card + the identity checklist repeated at the end.
3. ONE candidate per base plate by default; a failed plate is re-rolled in the audit loop. Two candidates only for hero shots (flagged `hero: true` in the scene plan) and thumbnails. Variants: "edit image 1, change only X". Crowds: composite from a cream row for exact counts.
4. Per-chapter job files (`scenes/full/jobs_bases_ch<n>.json`), `manifest.json`, resumable; cap set per run (video 1: $25 cap, spent $9.91 for 46 bases x2 + 40 variants + composites + 11 cards; single candidates should bring the base run near $6).
5. Close-ups of a big character go painterly: edit the character turnaround as the base instead of the place plate. Complex actions: split into two plates.

---

## Stage 7. Audit gate (render gate, no exceptions)

`scenes/full/audit_build.py` → `audit.json`, `AUDIT.md`. For every plate, viewed at full size next to its line, the previous line and the next line:
- Identity checklist per present character (one eye, laurel, red cloak, cloth band after the blinding, crew hair/tunic, etc.). Video 1: 421/433 checks passed on first full audit.
- Continuity: location, door state, cast, count, direction, time of day, action must not contradict the next line.
- Scale against the scene's scale line.
- Zero fails per chapter before the next chapter generates. Re-roll with state-injected prompts, max 2 rounds, then fix by hand (composite or manual edit). Video 1 continuity history: 104 → 15 → 1 → 0 fails.

---

## Stage 8. Edit (Remotion)

1. `scenes/full/build_cuts.py` → `cuts.json` (plate, in/out, move) from `beats_timing.json` + scene plan. `cut.py` renders.
2. Rules: hard cuts only; push-in on every 4th beat; no chapter bands, no text cards, no stamps or chips (William: cards are non-value). Pans on about 1 in 4 shots at most.
3. Render `out/v<n>_540p.mp4` + contact sheets (`v<n>_sheet_a/b/c.jpg`, `v<n>_stills.jpg`) → William reviews with notes by beat number.
4. Fix pass (new jobs file, cap ~$6) → `FIXES.md` → `v<n+1>_540p.mp4`. Video 1: v7 → notes → v8 (17/19 groups clean) → visual fact fixes → v9.
5. Final render 1080p (`v9_1080p_final.mp4`, ~137 MB for 9:30). Check soft crops (>3.7x zoom is visible at 1080).

**GATE 5: William's beat notes on the 540p cut; "approved" before the 1080p render.**

---

## Stage 9. Audio mix

`video2/audio-mix/`: narration + 2-4 synthesised stingers (no music bed) + light SFX; loudnorm to -16 LUFS; no third-party audio at all (no licence exposure). `MIX-REPORT.md`, `CREDITS.md`. Output `final_mix.wav/.m4a`, muxed into the final render.

---

## Stage 10. Packaging

`video2/packaging/PACKAGING.md`:
1. Five titles under 60 chars; default idiom "The ENTIRE Story of X in N Minutes" (N honest to runtime). William picks one.
2. Thumbnail 1280x720 by the CARD METHOD: Gemini, library cards + identity lines as references, 2 candidates, then title text applied with Pillow (Permanent Marker). Title inside the thumbnail (mobile truncation), "in N minutes" bottom-right, characters large. Never bare turnarounds. `gen_thumbs.py`, `text_thumbs.py`.
3. Description: two-line hook above the fold, chapters list, sources list (author + work; only verified links), one-line channel tagline.
4. Chapters: from `beats_timing.json`, then RE-TIMED against the final render (voice-only times drift).
5. 15-20 tags. Category 27 (Education). Not made for kids. No AI label needed for non-realistic animation.

**GATE 6: William picks title + thumbnail.**

---

## Stage 11. Upload and publish

1. `pipeline/yt_upload_ml.py <file> --title ... --desc-file ... --thumb ... --tags ... --privacy private` using the Myth Ledger refresh token. Writes `packaging/UPLOAD.json` (video id, URL, settings).
2. Private first, always. William reviews on YouTube.
3. Publish: once the token carries `youtube.force-ssl`, set Public or Schedule from chat via the API and confirm with a launch-check automation 10 minutes after the scheduled time. Until the re-auth is done, William sets it in Studio.
4. OPEN ACTION (one time, William's Google consent screen): re-auth the Myth Ledger OAuth with `youtube.upload` + `youtube.force-ssl` and store the new value in `GOOGLE_OAUTH_REFRESH_TOKEN_MYTHLEDGER`.

**GATE 7: William says public / schedule time.**

---

## Stage 12. Track and learn

- Log per video: cost by lane, hours, views at 24h / 7d, AVD, CTR, subs (CSV, like `projects/opusclip/experiment-log.csv`).
- Video 1 spend (production run only): Gemini plates $9.91 + fix pass $4.79 + thumbnails ~$0.20; library $8.30; narration ~7,800 chars Daniel. Experiments before the pipeline settled: ~$55 OpenAI.
- Fold lessons into this file and `refs/RECIPE-2026-11-13.md`; the next video starts at Stage 1 with the library already locked.

---

## Lessons that are now rules (video 1)

1. No cast sheet as an image reference (the model copies the line-up). Cards + identity lines only, one card per present character.
2. State ledger before any plate; the sentence-match audit is a render gate; zero fails before William sees a cut.
3. One master per place/prop; variants by edit; never regenerate a place.
4. Scene layer, not a plate per sentence: 7-8 cuts a minute, hold scenes, incremental edits, push-ins. A new plate every sentence reads as strobe.
5. Explicit scale per scene; scale drift is a fail.
6. Crowds above 5: composite. Bold character features only. Close-ups from the character turnaround, not the place plate.
7. Gemini Flash holds the card designs; OpenAI edits drift realistic on hard shots.
8. No text cards, bands, stamps or chips in the cut.
9. Test slice (2:30) before any full run; 540p cut with sheets before 1080p.
10. Pin worker models; Sonnet for tooling, Fable only for judgment on request.
11. Thumbnails and channel art use the same card method as plates.
12. Private upload first; status flips in Studio until the OAuth scope is widened.

## Audit decisions (2026-11-14, all approved by William)

13. Lock order is references → script → fact-check → library → narration → plates. Narration is recorded once, last.
14. Library is one round with the full checklist up front; new entities only.
15. One candidate per base plate; two only for hero shots and thumbnails.
16. Daniel is the voice. No auditions.
17. Simplified card spec (Stage 3 step 6) for new cards only; video 1 cards are NOT rebuilt.
18. No worker over 150k context without approval; Sonnet for every tooling lane.
19. Re-auth the upload token with force-ssl once, so publishing leaves Studio.
20. Dropped: Stage 0 balance check (auto-refill is on everywhere).
21. (2026-11-14, William) Variant characters get one card per variant, and plate generation must be told EXACTLY which card to pull. The script's `state:` line names the variant (e.g. "Tyr (hand)", "Tyr (stump)"); the state ledger (`state.json`) stores a card id per present character per beat; the prompt builder reads that card id and never infers a variant from the shot line. Audit checks the card named against the plate. Applies to every variant (wounded, disguised, aged, before/after).
22. (PROPOSED 2026-11-14, William's idea; confirm before first use) Milestone scenes (hero:true and any complex action: bracing, grappling, scale contrasts) get a LAYOUT first: blocking built in code from the locked cards (figures cut from the card turnarounds, placed and scaled on the place master, proportions fixed by us), then Gemini repaints it with 'edit image 1: keep composition, pose and proportions, repaint in the house style'. Reason: Norse N-092 Thor's legs vs body proportion was wrong when Gemini was left to invent the pose.

## Lessons from video 2, Norse (2026-11-15)

23. Hook before body: write and pick the hook (8 options, scored against VOICE.md, William picks) BEFORE the script is fact-checked or locked. Norse's hook was rewritten after the lock because outside feedback arrived late.
24. Check the title's promise against the script at Gate 2. "ENTIRE" did not match a spine-only Norse script; it was caught after narration and cost a patch and a re-record. Gate 2 now includes "does the script deliver the title?" and a list of what it skips (feeds the part-2 promise, PROMISES.md).
25. Workers cannot be steered mid-run (sessions_send steer is unsupported). If the brief changes, cancel and respawn immediately.
26. Image model content filter: bound or tortured figures (Loki bound, venom) and edits of them get PROHIBITED_CONTENT. Plan two-step builds (clean base, then edit), keep violence stylised, budget for code-drawn patches.
27. Cheap Gemini audit is a first pass only: strict scale prompt, results can flip on re-run; Claude still views hero shots, composites and flagged plates.
28. Renders: launch long Remotion/ffmpeg jobs as background processes from the start; two foreground launches stalled.
29. Keep each worker brief file-based and one worker per stage; the whole pipeline from library to private upload cost about 3% of the weekly plan (38% to 41%) and about $13 of image/voice spend.
