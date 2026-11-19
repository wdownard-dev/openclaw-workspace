import json,re,statistics as st
R='/home/williamdownard/.openclaw/workspace/projects/bluepill/'
O=R+'analysis_teardown_out/'
# ---- build sentence lists
def sentences_from_words(ws, key='text'):
    out=[];cur=[];t0=None
    for w in ws:
        if t0 is None:t0=w['start']
        cur.append(w[key])
        if re.search(r'[.?!]["”\']?$',w[key]) and not re.fullmatch(r'(Mr|Mrs|Dr|St)\.',w[key]):
            out.append((t0,' '.join(cur)));cur=[];t0=None
    if cur:out.append((t0,' '.join(cur)))
    return out
ref=json.load(open(O+'ref_words.json'))
ours=json.load(open(R+'video1/audio/words.json'))
ref_s=sentences_from_words(ref); our_s=sentences_from_words(ours)
ref_dur=ref[-1]['start']/60.0   # minutes of speech
our_dur=ours[-1]['end']/60.0
ref_total=788.64/60; our_total=612.8/60

def toks(s): return re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*",s)
def lc(s): return [t.lower() for t in toks(s)]
NUMW=set('two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred hundreds thousand thousands dozen million'.split())
def has_num(s):
    for t in toks(s):
        tl=t.lower()
        if re.search(r'\d',t): return True
        if any(p in NUMW for p in re.split(r'[-]',tl)): return True
    return False
SECOND={'you','your',"you're","you'd","you'll","you've",'yours','yourself',"let's",'us'}
FIRSTPL={'we',"we're","we'll","we've",'our','ours','us',"let's"}
HEDGE=set('may might perhaps possibly probably maybe argue argues argued suggest suggests suggested claim claims claimed theory hypothesis plausible unproven proven prove proof evidence likely unlikely apparently presumably seems seem appears appear could "arguably" implies imply speculation speculate suspect suspected sometimes'.split())
ATTR=set('says said writes wrote written argues argued reports reported claims claimed suggests suggested puts calls called lists listed names named notes noted mentions mentioned according adds added states stated describes described compares compared concluded conclude dates dated'.split())
# concrete physical/plot action verbs (stems; match with simple inflection)
ACT=set('''grab smash eat ate eaten drive drove driven shout scream run ran climb burn kill turn rolled roll sail raid party stay come came return blow blew hurl spear attack escape flee drag throw threw hit fire shoot string strap tie untie sharpen heat stab blind drown split slaughter wake sleep fall fell wash cling build sit cry beg dig fill summon embrace slip plug steer snatch rush gather open close push pull carry carried steal chase fight drink dig swing break broke smash storm land lift hold held hide hid walk dance wave kick jump leave left reach enter hunt lure die died die kneel stand stood sail row rise rose rain sink sank crash trap trapped devour devoured feast swallow bite laugh mock march charge capture seize seized slay slew pluck draw drew tear tore wield wove weave unravel announce'''.split())
CLAIM=set('say says said argue argues argued think thought suggest suggests claim claims report reports note notes call calls called name names list lists write writes wrote mention mentions believe believes know knows known prove proves find found date dates compare compares count counted explain explains conclude concludes imply implies describe describes consider considers point turn out put puts mean means'.split())
def stem_match(tok,S):
    t=tok.lower()
    if t in S:return True
    for suf in ('s','es','ed','ing','d'):
        if t.endswith(suf) and t[:-len(suf)] in S:return True
    if t.endswith('ied') and t[:-3]+'y' in S: return True
    return False
def analyse(name,sents,mins_speech,total_min,words):
    ws=[len(toks(s)) for _,s in sents]
    n=len(sents)
    all_t=[t for _,s in sents for t in toks(s)]
    N=len(all_t)
    q=sum(1 for _,s in sents if s.rstrip().endswith('?'))
    ex=sum(1 for _,s in sents if s.rstrip().endswith('!'))
    sec=sum(1 for t in all_t if t.lower() in SECOND)
    fp=sum(1 for t in all_t if t.lower() in FIRSTPL)
    hedge=sum(1 for t in all_t if t.lower() in HEDGE)
    attr=sum(1 for t in all_t if t.lower() in ATTR)
    act=sum(1 for t in all_t if stem_match(t,ACT))
    clm=sum(1 for t in all_t if stem_match(t,CLAIM))
    num_s=sum(1 for _,s in sents if has_num(s))
    # proper nouns mid-sentence
    pn=0
    for _,s in sents:
        tk=toks(s)
        for i,t in enumerate(tk):
            if i>0 and t[0].isupper() and t not in ('I',"I'm","I'll","I'd","I've") : pn+=1
    act_s=sum(1 for _,s in sents if any(stem_match(t,ACT) for t in toks(s)))
    quotes=sum(s.count('"')//2 + s.count('“') for _,s in sents)
    short=sum(1 for x in ws if x<=6); long_=sum(1 for x in ws if x>=25)
    res=dict(name=name,sentences=n,words=N,words_per_sentence_mean=round(N/n,1),median=st.median(ws),
        p10=sorted(ws)[int(0.1*n)],p90=sorted(ws)[int(0.9*n)],max=max(ws),
        pct_sentences_le6w=round(100*short/n,1),pct_sentences_ge25w=round(100*long_/n,1),
        sentences_per_min=round(n/total_min,1),
        question_sentences=q,questions_per_min=round(q/total_min,2),
        second_person_tokens=sec,second_person_per_100w=round(100*sec/N,2),
        we_our_tokens=fp,we_per_100w=round(100*fp/N,2),
        hedge_words=hedge,hedge_per_100w=round(100*hedge/N,2),
        attribution_verbs=attr,attr_per_100w=round(100*attr/N,2),
        action_verbs=act,action_per_100w=round(100*act/N,2),
        claim_verbs=clm,claim_per_100w=round(100*clm/N,2),
        pct_sentences_with_number=round(100*num_s/n,1),
        pct_sentences_with_action_verb=round(100*act_s/n,1),
        proper_nouns_midsentence_per_100w=round(100*pn/N,2),
        quote_marks_pairs=quotes)
    return res
rr=analyse('reference',ref_s,ref_dur,ref_total,ref)
oo=analyse('ours',our_s,our_dur,our_total,ours)
json.dump([rr,oo],open(O+'text_metrics.json','w'),indent=1)
for k in rr:
    print('%-36s %-12s %-12s'%(k,rr[k],oo[k]))
# sentence length hist
def hist(sents):
    ws=[len(toks(s)) for _,s in sents]
    b=[0]*7
    for x in ws:
        i=0 if x<=3 else 1 if x<=6 else 2 if x<=10 else 3 if x<=15 else 4 if x<=20 else 5 if x<=30 else 6
        b[i]+=1
    n=len(ws); return [round(100*x/n) for x in b]
print('hist <=3,4-6,7-10,11-15,16-20,21-30,31+  ref',hist(ref_s),' ours',hist(our_s))
# save our sentences
open(O+'ours_sentences.txt','w').write('\n'.join('[%d:%02d] %s'%(t//60,t%60,s) for t,s in our_s))
