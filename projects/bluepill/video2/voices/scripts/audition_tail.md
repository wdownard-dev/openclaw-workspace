
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
