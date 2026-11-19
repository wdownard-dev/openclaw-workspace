# Blue Pill tool stack (checked 2026-11-11)

Labels: [V] verified on this machine/docs today, [U] unverified, [E] estimate.

## Already have
- Claude (scripts, storyboards, accuracy pass), OpenClaw agents/subagents [V]
- YouTube Data API key + Google OAuth (research, later upload) [V]
- Node 24, Python 3.12, 12 cores, 23 GB RAM, 382 GB free disk, no GPU [V]
- OpenClaw image_generate, video_generate, music_generate, tts tools exist, but need a provider key [V docs]
- ImageMagick libs and librsvg installed (SVG to PNG) [V]

## Missing today
- No image-generation key. OpenClaw lists OpenAI as "configured" but there is no OpenAI auth profile, so I don't trust it. [V]
- No ElevenLabs key [V]
- No system ffmpeg, no sudo. Remotion ships its own ffmpeg through npm, so this is fine. [U until tested]
- No yt-dlp in Python (it was run another way earlier)

## Backgrounds
Possible, no outsourcing to a person or an app. Use an image API through image_generate.
Candidates (OpenClaw supports all): Google Gemini image (gemini-3.1-flash-image), OpenAI gpt-image-2 / 2.5, fal (Flux, Krea 2, GPT image, Nano Banana), OpenRouter (one key, several models).
Consistency method: generate 1 locked style-reference image, pass it as a reference (Gemini/OpenAI accept up to 5, fal GPT 2.5 up to 16) with every background prompt. Fixed style paragraph in every prompt.
Needs a key: pick one provider. Price per image [E]: about $0.02-0.15 depending on model and quality. Test 20 images before choosing.

## Characters
Round heads, dot eyes, simple bodies are better built as code (SVG parts: head, 6 expressions, pose set, costume colours) than generated. Zero cost, zero drift, easy pose swaps. Use image models only for rare complex figures (monsters, gods) in the same flat style.

## Voice
ElevenLabs (plan in PLAN.md). Alternatives to price: OpenAI TTS, Google TTS via OpenClaw tts tool. Narrator must sound human; test 3 voices on one script paragraph before paying for a plan.

## Captions / timing
Whisper (local whisper.cpp through Remotion, or API) for word timestamps. Local is free; 12 CPU cores is enough for 12 min of audio. [U]

## Assembly
Remotion (React, code-driven), plus remotion-superpowers as the base. Licence for commercial use to confirm. [U]

## Music / SFX
Free-licence libraries (YouTube Audio Library, Pixabay, Freesound with attribution rules). OpenClaw music_generate is an option once a provider exists. Check licence per track.

## Maps / arrows / title cards
Built in Remotion with SVG (route arrows, labels, counters, hand-lettered font that is free for commercial use, e.g. from Google Fonts).

## Thumbnails
Same character kit plus generated scene background, composited with Remotion or ImageMagick. Own layout, not Unknown Frequencies' template.

## Publish / track
YouTube upload via Google OAuth for The Myth Ledger: refresh token secret GOOGLE_OAUTH_REFRESH_TOKEN_MYTHLEDGER (client morpheus-yt; do NOT use GOOGLE_OAUTH_REFRESH_TOKEN, that is wrdclipz) [V 2026-11-12]. Always set privacyStatus explicitly (private first). Buffer key exists for Shorts scheduling [V]. Log CSV per video.

## Accounts William must create/approve
1. Image API key: DONE 2026-11-12. OPENAI_API_KEY stored in the protected store (host api.openai.com), $25 API credit added. Key verified (models call 200, gpt-image-2 listed). First test image: tests/palace_hall_gpt-image-2_medium.png (1536x1024, medium, about 1,400 output tokens). Note: the exec env var is an opaque sentinel; call the API with curl via exec, image_generate may not see this key (no auth profile).
2. ElevenLabs key (after voice test)
3. New Google/YouTube account for the channel

## Background test, round 1 (2026-11-12) [V]
20 images, 1536x1024, quality medium, same flat-illustration style paragraph (bg_test.py, tests/round1/, results.json). All 20 succeeded.
- gpt-image-2: darkest and most realistic, 1,372 output tokens, about 28 s each. Weakest fit for the flat explainer look.
- gpt-image-2.6-flare: fast (7-9 s), brighter, flatter, 1,132 tokens. Good fit, slightly busier.
- gpt-image-2.6-sunburst: flattest and most illustrated, closest to the target look, 1,132 tokens, about 31-42 s. Best fit so far.
- Observed quirk: a prompted "no text" held on all samples seen; ship hull had a decorative eye motif. Not yet checked: map_table, norse_hall, underworld, egypt_temple, troy_walls.
- Dollar cost per image NOT yet known: check platform.openai.com usage after this batch (21 images, 12 images 2.6, 9 images gpt-image-2).

## Round 2 (2026-11-12) [V]
Rendering: sharp (npm, in pipeline/) renders SVG and composites; no sudo or system tools needed. pipeline/character.js builds test character "Pip" (placeholder name, original design) with 4 expressions x 3 poses. pipeline/composite.js overlays Pip and a yellow caption on generated backgrounds.
- Code character composited on a generated background works and is free, but looks pasted on (floating feet, no shared lighting, crude stick limbs). Needs better art direction, shadows, and a more designed character before it reaches Unknown Frequencies level.
- Reference-edit (images/edits, gpt-image-2.6-sunburst, Pip PNG as image[]): the model kept Pip identical (head, eyes, tunic, belt, outline) and redrew the whole scene in matching flat style, with Pip well integrated. Tested 3 scenes (cave, Egyptian temple, Viking hall), 3 of 3 held. Pose stays as the reference, so keep a pose library and pass the right pose per shot. Not yet tested: two characters in one shot, 20+ shots in a row, drift over many generations.
- Map: clean parchment map of Greece/Turkey/Crete with large empty sea, no text, good for route arrows drawn in Remotion. Land colours would need checking for historical accuracy; coastlines are approximate.
- 4 images this round, about 0.14 USD at the 0.035-0.041 per image estimate.

## Characters (2026-11-12) [V]
Direction chosen by William: story characters only, narrated by voice-over, no host. Style: round plain white head, dot eyes, tiny smile, stubby white body, thick dark outline, flat colours (tests/characters/01_round_hero.png is the style anchor). Cast test in tests/characters3/: Zeus, Athena, Cyclops, Medusa generated from the anchor via images/edits (gpt-image-2.6-sunburst) and all matched the style. Two-character scenes (hero+Cyclops in cave, Zeus+Athena on Olympus) kept both characters identical and showed expressions (sweat drop, crossed arms) unprompted by the reference. Scripts: char_cast.sh (new character from style ref), char_restyle.sh (restyle an existing design), pipeline/contact*.js (contact sheets). A prompt asking for a "1930s rubber hose" style was rejected by OpenAI's safety filter: avoid naming real cartoon eras or franchises.
Open: expression and pose sets, drift over many generations, giving the same character a different pose (needs a pose library or a prompt per shot), fake-looking "white skin" is a style choice (all characters share it, which also avoids depicting real ethnicities).

## Real costs (2026-11-12, from OpenAI usage page) [V]
Dashboard lags (showed 37 requests and 1.58 USD when about 46 requests had been sent), so treat totals as lower bounds.
- Output pricing works out to 30 USD per million image tokens: gpt-image-2.6-flare 6 images = 0.204 USD (0.034 each, 1,132 tokens); gpt-image-2 1 image = 0.041 USD (1,372 tokens).
- gpt-image-2.6 at 1536x1024 medium: about 0.034 USD per image. gpt-image-2: about 0.041 USD.
- Reference edits add an image-input charge: about 0.007 USD per edit call (sunburst image input 0.115 USD over about 16 edits), so an edit shot is about 0.04 USD.
- Per video estimate: 100-150 shots at 0.034-0.041 = 3.40-6.15 USD, about 4.50-8 USD with 30% retries. Library reuse and quality=low drafts could cut it (quality=low untested).
- Credit added 25 USD; spent about 2 USD so far.

## Storyboard and cutout tests (2026-11-12) [V]
- tests/storyboard/: 6-shot Cyclops sequence from two reference characters (hero + Cyclops), 6 of 6 held both characters and read the beat. Flaw: continuity logic, the Cyclops kept his eye in the "blind" escape shot, so each shot prompt must state story state explicitly. Companions rendered as silhouettes.
- pipeline/cutout.js: free flood-fill background removal works because the dark outline stops the fill; heads stay opaque, no halo seen. tests/cutouts/demo_olympus_cast.png places 4 cutouts on one background. Cutouts allow pan, zoom and repositioning in Remotion without regenerating.

## ElevenLabs (2026-11-12) [V]
ELEVENLABS_API_KEY stored in the protected store (host api.elevenlabs.io). Account on Creator tier, active, character_limit 131,000 per period (the plan card said 121k). API works with this key: subscription and voices endpoints 200, text-to-speech 200. 21 premade voices listed. First voice test in tests/voice/ (george, brian, liam, callum), eleven_multilingual_v2, stability 0.5, similarity 0.75, style 0.2, about 510 characters each. Usage counter showed 0 right after the calls (lags like OpenAI).

## Voice decision (2026-11-12)
Narrator voice: George (JBFqnCBsd6RMkjVDRZzb), warm captivating British storyteller, chosen by William. Model eleven_multilingual_v2, stability 0.5, similarity 0.75, style 0.2 as starting settings. ElevenLabs has /with-timestamps endpoint for character-level alignment, which can drive captions without Whisper.

## Remotion proof (2026-11-12) [V]
Licence: Remotion is free for individuals and teams of up to 3 people, all features, unlimited commercial use, automation (renderMedia, CLI) included; Company licence needed only beyond that (remotion.dev/docs/license/pricing, faq fetched today). Not allowed: reselling Remotion itself.
Pipeline in pipeline/remotion-proof/: make_audio.py (George TTS with /with-timestamps, writes public/narration.mp3 and data/timing.json with per-word and per-shot times), src/Proof.tsx (Ken Burns on each shot, crossfades, word-highlight captions, audio), render with `npx remotion render src/index.ts Proof16x9 out.mp4 --concurrency=6`. Works on this machine with no sudo: 54.7 s, 1920x1080, 30 fps, 1,642 frames, rendered in under 5 minutes, 25.7 MB. Output copied to tests/proof/ (proof_16x9.mp4, proof_720p.mp4, proof_frames.jpg).
Known gaps: captions sit over the characters in the lower third on some shots (need smaller captions or per-shot placement); no music or SFX yet; 9:16 needs 2:3 generated frames because 3:2 images crop to a third of the width; character cutouts not used in the proof yet; per-shot camera moves are fixed presets, not tied to the action.
Caption fix (v2): the original captions used a sliding 5-word window that re-flowed and wrapped on every word, worst on long unpunctuated runs ("for the rest of the journey home"). Now chunks are fixed up front (max 3 words, break at punctuation), single line, thicker stroke. Left over: a highlight can overlap two adjacent words for about 0.1 s, and one-word chunks appear after punctuation ("NAME", "HOME"). tests/proof/proof_v2_720p.mp4.
