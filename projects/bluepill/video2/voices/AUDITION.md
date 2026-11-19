# AUDITION.md: voice exploration for video 1 (The Myth Ledger), 2026-11-13

**I cannot hear any of these clips.** Every pick below comes from voice metadata and measurements. William's ears decide. Nothing was uploaded, posted or sent; only audition lines were generated (no full script).

**Listen in this order:** `reel_narrators.mp3` (5:51: slate, then clip; every clip is level-matched to -19 LUFS so loudness does not bias you; slates are spoken by one fixed voice, River) and `reel_characters.mp3` (3:15, by role). The files in `narrators/` and `characters/` are raw, un-normalised.

**Reference traits** (REVIEW-ref-vs-draft section 4): pace 178 wpm overall, pitch spread 4.7 semitones, loudness range 3.6 LU, 1.9 pauses of 0.3 s or more per minute, performed voices for characters. Our V1 George take: 155 wpm, 2.9 st, 1.7 LU. Measurement method: the reference teardown's own F0 code (autocorrelation, std of voiced F0 in semitones), ported to numpy; LUFS/LRA from ffmpeg ebur128. Caveat: 8-24 second clips, one take each. Pitch spread and LRA wobble by a semitone or a couple of LU between takes of the same voice, and the pace falls as the text gets longer (see N09: 164 wpm on the short clip, 135 on the long). Read the numbers as hints.

## Narrator clips (`narrators/`)
First pass: 143 characters (beats 01 + 11), eleven_multilingual_v2, stability 0.5, style 0.2, boost on, speed 1.0. Spoken slate in the reel = the N number.

| # | file | voice: description [labels] (licence) | s | wpm | pitch st | LUFS / LRA |
|---|---|---|---|---|---|---|
| N01 | `narrators/N01_George.mp3` | **George**: Warm resonance that instantly captivates listeners. [british, middle_aged, mature, narrative_story] (premade, no owner notice) | 9.24 | 182 | 3.01 | -22.9 / 2.2 |
| N02 | `narrators/N02_Daniel.mp3` | **Daniel**: A strong voice perfect for delivering a professional broadcast or news story. [british, middle_aged, formal, informative_educational] (premade, no owner notice) | 10.63 | 158 | 3.43 | -23.6 / 1.4 |
| N03 | `narrators/N03_OliverSilk.mp3` | **OliverSilk**: Deep British RP. Optimized for sarcasm and intimate narration. Perfect for corporate, documentaries, and  [british, middle_aged, deep, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 9.43 | 178 | 2.65 | -22.9 / 1.7 |
| N04 | `narrators/N04_MichaelDan.mp3` | **MichaelDan**: A warm, mature British male narrator with clear diction, natural pacing, and steady authority. Well-suite [british, middle_aged, casual, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 11.01 | 153 | 3.21 | -20.9 / 2.0 |
| N05 | `narrators/N05_NathanielC.mp3` | **NathanielC**: Nathaniel C brings a perfect balance of natural flow, dramatic intensity, and a pleasant tone.   (Recomme [british, middle_aged, classy, entertainment_tv] (library, rate 1, owner notice 730 d, live-moderation off) | 11.05 | 152 | 4.29 | -25.7 / 2.5 |
| N06 | `narrators/N06_StephenDavis.mp3` | **StephenDavis**: A British male voice with a mostly upbeat, witty, and subtly sarcastic delivery. [british, middle_aged, casual, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 7.76 | 217 | 4.56 | -26.7 / 5.2 |
| N07 | `narrators/N07_Russell.mp3` | **Russell**: Fast paced, deep & serious British Documentary Narrator for dramatic subjects. For TV, News, Radio, YouTu [british, middle_aged, serious, entertainment_tv] (library, rate 1, owner notice 730 d, live-moderation off) | 9.29 | 181 | 5.02 | -15.4 / 4.6 |
| N08 | `narrators/N08_HeyItsBrad.mp3` | **HeyItsBrad**: Confident. Casual. Rock ’n’ roll, edgy young vibe. Reality TV. Music and pop culture news. Indie film nar [american, middle_aged, casual, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 10.63 | 158 | 3.27 | -21.3 / 3.5 |
| N09 | `narrators/N09_SpudsOxley.mp3` | **SpudsOxley**: A friendly Southern grandpa who knows how to enthrall his audience with tall tales and fun adventures! A  [american, old, gentle, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 10.22 | 164 | 4.66 | -23.3 / 3.6 |
| N10 | `narrators/N10_LiamCallahan.mp3` | **LiamCallahan**: Gruff middle-aged podcaster, perfect for reading out fantasies, YouTube shorts, or any other project. [american, middle_aged, confident, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 7.76 | 217 | 3.72 | -34.4 / 1.8 |
| N11 | `narrators/N11_JarnathanCross.mp3` | **JarnathanCross**: Effortless certainty, assurance, calm control and a knowing edge. [american, middle_aged, professional, conversational] (library, rate 1, owner notice 730 d, live-moderation off) | 8.08 | 208 | 4.34 | -25.2 / 1.1 |
| N12 | `narrators/N12_Kurt.mp3` | **Kurt**: Wry but likable. Genuine and candid, with a little edge when it's called for. A youngish American male wh [american, young, casual, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 9.06 | 186 | 1.97 | -18.8 / 6.6 |
| N13 | `narrators/N13_AlexSouthern.mp3` | **AlexSouthern**: Soft medium tenor with Southern tendencies. [us southern, middle_aged, gentle, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 9.66 | 174 | 2.46 | -20.6 / 2.4 |

Longer script (266 characters, beats 01, 02, 08, 11), same settings, top 4 by closeness to the reference plus N03 as the dry-British entry:

| # | file | voice: description [labels] (licence) | s | wpm | pitch st | LUFS / LRA |
|---|---|---|---|---|---|---|
| N03L | `narrators/N03L_OliverSilk.mp3` | **OliverSilk**: Deep British RP. Optimized for sarcasm and intimate narration. Perfect for corporate, documentaries, and  [british, middle_aged, deep, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 21.69 | 147 | 3.42 | -26.3 / 5.0 |
| N05L | `narrators/N05L_NathanielC.mp3` | **NathanielC**: Nathaniel C brings a perfect balance of natural flow, dramatic intensity, and a pleasant tone.   (Recomme [british, middle_aged, classy, entertainment_tv] (library, rate 1, owner notice 730 d, live-moderation off) | 20.71 | 154 | 3.62 | -25.8 / 3.1 |
| N07L | `narrators/N07L_Russell.mp3` | **Russell**: Fast paced, deep & serious British Documentary Narrator for dramatic subjects. For TV, News, Radio, YouTu [british, middle_aged, serious, entertainment_tv] (library, rate 1, owner notice 730 d, live-moderation off) | 19.04 | 167 | 3.56 | -17.0 / 2.6 |
| N08L | `narrators/N08L_HeyItsBrad.mp3` | **HeyItsBrad**: Confident. Casual. Rock ’n’ roll, edgy young vibe. Reality TV. Music and pop culture news. Indie film nar [american, middle_aged, casual, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 21.92 | 145 | 3.28 | -19.5 / 2.9 |
| N09L | `narrators/N09L_SpudsOxley.mp3` | **SpudsOxley**: A friendly Southern grandpa who knows how to enthrall his audience with tall tales and fun adventures! A  [american, old, gentle, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 23.59 | 135 | 3.59 | -24.4 / 3.1 |
| N09 V1 | `narrators/N09L_SpudsOxley_set-V1-0.75-0.05.mp3` | **SpudsOxley**: A friendly Southern grandpa who knows how to enthrall his audience with tall tales and fun adventures! A  [american, old, gentle, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) **settings V1 0.75 / 0.05** | 22.57 | 141 | 5.33 | -23.8 / 5.9 |
| N09 act | `narrators/N09L_SpudsOxley_set-act-0.4-0.3.mp3` | **SpudsOxley**: A friendly Southern grandpa who knows how to enthrall his audience with tall tales and fun adventures! A  [american, old, gentle, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) **settings 0.4 / 0.3** | 21.87 | 145 | 5.11 | -24.3 / 5.5 |

Model side test (Eleven v4 with an audio tag, 195 characters incl. tag; the tag text should not be spoken, I cannot confirm that by ear):

| # | file | voice: description [labels] (licence) | s | wpm | pitch st | LUFS / LRA |
|---|---|---|---|---|---|---|
| N01 v4 | `narrators/N01_George_model-eleven_v4-tag.mp3` | **George**: Warm resonance that instantly captivates listeners. [british, middle_aged, mature, narrative_story] (premade, no owner notice) **eleven_v4, `[dry, deadpan, amused documentary narrator]`** | 10.16 | 165 | 4.37 | -24.0 / 4.9 |
| N09 v4 | `narrators/N09_SpudsOxley_model-eleven_v4-tag.mp3` | **SpudsOxley**: A friendly Southern grandpa who knows how to enthrall his audience with tall tales and fun adventures! A  [american, old, gentle, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) **eleven_v4, `[dry, deadpan, amused documentary narrator]`** | 11.12 | 151 | 5.6 | -24.0 / 5.1 |

| O01 | `narrators/O01_OpenAI-gpt-4o-mini-tts_onyx.mp3` | OpenAI gpt-4o-mini-tts, voice onyx, instruction 'dry, amused documentary narrator' (12 words only; not in the reel) | 5.35 | 135 | 2.72 | -25.1 / 3.5 |

## Character clips (`characters/`)
Same lines as the Nobody exchange and neighbours (beats 28-33, 37, 39, 44 and a few one-liners), 144-217 characters, stability 0.4, style 0.3, boost on, speed 1.0. In the reel the spoken slate gives the role and the candidate number within the role (Odysseus one = C01, Polyphemus two = C05, and so on).

| # | file | voice: description [labels] (licence) | s | wpm | pitch st | LUFS / LRA |
|---|---|---|---|---|---|---|
| C01 | `characters/C01_ODY_DanielWarmBaritone.mp3` | **ODY DanielWarmBaritone**: A low-to-mid baritone with a warm, slightly gravelly tone. Daniel speaks quickly, in short bursts, and yo [american, young, confident, informative_educational] (library, rate 1, owner notice 730 d, live-moderation off) | 10.5 | 189 | 1.99 | -19.1 / 1.8 |
| C02 | `characters/C02_ODY_JustinTrustingCalm.mp3` | **ODY JustinTrustingCalm**: Deep, warm baritone with a calm, conversational delivery. Naturally low-pitched and steady, with a dry, u [american, young, deep, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 11.38 | 174 | 5.9 | -23.1 / 2.4 |
| C03 | `characters/C03_ODY_RyanUnhurried.mp3` | **ODY RyanUnhurried**: Smooth, effortlessly cool, and brimming with dry wit—this voice delivers a uniquely disaffected charm tha [american, young, calm, conversational] (library, rate 1, owner notice 730 d, live-moderation off) | 15.46 | 128 | 3.93 | -20.4 / 4.4 |
| C04 | `characters/C04_POLY_MichaelMoody.mp3` | **POLY MichaelMoody**: Listening to Michael’s voice is like coming home to grandpas house after a long absence.  His voice is ri [american, old, wise, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 21.83 | 115 | 6.75 | -22.8 / 4.8 |
| C05 | `characters/C05_POLY_PhilipQuietAuthority.mp3` | **POLY PhilipQuietAuthority**: Deep, commanding American baritone with real weight behind it — slow, deliberate, impossible to ignore. P [american, middle_aged, deep, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 14.35 | 176 | 2.65 | -19.0 / 3.1 |
| C06 | `characters/C06_POLY_UjjalSleepy.mp3` | **POLY UjjalSleepy**: Deep, warm male voice with a naturally sleepy, soothing quality. Smooth bass-baritone tone with a slow, c [american, young, calm, narrative_story] (library, rate 1, owner notice 730 d, live-moderation off) | 20.34 | 124 | 4.16 | -36.3 / 5.4 |
| C07 | `characters/C07_CYC2_DrewDeadpan.mp3` | **CYC2 DrewDeadpan**: American male voice. Deadpan delivery, sarcasm, vocal fry. Perfect for satirical TikTok, Reels, or YouTub [american, middle_aged, casual, social_media] (library, rate 1, owner notice 730 d, live-moderation off) | 13.7 | 127 | 3.38 | -18.2 / 2.7 |
| C08 | `characters/C08_CYC2_DannyMonotone.mp3` | **CYC2 DannyMonotone**: Middle-age, quirky, Midwestern male voice. Great for Storytelling. [american, middle_aged, relaxed, narrative_story] (library, rate 1, owner notice None d, live-moderation off) | 11.42 | 152 | 5.86 | -18.1 / 3.3 |
| C09 | `characters/C09_CYC2_DeadpanCynic.mp3` | **CYC2 DeadpanCynic**: Low-energy fatalist delivery with a distinctive speech pattern that makes every line more pathetic and fu [american, middle_aged, sad, characters_animation] (library, rate 1, owner notice 365 d, live-moderation off) | 12.96 | 134 | 6.82 | -23.0 / 3.5 |
| C10 | `characters/C10_CREW_HarryAnxiousFighter.mp3` | **CREW HarryAnxiousFighter**: An animated warrior ready to charge forward. [american, young, rough, characters_animation] (premade, no owner notice) | 11.61 | 134 | 3.6 | -22.2 / 3.7 |
| C11 | `characters/C11_CREW_LukasExcitedYouth.mp3` | **CREW LukasExcitedYouth**: Young man with a lot of passion and excitement in tone, happy, hopeful and confident. Good for characters [american, young, excited, characters_animation] (library, rate 1, owner notice 730 d, live-moderation off) | 9.1 | 171 | 4.97 | -20.2 / 2.0 |
| C12 | `characters/C12_CREW_TimmyAnxiousNerd.mp3` | **CREW TimmyAnxiousNerd**: A lovable nerdy voice with nasal tone, shy energy, stutters, and funny rambling delivery. Perfect for Soc [american, young, anxious, characters_animation] (library, rate 1, owner notice 730 d, live-moderation off) | 8.41 | 186 | 2.8 | -24.7 / 5.4 |

## My hints (metadata and measurements only)
**Narrator, listen to these three first:**
1. **N09 Spuds Oxley** (warm Southern storyteller). Closest on the short clip (164 wpm, 4.7 st, 3.6 LU against 178 / 4.7 / 3.6). Slow on the long clip (135 wpm), so it needs speed 1.1. Risk: a stylised grandfatherly baritone may read folksy, not dry.
2. **N07 Russell** (fast, deep, serious British TV documentary). Closest pace on both takes (181 and 167 wpm), widest spread on the short clip (5.0 st). Mastered hot (-15 to -17 LUFS, peak -0.9 dB). Risk: too serious for the jokes.
3. **N05 Nathaniel C** (British character actor and comedian, documentary). 4.3 and 3.6 st, 2.5 and 3.1 LU. Slower (152 wpm). Best metadata match for deadpan comic timing.

Also worth a listen: **N03 Oliver Silk** (described as "optimised for sarcasm"; measures flat, 2.7-3.4 st, very low at about 85 Hz) as the dry-British entry, and **N01 George with Eleven v4 plus a style tag**. v4 + tag moved both test voices the same way: George 3.0 to 4.4 st and 2.2 to 4.9 LU, Spuds 4.7 to 5.6 st and 3.6 to 5.1 LU. That keeps William's chosen voice and moves toward the reference measures.
**Settings:** the N09 ladder (0.75/0.05 V1, 0.5/0.2, 0.4/0.3) does not move the numbers in order (5.3, 3.6, 5.1 st), so it is noise at n=1; judge by ear. **Pace:** at speed 1.0 the long takes run 135-167 wpm, V1 George was 155 at speed 0.9, the reference is 178. Try speed 1.1-1.15.

**Per role** (target pace for Polyphemus about 140 wpm): **ODY** C02 Justin (deep warm baritone, "dry understated humour", 5.9 st), then C01 Daniel (warm gravelly baritone, flatter at 2.0 st, hot peak). C03 Ryan is too high (167 Hz) and slow. **POLY** C06 Ujjal (bass-baritone, sleepy, 126 wpm; raw file is -36 LUFS, so judge it in the reel), then C04 Michael Moody (warm velvety grandfather, 116 wpm). C05 Philip is too fast (176 wpm) and flat for "slow and gentle". **CYC2** C07 Drew (deadpan, 3.4 st, 130 wpm). C08 Danny's 5.9 st rests on 64 voiced frames, so it is unreliable; C09's lisp and 6.8 st read as expressive, not bored. **CREW** C11 Lukas (mid-high 182 Hz, fast, "passionate, hopeful"), then C10 Harry (205 Hz, "excited but slightly anxious", a premade voice with no withdrawal risk). C12 Timmy's description includes stutters and may over-act.

## Licence and plan notes
- Creator tier includes the commercial licence (pricing page, fetched today [E]). Shared-library voices can be added to My Voices through the API at no character cost and then used for TTS [V: 22 added, add endpoint 200, TTS 200]. They occupy voice slots: **22 of 30 used** (add counter 0 of 95). Remove the ones William does not pick with `DELETE /v1/voices/{id}`; all are named `BP <name> (audition)`.
- **Owner withdrawal:** library voices carry an owner "notice period" (730 days for most picks, 365 for DeadpanCynic, none listed for Danny). A withdrawn voice cannot reproduce later videos, so record all of a voice's lines in one session and archive the audio. Premade voices (George, Daniel, Harry) have no such risk.
- I excluded voices with a credit surcharge (rate 2 or 3) and voices with live moderation on (could block the Cyclops violence). Per-voice licence text beyond the platform terms: not read [U].
- Library voices flagged paid-plan-only (Ujjal, Justin, Kurt, Jarnathan, Alex) work on Creator. No other blocker found.

## Alternatives to ElevenLabs (nothing signed up for)
| Option | Steerable acting | Commercial use | Price | Status |
|---|---|---|---|---|
| OpenAI gpt-4o-mini-tts | free-text `instructions` | OpenAI terms; AI-voice disclosure rule [U] | $0.60/1M text tokens + $12/1M audio tokens (about $0.015/min, roughly $0.017 per 1,000 characters at 15 characters/s) | [V] call worked with the existing key, HTTP 200, 5.35 s; [E] price from the pricing page. No custom voices; 13 built-in voices. |
| Cartesia Sonic | speed/emotion controls [U] | [U] | 1 credit per character; paid from $5/month; overage $38-65 per 1M credits | [E] pricing page |
| Fish Audio (s2.1-pro, drama-3) | inline emotion tags [U] | API licence [U] | $15 per 1M UTF-8 bytes (about $0.015 per 1,000 characters); drama-3 $50/M ($10/M promo to 30 Nov 2026) | [E] docs |
| Google (Gemini TTS, Chirp 3 HD) | prompt-style control [U] | [U] | pricing page fetch failed | [U] |
| Hume Octave, PlayHT | [U] | [U] | not retrievable this session | [U] |

## Cost report
- **ElevenLabs characters generated:** 6,651 across 71 calls: first-pass narrators 1,859, long narrators 1,330, settings variants 532, v4 test 390, characters 2,064, slates 476. At the Creator rate ($22 for 121,000 credits, $0.182 per 1,000) that is about **$1.21** of plan value. The calls drew on the existing quota, so there is no extra charge.
- **Quota:** before 10,008 of 131,000 (read at start). After: the counter shows 12,931 right now and lags behind the calls, as noted in TOOLS.md; with every call counted it will read about 16,660, leaving about 114,000. No tier change; no overage.
- **OpenAI:** one 61-character call, 5.35 s of audio, about $0.001 [E-derived].
- **Full script (about 9,500 characters), multi-voice** (four voices: about 7,650 narrator, about 1,850 characters): narrator at 1.7 times (the V1 retake ratio) is 13,000, characters at 3 times (one-word lines generated inside longer takes, retakes) is 5,500. About **18,500 credits, about $3.40**; pessimistic 2.5 times is about 24,000 credits, about $4.40. v4 tags are billed as characters, so add up to 15%. This is plan quota, not extra spend, and it fits in the 114,000 left with room for five or six full passes.
- Reproduce: `scripts/gen.py`, `scripts/metrics.py`, `scripts/reel.py`, `scripts/build_audition.py`; every call is in `voice_log.csv`.
