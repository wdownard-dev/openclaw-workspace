#!/usr/bin/env python3
"""mk_retry.py <asset> <attempt> [--style-scene scene_cy.png] [--scene "new scene text"] [--note "extra text appended to the scene"] [--refs a,b]
Builds prompts/<asset>_a<attempt>.src.txt from the manifest prompt and registers it in retries.json."""
import sys, json, os, re, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_manifest as B
ap = argparse.ArgumentParser(); ap.add_argument('asset'); ap.add_argument('attempt', type=int)
ap.add_argument('--style-scene'); ap.add_argument('--scene'); ap.add_argument('--note', default=''); ap.add_argument('--refs'); ap.add_argument('--flat2', action='store_true')
ap.add_argument('--noref', action='store_true'); ap.add_argument('--t0', action='store_true'); ap.add_argument('--orig-style', action='store_true'); ap.add_argument('--ody-anchor', action='store_true')
a = ap.parse_args()
m = json.load(open(f'{HERE}/manifest.json')); ent = next(x for x in m['assets'] if x['id'] == a.asset)
p = ent['prompt']; refs = list(ent['refs'])
if a.t0:
    inv = {v: k for k, v in B.REFNAMES.items()}; p = B.prompt_t0([inv[r] for r in refs], a.scene or B.A[a.asset]['scene']); a.scene = None
if a.scene:
    p = re.sub(r'SCENE: .*?\n\n', 'SCENE: ' + a.scene.replace('\\', '\\\\') + '\n\n', p, count=1, flags=re.S)
if a.note:
    p = p.replace('\n\n' + B.FLAT, ' ' + a.note + '\n\n' + B.FLAT, 1)
if a.refs: refs = a.refs.split(',')
if a.noref: refs = []
if a.style_scene:
    n = len(refs) + 1
    sent = (f"Image {n} is a finished SCENE used for rendering STYLE only: copy its flat inked cartoon rendering (bold dark ink outlines, large flat colour areas, one flat shadow tone, only a few simple ink wrinkle lines); "
            f"do NOT copy its composition, its boulder, its sky or its lighting.")
    if p.startswith('Image 1') or 'Image 1' in p.split('\n\nSCENE')[0]:
        p = p.replace('\n\nSCENE:', ' ' + sent + '\n\nSCENE:', 1)
    else:
        p = sent + '\n\nSCENE:' + p.split('SCENE:', 1)[1] if p.startswith('SCENE') else sent + '\n\n' + p
    refs.append(a.style_scene)
if a.flat2 or a.style_scene:
    p = p.replace(B.FLAT, B.FLAT + " Draw with simple graphic shapes like a modern adult animated series: NOT a realistic, 3D-rendered or digitally painted look, no skin pores, no rendered hair strands, no soft gradients, no glossy highlights.", 1)
if a.ody_anchor:
    n = len(refs) + 1
    sent = (f"Image {n} is Odysseus, a human man who does NOT appear in this scene: use his drawing only as the reference for the flat inked cartoon rendering style "
            f"(outline weight, flat colour fills, one cel-shadow tone); do not draw him.")
    p = p.replace('\n\nSCENE:', ' ' + sent + '\n\nSCENE:', 1); refs.append('odysseus_A_flat.png')
if a.orig_style:
    p = p.split('\n\nSTYLE:')[0] + '\n\n' + B.STYLE_ORIG
    p = p.replace(B.KEEP_CH, B.KEEP_CH.replace('no text anywhere', 'the figures are large enough in frame that faces are readable; no text anywhere'))
pf = f'prompts/{a.asset}_a{a.attempt}.src.txt'; open(f'{HERE}/{pf}', 'w').write(p)
r = json.load(open(f'{HERE}/retries.json')) if os.path.exists(f'{HERE}/retries.json') else {}
r[f'{a.asset}:{a.attempt}'] = dict(prompt_file=pf, refs=refs); json.dump(r, open(f'{HERE}/retries.json', 'w'), indent=1)
print(a.asset, a.attempt, refs)
