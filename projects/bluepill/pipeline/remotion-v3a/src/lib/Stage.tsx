import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame, useVideoConfig} from 'remotion';
import {BG, IMG, dim} from './assets';

/**
 * Stage: a shared compositing pass that makes flat cutouts sit in a flat/inked background.
 * One colour grade per scene, one key light (fire or sun) shared by every layer:
 *  - directional shade (multiply) + warm glow (screen), clipped to each cutout's silhouette
 *  - rim light on the key-light side (a thin ring from CSS mask-composite, pulled back inside the silhouette by its own width)
 *  - cast shadow (silhouette sheared along the ground away from the light) + contact shadow
 *  - background: slight blur, atmospheric haze, light pool on the ground
 *  - scene grade, film grain, vignette
 * Usage: <Stage {...PRESETS.fire} /> (see stagePresets.ts). Cutout x,y = feet centre / ground line, h = height, all as frame fractions.
 */
export type StageFig = {id: string; src: string; x: number; y: number; h: number; blur?: number; haze?: number; shadow?: number; rim?: number; z?: number};
export type StageProps = {
  bg: string; bgPos?: string; bgBlur?: number; bgGrade?: string;
  light: {x: number; y: number; color: string; glow: number; rim: number; uplight?: number; pool?: {r: number; a: number}};
  shade: string;               // multiply colour on the side of a cutout facing away from the light
  lit?: string;                // multiply colour on the lit side (default white)
  shadowDir: {sx: number; sy: number; alpha: number; blur?: number};  // cast shadow shear (px per px of height) and foreshortening
  haze: {color: string; alpha: number; horizon: number};             // veil, strongest at the horizon line (frame fraction)
  grade: {color: string; alpha: number};                              // soft-light colour grade over everything
  grain?: number; vignette?: number; figs: StageFig[];
};

const maskStyle = (url: string): React.CSSProperties => ({WebkitMaskImage: `url(${url})`, WebkitMaskSize: '100% 100%', maskImage: `url(${url})`, maskSize: '100% 100%'} as any);

const Fig: React.FC<{f: StageFig; P: StageProps; W: number; H: number}> = ({f, P, W, H}) => {
  const d = dim(f.src), url = IMG(f.src);
  const hpx = f.h * H, wpx = hpx * d.w / d.h;
  const cx = f.x * W, gy = f.y * H, mid = gy - hpx * 0.55;
  const lx = P.light.x * W - cx, ly = P.light.y * H - mid, len = Math.hypot(lx, ly) || 1;
  const ux = lx / len, uy = ly / len;
  const theta = (Math.atan2(ux, -uy) * 180) / Math.PI;            // css gradient angle pointing toward the light
  const rimPx = Math.max(3.5, hpx * 0.009) * (f.rim ?? 1);
  const sh = f.shadow ?? 1;
  const {sx, sy, alpha, blur} = P.shadowDir;
  const lit = P.lit ?? '#ffffff';
  return <>
    {/* cast shadow on the ground */}
    <div style={{position: 'absolute', left: cx - wpx / 2, top: gy - hpx, width: wpx, height: hpx, transformOrigin: '50% 100%', opacity: alpha * sh,
      transform: `matrix(1,0,${-sx},${-sy},0,0)`, filter: `brightness(0) blur(${blur ?? 6}px)`, WebkitMaskImage: 'linear-gradient(to top, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%)', maskImage: 'linear-gradient(to top, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%)'} as any}>
      <Img src={url} style={{width: '100%', height: '100%', display: 'block'}} />
    </div>
    {/* contact shadow */}
    <div style={{position: 'absolute', left: cx - wpx * 0.45, top: gy - wpx * 0.045, width: wpx * 0.9, height: wpx * 0.09, borderRadius: '50%', opacity: 0.8 * sh,
      background: 'radial-gradient(ellipse at center, rgba(14,8,10,0.85) 0%, rgba(14,8,10,0.45) 50%, rgba(14,8,10,0) 75%)', filter: 'blur(2px)'}} />
    <div style={{position: 'absolute', left: cx - wpx / 2, top: gy - hpx, width: wpx, height: hpx, isolation: 'isolate', filter: f.blur ? `blur(${f.blur}px)` : undefined}}>
      <Img src={url} style={{width: '100%', height: '100%', display: 'block'}} />
      {/* directional shade: away-from-light side takes the shadow colour */}
      <div style={{position: 'absolute', inset: 0, mixBlendMode: 'multiply', background: `linear-gradient(${theta}deg, ${P.shade} 0%, ${P.shade} 8%, ${lit} 100%)`, ...maskStyle(url)}} />
      {/* warm glow toward the light, and uplight from the floor fire */}
      <div style={{position: 'absolute', inset: 0, mixBlendMode: 'screen', background: `linear-gradient(${theta}deg, rgba(0,0,0,0) 35%, ${P.light.color} 130%)`, opacity: P.light.glow, ...maskStyle(url)}} />
      {P.light.uplight ? <div style={{position: 'absolute', inset: 0, mixBlendMode: 'screen', background: `linear-gradient(to top, ${P.light.color} 0%, rgba(0,0,0,0) 60%)`, opacity: P.light.uplight, ...maskStyle(url)}} /> : null}
      {/* rim light */}
      <div style={{position: 'absolute', inset: 0, mixBlendMode: 'screen', opacity: P.light.rim * (f.rim ?? 1) * 0.85, background: P.light.color, filter: `blur(${rimPx * 0.45}px)`, transform: `translate(${-ux * rimPx}px,${-uy * rimPx}px)`,
        WebkitMaskImage: `url(${url}), url(${url})`, WebkitMaskSize: '100% 100%, 100% 100%', WebkitMaskRepeat: 'no-repeat, no-repeat', WebkitMaskPosition: `0px 0px, ${-ux * rimPx}px ${-uy * rimPx}px`, WebkitMaskComposite: 'source-out',
        maskImage: `url(${url}), url(${url})`, maskSize: '100% 100%, 100% 100%', maskRepeat: 'no-repeat, no-repeat', maskPosition: `0px 0px, ${-ux * rimPx}px ${-uy * rimPx}px`, maskComposite: 'subtract'} as any} />
      {/* depth haze on this figure */}
      {f.haze ? <div style={{position: 'absolute', inset: 0, background: P.haze.color, opacity: f.haze, ...maskStyle(url)}} /> : null}
    </div>
  </>;
};

export const Stage: React.FC<StageProps> = (P) => {
  const frame = useCurrentFrame();
  const {width: W, height: H} = useVideoConfig();
  const figs = [...P.figs].sort((a, b) => (a.z ?? a.y) - (b.z ?? b.y));
  const grain = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='${W}' height='${H}'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='${frame % 7}' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`;
  return (
    <AbsoluteFill style={{background: '#0d0a10', overflow: 'hidden'}}>
      <AbsoluteFill style={{overflow: 'hidden'}}>
        <Img src={BG(P.bg)} style={{position: 'absolute', inset: '-2%', width: '104%', height: '104%', objectFit: 'cover', objectPosition: P.bgPos ?? '50% 50%', filter: `blur(${P.bgBlur ?? 2}px)`}} />
        {P.bgGrade && <AbsoluteFill style={{background: P.bgGrade, mixBlendMode: 'multiply'}} />}
        {P.light.pool && <AbsoluteFill style={{mixBlendMode: 'screen', opacity: P.light.pool.a, background: `radial-gradient(ellipse ${P.light.pool.r * W}px ${P.light.pool.r * W * 0.45}px at ${P.light.x * W}px ${(P.light.y + 0.04) * H}px, ${P.light.color} 0%, rgba(0,0,0,0) 100%)`}} />}
        {/* atmospheric haze on the background only, strongest around the horizon */}
        <AbsoluteFill style={{opacity: P.haze.alpha, background: `linear-gradient(to bottom, rgba(0,0,0,0) 0%, ${P.haze.color} ${P.haze.horizon * 100 - 8}%, ${P.haze.color} ${P.haze.horizon * 100 + 4}%, rgba(0,0,0,0) ${P.haze.horizon * 100 + 30}%)`}} />
      </AbsoluteFill>
      {figs.map((f) => <Fig key={f.id} f={f} P={P} W={W} H={H} />)}
      {/* shared scene grade */}
      <AbsoluteFill style={{background: P.grade.color, opacity: P.grade.alpha, mixBlendMode: 'soft-light'}} />
      <AbsoluteFill style={{background: `radial-gradient(ellipse at center, rgba(0,0,0,0) 52%, rgba(0,0,0,${P.vignette ?? 0.4}) 100%)`}} />
      <AbsoluteFill style={{backgroundImage: grain, mixBlendMode: 'overlay', opacity: P.grain ?? 0.22}} />
    </AbsoluteFill>
  );
};
