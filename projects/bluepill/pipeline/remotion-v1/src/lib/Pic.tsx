import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {easeInOut, clamp01} from './theme';
import {Grain} from './ui';

const W = 1920, H = 1080;
export type Family = 'fire' | 'night' | 'grey' | 'day' | 'dawn';
const FAMILY: Record<Family, {filter: string; tint: string}> = {
  fire: {filter: 'saturate(0.94) contrast(1.05) brightness(0.99)', tint: 'rgba(36,18,8,0.07)'},
  night: {filter: 'saturate(0.95) contrast(1.06)', tint: 'rgba(8,14,28,0.07)'},
  grey: {filter: 'saturate(0.93) contrast(1.04)', tint: 'rgba(10,10,12,0.05)'},
  day: {filter: 'saturate(0.94) contrast(1.03) brightness(0.98)', tint: 'rgba(30,22,10,0.05)'},
  dawn: {filter: 'brightness(1.55) contrast(0.86) saturate(0.55)', tint: 'rgba(120,96,70,0.10)'},
};
export const FAMILY_OF: Record<string, Family> = {
  NB01: 'fire', NB02: 'fire', NB03: 'grey', NB04: 'night', NB05: 'fire', NB06: 'grey', NB07: 'fire', NB08: 'fire', NB09: 'fire', NB10: 'night', NB11: 'fire',
  NB12: 'night', NB13: 'grey', NB14: 'grey', NB15: 'grey', NB16: 'grey', NB17: 'grey', NB18: 'grey', NB19: 'fire', NB20: 'grey', NB21: 'day', NB22: 'fire',
  NB23: 'fire', NB24: 'night', NB25: 'day', NBG01: 'grey', NBG02: 'fire', NBG03: 'night', NBG04: 'day', NBG05: 'night', NBG06: 'night', NBG07: 'day', NBG08: 'day',
  NBG09: 'grey', RS07: 'fire', RS08: 'night', RS09: 'grey', RS10: 'grey', RC02: 'night', RC11: 'night',
};

export type CamSpec = {s: [number, number]; c: [number, number, number, number]; kick?: number[]};
/** push-in: zoom s0->s1 about window centre c */
export const inn = (c: [number, number] = [0.5, 0.5], s0 = 1, s1 = 1.04): CamSpec => ({s: [s0, s1], c: [c[0], c[1], c[0], c[1]]});
export const out = (c: [number, number] = [0.5, 0.5], s0 = 1.04, s1 = 1): CamSpec => ({s: [s0, s1], c: [c[0], c[1], c[0], c[1]]});
/** slow pan at constant zoom; dir +1 = window moves right */
export const pan = (dir: 1 | -1 = 1, s = 1.05, cy = 0.5): CamSpec => { const k = 0.5 - 0.5 / s; return {s: [s, s], c: [0.5 - dir * 0.92 * k, cy, 0.5 + dir * 0.92 * k, cy]}; };
/** near-still hold with a barely perceptible creep */
export const hold = (c: [number, number] = [0.5, 0.5], s = 1.0, d = 0.012): CamSpec => ({s: [s, s + d], c: [c[0], c[1], c[0], c[1]]});
/** crop with slow drift (zoom fixed or slightly easing) */
export const crop = (c0: [number, number], c1: [number, number], s0: number, s1: number = s0): CamSpec => ({s: [s0, s1], c: [c0[0], c0[1], c1[0], c1[1]]});

export type CutoutProps = {src: string; x: number; y: number; h: number; aspect: number; flip?: boolean; dark?: boolean; shadow?: boolean; opacity?: number; filter?: string};
export const Cutout: React.FC<CutoutProps> = ({src, x, y, h, aspect, flip, dark, shadow = true, opacity = 1, filter}) => {
  const hp = h * H, wp = hp * aspect;
  return (
    <>
      {shadow && <div style={{position: 'absolute', left: x * W - wp * 0.5, top: y * H - hp * 0.035, width: wp, height: hp * 0.07, borderRadius: '50%', background: 'radial-gradient(ellipse at center, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 70%)', opacity}} />}
      <Img src={staticFile(src)} style={{position: 'absolute', left: x * W - wp / 2, top: y * H - hp, width: wp, height: hp, opacity, transform: flip ? 'scaleX(-1)' : undefined, filter: dark ? 'brightness(0.1) contrast(1.2)' : (filter ?? 'saturate(0.9) brightness(0.93) contrast(1.03)')}} />
    </>
  );
};

export const Pic: React.FC<{img: string; dur: number; cam: CamSpec; family?: Family; scrim?: 'bottom' | 'top' | 'none'; children?: React.ReactNode; overlay?: React.ReactNode; vignette?: number; frameFilter?: string}> = ({img, dur, cam, family, scrim = 'bottom', children, overlay, vignette = 0.36, frameFilter}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const u = clamp01(dur > 0 ? t / dur : 1);
  const e = easeInOut(u);
  const s = cam.s[0] + (cam.s[1] - cam.s[0]) * e;
  const cx = cam.c[0] + (cam.c[2] - cam.c[0]) * e, cy = cam.c[1] + (cam.c[3] - cam.c[1]) * e;
  const left = Math.max(0, Math.min(1 - 1 / s, cx - 0.5 / s)), top = Math.max(0, Math.min(1 - 1 / s, cy - 0.5 / s));
  let kx = 0;
  for (const k of cam.kick ?? []) { const d = t - k; if (d >= 0 && d < 0.25) kx += 8 * Math.exp(-d * 10) * Math.sin(2 * Math.PI * 2.5 * d); }
  const fam = FAMILY[family ?? FAMILY_OF[img] ?? 'grey'];
  return (
    <AbsoluteFill style={{background: '#0c0a08', overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: W, height: H, transformOrigin: '0 0', transform: `translate3d(${(-left * W * s + kx).toFixed(3)}px, ${(-top * H * s).toFixed(3)}px, 0) scale(${s.toFixed(5)})`, filter: frameFilter ?? fam.filter}}>
        <Img src={staticFile(`img/${img}.jpg`)} style={{position: 'absolute', left: 0, top: 0, width: W, height: H}} />
        {children}
      </div>
      <AbsoluteFill style={{background: fam.tint}} />
      <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 52%, rgba(0,0,0,${vignette}) 100%)`}} />
      {scrim === 'bottom' && <AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(0,0,0,0) 78%, rgba(0,0,0,0.42) 100%)'}} />}
      {scrim === 'top' && <AbsoluteFill style={{background: 'linear-gradient(to top, rgba(0,0,0,0) 78%, rgba(0,0,0,0.42) 100%)'}} />}
      <Grain alpha={0.045} />
      {overlay}
    </AbsoluteFill>
  );
};
