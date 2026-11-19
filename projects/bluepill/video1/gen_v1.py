#!/usr/bin/env python3
"""Video 1 generator. gpt-image-2.6-sunburst via images/edits.
  gen_v1.py run <asset> <attempt> [--prompt-file F] [--refs a.png,b.png]   one call
  gen_v1.py batch <asset:attempt[:promptfile]> ...                          parallel (4 workers)
  gen_v1.py verdict <asset> <attempt> accepted|rejected "reason"             finalise log row, move files
Every API call (incl. errors) gets a row in cost_log.csv. No call cap (William: no hard cap). Stop flag: video1/STOP.
"""
import sys, os, json, base64, subprocess, time, fcntl, csv, re, shutil, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = f'{HERE}/cost_log.csv'
MODEL = 'gpt-image-2.6-sunburst'
FIELDS = ['timestamp', 'shot_ids', 'asset_id', 'kind', 'model', 'size', 'quality', 'n_refs', 'input_tokens', 'text_in_tokens', 'image_in_tokens', 'output_tokens', 'total_tokens', 'retry', 'http', 'seconds', 'outcome', 'reason', 'file']
BILLING = re.compile(r'insufficient_quota|billing|credit|quota', re.I)

def manifest():
    return json.load(open(f'{HERE}/manifest.json'))

def append_row(row):
    with open(LOG + '.lock', 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        new = not os.path.exists(LOG)
        with open(LOG, 'a', newline='') as f:
            w = csv.DictWriter(f, FIELDS)
            if new: w.writeheader()
            w.writerow(row)

def err_streak_file(): return f'{HERE}/.errstreak'

def bump_err(ok):
    with open(LOG + '.lock', 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        n = int(open(err_streak_file()).read()) if os.path.exists(err_streak_file()) else 0
        n = 0 if ok else n + 1
        open(err_streak_file(), 'w').write(str(n))
        if n >= 4: open(f'{HERE}/STOP', 'w').write('4 consecutive API errors')

def run_call(aid, attempt, prompt_file=None, refs=None):
    if os.path.exists(f'{HERE}/STOP'):
        print('STOP flag present', open(f'{HERE}/STOP').read()); return 'STOP'
    m = manifest(); a = next(x for x in m['assets'] if x['id'] == aid)
    ov = json.load(open(f'{HERE}/retries.json')).get(f'{aid}:{attempt}') if os.path.exists(f'{HERE}/retries.json') else None
    if ov:
        prompt_file = prompt_file or (f"{HERE}/{ov['prompt_file']}" if ov.get('prompt_file') else None)
        refs = refs or ov.get('refs')
    prompt = open(prompt_file).read().strip() if prompt_file else a['prompt']
    refs = a['refs'] if refs is None else refs
    os.makedirs(f'{HERE}/prompts', exist_ok=True); os.makedirs(f'{HERE}/gen', exist_ok=True)
    pf = f'{HERE}/prompts/{aid}_a{attempt}.txt'; open(pf, 'w').write(prompt)
    out = f'{HERE}/gen/{aid}_a{attempt}.png'
    key = os.environ['OPENAI_API_KEY']
    for net_try in range(3):
        t0 = time.time()
        hdr = tempfile.mktemp()
        if refs:
            cmd = ['curl', '-s', '-D', hdr, 'https://api.openai.com/v1/images/edits', '-H', f'Authorization: Bearer {key}',
                   '-F', f'model={MODEL}', '-F', f'size={a["size"]}', '-F', f'quality={a["quality"]}', '-F', f'prompt={prompt}']
            for r in refs: cmd += ['-F', f'image[]=@{HERE}/refs/{r}']
        else:
            body_in = json.dumps({'model': MODEL, 'prompt': prompt, 'size': a['size'], 'quality': a['quality'], 'n': 1})
            cmd = ['curl', '-s', '-D', hdr, 'https://api.openai.com/v1/images/generations', '-H', f'Authorization: Bearer {key}',
                   '-H', 'Content-Type: application/json', '-d', body_in]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            body = r.stdout
        except Exception as e:
            body = json.dumps({'error': {'message': 'curl failure ' + str(e)}})
        headers = open(hdr).read() if os.path.exists(hdr) else ''
        if os.path.exists(hdr): os.remove(hdr)
        http = (re.findall(r'HTTP/[\d.]+ (\d+)', headers) or ['0'])[-1]
        secs = int(time.time() - t0)
        row = dict(timestamp=time.strftime('%Y-%m-%dT%H:%M:%S%z'), shot_ids='+'.join(map(str, a['shots'])), asset_id=aid, kind=a['kind'], model=MODEL, size=a['size'],
                   quality=a['quality'], n_refs=len(refs), retry=attempt - 1, http=http, seconds=secs, file='', outcome='', reason='')
        try:
            d = json.loads(body)
            if 'data' not in d: raise ValueError(d.get('error', {}).get('message', body[:200]))
            open(out, 'wb').write(base64.b64decode(d['data'][0]['b64_json']))
            u = d.get('usage', {}) or {}
            det = u.get('input_tokens_details', {}) or {}
            row.update(input_tokens=u.get('input_tokens', ''), text_in_tokens=det.get('text_tokens', ''), image_in_tokens=det.get('image_tokens', ''),
                       output_tokens=u.get('output_tokens', ''), total_tokens=u.get('total_tokens', ''), outcome='pending', file=os.path.relpath(out, HERE))
            append_row(row); bump_err(True)
            print(f'{aid} a{attempt} ok {secs}s in={row["input_tokens"]} out={row["output_tokens"]}'); return 'ok'
        except Exception as e:
            msg = str(e)[:300].replace('\n', ' ')
            row.update(outcome='api_error', reason=msg); append_row(row); bump_err(False)
            print(f'{aid} a{attempt} ERROR http={http} {msg}')
            if BILLING.search(msg) and http in ('400', '402', '403', '429') and 'rate' not in msg.lower():
                open(f'{HERE}/STOP', 'w').write('billing/quota: ' + msg); return 'STOP'
            if http == '429' or http.startswith('5'):
                ra = re.findall(r'(?i)retry-after:\s*(\d+)', headers)
                time.sleep(int(ra[0]) if ra else 20 * (net_try + 1)); continue
            return 'ERR'
    return 'ERR'

def verdict(aid, attempt, outcome, reason):
    with open(LOG + '.lock', 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        rows = list(csv.DictReader(open(LOG)))
        for r in rows:
            if r['asset_id'] == aid and r['retry'] == str(attempt - 1) and r['outcome'] == 'pending':
                r['outcome'] = outcome; r['reason'] = reason
        with open(LOG, 'w', newline='') as f:
            w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
    src = f'{HERE}/gen/{aid}_a{attempt}.png'
    m = manifest(); a = next(x for x in m['assets'] if x['id'] == aid)
    if outcome == 'accepted':
        shutil.copy(src, f'{HERE}/images/{aid}.png')
    else:
        os.makedirs(f'{HERE}/rejects', exist_ok=True)
        shutil.copy(src, f'{HERE}/rejects/{aid}_a{attempt}.png')
        open(f'{HERE}/rejects/{aid}_a{attempt}.txt', 'w').write(reason + '\n')
    a['attempts'].append(dict(attempt=attempt, outcome=outcome, reason=reason))
    a['status'] = 'accepted' if outcome == 'accepted' else ('rejected_a%d' % attempt)
    json.dump(m, open(f'{HERE}/manifest.json', 'w'), indent=1, ensure_ascii=False)

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'run':
        pf = sys.argv[sys.argv.index('--prompt-file') + 1] if '--prompt-file' in sys.argv else None
        run_call(sys.argv[2], int(sys.argv[3]), pf)
    elif c == 'batch':
        jobs = []
        for s in sys.argv[2:]:
            p = s.split(':'); jobs.append((p[0], int(p[1]), p[2] if len(p) > 2 else None))
        with ThreadPoolExecutor(4) as ex:
            futs = []
            for j in jobs:
                futs.append(ex.submit(run_call, *j)); time.sleep(2)
            [f.result() for f in futs]
    elif c == 'verdict':
        verdict(sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5])
