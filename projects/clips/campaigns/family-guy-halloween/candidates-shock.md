# Family Guy Halloween: shock-value picks (Editor, 2026-10-29 ~12:30 ET)
Brief: find the two most jaw-drop, brand-safe beats in source/fg-p1..p6.mp4 (full transcripts in source/tr-p*.json, word timings re-run locally). Built as fg-04 and fg-05 with `clip_job.py --until thumbnail` only. Nothing hosted, scheduled, posted, submitted. review.json is not written (Morpheus approves).
Playbook basis: shock=yes only when the clip's own words state the surprising premise; hook and caption describe only what the footage shows.

## Ranking by shock
1. **fg-04** (p4 61.25-76.25): hell newcomers confess, escalating to "strangled 19 nursing students". Most "wait, did they just say that" per second, punchline in the middle of the clip, premise is a single deadpan line.
2. **fg-05** (p1 245.3-260.3): "Last thing you remember?" "Having ice cream? Then driving my family off a cliff?" then he drops out of frame with "NOOOO". Dark reveal, clean visual, slightly later hit (line lands at ~3.7-6.4 s), so the hook text carries the premise on mute.

## fg-04
- Source p4 61.25-76.25 (cut starts in the silence gap before "That's not even illegal anymore", ends in the gap after "let's just say the second thing").
- Premise: in hell's holding area, new arrivals confess their sins and each one is darker than the last.
- Transcript: "That's not even illegal anymore. I'm also Jack the Ripper. Okay, blowing by that. You, lady with crazy eyes. What did you do? I'm Catholic and I ate meat on a Friday. You don't belong here. I also strangled 19 nursing students to death. Okay, everybody, let's just say the second thing."
- Hook (7 words): "Jack the Ripper gets skipped in hell". Caption: "Hell's new arrivals confess, and it escalates." tiktok_caption has the mandatory sentence + #FamilyGuy #HuluPartner.
- shock=yes. shock_note: "I'm also Jack the Ripper." -> "Okay, blowing by that." ... "I also strangled 19 nursing students to death."
- Rule checks: guest voices: speakers are ensemble/background characters, voice actors NOT verifiable from the transcript or cast list (flag for Morpheus; no named guest, no Stewie/Brian guest). Password gag: absent (that is p3 60-66). Brand/celebrity call-outs: none in window (Jack the Ripper is a historical criminal, not a brand or celebrity; the KFC box line ends at 27.7, Matt Rife at 97, the priest line at 51-55 are all outside the window). Music: none (dialogue only). Length: 15.02 s (ffmpeg Duration, 1080x1920). Other franchises: none. Added text: hook and caption only, neutral.
- Residual risk (Morpheus to weigh): "strangled 19 nursing students" is dark; no sexual content, no slurs, no real-person target. It is a cartoon joke in the provided episode, but Disney's brand-safe clause is subjective. Contact sheet checked: hook text visible from frame 1; the scene (crowd of confessors) is readable.

## fg-05
- Source p1 245.3-260.3 (starts in the gap before "No, I'm asking you if we're dead").
- Premise: floating on rings after dying, a man tells Stewie and Brian his last memory.
- Transcript: "No, I'm asking you if we're dead. What's the last thing you remember? Uh, having ice cream? Then driving my family off a cliff? Yeah, wow. I think it's good we're not going where he's going. NOOOO!"
- Hook (7 words): "His last memory: driving off a cliff". Caption: "Stewie and Brian meet a man who remembers how it ended." tiktok_caption has the mandatory sentence + #FamilyGuy #HuluPartner.
- shock=yes. shock_note: "Uh, having ice cream? Then driving my family off a cliff?" ("Yeah, wow.")
- Rule checks: guest voices: the man is an unnamed side character; voice actor not verifiable (flag; he is not Satan or a named celebrity). Password gag: absent. Brand/celeb: none in window ("Eddie Redmayne" is at 191-197, outside). Music: none. Length: see Pipeline note. Other franchises: none. Added text neutral.
- Residual risk: dark (a character implied to have killed his family), cartoon, no gore shown. "Where he's going" is mildly religious. The scene is a plain wide shot of three rings; shock is audible, and carried on mute by the hook.

## Pipeline note
fg-04 is 15.02 s, same as approved fg-02. fg-05 renders at 15.06 s (24 fps source quantises; trims to 15.0 s trip the lint's 15 s minimum, `clip length 15.0s`). If Morpheus wants strictly <=15.0 s, the lint minimum would need loosening or a different start; I did not touch the pipeline. Schedules omitted on purpose (unscheduled; stops at thumbnail).

## Rejected moments (and why)
- p2 142.7-163 "Brian, you abandoned your wife because she had cancer ... you both beat a man to death with a bat on Christmas Eve": strong shock but speaker is the file clerk (voice unverified), cancer/weight and homicide stack is the riskiest for Disney brand-safe; backup candidate if Morpheus wants more.
- p6 131.8-149.8 they decide to leave the drowning man ("I say we leave him and just be more careful crossing the street. Look both ways"): darkly funny but needs the show context (second chance, ball ferry); premise not clear in 3 s. Third choice.
- p1 197-221 "He's likely got brain damage ... This guy's a vegetable": disability joke, named celebrity (Eddie Redmayne), Mr. Tux brand.
- p1 7-22 costume gag ("My culture is not your costume"): cultural-appropriation topic, brand-safe risk.
- p3 56 Jimmy Carter "built a house for every whore I banged" and Stephen Hawking line: real celebrities, sexual wording, disability joke.
- p3 60-66 password-sharing gag: banned by the brief.
- p4 51-55 "the children I molested": NSFW. p4 97-107 Matt Rife: celebrity call-out. p4 22 KFC box: brand.
- p2 36-41 "72 virgins ... extremist Muslim thing": religion/sexual. p2 70 Hotel California / Glen Fry / Don Felder: celebrity call-outs. p2 128 Mother Teresa: real-person call-out.
- p5 157-190 Carrier hold gag: brand call-out. p6 84.9-99.9 "all torture is back in the office": funny but not shocking and crowd voices unverified. p6 47-60 Satan "tired of being bad": no shock. Satan/Kieran Culkin beats in these parts are mild ("quit" is fg-02, already built, shock=no).
