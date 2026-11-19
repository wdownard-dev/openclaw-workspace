"""Assemble narration for video 1 from audio/chunks, write narration.wav/.mp3, words.json, beats_timing.json,
shots_timed.json, SHOTLIST-V1-RETIMED.md, audio/quality.json. No system ffmpeg: uses Remotion's bundled one.
Run from anywhere: python3 video1/assemble.py"""
import os, sys, json, re, wave, subprocess, math, array, statistics, importlib.util, collections
HERE=os.path.dirname(os.path.abspath(__file__)); PROJ=os.path.dirname(HERE)
os.chdir(HERE); sys.path.insert(0,HERE)
FF=os.path.join(PROJ,"pipeline/remotion-proof/node_modules/@remotion/compositor-linux-x64-gnu/ffmpeg")
AUD=os.path.join(HERE,"audio"); CH=os.path.join(AUD,"chunks")
SR=44100; TARGET_LUFS=-22.0; PEAK_CEIL=-1.0   # raw voice is ~-23.5 LUFS with -2..-6 dBFS peaks; louder targets clip, so level-match chunks and cap gain by peak
LEAD=0.40; PARA_GAP=0.30; TAIL_PAD=0.06; CH_GAP=0.35; BEFORE_CARD=0.0; CARD=2.0; AFTER_CARD=0.0; TAIL_MIN=1.5; ENDCARD_MIN=4.0   # card window = whole pause (2.0 s, was 0.35+2.5+0.45=3.3); sting fills it
STING_DIR=os.path.join(AUD,'stings')
import voice
cs=voice.chunks()
# render.py builds the (estimate) shot structure from beats.py; reuse it so shot numbering matches SHOTLIST-V1.md
ns={}; exec(open('render.py').read().split("if __name__=='__main__':")[0],ns)
SHOTS=ns['shots']; R=ns['R']; CHAP=ns['CH']; fmt=ns['fmt']

def decode(path,gain_db=0.0):
    af=["-af",f"volume={gain_db:.3f}dB"] if abs(gain_db)>1e-6 else []
    tmp=f"{AUD}/_dec.wav"
    subprocess.run([FF,"-v","error","-y","-i",path]+af+["-ac","1","-ar",str(SR),"-c:a","pcm_s16le",tmp],check=True)
    with wave.open(tmp,'rb') as w: assert w.getframerate()==SR and w.getnchannels()==1; fr=w.readframes(w.getnframes())
    a=array.array('h'); a.frombytes(fr); return a
def lufs(wavpath):
    p=subprocess.run([FF,"-hide_banner","-nostats","-i",wavpath,"-af","loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True)
    j=json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}',p.stderr).group(0)); return float(j['input_i']),float(j['input_tp']),float(j['input_lra'])
def write_wav(path,arr):
    with wave.open(path,'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(arr.tobytes())
def rms_db(a):
    if not len(a): return -99
    s=0.0
    for i in range(0,len(a),4): s+=a[i]*a[i]
    return 10*math.log10(s/(len(a)/4)/32768.0**2+1e-12)
def words_of(jp):
    a=json.load(open(jp))['alignment']; ws=[];cur="";s=None;pe=0
    for c,x,y in zip(a['characters'],a['character_start_times_seconds'],a['character_end_times_seconds']):
        if c.isspace():
            if cur: ws.append([cur,x_s,pe]); cur=""
        else:
            if not cur: x_s=x
            cur+=c; pe=y
    if cur: ws.append([cur,x_s,pe])
    return ws

# ---- pass 1: per-chunk loudness (raw, trimmed) ----
meta={}
for c in cs:
    k=c['id']; mp3=f"{CH}/c{k:02d}.mp3"; ws=words_of(f"{CH}/c{k:02d}.json")
    assert len(ws)==len(c['orig'].split()),(k,len(ws))
    a0=max(0.0,ws[0][1]-0.05); a1=ws[-1][2]+0.12
    raw=decode(mp3); n=len(raw)
    i0=int(a0*SR); i1=min(n,int(a1*SR)); seg=raw[i0:i1]
    tmp=f"{AUD}/_tmp.wav"; write_wav(tmp,seg); L,TP,LRA=lufs(tmp)
    # onset check: first 10 ms window above -45 dBFS in the untrimmed decode vs alignment first-word start
    win=int(0.01*SR); thr=32768*10**(-45/20); onset=None
    for i in range(0,min(n,int(1.5*SR)),win):
        if max(abs(x) for x in raw[i:i+win])>thr: onset=i/SR; break
    meta[k]=dict(a0=a0,a1=a1,ws=ws,L=L,TP=TP,LRA=LRA,onset_audio=onset,onset_align=ws[0][1],mp3_len=n/SR,raw_rms=rms_db(seg),raw_peak=20*math.log10(max(max(seg),-min(seg))/32768.0+1e-9))
med=statistics.median(m['L'] for m in meta.values())
for k,m in meta.items():
    m['gain']=max(-8.0,min(8.0,min(TARGET_LUFS-m['L'],PEAK_CEIL-m['raw_peak'])))
# ---- pass 2: decode with gain, build timeline ----
pcm=array.array('h'); t=0.0
def put_silence(sec):
    global t
    pcm.extend(array.array('h',bytes(2*int(round(sec*SR))))); t=len(pcm)/SR
put_silence(LEAD)
words=[]; beat_words=collections.defaultdict(list); cards={}   # ch -> (start,end)
prev_ch=None; chunk_tl={}
for c in cs:
    k=c['id']; m=meta[k]
    first_of_ch=(c['ch']!=prev_ch)
    if k>0:
        has_card=first_of_ch and CHAP[c['ch']][1]
        if has_card:
            put_silence(BEFORE_CARD); cards[c['ch']]=(t,t+CARD); put_silence(CARD+AFTER_CARD)   # sting is mixed into its own track below
        else: put_silence(PARA_GAP if not first_of_ch else CH_GAP)
    prev_ch=c['ch']
    full=decode(f"{CH}/c{k:02d}.mp3",m['gain'])
    # trim dead air: alignment end overstates the real end on some takes; find the last 10 ms window above -45 dBFS before a1 and cut TAIL_PAD after it
    win=int(0.01*SR); thr=32768*10**(-45/20); i1=min(len(full),int(m['a1']*SR)); real=None
    for i in range(i1-win,int(m['a0']*SR),-win):
        if max(abs(x) for x in full[i:i+win])>thr: real=(i+win)/SR; break
    a1n=min(m['a1'],real+TAIL_PAD) if real else m['a1']
    m['trimmed']=round(m['a1']-a1n,3); m['a1n']=a1n
    seg=full[int(m['a0']*SR):int(a1n*SR)]
    # 12 ms fade-out so the cut is click-free
    nf=int(0.012*SR)
    for j in range(nf): seg[len(seg)-1-j]=int(seg[len(seg)-1-j]*(j/nf))
    off=t-m['a0']                      # timeline time = chunk time + off
    pk=max(max(seg),-min(seg))/32768.0; m['peak_db']=20*math.log10(pk+1e-9)
    pcm.extend(seg); t=len(pcm)/SR
    sw=c['sent'].split(); ow=c['orig'].split(); bi=0; bcount=0; beats=c['beats']
    chunk_tl[k]=dict(start=m['ws'][0][1]+off,end=m['ws'][-1][2]+off,offset=off)
    for j,(w,sp,oo) in enumerate(zip(m['ws'],sw,ow)):
        while bcount>=len(R[beats[bi]]['text'].split()): bi+=1; bcount=0
        rec=dict(i=len(words),text=oo,spoken=w[0],start=round(w[1]+off,3),end=round(w[2]+off,3),chunk=k,beat=beats[bi],respelled=(w[0]!=oo))
        words.append(rec); beat_words[beats[bi]].append(rec['i']); bcount+=1
last_end=words[-1]['end']
# tail handled via final shot end below; pad audio with tail silence so the wav covers it
put_silence(TAIL_MIN)
voicep=f"{AUD}/narration_voice_only.wav"; write_wav(voicep,pcm)
# stings on their own track (same length), then the mix
stk=array.array('h',bytes(2*len(pcm))); sting_info={}
for ch,(a,b) in cards.items():
    sp=[f for f in os.listdir(STING_DIR) if f.startswith(f"sting_ch{ch}_") and f.endswith(".wav")]; assert len(sp)==1,(ch,sp)
    with wave.open(f"{STING_DIR}/{sp[0]}",'rb') as w: assert w.getframerate()==SR and w.getnchannels()==1; sa=array.array('h'); sa.frombytes(w.readframes(w.getnframes()))
    i0=int(round(a*SR)); assert len(sa)<=int(round((b-a)*SR))+1,"sting longer than card window"
    for j,v in enumerate(sa): stk[i0+j]=v
    sting_info[ch]=dict(file=sp[0],start=round(a,3),end=round(a+len(sa)/SR,3),card_end=round(b,3))
stp=f"{AUD}/stings_track.wav"; write_wav(stp,stk)
mix=array.array('h',(max(-32768,min(32767,v+u)) for v,u in zip(pcm,stk)))
wavp=f"{AUD}/narration.wav"; write_wav(wavp,mix)
subprocess.run([FF,"-v","error","-y","-i",wavp,"-codec:a","libmp3lame","-b:a","192k",f"{AUD}/narration.mp3"],check=True)
json.dump(words,open(f"{AUD}/words.json","w"),indent=0)

# ---- beats_timing.json ----
bt=[]
for bi,r in enumerate(R):
    ids=beat_words[bi]; w0=words[ids[0]]; w1=words[ids[-1]]
    bt.append(dict(beat=bi,chapter=r['ch'],text=r['text'],words=len(ids),start=w0['start'],end=w1['end'],duration=round(w1['end']-w0['start'],3),
        first_word=ids[0],last_word=ids[-1],new_paragraph=r['para']))
json.dump(bt,open(f"{AUD}/beats_timing.json","w"),indent=1)

# ---- shots ----
wi=0; timed=[]
for s in SHOTS:
    if s['card']:
        a,b=cards[s['ch']]; timed.append(dict(n=s['n'],card=True,ch=s['ch'],start=a,end=b,text="",words=0,w0=None,w1=None,s=s)); continue
    nw=s['words']; timed.append(dict(n=s['n'],card=False,ch=s['ch'],text=s['text'],words=nw,w0=wi,w1=wi+nw-1,s=s)); wi+=nw
assert wi==len(words),(wi,len(words))
for i,x in enumerate(timed):
    if x['card']: continue
    st=words[x['w0']]['start']
    if i==0: st=0.0
    elif timed[i-1]['card']: st=timed[i-1]['end']              # first shot after a card absorbs the post-card pause
    x['start']=st
for i,x in enumerate(timed):
    if i+1<len(timed):
        if not x['card']: x['end']=timed[i+1]['start'] if not timed[i+1]['card'] else timed[i+1]['start']
    else: x['end']=max(last_end+TAIL_MIN,x['start']+ENDCARD_MIN)
# a shot that precedes a card ends where the card starts (gap before card is absorbed)
total=timed[-1]['end']
flags=[]
for x in timed:
    x['dur']=round(x['end']-x['start'],3); x['start']=round(x['start'],3); x['end']=round(x['end'],3)
    x['flag']=None
    if not x['card']:
        if x['dur']<2.5: x['flag']="short"
        elif x['dur']>8.0: x['flag']="long"
def split_suggest(x):
    ws=[words[i] for i in range(x['w0'],x['w1']+1)]; mid=(x['start']+x['end'])/2; best=None
    for j,w in enumerate(ws[:-1]):
        if re.search(r'[,:;.?!]$',w['text']):
            d=abs(ws[j+1]['start']-mid)
            if best is None or d<best[0]: best=(d,j)
    if best is None: return None
    j=best[1]; return dict(after_word=ws[j]['text'],at=round(ws[j+1]['start'],2),part_a=round(ws[j+1]['start']-x['start'],2),part_b=round(x['end']-ws[j+1]['start'],2))
for x in timed:
    if x['flag']=="long": x['suggest']=split_suggest(x)
narr=[x for x in timed if not x['card']]
nshots=len(timed)
cpm=nshots/(total/60)
out=[]
for x in timed:
    s=x['s']; out.append(dict(shot=x['n'],start=x['start'],end=x['end'],sec=x['dur'],start_label=fmt(x['start']),chapter=ns['CH'][x['ch']][0],
        narration=x['text'],words=x['words'],type=("title card" if x['card'] else s['kind']),chars=s['chars'],light=s['light'],cam=s['cam'],asset=s['asset'],note=s['note'],
        old_start=round(s['start'],1),old_sec=round(s['d'],1),flag=x['flag'],split_suggestion=x.get('suggest')))
json.dump(dict(total_sec=round(total,2),total_label=f"{int(total//60)}:{total%60:05.2f}",shots=nshots,cuts_per_min=round(cpm,2),flagged_short=sum(1 for x in timed if x['flag']=='short'),
    flagged_long=sum(1 for x in timed if x['flag']=='long'),shot_list=out),open(f"{HERE}/shots_timed.json","w"),indent=1)

# ---- quality ----
fl,ftp,flra=lufs(wavp); vl,vtp,vlra=lufs(voicep)
# silence detect on the final wav
p=subprocess.run([FF,"-hide_banner","-nostats","-i",voicep,"-af","silencedetect=noise=-42dB:d=0.25","-f","null","-"],capture_output=True,text=True)   # (replaced below: run on voice-only track)
sil=[(float(a),float(b)) for a,b in zip(re.findall(r'silence_start: ([\d.]+)',p.stderr),re.findall(r'silence_duration: ([\d.]+)',p.stderr))]
sil_in=[(a,d) for a,d in sil if 0.5<a<last_end]
card_sil=[(a,d) for a,d in sil_in if any(a<cc[1] and a+d>cc[0] for cc in cards.values())]   # any silence overlapping a card window (starts earlier because the last word's alignment end overstates)
sil_nocard=[(a,d) for a,d in sil_in if (a,d) not in card_sil]
# within-chunk gaps from alignment
gaps=[]
for a,b in zip(words,words[1:]):
    if a['chunk']==b['chunk']: gaps.append((round(b['start']-a['end'],2),a['text'],b['text'],a['end']))
gaps.sort(reverse=True)
nwords=len(words); speech_span=last_end-words[0]['start']
per_chunk=[]
for c in cs:
    k=c['id']; m=meta[k]; dur=m['ws'][-1][2]-m['ws'][0][1]
    per_chunk.append(dict(chunk=k,chapter=c['ch'],words=len(m['ws']),chars=len(c['sent']),dur=round(dur,2),wpm=round(len(m['ws'])/dur*60),lufs_raw=round(m['L'],1),gain_db=round(m['gain'],1),
        peak_db_after=round(m['peak_db'],1),lra=round(m['LRA'],1),onset_audio=m['onset_audio'],onset_align=round(m['onset_align'],3),start=round(chunk_tl[k]['start'],2),end=round(chunk_tl[k]['end'],2)))
# name pronunciation timing: seconds per syllable vs overall
def syl(w):
    w=re.sub(r'[^a-z\-]','',w.lower()); return max(1,len(re.findall(r'[aeiouy]+',w)))
allsyl=sum(syl(w['spoken']) for w in words); sps=speech_span/allsyl
risky=[]
NAMES=["Polyphemus","Othenio","Abel","Empedocles","Theocritus","Thucydides","Tiryns","Pausanias","Brontes","Steropes","Arges","Aci","Trezza","Aguirre","Burkert","Buxton","Witton","Mayor","Hesiod","Euripides","Mycenae","Aeolian","Cyclopes","Odysseus","Poseidon","cyclopia","Virgil","Etna","Hing"]
HEDGE=["may","unproven","plausible","suspect","hypothesis","implies","presumably","perhaps","argues","bluntly","baseless","careful"]
for w in words:
    core=re.sub(r"[^\w']",'',w['text']).replace("'s","")
    d=w['end']-w['start']; sy=syl(w['spoken']); r=d/sy/sps
    if core in NAMES: risky.append(dict(kind="name",word=w['text'],spoken=w['spoken'],t=w['start'],dur=round(d,2),rel_per_syllable=round(r,2),respelled=w['respelled']))
    elif core.lower() in HEDGE: risky.append(dict(kind="hedge",word=w['text'],t=w['start'],dur=round(d,2),rel_per_syllable=round(r,2),respelled=False))
stl=lufs(stp); sil_cut=0
Q=dict(total_sec=round(total,2),narration_start=words[0]['start'],narration_end=last_end,words=nwords,speech_span_wpm=round(nwords/speech_span*60,1),
    wpm_all_in=round(nwords/total*60,1),final_lufs=fl,final_true_peak_db=ftp,final_lra=flra,voice_only_lufs=vl,voice_only_true_peak_db=vtp,voice_only_lra=vlra,stings_track_lufs_whole=stl[0],stings=sting_info,
    longest_silences_voice_only_excluding_card_pauses=sorted(sil_nocard,key=lambda x:-x[1])[:6],card_pause_silences_voice_only=card_sil,per_chunk=per_chunk,median_raw_lufs=round(med,1),
    longest_silences_voice_only_all=sorted(sil_in,key=lambda x:-x[1])[:8],longest_within_chunk_gaps=gaps[:6],seconds_per_syllable_avg=round(sps,3),risky=risky,
    inserted=dict(lead=LEAD,para_gap=PARA_GAP,before_card=BEFORE_CARD,card=CARD,after_card=AFTER_CARD,tail_min=TAIL_MIN,note='card window 2.0 s = whole pause; clip lead 0.05 s before first word, tail 0.12 s after last word'),
    cards={str(k):[round(v[0],2),round(v[1],2)] for k,v in cards.items()},
    chapter_starts={CHAP[ch][0]:round(min(x['start'] for x in timed if x['ch']==ch),2) for ch in sorted(set(x['ch'] for x in timed))})
# first word after each card: expected start vs first sample above -45 dBFS in the voice-only track; sting level per card
chk={}
for ch,(c0,c1) in cards.items():
    nxt=[w for w in words if w['start']>=c1-0.01][0]; thr=32768*10**(-45/20); win=int(0.01*SR); on=None
    for i in range(int((c1-0.1)*SR),int((c1+1.0)*SR),win):
        if max(abs(x) for x in pcm[i:i+win])>thr: on=i/SR; break
    ss=array.array('h',stk[int(c0*SR):int(c1*SR)]); pk=max(max(ss),-min(ss))/32768
    chk[str(ch)]=dict(card_start=round(c0,3),card_end=round(c1,3),card_len=round(c1-c0,3),first_word=nxt['text'],first_word_start=nxt['start'],voice_onset_audio=on,onset_minus_expected=round(on-nxt['start'],3),
        sting_peak_db=round(20*math.log10(pk+1e-9),1),sting_lufs=lufs(stp) if False else None)
Q['card_checks']=chk
Q['trimmed_per_chunk']={str(k):m['trimmed'] for k,m in meta.items()}
json.dump(Q,open(f"{AUD}/quality.json","w"),indent=1)
print(json.dumps({k:Q[k] for k in ['total_sec','words','speech_span_wpm','wpm_all_in','final_lufs','final_true_peak_db','final_lra','voice_only_lufs','voice_only_true_peak_db']}))
print("shots",nshots,"cuts/min",round(cpm,2),"short",sum(1 for x in timed if x['flag']=='short'),"long",sum(1 for x in timed if x['flag']=='long'))
