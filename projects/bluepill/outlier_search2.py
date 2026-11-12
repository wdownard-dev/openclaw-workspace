import os, json, urllib.request, urllib.parse, datetime
KEY=os.environ["YOUTUBE_API_KEY"]
def api(path, **p):
    p["key"]=KEY
    url="https://www.googleapis.com/youtube/v3/"+path+"?"+urllib.parse.urlencode(p)
    try:
        return json.load(urllib.request.urlopen(url, timeout=30))
    except Exception as e:
        body = getattr(e,'read',lambda:b'')().decode()[:300]
        return {"error": str(e), "body": body}
queries = ["every greek god explained","greek mythology explained","mythology animated explained","norse mythology explained",
 "egyptian mythology explained","myths that turned out to be true","mythical creatures that turned out to be real",
 "mesopotamian mythology explained","slavic mythology explained","japanese mythology explained","celtic mythology explained",
 "aztec mythology explained","mythology stick figure animation","greek mythology villains explained"]
after=(datetime.datetime.now(datetime.UTC)-datetime.timedelta(days=365)).strftime("%Y-%m-%dT00:00:00Z")
vids={}; used=0
for q in queries:
    for bucket in ("medium","long"):
        r=api("search", part="snippet", q=q, type="video", order="viewCount", videoDuration=bucket, publishedAfter=after, maxResults=15, relevanceLanguage="en", regionCode="US")
        used+=100
        if "error" in r:
            print("ERR", q, bucket, r); raise SystemExit
        for it in r.get("items",[]):
            vids.setdefault(it["id"]["videoId"], {"q":q,"bucket":bucket})
ids=list(vids); rows=[]
for i in range(0,len(ids),50):
    r=api("videos", part="snippet,statistics,contentDetails", id=",".join(ids[i:i+50])); used+=1
    rows+=r.get("items",[])
cids=list({it["snippet"]["channelId"] for it in rows}); chs={}
for i in range(0,len(cids),50):
    r=api("channels", part="statistics,snippet", id=",".join(cids[i:i+50])); used+=1
    for it in r.get("items",[]):
        chs[it["id"]]=dict(subs=int(it["statistics"].get("subscriberCount",0)), created=it["snippet"].get("publishedAt","")[:10], n=int(it["statistics"].get("videoCount",0)), country=it["snippet"].get("country",""))
out=[]
for it in rows:
    c=chs.get(it["snippet"]["channelId"],dict(subs=0,created="",n=0,country=""))
    out.append(dict(id=it["id"], title=it["snippet"]["title"], ch=it["snippet"]["channelTitle"], chid=it["snippet"]["channelId"], views=int(it["statistics"].get("viewCount",0)),
      likes=int(it["statistics"].get("likeCount",0)), comments=int(it["statistics"].get("commentCount",0)), subs=c["subs"], chan_created=c["created"], chan_videos=c["n"], country=c["country"],
      pub=it["snippet"]["publishedAt"][:10], dur=it["contentDetails"]["duration"], lang=it["snippet"].get("defaultAudioLanguage",""), q=vids[it["id"]]["q"]))
json.dump(out, open("/tmp/outlier/data2.json","w"))
print(len(out),"videos",len(chs),"channels","quota used ~",used)
