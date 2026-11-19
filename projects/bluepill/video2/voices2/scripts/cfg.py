"""Config for voice round 2 (video 1, Project Blue Pill). Texts come from SCRIPT-V3.md beats; names respelled as in video1/voice.py."""
import os
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.dirname(HERE); OLD=os.path.join(os.path.dirname(OUT),"voices")
FF="/home/williamdownard/openclaw-sites/bin/ffmpeg"
FMT="mp3_44100_128"
DANIEL=("Daniel","onwK4e9ZLuTAKqWW03F9")
RIVER=("River","SAz9YHcvj6GT2YYXdXww")
# round-1 long cold open (beats 01, 02, 08, 11) used for the 'L' clips
N_LONG=("Twelve men follow Odysseus into a cave. Six of them get out. A giant ate the other six, the one-eyed kind. "
        "So where did he come from? Racks of cheese. Pens full of lambs. Nobody home. "
        "The cleverest man in the poem is waiting for a gift basket from a stranger's cave.")
TAG_A="[dry, deadpan, amused documentary narrator]"
TAG_B="[wry, unhurried, quietly amused]"
S_R1 ={"stability":0.5,"similarity_boost":0.75,"style":0.2,"use_speaker_boost":True,"speed":1.0}
S_V1 ={"stability":0.5,"similarity_boost":0.75,"style":0.25,"use_speaker_boost":True,"speed":1.1}
S_V4 ={"stability":0.5,"similarity_boost":0.75,"style":0.2,"use_speaker_boost":True,"speed":1.0}
S_V4F={"stability":0.5,"similarity_boost":0.75,"style":0.2,"use_speaker_boost":True,"speed":1.1}
S_V4G={"stability":0.5,"similarity_boost":0.75,"style":0.2,"use_speaker_boost":True,"speed":1.2}
# (clip id, file stem, model, text, settings, label, note)
NARR=[
 ("D1","D1_multilingual_v2_speed1.1_style0.25","eleven_multilingual_v2",N_LONG,S_V1,"multilingual_v2, stability 0.5, style 0.25, speed 1.1","variant 1"),
 ("D2a","D2a_v4_tagA_speed1.0","eleven_v4",TAG_A+" "+N_LONG,S_V4,"eleven_v4, tag "+TAG_A+", speed 1.0","variant 2, tag A (round-1 tag)"),
 ("D2b","D2b_v4_tagB_speed1.0","eleven_v4",TAG_B+" "+N_LONG,S_V4,"eleven_v4, tag "+TAG_B+", speed 1.0","variant 2, tag B (new tag)"),
 ("D3","D3_v4_tagA_speed1.1","eleven_v4",TAG_A+" "+N_LONG,S_V4F,"eleven_v4, tag "+TAG_A+", speed 1.1","variant 3, v4 + tag A + speed 1.1"),
 ("D5","D5_v4_tagA_speed1.2","eleven_v4",TAG_A+" "+N_LONG,S_V4G,"eleven_v4, tag "+TAG_A+", speed 1.2 (maximum)","bonus variant, v4 + tag A + speed 1.2 (not requested; tests whether more speed closes the pace gap)"),
 ("D4","D4_control_r1_multilingual_v2","eleven_multilingual_v2",N_LONG,S_R1,"multilingual_v2, stability 0.5, style 0.2, speed 1.0 (round-1 settings, control)","variant 4, control"),
]
# role texts (SCRIPT-V3 beats)
T={
 "ODY":"You have eaten a great deal of man's flesh, Cyclops. Have some wine.\n\nMy name is Nobody.\n\nI am honoured.\n\nKeep your presents. I would send you to Hades if I could. Not even Poseidon will heal that eye.",
 "POLY_NOBODY":"More. Now tell me your name, and I will give you a present.\n\nNobody. Then here is my present, Nobody. I will eat Nobody's friends first, and Nobody last.",
 "POLY_RAM":"My good ram. You are always first out. Why are you last today? Are you sorry for your master's eye?",
 "POLY_PRAYER":"Father Poseidon, hear me. Never let Odysseus reach his home. Or if he must, let him come late, in misery, and with all his men lost.",
 "CYC2":"Pollifeemus, what is wrong? Is someone killing you?\n\nThen nobody is hurting you. It must be a sickness from Zeus. Pray to your father, and let us sleep.\n\nSheep.",
 "CREW":"Take the cheese. Let's go.\n\nHello?\n\nNope.\n\nPlease stop. He already threw one rock. He can throw another.\n\nWhere's the nose?",
}
# one-word / short lines to check for flatness (words)
ONEWORDS={"ODY":[],"POLY_NOBODY":["Nobody."],"CYC2":["Sheep."],"CREW":["Hello?","Nope."],"POLY_RAM":[],"POLY_PRAYER":[]}
# eleven_v4 acting tags per role (prepended)
TAGS={"ODY":"[dry, amused, controlled]","POLY_NOBODY":"[gentle, slow, enormous]","POLY_RAM":"[gentle, slow, enormous]","POLY_PRAYER":"[gentle, slow, enormous, solemn]",
      "CYC2":"[bored, flat, deadpan]","CREW":"[earnest, nervous]"}
# library voices, best 3 per role by round-1 metadata/measure (voice ids from voices/scripts/catalog.py)
LIB={
 "ODY":[("C02","JustinTrustingCalm","NyBVtlh1XAem9yCxNuWk"),("C01","DanielWarmBaritone","rFhx8PVgXxOyaeAGq9fq"),("C03","RyanUnhurried","gBDv2oGht23KfZZMSUEi")],
 "POLY":[("C06","UjjalSleepy","SIhHalPo6AKqWOgqhp9R"),("C04","MichaelMoody","PerZoH0r6nxBZXCoIPpv"),("C05","PhilipQuietAuthority","exurTFaGNF2gnRcPNH8I")],
 "CYC2":[("C07","DrewDeadpan","lCfIptVKzlPoj4vLmTLz"),("C09","DeadpanCynic","RIxlkEgVTlW2XuYWyYjL"),("C08","DannyMonotone","Nagtyt9MktF8AWSgjotJ")],
 "CREW":[("C11","LukasExcitedYouth","wSqOdjeNqDrHcoK0zorF"),("C10","HarryAnxiousFighter","SOYHLrjzK2X1ezoPC6cr"),("C12","TimmyAnxiousNerd","mrQhZWGbb2k9qWJb5qeA")],
}
ROLE_TEXTS={"ODY":["ODY"],"POLY":["POLY_NOBODY","POLY_RAM","POLY_PRAYER"],"CYC2":["CYC2"],"CREW":["CREW"]}
# Voice Design prompts: Native language. Gender, age. Quality. Persona. Emotion. timbre/pacing. Three different per role.
D=lambda s:s
DESIGN={
 "ODY":[
  ("A","Native English, light Mediterranean-tinged speech, a faint Greek-Cypriot lilt without caricature. Male, 40-45. Studio quality. Persona: wry ship captain, clever and controlled. Emotion: amused, dry, composed. Warm mid-baritone with a smooth, slightly husky timbre; unhurried, precise pacing with the faintest smile in the voice, intelligent understatement, never heroic or trailer-like."),
  ("B","Native English, neutral American, general Midwest, mild and unforced. Male, 35-40. Studio quality. Persona: dry-witted engineer who has seen everything. Emotion: amused, calm, mildly sardonic. Warm, medium-low baritone with a relaxed, conversational timbre; moderate pace, light ironic emphasis, controlled and a little tired, not dramatic."),
  ("C","Native English, soft Scottish lowland intonation, understated. Male, 50-55. Very good quality. Persona: seasoned, sharp-eyed negotiator. Emotion: wry, patient, quietly confident. Rich lower-mid baritone with a dry, slightly gravelly texture; measured pace with small deadpan pauses, intelligent and amused, never booming."),
 ],
 "POLY":[
  ("A","Native English, deep rural American South, slow and soft. Male, 45-55. Studio quality. Persona: enormous gentle shepherd, simple and sincere. Emotion: gentle, earnest, puzzled. Very deep, low-pitched, gravelly bass with a warm, rumbling timbre; slow, deliberate pacing, childlike literalness, no villain growl."),
  ("B","Native English, rural West Country England, thick and warm. Male, 55-65. Good quality. Persona: huge, lonely farmer who talks to his sheep. Emotion: tender, sincere, a little sad. Extremely deep, resonant bass-baritone with a rough, breathy texture; very slow pace with long soft vowels, simple and trusting, never menacing."),
  ("C","Native English, heavy Newfoundland-style rural intonation, unhurried. Male, 60-65. Good quality. Persona: gentle giant, big-hearted and slow of thought. Emotion: kind, earnest, innocent. Deep, booming yet soft bass with a gravelly, worn timbre; slow, steady pacing, sincere and literal-minded, warm rather than threatening."),
 ],
 "CYC2":[
  ("A","Native English, gruff Northern English, thick Yorkshire-style intonation. Male, 45-50. Good quality. Persona: grumpy neighbour woken in the middle of the night. Emotion: bored, irritated, flat. Mid-low, rough, nasal timbre; slow, sighing, monotone delivery with weary emphasis, working-class and unimpressed."),
  ("B","Native English, Midlands (Black Country style) intonation, plain and flat. Male, 55-60. Good quality. Persona: tired pub regular who has heard every excuse. Emotion: deadpan, weary, put-upon. Low-mid, dry and slightly raspy; slow pace, very little pitch variation, mumbling a little, bored.")  ,
  ("C","Native English, Northern Irish-tinged working-class speech, blunt and sleepy. Female, 40-50. Good quality. Persona: irritated neighbour in a dressing gown. Emotion: flat, annoyed, tired. Low-mid, gravelly, a little hoarse from sleep; unhurried, monotone with sharp tired sighs, unimpressed."),
 ],
 "CREW":[
  ("A","Native English, soft Irish lilt, light and natural. Male, 20-25. Good quality. Persona: nervous young sailor, an everyman. Emotion: earnest, frightened, breathless. Mid-high, slightly thin and boyish timbre; quick, breathy pacing with small catches in the voice, sincere and a little out of breath."),
  ("B","Native English, West Country England, mild rural intonation. Male, 20-25. Good quality. Persona: honest young deckhand out of his depth. Emotion: anxious, earnest, worried. Mid-high, bright and slightly nasal; fast, breathless delivery, rising worried inflection, plain and sincere."),
  ("C","Native English, neutral American with a hint of Appalachian twang. Male, 18-22. Good quality. Persona: scared young crewman trying to stay brave. Emotion: nervous, earnest, shaky. High-mid, light and slightly cracked timbre; rapid breathless speech, tense and sincere, not comedic."),
 ],
}
DESIGN_TEXT={"ODY":T["ODY"],"POLY":T["POLY_NOBODY"],"CYC2":T["CYC2"],"CREW":T["CREW"]}
# OpenAI gpt-4o-mini-tts: (voice, instruction) per role
OA={
 "ODY":[("ash","Voice: warm, dry mid-baritone, wry and controlled, intelligent and quietly amused. Delivery: unhurried, understated, a faint smile in the voice, deadpan on 'My name is Nobody.' and 'I am honoured.' Never heroic, never trailer-like."),
        ("onyx","Voice: a calm low baritone, dry and amused. Delivery: measured and precise, light irony, composed, like a clever man hiding a joke. No dramatic emphasis."),
        ("echo","Voice: easy mid-range male, sardonic and relaxed. Delivery: conversational, controlled, dry humour, not heroic.")],
 "POLY":[("onyx","Voice: enormous, very deep, slow. Delivery: gentle, simple sincerity with childlike literalness, gravelly but not a villain, no growl, warm and trusting."),
         ("ash","Voice: very deep and gravelly, huge and soft-spoken. Delivery: slow, deliberate, sincere, almost tender, innocent and literal, never menacing."),
         ("ballad","Voice: low, rumbling, slow and wounded. Delivery: gentle sincerity, simple and childlike, heavy with feeling but not theatrical, no villain growl.")],
 "CYC2":[("echo","Voice: bored, flat, tired working-class neighbour woken at night. Delivery: monotone, irritated, sighing, mid-low register, no energy, zero enthusiasm, the one word 'Sheep.' dead and flat."),
         ("sage","Voice: weary, flat, gruff. Delivery: deadpan, bored, put-upon, slow, as if woken at three in the morning and unimpressed."),
         ("fable","Voice: low-energy, nasal and fed up. Delivery: flat, irritated, sleepy, working-class, monotone with weary sighs.")],
 "CREW":[("verse","Voice: young, earnest everyman sailor, mid-high, a little frightened. Delivery: breathless, quick, nervous, sincere; 'Nope.' short and scared, 'Where's the nose?' puzzled."),
         ("alloy","Voice: young man, nervous and honest. Delivery: shaky, breathy, earnest, worried, not comedic."),
         ("coral","Voice: young, bright and anxious. Delivery: fast, breathless, earnest, a little scared, plain and sincere.")],
}
