"""Text metrics for SCRIPT-V2 spoken lines, same lexicons as analysis_teardown_scripts/text_metrics.py.
Usage: python3 -I metrics.py <SCRIPT-V2.md> [wpm]
Reads beat lines of the form:  **12 · NARR** spoken text
TEXT-CHIP beats are on-screen only and are not counted.
"""
import re, sys, json, statistics as st

path = sys.argv[1]
wpm = float(sys.argv[2]) if len(sys.argv) > 2 else 170.0

BEAT = re.compile(r'^\*\*(\d+)\s*·\s*(NARR|ODY|POLY|CREW|CYC2)\*\*\s+(.*\S)\s*$')
beats = []
sections = []
cur_sec = 'front'
for line in open(path, encoding='utf8'):
    if line.startswith('## '):
        cur_sec = line[3:].split('(')[0].strip().split(':')[0].strip()
    m = BEAT.match(line.rstrip('\n'))
    if m:
        beats.append((int(m.group(1)), m.group(2), m.group(3)))
        sections.append(cur_sec)

def toks(s):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", s)

def split_sentences(text):
    text = text.replace('’', "'").replace('“', '"').replace('”', '"')
    parts = re.findall(r'[^.?!]+[.?!]+["\']?|[^.?!]+$', text)
    return [p.strip() for p in parts if toks(p)]

sents = []
for _, tag, text in beats:
    for s in split_sentences(text):
        sents.append((tag, s))

NUMW = set('two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred hundreds thousand thousands dozen million'.split())
def has_num(s):
    for t in toks(s):
        tl = t.lower()
        if re.search(r'\d', t): return True
        if any(p in NUMW for p in re.split(r'[-]', tl)): return True
    return False

HEDGE = set('may might perhaps possibly probably maybe argue argues argued suggest suggests suggested claim claims claimed theory hypothesis plausible unproven proven prove proof evidence likely unlikely apparently presumably seems seem appears appear could arguably implies imply speculation speculate suspect suspected sometimes'.split())
ATTR = set('says said writes wrote written argues argued reports reported claims claimed suggests suggested puts calls called lists listed names named notes noted mentions mentioned according adds added states stated describes described compares compared concluded conclude dates dated'.split())
ACT = set('''grab smash eat ate eaten drive drove driven shout scream run ran climb burn kill turn rolled roll sail raid party stay come came return blow blew hurl spear attack escape flee drag throw threw hit fire shoot string strap tie untie sharpen heat stab blind drown split slaughter wake sleep fall fell wash cling build sit cry beg dig fill summon embrace slip plug steer snatch rush gather open close push pull carry carried steal chase fight drink dig swing break broke smash storm land lift hold held hide hid walk dance wave kick jump leave left reach enter hunt lure die died die kneel stand stood sail row rise rose rain sink sank crash trap trapped devour devoured feast swallow bite laugh mock march charge capture seize seized slay slew pluck draw drew tear tore wield wove weave unravel announce'''.split())
CLAIM = set('say says said argue argues argued think thought suggest suggests claim claims report reports note notes call calls called name names list lists write writes wrote mention mentions believe believes know knows known prove proves find found date dates compare compares count counted explain explains conclude concludes imply implies describe describes consider considers point turn out put puts mean means'.split())

def stem_match(tok, S):
    t = tok.lower()
    if t in S: return True
    for suf in ('s', 'es', 'ed', 'ing', 'd'):
        if t.endswith(suf) and t[:-len(suf)] in S: return True
    if t.endswith('ied') and t[:-3] + 'y' in S: return True
    return False

all_t = [t for _, s in sents for t in toks(s)]
N = len(all_t)
ws = [len(toks(s)) for _, s in sents]
n = len(sents)
mins = N / wpm
def per100(x): return round(100.0 * x / N, 2)

hedge_tokens = [t.lower() for t in all_t if t.lower() in HEDGE]
attr_tokens = [t.lower() for t in all_t if t.lower() in ATTR]
act_tokens = [t.lower() for t in all_t if stem_match(t, ACT)]
claim_n = sum(1 for t in all_t if stem_match(t, CLAIM))
act_s = sum(1 for _, s in sents if any(stem_match(t, ACT) for t in toks(s)))
num_s = sum(1 for _, s in sents if has_num(s))
q = sum(1 for _, s in sents if s.rstrip().endswith('?'))
pn = 0
for _, s in sents:
    tk = toks(s)
    for i, t in enumerate(tk):
        if i > 0 and t[0].isupper() and t not in ('I', "I'm", "I'll", "I'd", "I've"): pn += 1

# dialogue exchanges: maximal runs of consecutive beats by non-narrator speakers
runs = []
cur = []
for _, tag, _ in beats:
    if tag != 'NARR':
        cur.append(tag)
    else:
        if cur: runs.append(cur); cur = []
if cur: runs.append(cur)
speaker_lines = sum(len(r) for r in runs)
# narrator-gag runs also count as part of an exchange when sandwiched by <=1 narrator line
merged = []
tags = [t for _, t, _ in beats]
i = 0
while i < len(tags):
    if tags[i] != 'NARR':
        j = i
        while j < len(tags):
            if tags[j] != 'NARR': j += 1
            else: break
        merged.append((i, j)); i = j
    else:
        i += 1
# exchange = run of >=2 character lines (a back-and-forth) or a single quoted speech
exch_2plus = sum(1 for r in runs if len(r) >= 2)

res = dict(
    spoken_beats=len(beats), words=N, sentences=n,
    runtime_min_at_wpm=round(mins, 2), runtime_mmss='%d:%02d' % (int(mins), round((mins - int(mins)) * 60)), wpm=wpm,
    words_per_sentence_mean=round(N / n, 1), median=st.median(ws),
    pct_sentences_le6w=round(100.0 * sum(1 for x in ws if x <= 6) / n, 1),
    pct_sentences_ge25w=round(100.0 * sum(1 for x in ws if x >= 25) / n, 1),
    sentences_per_min=round(n / mins, 1), questions=q, questions_per_min=round(q / mins, 2),
    action_per_100w=per100(len(act_tokens)),
    pct_sentences_with_action_verb=round(100.0 * act_s / n, 1),
    claim_verbs_per_100w=per100(claim_n),
    hedge_words=len(hedge_tokens), hedge_per_100w=per100(len(hedge_tokens)),
    hedge_per_100w_excluding_suspect=per100(len([t for t in hedge_tokens if not t.startswith('suspect')])),
    attribution_verbs=len(attr_tokens), attr_per_100w=per100(len(attr_tokens)),
    pct_sentences_with_number=round(100.0 * num_s / n, 1),
    proper_nouns_midsentence_per_100w=per100(pn),
    character_voiced_lines=speaker_lines, character_runs=len(runs), runs_with_2plus_lines=exch_2plus,
    pct_words_by_characters=round(100.0 * sum(len(toks(s)) for tag, s in sents if tag != 'NARR') / N, 1),
)
print(json.dumps(res, indent=1))
print('hedge tokens:', sorted(set(hedge_tokens)), {k: hedge_tokens.count(k) for k in set(hedge_tokens)})
print('attr tokens:', {k: attr_tokens.count(k) for k in set(attr_tokens)})
print('action tokens:', {k: act_tokens.count(k) for k in set(act_tokens)})

# per-section breakdown
print()
print('%-28s %6s %7s %8s %6s %6s' % ('section', 'words', 'act/100', 'hedge/100', 'attr/100', 'sec@170'))
order = []
for sec in sections:
    if sec not in order: order.append(sec)
for sec in order:
    texts = [t for (b, tag, t), sc in zip(beats, sections) if sc == sec]
    tk = [t for x in texts for t in toks(x)]
    n_ = len(tk)
    if not n_: continue
    a = sum(1 for t in tk if stem_match(t, ACT)); h = sum(1 for t in tk if t.lower() in HEDGE); at = sum(1 for t in tk if t.lower() in ATTR)
    print('%-28s %6d %7.2f %8.2f %6.2f %6d' % (sec, n_, 100.0*a/n_, 100.0*h/n_, 100.0*at/n_, round(n_/wpm*60)))
