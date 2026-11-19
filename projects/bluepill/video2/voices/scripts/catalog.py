"""Audition catalog for Project Blue Pill video 1 voices. Voice IDs come from the ElevenLabs account/shared library (see _work/*.json)."""
# (clip id, voice name, voice_id, source, style note)
NARRATORS = [
 ("N01","George","JBFqnCBsd6RMkjVDRZzb","premade","V1 control: warm British storyteller"),
 ("N02","Daniel","onwK4e9ZLuTAKqWW03F9","premade","British steady broadcaster"),
 ("N03","OliverSilk","jfIS2w2yJi0grJZPyEsk","shared","deep British RP, 'optimized for sarcasm'"),
 ("N04","MichaelDan","QngvLQR8bsLR5bzoa6Vv","shared","British documentary, natural pacing"),
 ("N05","NathanielC","z7i51AlFqQJ8JzM16o7e","shared","British character actor/comedian, documentary"),
 ("N06","StephenDavis","F7n0VEnrij6y8mtpFPfu","shared","British, upbeat, subtly sarcastic"),
 ("N07","Russell","NYC9WEgkq1u4jiqBseQ9","shared","British, fast, dramatic TV documentary"),
 ("N08","HeyItsBrad","Dslrhjl3ZpzrctukrQSN","shared","American documentary, casual, edgy"),
 ("N09","SpudsOxley","NOpBlnGInO9m6vDvFkFC","shared","Southern grandpa tall-tale teller"),
 ("N10","LiamCallahan","ZIGffU92feoE7QFrof7N","shared","gruff witty American podcaster"),
 ("N11","JarnathanCross","7WggD3IoWTIPT19PNyrW","shared","witty, knowing, poised American"),
 ("N12","Kurt","42MPlPHxazRyNGWpSUyy","shared","wry but likable young American"),
 ("N13","AlexSouthern","LoowaiYE6qY0n5fRDzAX","shared","soft Southern tenor storyteller"),
]
# role -> list of (clip id, voice name, voice_id, source, note)
CHARS = {
 "ODY": [("C01","DanielWarmBaritone","rFhx8PVgXxOyaeAGq9fq","shared","warm low-mid baritone, slightly gravelly"),
         ("C02","JustinTrustingCalm","NyBVtlh1XAem9yCxNuWk","shared","deep warm baritone, dry understated humour"),
         ("C03","RyanUnhurried","gBDv2oGht23KfZZMSUEi","shared","unhurried, dry wit, disaffected charm")],
 "POLY": [("C04","MichaelMoody","PerZoH0r6nxBZXCoIPpv","shared","grandfatherly, warm, deep, velvety"),
          ("C05","PhilipQuietAuthority","exurTFaGNF2gnRcPNH8I","shared","deep, slow, deliberate baritone"),
          ("C06","UjjalSleepy","SIhHalPo6AKqWOgqhp9R","shared","bass-baritone, sleepy, slow, calm")],
 "CYC2": [("C07","DrewDeadpan","lCfIptVKzlPoj4vLmTLz","shared","deadpan, sarcastic, vocal fry"),
          ("C08","DannyMonotone","Nagtyt9MktF8AWSgjotJ","shared","quirky Midwestern, deep monotone"),
          ("C09","DeadpanCynic","RIxlkEgVTlW2XuYWyYjL","shared","low-energy fatalist, slight lisp")],
 "CREW": [("C10","HarryAnxiousFighter","SOYHLrjzK2X1ezoPC6cr","premade","'excited but slightly anxious fighter'"),
          ("C11","LukasExcitedYouth","wSqOdjeNqDrHcoK0zorF","shared","passionate, hopeful young man"),
          ("C12","TimmyAnxiousNerd","mrQhZWGbb2k9qWJb5qeA","shared","shy, nasal, nervous, stutters")],
}
SLATE_VOICE = ("River","SAz9YHcvj6GT2YYXdXww")   # premade, relaxed neutral; fixed for every slate

# Test scripts (words from SCRIPT-V3.md; names respelled as in video1/voice.py)
N_SHORT = ("Twelve men follow Odysseus into a cave. Six of them get out. "
           "The cleverest man in the poem is waiting for a gift basket from a stranger's cave.")      # beats 01, 11
N_LONG = ("Twelve men follow Odysseus into a cave. Six of them get out. A giant ate the other six, the one-eyed kind. "
          "So where did he come from? Racks of cheese. Pens full of lambs. Nobody home. "
          "The cleverest man in the poem is waiting for a gift basket from a stranger's cave.")      # beats 01, 02, 08, 11
C_TEXT = {
 "ODY": "You have eaten a great deal of man's flesh, Cyclops. Have some wine.\n\nMy name is Nobody.\n\nI am honoured.\n\nAnd then who moves the stone?\n\nAh.\n\nThen it was a short plan.",
 "POLY": "More. Now tell me your name, and I will give you a present.\n\nNobody. Then here is my present, Nobody. I will eat Nobody's friends first, and Nobody last.\n\nMy good ram. You are always first out. Why are you last today?",
 "CYC2": "Pollifeemus, what is wrong? Is someone killing you?\n\nThen nobody is hurting you. It must be a sickness from Zeus. Pray to your father, and let us sleep.\n\nSheep.",
 "CREW": "Take the cheese. Let's go.\n\nAnd if he wakes up?\n\nPlease stop. He already threw one rock. He can throw another.\n\nHello?\n\nNope.\n\nWhere's the nose?",
}
SET_PERF_N = {"stability":0.5,"similarity_boost":0.75,"style":0.2,"use_speaker_boost":True,"speed":1.0}
SET_V1     = {"stability":0.75,"similarity_boost":0.75,"style":0.05,"use_speaker_boost":True,"speed":1.0}
SET_ACT    = {"stability":0.4,"similarity_boost":0.75,"style":0.3,"use_speaker_boost":True,"speed":1.0}
SET_CHAR   = {"stability":0.4,"similarity_boost":0.75,"style":0.3,"use_speaker_boost":True,"speed":1.0}
MODEL="eleven_multilingual_v2"
