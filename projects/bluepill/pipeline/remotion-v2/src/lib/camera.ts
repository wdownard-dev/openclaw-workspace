import {easeInOut, easeOut} from './theme';

// Camera values: s = zoom, x/y = pan as a fraction of the frame (positive moves the picture right/down),
// ox/oy = zoom focus point (fraction of frame), shake offsets in fractions plus rotation in degrees.
export type Cam = {s: number; x: number; y: number; ox: number; oy: number; sx: number; sy: number; sr: number};
export type CamFn = (t: number, dur: number) => Cam;
export type ShakeKey = {at: number; amp?: number; dur?: number};

const shakeAt = (t: number, keys: ShakeKey[] = []) => {
  let sx = 0, sy = 0, sr = 0;
  for (const k of keys) {
    const u = t - k.at, d = k.dur ?? 0.5, a = k.amp ?? 0.012;
    if (u < 0 || u > d) continue;
    const env = Math.pow(1 - u / d, 2);
    sx += Math.sin(u * 71) * a * env;
    sy += Math.cos(u * 97) * a * 0.8 * env;
    sr += Math.sin(u * 53) * a * 90 * env; // degrees
  }
  return {sx, sy, sr};
};

type Opts = {from?: number; to?: number; fx?: number; fy?: number; x0?: number; x1?: number; y0?: number; y1?: number; shake?: ShakeKey[]; inOut?: boolean};
const make = (o: Opts): CamFn => (t, dur) => {
  const u = dur > 0 ? Math.min(1, t / dur) : 1;
  const e = o.inOut ? easeInOut(u) : (1 - Math.pow(1 - u, 1.6));
  const L = (a: number, b: number) => a + (b - a) * e;
  return {s: L(o.from ?? 1, o.to ?? 1), x: L(o.x0 ?? 0, o.x1 ?? 0), y: L(o.y0 ?? 0, o.y1 ?? 0), ox: o.fx ?? 0.5, oy: o.fy ?? 0.5, ...shakeAt(t, o.shake)};
};

export const cam = {
  /** slow zoom toward a focus point */
  pushIn: (to = 1.16, fx = 0.5, fy = 0.5, shake?: ShakeKey[], from = 1.02): CamFn => make({from, to, fx, fy, shake}),
  /** start tight, pull back to reveal */
  pullOut: (from = 1.2, fx = 0.5, fy = 0.5, shake?: ShakeKey[]): CamFn => make({from, to: 1.02, fx, fy, shake}),
  /** horizontal drift at constant zoom; dir +1 moves picture right (camera pans left) */
  pan: (dir = 1, amt = 0.05, s = 1.1, fy = 0.5): CamFn => make({from: s, to: s, x0: -dir * amt, x1: dir * amt, fy, inOut: true}),
  /** locked frame with impact shakes */
  hold: (shake: ShakeKey[] = [], s = 1.06, fx = 0.5, fy = 0.5): CamFn => make({from: s, to: s * 1.015, fx, fy, shake}),
  /** vertical tilt up/down */
  tilt: (dir = 1, amt = 0.04, s = 1.12): CamFn => make({from: s, to: s, y0: -dir * amt, y1: dir * amt, inOut: true}),
};
