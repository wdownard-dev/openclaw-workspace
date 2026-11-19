# scripts/figma: Figma previz loop

1. `build_kit.py` exports the asset kit to `video2/previz/kit/` (PNG per asset id, contact sheets, `KIT.md`); `make_beats.py` writes `previz/BEATS.md`.
2. William imports the kit into Figma, one 1920x1080 frame per beat named `B###`, and arranges layers (`previz/FIGMA-SETUP.md`).
3. He sends the file link. Morpheus runs `figma_pull.py` (REST read-only, PNG export of each frame, contact sheet, `layout.json`).
4. `figma_pull.py` also writes `storyboard_patch.json`; review frames and patch.
5. `apply_patch.py` (dry run by default) shows the diff against `storyboard.json`; `--write` backs up and applies.
6. Re-render the Remotion animatic; repeat from 2.

## Commands (python: `~/.venvs/refwatch/bin/python`, needs pillow; env `FIGMA_TOKEN` is injected for live calls)
```
python scripts/figma/build_kit.py
python scripts/figma/make_beats.py
python scripts/figma/figma_pull.py <file_key_or_url> [--out video2/previz/pulls/<date>] [--no-images]
python scripts/figma/figma_pull.py --fixture scripts/figma/fixtures/sample_file.json --out /tmp/pulltest   # offline test
python scripts/figma/apply_patch.py <pull dir>/storyboard_patch.json            # dry run
python scripts/figma/apply_patch.py <pull dir>/storyboard_patch.json --write [--prune-missing]
```
Output of a pull: `layout.json` (per frame, per layer: name, x/y/width/height from frame top-left, centre, rotation, flip_x, opacity), `frames/*.png`, `contact_N.jpg`, `storyboard_patch.json`.

## Mapping to storyboard.json
Frame px = renderer px (1920x1080). Sprite/prop event: `src` = layer name + `.png`, `x` = layer centre x, `y` = layer bottom edge (feet; centre if `| inset`), `h` = layer height, `mirror` = horizontally flipped. Plate/map layer sets `shot.bg`. Frame `B###` patches the beat's first shot; `B###_sNNN` a specific shot. Layer order (back to front) is the order of new events.
Apply keeps existing event timing; new sprites get `at` = shot start word and `"previz": true`, so set their timing by hand. Unmapped (reported, never applied): rotation, opacity, CAPTION/other text, unknown layer names, plate moves, labels/stamps/chips/counters/swaps (stay as in the storyboard).

## Limits
- The REST API is read-only for layers: Figma cannot be edited from here; only William's edits flow back. Comments can be posted.
- Rate limits: HTTP 429 handled with Retry-After/backoff; frames exported 15 ids per `/v1/images` call; exported image URLs expire after about 30 days (downloaded immediately).
- Ignored Figma features: effects, masks, image crops/fills modes, blend modes, components/instances (read as plain layers), auto layout, constraints, hidden layers (skipped), rotation of parent groups (only the layer's own transform is read). A plain group is flattened; positions come from `absoluteBoundingBox`, so group transforms are fine.
- Layer aspect different from the kit PNG (squashed): warned; the renderer keeps aspect and uses height.
- Fixture `fixtures/sample_file.json` is hand-written, not from Figma (see `fixtures/README.md`).

## Status
Tested: fixture parse, patch, dry run, `--write --out` (original untouched), local frame rendering, `GET /v1/me` = 200 (curl and Python urllib). [U] Untested: a real file via `GET /v1/files/:key`, `/v1/images` export and download, 429 backoff, how Figma names duplicated imports, group/section nesting from real exports.
