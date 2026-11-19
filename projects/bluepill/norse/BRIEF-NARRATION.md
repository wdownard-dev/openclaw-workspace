# BRIEF-NARRATION: Norse narration (ElevenLabs, Daniel), recorded once

Worker: Sonnet, context cap 80k. Mechanical job: adapt the video 1 scripts, run them, check quality. No images. Do not read session history. Write only inside `projects/bluepill/norse/audio-n/` (create it). Spend: ElevenLabs credits only (about 7,800 characters; do not exceed 12,000 characters total including any re-record).

## Read
- `video2/audio-v5/scripts/plan.py`, `assemble.py`, `quality.py` and `video2/audio-v5/SPOKEN-TEXT.md` header (settings), `PROCESS.md` Stage 4. Copy the three scripts into `norse/audio-n/scripts/` and adapt paths; do not edit the originals.
- `norse/SCRIPT-N-LOCKED.md` (LOCKED; do not change a spoken word). Spoken text = the text after `**N-xxx**`, with `[CTA]` and `[PULL]` markers stripped. Beat ids keep their gaps (N-026, N-027 are cut on purpose).

## Voice (LOCKED, no auditions)
Daniel (premade), eleven_multilingual_v2, stability 0.5, similarity 0.75, style 0.2, speed 1.0, speaker boost on, no v4 tags, no phoneme tags. `ELEVENLABS_API_KEY` is in the environment.

## Steps
1. Build `plan.json`: passages by chapter (cold open, then the 7 chapters, per the chapter plan in the script header); beats and char counts per passage; `SPOKEN-TEXT.md` listing exactly what is sent (blank line = sentence break between beats; single space = continuation of a beat that starts lower-case).
2. Name respellings (TTS-only, unhyphenated where possible; record every one in SPOKEN-TEXT.md): propose from the V5 convention. Names to cover: Ymir, Audhumla, Vili and Ve, Yggdrasil, Mjolnir, Jormungandr, Hymir, Fenrir, Gleipnir, Baldr, Hod, Sigyn, Vidar, Naglfar, Surt, Garm, Heimdall, Gjallarhorn, Snorri Sturluson, Reykholt, Midgard, Asgard, Jotunheim, Ginnungagap, Hel, Muspell, Vigrid, Odin, Loki, Tyr, Thor, Frigg, Modi, Magni, Ragnarok, Mimir, Nidhogg, Ratatosk, Hermod, Thokk, Angrboda. Test only the names you are unsure of in ONE short test passage (under 400 chars) before the real run; listen via the word timestamps and a transcript check is not possible, so keep respellings simple and phonetic. Do not respell names Daniel already says right (Odin, Thor, Loki).
3. Record each passage with `/with-timestamps`, one call per passage, saving `passages/P*.json` and `.mp3`. Watch for "B.C.." double stops and years: write "twelve forty-one" etc. exactly as the script has them.
4. `assemble.py`: cap inside-beat pauses (0.35 / 0.25 / 0.20 s), target 150-155 wpm, voice-only master at -19 LUFS, 0 artefacts. Output `narration_voice_only.wav`, `.mp3`, `words.json`, `beats_timing.json` (start/end seconds per beat id), `quality.json`.
5. Report the runtime, wpm, per-chapter start times (these become the chapter timestamps), LUFS, artefact count, characters used, list of respellings, and any passage you re-recorded and why (a re-record is a process failure; justify it).

## Final message (max 8 lines)
Runtime, wpm, characters used, chapter start times, quality result, respellings, open issues. Do not send the audio anywhere; the parent will.
