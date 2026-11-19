# Blue Pill Cyclops - locked reference library

Layout
- characters/<name>/: turnaround.png (canonical), face, expressions, silhouette/wardrobe where it matters, sheet.jpg (labelled composite), CHARACTER.md, manifest.json. Folders: odysseus, polyphemus, polyphemus_blinded (CANONICAL = turnaround_band.png, cloth band over the eye in every image; turnaround_scarred_hollow.png is non-canonical), crewman (+ turnaround_b / turnaround_c), neighbour_cyclops (three giants on one sheet), bard, hesiod, abel, pausanias, hackman, sailor, workers (2 variants; v3 regenerated with uniform cream skin; expressions.png = worker A, expressions_b.png = worker B), ram (front+side + 4 expressions: neutral, deadpan, straining, trotting), sheep (turnaround adult+lamb, group.png = flock of six + three tied side by side, face), maron (vineyard priest), odysseus also has turnaround_helmet.png (bronze crested helmet; NON-canonical variant, manifest canonical:false/variant:true, used only for helmet beats 329, 448, 551, 588; still copied to refs/).
- places/<name>/: wide/detail images, sheet.jpg, PLACE.md, manifest.json. Folders: cave_exterior (+ wide_notched_peak), cave_interior, beach_and_ship (+ ship_night_stars, ship_dusk_violet, harbour_dawn, shore_dusk_red), hillside_pasture, and v3 masters (master.png each): forge_cave, smithy, tiryns_wall (+ lion_gate_golden, wall_sunset), three_hilltops_night (+ thundercloud), vineyard_golden, library_lamplit, library_ancient_empty, study_1914, sea_storm (+ ship_in_storm), ship_deck (+ dusk). No characters in place images. Each has ONE master (manifest `master:true`); everything else is derived from it.
- props/: boulder, ship (+ ship_furled), stake_raw/stake_sharp/stake_fire (+ stake = the three stacked), wine, ram, and v3: torch, olive_club, cheese_set (cheese + basket + jar), lyre, scroll_quill, book_pile, brass_lamp, elephant_skull (+ _in_clay), dwarf_elephant, mule_pair, ox_cart, axe_tongs_trough, map_antique (+ map_rolled_blank), gulls, anvil_bolt, straw_bowls (+ PROPS.md, manifest.json, sheet.jpg contact sheet).
- refs/: flat copy of every canonical PNG as <folder>__<role>.png for quick upload to any generator.
- gen.py, SPEND.csv (running cap is the CAP constant in gen.py), prompts/, jobs*.json, build_prompts.py, compose.py, docs.py (legacy v1), derive.py (derive + verify variants), build_library.py (rebuilds sheets, manifests, MD, refs/ from the images on disk), stage_a/stage_b/chars_new.py (the v2 jobs). _superseded/ holds the pre-v2 images (do not use).

How to use
1. Pass only the canonical images of whoever (and whatever place) is present in the shot. Do not pass whole sheets.
2. Always include the text description from the matching CHARACTER.md / PLACE.md as well; the image carries the look, the text fixes colours and costume.
3. Prompt the scene with the shared STYLE.txt block. Odysseus has a laurel and no helmet; Polyphemus has exactly one eye (use polyphemus_blinded after the blinding).
4. For crew scenes pass crewman plus turnaround_b / turnaround_c so the crew are not clones.

Notes: silhouette.png files are cut from the turnaround front view in code, not generated. Expression sheets and some faces were generated using the face/turnaround as reference.

MASTER + DERIVE RULE (v2)
- A place or prop has ONE master image. Every variant (dusk, night, boulder moved, ship furled...) is DERIVED from that master with an image edit, never regenerated from text, so rocks, plants, objects and layout cannot drift.
- Method: `derive.py <id> <master.png> <out.png> "<change>" [--mode relight|same]` (wraps `gen.py edit`, which calls POST /v1/images/edits with the master as the image; prompt form: "Use the attached image as the exact scene. Keep every rock, tree, plant, object and the boulder in exactly the same position and shape. Change ONLY: <...>. Same painting style."). Two masters in one edit (e.g. beach + ship) work: the second image is named in the change text.
- Verify with derive.ground_diff on the lower 60% of the image (the ground): ground_raw_mad (mean abs pixel diff 0-255), ground_edge_corr (correlation of local-contrast-normalised edge maps) and top30_mad (sky changed). Max 3 tries, best kept.
- Thresholds that work (see DERIVATION_CHECKS.json): the raw pixel diff cannot be < 12 when the LIGHT changes (dusk/night/dawn legitimately move the ground colours: 35-73), so lighting variants are accepted on edge_corr >= 0.45 (true derivatives scored 0.59-0.74; the old text-regenerated variants scored -0.003..0.001, i.e. different caves). Same-lighting variants (boulder rolled across the mouth) must also show raw MAD < 12 on the ground outside the changed object: measured 7.7 (whole ground 19.8 because the boulder moved). Always eyeball the sheet too; the metric does not see small objects.
- To add a new variant: derive from the master, never from another variant.

COVERAGE (v3)
- CAST-CHECK.md maps every entity named in SCRIPT-V5.md shot lines to a library folder (cast_check.py regenerates it). No entity is MISSING.
- v3 scripts: stage_v3.py (masters), stage_v3b.py (derived variants), cast_check.py; build_library.py rebuilds sheets/manifests/MD/refs (79 refs).
- Place-variant derivation checks for v3 are in prompts/*.txt and the per-image .check.json files next to each derived PNG. Lion Gate is a zoomed re-framing of the tiryns master (edge check n/a).
- Script/library: V5 line 16 now has laurel + red cloak (matches). Helmet beats (329, 448, 551, 588) use the non-canonical turnaround_helmet variant (same red cloak).
