FIXTURE, not a real Figma file. `sample_file.json` is hand-written to follow the documented GET /v1/files/:key response
(document > CANVAS > FRAME > layers; absoluteBoundingBox, size, relativeTransform, opacity, characters).
It exercises: frame B001 (plate + sprite + crew group + an unknown layer), B003 (hand-placed sprite, flipped copy,
a rotated copy at 50% opacity, a nested GROUP, CAPTION text, an inset), a frame not named B###, and a beat with several shots.
Values were invented to look plausible; nothing here came from Figma. The live path (real file, /v1/images export) is [U].
