# PACKAGING: Norse (The Myth Ledger, video 2)
Uploaded PRIVATE only (see UPLOAD.json). Library and video2 untouched. Gemini spend: 4 image calls (about 1,500 output tokens each), about $0.27 at list price, under the $0.80 cap, no rerolls.

## 1. Titles (all under 60 chars, no "ENTIRE")
1. **Norse Mythology, Creation to Ragnarok, in 10 Minutes** (52). The honest idiom, trimmed (the full "The Story of Norse Mythology, ..." is 65).
2. The Sky Is a Skull: Norse Mythology in 10 Minutes (49). Hook-led on the opening picture.
3. The World Was a Giant: Norse Myth in 10 Minutes (47). Hook-led on the creation claim.
4. The Wolf, the Serpent and the End of the Gods (45). Hook-led on the two monsters.
5. Norse Mythology From a Dead Giant to Ragnarok (45). Hook-led on the strangest starting fact.
**Pick: #1.** It says what the video is, matches search intent ("norse mythology"), and pairs with the RAGNAROK thumbnail without repeating it. Runtime is 10:17. Use #2 as the A/B title if Test & Compare is available.

## 2. Thumbnails (1280x720; Gemini 3.1 Flash image with library cards + identity lines as refs; text by Pillow, Permanent Marker)
Raw outputs without text in `raw/` (A1, A2, B1, B2); generator `gen_thumbs.py`, text pass `text_thumbs.py`; finals `thumb_A.jpg`, `thumb_B.jpg`, `thumbs_2up.jpg`. Both checked at 320x180 (`raw/small_check.jpg`).
- **A, "THE SKY IS A SKULL"**: S01 skull plate with Odin in front. Strong picture, but Odin is seen from behind, so the eye patch does not read, he holds a plain staff instead of Gungnir, and the title overlaps his hat. Weaker.
- **B, "RAGNAROK"**: Fenrir's jaws open over Odin (armed, spear raised) against ember fire. Odin faces the viewer, the black eye patch reads at phone size, both characters are large, text sits in calm sky.
**Pick: B.** One eye patch reads, highest contrast, and the monster is the picture. A is the backup (the skull is the hook of the video; a crop with Odin turned toward camera would fix it).

## 3. Description, tags, pinned comment
See `description.txt`, `tags.txt` (19 tags, category 27, not made for kids), `pinned_comment.txt` (William pastes in Studio; our token cannot comment).
Chapters come from `audio-n/beats_timing.json` first-beat starts per chapter (the cold open's first beat is at 0.4 s, shown as 00:00). The render's audio is the mix and sync to the voice is within about 0.1 s (FINISH-NOTES: N-060 199.20 -> 199.27 etc.), so the voice times hold; the script header's times (1:46, 2:38 ...) are pre-recording estimates and were not used.
Links: only the two archive.org item pages, both returned HTTP 200.
