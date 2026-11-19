# Character style exploration, image call log (2026-11-12)
Hard cap 40 generations. Costs are estimates (0.034 per sunburst image, 0.041 gpt-image-2, +0.007 per reference image); OpenAI dashboard lags.

| # | id | model | size/quality | type | prompt file | est cost | status | time |
|---|----|-------|--------------|------|-------------|----------|--------|------|
| 1 | odysseus_A | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus.png | odysseus_A.txt | ~$0.041 | ok | 28s |
| 4 | odysseus_D | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus.png | odysseus_D.txt | ~$0.041 | ok | 24s |
| 3 | odysseus_C | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus.png | odysseus_C.txt | ~$0.041 | ok | 27s |
| 2 | odysseus_B | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus.png | odysseus_B.txt | ~$0.041 | ok | 29s |
| 5 | cyclops_A | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_A.png | cyclops_A.txt | ~$0.041 | ok | 31s |
| 7 | cyclops_C | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_C.png | cyclops_C.txt | ~$0.041 | ok | 31s |
| 6 | cyclops_B | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_B.png | cyclops_B.txt | ~$0.041 | ok | 32s |
| 8 | cyclops_D | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_D.png | cyclops_D.txt | ~$0.041 | ok | 35s |
| 9 | crew_A | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_A.png | crew_A.txt | ~$0.041 | ok | 25s |
| 12 | crew_D | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_D.png | crew_D.txt | ~$0.041 | ok | 27s |
| 10 | crew_B | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_B.png | crew_B.txt | ~$0.041 | ok | 29s |
| 11 | crew_C | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_C.png | crew_C.txt | ~$0.041 | ok | 29s |
| 13 | sheep_A | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_A.png | sheep_A.txt | ~$0.041 | ok | 27s |
| 15 | sheep_C | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_C.png | sheep_C.txt | ~$0.041 | ok | 31s |
| 14 | sheep_B | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_B.png | sheep_B.txt | ~$0.041 | ok | 33s |
| 16 | sheep_D | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_D.png | sheep_D.txt | ~$0.041 | ok | 35s |
| 17 | poseidon_A | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_A.png | poseidon_A.txt | ~$0.041 | ok | 29s |
| 18 | poseidon_B | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_B.png | poseidon_B.txt | ~$0.041 | ok | 30s |
| 19 | poseidon_C | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_C.png | poseidon_C.txt | ~$0.041 | ok | 31s |
| 20 | poseidon_D | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_D.png | poseidon_D.txt | ~$0.041 | ok | 32s |
| 21 | sheep_D2 | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_D.png | sheep_D2.txt | ~$0.041 | ok | 28s |
| 22 | cyclops_D2 | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_D.png | cyclops_D2.txt | ~$0.041 | ok | 35s |
| 24 | pose_ody_A | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_A.png | pose_ody_A.txt | ~$0.041 | ok | 27s |
| 26 | pose_ody_D | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_D.png | pose_ody_D.txt | ~$0.041 | ok | 29s |
| 23 | pose_ody_B | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_B.png | pose_ody_B.txt | ~$0.041 | ok | 31s |
| 25 | pose_ody_C | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=odysseus_C.png | pose_ody_C.txt | ~$0.041 | ok | 35s |
| 29 | pose_cy_D | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=cyclops_D.png | pose_cy_D.txt | ~$0.041 | ok | 30s |
| 27 | pose_cy_A | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=cyclops_A.png | pose_cy_A.txt | ~$0.041 | ok | 36s |
| 30 | pose_cy_C | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=cyclops_C.png | pose_cy_C.txt | ~$0.041 | ok | 38s |
| 28 | pose_cy_B | gpt-image-2.6-sunburst | 1024x1024 medium | edit, refs=cyclops_B.png | pose_cy_B.txt | ~$0.041 | ok | 40s |

## Totals
- 30 of 40 calls used, 10 unused. All gpt-image-2.6-sunburst, 1024x1024, medium, via images/edits (reference image in every call).
- Breakdown: 20 cast designs (5 characters x 4 options), 2 regenerations (sheep_D and cyclops_D, anchor leakage: saddle blanket and satchel strap; originals kept in tests/chars_v3/gen/rejected/), 8 pose tests (Odysseus shouting, Cyclops blinded, x 4 options). No separate probes: call 1 was the A Odysseus design and doubled as the method probe.
- Estimated cost 30 x ~0.041 = about 1.23 USD (0.034 image + 0.007 reference input). OpenAI dashboard lags, so check the real figure there.
- Free work: cutout test (pipeline/cutout.js flood fill) on 8 images, contact sheets via pipeline/tools/sheets.js.
- Failures: 0 API errors. A first background run of the batch script died when its shell exited before any call was made (counter unchanged).

## Addendum 2026-11-12: style-A scene mock (pipeline/remotion-v3a)
- 0 new image calls (still 30 of 40 used). Cutouts of the existing style-A art (odysseus_A, cyclops_A, crew_A, sheep_A, poseidon_A, pose_ody_A, pose_cy_A) made by `pipeline/remotion-v3a/cut_a.js` into `public/img3/`. Props: v2 cup, a painted boulder cropped from the cave background (`make_boulder.js`), v2 ship with cleaned matte (`make_ship.js`).
- Outputs: `tests/v3a/stills_*.jpg`, `tests/v3a/contact.jpg`, `tests/v3a/clip_sheet.jpg`, clip `pipeline/remotion-v3a/out.mp4` (26.2 s, shots 4-9 of v2).
| 33 | bg_sunrise | gpt-image-2.6-sunburst | 1536x1024 medium | edit, refs=cyclops_A.png | tests/cheap_test/prompts/bg_sunrise.txt | ~$0.057 | ok | 30s |
| 34 | baked_blind | gpt-image-2.6-sunburst | 1536x1024 medium | edit, refs=odysseus_A.png,cyclops_A.png | tests/cheap_test/prompts/baked_blind.txt | ~$0.064 | ok | 31s |
| 32 | bg_fire | gpt-image-2.6-sunburst | 1536x1024 medium | edit, refs=cyclops_A.png | tests/cheap_test/prompts/bg_fire.txt | ~$0.057 | ok | 32s |
| 31 | baked_face | gpt-image-2.6-sunburst | 1536x1024 medium | edit, refs=odysseus_A.png,cyclops_A.png | tests/cheap_test/prompts/baked_face.txt | ~$0.064 | ok | 36s |

## Addendum 2026-11-12: cheap test (tests/cheap_test/)
- 4 new calls (31-34 of 40 used, 6 unused; cheap-test cap was 38). 1536x1024 medium, gpt-image-2.6-sunburst, via images/edits with refs (the 1536 size costs more than the 1024 rows above): bg_fire and bg_sunrise (ref cyclops_A.png as line-style anchor, no figures asked for, none leaked), baked_face and baked_blind (refs odysseus_A.png + cyclops_A.png). No retries, 0 API errors.
- Estimated cost: 2 x ~$0.057 + 2 x ~$0.064 = about $0.24 (assuming ~$0.05 per 1536x1024 medium call plus $0.007 per reference; the real figure is on the OpenAI dashboard and may be up to ~$0.30). Test spend target of $0.50 met.
- Free work: the Stage compositing pass (pipeline/remotion-v3a/src/lib/Stage.tsx, presets in src/stagePresets.ts, render with stills_cheap.js), contact sheets (tests/cheap_test/make_sheets.js).

## Addendum 2026-11-12: Blue Pill baked-scene stress test (tests/stress_test/)
New cap for this task: 24 additional calls (34 + 24 = 58 total). Real cost is about $0.10 per call per William's OpenAI usage page; estimate $0.10-0.15 each with references. Every attempt, including API errors, is counted. Rows below are logged individually by tests/stress_test/gen.py.
| 35 | cy_v2a | gpt-image-2.6-sunburst | 1536x1024 medium | edit, refs=odysseus_A_flat.png,cyclops_A_flat.png | tests/stress_test/prompts/cy_v2a.txt | est $0.10-0.15 | ok | 35s |
| 36 | cy_v2b | gpt-image-2.6-sunburst | 1536x1024 medium | edit, refs=odysseus_A_flat.png,cyclops_A_flat.png | tests/stress_test/prompts/cy_v2b.txt | est $0.10-0.15 | ok | 36s |
| 37 | pos_v2a | gpt-image-2.6-sunburst | 1536x1024 medium | edit, refs=odysseus_A_flat.png,poseidon_A_flat.png | tests/stress_test/prompts/pos_v2a.txt | est $0.10-0.15 | ok | 42s |
| 38 | cy_v3 | gpt-image-2.6-sunburst | 1536x1024 medium | edit, refs=odysseus_A_flat.png,cy_v2b_flat.png | tests/stress_test/prompts/cy_v3.txt | est $0.10-0.15 | ok | 40s |
| 39 | s01 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png,cy_v2b_flat.png | tests/stress_test/prompts/s01.txt | est $0.10-0.15 | ok | 34s |
| 43 | s02 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png,cy_v2b_flat.png | tests/stress_test/prompts/s02.txt | est $0.10-0.15 | ok | 33s |
| 44 | s04 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png,cy_v2b_flat.png | tests/stress_test/prompts/s04.txt | est $0.10-0.15 | ok | 35s |
| 40 | s03 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png,cy_v2b_flat.png | tests/stress_test/prompts/s03.txt | est $0.10-0.15 | ok | 35s |
| 42 | s05 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png,cy_v2b_flat.png | tests/stress_test/prompts/s05.txt | est $0.10-0.15 | ok | 38s |
| 41 | s06 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png,cy_v2b_flat.png | tests/stress_test/prompts/s06.txt | est $0.10-0.15 | ok | 39s |
| 47 | s07 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png | tests/stress_test/prompts/s07.txt | est $0.10-0.15 | ok | 22s |
| 46 | s09 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png | tests/stress_test/prompts/s09.txt | est $0.10-0.15 | ok | 28s |
| 49 | s10 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png | tests/stress_test/prompts/s10.txt | est $0.10-0.15 | ok | 30s |
| 45 | s11 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=cy_v2b_flat.png | tests/stress_test/prompts/s11.txt | est $0.10-0.15 | ok | 36s |
| 48 | s08 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png | tests/stress_test/prompts/s08.txt | est $0.10-0.15 | ok | 37s |
| 54 | s16 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=crew_A_flat.png | tests/stress_test/prompts/s16.txt | est $0.10-0.15 | ok | 30s |
| 50 | s15 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=crew_A_flat.png,odysseus_A_flat.png | tests/stress_test/prompts/s15.txt | est $0.10-0.15 | ok | 32s |
| 53 | s13 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=cy_v2b_flat.png | tests/stress_test/prompts/s13.txt | est $0.10-0.15 | ok | 34s |
| 52 | s14 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=crew_A_flat.png | tests/stress_test/prompts/s14.txt | est $0.10-0.15 | ok | 35s |
| 51 | s12 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=cy_v2b_flat.png | tests/stress_test/prompts/s12.txt | est $0.10-0.15 | ok | 37s |
| 56 | s14b | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=crew_A_flat.png | tests/stress_test/prompts/s14b.txt | est $0.10-0.15 | ok | 32s |
| 57 | s05b | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png,cy_v2b_flat.png | tests/stress_test/prompts/s05b.txt | est $0.10-0.15 | ok | 36s |
| 55 | s12b | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=cy_v2b_flat.png | tests/stress_test/prompts/s12b.txt | est $0.10-0.15 | ok | 39s |
| 58 | s14c | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=s15.png,crew_A_flat.png | tests/stress_test/prompts/s14c.txt | est $0.10-0.15 | ok | 31s |

### Totals after the stress test (2026-11-12)
- 58 of 58 calls used (34 earlier + 24 for tests/stress_test/). 0 API errors. All gpt-image-2.6-sunburst via images/edits, quality medium: 4 uplift sheets at 1536x1024 (calls 35-38), 20 scene images at 1536x864 (calls 39-58: 16 first attempts, 4 retries s05b, s12b, s14b, s14c).
- Cost: about $0.10 per call per William's usage page, so about $2.40 for the 24 calls (range $2.40-3.60 with reference inputs). Dashboard figure not checked by me.
- Results and scores: tests/stress_test/SCORES.md; prompts: tests/stress_test/PROMPTS.md. Cap is now exhausted; no further image calls without a new instruction.

## Addendum 2026-11-12: Blue Pill crew-scene test (tests/crew_test/)
New cap for this task: 8 additional calls (58 + 8 = 66 total). 4 used (calls 59-62), then stopped by the stop rule: 0 of the first 4 passed, so 4 calls were left unspent. Real cost is about $0.10 per call per William's usage page; estimate $0.10-0.15 each with 2 refs. Rows are logged by tests/crew_test/gen.py. Refs are copies of stress-test scenes in tests/crew_test/refs/ (s15 = slot 15, s05b = slot 05 retry, s10, s01, s11).
| # | id | model | size/quality | type | prompt file | est cost | status | time |
|---|----|-------|--------------|------|-------------|----------|--------|------|
| 59 | c4 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=s15.png,s01.png | tests/crew_test/prompts/c4.txt | est $0.10-0.15 | ok | 29s |
| 60 | c3 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=s15.png,s05b.png | tests/crew_test/prompts/c3.txt | est $0.10-0.15 | ok | 32s |
| 61 | c1 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=s15.png,s10.png | tests/crew_test/prompts/c1.txt | est $0.10-0.15 | ok | 28s |
| 62 | c2 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=s15.png,s01.png | tests/crew_test/prompts/c2.txt | est $0.10-0.15 | ok | 28s |

### Totals after the crew test (2026-11-12)
- 62 of 66 calls used (58 earlier + 4 here). 0 API errors. All gpt-image-2.6-sunburst via images/edits, 1536x864 medium, 2 refs per call; 4 first attempts (c1-c4), 0 retries, 0 passes. Slots 5 and 6 not run.
- Cost: about $0.40-0.60 for the 4 calls at $0.10-0.15 each (not checked on the dashboard). Results: tests/crew_test/SCORES.md; prompts: tests/crew_test/PROMPTS.md; recommendation: PIPELINE-RECOMMENDATION.md. 4 calls remain under the 66 cap; do not spend them without a new instruction.
| 63 | cy_v4b | gpt-image-2.6-sunburst | 1536x1024 medium | edit, refs=odysseus_A_flat.png,cy_v2b_top.png | tests/stress_test/prompts/cy_v4b.txt | est $0.10-0.15 | ok | 36s |
| 64 | cy_v4a | gpt-image-2.6-sunburst | 1536x1024 medium | edit, refs=odysseus_A_flat.png,cy_v2b_top.png | tests/stress_test/prompts/cy_v4a.txt | est $0.10-0.15 | ok | 43s |
| 65 | cy_v4_s02 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=odysseus_A_flat.png,cy_v4_flat.png | tests/stress_test/prompts/cy_v4_s02.txt | est $0.10-0.15 | ok | 33s |
| 66 | cy_v4_s11 | gpt-image-2.6-sunburst | 1536x864 medium | edit, refs=cy_v4_flat.png | tests/stress_test/prompts/cy_v4_s11.txt | est $0.10-0.15 | ok | 39s |

### Addendum 2026-11-12: Cyclops v4 reference, bells removed (tests/stress_test/)
New cap for this task: 4 additional calls (62 + 4 = 66 total). All 4 used (calls 63-66), 0 API errors, 0 retries. Real cost about $0.10 per call per William's usage page; estimate $0.10-0.15 each, about $0.40-0.60 total (dashboard not checked). Rows above were logged by tests/stress_test/gen4.py (cap 66). Refs: odysseus_A_flat.png = style anchor; v4/cy_v2b_top.png = cy_v2b_flat cropped above the belt (head, beard, shoulder) so the bells could not leak; cy_v4_flat.png = front view cut from cy_v4a.
- Calls 63 (cy_v4b) and 64 (cy_v4a): new reference sheets, 1536x1024 medium. Both ignored the single-figure layout and returned multi-view turnarounds (front, side, back, head and detail panels), with no club and barefoot. Both met the four checks (one eye, no bells, olive skin, flat ink). cy_v4a picked: greener olive, more lopsided build, stitched hide patch. Prompts: prompts/cy_v4a.txt, prompts/cy_v4b.txt.
- Calls 65 (cy_v4_s02, refs odysseus_A_flat + cy_v4_flat) and 66 (cy_v4_s11, ref cy_v4_flat): 1536x864 validation scenes using the s02 and s11 prompts with the new identity paragraph (club described in text because the ref has none). Prompts: prompts/cy_v4_s02.txt, prompts/cy_v4_s11.txt.
- Outputs: refs/cy_v4.png (1024x1024, white background), refs/cy_v4_flat.png (same), gen/cy_v4a.png, gen/cy_v4b.png, gen/cy_v4_s02.png, gen/cy_v4_s11.png, cyclops_v4_check.jpg. 66 of 66 calls used; no further calls without a new instruction.

## Addendum 2026-11-12: video 1 art generation (video1/)
64 further calls (no cap, William's instruction), 0 API errors, gpt-image-2.6-sunburst 1536x864 medium, logged per call in video1/cost_log.csv with measured tokens (924 output, about 1,700 input per call). 37 of 38 new assets accepted, NB14 flagged. Estimated spend $3.4-3.9 (up to $6.4 at $0.10 per call); dashboard not readable (Cloudflare check, no login). Lesson: keep the stress-test prompt footer and STYLE paragraph unchanged plus the inline flat-ink clause; rewriting it made Cyclops scenes semi-realistic (17 of 20 rejected). Full report: video1/GENERATION-REPORT.md.
