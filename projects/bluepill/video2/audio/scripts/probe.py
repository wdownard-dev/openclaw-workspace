import os,sys,json
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from common import *; import tools
pid=sys.argv[1]; t0=float(sys.argv[2]); t1=float(sys.argv[3])
x=load(os.path.join(OUT,"passages",pid+".mp3"))
seg=x[int(t0*SR):int(t1*SR)]
r,H=rms_db_frames(seg,500); print("500ms rms dB:",[round(v) for v in r])
write_wav(os.path.join(OUT,"_work","_probe.wav"),seg)
segs,_=tools.model().transcribe(os.path.join(OUT,"_work","_probe.wav"),word_timestamps=True,beam_size=5,language="en",condition_on_previous_text=False)
print([ (w.word,round(w.start+t0,2)) for s in segs for w in s.words])
