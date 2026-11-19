# Editor review: character-style options (A-D) and the v3a scene mock, 2026-11-12

Read-only review. No project files were modified, nothing uploaded or messaged, no images generated.
Labels: [V] seen in the images or frames I opened, [E] my judgement or estimate, [U] could not judge.

Opened: `tests/chars_v3/cast_ALL.jpg`, `sheet_cyclops/poseidon/crew.jpg`, `sheet_poses.jpg`, `cutout_test_dark.jpg`; `tests/v3a/contact.jpg`, `clip_sheet.jpg`, `stills_a/b/c/d/e/f`; reference montages `tests/ref_mJS_sheet_0-2.jpg` plus full frames f_06, f_09, f_10, f_12; the v2 proof frames; CHARACTER-OPTIONS/LOG/STYLE-REF and NOTES.md. I did not play out.mp4; I judged the 11-frame clip sheet and stills. I did not run the cutout tests myself (B's ragged edge is taken from the write-up plus the dark-background strip, where it is not obvious at that size).

## Short answer
1. **A is the best base**, but only paired with (a) backgrounds redrawn in the same inked language and (c) a proper compositing pass. Ranking: **A > C > B > D**.
2. **Pasted-on is not fatal to cutouts. It is fatal to cutouts over soft-painted, back-lit backgrounds.** The reference does not do that outside maps.
3. **Correction to our own reference notes:** in its character scenes the reference's backgrounds are inked and flat, in the same line language as the characters, and the Cyclops is inked with cel shading, not painted-realistic.
4. Plan on **three shot types**: baked scenes with slow Ken Burns, cutouts on matched backgrounds, and maps/cards/white cutaways. Limb animation is not on the table.

---

## 1. Whole-cast ranking, with the decisive weakness of each

| Rank | Option | Why it ranks here | Decisive weakness |
|---|---|---|---|
| 1 | **A** mature cartoon | Reads clearly adult next to the control [V]. Hard outline gives clean cutouts [V, plus 7 cutouts in the v3a mock]. Flat colour plus one shadow tone is the only look that accepts a grade, rim and shadow without clashing [E]. Stylisation also hides AI tells. | It can look like generic clean-TV-cartoon. Faces are neutral and a little vacant, and the poses so far are front-facing and stiff [V]. |
| 2 | **C** textured 2D, rim light | Best faces and acting: the shouting Odysseus is the most alive of the four [V]. Strongest Cyclops silhouette. | The rim light and saturation are baked in. The orange skin on the Cyclops (Hulk or Oompa-Loompa risk) is a lighting decision made once for every scene, and it clashes with blue night scenes [E]. Sash drifted from blue to teal in both poses [V]. |
| 3 | **B** painterly | Most credible and adult, the best single images [V]. | Light is painted into the figure, edges are ragged, faces are tiny [per write-up]. It is also the most generic "AI digital painting" look, and a mythology audience is hardest on that. It only works if we go full baked scenes with no cutouts. |
| 4 | **D** paper-cut | Distinct from every competitor in the sample. | The "paper" is a flat image with a soft shadow [V]: no real cut edges or layers. Skin reads beige and plastic. Needs paper backgrounds too, and has no reference proof. Highest brand risk, lowest evidence. |

**Hybrid:** the "A for people, C or B for Cyclops/Poseidon" idea in CHARACTER-OPTIONS is a trap. Mixed styles in one frame recreate the pasted-on problem between the characters [E]. Do the reference's tiered fidelity inside A instead: heavier line, a second shadow tone, scars and texture on monsters and gods, plain faces on the crew. A's Poseidon is already good [V] (stern brows, trident, sea-green hair).

---

## 2. The pasted-on problem

**Is it fatal?** No. It has three separate causes, and the current mock hits all three [V in stills]:
1. **Language mismatch.** Hard ink outline over soft, textured, painted rock. Fixable (a).
2. **Light mismatch.** Backgrounds are back-lit sunsets and firelight. Characters are flat front-lit with no response to that light. In `stills_b` the Cyclops and Odysseus should be rim-lit or silhouetted against the sun and are not. Fixable (c).
3. **No ground contact or depth.** Shadows are faint ovals, there is no haze, and scale is by eye. Odysseus and the Cyclops share one ground line (feet at nearly the same y), so he reads as a small man standing beside a giant, not far from one. Fixable (c) plus a ground-plane convention.

The remaining problems are props and matting, not style: floating cup (`stills_d`), soft-edged grey disc as boulder (`stills_b`), ship matte residue and a front-facing man standing on a flat side-view hull (`stills_f`). They are asset defects. I would not judge the style on them.

| Fix | Cost per video | Drift risk | Effort | Verdict |
|---|---|---|---|---|
| **(a) Backgrounds in the characters' inked language** | About 8-12 unique backgrounds at 1536x1024, roughly $0.04-0.08 each [E], so under $2 with rejects. Reuse by crop and flip. | Low to medium: needs a style-anchor image. | Low: prompt work, plus an "empty stage, clear ground band" convention. | **Do this.** It is what the reference does. |
| **(b) Paint characters to match backgrounds (B/C)** | Cheap per image. | High. Light changes per scene (dusk, fire, night), so one painted figure matches one scene. Relighting means regenerating, which is (d) with extra steps. | Medium to high. | Reject. |
| **(c) Compositing: shared light, rim, grade, grain, contact shadow, haze, background blur** | Free per shot once built. | None. | About 1-2 days to build a shared Stage component with per-shot parameters [E]. Flat A cel art takes multiply and rim overlays well. | **Do this.** Necessary but not sufficient on its own. |
| **(d) Baked scenes, characters inside** | About 60-90 calls per video with rejects, at $0.05-0.08 with 2-3 reference images [E]: roughly $5-8 per video. | Highest: faces and costumes drift shot to shot. Mitigated by strong identifiers (Odysseus: wreath, red tunic, blue sash, beard; Cyclops: one eye, beard, fur) and by crowds, where drift reads as variety. | Medium: prompt plus a reject pass. | Use for action and ensemble shots, not as the only mode. |

**Recommendation: (a) plus (c) as the default, (d) for shots where several characters interact or move through space.**

**Cheap test for the pasted-on problem (4 image calls; same test as in section 6):**
- Generate 2 new empty-stage cave backgrounds in A's inked style, anchored on `odysseus_A.png`/`cyclops_A.png` (call them `cave_inked_dusk`, `cave_inked_fire`).
- Place the existing A cutouts on them with a first-draft Stage pass: multiply tint from the bg's dominant light, a thin rim overlay on the sun side, ground contact shadow, 3 px bg blur, light grain.
- Generate 2 baked scenes of the same two moments (Cyclops looming over Odysseus; boulder across the entrance) using the A anchors as references.
- Success: William and I blind-pick the inked bg plus Stage version over the current v3a mock, and the baked version is within one identity slip of the anchors (same eye count, wreath, sash colour).

---

## 3. What the reference does about it [V from frames]

It does face the same problem and uses four tactics:
1. **White cutaways** (f_03, f_07, f_15, f_22): no background, no integration needed.
2. **Inked backgrounds** for character scenes (f_05, f_08, f_10, f_11, f_12, f_13, f_16, f_20, f_24, f_27). Thick outline, flat colour, minimal texture, same line language as the figures. Many of these look like baked whole scenes: in f_10 and f_12 the Cyclops and the scene share one hand.
3. **Maps (f_00, f_04, f_06, f_17):** the characters really are stickers on a shaded painterly map, and it works because a map is abstract and the figure has a thick outline.
4. **Dark scenes (f_09):** the background is darkened, the character stays bright and gets a white sticker outline. This is deliberate "foreground layer", not integration.

This contradicts the STYLE-REF line "painterly backgrounds, flat characters on top" and "monsters painted semi-realistically". In f_09, f_10, f_12, f_13 the Cyclops has the same ink line and cel shading as everyone else, just with more anatomy and blood. Our A is much closer to the reference than the notes suggested, and our painted soft backgrounds are the part that does not match it.
Two further things the reference does that our mock does not: the Cyclops is posed (seated, drinking, kneeling, hurt) not standing, and his face acts. Ours stands with a neutral face [V].

---

## 4. Production reality

**Shot budget [E]:** 10-12 min at about 12 cuts/min is 120-145 shots (the reference does 164 in 13 min). Roughly 15% maps/cards, 25% cutout shots, 45-55% baked or action scenes, the rest cutaways.

**Distinct character images for one 10-12 min Odyssey chapter [E]:**
| Character | Poses/expressions needed |
|---|---|
| Odysseus | 12-15 (neutral, explain gesture, point/shout, fear, scheming, grief, triumph, back view, sitting, three-quarter left/right) |
| Cyclops | 8-10 (neutral, drinking, eating, throwing, blinded, pleading, asleep, petting sheep, back view) |
| Crew | 3-4 archetypes x 2-3 poses |
| Poseidon | 3-4 |
| Sheep, props | 4-6 |
Total about 40-50 images, 60-80 across several episodes, with 30-40% rejects. That is $3-6 in calls per video; the cost that matters is the review time.

**Evidence from `sheet_poses.jpg` [V]:** 8 of 8 pose edits worked first try in all four styles. Same face, costume, hair and beard held, and the blinded Cyclops covers one eye. A and D held identity best; C moved the sash colour; B shrank the face. This is n=8 on two characters, one extreme pose each, always from the full-body anchor on white. It does not show drift over 20+ shots, two-character consistency, or small-face readability. A new problem it did not test: faces are about 100 px tall at 1024 square. A figure 280 px tall on screen (the ship shot) has an unreadable face.

**Is cutout animation viable?** As posed stills that slide, swap and push in, yes. As animation, no. Each figure is one flat image: the only motion available is translate, scale, a 1-2 px bob. There are no limbs to move, and the jerk check says nothing about whether it feels alive. Use hard pose swaps on a cut, not tweening.

**Assembly recommendation:** hybrid.
- Baked scene plus slow push (about 2-6%) for wides, groups and action.
- Inked background plus pose cutout for one- and two-character dialogue and reaction shots.
- Maps, count cards, white cutaway plates.
A single mode will fail: all-cutout looks static and stuck-on (this mock), all-baked drifts and costs most.

---

## 5. Faces, bodies, maturity, slop risk

**Odysseus (A)** [V]: bearded, sensible proportions, readable brow. At neutral he is blank, which is fine for an explainer. Costume: laurel wreath is generic (Roman/Apollo, not a wanderer returning from Troy), the red chiton with blue himation sash is plausible, the Greek-key hem is a good touch. No Mycenaean/Bronze Age detail, but the reference does not care either.
**Crew** [V]: near-identical, differing only by hair and the tunic's blue shade. In the mock they read as the same man three times. They need 3-4 deliberately different silhouettes (build, hair, one has a beard, one has a headband). The baldric across the chest reads Roman or medieval, so drop it.
**Cyclops (A)** [V]: anatomy is solid (hands, feet, sandal lacing). He reads as a big caveman with a cyclops eye, not as a monster: calm face, small eye, a Flintstones-style fur and club. Fixes: bigger eye and heavier brow, scars, asymmetric face, scale from camera angles (low angle) rather than just size, and an olive-wood branch club (Homer: a green olive trunk, not a mallet). His best frame is the blinded pose (`stills_e`), which has real horror and pathos; the standing neutral frames are the weakest.
**Cyclops (C)**: orange skin is the problem. **B**: muddy, the least readable at small size. **D**: pale, soft, least threatening.
**Poseidon** [V]: all four are generic "fantasy sea god" (crown, trident, teal wavy hair, loincloth). A and C are the strongest. Poseidon traditionally has no crown; drop it or accept it as slop-adjacent. He has no mid or low angle and is only a standing figure so far.
**Slop tells a mythology audience will catch:** identical symmetric muscle on every male; everyone in an A-pose facing the camera; the sunset-orange glow on every scene; the wreath; Poseidon's stock look; ship eye reads as Eye of Horus unless clearly Greek. Flat inked stylisation is more forgiving here than painterly realism.

---

## 6. Top 3 recommendations, one test, and limits

**Top 3:**
1. **Adopt A with a monster and god detail uplift.** Pair it with inked backgrounds and a shared Stage compositing pass. Keep cross-option hybrids out.
2. **Assemble in three modes** (baked scene plus Ken Burns, cutout on inked bg, maps/cards/white cutaways). No limb animation. Hard pose swaps.
3. **Fix the assets the mock exposed before more style work:** posed Cyclops (seated, drinking, looming from low angle), crew with distinct silhouettes, a real boulder with edge and contact shadow, a hull drawn at the angle the figure is, no round-head cup.

**One A/B/C test, 4 core image calls (8 maximum with spares):**
- Same 2 moments (Cyclops looms over Odysseus at the cave mouth; the boulder is rolled across the entrance), three treatments:
  - **A** = existing A cutouts on 2 new inked empty-stage backgrounds (`cave_inked_dusk`, `cave_inked_fire`) plus the Stage pass (2 calls).
  - **B** = 2 baked scenes in A's inked style using `odysseus_A.png` and `cyclops_A.png` as references (2 calls).
  - **C** = existing v3a painted backgrounds plus the same Stage pass (0 calls, control).
  - Up to 4 spare calls for fixes (low-angle Cyclops pose, 3 distinct crew).
- Success criteria: (1) blind pick by William and me, at least one treatment beats the v3a mock for "looks like one image"; (2) baked scenes keep eye count, wreath, sash colour and beard on both characters in at least 3 of 4 images; (3) Odysseus's face reads (brow and mouth discernible) at 280 px tall; (4) total spend under $0.50 in calls and under 2 hours of work.

**What I could not judge [U]:** audio and music; real-time feel of motion (I used stills and a clip sheet, not playback); audience reaction, especially to AI-generated art from a mythology crowd; how well poses hold over 20+ shots; whether the reference's animation (which I have not watched, only 40 stills) uses movement that this analysis misses.
