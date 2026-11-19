# CONTINUITY-PLAN.md: make every V5 plate match what is being said, what has been said, and what is coming (2026-11-13)

William's verdict on the V5 animatic: imagery is loved, but plates do not track the narration. Seven mismatches in the first 1:45 alone (boulder pushed the wrong way, "no way past that stone" shown as a door, boulder shown open while the narration says sealed, THE CAVE card on a ship shot, goatskin shot walking away from the cave, lambs shown outside a castle, the Zeus plea shown by the boat). Priority: top. Budget: image re-rolls at ~$0.036 each; expect $5-10. Workers on claude-cli/claude-sonnet-5-5.

## Root causes
1. Prompts carried no scene state (location, time, door sealed/open, who is present, action direction).
2. QA checked "on-model", never "matches the sentence".
3. Chapter cards are hard-wired to the chapter's first beat.

## Steps (run in order; each is one Sonnet worker unless noted)

### Step 1: scene-state ledger (no spend)
Worker reads `SCRIPT-V5.md` and writes `plates-v5/state.json`: for each beat id, {location, time_of_day, door: sealed|open|none, present: [odysseus, giant, crew(n), neighbours, other], action, direction (screen left/right where it matters), continuity_note}. State carries forward beat to beat and only changes when the narration changes it (door sealed at V5-033, opened at V5-056, resealed at V5-067, opened at dawn V5-105; crew count 12 -> 10 (044) -> 8 (054) -> 6 (067); location beach -> path -> cave interior -> ship from V5-127; closing chapter is non-diegetic). Also write `plates-v5/cards.json`: each chapter card moved to the first beat whose shot shows the chapter subject (THE CAVE -> V5-018 or the first cave-interior beat; THE MEALS, NOBODY, THE RAMS, THE CURSE, WHERE DID HE COME FROM? likewise). Output a short STATE-REPORT.md listing every state change with the beat that causes it.

### Step 2: match audit (no spend)
Worker views every plate `plates-v5/img/V5-NNN.png` next to its narration line, its shot text, AND its state.json entry (plus the previous and next beat lines for context) and writes `plates-v5/AUDIT.md` + `audit.json`: pass | fail with a one-line reason, categories: wrong_location, door_state, wrong_cast, wrong_count, wrong_direction, wrong_action, wrong_time, other. Batch 8 plates per view call using the chapter sheets where legible, otherwise individual images. Report the fail rate per chapter.

### Step 3: re-roll with state-injected prompts (spend, cap $10)
Worker rebuilds the prompt for every failed beat: STYLE verbatim + state line ("Inside the giant's cave at night; the cave mouth is sealed by a huge boulder; present: Odysseus and ten grey crew; no one else") + shot text + explicit direction + "no text". Re-roll, move old to img/rejects/, update manifest.json and REROLLS.md (reason: continuity). Re-audit the new plates against the same rule; a second re-roll for any still failing, max 2. Rebuild chapter sheets.

### Step 4: re-render and gate (no spend)
Update `remotion-v3` to read `plates-v5/cards.json` for card placement, then `bash render.sh animatic`. Gate: audit.json must show 0 fails before sending the video to William. Produce out/animatic_540p.mp4 + stills_sheet.jpg + a FIRST-2MIN sheet (one frame per beat for V5-001..043, labelled with the narration line) so William can verify the stretch he flagged.

### Make it permanent
Add to `refs/RECIPE-2026-11-13.md` section 4 and to the learned skill: scene-state ledger before any plate generation; sentence-match audit is a render gate; cards land on the subject, not the chapter boundary.

## Deliver to William
The animatic, the first-two-minutes sheet, fail rates before/after, spend. Ask him to re-check his seven examples by beat id: 004, 006, 034 (open-door), 012 (card), 017, 020, 037.
