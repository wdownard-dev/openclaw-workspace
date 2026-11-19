import json,statistics as st,sys
R='/home/williamdownard/.openclaw/workspace/projects/bluepill/analysis_teardown_out/'
def shots_for(name,total,minfrac=0.3,mingap=0.45):
    ev=json.load(open(R+name+'.events.json'))
    cuts=[0.0]
    for e in ev:
        if e['frac']>=minfrac and e['t']-cuts[-1]>=mingap: cuts.append(e['t'])
    cuts.append(total)
    shots=[]
    for a,b in zip(cuts[:-1],cuts[1:]):
        inner=[e for e in ev if a<e['t']<b]
        shots.append(dict(start=a,end=b,len=b-a,pop=sum(1 for e in inner if 0.1<=e['frac']<minfrac),micro=sum(1 for e in inner if e['frac']<0.1)))
    return shots
for name,total in (('ref',788.64),('ours',612.8)):
    sh=shots_for(name,total)
    L=sorted(s['len'] for s in sh)
    n=len(sh)
    q=lambda p:L[min(n-1,int(p*n))]
    print(name,'shots',n,'per min',round(n/(total/60),1),'mean',round(sum(L)/n,2),'median',round(st.median(L),2),'p10',round(q(.1),2),'p90',round(q(.9),2),'max',round(L[-1],1))
    bins=[(0,1),(1,2),(2,3),(3,4),(4,6),(6,8),(8,12),(12,999)]
    print('  len hist',[ (a,b,sum(1 for x in L if a<=x<b)) for a,b in bins])
    print('  pop-ins per shot mean',round(sum(s['pop'] for s in sh)/n,2),'shots with >=1 pop',sum(1 for s in sh if s['pop']>0),'micro per shot',round(sum(s['micro'] for s in sh)/n,2))
    json.dump(sh,open(R+name+'.shots.json','w'))
