#!/usr/bin/env python
"""refwatch: study a YouTube video (free tools only, no uploads).

Usage: ~/.venvs/refwatch/bin/python scripts/refwatch/watch.py <url_or_id> [--out DIR] [--skip-download]
See README.md. Downloaded files are untrusted data; this script only reads them
with ffmpeg/ffprobe/PIL/json and never executes anything from the output dir.
"""
import argparse, json, os, re, statistics as st, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WS = '/home/williamdownard/.openclaw/workspace'
BIN = '/home/williamdownard/openclaw-sites/bin'
FFMPEG = BIN + '/ffmpeg'
W, H = 320, 180          # analysis resolution
FPS = 30
FR = W * H

# ---- comparison baselines -------------------------------------------------
# UF = Unknown Frequencies mJS-QVw8lzY, from video2/FORMAT-BIBLE.md sections 1-2 [V]
UF = {
    'wpm': 178, 'sentences_per_min': 18.5, 'words_per_sentence_mean': 9.6,
    'words_per_sentence_median': 8, 'pct_sentences_le6w': 39.5, 'questions_per_min': 1.22,
    'cuts_per_min': 10.7, 'pops_per_min': 7.4, 'visible_changes_per_min': 18.1,
    'shot_median_s': 4.2, 'shot_p90_s': 12.3, 'shot_max_s': None,
    'white_dominant_pct': 25.6,
}
# Our animatic, video2/remotion-v2/QA-ANIMATIC.md [V] (text numbers from text_metrics.json 'ours')
OURS = {
    'cuts_per_min': 9.5, 'pops_per_min': 6.5, 'visible_changes_per_min': 16,
    'shot_median_s': 4.89, 'shot_p90_s': 8.8, 'shot_max_s': 11.81,
    'white_dominant_pct': 41.9,
}
OURS_TEXT = {'wpm': 155.2, 'sentences_per_min': 13.8, 'words_per_sentence_mean': 11.2,
             'words_per_sentence_median': 11, 'pct_sentences_le6w': 24.1, 'questions_per_min': 0.29}


def log(*a):
    print('[refwatch]', *a, flush=True)


def video_id(s):
    m = re.search(r'(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})', s)
    if m:
        return m.group(1)
    if re.fullmatch(r'[A-Za-z0-9_-]{11}', s):
        return s
    sys.exit('cannot parse video id from %r' % s)


# ---- 1. download -----------------------------------------------------------
def download(vid, out):
    import yt_dlp
    opts = {
        'outtmpl': out + '/video.%(ext)s',
        'format': 'bv*[height<=480][ext=mp4]/bv*[height<=480]/b[height<=480]',
        'format_sort': ['res:480', '+size'],
        'merge_output_format': 'mp4',
        'writesubtitles': True, 'writeautomaticsub': True,
        'subtitleslangs': ['en', 'en-US', 'en-GB', 'en-orig'],
        'subtitlesformat': 'json3',
        'writeinfojson': False, 'quiet': True, 'no_warnings': True, 'noprogress': True,
        'ignoreerrors': 'only_download',
        'retries': 3,
    }
    with yt_dlp.YoutubeDL(opts) as y:
        info = y.extract_info('https://www.youtube.com/watch?v=' + vid, download=True)
    if info is None:
        # caption endpoint rate-limited (HTTP 429) fails the whole extract; get the video without captions
        log('caption download failed, retrying without captions')
        opts.update({'writesubtitles': False, 'writeautomaticsub': False})
        with yt_dlp.YoutubeDL(opts) as y:
            info = y.extract_info('https://www.youtube.com/watch?v=' + vid, download=True)
    meta = {k: info.get(k) for k in ('id', 'title', 'channel', 'uploader', 'duration', 'view_count',
                                     'like_count', 'upload_date', 'description', 'chapters',
                                     'width', 'height', 'fps', 'format', 'tags', 'categories')}
    meta['subtitle_kinds'] = {'manual': sorted((info.get('subtitles') or {}).keys()),
                              'auto': [k for k in (info.get('automatic_captions') or {}) if k.startswith('en')]}
    json.dump(meta, open(out + '/metadata.json', 'w'), indent=1)
    return meta


def find_video(out):
    for f in sorted(os.listdir(out)):
        if f.startswith('video.') and f.rsplit('.', 1)[-1] in ('mp4', 'mkv', 'webm'):
            return out + '/' + f
    return None


def find_caption(out):
    """prefer manual en over auto. yt-dlp names both video.en.json3; check metadata."""
    c = sorted(f for f in os.listdir(out) if f.startswith('video.') and f.endswith('.json3'))
    if 'video.en.json3' in c:
        return out + '/video.en.json3'
    return (out + '/' + c[0]) if c else None


# ---- words / sentences -----------------------------------------------------
def words_from_json3(path):
    d = json.load(open(path))
    words = []
    for e in d.get('events', []):
        if 'segs' not in e:
            continue
        t0 = e.get('tStartMs', 0)
        dur = e.get('dDurationMs', 0)
        segs = [s for s in e['segs'] if s.get('utf8', '').strip()]
        has_off = any('tOffsetMs' in s for s in segs)
        if not has_off and segs:
            # manual captions: line-level timing; spread words evenly over the event
            toks = [(w, s) for s in segs for w in s['utf8'].split()]
            for i, (w, _) in enumerate(toks):
                words.append({'text': w, 'start': (t0 + dur * i / max(1, len(toks))) / 1000})
            continue
        for s in segs:
            w = s['utf8'].strip()
            words.append({'text': w, 'start': (t0 + s.get('tOffsetMs', 0)) / 1000})
    seen, uniq = set(), []
    for w in words:
        k = (w['text'], round(w['start'], 2))
        if k in seen:
            continue
        seen.add(k)
        uniq.append(w)
    uniq.sort(key=lambda w: w['start'])
    return uniq


def sentences_from_words(ws):
    """punctuation split; if captions carry almost no punctuation (auto captions), split on pauses >0.7 s."""
    punct = sum(1 for w in ws if re.search(r'[.?!]["”\']?$', w['text']))
    mode = 'punctuation' if ws and punct / len(ws) > 0.02 else 'pause'
    out, cur, t0 = [], [], None
    for i, w in enumerate(ws):
        if t0 is None:
            t0 = w['start']
        cur.append(w['text'])
        end = False
        if mode == 'punctuation':
            end = bool(re.search(r'[.?!]["”\']?$', w['text'])) and not re.fullmatch(r'(Mr|Mrs|Dr|St)\.', w['text'])
        elif i + 1 < len(ws) and ws[i + 1]['start'] - w['start'] > 0.7 + 0.3 * len(w['text']) / 10:
            end = True
        if end:
            out.append((t0, ' '.join(cur)))
            cur, t0 = [], None
    if cur:
        out.append((t0, ' '.join(cur)))
    return out, mode


def toks(s):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", s)


def mmss(t):
    return '%d:%02d' % (int(t) // 60, int(t) % 60)


# ---- 2. frame series, shots, events ---------------------------------------
def probe_duration(video):
    """ffprobe is not installed; parse `ffmpeg -i` stderr."""
    r = subprocess.run([FFMPEG, '-hide_banner', '-i', video], capture_output=True, text=True)
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def analyse_frames(video):
    cmd = [FFMPEG, '-v', 'error', '-i', video, '-an', '-vf',
           'fps=%d,scale=%d:%d:flags=area,format=gray' % (FPS, W, H), '-f', 'rawvideo', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    g80, diff, white60, white40, edge, lum = [], [0.0], [], [], [], []
    prev = None
    i = 0
    while True:
        buf = p.stdout.read(FR)
        if len(buf) < FR:
            break
        f = np.frombuffer(buf, np.uint8)
        fi = f.astype(np.int16)
        if prev is not None:
            diff.append(float(np.abs(fi - prev).mean()))
        prev = fi
        g80.append(f.reshape(45, 4, 80, 4).mean(axis=(1, 3)).astype(np.uint8).ravel())
        wfrac = float((f > 235).mean())
        white60.append(wfrac > 0.6)
        white40.append(wfrac > 0.4)
        lum.append(float(f.mean()))
        if i % FPS == 0:   # text proxy: share of pixels with strong horizontal gradient, 1 sample/s
            im = fi.reshape(H, W)
            edge.append(float((np.abs(np.diff(im, axis=1)) > 80).mean()))
        i += 1
    p.wait()
    return dict(N=i, g80=np.array(g80), diff=np.array(diff[:i]), white60=np.array(white60),
                white40=np.array(white40), edge=np.array(edge), lum=np.array(lum))


def detect_events(S):
    d, g, N = S['diff'], S['g80'].astype(np.int16), S['N']
    ev = []
    for i in range(2, N - 2):
        if d[i] > 2.5 and d[i] >= d[i - 1] and d[i] >= d[i + 1]:
            a, b = g[i - 1], g[min(N - 1, i + 2)]
            frac = float((np.abs(a - b) > 25).mean())
            ev.append(dict(i=i, t=round(i / FPS, 2), d=round(float(d[i]), 3), frac=round(frac, 2)))
    return ev


def build_shots(ev, total, minfrac=0.3, mingap=0.45):
    cuts = [0.0]
    for e in ev:
        if e['frac'] >= minfrac and e['t'] - cuts[-1] >= mingap:
            cuts.append(e['t'])
    cuts.append(total)
    shots = []
    for k, (a, b) in enumerate(zip(cuts[:-1], cuts[1:])):
        inner = [e for e in ev if a < e['t'] < b]
        shots.append(dict(n=k, start=round(a, 2), end=round(b, 2), len=round(b - a, 2),
                          pop=sum(1 for e in inner if 0.1 <= e['frac'] < minfrac),
                          micro=sum(1 for e in inner if e['frac'] < 0.1)))
    return shots


# ---- 3. sheets ---------------------------------------------------------------
def font(sz):
    try:
        return ImageFont.load_default(size=sz)
    except TypeError:
        return ImageFont.load_default()


def grab(video, t, w, h):
    r = subprocess.run([FFMPEG, '-v', 'error', '-ss', '%.3f' % t, '-i', video, '-frames:v', '1',
                        '-vf', 'scale=%d:%d' % (w, h), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True)
    if len(r.stdout) != w * h * 3:
        return Image.new('RGB', (w, h), (60, 60, 60))
    return Image.frombytes('RGB', (w, h), r.stdout)


def shot_sheets(video, shots, out, cols=8, per=40, cw=232, ch=130, label_h=18):
    fnt = font(13)
    times = [min(s['start'] + min(0.3, s['len'] / 2), max(0, s['end'] - 0.05)) for s in shots]
    with ThreadPoolExecutor(10) as ex:
        imgs = list(ex.map(lambda t: grab(video, t, cw, ch), times))
    files = []
    for si in range(0, len(shots), per):
        chunk = list(range(si, min(si + per, len(shots))))
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * (cw + 2), rows * (ch + label_h + 2)), (20, 20, 20))
        dr = ImageDraw.Draw(sheet)
        for k, idx in enumerate(chunk):
            x, y = (k % cols) * (cw + 2), (k // cols) * (ch + label_h + 2)
            sheet.paste(imgs[idx], (x, y))
            dr.text((x + 3, y + ch + 2), '#%d %s  %.1fs' % (idx, mmss(shots[idx]['start']), shots[idx]['len']),
                    fill=(255, 255, 255), font=fnt)
        fn = 'shots_%d.jpg' % (si // per)
        sheet.save(out + '/' + fn, quality=82)
        files.append(fn)
    return files


def hook_sheet(video, out, secs=30, cols=6, cw=320, ch=180):
    p = subprocess.run([FFMPEG, '-v', 'error', '-i', video, '-t', str(secs), '-an', '-vf',
                        'fps=1,scale=%d:%d' % (cw, ch), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True)
    n = len(p.stdout) // (cw * ch * 3)
    rows = (n + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (cw + 2), max(1, rows) * (ch + 2)), (20, 20, 20))
    dr = ImageDraw.Draw(sheet)
    fnt = font(18)
    for k in range(n):
        im = Image.frombytes('RGB', (cw, ch), p.stdout[k * cw * ch * 3:(k + 1) * cw * ch * 3])
        x, y = (k % cols) * (cw + 2), (k // cols) * (ch + 2)
        sheet.paste(im, (x, y))
        dr.rectangle([x, y, x + 44, y + 22], fill=(0, 0, 0))
        dr.text((x + 4, y + 1), '%ds' % k, fill=(255, 255, 0), font=fnt)
    sheet.save(out + '/hook_sheet.jpg', quality=82)


# ---- palette -----------------------------------------------------------------
def palette(video, out, k=6):
    pw, phh = 96, 54
    p = subprocess.run([FFMPEG, '-v', 'error', '-i', video, '-an', '-vf', 'fps=1,scale=%d:%d' % (pw, phh),
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8).reshape(-1, 3)
    rng = np.random.default_rng(0)
    pts = a[rng.choice(len(a), min(60000, len(a)), replace=False)].astype(np.float32)
    cent = pts[rng.choice(len(pts), k, replace=False)]
    for _ in range(25):
        lab = ((pts[:, None, :] - cent[None]) ** 2).sum(-1).argmin(1)
        for j in range(k):
            m = pts[lab == j]
            if len(m):
                cent[j] = m.mean(0)
    lab = ((a.astype(np.float32)[::7, None, :] - cent[None]) ** 2).sum(-1).argmin(1)
    share = np.bincount(lab, minlength=k) / len(lab)
    order = np.argsort(-share)
    pal = [dict(hex='#%02x%02x%02x' % tuple(int(round(c)) for c in cent[j]), share_pct=round(float(share[j]) * 100, 1))
           for j in order]
    sw = Image.new('RGB', (k * 100, 100))
    dr = ImageDraw.Draw(sw)
    fnt = font(12)
    for n, c in enumerate(pal):
        dr.rectangle([n * 100, 0, n * 100 + 99, 99], fill=c['hex'])
        lum = sum(int(c['hex'][i:i + 2], 16) for i in (1, 3, 5)) / 3
        dr.text((n * 100 + 6, 80), '%s %.0f%%' % (c['hex'], c['share_pct']), fill=(0, 0, 0) if lum > 128 else (255, 255, 255), font=fnt)
    sw.save(out + '/palette.png')
    return pal


# ---- metrics -------------------------------------------------------------------
def pct(L, p):
    return L[min(len(L) - 1, int(p * len(L)))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--out')
    ap.add_argument('--skip-download', action='store_true', help='reuse files already in --out')
    a = ap.parse_args()
    t_start = time.time()
    vid = video_id(a.url)
    out = os.path.abspath(a.out or '%s/projects/bluepill/refs/%s' % (WS, vid))
    os.makedirs(out, exist_ok=True)
    timings = {}

    t = time.time()
    video = find_video(out)
    if a.skip_download and video:
        meta = json.load(open(out + '/metadata.json')) if os.path.exists(out + '/metadata.json') else {}
    else:
        log('downloading', vid)
        meta = download(vid, out)
        video = find_video(out)
    if not video:
        sys.exit('no video downloaded')
    timings['download'] = round(time.time() - t, 1)
    total = probe_duration(video)
    total_min = total / 60
    log('video', os.path.basename(video), '%.1fs' % total)

    # words / sentences
    cap = find_caption(out)
    words, sents, smode = [], [], None
    if cap:
        words = words_from_json3(cap)
        sents, smode = sentences_from_words(words)
        json.dump(words, open(out + '/words.json', 'w'))
        open(out + '/sentences.txt', 'w').write('\n'.join('[%s] %s' % (mmss(t0), s) for t0, s in sents))
        log('captions', os.path.basename(cap), len(words), 'words', len(sents), 'sentences', '(split by %s)' % smode)
    else:
        log('NO CAPTIONS: text metrics skipped')

    # frames
    t = time.time()
    log('decoding frames')
    S = analyse_frames(video)
    timings['frames'] = round(time.time() - t, 1)
    total_f = S['N'] / FPS
    ev = detect_events(S)
    shots = build_shots(ev, total_f)
    json.dump(ev, open(out + '/events.json', 'w'))
    json.dump(shots, open(out + '/shots.json', 'w'))
    log('events', len(ev), 'shots', len(shots))

    t = time.time()
    sheets = shot_sheets(video, shots, out)
    hook_sheet(video, out)
    pal = palette(video, out)
    timings['sheets'] = round(time.time() - t, 1)

    # metrics
    M = {'video_id': vid, 'title': meta.get('title'), 'duration_s': round(total_f, 2)}
    L = sorted(s['len'] for s in shots)
    n = len(shots)
    M['visual'] = dict(
        shots=n, cuts_per_min=round(n / total_min, 1),
        pops_per_min=round(sum(1 for e in ev if 0.1 <= e['frac'] < 0.3) / total_min, 1),
        visible_changes_per_min=round(sum(1 for e in ev if e['frac'] >= 0.1) / total_min, 1),
        shot_p10_s=round(pct(L, .1), 2), shot_median_s=round(st.median(L), 2),
        shot_p90_s=round(pct(L, .9), 2), shot_max_s=round(L[-1], 1),
        white_dominant_pct_gt60=round(100 * float(S['white60'].mean()), 1),
        white_dominant_pct_gt40=round(100 * float(S['white40'].mean()), 1),
        mean_luminance=round(float(S['lum'].mean()), 1),
        text_edge_density_mean_E=round(float(S['edge'].mean()), 4),
        text_heavy_frames_pct_E=round(100 * float((S['edge'] > 0.02).mean()), 1),
        palette=pal)
    M['text'] = None
    if words:
        ws = [len(toks(s)) for _, s in sents]
        ns = len(sents)
        qs = sum(1 for _, s in sents if s.rstrip().endswith('?'))
        M['text'] = dict(
            sentence_split=smode, words=len(words),
            wpm=round(len(words) / total_min, 1),
            wpm_speaking_span=round(len(words) / max(0.1, (words[-1]['start'] - words[0]['start']) / 60), 1),
            sentences=ns, sentences_per_min=round(ns / total_min, 1),
            words_per_sentence_mean=round(len(toks(' '.join(s for _, s in sents))) / ns, 1),
            words_per_sentence_median=st.median(ws),
            pct_sentences_le6w=round(100 * sum(1 for x in ws if x <= 6) / ns, 1),
            questions_per_min=round(qs / total_min, 2))
        if smode == 'pause':
            M['text']['note'] = 'auto captions without punctuation: sentence metrics are [E] (pause-split)'
    # hook
    hs = [s for s in shots if s['start'] < 30]
    M['hook'] = dict(shots=[dict(start=s['start'], len=s['len']) for s in hs],
                     words=' '.join(w['text'] for w in words if w['start'] < 30))
    M['chapters'] = meta.get('chapters')
    json.dump(M, open(out + '/METRICS.json', 'w'), indent=1)

    # REF md
    write_md(out, vid, meta, M, sheets, sents, total, timings)
    timings['total'] = round(time.time() - t_start, 1)
    json.dump(timings, open(out + '/timings.json', 'w'))
    log('done', timings, '->', out)


def cmp_row(label, key, mine, uf=UF, ours=None, src=None):
    def f(x):
        return '-' if x is None else str(x)
    return '| %s | %s | %s | %s |' % (label, f(mine), f(uf.get(key)), f((ours or {}).get(key)))


def write_md(out, vid, meta, M, sheets, sents, total, timings):
    v, t = M['visual'], M['text']
    L = []
    L.append('# REF-%s: %s' % (vid, M['title']))
    L.append('')
    L.append('Channel: %s | Duration: %s (%.0fs) | Views: %s | Uploaded: %s' % (
        meta.get('channel') or meta.get('uploader'), mmss(total), total, meta.get('view_count'), meta.get('upload_date')))
    L.append('Source: https://www.youtube.com/watch?v=%s | Analysed %s at <=480p (refwatch). Labels: [V] measured, [E] estimate/heuristic.' % (vid, time.strftime('%Y-%m-%d')))
    L.append('')
    L.append('## Description')
    L.append('')
    L.append('```')
    L.append((meta.get('description') or '')[:1500])
    L.append('```')
    L.append('')
    L.append('## Chapters / structure')
    L.append('')
    if meta.get('chapters'):
        for c in meta['chapters']:
            L.append('- %s  %s' % (mmss(c['start_time']), c['title']))
    else:
        L.append('No chapters on the video. First lines of each ~minute from the captions:')
        L.append('')
        last = -60
        for t0, s in sents:
            if t0 - last >= 60:
                L.append('- %s  %s' % (mmss(t0), s[:110]))
                last = t0
    L.append('')
    L.append('## Metrics (columns: this video | UF reference | our animatic)')
    L.append('')
    L.append('UF = Unknown Frequencies mJS-QVw8lzY, FORMAT-BIBLE.md sections 1-2. Ours = QA-ANIMATIC.md / text_metrics.json. "-" = no baseline.')
    L.append('')
    L.append('| Metric | This video | UF | Ours |')
    L.append('|---|---|---|---|')
    mt = t or {}
    for lab, key in [('Words per minute', 'wpm'), ('Sentences/min', 'sentences_per_min'),
                     ('Words/sentence mean', 'words_per_sentence_mean'),
                     ('Words/sentence median', 'words_per_sentence_median'),
                     ('% sentences <=6 words', 'pct_sentences_le6w'), ('Questions/min', 'questions_per_min')]:
        L.append(cmp_row(lab, key, mt.get(key) if t else 'n/a (no captions)', UF, OURS_TEXT))
    for lab, key in [('Hard cuts/min (shots/min)', 'cuts_per_min'), ('Pops/min (10-30% px)', 'pops_per_min'),
                     ('Visible changes/min (>=10% px)', 'visible_changes_per_min'),
                     ('Shot length median s', 'shot_median_s'), ('Shot length p90 s', 'shot_p90_s'),
                     ('Shot length max s', 'shot_max_s')]:
        L.append(cmp_row(lab, key, v.get(key), UF, OURS))
    L.append('| Shot length p10 s | %s | - | - |' % v['shot_p10_s'])
    L.append('| White-dominant frames %% (>60%% px lum>235) | %s | - | - |' % v['white_dominant_pct_gt60'])
    L.append('| White-dominant frames %% (>40%% px lum>235) | %s | 25.6 | 41.9 |' % v['white_dominant_pct_gt40'])
    L.append('| Mean luminance /255 | %s | 135 | 59 (draft v1) |' % v['mean_luminance'])
    L.append('| Text share [E]: mean strong-edge density / %% frames >2%% | %s / %s | - | - |' % (v['text_edge_density_mean_E'], v['text_heavy_frames_pct_E']))
    L.append('')
    if t and t.get('note'):
        L.append('Note: ' + t['note'])
        L.append('')
    L.append('Caveat: FORMAT-BIBLE pops/min (7.4) and visible changes/min (18.1) came from the Editor\'s windowed seg2 detector; the raw events.js detector used here gives about 11 and 25 on UF itself (see README). Compare other videos against the UF re-run in refs/mJS-QVw8lzY/METRICS.json for like-for-like pops and visible changes.')
    L.append('')
    L.append('Detector: 30 fps, 320x180 gray; events = local maxima of mean frame diff >2.5; cut = >=30% of 80x45 pixels changed by >25 and >=0.45 s after the previous cut; pop = 10-30%. Same settings as analysis_teardown_scripts (events.js, shots.py).')
    L.append('')
    L.append('## Palette (6 colours, k-means on 1 fps frames)')
    L.append('')
    L.append('![palette](palette.png)')
    L.append('')
    L.append(' '.join('`%s` %s%%' % (c['hex'], c['share_pct']) for c in v['palette']))
    L.append('')
    L.append('## Hook (first 30 s)')
    L.append('')
    L.append('Sheet: `hook_sheet.jpg` (one frame per second).')
    L.append('')
    L.append('Shots: ' + ', '.join('%.1f+%.1fs' % (s['start'], s['len']) for s in M['hook']['shots']))
    L.append('')
    L.append('Words: ' + (M['hook']['words'] or '(no captions)'))
    L.append('')
    L.append('## Sheets')
    L.append('')
    for f in sheets:
        L.append('- `%s`' % f)
    L.append('')
    L.append('Each cell: shot number, start time, shot length. 8 columns, <=40 shots per sheet. View with view_image.')
    L.append('')
    L.append('## Recipe (Morpheus fills this by viewing the sheets; leave blank until viewed)')
    L.append('')
    for h in ('Script grammar', 'Visual grammar', 'Pacing', 'What to copy', 'What to avoid'):
        L.append('### %s' % h)
        L.append('')
        L.append('')
    open(out + '/REF-%s.md' % vid, 'w').write('\n'.join(L))


if __name__ == '__main__':
    main()
