# SOUNDS.md - Blue Pill v2 upgrade test (Cyclops)

Every audio asset in this render is either synthesised in code by `synth.js` (own work, no samples, no third-party audio, dedicated CC0 / public domain, free for commercial use) or is the ElevenLabs narration. Nothing was downloaded. I cannot judge audio quality; see "Not verified".

## Files

| File | Source | Licence |
|---|---|---|
| public/sfx/whoosh.wav | `synth.js`: noise through a bandpass swept 250 to 3450 Hz and back | own work, CC0 |
| public/sfx/thud.wav | `synth.js`: sine dropping 155 to 45 Hz plus low noise burst | own work, CC0 |
| public/sfx/pop.wav | `synth.js`: pitch-falling blip with click | own work, CC0 |
| public/sfx/tick.wav | `synth.js`: 2.4 kHz click (generated, not used in this cut) | own work, CC0 |
| public/sfx/ding.wav | `synth.js`: three inharmonic sine partials, glass bell | own work, CC0 |
| public/sfx/scrape.wav | `synth.js`: filtered noise with a 3.2 Hz stroke rhythm | own work, CC0 |
| public/sfx/rumble.wav | `synth.js`: lowpassed brown noise with wobble | own work, CC0 |
| public/sfx/thunder.wav | `synth.js`: brown-noise roll plus crack | own work, CC0 |
| public/sfx/sting.wav | `synth.js`: A-minor add9 bell chord plus drum and shimmer swell (chapter sting) | own work, CC0 |
| public/music/bed.wav | `synth.js`: 84 s A-minor pad (Am F C G, 64 bpm), bass, sparse plucks, soft frame drum, echo | own work, CC0 |
| public/vo/vo_0..8.mp3 | ElevenLabs `eleven_multilingual_v2`, voice JBFqnCBsd6RMkjVDRZzb (same voice and settings as the proof), one call per paragraph via `make_audio.py` | ElevenLabs commercial terms of William's plan; check the plan's licence before publishing [U] |

Fonts (visual, listed for completeness): Bangers (SIL OFL 1.1, Google Fonts, Vernon Adams) for impact words and titles; Lilita One (SIL OFL 1.1, Google Fonts, Juan Montoreano) for captions and labels. Both free for commercial use.

## Mix

- Narration volume 1.0. Music bed volume 0.34, ducked to 0.12 whenever any narration is within 0.15 s before / 0.3 s after, with a 0.45 s ramp; 2 s fade in (baked into the file) and 2.5 s fade out at the end. Measured on the final mix: peak -0.6 dBFS (hot, from the thud/sting peaks; lower SFX volumes if it clips on a platform), voice seconds sit around -24 to -27 dB RMS.

## Cue list (absolute time in out.mp4; word-driven cues are glued to the narration timing in data/timing.json)

| Time | Cue | Where |
|---|---|---|
| 2.00 | thud (0.8) | hook, "SIX" impact word slams in |
| 3.78 | sting (0.75) | chapter card "THE CYCLOPS" |
| 6.18 | whoosh (0.55 + 0.35) | whip transition into the map |
| 10.03 | whoosh (0.55) | whip into the cave |
| 13.78 | pop (0.7) | sheep pops in ("sheep") |
| 17.34 | thud (0.8) | "MISTAKE" impact word |
| 19.23 | whoosh (0.5) | Cyclops starts to run in |
| 19.76 | thud (0.9) | Cyclops lands, camera shake |
| 22.82 | rumble (0.7) | boulder starts rolling |
| 23.92 | thud (1.0) | boulder lands, camera shake, light dims |
| 27.78 | whoosh (0.55) | whip into the wine shot |
| 29.84 | ding (0.7) | wine cup appears |
| 37.58 | pop (0.8) | "NOBODY" impact word |
| 40.61 | thud (0.6) | Cyclops tips over asleep |
| 43.04 | scrape (0.6) | stake being sharpened |
| 46.93 | thud (0.8) | "BLIND!" impact word (white flash cut at 45.94) |
| 51.58 | whoosh (0.55) | whip to dawn |
| 59.18 | whoosh (0.6) | ship sails in ("The plan works") |
| 63.93 | pop (0.8) | "ODYSSEUS!" impact word |
| 65.80 / 68.00 | thunder (0.8 / 0.65) | storm shot, with white lightning flashes |
| 65.87 | thud (0.8) | "PRIDE" impact word |
| 69.71 | whoosh (0.3) | fade into end card |
| 70.01 | thud (0.8) | end card title |
| 71.11 / 73.61 | thunder (0.7 / 0.6) | end card lightning |
| 72.31 | pop (0.6) | subscribe pill pops |
| 0 to 76.5 | music bed, ducked under voice | whole video |

## Not verified
I cannot hear audio. Checked only: files exist, the mix decodes, no silent gaps over a second (per-second RMS of the final mix never drops below -37 dB), peak -0.6 dBFS. Whether the synthesised music is pleasant, whether the whooshes and thuds sound cheap, and whether the levels balance are all unjudged: a human has to listen. If the synthesised music or SFX do not pass, swap in free-licence tracks (YouTube Audio Library, Pixabay) and record each licence here.
