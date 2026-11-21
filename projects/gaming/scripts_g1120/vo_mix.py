#!/usr/bin/env python3
"""vo_mix.py CUT.mp4 OUT.mp4 SLUG "narration" "overlay text" : Liam VO over a cut, creator audio ducked, text line on top."""
import sys, os, json, base64, subprocess, hashlib
from PIL import Image, ImageDraw, ImageFont
B="/home/williamdownard/.openclaw/workspace/projects/gaming"; FF="/home/williamdownard/openclaw-sites/bin/ffmpeg"
cut,out,slug,text,over=sys.argv[1:6]
d=f"{B}/work/g1120/{slug}"; os.makedirs(d,exist_ok=True)
body={"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.4,"similarity_boost":0.75,"style":0.35,"use_speaker_boost":True,"speed":1.1}}
open(d+"/b.json","w").write(json.dumps(body))
r=subprocess.run(["curl","-s","-m","120","-X","POST","https://api.elevenlabs.io/v1/text-to-speech/TX3LPaxmHKxFdv7VOQHJ?output_format=mp3_44100_128","-H","xi-api-key: "+os.environ["ELEVENLABS_API_KEY"],"-H","Content-Type: application/json","-d","@"+d+"/b.json"],capture_output=True)
if r.stdout[:3]!=b"ID3" and r.stdout[:2]!=b"\xff\xfb": sys.exit("TTS ERR "+r.stdout[:200].decode("latin1"))
open(d+"/vo.mp3","wb").write(r.stdout)
im=Image.new("RGBA",(1080,170),(0,0,0,0)); dr=ImageDraw.Draw(im)
f=ImageFont.truetype("/usr/share/fonts/opentype/fira/FiraSans-ExtraBold.otf",74); tw=dr.textlength(over,font=f)
if tw>1000: f=ImageFont.truetype("/usr/share/fonts/opentype/fira/FiraSans-ExtraBold.otf",int(74*1000/tw)); tw=dr.textlength(over,font=f)
dr.text(((1080-tw)/2,40),over,font=f,fill="white",stroke_width=6,stroke_fill="black"); im.save(d+"/over.png")
cmd=[FF,"-y","-i",cut,"-i",d+"/vo.mp3","-i",d+"/over.png","-filter_complex",
 "[0:a]volume=0.12[a0];[1:a]volume=1.6,apad[a1];[a0][a1]amix=inputs=2:duration=first:normalize=0[a];[0:v][2:v]overlay=0:230:enable='between(t,0.5,6)'[v]",
 "-map","[v]","-map","[a]","-c:v","libx264","-crf","20","-preset","medium","-c:a","aac","-b:a","160k","-movflags","+faststart","-shortest",out]
r=subprocess.run(cmd,capture_output=True,text=True); print(r.returncode,r.stderr[-300:])
