# LOOK-G2.md: gate G2 look test (colour, fonts, stamps) for video 1

Written 2026-11-13. Contact sheet: `video2/LOOK-G2.jpg` (2880x1752, nine cells of 960x540; each cell is a full 1920x1080 tile at half size, except cell 9 which is 1:1 pixels at 480 px wide). Phone tile alone: `video2/LOOK-G2.phone480.jpg`. Render script: `video2/LOOK-G2.js` (sharp + SVG text, no image API, no network after the font download). Re-run from `video2/`:

```
FONTCONFIG_FILE=$PWD/spike/fonts/fonts.conf FONTCONFIG_PATH=$PWD/spike/fonts node LOOK-G2.js
```

Labels: [V] verified by reading the file or looking at the render, [E] my judgement.

## 1. Font licences [V]

Both fonts sit in the `apache/` tree of the google/fonts repository, and their METADATA.pb says `license: "APACHE2"`. Apache 2.0 allows commercial use, embedding and redistribution; attribution is only needed if the font file itself is redistributed (keep the LICENSE file next to the TTF, which we do). Rendering text into a video needs nothing.

| Font | Role | Licence | Source checked | Local file (sha256, first 12) |
|---|---|---|---|---|
| Permanent Marker Regular (Font Diner, 2010) | hand-lettered display: impact words, counters, stamps, bubbles | Apache License 2.0 | https://github.com/google/fonts/blob/main/apache/permanentmarker/METADATA.pb and `LICENSE.txt` in the same folder; fonts.google.com/specimen/Permanent+Marker | `spike/fonts/PermanentMarker-Regular.ttf` (28f82c8a7943) |
| Special Elite Regular (Astigmatic, 2010) | typewriter: source chips | Apache License 2.0 | https://github.com/google/fonts/blob/main/apache/specialelite/METADATA.pb and `LICENSE.txt`; fonts.google.com/specimen/Special+Elite | `spike/fonts/SpecialElite-Regular.ttf` (a776fcb4ceb8) |

Licence texts saved as `spike/fonts/LICENSE-permanentmarker.txt` and `spike/fonts/LICENSE-specialelite.txt`. Fonts are loaded through `spike/fonts/fonts.conf` (a local fontconfig that adds the folder), so nothing was installed system-wide. The Remotion spike would load them with `@font-face` from `remotion/public/` instead; not wired yet.

No alternatives are needed. If William wants options anyway, the free ones I would test next: hand-lettered Caveat Brush or Rock Salt (both OFL/Apache on Google Fonts, unverified this session), typewriter Courier Prime (OFL, unverified).

## 2. What is on the sheet

| Cell | Element | Values used |
|---|---|---|
| 1 | Impact word on a painted plate (NB10, night cave) | "NOBODY", Permanent Marker 170 px, cream `#f3e9d2` fill, ink `#1a1204` outline 11% of size, rotated -2 deg; chip in the corner |
| 2 | Impact word on white beside the Odysseus cutout | "SIX MEN / GOT OUT", 190 px, solid ink blue `#1f3a5f`, lines rotated -3 and +2 deg |
| 3 | Counter | "22" 260 px ink blue; "WAGONS" 110 px verdigris `#2e7d73` |
| 4 | Four stamps on white | 96 px (64 px for the two-line one), double rounded border, rotated -5, +4, +6, -3 deg. Left column proposed gold `#c9a227`; right column deep gold `#a8841c` |
| 5 | Source chip at the fixed corner, on plate NB05 | "HOMER, ODYSSEY 9", Special Elite 48 px, cream text on a verdigris pill, bottom-left, 60 px margins; plus "THE CAVE" place label in cream with ink outline |
| 6 | Bubble | "MY NAME IS NOBODY.", 64 px ink blue, thin 4 px curved tail to the mouth, no box |
| 7 | New palette, everything on one plate (NB01) | impact cream/ink, stamp deep gold on an 85% cream sticker halo, chip verdigris |
| 8 | Same as 7 in the old rust `#b8472a` (same fonts, so only colour differs) | the draft theme also used Fira Sans Condensed, which is not shown; this isolates the colour decision |
| 9 | Phone check | cells 7 and 5 at 480 px wide, 1:1 pixels |

## 3. Readability at 480 px wide (phone) [V]

Sizes at 1080p and what they become at 480 px (divide by 4):

| Element | 1080p size | at 480 px | Reads? |
|---|---|---|---|
| Impact word on plate | 170 px | 42 px | yes, easily |
| Impact word on white | 190 px | 48 px | yes |
| Counter number / unit | 260 / 110 px | 65 / 28 px | yes |
| Stamp text | 96 px | 24 px | yes; the border lines (9 px and 3 px) become 2 px and under 1 px, the inner line nearly disappears |
| Two-line stamp | 64 px | 16 px | yes, just |
| Source chip | 48 px | 12 px | yes, legible at a glance ("MAYOR, 2000", "HOMER, ODYSSEY 9"). At the first pass I used 40 px, which became 10 px and was guessable but not readable. 48 px is the floor; 52 would be safer for long chips |
| Bubble | 64 px | 16 px | yes for 3-4 words; an 8-word bubble at 64 px would run 1,000+ px wide, so bubbles should be 56-64 px and break into two lines after 4 words |

Minimum rule I propose for the bible: no label text under 48 px at 1080p; stamps at 96 px or larger; impact words 160-200 px.

## 4. Contrast findings [V, computed WCAG ratios]

| Colour | on white | on cream `#f3e9d2` | Note |
|---|---|---|---|
| ink blue `#1f3a5f` | 11.5 | 9.5 | strong; carries impact words and bubbles with no outline |
| verdigris `#2e7d73` | 4.9 | 4.1 | fine for unit words and place labels; cream text on a verdigris pill is 4.1, fine at 48 px |
| gold `#c9a227` (proposed) | 2.4 | 2.0 | **too weak** on white and on the Cyclops' olive skin: cell 4 left column looks faint, and in the first render the stamp vanished over the body |
| deep gold `#a8841c` | 3.5 | 2.9 | reads as "gold" and holds up; still needs the cream halo on busy plates |
| old rust `#b8472a` | 5.3 | 4.4 | reads better than either gold on its own; that is why cell 8 pops more than cell 7, and it is the colour we are leaving for originality |

So the three-colour idea works, but the stamp colour must be the deeper gold, and stamps on plates sit on a cream sticker halo (cell 7). On white, the stamp could alternatively be ink blue with the gold reserved for a REAL verdict only; not rendered, flagged as an option.

## 5. Clashes with the existing brand [V]

- **Avatar** (`brand/avatar_800.png`): navy `#081858` field, gold `#f2b632` ring and laurel, cream head, rust-and-blue tunic. Ink blue `#1f3a5f` is a near neighbour of that navy (contrast 1.4, so they read as the same family). Gold stamps echo the ring. No clash; the palette extends the avatar.
- **Banner** (`brand/banner_final_2560x1440.jpg`): dominant terracotta `#c85828`, which is within a hair of UF's rust `#b8472a` and of the draft accent we are dropping. The banner also uses black figures and cream serif type. So the channel banner currently wears the colour the FORMAT-BIBLE bans from the videos. Two options: accept it (the banner is a static page element, not video lettering, so the originality rule in section 9 does not strictly apply) or re-tint the banner field to the ink blue with gold line-art before launch. I recommend the re-tint, at low priority, so thumbnails, avatar and video share one family; it is a one-line change in `banner_r2.py`.
- **Odysseus cutout**: rust tunic with a blue sash and gold trim. Ink-blue impact words next to him pick up the sash; the tunic's rust is a costume colour, not lettering, and is fine.
- **Verdigris** has no relative anywhere in the brand yet. It is the one new note; it works because it only carries small elements (chips, unit words, place labels). If it feels foreign on the thumbnails, the fallback is to run chips in ink blue too and keep verdigris for maps only.

## 6. Recommendation [E]

Approve Permanent Marker for all hand lettering and Special Elite for chips; both are Apache 2.0 and already in the spike folder. Keep ink blue `#1f3a5f` as the accent and verdigris `#2e7d73` for chips and units exactly as proposed, but change the stamp gold from `#c9a227` to `#a8841c` and give any stamp placed over paint an 85% cream sticker halo, otherwise the signature stamp is the weakest element on screen. Fix the size floor at 48 px for chips and 96 px for stamps. The A/B in cells 7 and 8 is honest: the rust is punchier on these warm cave plates, so the blue palette buys originality at a small cost in pop, which the halo and the deeper gold recover. The one thing outside the videos to settle is the banner, which still wears the rust we are dropping.

## 7. Files written

- `video2/LOOK-G2.jpg`, `video2/LOOK-G2.phone480.jpg`, `video2/LOOK-G2.js`, `video2/LOOK-G2.md`
- `video2/spike/fonts/`: the two TTFs, two LICENSE texts, `fonts.conf`, and a `.cache/` fontconfig cache
- Nothing else touched. No uploads, no spend, no image-API calls.
