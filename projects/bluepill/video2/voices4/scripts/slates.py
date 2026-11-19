import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
SET={"stability":0.75,"similarity_boost":0.75,"style":0.0,"use_speaker_boost":True,"speed":1.0}
S={"A4":"Method A, one. Daniel does everything, with tags.","A2":"Method A, two. Daniel does everything, without tags.","B":"Method B. Dialogue endpoint, library voices.","C":"Method C. Daniel, processed."}
for k,t in S.items(): el_tts("slate_"+k,*RIVER,t,SET,f"{W}/slate_{k}.mp3","eleven_multilingual_v2","reel slate")
