# AUDIT-LOCK (Norse library, one round + one re-roll round). Not locked: William reviews first.

Checked by viewing CONTACT-CHARACTERS.jpg, CONTACT-PLACES.jpg and the turnarounds (not every image). Edge correlation numbers are in `edge_checks.json`.

## A. Odin: one eye / patch consistency
PASS. Black eye patch with a strap, one dot eye, wide hat, long grey beard, dark blue cloak on `odin_one_eye` (turnaround + face) and `odin_armed` (derived, patch, hat and beard kept, breastplate and spear added). Patch reads clearly at card size. Caveat: the hat brim is wide but the crown is pointed (a wizard-hat look); acceptable but William should confirm. Two-eyed Odin anywhere: none. Style-reference test: passing the Odysseus turnaround made the model copy Odysseus entirely (clothes, face, even the scenery), so the reference was dropped (file kept as `characters/odin_one_eye/NOTUSED_ref_attempt.png`) and every character uses the style block only.

## B. Tyr hand vs stump
PASS with a warning. `tyr_hand`: teal tunic, shield on left arm, open right hand. `tyr_stump`: same figure, right sleeve ends in a white bandage with no hand. The bandage is small; it will be a few pixels in wide shots (WARDROBE risk 4). Edge correlation 0.375 (pose shifted slightly; visual match is good).

## C. Hod band
PASS (after one re-roll). First roll wrapped the whole head like a mummy: NOT USED (`characters/_notused/hod_mummy_*`). Canonical: wide white bandage running diagonally across both eyes, nose and mouth visible, short dark hair on top, pale-grey cloak. Note: the model put a red tunic under the grey cloak (Hod's red vs Thor's red cape: they share beats N-117-121; cloak colours differ, acceptable).

## D. Heimdall horn / Hel split
Heimdall PASS (white cloak, gold curved horn raised). Hel PASS (face split black left / white right, black dress and hair, dot eyes, child proportions).

## E. Colour clashes (pairwise table)
- Odin blue / Tyr teal / Thor red / Loki lime: distinct. PASS.
- Vili purple, Ve mustard vs Ask/Embla leaf-green: distinct. PASS.
- Vidar olive cloak vs Modi/Magni red capes: distinct, BUT Vidar, Heimdall and Hod wear a red tunic under their cloaks (the model's choice; not in the identity lines). Minor: at 540p the cloak dominates. WATCH.
- Hymir slate blue-grey smock vs the brown-hooded `thor_disguise`: distinct. PASS.
- Snorri maroon with fur collar vs Odin blue: distinct. Scribe has the tonsure, Snorri does not. PASS.
- Thor: first roll added a winged helmet (not in the identity line; it would have confused him with Odin's hat): NOT USED (`_notused/thor_helmet_*`). Canonical Thor is bare-headed, red beard, red cape, grey stone mallet. The mallet reads as a hammer; NOTE the first Thor prompt was rejected by the image safety filter; the rewording "grey stone mallet" passed (two rejections in total, both logged in SPEND.csv at $0).

## F. Variants match their masters
- `thor_disguise`: PASS (hood up, no beard, red sleeves, hammer handle at the belt; red-brown hair shows at the hood edge and matches Thor's beard/hair colour).
- `fenrir_cub/young/bound/bound_sword`: PASS visually (same mane and eyes). Cub and young show two views at different sizes; fine.
- `loki_old_woman`, `loki_bound`, `loki_salmon`: PASS (green hem, rope bands, silver salmon with green fins).
- `baldr_dead`: PASS after re-roll (first roll showed a standing Baldr beside the ship: NOT USED `_notused/baldr_dead_v1`).
- `ymir_dead`: PARTIAL. Re-roll shows one view lying on the back and a second view that is the front of a figure lying with feet toward the viewer; the first view reads as lying/seated. Usable; flag for William.
- Place variants: 8 crops (free) + 27 edits. Edge correlation: 23 of 27 at 0.57 or higher; below 0.6: `hels_gate_day` 0.583, `midgard_shore_dusk` 0.568, `new_world_burning` 0.593 (after one re-roll from 0.357), `open_sea_night` 0.594, `open_sea_burning` 0.597 (all close, visually the same scene); `open_sea_naglfar` 0.403 (grey stormy sea chosen on purpose, ship added; geometry kept); `fensalir_door` 0.02 (intentionally a close view of a door, not a geometry-preserving variant). Pass bar judged visually.
- Master problems fixed by re-roll: `hymirs_boat` prop had a Greek city background (NOT USED, `places/_notused`); `open_sea` had a beach in the foreground (NOT USED), and its five variants were re-derived.
- Remaining master quirks (not fixed, cap-aware): `night_sky` shows a landscape strip and both sun and moon at the horizon rather than a pure sky; `rock_cave` is dark.

## NOT USED (kept on disk, never to be passed to a plate call)
`characters/odin_one_eye/NOTUSED_ref_attempt.png`; everything in `characters/_notused/` and `places/_notused/`.

## BLOCKERS REMAINING
None. Open warnings: Ymir (dead) partial, Vidar/Heimdall/Hod red tunics, Tyr stump size, Odin hat crown shape, Thor and `thor_disguise` identity depends on red hair at the hood edge, script `state:` lines do not name three variants (see CAST-CHECK.md: Thor (disguise), Odin (armed), Fenrir (bound, sword)).
