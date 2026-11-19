import re,json,subprocess
F='/home/williamdownard/openclaw-sites/bin/ffmpeg'
# original word times from vtt
t=open('src/src.en.vtt').read().split('\n')
def ts(s):
    h,m,x=s.split(':');return int(h)*3600+int(m)*60+float(x)
ow=[]
for i,l in enumerate(t):
    if '-->' in l and i+2<len(t) and re.search(r'<\d\d:',t[i+2]):
        line=t[i+2]; st=ts(l.split(' --> ')[0])
        first=re.match(r'([^<]+)',line).group(1).strip()
        ow.append((st,first))
        for m in re.finditer(r'<(\d\d:\d\d:\d\d\.\d+)><c>([^<]+)</c>',line):
            ow.append((ts(m.group(1)),m.group(2).strip()))
txt=open('transcript.txt').read()
words=txt.split()
assert len(ow)==len(words),(len(ow),len(words))
# sentence starts by word index
sent=[0]
for i,w in enumerate(words[:-1]):
    if re.search(r'[.?!]$',w): sent.append(i+1)
o_start=[ow[i][0] for i in sent]+[64.23]
# new times from char alignment
a=json.load(open('align.json'));cs=a['character_start_times_seconds'];ce=a['character_end_times_seconds']
pos=0;cstart=[]
wi=0;idx=[]
for w in words:
    pos=txt.index(w,pos);idx.append(pos);pos+=len(w)
n_start=[cs[idx[i]] for i in sent]
# narration atempo
AT=1.1
n_start=[x/AT for x in n_start]; n_end=ce[-1]/AT+0.4
n_bounds=n_start+[n_end]
segs=[]
for k in range(len(sent)):
    od=o_start[k+1]-o_start[k]; nd=n_bounds[k+1]-n_bounds[k]
    segs.append((o_start[k],o_start[k+1],nd,nd/od))
    print(k,round(o_start[k],2),round(od,2),'->',round(nd,2),'x',round(nd/od,2))
fc=[];lab=''
for k,(s,e,nd,r) in enumerate(segs):
    fc.append(f"[0:v]trim={s}:{e},setpts=(PTS-STARTPTS)*{r:.4f},fps=30[v{k}]")
    lab+=f"[v{k}]"
fc.append(f"{lab}concat=n={len(segs)}:v=1:a=0[v]")
fc.append(f"[1:a]atempo={AT},adelay=0|0,apad[a]")
dur=n_bounds[-1]
subprocess.run([F,'-y','-i','src/src.f399.mp4','-i','narr.mp3','-filter_complex',';'.join(fc),'-map','[v]','-map','[a]','-t',str(dur),'-c:v','libx264','-crf','20','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','repost_test.mp4'],check=True,capture_output=True)
print('done',dur)
