// Prepares public/ assets for video 1: upscaled scene JPEGs (lanczos + light sharpen), trimmed prop PNGs, the NB14 side-fill composite,
// a grain tile, and clipped map geometry from Natural Earth (public domain). Run: node prep_assets.js
const fs = require('fs'), path = require('path');
const sharp = require('../node_modules/sharp');
const IMG = path.resolve(__dirname, '../../video1/images');
const OUT = path.resolve(__dirname, 'public/img');
fs.mkdirSync(OUT, {recursive: true});
const W2 = 2304, H2 = 1296;

(async () => {
  const ids = fs.readdirSync(IMG).filter((f) => /^(NB\d\d|NBG\d\d|RC\d\d|RS\d\d)\.png$/.test(f) && f !== 'NB14.png');
  for (const f of ids) {
    const id = f.replace('.png', '');
    await sharp(path.join(IMG, f)).resize(W2, H2, {kernel: 'lanczos3'}).sharpen({sigma: 0.6, m1: 0.8, m2: 1.6}).jpeg({quality: 90, mozjpeg: true}).toFile(path.join(OUT, id + '.jpg'));
  }
  console.log('scenes', ids.length);

  // props (transparent PNG): trim to content
  const dims = {};
  for (const id of ['NP01', 'NP02', 'NP03', 'NP04']) {
    const b = await sharp(path.join(IMG, id + '.png')).trim({threshold: 8}).png().toBuffer({resolveWithObject: true});
    fs.writeFileSync(path.join(OUT, id + '.png'), b.data);
    dims[id] = [b.info.width, b.info.height];
  }
  for (const id of ['ody', 'cy']) { const m = await sharp(path.join(OUT, id + '.png')).metadata(); dims[id] = [m.width, m.height]; }
  fs.writeFileSync(path.join(__dirname, 'src/data/dims.json'), JSON.stringify(dims));
  console.log('props', JSON.stringify(dims));

  // NB14: left 52% crop (799x864) centred on a 2304x1296 canvas, side bars built from the crop's own edge colours (smooth vertical gradient, darkened, no blur detail)
  const cm = await sharp(path.join(IMG, 'NB14_crop_left55.png')).metadata();
  const ch = H2, cw = Math.round(cm.width * H2 / cm.height);
  const cropBuf = await sharp(path.join(IMG, 'NB14_crop_left55.png')).resize(cw, ch, {kernel: 'lanczos3'}).sharpen({sigma: 0.6}).removeAlpha().png().toBuffer();
  const x0 = Math.round((W2 - cw) / 2), barW = x0;
  const edge = async (left) => {
    const raw = await sharp(cropBuf).extract({left: left ? 0 : cw - 8, top: 0, width: 8, height: ch}).resize(1, ch, {kernel: 'cubic'}).raw().toBuffer();
    const out = Buffer.alloc(raw.length); const R = 110;
    for (let y = 0; y < ch; y++) { for (let c = 0; c < 3; c++) { let s = 0, n = 0; for (let k = -R; k <= R; k++) { const yy = Math.min(ch - 1, Math.max(0, y + k)); s += raw[yy * 3 + c]; n++; } out[y * 3 + c] = s / n; } }
    const bar = Buffer.alloc(barW * ch * 3);
    for (let y = 0; y < ch; y++) for (let x = 0; x < barW; x++) {
      const u = left ? x / barW : 1 - x / barW; // 0 outer .. 1 seam
      const k = 0.42 + 0.40 * Math.pow(u, 1.4);
      for (let c = 0; c < 3; c++) bar[(y * barW + x) * 3 + c] = Math.round(out[y * 3 + c] * k);
    }
    return sharp(bar, {raw: {width: barW, height: ch, channels: 3}}).png().toBuffer();
  };
  const lb = await edge(true), rb = await edge(false);
  const F = 36;
  const alpha = Buffer.alloc(cw * ch); for (let y = 0; y < ch; y++) for (let x = 0; x < cw; x++) alpha[y * cw + x] = Math.round(255 * Math.min(1, x / F, (cw - 1 - x) / F));
  const cropA = await sharp(cropBuf).joinChannel(alpha, {raw: {width: cw, height: ch, channels: 1}}).png().toBuffer();
  await sharp({create: {width: W2, height: H2, channels: 3, background: '#111'}}).composite([{input: lb, left: 0, top: 0}, {input: rb, left: x0 + cw, top: 0}, {input: cropA, left: x0, top: 0}])
    .jpeg({quality: 92}).toFile(path.join(OUT, 'NB14.jpg'));
  console.log('NB14 composed', cw, x0);

  // grain tile
  const N = 256, g = Buffer.alloc(N * N * 4); let s = 987654321;
  const rnd = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  for (let i = 0; i < N * N; i++) { const v = Math.round(128 + (rnd() + rnd() + rnd() - 1.5) * 90); g[i * 4] = g[i * 4 + 1] = g[i * 4 + 2] = v; g[i * 4 + 3] = 255; }
  await sharp(g, {raw: {width: N, height: N, channels: 4}}).png().toFile(path.join(OUT, 'grain.png'));

  // ---- maps: Sutherland-Hodgman clip of Natural Earth land polygons to a bbox ----
  const clip = (ring, b) => {
    const edges = [(p) => p[0] >= b[0], (p) => p[0] <= b[2], (p) => p[1] >= b[1], (p) => p[1] <= b[3]];
    const inter = [(a, c) => { const t = (b[0] - a[0]) / (c[0] - a[0]); return [b[0], a[1] + t * (c[1] - a[1])]; }, (a, c) => { const t = (b[2] - a[0]) / (c[0] - a[0]); return [b[2], a[1] + t * (c[1] - a[1])]; },
      (a, c) => { const t = (b[1] - a[1]) / (c[1] - a[1]); return [a[0] + t * (c[0] - a[0]), b[1]]; }, (a, c) => { const t = (b[3] - a[1]) / (c[1] - a[1]); return [a[0] + t * (c[0] - a[0]), b[3]]; }];
    let out = ring;
    for (let e = 0; e < 4; e++) {
      const inp = out; out = []; if (!inp.length) break;
      for (let i = 0; i < inp.length; i++) {
        const cur = inp[i], prev = inp[(i + inp.length - 1) % inp.length], ci = edges[e](cur), pi = edges[e](prev);
        if (ci) { if (!pi) out.push(inter[e](prev, cur)); out.push(cur); } else if (pi) out.push(inter[e](prev, cur));
      }
    }
    return out;
  };
  const rings = (gj) => { const r = []; for (const f of gj.features) { const g = f.geometry; const polys = g.type === 'Polygon' ? [g.coordinates] : g.coordinates; for (const p of polys) r.push({ring: p[0]}); } return r; };
  const round = (r) => r.map((p) => [Math.round(p[0] * 1000) / 1000, Math.round(p[1] * 1000) / 1000]);
  const med = JSON.parse(fs.readFileSync('/tmp/ne_dl/land50.geojson')); const bb = [-12, 25, 42, 49];
  const medOut = [];
  for (const {ring} of rings(med)) { const c = clip(ring, bb); if (c.length > 3) medOut.push(round(c)); }
  const wor = JSON.parse(fs.readFileSync('/tmp/ne_dl/land110.geojson')); const worOut = [];
  for (const {ring} of rings(wor)) worOut.push(round(ring));
  fs.writeFileSync(path.join(__dirname, 'src/data/med.json'), JSON.stringify(medOut));
  fs.writeFileSync(path.join(__dirname, 'src/data/world.json'), JSON.stringify(worOut));
  console.log('maps', medOut.length, worOut.length, fs.statSync(path.join(__dirname, 'src/data/med.json')).size);
})();
