// resolve.js: storyboard.json + words.json -> src/timeline.json (absolute seconds), stages assets into public/a/, lists missing assets.
// usage: node resolve.js            (reads ../storyboard.json and ../audio/words.json)
// Never fails on a missing asset: it becomes {kind:'missing'} and the renderer draws a labelled grey card.
const fs = require('fs');
const path = require('path');
const sharp = require('../../pipeline/node_modules/sharp');

const ROOT = path.resolve(__dirname, '..', '..'); // projects/bluepill
const V2 = path.resolve(__dirname, '..'); // video2
const ASSETS = path.join(V2, 'assets'); // produced by the asset worker (ASSET-PLAN.md names)
const PUB = path.join(__dirname, 'public', 'a');
fs.mkdirSync(PUB, {recursive: true});

const sb = JSON.parse(fs.readFileSync(path.join(V2, 'storyboard.json')));
const W = JSON.parse(fs.readFileSync(path.join(V2, 'audio', 'words.json')));
const FPS = sb.fps || 30;
const DUR = sb.duration_s;

// ---- 1. times -------------------------------------------------------------
const T = (a) => ('t' in a ? a.t : W[a.word].start + (a.off || 0));
const shots = sb.shots.map((s, i) => ({...s, t0: i === 0 ? 0 : T(s.start)}));
shots.forEach((s, i) => { s.t1 = i + 1 < shots.length ? shots[i + 1].t0 : DUR; s.f0 = Math.round(s.t0 * FPS); s.f1 = Math.round(s.t1 * FPS); });
const byId = Object.fromEntries(shots.map((s) => [s.id, s]));
const events = sb.events.map((e, i) => ({...e, i, t: T(e.at)}));

// ---- 2. asset lookup ------------------------------------------------------
// reuse table (ASSET-PLAN.md section 1.1, 2, 3, 5)
const V1IMG = path.join(ROOT, 'video1', 'images');
const IMG3 = path.join(ROOT, 'pipeline', 'remotion-v3a', 'public', 'img3');
const REUSE = {
  'odysseus__neutral__a.png': path.join(IMG3, 'ody.png'),
  'odysseus__point__a.png': path.join(IMG3, 'ody_shout.png'),
  'odysseus__tired_helm__a.png': path.join(IMG3, 'ody.png'), // plan: neutral at 260 px on the map
  'prop__boulder__a.png': path.join(IMG3, 'boulder3.png'),
  'prop__ram__a.png': path.join(IMG3, 'sheep.png'), // plan: reuse sheep.png if the horns read
  'RC11.png': path.join(V1IMG, 'RC11.png'),
  'RS08.png': path.join(V1IMG, 'RS08.png'),
  'RS10.png': path.join(V1IMG, 'RS10.png'),
};
// props on white that need a cutout before use as sprites
const CUTOUT = new Set(['NP01.png', 'NP03.png', 'NP04.png']);
// code-drawn items (ASSET-PLAN 3.2): the renderer draws these as SVG unless a file exists in assets/
const CODE = new Set(['prop__ring_small__a.png', 'prop__ring_large__a.png', 'prop__eye_icon__a.png', 'prop__oneeye_crossed__a.png', 'prop__ship_crossed__a.png', 'prop__ship_icon__a.png', 'prop__height_line__a.png', 'prop__person_silhouette__a.png', 'prop__waterdrops__a.png', 'prop__pin__a.png', 'prop__bone_pin__a.png', 'prop__book_icon__a.png', 'prop__arrow_left__a.png', 'prop__pointer__a.png', 'prop__heart__a.png', 'prop__flame_glow__a.png', 'prop__dustpuff__a.png', 'prop__source_slip_empty__a.png', 'prop__etna_icon__a.png', 'prop__whirlpool__a.png', 'NP04_listing.png', 'polyphemus__silhouette__a.png', 'cyc2__trio_silhouette__a.png', 'crew__line12__a.png', 'crew__huddle4__a.png', 'crew__workers_group__a.png', 'board_base.png', 'map_med_west.png', 'map_med_loop.png', 'map_sicily.png', 'map_world.png', 'map_argolid.png']);
// code items that are built from another sprite when it exists
const DERIVED = {'NP04_listing.png': 'NP04.png', 'prop__ship_icon__a.png': 'NP04.png', 'prop__ship_crossed__a.png': 'NP04.png', 'polyphemus__silhouette__a.png': 'polyphemus__neutral__a.png', 'cyc2__trio_silhouette__a.png': 'cyc2__neutral__a.png', 'crew__line12__a.png': 'crew__neutral__a.png', 'crew__huddle4__a.png': 'crew__neutral__a.png', 'crew__workers_group__a.png': 'crew__neutral__a.png'};

// only the delivery folders count; gen/, rejects/, masters/, checks/, sheets/ hold work in progress and may carry the same file names
const ASSET_DIRS = ['', 'plates', 'sprites', 'props', 'maps', 'sourced', 'sfx'];
function findInAssets(name) {
  for (const d of ASSET_DIRS) { const p = path.join(ASSETS, d, name); if (fs.existsSync(p)) return p; }
  return null;
}
function findReuse(name) {
  if (REUSE[name] && fs.existsSync(REUSE[name])) return REUSE[name];
  const p = path.join(V1IMG, name); // NBxx, NBGxx, NPxx, NB14_crop_left55
  if (fs.existsSync(p)) return p;
  return null;
}

const resolved = {}; // name -> {kind, src, from}
const missing = [];
const jobs = [];
function resolveAsset(name, role) {
  if (resolved[name]) return resolved[name];
  if (name === 'none' || name === 'slide_out_left') return (resolved[name] = {kind: 'control'});
  let p = findInAssets(name), from = 'assets';
  if (!p) { p = findReuse(name); from = 'reuse'; }
  let r;
  if (p) {
    const out = path.join(PUB, name);
    if (CUTOUT.has(name) && from === 'reuse') jobs.push(cutout(p, out)); else jobs.push(fs.promises.copyFile(p, out));
    r = {kind: 'file', src: 'a/' + name, from: from + ':' + path.relative(ROOT, p)};
  } else if (CODE.has(name)) {
    r = {kind: 'code', code: name.replace(/\.png$/, ''), from: 'code'};
    if (DERIVED[name]) { const b = resolveAsset(DERIVED[name], role); if (b.kind === 'file') r.base = b.src; }
  } else {
    r = {kind: 'missing', from: 'placeholder'};
    missing.push({name, role});
  }
  resolved[name] = r;
  return r;
}
// flood-fill white backdrop from the borders (pipeline/cutout.js), then trim
async function cutout(inp, outp, tol = 34) {
  const {data, info} = await sharp(inp).ensureAlpha().raw().toBuffer({resolveWithObject: true});
  const Wd = info.width, H = info.height, bg = [data[0], data[1], data[2]];
  const near = (i) => Math.abs(data[i] - bg[0]) < tol && Math.abs(data[i + 1] - bg[1]) < tol && Math.abs(data[i + 2] - bg[2]) < tol;
  const seen = new Uint8Array(Wd * H), q = [];
  const push = (x, y) => { const p = y * Wd + x; if (!seen[p] && near(p * 4)) { seen[p] = 1; q.push(p); } };
  for (let x = 0; x < Wd; x++) { push(x, 0); push(x, H - 1); } for (let y = 0; y < H; y++) { push(0, y); push(Wd - 1, y); }
  while (q.length) { const p = q.pop(), x = p % Wd, y = (p / Wd) | 0; if (x > 0) push(x - 1, y); if (x < Wd - 1) push(x + 1, y); if (y > 0) push(x, y - 1); if (y < H - 1) push(x, y + 1); }
  for (let p = 0; p < Wd * H; p++) if (seen[p]) data[p * 4 + 3] = 0;
  await sharp(data, {raw: {width: Wd, height: H, channels: 4}}).trim().png().toFile(outp);
}

for (const s of shots) if (s.bg.src) s.bg.asset = resolveAsset(s.bg.src, 'bg:' + s.id);
for (const e of events) if ((e.kind === 'sprite' || e.kind === 'swap') && e.src) e.asset = resolveAsset(e.src, e.kind + ':' + e.shot);
// board frame art (used by every board state and the pings)
const BOARD = {skull: 'skull_front_pd_small.png', anvil: 'prop__anvil__a.png', wall: 'NBG07.png'};
const board = Object.fromEntries(Object.entries(BOARD).map(([k, n]) => [k, resolveAsset(n, 'board:' + k)]));
// sfx hook: files only if present in assets/sfx (none required)
const sfx = events.filter((e) => e.kind === 'sfx').map((e) => ({t: e.t, src: e.src, file: findInAssets(e.src)}));

// ---- 3. board memory: verdict stamps earned in earlier board shots persist on later boards ----
const CARDS = [[560, 420], [1360, 420], [560, 820], [1360, 820]];
const VERDICTS = new Set(['UNPROVEN', 'PLAUSIBLE', 'REAL', 'PROBABLY OLDER']);
const earnedByShot = {};
let earned = [];
for (const s of shots) {
  if (s.bg.type !== 'board') continue;
  earnedByShot[s.id] = earned.slice();
  const states = events.filter((e) => e.shot === s.id && e.kind === 'label' && e.style === 'board').map((e) => e.state);
  if (states.includes('frame4_full_world')) continue; // stamps across the full-screen map are not card stamps
  for (const e of events.filter((e) => e.shot === s.id && e.kind === 'stamp' && VERDICTS.has(e.text))) {
    let best = 0, bd = 1e9; CARDS.forEach(([cx, cy], i) => { const d = Math.hypot(cx - e.x, cy - e.y); if (d < bd) { bd = d; best = i; } });
    if (!earned.some((x) => x.card === best)) earned.push({card: best, text: e.text, sub: e.sub || null});
  }
}
for (const s of shots) if (s.bg.type === 'board') s.earned = earnedByShot[s.id];

// ---- 4. swap targets -> sprite index ---------------------------------------
const stem = (n) => n.replace(/\.png$/, '');
for (const e of events.filter((e) => e.kind === 'swap')) {
  const sprites = events.filter((x) => x.shot === e.shot && x.kind === 'sprite' && x.t <= e.t + 1e-6);
  const tgt = e.target;
  let cands = sprites.filter((x) => stem(x.src).startsWith(tgt + '__') || stem(x.src).startsWith(tgt.replace(/_/g, '__')));
  if (!cands.length) { const m = tgt.match(/^(.*)_(\d+)$/); if (m) { const pre = m[1]; const all = sprites.filter((x) => stem(x.src).startsWith(pre + '__')); if (all[+m[2] - 1]) cands = [all[+m[2] - 1]]; } }
  if (cands.length) e.targetIndex = cands[cands.length - 1].i; else { e.targetIndex = -1; console.warn('swap target not found', e.shot, tgt); }
}

Promise.all(jobs).then(() => {
  const tl = {fps: FPS, duration: DUR, frames: Math.round(DUR * FPS), audio: path.relative(__dirname, path.join(V2, 'audio', 'narration_voice_only.wav')), shots, events, board, sfx, cards: CARDS};
  fs.writeFileSync(path.join(__dirname, 'src', 'timeline.json'), JSON.stringify(tl));
  fs.mkdirSync(path.join(__dirname, 'out'), {recursive: true});
  const uniq = [...new Map(missing.map((m) => [m.name, m])).values()];
  const report = {generated: new Date().toISOString(), assetsDir: fs.existsSync(ASSETS) ? ASSETS : null, resolved: Object.entries(resolved).map(([name, r]) => ({name, ...r})), missing: uniq};
  fs.writeFileSync(path.join(__dirname, 'out', 'assets_report.json'), JSON.stringify(report, null, 1));
  const kinds = {}; for (const r of Object.values(resolved)) kinds[r.kind] = (kinds[r.kind] || 0) + 1;
  console.log('resolved', shots.length, 'shots,', events.length, 'events,', tl.frames, 'frames; assets', JSON.stringify(kinds), '; missing', uniq.length);
});
