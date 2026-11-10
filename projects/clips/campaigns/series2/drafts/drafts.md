# Series 2: LAPD Pacific Area OIS 6/5/2026 (NRF025-26), 3-part DRAFT series for wrdclipz

NOTHING posted, uploaded, scheduled, or sent to OpusClip/Buffer. Drafts only; William reviews first.

## Source
- Video: https://www.youtube.com/watch?v=a5c4-ZpEZ1A
- Uploader: Los Angeles Police Department (official channel), "Pacific Area OIS 6/5/2026 (NRF025-26)", uploaded 2026-07-17, 16:42, ~30k views. Incident date 2026-06-05, about 4:15 to 4:40 AM. Source is about 4 months old.
- Format: LAPD Critical Incident Community Briefing. Captain intro, agency captions, red-circle annotations, radio audio, official dashcam and body-worn video. No AI voice, no commentary, no music.
- Copyright risk: LOW to MEDIUM. Official agency release of public-record footage, no Content ID music; the channel states no reuse licence. Credit LAPD.
- Local files: ~/dl/series2-pacific/src.mp4 (1080p). Low-res look-over of other candidates in ~/dl/s2-*.
- Contact sheets (1 frame / 2 s of the fitted band): q1-sheet.png, q2-sheet.png, q3-sheet.png (this folder); end-frame checks in ~/.openclaw/workspace/projects/opusclip/screens/series2/end1-3.png.

## Layout and cuts
render_cut.py --blur (16:9 fitted over blurred copy), hook "PART n/3" for 4 s (same label style as the earlier LAPD test), source audio untouched, no music. Source timestamps in seconds (m:ss).

| Part | Segments | Length | Ends on |
|---|---|---|---|
| 1 | 367.6-401 (6:07-6:41) \| 425-472 (7:05-7:52) \| 492.8-500.6 (8:13-8:21) | 1:28 | LAPD's slowed, red-circled replay of the muzzle flash from the driver's window |
| 2 | 569-577 (9:29-9:37) \| 598-645.55 (9:58-10:45) | 0:56 | Officer shouts "Drop that or I'm going to f---en shoot you right now!" then silence, before the shots |
| 3 | 645.6-669 (10:46-11:09) \| 759.5-794.3 (12:39-13:14) | 0:58 | Radio: "14A67, shots fired, officer needs help!" |

## What the viewer sees
- Part 1: Official patrol dashcam, night. The driver takes off from a parking garage ("Hey, he's going to take off again" / "Heads up"), officers light him up and call the pursuit of a 211 suspect, slow-speed chase onto the 405, "SHOT FIRED", "Officer needs help, he's shooting from the vehicle", then the slowed replay circling the gun at the window. Hook: opens inside the garage with the car about to bolt; payoff is the bang at the end.
- Part 2: Dashcam: the driver stops on the 405 at Centinela, door opens, he stands in the headlight glare with hands up; LAPD circle marks the gun; "Put your hands up", "Hey, he's reloading a gun", "Hit him with the 40", "Drop that or I'm going to shoot you right now". Cliffhanger: cut on the silent beat right before the first shot (gunshot onset is at 645.8 s in the source; we end at 645.55).
- Part 3: Opens on the shots (dashcam, "SHOTS FIRED", "shots fired, officer needs help", "Don't reach for that gun", "Driver's down, not moving, no other movement from the car"), then the same seconds from an officer's body camera (door open, "He's out", "He's reloading a gun", "Where's the 40?", *SHOTS FIRED*, radio call). Part 3 deliberately replays the moment from the closer angle.

## Hook / cliffhanger summary
- Part 1 -> 2: muzzle flash reveal; viewer wants to know what happens at the next stop.
- Part 2 -> 3: threat then silence; viewer wants to hear what comes next.
- Part 3: payoff, ends on the radio call. No aftermath shown.

## Gore screening
- Frame sheets of every part viewed (1 frame per 2 s of the band) plus 0.5 s rows over the last 4 s of each part: no blood, wounds, injured person up close, or children. Suspect is shown only as a small standing figure in headlight glare (Part 2) and a small distant shape on the road after the shots (Part 3 dashcam, tiny).
- Excluded from the source on purpose: the CPR and medical aid section (about 13:42 to 14:51), the custody and EMS bodycams, the evidence slide (guns), and the line that the man was pronounced deceased. The cab-driver 911 call and robbery CCTV (0:00 to 5:40) are not used.
- Not used: captain's talking-head segments, "zoomed and slowed" title slides (except the replay itself), body-worn camera explainer b-roll.
- Flag for William: the source audio (narrator) and LAPD's red circle labels ("... firing gun", "... holding gun") name the suspect. Source audio is untouched and the labels are the agency's own annotations; our titles and descriptions below do not name him. Say so if you want those labels cropped or the narration trimmed.
- Outcome note: per LAPD the suspect died; that is only in the narrated aftermath, which is not in the parts. Titles avoid stating it.

## Proposed titles and descriptions
Part 1/3: "Driver Flees LAPD Into a Freeway Chase, Then Fires From the Window (Part 1/3)"
Per LAPD: on June 5, 2026 officers responding to a report of a robbery in the Pacific Division followed a man who drove away, and a pursuit onto the northbound 405 followed. The agency says he stopped and fired a round from his handgun out the driver's window; the slowed replay is LAPD's. These are the agency's allegations; the man is presumed innocent of any charge. Footage: Los Angeles Police Department critical incident community briefing (official release). Source: https://www.youtube.com/watch?v=a5c4-ZpEZ1A

Part 2/3: "He Stops on the 405 With a Gun. Officers: 'Drop It Or We'll Shoot' (Part 2/3)"
Per LAPD: after the pursuit the driver stopped on the northbound 405 near Centinela, exited with a handgun, and did not comply with repeated commands to drop it. Officers' dashcam. Allegations only; the man is presumed innocent. Footage: LAPD (official release). Source: https://www.youtube.com/watch?v=a5c4-ZpEZ1A

Part 3/3: "Shots Fired on the 405: LAPD Dashcam and Bodycam of the Final Seconds (Part 3/3)"
Per LAPD: the video shows the officer-involved shooting on the northbound 405. The agency says the man was armed with a handgun and did not comply; the incident is under review by LAPD's critical incident review process and the Board of Police Commissioners. Footage: LAPD (official release). Source: https://www.youtube.com/watch?v=a5c4-ZpEZ1A
(Dashcam and body-worn video, strong language in the audio.)

## Files
- part-1.mp4 (1:28), part-2.mp4 (0:56), part-3.mp4 (0:58): 1080x1920.
- part-N-preview.mp4: 540x960, crf 29, aac 96k, 5.6 / 3.4 / 3.8 MB.

## Backup candidate (not built)
LAPD Mission Area OIS 5/5/2026 (NRF023-26), https://www.youtube.com/watch?v=tnQiPLgZdW8 (13:18, release date not checked). Daylight bodycam foot pursuit of an armed carjacking suspect across 210-freeway lanes, "Put the gun down", semi-truck standoff, "SHOTS FIRED" caption (40 mm less-lethal foam round), no deaths, no blood seen on the sheets. More legible than Pacific but only about 2 minutes of strong action with replays and red-circle slides; would be a good standalone Short. Local low-res: ~/dl/s2-mission/src.mp4, 1080p: ~/dl/series2-mission/src.mp4.
