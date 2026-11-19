import json,sys
def words(jp):
    a=json.load(open(jp))['alignment']; ch=a['characters'];st=a['character_start_times_seconds'];en=a['character_end_times_seconds']
    ws=[];cur="";s=None;pe=0
    for c,x,y in zip(ch,st,en):
        if c.isspace():
            if cur: ws.append((cur,s,pe)); cur=""
        else:
            if not cur: s=x
            cur+=c; pe=y
    if cur: ws.append((cur,s,pe))
    return ws
if __name__=="__main__":
    ws=words(sys.argv[1]); print(len(ws),'words end',round(ws[-1][2],2),'wpm',round(len(ws)/ws[-1][2]*60))
    gaps=[(round(b[1]-a[2],2),a[0],b[0]) for a,b in zip(ws,ws[1:])]
    print(sorted(gaps,reverse=True)[:6])
    sent=[g for g in gaps if g[1][-1] in '.?!']; print('sentence gaps',[g[0] for g in sent])
    print('speech time excl gaps>0.15:',round(sum(w[2]-w[1] for w in ws),2))
