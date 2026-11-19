import React, {useMemo} from 'react';
import med from '../med.json';
import world from '../world.json';
import {C, W, H} from './theme';

type LL = [number, number];
type BBox = [number, number, number, number]; // lon0, lat0, lon1, lat1
const MED = med as unknown as number[][][];
const WORLD = world as unknown as number[][][];

/** bbox per code map (storyboard map ids). Equirectangular, fit inside 1920x1080, centred. */
export const MAP_BBOX: Record<string, {bbox: BBox; data: 'med' | 'world'}> = {
  map_med_west: {bbox: [4, 32.5, 26, 44.5], data: 'med'},
  map_med_loop: {bbox: [6, 33, 26, 44], data: 'med'},
  map_sicily: {bbox: [11, 35.4, 17.6, 39.2], data: 'med'},
  map_world: {bbox: [-180, -58, 180, 82], data: 'world'},
  map_argolid: {bbox: [22, 37.1, 23.6, 38.2], data: 'med'},
};
export const makeProj = (bbox: BBox, w = W, h = H) => {
  const [lo0, la0, lo1, la1] = bbox;
  const cosf = Math.cos((((la0 + la1) / 2) * Math.PI) / 180);
  // cover the frame (no empty margins): scale so the bbox at least fills both axes
  const sy = Math.max(h / (la1 - la0), w / ((lo1 - lo0) * cosf));
  const sx = sy * cosf;
  const ox = (w - (lo1 - lo0) * sx) / 2, oy = (h - (la1 - la0) * sy) / 2;
  return (ll: LL): [number, number] => [ox + (ll[0] - lo0) * sx, oy + (la1 - ll[1]) * sy];
};
export const projFor = (mapId: string) => { const m = MAP_BBOX[mapId] || MAP_BBOX.map_med_west; return makeProj(m.bbox); };

/** flat inked map: slate sea, olive-cream land, thin dark coastline; no names (ASSET-PLAN 1.4) */
export const CodeMap: React.FC<{mapId: string}> = ({mapId}) => {
  const m = MAP_BBOX[mapId] || MAP_BBOX.map_med_west;
  const P = useMemo(() => makeProj(m.bbox), [mapId]);
  const rings = m.data === 'world' ? WORLD : MED;
  const paths = useMemo(() => rings.map((r) => { let d = ''; r.forEach((p, i) => { const [x, y] = P(p as LL); d += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1); }); return d + 'Z'; }), [mapId]);
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', left: 0, top: 0}}>
      <rect width={W} height={H} fill={C.sea} />
      {paths.map((d, i) => <path key={i} d={d} fill={C.land} stroke={C.coast} strokeWidth={m.data === 'world' ? 1.5 : 3} strokeLinejoin="round" />)}
    </svg>
  );
};

/** route: quadratic from->via->to drawn in 15 fps steps; loop:true closes the curve back to the start. Ink on a cream under-stroke, arrow head at the end. */
export const Route: React.FC<{e: any; mapId: string; prog: number}> = ({e, mapId, prog}) => {
  const P = useMemo(() => projFor(mapId), [mapId]);
  if (prog <= 0) return null;
  const a = P(e.from), c = P(e.via), b = P(e.to);
  let d = `M${a[0]} ${a[1]} Q${c[0]} ${c[1]} ${b[0]} ${b[1]}`;
  if (e.loop) { const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2; const c2: [number, number] = [2 * mx - c[0], 2 * my - c[1]]; d += ` Q${c2[0]} ${c2[1]} ${a[0]} ${a[1]}`; }
  const end = e.loop ? a : b, ctl = e.loop ? [2 * (a[0] + b[0]) / 2 - c[0], 2 * (a[1] + b[1]) / 2 - c[1]] : c;
  const ang = (Math.atan2(end[1] - ctl[1], end[0] - ctl[0]) * 180) / Math.PI;
  return (
    <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
      <path d={d} pathLength={1} fill="none" stroke={C.cream} strokeWidth={22} strokeLinecap="round" strokeDasharray={`${prog} 1`} />
      <path d={d} pathLength={1} fill="none" stroke={C.ink} strokeWidth={12} strokeLinecap="round" strokeDasharray={`${prog} 1`} />
      {prog >= 0.97 && <polygon points="0,-28 56,0 0,28" fill={C.ink} stroke={C.cream} strokeWidth={5} transform={`translate(${end[0]} ${end[1]}) rotate(${ang})`} />}
    </svg>
  );
};
