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
YouTube upload via existing Google OAuth (needs the new channel's OAuth). Buffer key exists for Shorts scheduling [V]. Log CSV per video.

## Accounts William must create/approve
1. Image API key: OpenAI chosen, William adding it (pending)
2. ElevenLabs key (after voice test)
3. New Google/YouTube account for the channel
