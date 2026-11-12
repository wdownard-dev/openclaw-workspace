import os, json, sys, urllib.request, urllib.parse, datetime
KEY=os.environ["YOUTUBE_API_KEY"]
def api(path, **p):
    p["key"]=KEY
    url="https://www.googleapis.com/youtube/v3/"+path+"?"+urllib.parse.urlencode(p)
    try:
        return json.load(urllib.request.urlopen(url, timeout=30))
    except Exception as e:
        body = getattr(e,'read',lambda:b'')().decode()[:300]
        return {"error": str(e), "body": body}
queries = [
 "greek mythology explained", "who was medusa", "who was zeus", "who was hades", "norse mythology explained",
 "egyptian gods explained", "myths that turned out to be true", "who was cleopatra", "what really happened at troy",
 "mythical creatures real animals", "who was king arthur real", "greek gods animated"
]
after=(datetime.datetime.utcnow()-datetime.timedelta(days=365)).strftime("%Y-%m-%dT00:00:00Z")
vids={}
for q in queries:
    r=api("search", part="snippet", q=q, type="video", order="viewCount", videoDuration="long", publishedAfter=after, maxResults=12, relevanceLanguage="en")
    if "error" in r:
        print("ERR", q, r); break
    for it in r.get("items",[]):
        vids.setdefault(it["id"]["videoId"], {"q":q})
ids=list(vids)
chs={}
rows=[]
for i in range(0,len(ids),50):
    r=api("videos", part="snippet,statistics,contentDetails", id=",".join(ids[i:i+50]))
    for it in r.get("items",[]):
        rows.append(it)
cids=list({it["snippet"]["channelId"] for it in rows})
for i in range(0,len(cids),50):
    r=api("channels", part="statistics,snippet", id=",".join(cids[i:i+50]))
    for it in r.get("items",[]):
        chs[it["id"]]=(int(it["statistics"].get("subscriberCount",0)), it["snippet"].get("publishedAt","")[:10], it["statistics"].get("videoCount"))
out=[]
for it in rows:
    s=it["statistics"]; v=int(s.get("viewCount",0)); c=chs.get(it["snippet"]["channelId"],(0,"",0))
    pub=it["snippet"]["publishedAt"][:10]
    out.append(dict(id=it["id"], title=it["snippet"]["title"], ch=it["snippet"]["channelTitle"], views=v, subs=c[0], chan_created=c[1], pub=pub, dur=it["contentDetails"]["duration"], q=vids[it["id"]]["q"]))
json.dump(out, open("/tmp/outlier/data.json","w"))
print(len(out), "videos", len(chs), "channels")
