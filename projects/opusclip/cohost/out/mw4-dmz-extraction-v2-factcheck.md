# Fact-check report: mw4-dmz-extraction-v2

**Result: PASS**  (structure: one_number, interrupt_level: low)

Guard: every factual claim must link to a fact whose quote was found verbatim on its official page; digits, month names and proper nouns in script lines must appear in a linked quote (or in the clip transcript near the moment). Spoken interjections must start in a transcript pause.

## Facts (all from official pages, quote checked verbatim against the fetched page)

| id | date | quote | source | verified |
|---|---|---|---|---|
| f1 | 2026-10-09 | "starting on Tuesday October 20, players who have digitally pre-ordered or pre-purchased Call of Duty®: Modern Warfare® 4 can gain Early Access to all of DMZ" | https://www.callofduty.com/blog/2026/10/call-of-duty-modern-warfare-4-dmz-how-to-play-forward-operating-base-guide | yes |
| f2 | 2026-10-23 | "Modern Warfare 4 is now live worldwide!" | https://www.callofduty.com/blog/2026/10/call-of-duty-modern-warfare-4-live-worldwide-now | yes |
| f3 | 2026-11-02 | "Season 1 arrives November 6." | https://www.callofduty.com/blog/2026/11/call-of-duty-modern-warfare-4-warzone-season-1 | yes |
| f4 | 2026-11-02 | "players will get their hands on new Multiplayer maps and modes, a new area, bosses, and other bonus content in DMZ" | https://www.callofduty.com/blog/2026/11/call-of-duty-modern-warfare-4-warzone-season-1 | yes |
| f5 | 2026-10-05 | "players loot, complete objectives, fight both enemies and rival Operators, and hope to extract with their rewards" | https://www.callofduty.com/blog/2026/10/call-of-duty-modern-warfare-4-dmz-deep-dive-hajin | yes |
| f6 | 2026-10-05 | "Call in the Twin Heli Exfil helicopter, then hold the site until it arrives as enemy pressure intensifies." | https://www.callofduty.com/blog/2026/10/call-of-duty-modern-warfare-4-dmz-deep-dive-hajin | yes |
| f7 | 2026-10-09 | "anything not placed in a Secure Slot is lost if you fail to Exfil" | https://www.callofduty.com/blog/2026/10/call-of-duty-modern-warfare-4-dmz-how-to-play-forward-operating-base-guide | yes |
| f8 | 2026-11-05 | "Criteria: Obtain 100 Points. MP: 1 Match Win = 10 Points DMZ: 1 successful Exfil = 20 Points" | https://www.callofduty.com/blog/2026/11/call-of-duty-modern-warfare-4-season-1-battle-pass-blackcell-store-bundles | yes |
| f9 | 2026-11-05 | "Expand your BlackCell Agent roster and Blueprint collection by completing in-game challenges to unlock two additional XERO Operator Skins and two additional M4 Assault Rifle Weapon Blueprints." | https://www.callofduty.com/blog/2026/11/call-of-duty-modern-warfare-4-season-1-battle-pass-blackcell-store-bundles | yes |

## Claims by script line

| line | kind | text | fact ids | status |
|---|---|---|---|---|
| i1 | interjection | Math. | - | PASS |
| i2 | interjection | Hefty. | - | PASS |
| c1 | card | In DMZ, anything not placed in a Secure Slot is lost if you fail to Exfil. | f7 | PASS |
| c2 | card | Call in the helicopter, then hold the site until it arrives. | f6 | PASS |
| c3 | card | Half a million, not yet extracted. The official word is "hope." | f5 | PASS |
| c4 | card | Season 1 adds a new DMZ area and bosses. | f3, f4 | PASS |
| o1 | outro_takeaway | One number: 20 Points per successful Exfil. | f8 | PASS |
| o2 | outro_opinion | Five exfils. Survival not included. | f8 | PASS |
| o3 | outro_question | Five exfils, or one bag? | - | PASS |

## Lines tied to the transcript

- t=12.36 s, clip says: "No" -> NULL (spoken): "Math."
- t=24.68 s, clip says: "Mr. Beast" -> NULL (spoken): "Hefty."
- t=8.56 s, clip says: "Oh my god" -> NULL (card): "In DMZ, anything not placed in a Secure Slot is lost if you fail to Exfil."
- t=18.62 s, clip says: "Oh my god" -> NULL (card): "Call in the helicopter, then hold the site until it arrives."
- t=25.74 s, clip says: "$500,000 boys" -> NULL (card): "Half a million, not yet extracted. The official word is "hope.""
- t=29.3 s, clip says: "Let's go" -> NULL (card): "Season 1 adds a new DMZ area and bosses."

## Terms allowed without a source (topic names, declared in script.json): DMZ

## Derived statements (opinion or arithmetic, not quoted facts; read against the quotes)

- o2 'Five exfils': arithmetic from f8, 100 Points needed / 20 Points per successful DMZ Exfil = 5. The page states both numbers, not the result. The 100-Point criterion belongs to BlackCell Challenge Two (f8/f9); the on-screen card says so.
- c3 'Half a million, not yet extracted': describes the clip ('$500,000 boys' said at 25.74 s) and is NULL's remark; 'hope' is from f5.
- c4 'Season 1 adds a new DMZ area and bosses': paraphrase of f4 ('a new area, bosses, and other bonus content in DMZ'), the official page gives no detail on which area or bosses; none is claimed.
- o2 'Survival not included' and o3 'one bag' are opinion/jokes about the clip, not claims about game content.
- i1 'Math.', i2 'Hefty.': jokes, no factual content.

## Limits of this check

It proves quotes exist on official pages and that numbers/names in the script come from those quotes. It does not prove the quote supports the sentence's meaning; a human (or the agent) must read each fact-linked line against its quote before publishing.
