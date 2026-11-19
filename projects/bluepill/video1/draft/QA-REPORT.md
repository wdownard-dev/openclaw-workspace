# QA-REPORT.md: Video 1 private draft (2026-11-12)

Nothing uploaded, posted or sent. File: `video1/draft/video1_draft.mp4` (H.264 High, AAC 256 kb/s, 1920x1080, 30 fps). Source: `pipeline/remotion-v1/` (Remotion). I cannot judge motion feel or audio by ear; everything below is measured or seen in stills.

## Numbers
- **Runtime 10:12.80** (audio 612.77 s; video 612.80 s, 18,384 frames; duration matches). Step 0 trim took the timeline from 10:17.43 to 10:12.77 (chunk tails trimmed to 0.06 s after the last audible sound; paragraph gap about 0.41 s; the 2.0 s card windows and stings untouched). Backups in `video1/audio/v3_backup/`.
- **Render:** 1,279 s (21.3 min), 11 parallel tabs; file **318 MB** (3.9 Mb/s video). A first render at CRF 17 was 1.66 GB and was replaced.
- **Jerk/shake check** (Editor's `motion.js` run on the full encoded video, 83 picture shots, 320x180 estimator, px at 1080p; `qa/jerk_report.json`): per-shot jerk rms max **0.33 px**, mean 0.06 px; max shift 1.9 px per frame; clip-wide jerk rms outside +-0.2 s of every boundary **0.77 px**. Pass criteria (rms <= 2 px, no jump > 15 px outside cuts): pass for every picture shot. Six frames over 15 px (309.57, 489.0, 489.03, 599.73-599.8 s) are text-card reveals 0.25-0.3 s after a card starts, not camera movement. The single impact kick (shot 37, 8 px, 2.5 Hz, 0.25 s, x only) is the shot with the highest jerk, 0.33 px.
- **Loudness** (encoded mp4 audio, bundled-ffmpeg `loudnorm` measurement pass, since the build has no ebur128): **-16.16 LUFS integrated, true peak -1.20 dBFS, LRA 1.7 LU**. Parts: narration -16.15 LUFS, stings -25.1 LUFS (9.0 dB under the voice), bed -29.5 LUFS un-ducked reference / -35.2 LUFS as ducked. Details in `MUSIC.md`.

## Checks done
(a) 48 evenly spaced stills, 4 sheets: `qa/contact_sheet_1-4.jpg`. (b) Jerk check above. (c) Caption overlap on 15 stills (shots 5, 11, 20, 24, 26, 32, 34, 44, 48, 49, 52, 55, 67, 89, 104): no caption covers a face; captions touch foot, sandal or ground detail in shots 34, 44 and 104, and the boat rail in 55. (d) Every card, map and diagram (55 code shots, mid-shot and end-of-shot states) and 18 overlay picture shots passed a DOM text-extent check (nothing within 60 px of the sides, 50 px of the top or 40 px of the bottom). (e) Loudness above. (f) Stretch list: `qa/stretch_factors.json`.

## Defects found and fixed before the final render
1. White captions unreadable on the cream paper cards (2, 41, 42, 57, 61, 62): dark caption tone added.
2. Caption splits such as "Today we check what / is under it": chunk limit raised to 8 words, 50 characters.
3. Skull plate: "trunk opening" and comparison labels overlapped the skull outline, footnote ran into a tusk, stamp sat on the skull: relabelled outside the outline, footnote wrapped, stamp moved.
4. Shot 39 crop cut Odysseus' laurel: crop window moved up.
5. Scale chart (61): the 4 m elephant popped in cropped, its label ran off the left edge, "1.7 m" ran off the right, "under 1 m" label sat on the frame border (2, 62): layout and timing reworked, checked at six states.
6. "TURKEY" label clipped when the map pushes in (1, 84).
7. Shot 90 (Hesiod's names) showed an empty card for about 5 s: "names three Cyclopes" line added.
8. Measuring rod (72) was cream on cream bone: rust with dark halo.
9. Argolid map too tight (106): wider frame. Cyclops cutout on the Etna plate (98) too bright and large: darker, smaller.
10. Mix: the stings measured 1.5 dB under the voice in my first mix; reset to 9 dB under.
11. QA tooling bugs (ffmpeg build lacks fps, ebur128, rawvideo, compressor and limiter filters; overflow check first used the wrong DOM selector and found nothing): replaced with PNG-sequence extraction, loudnorm measurement, a Node compressor/limiter and `body *` with text ranges; all checks re-run.

## Remaining issues (not fixed)
- **Resolution stretch:** images are 1536x864, base fit is 1.25x. 39 of 83 picture shots exceed an effective 1.3x because of the B-shot crops the shot list asks for; worst: 7 (NB01 eye, 1.63x), 13 (NB02, 1.60x), 105 (NB24, 1.56x), 92 (NB22, 1.55x), 17 and 16 (NBG01, 1.52x, 1.47x), 35 (NB08, 1.52x), 30 (NB06, 1.50x), 54, 12, 27, 73, 129, 72 (1.44-1.47x). NB19 crops (68, 75, 82, 87, 130, 131) kept at 1.05-1.10 zoom, so the skull stays small. Expect softness on these; fresh generations or fewer B-crops would fix it.
- **NB14 (shot 47):** left 52% crop centred with smooth dark side bars built from its own edge colours (no blur). Clean but plain.
- **Cutouts:** only Odysseus (19, 109, 144), the Cyclops (98) and three dark Cyclops silhouettes (43, 45) are composited, plus the NP04 ship (50, 51, 144); no crew cutouts in 17-19, no Stage rim-light pass.
- **Shot 103** ("day-grade" of the night volcano) is a grey dawn tint, not a real day scene.
- **Paraphrase and caveats:** overlays on 69 and 82 are labelled PARAPHRASE (Witton and Hing remains second-hand, see RESEARCH-V1.md); Empedocles dates come from RESEARCH-V1.md C4; the "4 m" elephant is the same dwarf sprite enlarged (captioned so); skull is an original simplified vector illustration, labelled as such; the world-folktale markers are regional, not sites; Tilos is a dot (no polygon at 50 m).
- 14 shots are under 2.5 s (13, 15, 17, 29, 62, 64, 92, 106, 124, 128, 130, 135, 138, 142), unchanged from the retimed list.

## Watch first (time, shot)
- **Chapter cards** with the stings: 0:38.3 (I), 3:56.1 (II), 6:08.5 (III), 8:25.7 (IV), 9:32.1 (V); check the 12-frame crossfades and that each sting fades out before the first word.
- **Skull diagram:** 0:07.6, 0:21.7 (split with the Cyclops eye), 4:26.3-4:36.2 (ghost eyes, sockets, trunk opening), 8:42.7, 9:26.8 (HYPOTHESIS), 9:50.2 (SUSPECT).
- **Maps:** 0:00 Mediterranean push, 4:07.2 dwarf-elephant route, 6:46.8 Etna and Aeolian, 7:30.3 Argolid, 8:48.1 folktale markers and 200+ counter.
- **Blinding beat:** 2:24.0 (shot 37, the one 8 px kick, on "into the eye"), 2:34.4 Greek lower-third.
- **NB14:** 3:15.3 (side bars, slow push).
- **Scale chart zoom-out:** 4:17.3.
- **Quotes:** 5:12.6 (Mayor), 6:28.7 (Hesiod), 7:01 and 7:07 (Thucydides), 7:43 (Pausanias).
- **Ending:** 9:59.5 teaser, 10:04.1 suspects, 10:08.8 end card.
- By ear: voice level and limiter pumping, bed audibility (it is very quiet), caption timing against speech.
