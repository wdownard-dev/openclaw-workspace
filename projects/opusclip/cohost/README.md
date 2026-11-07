# NULL//SMIRK AI co-host pipeline (variant A "Subtle"), gaming clips

Takes a gaming clip + a story, writes sourced co-host reactions and a 3-part outro, and renders a 1080x1920 Short. Free/local only: faster-whisper, Kokoro `am_onyx`, Pillow rig (`../cohost-options/null-v2`), ffmpeg static. Nothing here posts, schedules, messages anyone or calls OpusClip.

## One-command usage
```
PY=/home/williamdownard/openclaw-sites/tts-venv/bin/python
cd /home/williamdownard/.openclaw/workspace/projects/opusclip/cohost
$PY render_cohost.py prep CLIP.mp4 --slug my-story --story "topic" --handle @creator --urls OFFICIAL_URL [OFFICIAL_URL...]
#  -> transcript (word timestamps), fetched official pages, structure pick, work/my-story/prompt.md
#  (agent writes work/my-story/facts.json and script.json, see below)
$PY render_cohost.py render my-story      # fact-check guard -> TTS -> render -> out/
```
Outputs in `out/`: `<slug>-cohost.mp4`, `<slug>-factcheck.md`, `<slug>-description.txt`. `check <slug>` runs only the guard. `render --skip-tts` re-renders with the existing voice. `--facts-file f.json` on `prep` copies an operator-supplied facts file (still verified).

## How the agent writes script.json
1. `prep` prints the structure for this run (rotation: not either of the last two used; `--structure id` overrides) and writes `work/<slug>/prompt.md` from `prompts/script_prompt.md` (voice rules, hard rules, JSON shape).
2. Find facts: `python3 facts.py fetch <slug> URL...` (official domains only, see `config.json`), `python3 facts.py find <slug> keyword...` prints candidate sentences. Write `facts.json`: `{id, claim, quote, url, date YYYY-MM-DD|"Unknown", source}`. The quote is copied verbatim; `facts.py verify` rejects any quote not found on the fetched page, any non-official domain, and any date not printed on the page.
3. Write `script.json`: `clip {start,len,handle}`, `reactions[{id,t,quote,text,expr,facts}]` (t and quote point at a transcript moment), `outro[{part: takeaway|opinion|question, text, facts, card, expr}]`, `title`, `description_intro`, `allow_terms` (topic names only; listed in the report).
4. `render` runs the guard first and exits non-zero (and writes the report) if any line has an unverified fact, an unsourced digit/month/proper noun, a reaction whose quote is not in the transcript within 2 s of `t`, more than 14 words, no fact-linked takeaway, or no on-screen source card. It also refuses to reuse the previous output's structure (`--allow-repeat` overrides).

## Add a script structure
Append an object to `structures.json`: `{id, name, guide, reaction_style}`. `guide` is what the takeaway/opinion/question should do. Nothing else to change; rotation picks it up.

## What the video contains
Clip fitted over a blurred copy at y=400, NULL//SMIRK in the corner with expression cues and loudness-based mouth sync, clip audio sidechain-ducked under the voice, `Source: @handle` bottom-left throughout, `AI CO-HOST` tag, captions in 4-word chunks (timed proportionally, not word-aligned), then full-screen outro: part label, captions, an on-screen card per fact line with the official page and its date in small text.

## Runtime
About 4-5 s of render per second of video on 12 CPU threads (mascot layer cache warms up): see the dry-run numbers in `work/<slug>/accounting.json` and the summary below. Transcription of a 35 s clip: about 20 s. Kokoro: about 1 s per line after a 10 s model load.

## Still manual
- Choosing the clip and the story, and confirming the clip owner allows reuse (a Vyro/campaign clip may be licensed only for that campaign).
- Reading each fact-linked line against its quote: the guard proves the quote is on the official page and that numbers/names come from it, not that the sentence means what the quote means.
- The description's `description_intro` is not machine-checked: keep it to facts already in facts.json.
- YouTube Studio: confirm the altered/synthetic-content answer (NULL is a stylized cartoon with a synthetic voice, so the label should not be needed) and the paid-promotion box if the footage came from a partnership.
- Watching the render with sound. The machine has no audio output, so voice and mix were checked only by waveform/transcript, not by ear.
- Posting. Nothing here uploads.

## Files
`render_cohost.py` (CLI, TTS, ASS, avatar, ffmpeg), `facts.py` (fetch + verify), `factcheck.py` (guard + report), `transcribe.py` (clips-venv), `structures.json`, `config.json`, `prompts/script_prompt.md`, `state.json` (last structures), `work/<slug>/` (transcript, sources, facts, script, voice, ass), `out/`.

## Dry run (2026-11-06): `mw4-dmz-extraction`
- Clip: `clips-work/cut/mw4-01-cut.mp4` (34.5 s cut from MrBeast Gaming's "Escape Call of Duty's DMZ, Win $1,000,000", a Vyro campaign clip, source credit `@MrBeastGaming`); shown 7.0 to 31.5 s (24.5 s). No GTA 6 or T5G/TmarTn2 clip is on disk (those exist only inside OpusClip, not downloaded: no OpusClip calls allowed).
- Structure: timeline. Facts: 5, all callofduty.com blog pages (Oct 5, Oct 9, Oct 23, Nov 2 2026), quotes verified verbatim against the fetched pages.
- Output: 50.0 s, 1080x1920, 30 fps, H.264/AAC, 10.5 MB. Render 164 s (14 s TTS prep + about 150 s frames) on CPU; transcription 21 s.
- Footage: third-party. Source clip 24.5 s (49% of the runtime); original material (full-screen outro 26.1 s of NULL//SMIRK with sourced timeline, plus 3 in-clip reactions) 26.1 s = 52%. Co-host voice totals 34.0 s (68% of runtime has NULL speaking, 8 lines, about 62 spoken words, of which 26 are the sourced takeaway).
- Honest assessment: borderline. YouTube's bar is "significant original commentary", and a human reviewer will see a synthetic voice reading three dates taken from a publisher blog over a creator's clip. The dates are accurate and add information the clip lacks, but they are a restatement of an official blog (the policy lists "readings of other materials" as non-original), and the takeaway is a schedule, not analysis. Likely needs more: a longer, opinionated outro (45 to 60 s) built on something the sources do not state themselves (a comparison, a calculation, a tested claim), 4 to 6 reactions that interpret the clip rather than label it, and own-footage B-roll (own gameplay capture or screen recordings of the patch notes). Rotation of structures helps the "templated" test only if the content differs, not just the format.


## Low-interruption mode (v2, 2026-11-06)
Design rule: "the main thing is to have the host, but also not interrupt the video too much." Two knobs, set in `config.json` or per run on the command line (`render ... --interrupt-level low|medium|high --ai-tag always|intro_outro|off`).

| knob | values | default | effect |
|---|---|---|---|
| `interrupt_level` | `low`, `medium`, `high` | `low` | table `levels` in config.json: max spoken interjections (2/4/6) and their max length (4.5/5.5/7 s), max comment cards (4/6/8), card length (2-3.2/3.5/4 s), outro cap (10/15/24 s), outro speech rate, NULL opacity (0.72/0.88/1.0), clip-audio duck depth `duck_db` (-6/-9/-12 dB). The guard and the renderer refuse a script that exceeds the level. |
| `ai_tag` | `always`, `intro_outro`, `off` | `always` | the small semi-transparent `AI CO-HOST` tag in the top-right corner (30 px): always, only first 3 s plus the outro, or hidden. The description disclosure line is written regardless. |

What v2 renders: the clip plays for its whole length in a large window (`layout.clip_*`: centre crop 1296x1080 scaled to 1080x900) over its blurred copy, with no takeover. NULL (variant A, about 20% of the width, semi-transparent) sits in the bottom-right corner under the clip for the whole clip, changing expression silently (`expressions[]` keyed to source seconds, plus a held expression per card). Spoken interjections are `interjections[]`: each must start inside a whisper pause and the TTS length is checked against the next transcript word, so they never run over source speech (the renderer refuses otherwise); the clip audio is ducked by `duck_db` only while they play. Most added content goes into `cards[]`: 2-3 s text boxes next to NULL, `{id,t,quote,dur,label,text,facts,expr}`, tied to a transcript moment, 22 words max, each factual card shows `host (date)` of its official page and passes the same fact-check guard as spoken lines. The outro is 6-10 s at `low` (dense sourced fact, one deadpan opinion, one question); NULL grows to full size; each sentence is shown whole and wrapped over lines (v1 chunked it into 4-word pieces and cut sentences). `derived_notes[]` in script.json (arithmetic, opinion) is printed in the fact-check report.

v2 `script.json` shape: `clip{start,len,handle,protect}`, `interjections[]`, `cards[]`, `expressions[{t,expr,dur}]`, `outro[]`, `title`, `description_intro`, `allow_terms`, `derived_notes`. `python render_cohost.py gaps SLUG` lists the pauses where interjections fit (in a loud clip they are about 1 s, so keep spoken lines to 1-2 words). The old `reactions[]` key is gone: use `interjections` and `cards`.

## Dry run v2 (2026-11-06): `mw4-dmz-extraction-v2`
Same clip, structure `one_number` (20 Points per successful DMZ Exfil from the official Season 1 BlackCell challenge page, vs the clip's $500,000). Outputs `out/mw4-dmz-extraction-v2-{cohost.mp4,factcheck.md,description.txt}`; numbers in `work/mw4-dmz-extraction-v2/accounting.json`. Extra official facts f6-f9 come from the Oct 5 and Oct 9 DMZ deep dives and the Nov 5 battle pass page, all quote-verified.
Result: 36.2 s, 1080x1920, 12.3 MB, render 112 s (+8 s TTS). Source clip 27.0 s (75% of runtime incl. 0.5 s crossfade); in-clip added content (4 cards + 2 interjections, union) 13.6 s; outro 9.7 s; NULL speaks about 10.5 s (2 interjections 2.1 s, outro 8.4 s, about 20 words). Review frames: `work/review-v2/`. Voice and mix were not heard (no audio device); interjection timing was verified against transcript word times. Known flaws: interjections are 1 word because the clip has only about 1 s pauses; the outro takeover still hard-switches the clip out; the "five exfils" arithmetic is ours (flagged in the report).
