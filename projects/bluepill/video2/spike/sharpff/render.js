// UF-style state renderer: composite only frames whose visual state changed, pipe raw frames to ffmpeg.
// usage: node render.js timeline.json out.mp4
const sharp = require('../../../pipeline/node_modules/sharp');
const {spawn} = require('child_process');
const A = require('../common/anim.js');
const path = require('path');
const C = (f) => path.join(__dirname, '../common', f);
const FFMPEG = '/home/williamdownard/openclaw-sites/bin/ffmpeg';
const [,, tlPath, outPath] = process.argv;
const TL = require(path.resolve(tlPath));
const S = +(process.env.S || 1), W = 1920 * S, H = 1080 * S, FPS = TL.fps, N = Math.round(TL.duration * FPS);
const FONT = 'font-family="Fira Sans Condensed" font-weight="800"';
const cache = new Map();
const memo = async (k, f) => { if (!cache.has(k)) cache.set(k, await f()); return cache.get(k); };

const bgOf = (b) => memo('bg' + JSON.stringify(b), async () => {
  const s = b.type === 'map' ? sharp(C('map.png')).resize(W, H) : b.type === 'white' ? sharp({create: {width: W, height: H, channels: 3, background: '#ffffff'}}) : sharp(C(b.src)).resize(W, H, {fit: 'cover'});
  return s.removeAlpha().raw().toBuffer();
});
const textPng = (e, text) => memo('txt' + JSON.stringify([e.x, e.size, e.color, e.rot, e.stroke, text, S]), async () => {
  const sz = e.size * S, w = Math.ceil(text.length * sz * 0.62 + 80), h = Math.ceil(sz * 1.5), diag = Math.ceil(Math.hypot(w, h));
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${diag}" height="${diag}"><g transform="rotate(${e.rot || 0} ${diag / 2} ${diag / 2})"><text x="${diag / 2}" y="${diag / 2 + sz * 0.35}" text-anchor="middle" ${FONT} font-size="${sz}" fill="${e.color}" ${e.stroke ? `stroke="${e.stroke}" stroke-width="${sz * 0.09}" stroke-linejoin="round" paint-order="stroke"` : ''}>${text}</text></g></svg>`;
  return sharp(Buffer.from(svg)).png().trim().toBuffer({resolveWithObject: true}); // tight bbox
});
const spritePng = (e) => memo('spr' + e.src + e.h + S, async () => sharp(C(e.src)).resize({height: e.h * S}).png().toBuffer({resolveWithObject: true}));
const scaled = (key, src, s) => memo(key + Math.round(s * 100), async () => sharp(src.data).resize({width: Math.max(1, Math.round(src.info.width * s))}).png().toBuffer({resolveWithObject: true}));

const kbFrame = async (shot, t) => { const z = 1 + TL.kb * (t - shot.t0) / (shot.t1 - shot.t0), w = Math.round(W * z), h = Math.round(H * z);
  const src = await memo('src' + shot.bg.src, async () => sharp(C(shot.bg.src)).resize(W, H, {fit: 'cover'}).removeAlpha().raw().toBuffer());
  return sharp(src, {raw: {width: W, height: H, channels: 3}}).resize(w, h).extract({left: Math.floor((w - W) / 2), top: Math.floor((h - H) / 2), width: W, height: H}).raw().toBuffer(); };
async function layers(shot, t) {
  const out = []; let key = shot.id; const kb = TL.kb || 0; if (kb && shot.bg.type === 'img') key += '|kb' + Math.round(t * FPS);
  for (const e of TL.events.filter((e) => e.shot === shot.id && t >= e.t)) {
    const dt = t - e.t;
    if (e.kind === 'sprite' || e.kind === 'label') {
      const s = A.popScale(dt), k = dt < 0.2 ? s.toFixed(2) : '1'; key += `|${e.t}:${k}`;
      const base = e.kind === 'sprite' ? await spritePng(e) : await textPng(e, e.text);
      const img = k === '1' ? base : await scaled(e.src || e.text, base, s), {width: w, height: h} = img.info;
      const left = Math.round(e.x * S - w / 2), top = Math.round(e.kind === 'sprite' ? e.y * S - h : e.y * S - h / 2);
      out.push({input: img.data, left, top});
    } else if (e.kind === 'counter') {
      const v = A.counterValue(dt, e.dur, e.from, e.to); key += `|c${v}`;
      const img = await textPng(e, String(v)); out.push({input: img.data, left: Math.round(e.x * S - img.info.width / 2), top: Math.round(e.y * S - img.info.height / 2)});
    } else if (e.kind === 'route') {
      const p = A.routeProgress(dt, e.dur); key += `|r${p.toFixed(2)}`;
      out.push({input: await memo('route' + p.toFixed(2), async () => sharp(Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 1920 1080">${A.routeSvgInner(e, p)}${A.arrowHead(e, p)}</svg>`)).png().toBuffer()), left: 0, top: 0});
    }
  }
  return {key, out};
}

(async () => {
  const t0 = Date.now();
  const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-framerate', String(FPS), '-i', 'pipe:0', '-i', C(TL.audio || 'narr20.mp3'),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', outPath], {stdio: ['pipe', 'inherit', 'inherit']});
  ff.stdin.on('error', () => {}); let lastKey = null, lastBuf = null, unique = 0, tComp = 0, tLay = 0;
  for (let f = 0; f < N; f++) {
    const t = f / FPS, shot = TL.shots.find((s) => t >= s.t0 && t < s.t1) || TL.shots[TL.shots.length - 1];
    const a0 = Date.now(); const {key, out} = await layers(shot, t); tLay += Date.now() - a0;
    if (key !== lastKey) { const b0 = Date.now(); // new visual state: composite
      const base = TL.kb && shot.bg.type === 'img' ? await kbFrame(shot, t) : await bgOf(shot.bg);
      lastBuf = await sharp(base, {raw: {width: W, height: H, channels: 3}}).composite(out).removeAlpha().raw().toBuffer(); lastKey = key; unique++; if (lastBuf.length !== W * H * 3) throw new Error('bad frame size ' + lastBuf.length); tComp += Date.now() - b0;
    }
    if (!ff.stdin.write(lastBuf)) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r));
  console.log(`layers ${tLay} ms, composite ${tComp} ms`); console.log(`frames ${N}, unique composites ${unique}, wall ${((Date.now() - t0) / 1000).toFixed(1)} s`);
})();
