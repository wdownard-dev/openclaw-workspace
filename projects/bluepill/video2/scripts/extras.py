"""Extra script metrics that metrics.py does not compute, same beat parser.
Usage: python3 -I extras.py <SCRIPT.md> [wpm ...]
Reports: sentence-length buckets, dialogue runs, longest dialogue-free stretch,
gag count (beats whose trace line contains the word 'gag'), gags per minute, longest gap between gags,
section word counts and cumulative times, and runtime at each wpm.
"""
import re, sys, json

path = sys.argv[1]
wpms = [float(x) for x in sys.argv[2:]] or [155.0, 165.0, 170.0]

BEAT = re.compile(r'^\*\*(\d+)\s*·\s*(NARR|ODY|POLY|CREW|CYC2)\*\*\s+(.*\S)\s*$')
beats = []   # dict(n, tag, text, trace, section)
sec = 'front'
for line in open(path, encoding='utf8'):
    line = line.rstrip('\n')
    if line.startswith('## '):
        sec = line[3:].split('(')[0].strip().split(':')[0].strip()
        continue
    if line.startswith('# END MATTER'):
        break
    m = BEAT.match(line)
    if m:
        beats.append(dict(n=int(m.group(1)), tag=m.group(2), text=m.group(3), trace='', section=sec))
    elif line.startswith('- trace:') and beats:
        beats[-1]['trace'] = line

def toks(s):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", s)

def split_sentences(text):
    text = text.replace('’', "'").replace('“', '"').replace('”', '"')
    parts = re.findall(r'[^.?!]+[.?!]+["\']?|[^.?!]+$', text)
    return [p.strip() for p in parts if toks(p)]

lens = [len(toks(s)) for b in beats for s in split_sentences(b['text'])]
buckets = [(1, 3), (4, 6), (7, 10), (11, 15), (16, 20), (21, 999)]
dist = {}
for lo, hi in buckets:
    c = sum(1 for x in lens if lo <= x <= hi)
    dist['%d-%s' % (lo, hi if hi < 999 else '+')] = '%d (%.1f%%)' % (c, 100.0 * c / len(lens))

words = [len(toks(b['text'])) for b in beats]
total = sum(words)
cum = []
c = 0
for w in words:
    cum.append(c)   # words spoken before this beat starts
    c += w

def sec_of(x, wpm):
    return x / wpm * 60.0

out = dict(file=path, beats=len(beats), words=total, sentences=len(lens),
           sentence_length_buckets=dist, longest_sentence=max(lens))
out['runtime'] = {('%d wpm' % w): '%d:%02d' % divmod(round(total / w * 60), 60) for w in wpms}

# dialogue runs
runs, cur = [], []
for b in beats:
    if b['tag'] != 'NARR':
        cur.append(b['tag'])
    elif cur:
        runs.append(cur); cur = []
if cur: runs.append(cur)
out['character_lines'] = sum(len(r) for r in runs)
out['dialogue_runs'] = len(runs)
out['dialogue_runs_2plus'] = sum(1 for r in runs if len(r) >= 2)
out['words_by_speaker'] = {t: sum(w for b, w in zip(beats, words) if b['tag'] == t) for t in ('NARR', 'ODY', 'POLY', 'CREW', 'CYC2')}

# longest dialogue-free stretch, and the same after the turn
def stretches(idx_from, wpm):
    last_t = None; best = (0, None, None)
    prev_i = None
    for i, b in enumerate(beats):
        if i < idx_from: continue
        if b['tag'] != 'NARR':
            t = sec_of(cum[i], wpm)
            if last_t is not None and t - last_t > best[0]:
                best = (t - last_t, prev_i, b['n'])
            last_t = t; prev_i = b['n']
    return best

turn_idx = next((i for i, b in enumerate(beats) if b['section'] == 'THE TURN'), 0)
for wpm in wpms:
    d, a, z = stretches(0, wpm)
    d2, a2, z2 = stretches(turn_idx, wpm)
    out['longest_dialogue_free_gap_s_at_%d' % wpm] = dict(overall=round(d), between_beats=[a, z], after_turn=round(d2), after_turn_between=[a2, z2])
out['character_lines_between_turn_and_last_beat'] = sum(1 for b in beats[turn_idx:] if b['tag'] != 'NARR')
out['character_lines_from_turn_to_final_Nobody'] = None

# gags
gag_idx = [i for i, b in enumerate(beats) if re.search(r'\bgag\b', b['trace'])]
out['gag_beats'] = [beats[i]['n'] for i in gag_idx]
out['gag_count'] = len(gag_idx)
for wpm in wpms:
    mins = total / wpm
    ts = [sec_of(cum[i], wpm) for i in gag_idx]
    gaps = [b - a for a, b in zip(ts, ts[1:])]
    out['gags_per_min_at_%d' % wpm] = round(len(gag_idx) / mins, 2)
    if gaps:
        k = max(range(len(gaps)), key=lambda j: gaps[j])
        out['longest_gag_gap_s_at_%d' % wpm] = dict(seconds=round(gaps[k]), between_beats=[beats[gag_idx[k]]['n'], beats[gag_idx[k + 1]]['n']], first_gag_at_s=round(ts[0]), last_gag_to_end_s=round(sec_of(total, wpm) - ts[-1]))

# sections
secs = []
for b, w in zip(beats, words):
    if not secs or secs[-1][0] != b['section']:
        secs.append([b['section'], 0, b['n']])
    secs[-1][1] += w
t = 0.0
rows = []
for name, w, first in secs:
    start = t
    t += w
    rows.append((name, w, first, start))
out['sections'] = [dict(section=n, words=w, first_beat=f, start_at_155=sec_of(s, 155), start_at_165=sec_of(s, 165), seconds_at_155=round(sec_of(w, 155)), seconds_at_165=round(sec_of(w, 165))) for n, w, f, s in rows]
print(json.dumps(out, indent=1, default=lambda x: round(x, 1)))
