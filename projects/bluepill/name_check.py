import os, json, urllib.request, urllib.parse, urllib.error, concurrent.futures as cf
KEY=os.environ["YOUTUBE_API_KEY"]
import sys
NAMES=sys.argv[1].split(",")
def yt(n):
    u="https://www.googleapis.com/youtube/v3/channels?"+urllib.parse.urlencode({"part":"snippet,statistics","forHandle":"@"+n,"key":KEY})
    try:
        d=json.load(urllib.request.urlopen(u,timeout=30)); it=d.get("items",[])
        if it: return n,"TAKEN",f'{it[0]["snippet"]["title"]} ({it[0]["statistics"].get("subscriberCount","hidden")} subs, {it[0]["statistics"].get("videoCount")} videos)'
        return n,"free",""
    except Exception as e: return n,"ERR",str(getattr(e,"read",lambda:b"")()[:150] or e)
def dom(n):
    try:
        urllib.request.urlopen(f"https://rdap.verisign.com/com/v1/domain/{n.lower()}.com",timeout=20); return "com taken"
    except urllib.error.HTTPError as e: return "com free" if e.code==404 else f"com ?{e.code}"
    except Exception as e: return "com ?"
with cf.ThreadPoolExecutor(6) as ex:
    a=list(ex.map(yt,NAMES)); b=list(ex.map(dom,NAMES))
for (n,s,i),d in zip(a,b): print(f"{n:16} yt:{s:5} {d:10} {i}")
