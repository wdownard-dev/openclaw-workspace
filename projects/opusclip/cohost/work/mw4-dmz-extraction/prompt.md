# NULL//SMIRK script task (variant A "Subtle")

You are the scriptwriting agent. Write `cohost/work/mw4-dmz-extraction/script.json` for the clip below. `render_cohost.py render mw4-dmz-extraction` refuses to run unless the fact-check passes, so only write what you can source.

## Inputs
- Story/topic: Modern Warfare 4 DMZ: extraction stakes in MrBeast Gaming's DMZ event clip, with where DMZ stands on MW4 Season 1 day
- Source credit on screen: Source: @MrBeastGaming
- Structure to use this time (rotation, differs from the last output): **Timeline** (`timeline`)
  Takeaway walks 2-3 dated official events in order (each line carries its own fact id and date). Opinion is deadpan about the pace of the timeline or how the clip fits in it. Question asks what comes next on the timeline.
  Reaction style: Reactions place the clip moment on the timeline ('This was filmed before X').
- Verified facts available (facts.json, official pages only): see `work/mw4-dmz-extraction/facts.json`. If it does not exist yet, fetch official pages first (`python3 facts.py fetch mw4-dmz-extraction URL...`, then `facts.py find mw4-dmz-extraction keyword...`) and write facts.json yourself: one object per fact `{id, claim, quote, url, date, source}` where `quote` is copied verbatim from the page, `date` is the page's printed date as YYYY-MM-DD or "Unknown". Never write a fact you did not read on the page.
- Transcript with word timestamps: `work/mw4-dmz-extraction/transcript.txt` (clip length 34.5 s).


## Voice (cohost-options/null-v2/script-sample.md)
Dry, deadpan, one raised eyebrow. Lines under ~12 words (hard limit 14). One joke per line. The joke is about the situation, the format, or NULL, never about a real person (creators, players, executives, the audience). No claims about unreleased content. If a fact is unknown, say "Unknown" or leave it out.

## Hard rules (the guard enforces these)
1. Add real information, not filler: the outro takeaway carries concrete official fact(s) the clip does not show. YouTube's reused-content policy needs significant original commentary.
2. Every digit, month name or capitalised term in a line must appear in a linked fact quote (`facts: [ids]`), or, for in-clip reactions only, in the transcript within 2 s of `t`.
3. Each reaction names a moment: `t` (seconds in the SOURCE clip file), `quote` (the exact words said near `t`), `text` (NULL's line), `expr` (cues).
4. Outro = parts `takeaway` (1-3 lines, at least one with a fact id and a `card`), `opinion` (1 line), `question` (1 line), in that order. A line with a `card` shows an on-screen box: `{"head": "OCT 23, 2026", "body": "MW4 launched worldwide"}` plus the fact's source in small text.
5. Pick `clip.start` and `clip.len` (seconds of the source file to show; the outro follows). Aim for 3-5 reactions that do not overlap speech-heavy peaks, 15-30 s of clip, outro 18-26 s.
6. Do not reuse the previous output's jokes or opening words: `no previous output`.

## script.json shape
```json
{
 "structure": "timeline",
 "clip": {"start": 12.0, "len": 18.0, "handle": "@MrBeastGaming"},
 "reactions": [
  {"id": "r1", "t": 14.3, "quote": "How many tracks left", "text": "Counting. Out loud. Bold.", "expr": [["0", "squint"], ["1.2", "raised"]], "facts": []}
 ],
 "outro": [
  {"id": "o1", "part": "takeaway", "text": "...", "facts": ["f1"], "card": {"head": "...", "body": "..."}, "expr": [["0", "smug"]]},
  {"id": "o2", "part": "opinion", "text": "...", "facts": [], "expr": [["0", "squint"], ["1.4", "laugh"]]},
  {"id": "o3", "part": "question", "text": "...", "facts": [], "expr": [["0", "raised"], ["1.3", "glance"]]}
 ],
 "title": "short YouTube title (no claim beyond the facts)",
 "allow_terms": []
}
```
Expressions: smug laugh squint raised glance glanceL blink roll (roll takes a duration as third value). Offsets are seconds from the line start.

## After writing
`/home/williamdownard/openclaw-sites/tts-venv/bin/python render_cohost.py check mw4-dmz-extraction` shows the fact-check; fix until PASS, then `render`.
