# PIPELINE-RECOMMENDATION.md: baked-scene pipeline for video 1 (2026-11-12)

Nothing uploaded or sent. Labels: **[M]** measured (counted from images, the call log, or William's usage page), **[E]** my estimate, **[U]** not assessed.
Evidence: cheap test (`tests/cheap_test/`, 4 calls), Editor reviews (`REVIEW-chars-2026-11-12.md`, `REVIEW-v2-2026-11-12.md`), stress test (`tests/stress_test/SCORES.md`, 24 calls), crew test (`tests/crew_test/SCORES.md`, 4 calls). The two image tests were scored by one reviewer (me); the Editor has not scored either.

## Verdict
**Conditional GO for a hybrid pipeline for video 1. NO-GO for crew-centred baked scenes until a second crew method passes. NO-GO for "all baked".**
- GO: baked 16:9 scenes in style A for **Odysseus-only, Odysseus + Cyclops and Cyclops-only** shots, with locked refs and a retry allowance. [M] Final slots passing: Odysseus-only 4/4, Odysseus + Cyclops 4/6, Cyclops-only 2/3. Odysseus' wreath, sash and beard held in 11/11 scenes.
- NO-GO as proven: baked scenes where **the crew is the subject**. [M] 0 of 7 crew-centred first attempts passed (3 in the stress test, 4 in the crew test). Only one of the 7 returned a real scene with distinct men (s14c, slot 14, which failed on soft style).
- Not a blocker: crew can appear small in wide shots, as extras in Odysseus shots, or as cutouts (see mix).

## Evidence in one table
| Source | Result |
|--------|--------|
| Cheap test | William's blind pick: baked scenes beat the inked-background + compositing pass and the v3a cutout control in both moments. Editor and worker ranking agreed. [M, n=2 moments] |
| Editor, characters | Style A ranks first (clear adult read, clean ink outline, flat colour + one shadow). Mixed styles in one frame recreate the pasted-on look. Three shot types (baked + Ken Burns, cutouts on matched backgrounds, maps/cards/white cutaways). No limb animation. Slop tells to avoid: symmetric muscle men, A-poses, sunset glow, stock Poseidon, ship eye. |
| Editor, v2 | "Childish" came from motion, type, grade, sound and the round head together. Calm motion, restrained type and a cooler grade matter as much as the art. [Editor's estimate] |
| Stress test | 10/16 final slots pass (62.5%, bar 12/16 missed); 9/16 first attempts (56%). Style drift was the largest failure (5/16 slots). Crew 0/3. 1536x864 baked scenes survive a 1.00-1.33x push-in at 1080p. |
| Crew test | 0/4. All four returned one bald man (cast member (a)) as a portrait; the scene, the other crew and Odysseus were ignored. Flat ink style held in 3/4 when a flat-ink scene was ref 2. |

## Recommended shot-type mix for video 1 [E, from the evidence above]
Reference pacing is about 12 cuts per minute.
| Shot type | Share | Notes |
|-----------|-------|-------|
| Baked scenes: Odysseus-only, Odysseus + Cyclops, Cyclops-only (16:9, 1536x864, Ken Burns push-in) | about 45% | The proven core. Prefer close and medium shots; keep faces large |
| Cutouts on inked empty-stage backgrounds + Stage pass | about 20% | Crew, ships, group moments, reaction beats. Backgrounds by the cheap-test method (about $0.06 each) |
| Baked scenes with crew as extras (crew small or in the background of an Odysseus shot, like slot 06) | about 5% | Only where Odysseus or the Cyclops is the focus |
| Maps, title cards, white cutaways, text | about 30% | Cheap, and the reference uses them heavily |
| Baked crew-centred scenes | 0% until a method passes | Optional upgrade if a retest passes |

## Reference-chaining method
1. **Two locked refs per call, flattened onto white**: `odysseus_A_flat` + `cy_v4_flat` (was `cy_v2b_flat`; or `pos_v2a`). Fixed identity paragraph per ref, plus "do not copy the white background, layout or pose". [M] Held Odysseus 11/11 and the Cyclops eye 8/9.
2. **Always include the flat-ink clause** ("flat inked cartoon rendering: clean ink outlines, flat colour, no painterly texture, no soft gradients, no mud"). [M] It restored style in s05b, and flat rendering held in 3/4 of the crew test. The retry without it drifted (s12b).
3. **Use an accepted flat-ink scene as the style anchor** when the subject needs a setting (ship, fire, dawn). [M, n=4] It improved flatness; it does not carry identity by itself.
4. **For a group, chain from an accepted group scene**, not the white-background crew sheet. [M] The crew sheet alone: 3/3 line-ups. Chaining from slot 15: s14c delivered a scene (1/1), but the crew test then collapsed to one man (0/4). Treat the method as unproven. Do not name the individual crewmen in a lettered list; describe the group in the plural and lead with the action.
5. State shot geometry, lighting and "UNDER, not behind" positions explicitly; state "no other eye visible" for occluded Cyclops faces. [M] Each fixed a failure once.
6. **Cyclops ref fixed (done 2026-11-12): `cy_v4` replaces `cy_v2b`** (`tests/stress_test/refs/cy_v4_flat.png`). The two brass belt bells leaked into 8 scenes with cy_v2b [M]. cy_v4 has a plain rope belt with nothing hanging from it, and its two validation scenes (`cyclops_v4_check.jpg`) show no bells and no pouch [M, n=2]. Use cy_v4 in place of cy_v2b in every call, and describe the club in the prompt text (the ref does not show it). Always include: "plain twisted rope belt with NOTHING hanging from it (no bells, no pouch, no gourd, no knife, no metal)".

## Expected rejection rate and cost
All numbers cover 1536x864 medium scenes.
| Item | Value | Basis |
|------|-------|-------|
| First-attempt reject rate, non-crew shots | about 30% (4 of 13) | [M] n=13 |
| First-attempt reject rate, crew-centred shots | 100% (7 of 7) | [M], but 6 of the 7 used the same ref method; the method may be the issue |
| Attempts per accepted non-crew scene | about 1.5 (15 attempts, 10 accepted) | [M] |
| Cost per call | $0.10-0.15 | about $0.10 per William's usage page (stress test) [M]; $0.15 allows for refs [E] |
| Cost per accepted baked scene | about $0.15-0.23 | [E] 1.5 attempts x $0.10-0.15 |
| Cost per minute, all-baked non-crew | about $1.8-2.8 | [E] 12 cuts x $0.15-0.23; unrealistic because of crew shots |
| **Cost per minute, recommended mix** | **about $0.9-1.5** | [E] |
| 10-minute video 1, generation only | about $9-15 | [E] |
| Spend so far | $5.05 for about 110 requests at 14:05 ET, before the stress test | [M] William's usage page. About $0.046 per request on average; lower than later calls because early calls were 1024x1024 |
| Spend since | stress test about $2.40-3.60 (24 calls), crew test about $0.40-0.60 (4 calls) | [E], dashboard not checked. Running total about $7.9-9.3 [E] |

Review time is the real cost and is **not measured** [U]. Budget at least one reject pass per batch (Editor or William) and a 2-call retry allowance per 3 scenes.

## Remaining weak points and risks
1. **Crew-centred scenes** (above). Highest priority. A cheap fix attempt would use up to the 4 remaining calls (SCORES.md lists the untested ideas); do not block video 1 on it.
2. **Style drift to painterly or semi-real** (5/16 in the stress test: slots 03, 06, 12, 14, 15). It shows at full size, less at thumbnail size. Mitigation: the flat-ink clause plus a flat-ink style-anchor ref. Not yet proven to bring drift below about 15%.
3. **Occluded or tilted faces** (Cyclops eye count). Fixable with explicit wording, but each failure costs a retry.
4. **Odysseus too small in wide shots** (slot 06: about 190 px tall at 1080p, face unreadable). Rule: wide shots carry the Cyclops or the crew, not Odysseus' face.
5. **Prop and symbol leakage**: bells (fixed in cy_v4), a ship-hull eye symbol (reads as Eye of Horus), a stake that reads as a short sword.
6. **Cyclops skin (cy_v4)**: now a cool olive-brown with a grey-green cast, no longer tan or orange [M, 2 scenes]. Trade-offs I saw: it reads close to khaki or ogre-green in the sheet, the eye is smaller and less menacing than cy_v2b's, line detail is lighter, and the ref has no club and bare feet (the scenes added the club and sandals from the prompt text). Asymmetry is still mild. Judgement call; the Editor has not scored it [U].
7. **Resolution**: 1536x864 upscales 1.25-1.33x in a push-in. Crisp at normal viewing, slightly soft at 100% [V on stills]. Playback and compression artefacts [U].
8. **Sample sizes are small** (16 slots, 4 crew images, 2 blind moments) and scored by one reviewer. Pass and reject rates carry wide error bars.
9. **Not assessed [U]**: audio and music; motion feel in real playback; how a mythology audience reacts to AI art; platform AI-disclosure and monetisation rules; whether calm motion fixes the "childish" criticism (the Editor says it matters as much as the art).
10. **Style A can look like generic clean-TV cartoon** (Editor). The stress-test images read more adult than the earlier cutouts, but this is a judgement, not a measurement.

## Suggested next steps
1. William decides the crew route: (a) one more crew test with up to the 4 remaining calls and the revised wording, or (b) drop baked crew scenes and use cutouts and extras.
2. ~~Regenerate the Cyclops ref without bells~~ **Done (calls 63-66, all 4 spent): `cy_v4` locked, ready for production** (2 of 2 validation scenes passed one eye, no bells, olive skin, style match; see `tests/stress_test/cyclops_v4_check.jpg`). Worth William's eye on the skin tone; to push it more brown, add "warm olive-brown" to the identity paragraph rather than regenerating the ref. The call cap (66) is exhausted.
3. Build the video 1 shot list from the proven core (Odysseus-only, Odysseus + Cyclops, Cyclops-only) and tag every crew shot with its fallback route.
