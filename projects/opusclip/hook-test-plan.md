# Project Red Pill: hook-text A/B test (FROZEN 2026-11-03 ~21:15 ET, before any results)

Approved by William 2026-11-03: run the test now, TikTok included, record results. Design C from hook-text-test.md (Strategist): same 4 clips, hook-text version on one platform, plain version on the other, counterbalanced.
Platforms: YouTube = wrdclipz (OpusClip acct 6aea02988e21955f59a43b64). TikTok = wrdclipz TikTok Business (OpusClip acct 6aea056ed75294f98bf78c4a), the Red Pill TikTok. NOT @rvclips6 (campaign project, kept separate).

| Slot (ET) | Clip (project.clip) | Hook version on | Plain version on | Overlay text (FROZEN) |
|---|---|---|---|---|
| Fri 11/6 11:00 AM | A1 Nate "Make it better" (rSTR.ZlEtdtwPDU) | YouTube | TikTok | Sonnet vs Opus: 100 rounds on an ugly site |
| Fri 11/6 5:00 PM | Y4 SMii7Y LeBron (rwp0.JlwLFe6hPW) | TikTok | YouTube | Monkey LeBron goes for the jump |
| Sat 11/7 5:00 PM | A2 Nate "ceiling" (rSTR.7tsdXshCzT) | TikTok | YouTube | Same prompt, two AIs, wildly different sites |
| Sun 11/8 11:00 AM | Y6 SMii7Y crab (rwp0.0SCsIK1K2M) | YouTube | TikTok | Catch the crab. It fights back. |

Treatment: custom text overlay (editor Text tab), top third clear of karaoke caption and platform UI, 0 to 2.5 s, same style on all four, no SFX, no zoom. Duplicate the clip first (free) so the original stays plain. Same title/caption pattern and source credit on both versions.
Credits: expected 0 to 2 per clip; whole test capped at 16.

Measure at 72 h (re-check 7 d), per clip and platform: primary = YouTube average % viewed; TikTok avg watch time / clip length. Secondary: YouTube viewed vs swiped away, impressions; TikTok 2 s retention; views at 24 h and 72 h; subs/followers gained; any flag or Content ID claim. Log in experiment-log.csv.

Decision rule (do not change): e = hook-platform metric minus plain-platform metric, with the average YouTube-minus-TikTok gap over all four clips removed. Use only clips with >= 200 views on each platform (else wait to 7 d; < 3 usable = not enough data).
- Adopt if mean e >= +5 points, >= 3 of 4 clips positive, none <= -5.
- Drop if mean e <= 0 or >= 2 clips negative.
- Otherwise one extension round of 4 clips; adopt only if >= 6 of 8 positive and mean e >= +4.
Report a pass as "directional signal", not proof (3 of 4 positive happens 31% by luck).
Auto headline (`enableAutoHook` in opus.py submit): only after William and I discuss results (William, 2026-11-03).
