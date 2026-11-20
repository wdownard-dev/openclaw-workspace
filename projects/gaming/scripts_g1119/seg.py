#!/usr/bin/env python3
"""seg.py VID START END NAME : download video-only <=720p section to work/g1119/seg/NAME.mp4 (src time START maps to t=0)."""
import sys,os,glob,subprocess
B="/home/williamdownard/.openclaw/workspace/projects/gaming"; sys.path.insert(0,B)
import cut_moment as c
vid,s,e,name=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
d=f"{B}/work/g1119/seg"; os.makedirs(d,exist_ok=True)
for o in glob.glob(f"{d}/{name}.*"): os.remove(o)
port=c.start_proxy()
r=subprocess.run([c.YTDLP,"--no-warnings","--proxy",f"http://127.0.0.1:{port}","--download-sections",f"*{s}-{e}","--force-keyframes-at-cuts","--ffmpeg-location",c.FFMPEG,"-f","bv*[height<=720]","-o",f"{d}/{name}.%(ext)s",f"https://www.youtube.com/watch?v={vid}"],capture_output=True,text=True,timeout=900)
fs=glob.glob(f"{d}/{name}.*")
if not fs: sys.exit("FAIL "+r.stderr[-300:])
print("OK",fs[0],c.probe(fs[0]))
