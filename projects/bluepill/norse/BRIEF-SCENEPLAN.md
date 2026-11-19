# BRIEF-SCENEPLAN: Norse scene plan and state ledger (Stage 5; planning only, no images, no spend)

Worker: Sonnet, context cap 100k. Do not read session history. Write only inside `projects/bluepill/norse/scenes/` (create it). Do not modify anything else.

## Read
- `norse/STATE-2026-11-14.md` (where everything is), `PROCESS.md` Stages 5 to 7 and rule 21, `refs/RECIPE-2026-11-13.md` section 7 (production recipe).
- Video 1's results as the model: `video2/scenes/scene_plan.json` (schema), `video2/scenes/SCENE-PLAN.md`, `video2/scenes/full/defs.py`, `video2/scenes/full/audit_build.py`, `video2/scenes/full/build_cuts.py` (reuse their data formats so the same tools run on Norse with path changes).
- Inputs: `norse/SCRIPT-N-LOCKED.md` (177 beats; shot/state/trace lines), `norse/audio-n/beats_timing.json` (start/end seconds per beat), `norse/library/cards.json`, `norse/library/WARDROBE.md` (scale line, variants, 17 place masters and their variants), `norse/library/CAST-CHECK.md`.

## Deliver
1. `scenes/scene_plan.json` + `scenes/SCENE-PLAN.md`: group the 177 beats into about 72 scenes (7-8 cuts a minute over 10:17). One base plate per scene, held 4-20 s; every change inside a scene is a camera move (push_in, pull_out, pan, crop_close) or ONE derived variant ("edit image 1, change only ..."). Per scene: id, beats, start/end seconds from `beats_timing.json`, place master/variant (from the library), characters present BY CARD ID (rule 21; use `cards.json` and the `state:` names), variant changes, camera moves (push-in on every 4th beat, pans on at most 1 in 4 shots), hero flag (hero:true only for about 6 shots: the hook's skull sky, Tyr's hand, Mjolnir/serpent, Baldr falls, Odin and Fenrir, the final tree), scale line (Odin 1.0, giants 3.0-4.0, dwarfs 0.5, Fenrir by stage, Jormungandr, etc. from WARDROBE.md), and a one-line prompt-ready shot description.
2. `scenes/state.json`: per beat, `{place, time_of_day, cast:[card_ids], count, direction}` from the script's state lines, with the exact card id per character (e.g. `tyr_hand`, `tyr_stump`, `odin_one_eye`, `odin_armed`, `thor_disguise`, `fenrir_bound_sword`). Flag any beat whose state lines contradict the next beat (continuity) and fix in the ledger, not the prompt. Report script bugs; do NOT change the script.
3. Crowd beats above 5 figures (frost giants drowning, the gods arming, the einherjar, the army at Ragnarok): list them as COMPOSITE scenes with exact counts, or as tiny figures in the distance, per PROCESS rule on crowds.
4. `scenes/TEST-SLICE.md`: the first ~2:30 as the test slice (about 22 scenes): list the scene ids, which bases and variants it needs, estimated Gemini calls (1 candidate per base; 2 for hero shots) and dollars (~$0.07 per image).
5. `scenes/COST-ESTIMATE.md`: full run estimate: bases, variants, composites, hero doubles, the plate count and dollars at ~$0.07 per Gemini image; and the audit's size (number of plates William/Claude would have to view) plus a proposal to cut Claude's vision cost (first-pass audit by a cheaper automated check with Gemini vision; Claude reviews only flagged plates).
6. Hook rule: the first five scenes (cold open to N-015) must be the most visual plates in the video; check that every hook beat has a distinct plate or camera move so there is no static 25 seconds.

## Final message (max 10 lines)
Scene count, cuts per minute, hero shots, composite scenes, slice scene ids and estimated slice cost, full-run estimate, continuity problems found, and open questions.
