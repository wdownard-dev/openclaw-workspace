#!/usr/bin/env python3
"""V5 plates asset generator. gpt-image-2.6-sunburst via curl.
  gen.py run <call_id> <out.png> <prompt_file> [--size WxH] [--refs a.png,b.png]
  gen.py edit <call_id> <out.png> <prompt_file> <master.png[,extra.png]> [--size WxH]   (derive a variant: --refs path already uses POST /v1/images/edits)
  gen.py batch <jobs.json>        jobs: [{id,out,prompt_file,refs:[],size}], 3 workers, 2 s stagger
Every call (incl. errors) is a row in SPEND.csv. HARD CAP: see CAP estimated; a STOP file is written and no further call is made.
Cost estimate per call from the usage block: output tokens $30/M, image input $10/M, text input $5/M (TOOLS.md measured $30/M out).
"""
import sys, os, json, base64, subprocess, time, fcntl, csv, re, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = f'{HERE}/SPEND.csv'
MODEL = 'gpt-image-2.6-sunburst'
CAP = 13.59
FIELDS = ['timestamp', 'call_id', 'model', 'size', 'quality', 'n_refs', 'text_in_tokens', 'image_in_tokens', 'output_tokens',
          'est_cost_usd', 'running_total_usd', 'http', 'seconds', 'status', 'file', 'prompt_file', 'refs']
BILLING = re.compile(r'insufficient_quota|billing|credit|quota', re.I)

def est(u, n_refs, size):
    if u and u.get('output_tokens'):
        det = u.get('input_tokens_details', {}) or {}
        return (u['output_tokens'] * 30 + det.get('image_tokens', 0) * 10 + det.get('text_tokens', 0) * 5) / 1e6
    # fallback if usage missing: by size
    base = 0.034 if size.startswith('1536') or size.endswith('1536') else 0.028
    return base + 0.008 * n_refs

def total():
    if not os.path.exists(LOG): return 0.0
    rows = list(csv.DictReader(open(LOG)))
    return sum(float(r['est_cost_usd'] or 0) for r in rows)

def append(row):
    with open(LOG + '.lock', 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        new = not os.path.exists(LOG)
        row['running_total_usd'] = f"{total() + float(row['est_cost_usd']):.4f}"
        with open(LOG, 'a', newline='') as f:
            w = csv.DictWriter(f, FIELDS)
            if new: w.writeheader()
            w.writerow(row)
        if float(row['running_total_usd']) >= CAP:
            open(f'{HERE}/STOP', 'w').write(f'HARD CAP reached: {row["running_total_usd"]}')

def run(cid, out, prompt_file, refs=(), size='1024x1024', quality='medium'):
    if os.path.exists(f'{HERE}/STOP'):
        print('STOP:', open(f'{HERE}/STOP').read()); return 'STOP'
    key = os.environ.get('OPENAI_API_KEY')
    if not key: print('NO KEY'); return 'NOKEY'
    prompt = open(prompt_file).read().strip()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for net_try in range(3):
        t0 = time.time(); hdr = tempfile.mktemp()
        if refs:
            cmd = ['curl', '-s', '-D', hdr, 'https://api.openai.com/v1/images/edits', '-H', f'Authorization: Bearer {key}',
                   '-F', f'model={MODEL}', '-F', f'size={size}', '-F', f'quality={quality}', '-F', f'prompt={prompt}']
            for r in refs: cmd += ['-F', f'image[]=@{r}']
        else:
            body_in = json.dumps({'model': MODEL, 'prompt': prompt, 'size': size, 'quality': quality, 'n': 1})
            cmd = ['curl', '-s', '-D', hdr, 'https://api.openai.com/v1/images/generations', '-H', f'Authorization: Bearer {key}',
                   '-H', 'Content-Type: application/json', '-d', body_in]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=600); body = r.stdout
        except Exception as e:
            body = json.dumps({'error': {'message': 'curl failure ' + str(e)}})
        headers = open(hdr).read() if os.path.exists(hdr) else ''
        if os.path.exists(hdr): os.remove(hdr)
        http = (re.findall(r'HTTP/[\d.]+ (\d+)', headers) or ['0'])[-1]
        secs = int(time.time() - t0)
        row = dict(timestamp=time.strftime('%Y-%m-%dT%H:%M:%S%z'), call_id=cid, model=MODEL, size=size, quality=quality, n_refs=len(refs),
                   http=http, seconds=secs, file='', prompt_file=os.path.relpath(prompt_file, HERE), refs=';'.join(os.path.basename(x) for x in refs),
                   text_in_tokens='', image_in_tokens='', output_tokens='', est_cost_usd='0', status='')
        try:
            d = json.loads(body)
            if 'data' not in d: raise ValueError(d.get('error', {}).get('message', body[:200]))
            open(out, 'wb').write(base64.b64decode(d['data'][0]['b64_json']))
            u = d.get('usage', {}) or {}; det = u.get('input_tokens_details', {}) or {}
            row.update(text_in_tokens=det.get('text_tokens', ''), image_in_tokens=det.get('image_tokens', ''), output_tokens=u.get('output_tokens', ''),
                       est_cost_usd=f'{est(u, len(refs), size):.4f}', status='ok', file=os.path.relpath(out, HERE))
            append(row); print(f'{cid} ok {secs}s out={row["output_tokens"]} est=${row["est_cost_usd"]} total=${row["running_total_usd"]}'); return 'ok'
        except Exception as e:
            msg = str(e)[:300].replace('\n', ' ')
            row.update(status='api_error: ' + msg); append(row)
            print(f'{cid} ERROR http={http} {msg}')
            if BILLING.search(msg) and http in ('400', '402', '403', '429') and 'rate' not in msg.lower():
                open(f'{HERE}/STOP', 'w').write('billing/quota: ' + msg); return 'STOP'
            if http == '429' or http.startswith('5'):
                ra = re.findall(r'(?i)retry-after:\s*(\d+)', headers)
                time.sleep(int(ra[0]) if ra else 20 * (net_try + 1)); continue
            return 'ERR'
    return 'ERR'

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'run':
        a = sys.argv[2:]
        size = a[a.index('--size') + 1] if '--size' in a else '1024x1024'
        refs = a[a.index('--refs') + 1].split(',') if '--refs' in a else []
        run(a[0], a[1], a[2], refs, size)
    elif c == 'batch':
        jobs = json.load(open(sys.argv[2]))
        with ThreadPoolExecutor(3) as ex:
            futs = []
            for j in jobs:
                futs.append(ex.submit(run, j['id'], j['out'], j['prompt_file'], j.get('refs', []), j.get('size', '1024x1024'))); time.sleep(2)
            [f.result() for f in futs]
    elif c == 'edit':  # gen.py edit <id> <out.png> <prompt_file> <master.png[,extra.png]> [--size WxH]  (images/edits endpoint; same as run --refs)
        a = sys.argv[2:]
        size = a[a.index('--size') + 1] if '--size' in a else '1536x1024'
        run(a[0], a[1], a[2], a[3].split(','), size)
    elif c == 'total':
        print(f'{total():.4f}')
