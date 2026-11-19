# FIGMA-SETUP.md: arrange the beats in Figma (about 10 minutes of setup)

Kit: `video2/previz/kit/` (130 PNGs, 118 MB; contact sheets `kit_sheet_*.jpg`; sizes and ids in `KIT.md`). What each beat shows now: `BEATS.md`.

1. **Create a Figma file** (free plan is enough). Name it e.g. `Blue Pill previz`.
2. **One page per video**: rename Page 1 to `Video 1 Cyclops`. Add `Video 2 ...` pages later.
3. **Frames**: press `F`, pick the `Desktop 1920x1080` preset (or set W 1920, H 1080). Name each frame **B###** with the beat number, three digits: `B001`, `B002`, ... (list in `BEATS.md`). Beats with several shots: `B001` is the first shot; add `B001_s002` for the second. Duplicate a frame (Ctrl/Cmd+D) to start the next one, and keep frames in a grid, any order. Start with the beats you care about; unfilled ones are simply not pulled.
4. **Drag the kit PNGs in** (from `kit/sprites`, `props`, `plates`, `maps`; a few dozen at a time is easier than all 130). Drop a plate first as the bottom layer (it is already 1080 high; leave it full-frame), then characters and props. Drop each PNG straight onto the frame, so it becomes a child of that frame.
5. **Do not rename layers.** The layer name is the asset id and is how the pull matches it back to the storyboard. A duplicate named `odysseus__walk__a 2` is fine. Moving, scaling, flipping (Shift+H) are all read. Keep proportions (hold Shift while resizing).
6. **Position by feet**: the bottom edge of a character layer is where the feet stand (the renderer anchors sprites at their bottom edge). Use the frame's bottom third as the floor on white shots.
7. **Insets** (picture-in-picture): add `| inset` to the layer name, e.g. `prop__ram_with_feet__a | inset`.
8. **Ids with no image** (rings, pins, arrows, icons, maps drawn in code; list at the bottom of `KIT.md`): draw a rectangle and name it with the id.
9. **Optional**: a text layer named `CAPTION` with a note for me ("he looks up here"). It is recorded, not rendered.
10. **Share**: Share > anyone with the link can **view** (Figma's REST read needs the file in your account or a link I can read; if the pull says 403, tell me and we will switch to a team/file access setting). Paste the link in chat and say which beats are ready. Tell me when you edit again; I pull fresh each time.

Ignored on purpose: effects (shadows, blurs), masks, crops, blend modes, components/variants (use plain images), rotation and opacity (recorded, not rendered yet).
