import sys,subprocess,json
sys.path.insert(0,"/home/williamdownard/.openclaw/workspace/projects/gaming")
import cut_moment as c
port=c.start_proxy()
qs=sys.argv[1:]
for q in qs:
    r=subprocess.run([c.YTDLP,"--proxy",f"http://127.0.0.1:{port}","--no-warnings","--flat-playlist","-j","https://www.youtube.com/results?search_query="+q.replace(" ","+")+"&sp=CAISBAgCEAE%253D"],capture_output=True,text=True,timeout=170)
    print("##",q)
    for l in r.stdout.splitlines():
        try:j=json.loads(l)
        except: continue
        print(j.get("id"),"|",j.get("channel"),"|",j.get("title")[:80],"|",j.get("duration"),"|",j.get("view_count"),"|",j.get("upload_date") or j.get("release_timestamp"))
    if not r.stdout: print(r.stderr[-300:])
