#!/usr/bin/env python3
"""usage: chargen.py <id> <out.png> <model> <prompt_file> [ref1.png ref2.png ...]
Hard cap: 40 calls, counted in tests/chars_v3/calls.count, each logged to CHARACTER-LOG.md."""
import sys, os, json, base64, subprocess, time, fcntl
ROOT = '/home/williamdownard/.openclaw/workspace/projects/bluepill'
CAP = 40
COST = {'gpt-image-2.6-sunburst': 0.034, 'gpt-image-2': 0.041}
cid, out, model, pfile, *refs = sys.argv[1:]
prompt = open(pfile).read().strip()
cnt_path = f'{ROOT}/tests/chars_v3/calls.count'
with open(cnt_path + '.lock', 'w') as lk:
    fcntl.flock(lk, fcntl.LOCK_EX)
    n = int(open(cnt_path).read()) if os.path.exists(cnt_path) else 0
    if n >= CAP:
        print('CAP REACHED'); sys.exit(2)
    open(cnt_path, 'w').write(str(n + 1))
    call_no = n + 1
est = COST.get(model, 0.04) + (0.007 * len(refs))
t0 = time.time()
if refs:
    cmd = ['curl', '-s', 'https://api.openai.com/v1/images/edits', '-H', f'Authorization: Bearer {os.environ["OPENAI_API_KEY"]}',
           '-F', f'model={model}', '-F', 'size=1024x1024', '-F', 'quality=medium', '-F', f'prompt={prompt}']
    for r in refs:
        cmd += ['-F', f'image[]=@{r}']
else:
    body = json.dumps({'model': model, 'prompt': prompt, 'size': '1024x1024', 'quality': 'medium', 'n': 1})
    cmd = ['curl', '-s', 'https://api.openai.com/v1/images/generations', '-H', f'Authorization: Bearer {os.environ["OPENAI_API_KEY"]}',
           '-H', 'Content-Type: application/json', '-d', body]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=400)
status = 'ok'
try:
    d = json.loads(r.stdout)
    open(out, 'wb').write(base64.b64decode(d['data'][0]['b64_json']))
except Exception as e:
    status = 'ERR ' + (r.stdout[:200].replace('\n', ' ') if r.stdout else str(e))
with open(f'{ROOT}/CHARACTER-LOG.md', 'a') as f:
    f.write(f'| {call_no} | {cid} | {model} | 1024x1024 medium | {"edit, refs=" + ",".join(os.path.basename(x) for x in refs) if refs else "generation"} | {os.path.basename(pfile)} | ~${est:.3f} | {status} | {int(time.time()-t0)}s |\n')
print(call_no, cid, status)
