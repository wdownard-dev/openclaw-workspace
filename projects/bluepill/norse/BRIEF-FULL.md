# BRIEF-FULL: Norse full plate run, one HALF per worker (two workers run in parallel). Real Gemini spend.

You are ONE of two workers. Your half is given in the task text: HALF A = scenes S21-S50 (beats N-048..N-123), HALF B = scenes S51-S81 (beats N-124..N-178). Sonnet, context cap 100k: view contact sheets and flagged plates only, never every plate. Do not read session history. Write only inside `projects/bluepill/norse/scenes/full/` (create; use subfolders `halfA/` or `halfB/` for your jobs, manifest, candidates and spend log so you do not collide with the other worker; shared `img/` is fine because filenames are per scene id). Never modify `video2/`, `library/`, or `norse/library/` (read-only; LOCKED). Spend cap for YOUR half: Gemini $5.00 (estimate A about $3.6, B about $3.9 with heroes). `GEMINI_API_KEY` is in the environment. On quota errors wait a minute and retry.

## Reuse the slice tooling (it worked: 27/27 after one round)
Copy and adapt the slice builder, caller, prompt builder, and Gemini audit in `norse/scenes/slice/` (and `norse/scenes/*.py`); they already implement PROCESS Stage 6 and the first-pass audit. Read `norse/scenes/slice/SLICE-REPORT.md` first for lessons.

## Production rules (binding)
1. Plate = place master/variant (`norse/library/places/...`) as image 1, then ONE labelled card per character PRESENT, with the exact card id from `norse/scenes/state.json` (rule 21; the card wins over any shot-line colour). No absent characters, no cast sheet, no bare turnarounds. Silhouettes and cardless props (cave serpent, grey horse, sun wolves, frost-giant crowd, oath objects, unnamed teaser silhouettes) are prompt text.
2. Prompt = scene state line + shot line + identity lines verbatim + the identity checklist repeated + the scale line from `scene_plan.json`. Odin has a black eye patch (never "empty socket"). Mjolnir returns to Thor's hand from N-101.
3. ONE candidate per base; TWO only for the six hero shots in your half (hero:true). Variants: "edit image 1, change only X". Crowds and exact counts: composites from a cream row (N-108 oath objects: composite; N-136 winter triptych: cut in code, no call).
4. Library-only and crop scenes cost nothing (copy/crop).
5. Per-chapter job files, resumable, `manifest.json`.

## Audit gate (render gate, zero fails before you report)
- Rule-based first: card id in state vs card used in the job (mechanical), plate size, crops inside the plate.
- Gemini vision first pass on every plate in your half: plate + the cards present + state/shot/prev/next beat text + scale line. Checks: identity features per character (patch on Odin, Tyr hand vs stump, Hod's bandage, Vili purple, etc.), exact figure count, continuity (place, time of day, who is present), scale. MAKE THE SCALE CHECK STRICT (the slice audit missed a too-small Odin): give the model the scale ratios and ask for the visible height ratio of each character against Odin.
- You view: the contact sheets of your half, every hero plate, every composite, every flagged plate. Re-roll flagged plates with state-injected prompts, max 2 rounds, within the cap; then fix by hand (composite or manual edit) or mark UNRESOLVED. Chapter order: finish and clear one chapter before the next.
- Known ledger issue: `state.json` N-038 lists the brothers in `state_names` but not `cast` (fix in the ledger; not in your half unless it applies). Cheap-audit false flag source: ledger mismatches; fix the ledger, never the script, and list every ledger fix.

## Deliver
- `scenes/full/img/` plates named per scene (S21_base.png, S21_v1.png...), `scenes/full/halfX/manifest.json`, `scenes/full/halfX/audit.json`, `AUDIT-halfX.md` (per plate PASS/FAIL, re-rolls, unresolved), `CONTACT-halfX_a/b/c.jpg` (labelled with scene id and beat ids, 4 across, 2400 px wide).
- `scenes/full/halfX/REPORT.md`: calls and dollars from the spend log vs estimate, re-rolls, unresolved plates and why, agreement between the cheap audit and your eyes, and the plates William should look at first.

## Final message (max 10 lines)
Half, calls and dollars, plates, audit result (fails remaining), re-rolls, unresolved plates, plates to look at first, ledger fixes, open issues.
