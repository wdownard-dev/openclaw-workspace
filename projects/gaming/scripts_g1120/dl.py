import sys,subprocess,os
sys.path.insert(0,"/home/williamdownard/.openclaw/workspace/projects/gaming")
import cut_moment as c
B="/home/williamdownard/.openclaw/workspace/projects/gaming/work/g1120"
port=c.start_proxy()
for vid in sys.argv[1:]:
    d=f"{B}/{vid}"; os.makedirs(d,exist_ok=True)
    if any(f.startswith("src.") for f in os.listdir(d)): print(vid,"have");continue
    r=subprocess.run([c.YTDLP,"--proxy",f"http://127.0.0.1:{port}","--ffmpeg-location",c.FFMPEG,"--no-warnings","-f","bv*[height<=480]","-o",d+"/src.%(ext)s","https://www.youtube.com/watch?v="+vid],capture_output=True,text=True,timeout=600)
    print(vid,r.returncode,r.stderr[-150:],flush=True)
