// shared easing/state functions used by BOTH renderers (CommonJS so Remotion and Node import the same code)
const clamp = (v) => Math.max(0, Math.min(1, v));
const popScale = (dt, dur = 0.2) => { const u = clamp(dt / dur), c = 1.4; return dt < 0 ? 0 : 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); }; // easeOutBack
const step15 = (dt) => Math.floor(dt * 15) / 15; // stop-motion quantisation for route/counter
const routeProgress = (dt, dur) => clamp(step15(dt) / dur);
const counterValue = (dt, dur, a, b) => (dt < 0 ? null : Math.round(a + (b - a) * clamp(step15(dt) / dur)));
// map projection (equirectangular, Sicily-centred)
const MAP = {lon0: 4, lon1: 24, W: 1920, H: 1080, latC: 38};
const proj = (lon, lat) => { const kx = MAP.W / (MAP.lon1 - MAP.lon0), ky = kx / Math.cos(MAP.latC * Math.PI / 180); return [(lon - MAP.lon0) * kx, MAP.H / 2 - (lat - MAP.latC) * ky]; };
const routePath = (e) => { const a = proj(...e.from), c = proj(...e.via), b = proj(...e.to); return `M${a[0]} ${a[1]} Q${c[0]} ${c[1]} ${b[0]} ${b[1]}`; };
const mapSvg = (med) => {
  let p = '';
  for (const poly of med) p += 'M' + poly.map(([lo, la]) => proj(lo, la).map((v) => v.toFixed(1)).join(' ')).join('L') + 'Z';
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><rect width="1920" height="1080" fill="#cfe2e6"/><path d="${p}" fill="#efe2bf" stroke="#3a2f22" stroke-width="3" stroke-linejoin="round"/></svg>`;
};
const routeSvgInner = (e, prog) => prog <= 0 ? '' : `<path d="${routePath(e)}" pathLength="1" fill="none" stroke="#b8472a" stroke-width="14" stroke-linecap="round" stroke-dasharray="${prog} 1" /><path d="${routePath(e)}" pathLength="1" fill="none" stroke="#b8472a" stroke-width="0"/>`;
const arrowHead = (e, prog) => { // small triangle at path end once progress >= 0.97
  if (prog < 0.97) return ''; const b = proj(...e.to), c = proj(...e.via); const ang = Math.atan2(b[1] - c[1], b[0] - c[0]) * 180 / Math.PI;
  return `<polygon points="0,-30 60,0 0,30" fill="#b8472a" transform="translate(${b[0]} ${b[1]}) rotate(${ang})"/>`; };
module.exports = {clamp, popScale, step15, routeProgress, counterValue, MAP, proj, routePath, mapSvg, routeSvgInner, arrowHead};
