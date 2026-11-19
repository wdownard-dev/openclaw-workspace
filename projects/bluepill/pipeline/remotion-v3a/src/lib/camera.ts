import {easeInOut} from './theme';

// Calm camera: one zoom (6-8 % max) with ease-in-out, an optional slow pan at constant zoom, and an optional single
// damped kick (2-3 Hz, 6-10 px, no rotation) applied identically to every layer.
export type Cam = {s: number; x: number; y: number; ox: number; oy: number; sx: number; sy: number; sr: number};
export type CamFn = (t: number, dur: number) => Cam;
export type ShakeKey = {at: number; px?: number; hz?: number; dur?: number};

const W = 1920;
const kickAt = (t: number, keys: ShakeKey[] = []) => {
  let sx = 0;
  for (const k of keys) {
    const u = t - k.at, d = k.dur ?? 0.3, a = (k.px ?? 8) / W;
    if (u < 0 || u > d) continue;
    sx += a * Math.exp(-u * 10) * Math.sin(2 * Math.PI * (k.hz ?? 2.5) * u);
  }
  return {sx, sy: 0, sr: 0};
};

type Opts = {from?: number; to?: number; fx?: number; fy?: number; x0?: number; x1?: number; y0?: number; y1?: number; shake?: ShakeKey[]};
const make = (o: Opts): CamFn => (t, dur) => {
  const u = dur > 0 ? Math.min(1, t / dur) : 1;
  const e = easeInOut(u);
  const L = (a: number, b: number) => a + (b - a) * e;
  return {s: L(o.from ?? 1, o.to ?? 1), x: L(o.x0 ?? 0, o.x1 ?? 0), y: L(o.y0 ?? 0, o.y1 ?? 0), ox: o.fx ?? 0.5, oy: o.fy ?? 0.5, ...kickAt(t, o.shake)};
};

export const cam = {
  pushIn: (to = 1.07, fx = 0.5, fy = 0.5, shake?: ShakeKey[], from = 1.02): CamFn => make({from, to, fx, fy, shake}),
  pullOut: (from = 1.08, fx = 0.5, fy = 0.5, shake?: ShakeKey[]): CamFn => make({from, to: 1.02, fx, fy, shake}),
  pan: (dir = 1, amt = 0.02, s = 1.05, fy = 0.5): CamFn => make({from: s, to: s, x0: -dir * amt, x1: dir * amt, fy}),
  hold: (shake: ShakeKey[] = [], s = 1.04, fx = 0.5, fy = 0.5): CamFn => make({from: s, to: s * 1.02, fx, fy, shake}),
};
