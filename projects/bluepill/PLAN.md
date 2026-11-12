# Project Blue Pill: original long-form animated YouTube channel (PLANNING, nothing started, no spend)

Named by William 2026-11-11. Not Project Red Pill (that is the OpusClaw/wrdclipz clipping project in projects/opusclip). Blue Pill is a separate channel with in-house production. Supersedes the "spitballing" notes in projects/future/youtube-channel*.md; those stay as research.

Labels: **[V]** verified this session, **[U]** unverified, **[E]** my estimate.

## 1. Goal

A separate YouTube channel making original long-form (10-18 min) animated explainers, produced in house by agents with light human review, grown to monetisation, and cut into Shorts for discovery. Spend is acceptable if it is justified (William, 2026-11-11).

## 2. What we decided in the spitball

- **Not Framesail-dependent.** Framesail ($35/mo Creator without MCP, $63/mo Pro with MCP, quarterly billing, about 35-55 min of video/month [V framesail.com/pricing]) is a fallback or one-month trial, not the plan.
- **MCP is a requirement** (William): we want the pipeline driven from chat/agents. Build or wrap a small MCP over our own pipeline.
- **No GPU purchase.** The Dell T7810 (825W PSU [V], 300W total graphics limit per Dell spec sheet [V], currently a FirePro V4800 with 1GB) could take a 4060 Ti 16GB, but APIs are cheaper until volume is proven. Tower stays a spare node for later.
- **Format = stick-figure explainer, not AI-video-clip generation.** Per-clip video generation is the costly path and fails often (seen in the Planet Ai tutorial). We compose reusable character files plus generated backgrounds.
- **Long-form first**, not Shorts.

## 3. Format spec (reduced from the two reference videos)

Source: projects/future/format-refs/ (transcripts). Paint Explainer "Ancient Greek Myths That Turned Out to Be True" (11:09, 1.1M views) and Good Enough "The Worst Punishments in Human History" (18:00, 17M views).

| | Target for Blue Pill |
|---|---|
| Length | 10-15 min (round-2 outlier data: 8-16 min performs as well as 20+ for small channels); revisit 20+ min after retention data |
| Script | 2,200-3,500 words, countdown or list of 8-10 segments, about 200-350 words each |
| Segment shape | claim, "but here is what they found", evidence, the twist |
| Cuts | one every 4-5.5 s (about 130-170 shots per video) |
| Visual | flat 2D, stick-figure cast with 6 expressions, flat generated backgrounds, headers, maps, photos, yellow keyword pops, red speech-bubble punchlines |
| Audio | one narrator (ElevenLabs), light music, a few SFX |
| Asset reuse | many shots reuse a background with a new pose, so images generated per video are far fewer than shots |

Own character and style only. Do not copy either channel's art. Preferred visual target (William, 2026-11-11): the Unknown Frequencies look, simple consistent cartoon characters over detailed illustrated backgrounds, see REF-unknown-frequencies.md.

**Multi-platform (William, 2026-11-11):** the same animated style should also feed TikTok and Instagram Reels. Build Remotion compositions in both 16:9 and 9:16 from the start (keep key action and captions inside a centre-safe area) so Shorts/Reels/TikTok cuts need no redo. Check each platform's repost and AI-label rules before publishing [U].

**Image provider (William, 2026-11-11):** OpenAI account available. Key to be added by William via `openclaw models auth paste-api-key --provider openai` (or Control UI). Then run the 20-image background test with gpt-image-2.

## 4. Pipeline (one MCP tool per stage)

1. **Channel bible:** style rules, palette hex codes, character sheets, voice, hook and title rules (JSON/MD in this folder).
2. **Topic and outline:** outlier check of the niche (reuse swipe.py logic from projects/side-income/youtube-agent-skill.md after re-reading), then a segment outline. Human approves the topic.
3. **Script:** Claude writes it with a hook-first structure and an accuracy pass (fact-stating, so each claim gets a source).
4. **Storyboard:** shot list (about 150): shot id, narration line, background, character pose/expression, text overlay, motion.
5. **Character kit:** one-time multi-view sheet plus 6 expressions and about 12 poses, built with fixed hex colours and proportions. Method borrowed from the Planet Ai tutorial: locked sheet, "immutable features" rules, a continuity-supervisor instruction. Characters become fixed image files.
6. **Backgrounds and props:** image-model generation in the locked flat style; a reusable library grows over time so cost per video falls.
7. **Voiceover:** ElevenLabs, one pass per segment, timestamps feed the edit.
8. **Assembly:** Remotion (code-based) renders shots with pan/zoom, pose swaps, text and bubbles, captions (Whisper), music. Closest open-source base: DojoCodingLabs/remotion-superpowers (MIT, Claude Code plugin with 5 MCP servers, updated 2026-10-29 [V]). Licence of Remotion for commercial use is **[U]**, confirm before relying on it.
9. **QA gate:** automated checks (audio sync, black frames, text overflow, character colour drift) plus a human watch.
10. **Publish:** private YouTube upload through the existing Google OAuth, thumbnail and title from the hook scorer, human flips to public.
11. **Shorts:** cut 2-4 Shorts per video from the strongest segments.
12. **Track:** log every video (cost, hours, views, AVD, subs) in a CSV, like projects/opusclip/experiment-log.csv.

## 5. Policy and monetisation risk (the main thing that can sink this)

- **Inauthentic content policy [V, support.google.com/youtube/answer/1311392]:** templated storylines and generic AI content can be demonetised. A set of characters across episodes is allowed if each video has a distinct storyline. Our format must have a different topic, research, script and twist every video, not just swapped nouns.
- **AI disclosure [V, support.google.com/youtube/answer/14328491]:** fully animated, non-realistic content does not need the label. Realistic synthetic content does.
- **YPP thresholds [V]:** 1,000 subscribers plus 4,000 public watch hours (or 10M Shorts views in 90 days). Review takes about a month.
- **Content risk:** graphic topics (torture, gore) limit ads and risk age restriction. Pick a general-audience niche.
- **Mitigations:** original research per video, a distinct human-approved angle, our own character and voice, a visible human editorial pass, and keep early videos few and strong instead of many and thin.

## 6. Budget (all [E] unless noted; price everything before buying)

| Item | Estimate |
|---|---|
| ElevenLabs | a paid plan is likely needed for 10-min voice per video; price it first [U] |
| Image generation | roughly $2-10 per video, fewer once the background library exists [E] |
| Music | free-licence library, $0 to start |
| Remotion | free for an individual or small team per my recollection [U], confirm |
| Framesail Pro trial (optional) | $63 one billing period [V], only if we want a head-to-head |
| Hardware | $0, tower held in reserve |
| Human time | script approval, QA watch, thumbnail approval: about 1-2 h per video once running [E] |

## 7. Phases and gates

- **Phase 0, decisions (now):** niche, channel identity, budget ceiling, voice. Gate: William signs off the Section 8 questions.
- **Phase 1, spike:** one 3-minute proof video, our own character, one topic. Measures: does the look hold, shot count, cost, hours. Gate: William likes the look.
- **Phase 2, full video 1:** 10-12 min, full QA, private upload. Gate: William approves publish.
- **Phase 3, 4-video batch:** prove repeatability and per-video cost, build the MCP wrapper properly, add Shorts cutting.
- **Phase 4, review:** after about 8-12 videos, read retention and CTR, then decide whether to keep tuning the pipeline, move to the harder illustrated style, or revisit the GPU.

## 8. Open questions for William

1. **Niche and topic lane. DECIDED (William, 2026-11-11): mythology, framed as "who was" / "all about" explainers.** Open to widening later to historical figures, historical events and fictional characters. Guardrails (my proposal, awaiting William): stay with public-domain subjects (myth, folklore, history, pre-1930 literature) and avoid modern franchise IP (Content ID, trademark risk); cite the source tradition per claim (Homer, Hesiod, Ovid and so on) since myths have several versions; keep violence stylised for ad suitability; avoid living or recent real people. Outlier check (projects/bluepill/OUTLIER-CHECK.md, rounds 1-2) says: lead with "Every ___ Explained" catalogues and "myths that turned out to be true"; Egyptian, Mesopotamian, Japanese and Norse are the least saturated mythologies, Greek is the most crowded; single-subject "who was" videos underperform. Series formats: (A) "Who Was ___" single-subject deep dive, (B) myth-vs-reality countdown lists (the Paint Explainer pattern), (C) "What really happened at ___" event explainers. Start with B and A. The GTA 6 lore idea is parked, possibly for the separate gaming channel.
2. **Channel identity.** Name, handle, character concept (does the narrator have a name and personality?).
3. **Budget ceiling** for setup and the first month.
4. **Voice.** Stock ElevenLabs voice, a custom designed voice, or William's cloned voice (Pro plan features need pricing).
5. **Human involvement.** How much review does William want per video, and who approves publish?
6. **Separate Google/YouTube account** for the channel (needs William to create, login and approve).

## 9. Accounts and keys needed (none requested yet)

- ElevenLabs API key
- An image-model API key (Gemini/Nano Banana via Google AI key, or OpenAI/Replicate); check what our Google OAuth already allows before buying anything
- New YouTube channel plus OAuth for it
- Optional: Pexels/Wikimedia (free) for photos

## 10. Next steps (when William says go)

1. Answer Section 8.
2. I price ElevenLabs and two image APIs against the per-video estimate.
3. I check Remotion licensing and test remotion-superpowers install in a scratch folder.
4. Build the character kit (needs the image key) and the Phase 1 spike.
