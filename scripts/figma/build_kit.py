#!/usr/bin/env python3
"""Build the Figma import kit from video2/assets (no generation, no network).
Run with ~/.venvs/refwatch/bin/python scripts/figma/build_kit.py"""
import json, os, shutil, statistics, glob
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

V2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../projects/bluepill/video2')
V2 = os.path.normpath(V2)
V1 = os.path.normpath(os.path.join(V2, '../video1/images'))
KIT = os.path.join(V2, 'previz/kit')
sb = json.load(open(os.path.join(V2, 'storyboard.json')))
hs = defaultdict(list); beats_by_src = defaultdict(set)
shot_beat = {s['id']: s['beat'] for s in sb['shots']}
for e in sb['events']:
    if e['kind'] == 'sprite':
        hs[e['src']].append(e['h']); beats_by_src[e['src']].add(shot_beat[e['shot']])
bg_use = defaultdict(set)
for s in sb['shots']:
    if s['bg'].get('src'): bg_use[s['bg']['src']].add(s['beat'])

FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
rows = []  # (group, id, kind, w, h, note, beats)

def reset():
    if os.path.isdir(KIT):
        shutil.rmtree(KIT)
    for d in ('sprites', 'props', 'plates', 'maps'):
        os.makedirs(os.path.join(KIT, d))

def kind_of(name):
    if name.startswith('prop__'): return 'props'
    return 'sprites'

def beats_txt(b):
    b = sorted(b)
    return ','.join(map(str, b[:8])) + ('…' if len(b) > 8 else '') if b else 'unused'

reset()
# sprites + props
for f in sorted(os.listdir(os.path.join(V2, 'assets/sprites'))):
    if not f.endswith('.png'): continue
    im = Image.open(os.path.join(V2, 'assets/sprites', f)).convert('RGBA')
    target = round(statistics.median(hs[f])) if hs[f] else min(im.height, 400)
    target = min(target, im.height)
    w = round(im.width * target / im.height)
    im = im.resize((w, target), Image.LANCZOS)
    im.save(os.path.join(KIT, 'sprites', f))
    rows.append(('sprites', f, 'sprite', w, target, 'median storyboard height' if hs[f] else 'not used in storyboard; default 400', beats_txt(beats_by_src[f])))
for f in sorted(os.listdir(os.path.join(V2, 'assets/props'))):
    if not f.endswith('.png'): continue
    im = Image.open(os.path.join(V2, 'assets/props', f)).convert('RGBA')
    target = min(round(statistics.median(hs[f])) if hs[f] else 300, im.height)
    w = round(im.width * target / im.height)
    im.resize((w, target), Image.LANCZOS).save(os.path.join(KIT, 'props', f))
    rows.append(('props', f, 'prop', w, target, 'median storyboard height' if hs[f] else 'not used in storyboard; default 300', beats_txt(beats_by_src[f])))
# plates (delivered + video1 plates used as backgrounds) scaled to cover 1920x1080
plates = {}
for f in os.listdir(os.path.join(V2, 'assets/plates')): plates[f] = os.path.join(V2, 'assets/plates', f)
for f in bg_use:
    if f not in plates and os.path.exists(os.path.join(V1, f)): plates[f] = os.path.join(V1, f)
for f, p in sorted(plates.items()):
    if f == 'board_base.png' and False: pass
    im = Image.open(p).convert('RGB')
    sc = 1080 / im.height
    im = im.resize((round(im.width * sc), 1080), Image.LANCZOS)
    im.save(os.path.join(KIT, 'plates', f))
    rows.append(('plates', f, 'plate', im.width, 1080, 'background; scaled x%.3f to fill 1080 high (renderer uses cover)' % sc, beats_txt(bg_use.get(f, set()))))
for f in sorted(os.listdir(os.path.join(V2, 'assets/maps'))):
    im = Image.open(os.path.join(V2, 'assets/maps', f)).convert('RGB')
    sc = 1080 / im.height
    im.resize((round(im.width * sc), 1080), Image.LANCZOS).save(os.path.join(KIT, 'maps', f))
    rows.append(('maps', f, 'map', round(im.width * sc), 1080, 'map background (renderer draws code maps; plates are reference)', beats_txt(bg_use.get(f, set()))))
# sourced
src_dir = os.path.join(V2, 'assets/sourced')
os.makedirs(os.path.join(KIT, 'sourced'))
for f in ('skull_front_pd.png', 'skull_front_pd_small.png', 'homer_bust_pd.png', 'greek_line_9_394.png'):
    p = os.path.join(src_dir, f)
    if os.path.exists(p):
        im = Image.open(p).convert('RGBA'); t = min(round(statistics.median(hs[f])) if hs[f] else 400, im.height)
        w = round(im.width * t / im.height); im.resize((w, t), Image.LANCZOS).save(os.path.join(KIT, 'sourced', f))
        rows.append(('sourced', f, 'sourced', w, t, 'sourced picture', beats_txt(beats_by_src[f] | bg_use.get(f, set()))))
# renderer-drawn ids with no image
code_ids = sorted(set(hs) - {r[1] for r in rows})
json.dump({'rows': rows, 'code_only': code_ids}, open(os.path.join(KIT, 'kit_index.json'), 'w'), indent=1)

# contact sheets
def sheet(name_prefix, items, bg=(200, 200, 200), cell=(230, 250), cols=10):
    pages = []
    per = cols * 6
    for pi in range(0, len(items), per):
        chunk = items[pi:pi + per]
        r = (len(chunk) + cols - 1) // cols
        W, H = cols * cell[0], r * cell[1]
        S = Image.new('RGB', (W, H), bg); d = ImageDraw.Draw(S)
        for i, (fid, path, grp) in enumerate(chunk):
            x, y = (i % cols) * cell[0], (i // cols) * cell[1]
            im = Image.open(path).convert('RGBA'); im.thumbnail((cell[0] - 10, cell[1] - 42))
            S.paste(im, (x + (cell[0] - im.width) // 2, y + 4 + (cell[1] - 42 - im.height)), im)
            lab = fid[:-4]
            if len(lab) > 27: lab = lab[:26] + '…'
            d.rectangle([x, y + cell[1] - 36, x + cell[0] - 1, y + cell[1] - 1], fill=(30, 30, 30))
            d.text((x + 4, y + cell[1] - 33), lab, fill=(255, 255, 255), font=FONT)
            d.text((x + 4, y + cell[1] - 17), '%dx%d' % im.size if False else '', fill=(200, 200, 200), font=FONT)
        n = '%s_%d.jpg' % (name_prefix, pi // per + 1)
        S.save(os.path.join(KIT, n), quality=88); pages.append(n)
    return pages
cat = lambda g: [(r[1], os.path.join(KIT, g, r[1]), g) for r in rows if r[0] == g]
sheets = sheet('kit_sheet_sprites', cat('sprites'))
sheets += sheet('kit_sheet_props', cat('props'), cell=(230, 200))
sheets += sheet('kit_sheet_plates', cat('plates') + cat('maps') , cell=(300, 200), cols=8, bg=(60, 60, 60))
print('rows', len(rows), 'code_only', len(code_ids), sheets)

# KIT.md
by = defaultdict(list)
for r in rows: by[r[0]].append(r)
L = ['# KIT.md: Figma import kit', '',
     'Frame = 1920x1080. Layer name = asset id (filename without .png). Sizes below are the default drop size = the median height the storyboard uses, so a freshly dragged layer is roughly right; resize freely (pull reads the final height).',
     'Sprites are bottom-anchored in the renderer: the **bottom edge of the layer is the feet** (storyboard `y`), the horizontal centre is `x`. Insets (picture-in-picture) are centre-anchored.', '',
     'Counts: ' + ', '.join('%s %d' % (g, len(v)) for g, v in by.items()) + ' = %d images.' % len(rows),
     'Contact sheets: ' + ', '.join(sheets), '']
for g in ('sprites', 'props', 'plates', 'maps', 'sourced'):
    if g not in by: continue
    L += ['## ' + g, '', '| asset id | kind | default size on 1920x1080 | note | used in beats |', '|---|---|---|---|---|']
    for r in by[g]:
        L.append('| %s | %s | %dx%d | %s | %s |' % (r[1][:-4], r[2], r[3], r[4], r[5], r[6]))
    L.append('')
L += ['## Renderer-drawn ids (no image in the kit)', '',
      'These are drawn in code by Remotion (rings, pins, arrows, icons, NP cutouts). To place one in Figma, draw a rectangle (or text) and **name the layer with the id**; pull records its box and ignores the fill.', '',
      ', '.join(c[:-4] for c in code_ids if c not in ()), '']
open(os.path.join(V2, 'previz/KIT.md'), 'w').write('\n'.join(L))
shutil.copy(os.path.join(V2, 'previz/KIT.md'), os.path.join(KIT, 'KIT.md'))
