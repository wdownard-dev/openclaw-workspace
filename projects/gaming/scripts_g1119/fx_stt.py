from faster_whisper import WhisperModel
m=WhisperModel("small.en",device="cpu",compute_type="int8")
segs,_=m.transcribe("/home/williamdownard/.openclaw/workspace/projects/gaming/work/fluxx_1119/audio.wav",word_timestamps=False,beam_size=5)
for s in segs: print(f"[{s.start:.1f}-{s.end:.1f}] {s.text}")
