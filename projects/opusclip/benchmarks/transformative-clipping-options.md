# Transformative clipping options: making clips genuinely original (research, 2026-11-06)

Research and design only. Not legal advice. Nothing posted, emailed or submitted; no OpusClip or paid API calls. Builds on `reuse-permissions.md` (reused-content policy, Shorts ineligibility, credit does not equal fair use), which is not repeated here.

**The goal is compliance, not disguise.** Each clip has to be different and worth watching for a viewer. Tricks meant to get past detection (mirroring, pitch-shifting, zoom/crop to dodge Content ID, hiding the source) are excluded. They don't add value and they don't answer the reused-content test, which a human reviewer applies by looking at the channel.

## 0. What this host already has (checked 2026-11-06)

| Tool | Status | Path / note |
|---|---|---|
| ffmpeg 7.0.2 static | Installed | `/home/williamdownard/openclaw-sites/bin/ffmpeg`; built with libass, libfreetype, fontconfig. `subtitles`/`ass` filters exist; `drawtext` did not appear in `-filters`, so render cards and captions as ASS subtitles (or PNG overlays made with Pillow). |
| yt-dlp 2026.10.26 | Installed | `/home/williamdownard/openclaw-sites/ytdlp-venv` |
| faster-whisper 1.2.1 | Installed | `clips-venv`; models cached: `faster-whisper-base.en`, `small.en` (`openclaw-sites/models`). Enough for word-level transcripts on CPU. |
| OpenCV + YuNet face model | Installed | `reframe-venv`, `reframe-models/yunet.onnx` (face tracking for reframe/split-screen). |
| TTS | **None installed** | No piper, kokoro, edge-tts or espeak. Needs adding (section 3). |
| GPU | None seen (`nvidia-smi` absent); 12 CPU threads, 23 GB RAM | CPU-only TTS (Piper, Kokoro-82M) is realistic; local video-avatar models are not. |
| LLM | Agent's own model (Claude) is available to the pipeline | Script writing can run in the agent turn that already screens clips; no new API account needed. |
| OpusClip Pro | In use | `opus.py` submit/status/post; OpusClip does the cutting, captions and reframe. |

## 2. What YouTube says about AI voice, AI commentary and templated content (fetched 2026-11-06)

### 2.1 Channel monetization policies, https://support.google.com/youtube/answer/1311392
The page now has three sections that bear on an automated pipeline, plus the reused-content section already covered in `reuse-permissions.md`.

**What reviewers expect (verbatim):** content should "Be your original creation. If you borrow content from someone else, you need to change it significantly to make it your own." and "Not be mass-produced, generic, repetitive, or manipulative. It should be made for the enjoyment or education of viewers, rather than for the sole purpose of getting views."

**Generic or repetitive content ("inauthentic", renamed July 15, 2025), verbatim:**
- Definition: "content that looks like it's made with a template, or that may feel repetitive to viewers after watching several videos in a row from the same channel."
- Allowed: "Same intro and outro for your videos, but the bulk of your content is different"; "a series ... in which each video has a distinct storyline, focus, or concept". Key line: "What's important is that the substance of each video should be materially varied and deliver creative, educational, or other value."
- Not allowed: "channels where content feels interchangeable from video to video"; "Similar or repetitive content with low educational value, commentary, narratives, or minimal variation across videos"; "Image slideshows, templated storylines, or scrolling text with minimal or no narrative, commentary, or educational value"; and, directly on point, **"AI-generated content made with generic or unoriginal templates giving the impression of mass production without adding the creator's original, authentic insights or perspective"**.

**Reused content, lines that matter most for AI narration (verbatim):**
- Not allowed: **"Content that exclusively features readings of other materials you did not originally create, like text from websites or news feeds"**. A TTS voice reading a rewritten press release or headline is this case.
- Not allowed: "Content that gets views from mostly non-verbal reactions to your videos without added voice commentary". Emoji or "facecam reacting" overlays without real speech do not count.
- Not allowed: "Content uploaded many times by other creators". GTA 6 trailer moments are re-cut by hundreds of channels.
- Allowed: "Using clips for a critical review"; "Replays of a sports tournament where you explain the moves a competitor did to succeed"; "Reaction videos where you comment on the original video"; "Edited footage from other creators where you add a storyline and commentary"; "Reused content from other online sources where the creator is either visible in the content or explains how the creator added to the content".

**Unsatisfying or off-putting content (verbatim):** "If you use automated tools or templates to help create your content, the final product must still demonstrate your creative vision and provide educational or entertainment value." Allowed: "Content that utilizes creative tools to assist in delivering a unique, well-researched, or creative narrative, like using AI to edit your video scripts or generate a unique background visual for your content." So AI tools are permitted as assistance; the policy judges the output, not the tool.

**AI personas on sensitive topics (verbatim):** "channels that use AI-generated personas to deliver information on sensitive topics ... health, legal issues, finances, or politics ... will not be allowed to monetize." Relevant to wrdclipz (news): an AI anchor persona on political or legal stories is a stated non-monetizable case. Gaming news is not on that list.

**Process:** "videos undergoing checks ... may receive an additional review that may be completed by a human" (March 10, 2025 note). Reviewers sample main theme, most-viewed, newest, biggest watch-time share, metadata and About.

### 2.2 AI disclosure (altered or synthetic content), https://support.google.com/youtube/answer/14328491
- Must disclose realistic AI content that "Makes a real person appear to say or do something they didn't do", "Alters footage of a real event or place", or "Generates a realistic scene that didn't actually occur".
- No disclosure needed for "Production assistance, like using generative AI tools to create or improve a video outline, script, thumbnail, title, or infographic", "Caption creation", "Cloning one's own voice to create voice overs or dubs", "Gameplay footage from video games".
- An AI narrator voice that is plainly a narrator (not impersonating a real person) is not on the must-disclose list. A synthetic voice that sounds like a real streamer or anchor, or an avatar that looks like a real person, would be.
- "Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money." Non-disclosure risk: "penalties from YouTube, including removal of content or suspension from the YouTube Partner Program."
- YouTube may auto-label content its systems detect as AI generated or altered, or content carrying C2PA metadata.

**Takeaway:** YouTube does not ban AI voices or AI-assisted scripts. It bans (a) templated, interchangeable, mass-produced output, (b) reading other people's text, and (c) AI personas giving advice on politics/legal/health/finance. A TTS commentator passes only if what it says is genuinely new information or a real take, and differs materially between videos.

### 2.3 Shorts revenue: the threshold matters more than the format (https://support.google.com/youtube/answer/12504220)
- Verbatim: "Starting February 1, 2027, to be eligible to earn a share of Shorts ad revenue from the Creator Pool and YouTube Premium revenue for each month, you will need to have at least 10 million qualified Shorts views in the last 90 days."
- Ineligible views include "reuploading other creators' content from YouTube or other platform, or compilations with no original content added".
- Implication: at today's scale (about 1,300 views on the best news clip), Shorts ad revenue is out of reach from February 2027 whatever the format. Long-form (where watch-page ads pay per video) is where transformed content can actually earn at small scale. Design B below is long-form-capable for that reason.

### 2.4 Documented enforcement and reporting (secondary sources, read 2026-11-06)
- **July 2026 clarification (TechCrunch, 2026-07-20, https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/):** inauthentic content is now split into three categories: generic/repetitive/template-based, off-putting/distressing, and AI personas on sensitive topics. Quoting YouTube trust and safety chief Matt Halprin (from a Creator Insider video): "But that exact same new tool can allow you to make lots of videos really quickly that are very similar. They're very generic and don't really have a narrative arc and don't really show your creativity... that's the stuff that we don't want to have in YPP." Article: "Any YouTube channel that has too much of any of these three types of content will not be able to monetize, Halprin said." Rolled out July 16 (2026).
- **Faceless channels (The Hollywood Reporter, June 2026, https://www.hollywoodreporter.com/business/digital/faceless-creators-youtube-ai-damage-1236617586/):** Doctor NOS (1.7M subs) quoted: "The people who do the same content as me without their face in it, most of them are getting demonetized." An operator of six faceless channels (Noah Morris) says some are hiring human hosts and mixing in to-camera narration; THR: "It's unclear whether the gambit will ultimately work." The claim that the algorithm was "tweaked to reward videos incorporating human faces" is Morris's, not YouTube's; treat as anecdote.
- **Fake AI trailers (Deadline, Dec 2025, exclusive):** YouTube terminated Screen Culture and KH Studio ("well over 2 million subscribers and more than a billion views"), which "spliced together official footage with AI images to create franchise trailers". Earlier in 2025 YouTube had suspended their ads; they regained monetization after adding "fan trailer", "parody" and "concept trailer" to titles, then lost the channels when those labels disappeared; YouTube cited "spam and misleading-metadata policies". Directly relevant to GTA 6: AI "trailer 3" or "leak" videos are the pattern that got channels terminated.
- **Other headlines found, not read in full (Google News RSS):** "YouTube Wiped 35M Subscribers Over AI Slop" (Tech Times, 2026-07-15); "YouTubers fume at AI as popular animation channels demonetized" (Dexerto, 2026-02-11); "More than 20% of videos shown to new YouTube users are 'AI slop', study finds" (The Guardian, 2025-12-27); "Never fear, reaction videos are still allowed under YouTube's new 'inauthentic content' policy" (Engadget, 2025-07-14). Details Unknown here.
- **Thriving AI-narrated gaming/news channels with confirmed monetization:** Unknown. No source found that documents a monetized, fully AI-voiced gaming clip channel. Many small "GTA 6 News/Leaks" channels with AI voices exist (noted in `gaming-news.md`), but monetization is not publicly visible. One proxy: a "Join" (channel membership) button requires YPP, so its presence shows the channel is in YPP, though not whether specific videos earn.

## 1. What successful clip, news and commentary channels actually add

Subscriber counts read from channel pages 2026-11-06 unless marked. View counts are from YouTube search results for one sample video. "Monetized?" is Unknown for all of them because YouTube does not show it publicly; all of these are large enough to be in YPP, but that is an inference.

| # | Channel / format | URL | What they add on top of borrowed footage | Scale (sample) |
|---|---|---|---|---|
| 1 | **TGG**: GTA 6 news, narrated breakdowns | https://www.youtube.com/channel/UC72PuhDwKtZ5MikpGNhPAtA | Own scripted voiceover; trailer used as illustration of a claim ("Everything You MISSED"); comparisons to earlier trailers/leaks; frame call-outs. | 2.29M subs; "GTA 6 Trailer 2 Breakdown: Everything You MISSED!" 1.07M views |
| 2 | **IGN**: "89 Details From GTA 6 Trailer 2" | https://www.youtube.com/channel/UCKy1dAqELo0zrOtPkf0eTMw | Numbered list format, editorial research, on-screen labels; publisher relationship (press access). | 20M subs (regex read, not verified in header); 1.55M views |
| 3 | **Jetro**: "100+ Hidden Details in GTA 6 Trailer 2" | https://www.youtube.com/channel/UC1lRz_clX4l9ORCtjDRBs1g | Shot-by-shot detail hunting with narration; the value is the observation, not the footage. | ~98K subs (regex read); 904K views |
| 4 | **Kai The Criminal**: "Every Detail... Explained in 24 Minutes" | https://www.youtube.com/channel/UCsGy80SaKVYU3XTloXyTI4Q | Long, dense scripted explainer; another title advertises "(Without AI)", a sign viewers are tired of AI narration. | ~3K subs (regex read), 182K-view video: a tiny channel can break out with a researched long video |
| 5 | **DarkViperAU**: trailer + lore analysis | https://www.youtube.com/channel/UCV6mNrW8CrmWtcxWfQXy11g | Personal expertise (GTA speedrunner, GTA 6 voice actor per his About), long-form analysis. | 2.34M subs (reuse-permissions.md) |
| 6 | **TrueGameData**: CoD weapon data | https://www.youtube.com/channel/UCzcuXZhpbH99W-CTBJgZoJQ | Original measured data (TTK, damage ranges) shown as charts; runs TrueGameData.com. Footage is incidental, the data is the content. | 238K subs; "BEST SMGs..." 85K, "Balanced Play Style Ep. 1" 111K |
| 7 | **JGOD / WhosImmortal**: Warzone loadouts and patch notes | https://www.youtube.com/channel/UCG0yjoHan7kXjROe0JgvhzQ, https://www.youtube.com/channel/UCLEsipUKnZpQnGDJ1Dpk6wg | Own gameplay capture, tested loadouts, patch-note explanations with opinion ("MW4 new gameplay changes & update patch notes"). | JGOD "Top 10 Loadouts" 685K views; subs not verified |
| 8 | **T5G / Top5Gaming**: top-5 and news narration | https://www.youtube.com/@T5G | Scripted narration over game footage, list structure, takes ("BAD NEWS About Fortnite's ..."). A source for William's clips is itself a transformative narrator. | 1.5M subs; recent 444K-view video |
| 9 | **penguinz0 (MoistCr1TiKaL)**: reaction/commentary | https://www.youtube.com/@penguinz0 | A recognizable person reacting with jokes and opinion; footage is a prompt for the commentary. | 18.3M subs; recent videos 858K-880K |
| 10 | **Daily Dose Of Internet**: narrated compilation | https://www.youtube.com/@DailyDoseOfInternet | His own voiceover introducing each clip with a joke, and permission-cleared footage. About page: "I always ask for permission to share videos" and "I don't feature AI generated content, ever." | 20.7M subs; recent 757K-view video |
| 11 | **Luke Stephens CLIPS / TmarTn2 Shorts** (from `gaming-news.md`) | see gaming-news.md | Their own face and opinion; clips of their own streams. Hooks are takes ("No Chance GTA 6 Runs Past 30FPS..."). | TmarTn2 Shorts median 121K; Luke Stephens CLIPS median 63K on 58K subs |
| 12 | **Faceless AI "GTA 6 News/Leaks" farms** | (many, under 300 subs, noted in gaming-news.md) | TTS reading headlines over trailer footage. | Tiny reach; these are the inauthentic-content pattern, not a model to copy |

**Pattern across the winners:** the borrowed footage is evidence for something original: a claim, a data point, a count of details, a joke, a comparison. Nobody successful just re-posts another streamer's moment. The ones growing in 2026 add (1) research or data viewers can't get from the source video, (2) a consistent identity (a face, a known voice or a branded data style), and (3) a take. "Every detail" and "explained" lists and opinion hooks drove the top views in this sample. Split-screen reaction in particular works for penguinz0 because he is penguinz0; a nameless reactor doesn't get the same benefit.

**Not found / Unknown:** a confirmed, monetized, fully AI-voiced gaming clip channel at scale; a channel using an AI avatar co-host for gaming news with known results; Gameranx (handle returned 404 this session).

## 3. Candidate automated designs

Common cost basis (estimates, 2026-11-06): LLM script written in the agent turn that already screens clips (no new spend), or about $0.01-0.03 per clip via a small API model. TTS: **Kokoro-82M** (Apache-2.0, runs on CPU, near real time on 12 threads) or **Piper** (MIT, very fast on CPU, more robotic), $0. **edge-tts** is free but uses Microsoft's unofficial online endpoint (terms grey, could break); ElevenLabs is the quality option at about $5-22/month. ffmpeg and faster-whisper are installed. OpusClip about 1 credit per source minute (existing). Render on CPU: about 1-3 min per 60 s Short.

Fact-checking applies to every design: the script may only state things that come from the transcript, an official source (Rockstar Newswire, Activision/CoD blog patch notes, publisher press releases) or a data source we fetched, with the source shown in the description. A hallucinated "fact" in a news-style video is worse than no commentary.

### (a) LLM reactive commentary + TTS over the clip
- **Concept:** clip plays; a narrator voice interjects 2-4 times with jokes, context and an opinion; ducked source audio.
- **Bar met?** Weakly. Policy allows "Reaction videos where you comment on the original video", but commentary that is short, generic ("Wow, that was crazy!") or the same shape each time is what YouTube calls templated AI content. The clip still carries most of the runtime, so the original part is small.
- **Steps:** OpusClip clip -> faster-whisper word timestamps -> LLM finds pauses and writes interjections tied to specific moments -> Kokoro TTS -> ffmpeg `sidechaincompress`/volume duck, mix, burn ASS captions labelling "Commentary" -> post.
- **Cost:** about $0-0.03 per clip plus OpusClip credits.
- **Quality risk:** high: LLM jokes are bland, interjections over a streamer talking are annoying, and the voice is the same in every video.
- **Monetization risk: HIGH.** Still mostly someone else's moment, credited, with a thin AI layer; close to "minimal changes". Fine as an ingredient inside (b), weak as the whole design.

### (b) News-recap: original narrated script, clip as an illustrated segment (recommended)
- **Concept:** a 45-60 s Short or a 6-10 min long-form "GTA 6 / MW4 news" episode. The narration tells a story: what happened, why it matters, timeline, what it contradicts or confirms (earlier trailer, earlier Rockstar statement, patch history). Creator clips appear as short quoted segments (3-10 s, "@T5G said...") next to official trailers and on-screen cards.
- **Bar met?** Yes if done honestly: it matches "Edited footage from other creators where you add a storyline and commentary" and "Using clips for a critical review". It must not be a reading of the press release ("exclusively features readings of other materials ... like text from websites or news feeds").
- **Steps:** (1) radar (existing) finds a story; (2) collect sources: official trailer/press post via yt-dlp + Newswire/blog text, 1-3 creator takes (OpusClip or direct whisper transcripts); (3) LLM writes a script with a structure that changes per story type (leak check, patch explainer, timeline, "what we know vs rumor"), cites a source for every fact, and includes one clear take; (4) the agent (or a human, see f) checks facts against sources; (5) Kokoro TTS; (6) ffmpeg edit: B-roll from official footage, quoted creator segments with on-screen credit, cards (dates, numbers) as ASS/Pillow overlays, captions; (7) same piece cut as a Short (45-60 s) and, weekly, a long-form roundup.
- **Cost:** about $0-0.05 per Short; OpusClip credits only if a long source needs cutting (often use direct trims instead).
- **Quality risk:** medium: script quality decides everything; a single fixed template makes the channel interchangeable. Rotate 4-6 segment structures, vary length and openings, and only run a story when there is real new information.
- **Monetization risk: MEDIUM-LOW** when each video carries real information and the footage is a minority of runtime and mostly official; MEDIUM with a stock AI voice, because a faceless AI-voiced news channel is the profile the 2026 crackdown hit (THR).

### (c) AI co-host / avatar split-screen reactor
- **Concept:** split screen, clip on top, an animated host at the bottom "reacting" with TTS lines.
- **Bar met?** Doubtful. The value is still the LLM's words; the avatar is decoration. A photoreal avatar would need AI disclosure, and one that looks or sounds like a real person is a must-disclose and an impersonation risk. On wrdclipz, an AI news "anchor" is close to the "AI personas ... on sensitive topics" ban for politics, legal or court stories.
- **Tools:** photoreal talking heads (HeyGen, D-ID: paid subscriptions) or open-source (SadTalker, LivePortrait: practical only with a GPU, which this host lacks). Cheap option: a cartoon mascot PNG with mouth frames driven by TTS loudness (non-realistic, no disclosure needed), rendered in ffmpeg.
- **Cost:** $0 (cartoon) to $25-90/month (paid avatars).
- **Quality risk:** high; viewers find a lip-synced AI host uncanny and recognize it as slop.
- **Monetization risk: HIGH.** Looks like the "faceless channel hiring a face" workaround without the human. Cosmetic, not substantive.

### (d) Clip + original data/analysis cards (recommended for wrdgamingclipz)
- **Concept:** footage plus data the viewer can't get from the source clip: Warzone/MW4 weapon TTK, damage ranges, patch-to-patch changes, pick rates; GTA 6 trailer shot-by-shot facts (location identified on the leaked/official map, timestamp in trailer 1 vs 2, what changed since).
- **Bar met?** Yes: the "Replays of a sports tournament where you explain the moves" example is the closest; TrueGameData shows data can be the whole product.
- **Steps:** (1) pull data: official patch notes (callofduty.com blog), our own structured notes per GTA 6 trailer (built once, reused), public stats sites only where their terms permit; (2) LLM picks the 2-4 numbers that matter for this clip and writes the explanation; (3) Pillow renders chart/card PNGs (bar of TTK before/after, map pin); (4) ffmpeg overlays cards, captions, short TTS narration; (5) post with sources listed.
- **Cost:** about $0-0.03 per clip; one-off build of the data tables (a few hours).
- **Quality risk:** medium: data needs to be right and fresh; stale patch data is misinformation. Cards must change per video (different stats, layouts), not one frame template.
- **Monetization risk: LOW-MEDIUM.** The strongest "educational value" case; the risk is data licensing (do not scrape sites that forbid it) and templated look.

### (e) Multi-source synthesis: "what 5 creators think about X"
- **Concept:** one story, several creators' takes (T5G, TmarTn2, DarkViperAU...), short quoted segments, an original narrator framing agreements and disagreements, and a verdict.
- **Bar met?** Plausibly, if the narrative is real ("three of five think the delay is about performance; here's what the data says"). Without that, it is a compilation, which the policy names: "compilations with no original content added" (Shorts) and "Clips of moments ... edited together with little or no narrative".
- **Steps:** radar picks a story -> yt-dlp the creators' videos -> whisper transcripts -> LLM extracts claims, clusters them, writes a script with a conclusion -> trim 4-8 s quotes -> narrate, cards, captions.
- **Cost:** about $0-0.05; more source downloads; no OpusClip needed.
- **Quality risk:** medium-high: easy to slide into "clip, clip, clip"; and five creators' footage multiplies Content ID claim chances.
- **Monetization risk: MEDIUM.** Lowers dependence on any single creator, but raises total third-party footage share. Better as a weekly long-form than a daily Short.

### (f) Hybrid with a 10-second human approval
- **Concept:** any of (b), (d) or (e), but the agent sends William the script plus a preview frame on Telegram; "ok" posts, a one-line edit ("say it's a rumor") reruns.
- **Why it helps:** (1) catches wrong facts and bland scripts before they post; (2) lets William add a line of his own opinion, which is the "creator's original, authentic insights" the policy asks for; (3) cheap: the alert flow already exists ("clip it"). Recording his own voice for one line, or cloning his own voice (YouTube says "Cloning one's own voice to create voice overs or dubs" needs no disclosure), would raise the bar much more than any AI persona.
- **Cost:** about 10-30 s of William's time per post.
- **Monetization risk:** one level lower than the same design fully automated.

### Footage strategy (all designs)
- **Shorter borrowed segments:** keep third-party creator footage to brief quoted segments (a few seconds each) and a minority of runtime. This is a working heuristic, not a YouTube rule (no percentage is published); it puts the original part in the majority and lowers Content ID exposure.
- **Prefer official footage:** publisher trailers (Rockstar Games, Call of Duty channels), press kits and patch notes. These are still not ours (Content ID may claim; "Content uploaded many times by other creators" applies to trailers too) so the narration still has to carry the video.
- **Own capture:** MW4 appears to be out (TrueGameData has "MW4 MP and DMZ Full Data") and GTA 6 is near release. Owning the game and capturing gameplay (YouTube: "Gameplay footage from video games" needs no AI disclosure) is the biggest single step away from reliance on creators. Not fully automatable (needs someone to play), but 30 min of capture can supply B-roll for weeks. Rockstar's posting policy page could not be read (see reuse-permissions.md) and needs a manual check.
- **CC/public-domain:** little useful gaming footage exists under CC; YouTube's "Creative Commons" filter is worth a check per story but should not be relied on.
- **Never:** mirroring, pitch/speed shifts, crops or zooms meant to beat Content ID, fake "leak" or AI-generated trailer footage (the Screen Culture/KH Studio terminations).

## 4. Recommendation

**Best designs for an automated pipeline:**
1. **(b) News-recap with the clip as a quoted segment**, for both channels: an original script built around new information, official footage as B-roll, creator clips as short credited quotes. It keeps the radar -> clip -> screen -> post flow and only adds a script, TTS and an ffmpeg edit step.
2. **(d) Data/analysis cards**, for wrdgamingclipz: MW4/Warzone patch and weapon data, GTA 6 trailer fact tables. Strongest "educational value" case and hardest to call templated if the data changes per video.
Run both as **(f) hybrids**: William approves the script in about 10 s and, when he wants, adds one line in his own words or his own cloned voice. Fully unattended is possible, but it is exactly the profile YouTube described in July 2026 ("lots of videos really quickly that are very similar").

Not recommended as the main format: (a) on its own (too thin), (c) avatar co-host (cosmetic, uncanny, persona risk on news), (e) as a daily Short (compilation risk; fine as a weekly long-form).

**Phased rollout**
- **Phase 0 (now, no spend):** install Kokoro or Piper in a venv; write the script prompt with 4-6 rotating structures and a "cite a source for every fact" rule; build the GTA 6 trailer fact table and an MW4 patch-notes table; make 3 test renders locally, not posted.
- **Phase 1 (2 weeks, gaming channel):** every new post is (b) or (d). Stop posting plain re-cuts on any channel meant to be monetized, since reviewers look at the newest and most-viewed videos and the policy is channel-wide. About 1 post/day; a weekly 6-10 min long-form roundup from the week's scripts.
- **Phase 2:** apply what wins to wrdclipz. News (b) fits, but no AI anchor persona on politics or legal stories (sensitive-topic ban). Keep attributing to the agency.
- **Phase 3:** add own gameplay capture once GTA 6 is out; add William's voice for intros if he's willing.

**Cheap A/B plan (measure the viewer and YouTube response)**
- Arms on wrdgamingclipz, alternating day by day on comparable stories: **A** = (b) with AI voice fully automated, **B** = (b)/(d) with William's 10-second approval plus one line of his. Plain re-cuts are not an arm: posting more of them hurts the channel-wide review.
- Per video, at 24 h / 72 h / 7 d (existing log): average % viewed, swiped-away rate, engaged views, subscribers gained, comments that mention the commentary (a direct test of "viewers can tell there's a meaningful difference"), Content ID claims.
- YouTube signals: YPP application result and the stated reason (a "reused content" rejection names it), yellow-$ or limited-ads icons per video, any automatic AI label, Studio notices. RPM only once in YPP. Shorts revenue needs 10M qualified Shorts views per 90 days from Feb 1, 2027, so at current scale the real money test is long-form watch-page monetization, not Shorts.
- Decision rule: n >= 6 per arm before concluding (existing LEARNINGS rule). If a YPP review rejects for reused content, stop, change the format, and do not open new channels to get around it (the policy's creator-responsibility section bars that).

**Three biggest caveats**
1. **Nothing guarantees monetization.** Review is human and channel-wide; the policy judges output quality and variety, not the tools used. Fully automated, templated AI commentary is itself the pattern the inauthentic-content policy targets, so real variety and real added information per video are essential, not optional.
2. **Copyright is separate.** Transformative for YPP does not mean fair use; Content ID can still claim official trailers and creator footage (Shorts over 1 min with claimed content are blocked). Rockstar's and Activision's creator policies are still unread (see reuse-permissions.md).
3. **Accuracy and identity.** An LLM news script that gets a fact wrong damages the channel faster than a plain clip. Synthetic voices that sound like real people, AI personas on sensitive news, and AI "leak" footage are disclosure and termination risks. Keep humans, or at least sources, in the loop.

Research, not legal advice. File sections in order of writing: 0 (host), 2 (policy), 1 (benchmarks), 3 (designs), 4 (recommendation).
