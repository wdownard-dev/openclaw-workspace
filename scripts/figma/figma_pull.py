#!/usr/bin/env python3
"""Pull a Figma previz file and translate it into a storyboard patch.

  figma_pull.py <file_key_or_url> [--out DIR]         live: REST read + PNG export   [U until William's file exists]
  figma_pull.py --fixture scripts/figma/fixtures/sample_file.json [--out DIR]   offline: parse a saved /v1/files JSON,
                                                       frames are rendered locally from the kit PNGs instead of /v1/images

Outputs in DIR: layout.json, storyboard_patch.json, frames/B###.png, contact_*.jpg
Never touches storyboard.json (see apply_patch.py). Token: env FIGMA_TOKEN (never printed).
Coordinates: frame px == renderer px (1920x1080). Sprite x = layer centre, y = layer bottom edge (feet), h = layer height.
"""
import argparse, datetime, json, math, os, re, subprocess, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.normpath(os.path.join(HERE, '../../projects/bluepill/video2'))
KIT = os.path.join(V2, 'previz/kit')
API = 'https://api.figma.com'
FRAME_RE = re.compile(r'^B(\d+)(?:[ _-]*(s\d+\w*))?\b', re.I)


# ---------------------------------------------------------------- REST
def api_get(path, retries=6):
    tok = os.environ.get('FIGMA_TOKEN')
    if not tok:
        sys.exit('FIGMA_TOKEN not set')
    url = API + path
    delay = 2
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={'X-Figma-Token': tok})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < retries - 1:
                wait = int(e.headers.get('Retry-After') or delay)
                print('  HTTP %d, waiting %ds' % (e.code, wait), file=sys.stderr)
                time.sleep(min(wait, 120)); delay = min(delay * 2, 60); continue
            sys.exit('Figma API %s -> HTTP %d %s' % (path.split('?')[0], e.code, e.read()[:200]))
        except urllib.error.URLError as e:
            if i < retries - 1:
                time.sleep(delay); delay = min(delay * 2, 60); continue
            sys.exit('network error: %s' % e)


def download(url, dest):
    for i in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r, open(dest, 'wb') as f:
                f.write(r.read())
            return True
        except Exception as e:
            time.sleep(2 * (i + 1))
    return False


def parse_key(s):
    m = re.search(r'figma\.com/(?:file|design|proto|board)/([A-Za-z0-9]+)', s)
    return m.group(1) if m else s


# ---------------------------------------------------------------- parsing
def load_kit():
    try:
        idx = json.load(open(os.path.join(KIT, 'kit_index.json')))
    except Exception:
        return {}, set()
    info = {r[1][:-4]: {'group': r[0], 'w': r[3], 'h': r[4], 'file': r[1]} for r in idx['rows']}
    return info, {c[:-4] for c in idx['code_only']}


def clean_name(n):
    n = n.strip()
    flags = set()
    for m in re.finditer(r'[|#]\s*(inset|mirror)', n, re.I):
        flags.add(m.group(1).lower())
    n = re.split(r'\s*[|#]', n)[0]
    n = re.sub(r'\.(png|jpe?g|webp)$', '', n, flags=re.I)
    n = re.sub(r'(?:\s+(?:copy|\d+))+$', '', n)           # "name 2", "name copy"
    return n, flags


def box(n):
    b = n.get('absoluteBoundingBox') or n.get('absoluteRenderBounds')
    return b


def decompose(t):
    """relativeTransform [[a,c,tx],[b,d,ty]] -> (rotation_deg clockwise on screen, flipped_x)."""
    if not t:
        return 0.0, False
    a, c = t[0][0], t[0][1]
    b, d = t[1][0], t[1][1]
    det = a * d - b * c
    if det < 0:  # M = R * diag(-1, 1)
        return round(math.degrees(math.atan2(-b, -a)), 2), True
    return round(math.degrees(math.atan2(b, a)), 2), False


def layer_record(n, order, frame_bb, info, code_ids):
    nm, flags = clean_name(n.get('name', ''))
    bb = box(n)
    if not bb:
        return None
    size = n.get('size') or {'x': bb['width'], 'y': bb['height']}
    rot, flip = decompose(n.get('relativeTransform'))
    cx = bb['x'] + bb['width'] / 2 - frame_bb['x']
    cy = bb['y'] + bb['height'] / 2 - frame_bb['y']
    w, h = size['x'], size['y']
    rec = {'name': nm, 'raw_name': n.get('name'), 'type': n.get('type'), 'z': order,
           'x': round(cx - w / 2, 1), 'y': round(cy - h / 2, 1), 'width': round(w, 1), 'height': round(h, 1),
           'cx': round(cx, 1), 'cy': round(cy, 1), 'rotation': rot, 'flip_x': flip or 'mirror' in flags,
           'opacity': n.get('opacity', 1), 'flags': sorted(flags)}
    if nm in info:
        rec['kind'] = info[nm]['group']
        k = info[nm]
        if abs((w / h) / (k['w'] / k['h']) - 1) > 0.03:
            rec['warn'] = 'aspect %.2f differs from kit %.2f (layer squashed or cropped; renderer keeps aspect, uses height)' % (w / h, k['w'] / k['h'])
    elif nm in code_ids:
        rec['kind'] = 'code'
    elif n.get('type') == 'TEXT':
        rec['kind'] = 'caption' if nm.upper() == 'CAPTION' or n.get('name', '').upper().startswith('CAPTION') else 'text'
        rec['text'] = n.get('characters', '')
    else:
        rec['kind'] = 'unknown'
    return rec


def walk_layers(node, frame_bb, info, code_ids, out):
    for ch in node.get('children', []):
        if ch.get('visible') is False:
            continue
        nm, _ = clean_name(ch.get('name', ''))
        known = nm in info or nm in code_ids or ch.get('type') == 'TEXT'
        if ch.get('children') and not known:
            walk_layers(ch, frame_bb, info, code_ids, out)          # plain group: flatten
        else:
            r = layer_record(ch, len(out), frame_bb, info, code_ids)
            if r:
                out.append(r)
    return out


def find_frames(doc):
    frames = []
    for page in doc.get('children', []):
        if page.get('type') != 'CANVAS':
            continue
        for ch in page.get('children', []):
            if ch.get('type') in ('FRAME', 'COMPONENT', 'SECTION') and ch.get('type') != 'SECTION':
                frames.append((page['name'], ch))
            elif ch.get('type') == 'SECTION':
                for c2 in ch.get('children', []):
                    if c2.get('type') == 'FRAME':
                        frames.append((page['name'], c2))
    return frames


def parse_file(filejson):
    info, code_ids = load_kit()
    out = []
    for page, fr in find_frames(filejson['document']):
        bb = box(fr)
        if not bb:
            continue
        m = FRAME_RE.match(fr['name'])
        layers = walk_layers(fr, bb, info, code_ids, [])
        out.append({'id': fr['id'], 'name': fr['name'], 'page': page,
                    'beat': int(m.group(1)) if m else None, 'shot_hint': m.group(2) if m else None,
                    'width': bb['width'], 'height': bb['height'], 'layers': layers})
    return out


# ---------------------------------------------------------------- storyboard patch
def build_patch(frames, storyboard_path):
    sb = json.load(open(storyboard_path))
    by_beat = {}
    for s in sb['shots']:
        by_beat.setdefault(s['beat'], []).append(s['id'])
    shots, notes = {}, []
    for fr in frames:
        if fr['beat'] is None:
            notes.append('frame "%s" (page %s) is not named B###; layout recorded, no patch entry' % (fr['name'], fr['page']))
            continue
        cands = by_beat.get(fr['beat'])
        if not cands:
            notes.append('frame %s: beat %d has no shot in storyboard (cut beat?)' % (fr['name'], fr['beat'])); continue
        sid = fr['shot_hint'] if fr['shot_hint'] in cands else cands[0]
        if fr['shot_hint'] and fr['shot_hint'] not in cands:
            notes.append('frame %s: shot hint %s not in beat; used %s' % (fr['name'], fr['shot_hint'], sid))
        if len(cands) > 1 and not fr['shot_hint']:
            notes.append('frame %s: beat has %d shots (%s); patch applied to %s only; name frames B%03d_sNNN to target others' % (fr['name'], len(cands), ','.join(cands), sid, fr['beat']))
        if sid in shots:
            notes.append('frame %s: duplicate for shot %s; later frame wins' % (fr['name'], sid))
        entry = {'beat': fr['beat'], 'frame': fr['name'], 'bg': None, 'sprites': [], 'caption': None, 'unmapped': []}
        scale_x = 1920 / fr['width'] if fr['width'] else 1
        if abs(fr['width'] - 1920) > 1 or abs(fr['height'] - 1080) > 1:
            entry['unmapped'].append('frame is %dx%d, not 1920x1080; coordinates scaled by %.3f' % (fr['width'], fr['height'], scale_x))
        for L in sorted(fr['layers'], key=lambda l: l['z']):                 # z ascending = back to front
            k = L['kind']
            f = scale_x
            if L.get('warn'):
                entry['unmapped'].append('%s: %s' % (L['name'], L['warn']))
            if L['rotation'] and abs(L['rotation']) > 0.5:
                entry['unmapped'].append('%s: rotation %.1f deg ignored (renderer sprites have no rotation field)' % (L['name'], L['rotation']))
            if L['opacity'] is not None and L['opacity'] < 0.99:
                entry['unmapped'].append('%s: opacity %.2f ignored (no opacity field)' % (L['name'], L['opacity']))
            if k in ('plates', 'maps'):
                entry['bg'] = {'type': 'map' if k == 'maps' else ('board' if L['name'] == 'board_base' else 'img'), 'src': L['name'] + '.png'}
                if abs(L['width'] * f - 1920) > 8 and abs(L['height'] * f - 1080) > 8:
                    entry['unmapped'].append('%s: plate moved/resized (renderer always covers the full frame)' % L['name'])
            elif k in ('sprites', 'props', 'sourced', 'code'):
                h = L['height'] * f
                cx, cy = L['cx'] * f, L['cy'] * f
                inset = 'inset' in L['flags']
                ev = {'src': L['name'] + '.png', 'x': round(cx), 'y': round(cy if inset else cy + h / 2), 'h': round(h)}
                if L['flip_x']:
                    ev['mirror'] = True
                if inset:
                    ev['inset'] = True
                if k == 'code':
                    ev['note'] = 'renderer-drawn id'
                entry['sprites'].append(ev)
            elif k == 'caption':
                entry['caption'] = L.get('text', '')
                entry['unmapped'].append('CAPTION text "%s": storyboard has no burned-in captions (rule); recorded only' % L.get('text', '')[:60])
            elif k == 'text':
                entry['unmapped'].append('text layer "%s": no field; use label events by hand' % L.get('text', '')[:40])
            else:
                entry['unmapped'].append('layer "%s" (%s): unknown asset id, skipped' % (L['raw_name'], L['type']))
        shots[sid] = entry
    return {'_meta': {'generated': datetime.datetime.now().isoformat(timespec='seconds'), 'storyboard': os.path.relpath(storyboard_path),
                      'schema': 'sprite: x=centre, y=bottom (feet) or centre if inset, h=height px at 1080; bg replaces shot.bg',
                      'notes': notes}, 'shots': shots}


# ---------------------------------------------------------------- images
def kit_path(name):
    for g in ('sprites', 'props', 'plates', 'maps', 'sourced'):
        p = os.path.join(KIT, g, name + '.png')
        if os.path.exists(p):
            return p


def local_render(fr, dest):
    from PIL import Image
    W, H = int(fr['width']), int(fr['height'])
    base = Image.new('RGB', (W, H), (255, 255, 255))
    for L in sorted(fr['layers'], key=lambda l: l['z']):
        p = kit_path(L['name'])
        if not p:
            continue
        im = Image.open(p).convert('RGBA')
        im = im.resize((max(1, round(L['width'])), max(1, round(L['height']))))
        if L['flip_x']:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if L['rotation']:
            im = im.rotate(-L['rotation'], expand=True, resample=Image.BICUBIC)
        if L['opacity'] < 1:
            a = im.getchannel('A').point(lambda v: int(v * L['opacity'])); im.putalpha(a)
        base.paste(im, (round(L['cx'] - im.width / 2), round(L['cy'] - im.height / 2)), im)
    base.save(dest)


def export_frames(key, frames, outdir):
    os.makedirs(outdir, exist_ok=True)
    ids = [f['id'] for f in frames]
    got = {}
    for i in range(0, len(ids), 15):
        batch = ids[i:i + 15]
        r = api_get('/v1/images/%s?ids=%s&format=png&scale=1' % (key, ','.join(batch)))
        if r.get('err'):
            print('  export error', r['err'], file=sys.stderr)
        for fid, url in (r.get('images') or {}).items():
            if url:
                got[fid] = url
        time.sleep(1)
    paths = {}
    for f in frames:
        url = got.get(f['id'])
        dest = os.path.join(outdir, re.sub(r'[^A-Za-z0-9_.-]+', '_', f['name']) + '.png')
        if url and download(url, dest):
            paths[f['id']] = dest
        else:
            print('  no image for frame', f['name'], file=sys.stderr)
    return paths


def contact_sheets(frames, paths, outdir, maxw=2500, cols=3):
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
    cw = (maxw - 4 * (cols - 1)) // cols
    ch = round(cw * 9 / 16)
    items = [(f, paths[f['id']]) for f in frames if f['id'] in paths]
    out = []
    per = cols * 4
    for pi in range(0, len(items), per):
        chunk = items[pi:pi + per]
        rows = (len(chunk) + cols - 1) // cols
        S = Image.new('RGB', (maxw, rows * (ch + 4)), (40, 40, 40))
        d = ImageDraw.Draw(S)
        for i, (f, p) in enumerate(chunk):
            im = Image.open(p).convert('RGB'); im.thumbnail((cw, ch))
            x, y = (i % cols) * (cw + 4), (i // cols) * (ch + 4)
            S.paste(im, (x, y))
            d.rectangle([x, y, x + 130, y + 28], fill=(0, 0, 0)); d.text((x + 6, y + 3), f['name'][:10], fill=(255, 255, 0), font=font)
        n = os.path.join(outdir, 'contact_%d.jpg' % (pi // per + 1))
        S.save(n, quality=88); out.append(n)
    return out


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file', nargs='?', help='Figma file key or URL')
    ap.add_argument('--out', help='output dir (default video2/previz/pulls/<date>)')
    ap.add_argument('--fixture', help='parse a saved /v1/files JSON instead of calling the API')
    ap.add_argument('--storyboard', default=os.path.join(V2, 'storyboard.json'))
    ap.add_argument('--no-images', action='store_true', help='skip frame export / previews')
    a = ap.parse_args()
    out = a.out or os.path.join(V2, 'previz/pulls', datetime.date.today().isoformat())
    os.makedirs(out, exist_ok=True)
    key = None
    if a.fixture:
        filejson = json.load(open(a.fixture))
    elif a.file:
        key = parse_key(a.file)
        print('reading file', key)
        filejson = api_get('/v1/files/%s' % key)
    else:
        ap.error('give a file key/URL or --fixture')
    frames = parse_file(filejson)
    print('%d top-level frames, %d layers' % (len(frames), sum(len(f['layers']) for f in frames)))
    layout = {'file': key or a.fixture, 'name': filejson.get('name'), 'lastModified': filejson.get('lastModified'),
              'version': filejson.get('version'), 'fixture': bool(a.fixture), 'frames': frames}
    json.dump(layout, open(os.path.join(out, 'layout.json'), 'w'), indent=1)
    patch = build_patch(frames, a.storyboard)
    json.dump(patch, open(os.path.join(out, 'storyboard_patch.json'), 'w'), indent=1)
    if not a.no_images:
        fdir = os.path.join(out, 'frames')
        if a.fixture:
            os.makedirs(fdir, exist_ok=True)
            paths = {}
            for f in frames:
                p = os.path.join(fdir, re.sub(r'[^A-Za-z0-9_.-]+', '_', f['name']) + '.png')
                local_render(f, p); paths[f['id']] = p
            print('frames rendered LOCALLY from kit (fixture mode, not Figma export)')
        else:
            paths = export_frames(key, frames, fdir)
        sheets = contact_sheets(frames, paths, out)
        print('contact sheets:', *sheets)
    print('wrote', os.path.join(out, 'layout.json'), 'and storyboard_patch.json;', len(patch['shots']), 'shots patched')
    for n in patch['_meta']['notes']:
        print('  note:', n)


if __name__ == '__main__':
    main()
