# BRIEF-SLICE: Norse test slice (S01-S20, first 2:35), plates via Gemini, scripted

Worker: Sonnet, context cap 100k. View contact sheets only, never every plate. Do not read session history. Write only inside `projects/bluepill/norse/scenes/slice/` (create it) plus tools in `norse/scenes/`. Never modify the Greek `video2/` or `library/` (copy what you need). Spend: Gemini cap $2.40 for this run (est. $1.61, 25% re-roll allowance). `GEMINI_API_KEY` is in the environment. On quota errors wait a minute and retry (auto-refill is on).

## Read
- `norse/scenes/TEST-SLICE.md` (the 20 scenes, calls), `norse/scenes/scene_plan.json`, `norse/scenes/state.json`, `norse/scenes/CONTINUITY.md`, `norse/library/cards.json`, `norse/library/refs/*__card.png`, place masters in `norse/library/places/`.
- Video 1's production template, to copy not edit: `video2/scenes/full/g2.py` (Gemini caller, per-call SPEND log, resumable), `mkjobs.py`, `cards.py`, `defs.py`, `comps.py`, `audit_build.py`, `build_cuts.py`; `PROCESS.md` Stage 6 and 7; `refs/RECIPE-2026-11-13.md` section 7 (F1 edit framing).

## Production template (Stage 6, binding)
1. Image 1 = the place plate (library master or derived variant). Then ONE labelled card per character PRESENT in that scene, using the exact card id from `state.json` (rule 21: never infer a variant from the shot line; shot-line cloak colours that contradict the card lose to the card). No cast sheet, no absent characters, no bare turnarounds.
2. Prompt = scene state line + shot line (patch the Odin "eye" wording to the black eye patch) + the identity lines copied verbatim from each card + the identity checklist repeated at the end + the scale line. Unnamed silhouettes and props that have no card are prompt text only.
3. ONE candidate per base plate; TWO only for the hero shot (S01). Variants: "edit image 1, change only X". The 4 dwarfs (S12): composite from the cream row for the exact count; Vili/Ve/Odin brothers: use the vili_ve and odin_one_eye cards.
4. Library-only and crop scenes (0 calls) just copy the library plate into the slice folder.
5. Resumable job files per chapter; `manifest.json` with scene id, plate path, card ids used, prompt, call id.

## Audit gate (Stage 7), cost-aware
- Build a first-pass automated audit with Gemini vision (billed separately, about $0.50 for the whole video): for each plate, give the plate, the cards of the characters present, the beat text, previous/next beat text, and the scale line; ask for the identity checklist (patch on Odin, Vili purple cloak, Ymir huge, etc.), count of figures, continuity (location, time of day, who is present), and scale. Output JSON per plate with PASS/FAIL per check and the reason.
- Then YOU view only the contact sheet(s), the hero plate, the composite, and every plate the automated pass flagged. Re-roll flagged plates with state-injected prompts, max 2 rounds, within the cap. Record the audit's agreement with your own eyes on the plates you viewed (this calibrates the cheap audit for the full run).

## Review artefacts for William
- `scenes/slice/CONTACT-SLICE.jpg`: every scene's plate in order, labelled with scene id and beat ids, 4 across, about 2400 px wide.
- `scenes/slice/SLICE-REPORT.md`: calls and dollars from the spend log vs estimate, re-rolls, audit result (flags and how the cheap audit compared), the first things William should look at (S01 hook, Odin patch at S04/S20, Ymir scale at S07/S08, the 7-figure scene at S12, Ask and Embla at S14).
- A rough 2:35 animatic is NOT required. If `video2/remotion-v3/` tooling runs unchanged with path changes in under 10 minutes of work and zero model calls, build `out/norse_slice_540p.mp4` using `audio-n/narration_voice_only.mp3` cut to 0-155 s with push-ins every 4th beat; otherwise skip it and say so.

## Final message (max 10 lines)
Calls and dollars, plates passing the audit, re-rolls, the plates William should look at first, whether the animatic was built, and open issues.
