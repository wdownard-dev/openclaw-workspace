# Character options for The Myth Ledger (2026-11-12)

Inputs: CHARACTER-STYLE-REF.md (what the reference does), CHARACTER-LOG.md (calls and cost). Nothing was uploaded or sent.
Labels: [V] seen in the generated images, [E] my judgement, [U] not tested.

## Where things are (all under tests/chars_v3/)
- Per-character sheets, CONTROL left then A-D: `sheet_odysseus.jpg`, `sheet_cyclops.jpg`, `sheet_crew.jpg`, `sheet_sheep.jpg`, `sheet_poseidon.jpg`
- Whole-cast sheet per option (CONTROL row above, option row below): `cast_A.jpg`, `cast_B.jpg`, `cast_C.jpg`, `cast_D.jpg`; overview of all four: `cast_ALL.jpg`
- Pose/expression test (rows: Odysseus neutral, Odysseus shouting, Cyclops neutral, Cyclops blinded; columns A-D): `sheet_poses.jpg`
- Cutout tests: `cutout_test_heads.jpg`, `cutout_test_dark.jpg`, files in `cut/`
- Raw designs `gen/<char>_<A-D>.png` (1024x1024, white background), prompts in `prompts/`, controls in `control/`.
- Crew control is the hero art tinted as in v2 (there is no separate crew art). Poseidon has no control (the v2 end card is text only), so his CONTROL cell reads NO ART YET.

## What the reference taught us (short)
It is not one style. Minor figures are simple (round head, dot eyes, brows), the hero soldier has a detailed painted costume, and monsters and gods are drawn realistically with scars and blood. Detail contrast carries importance, and the Cyclops is menacing because he is drawn like a person. Our v2 cast was the minor tier applied to everyone, which is a big part of "childish". Full notes: CHARACTER-STYLE-REF.md.

## The four options
All five characters in each option come from the same style paragraph plus the option's Odysseus as style anchor. Heights are all full-figure on white; real scale (Cyclops larger than Odysseus) is set at composite time.

| | Look | Reference tie |
|---|---|---|
| A | Mature cartoon: dark brown ink outline, flat colour plus one cel shadow, about 4 heads tall, human oval faces with brows and a small mouth | Closest to the reference's outlined characters on painterly backgrounds |
| B | Painterly storybook, gouache texture, no outline, about 6.5 heads | Closest to the reference's painted monsters and backgrounds |
| C | Stylised 2D with rim light, layered colour shadows, grain, expressive eyes, about 5.5 heads | Between the two: modelled like their monsters, graphic like their heroes |
| D | Layered paper-cut collage, paper fibre, soft drop shadows | Not in the reference (wildcard) |

## Honest assessment [V = looked at the images]

**Credibility and maturity.** All four read clearly older than the round-head control. B is the most "adult", A the most clearly "cartoon".

**Artefacts found and fixed.** Sheep D was wearing Odysseus' sash and a saddle blanket, and Cyclops D had a blue satchel strap (the anchor image leaked into the new character). Regenerated with an explicit "copy only the style, not clothing" line, both clean now. Cyclops has exactly one eye in all four, checked at high zoom. Remaining drift [V]: C changed Odysseus' blue sash to teal; C gives the Cyclops orange skin and a warm rim light on every character; crew and Odysseus have almost the same silhouette in every option (they differ by colour only).

**Pose and expression test (the key animatability check)** [V]. Re-drawing the same character in a new pose and expression via image edit worked first try in all 8 cases: same face, costume and style, readable shouting and agony, one eye still covered by the hand on the blinded Cyclops. So per-shot poses can be generated from a locked design, no pose library needed.

**Cutouts** [V on 8 images, flood fill from pipeline/cutout.js]: A clean (the outline stops the fill). C clean. D clean. B has slightly ragged, feathered edges and a faint light fringe on hair and shoulder, so it needs a better matte for hair and cloth.

| | Credible / mature | Animatable (cut into parts and poses) | Drift risk | Main risk |
|---|---|---|---|---|
| A | Good, still a cartoon | Best: hard outline, easy cutout, clean flat areas [V] | Lowest [E] | Can look generic, like a clean explainer or TV cartoon; faces are less deadpan than the reference's blank faces |
| B | Best | Weakest: ragged edge, lighting painted into the figure (bad when moved around), face detail too small to read at ship-deck size [E] | Highest [E] | Painted-in shadows and light direction will not match each background |
| C | Very good, most polished | Good: clean edge [V], strong face acting [V] | Medium: colour drift [V], orange rim [V] | Look shifts across 100+ shots; saturated orange skin on the Cyclops looks odd on cool night scenes |
| D | Good, distinctive | Good for flat cutouts [V]; real layered puppet parts would need manual or model-based splitting [U] | Medium [E] | Craft look may read as a "kids' craft" video if backgrounds stay painted; clashes with painted scenes unless they are paper-cut too |

## Ranked recommendation
1. **A for the main cast.** It is the only option that meets all three needs at once: it looks older than v2, cuts out cleanly, and holds identity across poses at the lowest cost and drift. It also matches how the reference layers outlined characters over painterly backgrounds. Weakness to manage: lean on posed faces and costume detail, not emoji marks, so it does not become a generic cartoon.
2. **C if you want more polish than the reference.** Best faces and the richest look. Fix its sash and skin colour drift by locking a palette in the prompt, and expect more regenerations.
3. **D if brand difference matters more than matching the reference.** Distinct from every competitor in the sample, but a real change of direction (backgrounds would need to match).
4. **B last for characters.** It is the best-looking single image, but light is baked in and edges are ragged, so it fails exactly where we need reuse and cutouts. It may suit monsters or gods only, as the reference does.

**Suggested hybrid [E]:** use the reference's tier idea. A for people and crew, and C or B rendering for the Cyclops and Poseidon so they look dangerous. That is not tested together in one scene.

## What I did not test [U]
Two characters in one scene, drift over 20+ shots, matching a character to a painted background (lighting, scale, shadows), real layered-part splitting for D, face expression sets beyond one shouting and one blinded pose, any motion. I also have not watched the reference in motion, only 40 stills. "Blue-skinned crew" in the v2 render was a tint on the hero art, so I designed the crew as normal-skinned men in blue-grey tunics; say if you want them literally blue.
