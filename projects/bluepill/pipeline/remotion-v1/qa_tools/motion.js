// usage: node motion.js gray.raw W H out.json
const fs = require('fs');
const [,, file, Ws, Hs, out] = process.argv;
const W = +Ws, H = +Hs, N = W * H;
const buf = fs.readFileSync(file);
const nF = Math.floor(buf.length / N);
const R = +(process.env.R||5);
function shift(a, b, x0, y0, x1, y1) {
  // find (dx,dy) such that b(x,y) ~ a(x-dx,y-dy); returns sub-pixel via parabola
  const S = {};
  let best = 1e18, bx = 0, by = 0;
  for (let dy = -R; dy <= R; dy++) for (let dx = -R; dx <= R; dx++) {
    let s = 0, c = 0;
    for (let y = y0; y < y1; y += 2) {
      const ro = y * W, rp = (y - dy) * W;
      for (let x = x0; x < x1; x += 2) { s += Math.abs(buf[b + ro + x] - buf[a + rp + x - dx]); c++; }
    }
    s /= c; S[dx + ',' + dy] = s;
    if (s < best) { best = s; bx = dx; by = dy; }
  }
  const g = (x, y) => S[x + ',' + y];
  let fx = 0, fy = 0;
  if (Math.abs(bx) < R) { const l = g(bx - 1, by), m = g(bx, by), r = g(bx + 1, by); const d = l - 2 * m + r; if (d > 0) fx = 0.5 * (l - r) / d; }
  if (Math.abs(by) < R) { const l = g(bx, by - 1), m = g(bx, by), r = g(bx, by + 1); const d = l - 2 * m + r; if (d > 0) fy = 0.5 * (l - r) / d; }
  return [bx + fx, by + fy, best];
}
const res = [];
const m = R + 2;
for (let f = 1; f < nF; f++) {
  const a = (f - 1) * N, b = f * N;
  let d = 0; for (let i = 0; i < N; i += 3) d += Math.abs(buf[a + i] - buf[b + i]); d /= N / 3;
  // full-frame (centre) shift, top band (bg), bottom band (chars)
  const all = shift(a, b, m, m, W - m, H - m);
  const top = shift(a, b, m, m, W - m, Math.floor(H * 0.4));
  const bot = shift(a, b, m, Math.floor(H * 0.55), W - m, H - m);
  res.push({f, t: +(f / 30).toFixed(3), diff: +d.toFixed(3), dx: +all[0].toFixed(2), dy: +all[1].toFixed(2), sad: +all[2].toFixed(2), tdx: +top[0].toFixed(2), tdy: +top[1].toFixed(2), bdx: +bot[0].toFixed(2), bdy: +bot[1].toFixed(2)});
}
fs.writeFileSync(out, JSON.stringify(res));
console.log('frames', nF, 'pairs', res.length);
