import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {BG, IMG, SFX, dim} from './assets';
import {CamFn, cam as camPresets} from './camera';
import {FONT_IMPACT, INK, GOLD, clamp01, easeOut, hash} from './theme';

// ---------- types ----------
export type Cue = {at: number; sfx: string; vol?: number};
export type Reaction = {at: number; kind: 'hop' | 'shake' | 'wobble' | 'recoil' | 'squash'; dur?: number};
export type MarkSpec = {at: number; kind: '!' | '?' | 'zzz' | 'sweat' | 'shh' | 'x' | 'sparks'; fx?: number; fy?: number; size?: number; dur?: number; color?: string};
export type Enter = 'none' | 'left' | 'right' | 'drop' | 'pop' | 'rise' | 'fade';

export type CutoutSpec = {
  id: string;
  src: string;            // name in public/img (without .png)
  x: number;              // feet centre, fraction of frame width
  y: number;              // ground line, fraction of frame height
  h: number;              // height, fraction of frame height
  depth?: 'bg' | 'char' | 'fg';
  at?: number;            // entrance time (s into shot)
  enter?: Enter;
  enterDist?: number;     // fraction of frame width/height travelled by the entrance
  exitAt?: number;        // slide-out time (direction = enter direction)
  moveTo?: {x?: number; y?: number; at: number; dur: number}; // simple travel after entrance
  flip?: boolean;
  bob?: number;           // idle bob amplitude px (default 6; 0 disables)
  bobSpeed?: number;
  tint?: string;          // multiply colour overriding the scene char tint
  noShadow?: boolean;
  shadowW?: number;       // shadow width as fraction of frame height (overrides default)
  rot?: number;           // static rotation, degrees
  rotateTo?: {at: number; deg: number; dur?: number; pivot?: string; lift?: number};
  spin?: number;          // total degrees rolled during the entrance (rolling props)
  react?: Reaction[];
  marks?: MarkSpec[];
  sfx?: string;           // sound on entrance (cue auto-added)
  opacity?: number;
  hidden?: boolean;
  noWalkHop?: boolean;    // disable the hop while moveTo travels (ships)
  walk?: boolean;         // hop-bob while travelling in (default true for left/right)
  z?: number;
};
export type ImpactSpec = {text: string; at: number; x: number; y: number; size?: number; rot?: number; color?: string; dur?: number; sfx?: string; shake?: number};
export type SceneProps = {
  bg: string;
  bgPos?: string;           // CSS object-position, picks which band of the painting is visible
  bgFlip?: boolean;
  bgOverscan?: number;      // bleed so pans never reveal edges (default 1.14)
  flatParallax?: boolean;   // true for maps: overlay must stay registered with the picture
  cam?: CamFn;
  grade?: string;           // multiply colour on the background (mood)
  tint?: string;            // multiply colour on cutouts (so they sit in the light)
  cutouts?: CutoutSpec[];
  impacts?: ImpactSpec[];
  cues?: Cue[];
  dimKeys?: [number, number][];   // [time, alpha] black overlay keyframes
  flash?: number[];               // times of white flashes (lightning)
  blur?: number;                  // bg blur px
  vignette?: number;
  extras?: (c: {t: number; f: number; fps: number; W: number; H: number}) => React.ReactNode;     // screen-space overlays (labels, counters)
  world?: (c: {t: number; f: number; fps: number; W: number; H: number}) => React.ReactNode;      // overlays that move with the camera (map routes)
  dur: number;
};

// ---------- helpers ----------
const mixToWhite = (hex: string, k: number) => {
  const n = parseInt(hex.slice(1), 16), r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
  const m = (c: number) => Math.round(255 + (c - 255) * k);
  return `rgb(${m(r)},${m(g)},${m(b)})`;
};

export const Sfx: React.FC<{cues: Cue[]}> = ({cues}) => {
  const {fps} = useVideoConfig();
  return <>{cues.map((c, i) => (
    <Sequence key={i} from={Math.max(0, Math.round(c.at * fps))} durationInFrames={Math.ceil(5 * fps)} layout="none">
      <Audio src={SFX(c.sfx)} volume={c.vol ?? 0.7} />
    </Sequence>))}</>;
};

// ---------- marks ----------
export const Mark: React.FC<{m: MarkSpec; t: number; boxW: number; boxH: number}> = ({m, t, boxW, boxH}) => {
  const {fps} = useVideoConfig();
  const u = t - m.at; const dur = m.dur ?? 1.5;
  if (u < 0 || u > dur) return null;
  const p = spring({frame: u * fps, fps, config: {damping: 8, stiffness: 220, mass: 0.5}});
  const out = clamp01((dur - u) / 0.2);
  const size = (m.size ?? 0.16) * boxH;
  const left = (m.fx ?? 0.5) * boxW, top = (m.fy ?? 0) * boxH;
  const base: React.CSSProperties = {position: 'absolute', left, top, transform: `translate(-50%,-50%) scale(${p * out})`, fontFamily: FONT_IMPACT, fontSize: size, lineHeight: 1, color: m.color ?? '#ff4b3e', WebkitTextStroke: `${size * 0.14}px ${INK}`, paintOrder: 'stroke fill', pointerEvents: 'none'} as any;
  if (m.kind === '!' || m.kind === '?') return <div style={base}>{m.kind}</div>;
  if (m.kind === 'shh') return <div style={{...base, color: '#fff', fontSize: size * 0.8}}>SHH</div>;
  if (m.kind === 'zzz') {
    return <>{[0, 1, 2].map((i) => {
      const v = ((u * 0.7 + i / 3) % 1);
      return <div key={i} style={{...base, color: '#cfe3ff', fontSize: size * (0.55 + 0.25 * v), left: left + v * size * 1.6 + i * size * 0.15, top: top - v * size * 2.2, opacity: Math.sin(Math.PI * v) * out, transform: `translate(-50%,-50%) rotate(${-10 + v * 20}deg)`}}>Z</div>;
    })}</>;
  }
  if (m.kind === 'sweat') {
    return <svg style={{position: 'absolute', left, top, transform: `translate(-50%,-50%) scale(${p * out})`}} width={size * 0.7} height={size} viewBox="0 0 70 100">
      <path d="M35 4 C 60 40 68 62 50 82 C 40 94 22 94 14 82 C 0 62 12 40 35 4Z" fill="#7fd4ff" stroke={INK} strokeWidth="8" strokeLinejoin="round" /></svg>;
  }
  if (m.kind === 'x') {  // blinded eye
    const s = size;
    return <svg style={{position: 'absolute', left, top, transform: `translate(-50%,-50%) rotate(${Math.sin(u * 14) * 4}deg) scale(${p})`}} width={s} height={s} viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="46" fill="#fff" stroke={INK} strokeWidth="7" />
      <path d="M26 26 L74 74 M74 26 L26 74" stroke="#d6342b" strokeWidth="16" strokeLinecap="round" /></svg>;
  }
  if (m.kind === 'sparks') {
    return <>{[0, 1, 2, 3, 4].map((i) => {
      const v = ((u * 1.4 + i * 0.21) % 1), ang = -90 + (i - 2) * 28;
      const r = v * size * 1.6;
      return <div key={i} style={{position: 'absolute', left: left + Math.cos(ang * Math.PI / 180) * r, top: top + Math.sin(ang * Math.PI / 180) * r, width: size * 0.12, height: size * 0.12, borderRadius: '50%', background: i % 2 ? '#ffd23f' : '#ff7a2e', opacity: (1 - v) * out}} />;
    })}</>;
  }
  return null;
};

// ---------- cutout ----------
const Cutout: React.FC<{c: CutoutSpec; t: number; W: number; H: number; tint: string}> = ({c, t, W, H, tint}) => {
  const {fps} = useVideoConfig();
  const d = dim(c.src);
  const hpx = c.h * H, wpx = hpx * (d.w / d.h);
  const at = c.at ?? 0;
  const enter = c.enter ?? 'none';
  const sp = (u: number, cfg = {damping: 10, stiffness: 120, mass: 0.8}) => spring({frame: Math.max(0, u) * fps, fps, config: cfg});
  const p = enter === 'none' ? 1 : t < at ? 0 : sp(t - at);
  let tx = 0, ty = 0, sx = 1, sy = 1, op = c.opacity ?? 1;
  const dist = c.enterDist ?? 0.5;
  if (enter === 'left') tx = -(1 - p) * dist * W;
  if (enter === 'right') tx = (1 - p) * dist * W;
  if (enter === 'drop') { ty = Math.min(0, -(1 - p) * H); const k = Math.min(0.28, Math.max(0, p - 1) * 1.4); sy = 1 - k; sx = 1 + k * 0.6; }
  if (enter === 'rise') ty = (1 - p) * 0.5 * H;
  if (enter === 'pop') { sx = sy = Math.max(0, p); }
  if (enter === 'fade') op *= clamp01((t - at) / 0.35);
  if (enter !== 'none' && t < at) op = 0;
  // walking hop while travelling in
  if ((enter === 'left' || enter === 'right') && c.walk !== false && t >= at && p < 0.985) ty -= Math.abs(Math.sin((t - at) * 11)) * 0.018 * H * (1 - p * 0.6);
  // exit
  if (c.exitAt !== undefined && t > c.exitAt) {
    const q = easeOut((t - c.exitAt) / 0.5);
    const dirn = enter === 'right' ? 1 : enter === 'left' ? -1 : 1;
    tx += dirn * q * 0.6 * W; op *= 1 - clamp01((t - c.exitAt - 0.3) / 0.2);
  }
  if (c.moveTo && t >= c.moveTo.at) {
    const q = easeOut((t - c.moveTo.at) / c.moveTo.dur);
    tx += (c.moveTo.x ?? c.x) * W * q - c.x * W * q;
    ty += ((c.moveTo.y ?? c.y) - c.y) * H * q;
    if (q > 0 && q < 0.995 && c.walk !== false && !c.noWalkHop) ty -= Math.abs(Math.sin((t - c.moveTo.at) * 10)) * 0.012 * H;
  }
  // idle bob + breathing (only once settled)
  const bobAmp = c.bob ?? 6, ph = (hash(c.id) % 100) / 100 * 6.28;
  if (bobAmp > 0 && (t >= at)) {
    ty += Math.sin(t * 2 * Math.PI * (c.bobSpeed ?? 0.85) + ph) * bobAmp * Math.min(1, p);
    sy *= 1 + Math.sin(t * 2 * Math.PI * (c.bobSpeed ?? 0.85) + ph + 1) * 0.008;
  }
  let rot = c.rot ?? 0; let pivot = '50% 100%';
  if (c.spin) rot += c.spin * (1 - Math.min(1, p));
  if (c.rotateTo) {
    const q = Math.min(1, sp(t - c.rotateTo.at, {damping: 14, stiffness: 70, mass: 1}));
    rot += c.rotateTo.deg * (t >= c.rotateTo.at ? q : 0);
    if (c.rotateTo.pivot) pivot = c.rotateTo.pivot;
    if (c.rotateTo.lift && t >= c.rotateTo.at) ty -= c.rotateTo.lift * H * Math.min(1, q);
  }
  for (const r of c.react ?? []) {
    const u = (t - r.at) / (r.dur ?? 0.6);
    if (u < 0 || u > 1) continue;
    if (r.kind === 'hop') ty -= Math.sin(Math.PI * u) * 0.05 * H;
    if (r.kind === 'shake') tx += Math.sin(u * 40) * 0.006 * W * (1 - u);
    if (r.kind === 'wobble') rot += Math.sin(u * 22) * 7 * (1 - u);
    if (r.kind === 'recoil') { tx += -Math.sin(Math.PI * Math.min(1, u * 1.4)) * 0.03 * W * (c.flip ? -1 : 1); rot += -Math.sin(Math.PI * u) * 5; }
    if (r.kind === 'squash') { const k = Math.sin(Math.PI * u) * 0.12; sy *= 1 - k; sx *= 1 + k * 0.7; }
  }
  const flip = c.flip ? -1 : 1;
  const left = c.x * W - wpx / 2, top = c.y * H - hpx;
  const tintCol = mixToWhite(c.tint ?? tint, 1);
  const lift = Math.max(0, -ty);
  const shW = (c.shadowW ? c.shadowW * H : wpx * 0.82) / (1 + lift / 450);
  const url = IMG(c.src);
  return <>
    {!c.noShadow && op > 0 && (
      <div style={{position: 'absolute', left: c.x * W + tx - shW / 2, top: c.y * H - shW * 0.07, width: shW, height: shW * 0.14, borderRadius: '50%',
        background: 'radial-gradient(ellipse at center, rgba(10,6,14,0.7) 0%, rgba(10,6,14,0.38) 45%, rgba(10,6,14,0) 72%)', opacity: op / (1 + lift / 350), filter: 'blur(4px)'}} />)}
    <div style={{position: 'absolute', left, top, width: wpx, height: hpx, opacity: op, isolation: 'isolate',
      transform: `translate(${tx}px,${ty}px) rotate(${rot}deg) scale(${sx * flip},${sy})`, transformOrigin: pivot, display: c.hidden ? 'none' : undefined}}>
      <Img src={url} style={{width: '100%', height: '100%', display: 'block'}} />
      {/* colour tint + darker feet, clipped to the cutout shape, so characters sit in the scene light */}
      <div style={{position: 'absolute', inset: 0, mixBlendMode: 'multiply',
        background: `linear-gradient(to bottom, ${tintCol} 0%, ${tintCol} 60%, rgba(196,186,200,1) 100%)`,
        WebkitMaskImage: `url(${url})`, WebkitMaskSize: '100% 100%', maskImage: `url(${url})`, maskSize: '100% 100%'} as any} />
      <div style={{position: 'absolute', inset: 0, transform: `scaleX(${flip})`}}>
        {(c.marks ?? []).map((m, i) => <Mark key={i} m={m} t={t} boxW={wpx} boxH={hpx} />)}
      </div>
    </div>
  </>;
};

// ---------- impact word ----------
export const Impact: React.FC<{w: ImpactSpec; t: number}> = ({w, t}) => {
  const {fps} = useVideoConfig();
  const u = t - w.at, dur = w.dur ?? 1.6;
  if (u < 0 || u > dur) return null;
  const p = spring({frame: u * fps, fps, config: {damping: 9, stiffness: 240, mass: 0.6}});
  const sc = 1 + (1 - p) * 1.6;
  const out = clamp01((dur - u) / 0.15);
  const sh = (w.shake ?? 1) * Math.max(0, 1 - u / 0.6);
  const jx = Math.sin(u * 83) * 14 * sh + Math.sin(u * 17) * 2, jy = Math.cos(u * 61) * 10 * sh;
  const boil = (Math.floor(u * 8) % 2 ? 1 : -1) * 0.8; // hand-lettered line boil
  const size = w.size ?? 220;
  return (
    <div style={{position: 'absolute', left: `${w.x * 100}%`, top: `${w.y * 100}%`, transform: `translate(-50%,-50%) translate(${jx}px,${jy}px) rotate(${(w.rot ?? -6) + boil}deg) scale(${sc * out})`,
      fontFamily: FONT_IMPACT, fontSize: size, lineHeight: 1, letterSpacing: 4, color: w.color ?? GOLD, whiteSpace: 'nowrap',
      WebkitTextStroke: `${size * 0.1}px ${INK}`, paintOrder: 'stroke fill', textShadow: `0 ${size * 0.05}px 0 ${INK}`, opacity: out} as any}>{w.text}</div>
  );
};

// ---------- scene ----------
export const Scene: React.FC<SceneProps> = (P) => {
  const f = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  const t = f / fps;
  const cam = (P.cam ?? camPresets.hold())(t, P.dur);
  const flat = P.flatParallax;
  const K = {bg: {z: flat ? 1 : 0.85, p: flat ? 1 : 0.55}, char: {z: 1, p: 1}, fg: {z: flat ? 1 : 1.25, p: flat ? 1 : 1.5}};
  const layerStyle = (k: 'bg' | 'char' | 'fg', shakeK = 1): React.CSSProperties => {
    const s = 1 + (cam.s - 1) * K[k].z;
    return {position: 'absolute', inset: 0, transformOrigin: `${cam.ox * 100}% ${cam.oy * 100}%`,
      transform: `translate(${(cam.x + cam.sx * shakeK) * W * K[k].p}px,${(cam.y + cam.sy * shakeK) * H * K[k].p}px) rotate(${cam.sr * shakeK}deg) scale(${s})`};
  };
  const over = P.bgOverscan ?? 1.14;
  const tint = P.tint ?? '#ffffff';
  const sorted = [...(P.cutouts ?? [])].sort((a, b) => (a.z ?? 0) - (b.z ?? 0));
  const layer = (k: 'bg' | 'char' | 'fg') => sorted.filter((c) => (c.depth ?? 'char') === k);
  const cues: Cue[] = [...(P.cues ?? [])];
  (P.cutouts ?? []).forEach((c) => c.sfx && cues.push({at: c.at ?? 0, sfx: c.sfx, vol: 0.7}));
  (P.impacts ?? []).forEach((w) => w.sfx && cues.push({at: w.at, sfx: w.sfx, vol: 0.8}));
  const dimA = P.dimKeys ? (() => {
    const k = P.dimKeys!; if (t <= k[0][0]) return k[0][1]; if (t >= k[k.length - 1][0]) return k[k.length - 1][1];
    for (let i = 0; i < k.length - 1; i++) if (t >= k[i][0] && t < k[i + 1][0]) { const q = (t - k[i][0]) / (k[i + 1][0] - k[i][0]); return k[i][1] + (k[i + 1][1] - k[i][1]) * q; }
    return 0; })() : 0;
  const flashA = (P.flash ?? []).reduce((a, ft) => { const u = t - ft; return u >= 0 && u < 0.5 ? Math.max(a, (u < 0.05 ? 0.9 : 0.9 * Math.pow(1 - (u - 0.05) / 0.45, 2))) : a; }, 0);
  const ctx = {t, f, fps, W, H};
  return (
    <AbsoluteFill style={{background: '#0d0a10', overflow: 'hidden'}}>
      <div style={layerStyle('bg', 0.6)}>
        <div style={{position: 'absolute', left: `${-(over - 1) / 2 * 100}%`, top: `${-(over - 1) / 2 * 100}%`, width: `${over * 100}%`, height: `${over * 100}%`, transform: P.bgFlip ? 'scaleX(-1)' : undefined}}>
          <Img src={BG(P.bg)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: P.bgPos ?? '50% 50%', filter: P.blur ? `blur(${P.blur}px)` : undefined}} />
          {P.grade && <div style={{position: 'absolute', inset: 0, background: P.grade, mixBlendMode: 'multiply'}} />}
        </div>
        {layer('bg').map((c) => <Cutout key={c.id} c={c} t={t} W={W} H={H} tint={tint} />)}
      </div>
      <div style={layerStyle('char')}>
        {layer('char').map((c) => <Cutout key={c.id} c={c} t={t} W={W} H={H} tint={tint} />)}
        {P.world?.(ctx)}
      </div>
      <div style={layerStyle('fg', 1.4)}>
        {layer('fg').map((c) => <Cutout key={c.id} c={c} t={t} W={W} H={H} tint={tint} />)}
      </div>
      {P.vignette !== 0 && <AbsoluteFill style={{background: `radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,${P.vignette ?? 0.38}) 100%)`}} />}
      {dimA > 0 && <AbsoluteFill style={{background: `rgba(6,4,10,${dimA})`}} />}
      <AbsoluteFill style={{transform: `translate(${cam.sx * W}px,${cam.sy * H}px)`}}>
        {(P.impacts ?? []).map((w, i) => <Impact key={i} w={w} t={t} />)}
      </AbsoluteFill>
      {P.extras?.(ctx)}
      {flashA > 0 && <AbsoluteFill style={{background: `rgba(255,255,255,${flashA})`}} />}
      <Sfx cues={cues} />
    </AbsoluteFill>
  );
};
