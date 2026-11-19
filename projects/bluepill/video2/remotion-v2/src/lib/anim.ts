// Shared easing / stop-motion helpers (FORMAT-BIBLE section 4).
export const clamp = (v: number) => Math.max(0, Math.min(1, v));
/** pop: scale 0 -> ~1.06 -> 1 over 0.2 s, easeOutBack (overshoot constant 1.3 peaks at 1.06) */
export const popScale = (dt: number, dur = 0.2) => {
  if (dt < 0) return 0;
  const u = clamp(dt / dur), c = 1.3;
  return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2);
};
/** stamp: slams down from 1.35 to 1 over 0.2 s (ease out cubic) */
export const stampScale = (dt: number, dur = 0.2) => { if (dt < 0) return 0; const u = clamp(dt / dur); return 1 + 0.35 * Math.pow(1 - u, 3); };
/** 15 updates per second stop-motion quantisation for counters and routes */
export const step15 = (dt: number) => Math.floor(dt * 15) / 15;
export const routeProgress = (dt: number, dur: number) => clamp(step15(dt) / dur);
export const counterValue = (dt: number, dur: number | undefined, a: number, b: number) => (dt < 0 ? null : !dur || a === b ? b : Math.round(a + (b - a) * clamp(step15(dt) / dur)));
/** entrance slide: 160 px over 0.15 s, ease out (used only when an event asks for enter:'slide') */
export const slideIn = (dt: number, px = 160, dur = 0.15) => { if (dt < 0) return px; const u = clamp(dt / dur); return px * Math.pow(1 - u, 2); };
/** exit slide (swap src 'slide_out_left'): 200 px over 0.15 s, then gone */
export const slideOut = (dt: number, px = 200, dur = 0.15) => { const u = clamp(dt / dur); return -px * (1 - Math.pow(1 - u, 2)); };
/** deterministic small tilt for impact words, -3..3 deg from the text */
export const tiltOf = (s: string) => { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; const r = ((h >>> 0) % 7) - 3; return r === 0 ? -2 : r; };
