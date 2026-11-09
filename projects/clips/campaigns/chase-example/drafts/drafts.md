# Chase series example: DRAFT ONLY (nothing posted, uploaded, scheduled, or sent to OpusClaw/Buffer)

## Source
- ABC7 Los Angeles, "FULL CHASE: Speeding suspect leads deputies on chase through Downey/Norwalk"
- https://www.youtube.com/watch?v=Lg--YZJ7fj8 (streamed/uploaded 2026-11-03, 10:45, 720p60, AIR7 helicopter, daytime)
- Local copy: ~/dl/chase-abc7/src.mp4. Auto-captions: ~/dl/chase-abc7-subs/s.en.vtt
- Copyright/Content ID risk (third-party TV news footage, not an agency release): ABC7/Disney owns it. Expect a Content ID claim, with a real chance of a copyright strike or demonetization or takedown if posted. Attribute to ABC7 / LA County Sheriff's Department, but attribution is not a license.
- Visible on-screen: ABC7 logo, lower-third ("SHERIFF PURSUIT" / "DEPUTIES CHASING SUSPECT..."), SKY/AIR7 location bar. They sit on the news graphics, not over the car. Anchor and reporter commentary is the live source audio, untouched.

## Parts (source timestamps in seconds; cut at sentence-end pauses)
| Part | Source range | Length | What happens | Ends on |
|---|---|---|---|---|
| 1/4 | 0:00-2:51.4 (0-171.4) | 2:51 | AIR7 picks up the LA County Sheriff's pursuit on surface streets after a missed spike strip; erratic stretches, red light blown, U-turns, curb strike | Turn onto a smaller side street ("...onto a smaller surface street.") |
| 2/4 | 2:51.4-5:21.2 (171.4-321.2) | 2:30 | Side streets, near cul-de-sac, suspect appears to throw an item out the window, ducks into a parking lot and back out past deputies, wobbly rear tire, another U-turn | "...westbound on Downey Avenue." |
| 3/4 | 5:21.2-7:45 (321.2-465.0) | 2:24 | Pursuit continues, close call with a pedestrian, suspect pulls into a lot, deputies box him in, guns drawn | "Sheriff's Department has guns drawn right now." (cliffhanger) |
| 4/4 | 7:45-9:00.35 (465.0-540.35) | 1:15 | Suspect keeps trying to drive off, is boxed in, driver door opened, taken into custody in handcuffs; AIR7 wrap-up | "...in that same area." |
Dropped: 9:00-10:45 (anchor chatter over the arrest scene, then handoff to election coverage and studio shot).

## Render
render_cut.py --blur (16:9 fitted band over a blurred copy), 1080x1920, 30fps, source audio untouched, "PART n/4" label for the first 4 s only, no music, no other text. Files are about 40-110 MB each (high bitrate, CRF 20).
Files: ~/.openclaw/workspace/projects/clips/campaigns/chase-example/drafts/part-1.mp4 ... part-4.mp4
Contact sheets: ~/.openclaw/workspace/projects/opusclip/screens/chase-example/part-1.jpg ... part-4.jpg

## Gore screening
Viewed contact sheets of all 4 parts and the full source (every 10 s): aerial daytime shots only. No blood, no injury, no person down. The arrest is wide-angle, with deputies around the car and the suspect cuffed. Clean. No child or sexual-violence content.

## Proposed titles and descriptions (confirmed facts only; verify against ABC7 before any posting)
1. **Deputies Chase Speeding Suspect Through Downey and Norwalk | Part 1/4**
   LA County Sheriff's deputies pursued a driver wanted for excessive speed in the Downey-Norwalk area on Tuesday, Nov. 3. A spike strip missed. Aerial video from ABC7's AIR7. Source: ABC7 Los Angeles.
2. **Suspect Ducks Into a Parking Lot, Then Bolts Back Out | Part 2/4**
   The pursuit continues on side streets as the driver pulls U-turns and appears to throw an item from the car. Aerial video from ABC7's AIR7. Source: ABC7 Los Angeles.
3. **Deputies Box In the Car, Guns Drawn | Part 3/4**
   After a close call near a pedestrian, the driver pulls into a parking lot and deputies move in. Aerial video from ABC7's AIR7. Source: ABC7 Los Angeles.
4. **The Pursuit Ends: Suspect Taken Into Custody | Part 4/4**
   Deputies box in the car near Alondra Boulevard and Downey Avenue and take the driver into custody after about 15 minutes. Aerial video from ABC7's AIR7. Source: ABC7 Los Angeles.
(Avoid guessing the motive. The sheriff's department had not stated a reason beyond excessive speed on air.)
