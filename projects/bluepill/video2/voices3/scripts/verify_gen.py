"""Step 2: render one short line per saved voice with two candidate models, same text as the chosen clip's first line. ~410 characters."""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
LINES={"ODY":"You have eaten a great deal of man's flesh, Cyclops. Have some wine.",
       "POLY":"More. Now tell me your name, and I will give you a present.",
       "CYC2":"Pollifeemus, what is wrong? Is someone killing you?",
       "CREW":"Take the cheese. Let's go."}
S={"stability":0.5,"similarity_boost":0.75,"style":0.2,"use_speaker_boost":True,"speed":1.0}
if __name__=="__main__":
    print("quota before",quota()); sv=saved()
    for role,text in LINES.items():
        for model in ("eleven_multilingual_v2","eleven_v3"):
            el_tts(f"verify_{role}_{model}",sv[role]["name"],sv[role]["voice_id"],text,S,f"{OUT}/verify/{role}_{model}.mp3",model,"step 2 verification line")
    print("quota after",quota())
