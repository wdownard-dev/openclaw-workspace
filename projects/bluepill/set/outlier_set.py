import os, json, urllib.request, urllib.parse, datetime, re
KEY=os.environ["YOUTUBE_API_KEY"]
def api(path, **p):
    p["key"]=KEY
    url="https://www.googleapis.com/youtube/v3/"+path+"?"+urllib.parse.urlencode(p)
    try: return json.load(urllib.request.urlopen(url, timeout=30))
    except Exception as e:
        body=getattr(e,'read',lambda:b'')().decode()[:300]
        return {"error":str(e),"body":body}
# (character, query) ; one search each, medium bucket (4-20 min), 365 days, ordered by views
Q=[("Set","the real story of Set Egyptian god explained"),("Set","Seth vs Horus explained"),("Set","Egyptian god of chaos explained"),
   ("Set","Egyptian villain explained"),("Medusa","the real story of Medusa explained"),("Circe","the real story of Circe explained"),
   ("Gilgamesh","the real story of Gilgamesh explained"),("Baba Yaga","the real story of Baba Yaga explained"),
   ("Cu Chulainn","the real story of Cu Chulainn explained")]
after=(datetime.datetime.now(datetime.UTC)-datetime.timedelta(days=365)).strftime("%Y-%m-%dT00:00:00Z")
vids={}; used=0
for ch,q in Q:
    r=api("search",part="snippet",q=q,type="video",order="viewCount",videoDuration="medium",publishedAfter=after,maxResults=25,relevanceLanguage="en",regionCode="US")
    used+=100
    if "error" in r: print("ERR",q,r); break
    for it in r.get("items",[]): vids.setdefault(it["id"]["videoId"],{"char":ch,"q":q,"scope":"365d"})
# all-time Set search
r=api("search",part="snippet",q="Set Seth Egyptian god",type="video",order="viewCount",maxResults=25,relevanceLanguage="en",regionCode="US"); used+=100
if "error" in r: print("ERR alltime",r)
else:
    for it in r.get("items",[]): vids.setdefault(it["id"]["videoId"],{"char":"Set","q":"Set Seth Egyptian god (all time)","scope":"all"})
ids=list(vids); rows=[]
for i in range(0,len(ids),50):
    r=api("videos",part="snippet,statistics,contentDetails",id=",".join(ids[i:i+50])); used+=1
    rows+=r.get("items",[])
cids=list({it["snippet"]["channelId"] for it in rows}); chs={}
for i in range(0,len(cids),50):
    r=api("channels",part="statistics,snippet",id=",".join(cids[i:i+50])); used+=1
    for it in r.get("items",[]):
        chs[it["id"]]=dict(subs=int(it["statistics"].get("subscriberCount",0)),created=it["snippet"].get("publishedAt","")[:10],n=int(it["statistics"].get("videoCount",0)))
out=[]
for it in rows:
    c=chs.get(it["snippet"]["channelId"],dict(subs=0,created="",n=0))
    out.append(dict(id=it["id"],title=it["snippet"]["title"],ch=it["snippet"]["channelTitle"],views=int(it["statistics"].get("viewCount",0)),subs=c["subs"],chan_created=c["created"],chan_videos=c["n"],pub=it["snippet"]["publishedAt"][:10],dur=it["contentDetails"]["duration"],lang=it["snippet"].get("defaultAudioLanguage",""),**vids[it["id"]["id"] if False else it["id"]]))
json.dump(out,open("set/outlier-data-set-2026-11-18.json","w"),indent=1)
print(len(out),"videos",len(chs),"channels; quota used",used)
