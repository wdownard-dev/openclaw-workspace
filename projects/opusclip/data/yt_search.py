import sys,re,json,urllib.request,urllib.parse
q=sys.argv[1]; sp=sys.argv[2] if len(sys.argv)>2 else "CAISBAgDEAE%3D"
u="https://www.youtube.com/results?search_query="+urllib.parse.quote_plus(q)+"&sp="+sp
h=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0","Accept-Language":"en-US"}),timeout=30).read().decode()
d=json.loads(re.search(r'var ytInitialData = (\{.*?\});</script>',h,re.S).group(1))
def walk(o):
    if isinstance(o,dict):
        if 'videoRenderer' in o:
            v=o['videoRenderer']
            print(v['videoId'],'|',v['title']['runs'][0]['text'][:90],'|',v.get('ownerText',{}).get('runs',[{}])[0].get('text'),'|',v.get('publishedTimeText',{}).get('simpleText'),'|',v.get('lengthText',{}).get('simpleText'),'|',v.get('viewCountText',{}).get('simpleText'))
        for x in o.values(): walk(x)
    elif isinstance(o,list):
        for x in o: walk(x)
walk(d)
