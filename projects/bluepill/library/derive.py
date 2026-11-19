#!/usr/bin/env python3
"""derive.py <id> <master.png> <out.png> <change text> [--check ground|none] [--size WxH] [--mode relight|same] [--tries 3]
Derives a variant from a master via gen.py --refs (images/edits endpoint). Prompt form:
 "Use the attached image as the exact scene. Keep every rock, tree, plant, object and the boulder in exactly the same position and shape. Change ONLY: <change>. Same painting style."
Verifies with ground_diff (lower 60%). Re-rolls up to --tries; keeps best attempt, writes <out>.check.json."""
import sys, os, json, shutil, gen
import numpy as np
from PIL import Image, ImageFilter
def load(p, size=None):
    im = Image.open(p).convert('RGB')
    return im.resize(size) if size else im
def _edges(im, frac):
    g = np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(1.5)), float)
    gy, gx = np.gradient(g); m = np.hypot(gx, gy)[int(im.height * (1 - frac)):]
    h, w = m.shape
    box = np.asarray(Image.fromarray(m.astype('float32'), mode='F').resize((w // 8, h // 8), Image.BOX).resize((w, h), Image.BILINEAR))
    return m / (box + 1e-3)
def ground_diff(master, var, frac=0.6):
    """ground = lower `frac` of the image. raw_mad = mean |a-b| (0-255) there; edge_corr = correlation of
    local-contrast-normalised edge maps there (relight-proof: ~0.6 for a true relit derivative, ~0.0 for a different scene,
    1.0 identical); top30 = mean |a-b| in the top 30% (sky) to prove the sky changed."""
    a = load(master); b = load(var, a.size)
    y0 = int(a.height * (1 - frac))
    raw = float(np.abs(np.asarray(a, float)[y0:] - np.asarray(b, float)[y0:]).mean())
    ec = float(np.corrcoef(_edges(a, frac).ravel(), _edges(b, frac).ravel())[0, 1])
    sky = float(np.abs(np.asarray(a, float)[:int(a.height*.3)] - np.asarray(b, float)[:int(a.height*.3)]).mean())
    return dict(ground_raw_mad=round(raw, 2), ground_edge_corr=round(ec, 3), top30_mad=round(sky, 2))
def derive(cid, master, out, change, size=None, tries=3, check='ground', thr=None, region=0.6, preface=None, extra_refs=()):
    size = size or '%dx%d' % Image.open(master).size
    pf = preface or "Use the attached image as the exact scene. Keep every rock, tree, plant, object and the boulder in exactly the same position and shape."
    prompt = f"{pf} Change ONLY: {change}. Same painting style. No people."
    pdir = os.path.join(gen.HERE, 'prompts'); os.makedirs(pdir, exist_ok=True)
    pf_path = os.path.join(pdir, f'{cid}.txt'); open(pf_path, 'w').write(prompt)
    best = None; log = []
    for t in range(1, tries + 1):
        tmp = out + f'.try{t}.png'
        r = gen.run(f'{cid}_t{t}', tmp, pf_path, [master, *extra_refs], size)
        if r != 'ok': break
        m = ground_diff(master, tmp, region) if check != 'none' else {}
        m['try'] = t; log.append(m); print(cid, m)
        score = -m.get('ground_edge_corr', 0)
        if best is None or score < best[0]: best = (score, tmp)
        if check == 'none' or (thr is not None and m['ground_edge_corr'] >= thr[0] and m['ground_raw_mad'] <= thr[1]): break
    if best:
        shutil.copy(best[1], out)
    for t in range(1, tries + 1):
        p = out + f'.try{t}.png'
        if os.path.exists(p) and not os.environ.get('KEEP'): os.remove(p)
    json.dump(dict(id=cid, master=master, change=change, tries=log), open(out + '.check.json', 'w'), indent=1)
    return log
if __name__ == '__main__':
    a = sys.argv[1:]
    g = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    # --mode relight (lighting changes: raw MAD meaningless, need edge_corr>=0.45) | same (lighting unchanged: raw<=12, edge_corr>=0.8)
    thr = (0.45, 999) if g('--mode', 'relight') == 'relight' else (0.8, 12)
    derive(a[0], a[1], a[2], a[3], g('--size'), int(g('--tries', 3)), g('--check', 'ground'), thr)
