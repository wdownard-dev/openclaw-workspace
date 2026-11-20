import sys,subprocess,os
sys.path.insert(0,"/home/williamdownard/.openclaw/workspace/projects/gaming")
import cut_moment as c
B="/home/williamdownard/.openclaw/workspace/projects/gaming/work/g1120/hd"
port=c.start_proxy()
vid=sys.argv[1]
r=subprocess.run([c.YTDLP,"--proxy",f"http://127.0.0.1:{port}","--ffmpeg-location",c.FFMPEG,"--no-warnings","-f","bv*[height<=1080]","-o",f"{B}/{vid}.%(ext)s","https://www.youtube.com/watch?v="+vid],capture_output=True,text=True,timeout=600)
print(vid,r.returncode,r.stderr[-200:])
