import React from 'react';
import {AbsoluteFill, Img, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {getLength, getPointAtLength, getTangentAtLength} from '@remotion/paths';
import {BG, IMG} from './assets';
import {cam} from './camera';
import {FONT_CAP, FONT_IMPACT, GOLD, INK, clamp01, easeInOut, easeOut} from './theme';
import {Scene, Sfx, SceneProps} from './Scene';

const bgBlur = (name: string, scale: number, dark: number) => ({name, scale, dark});

/** Chapter / title card: slow-zoom blurred painting, gold rules wipe in, letters pop one by one, sting. */
export const TitleCard: React.FC<{kicker: string; title: string; sub?: string; numeral?: string; bg?: string; dur: number}> = ({kicker, title, sub, numeral, bg = 'cavedawn', dur}) => {
  const f = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  const t = f / fps;
  const letters = title.split('');
  const rule = easeOut((t - 0.05) / 0.55);
  return (
    <AbsoluteFill style={{background: '#0d0a10', overflow: 'hidden'}}>
      <Img src={BG(bg)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', filter: 'blur(6px) brightness(0.7) saturate(1.15)', transform: `scale(${1.08 + t * 0.03})`}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(10,6,14,0.15) 30%, rgba(10,6,14,0.7) 100%)'}} />
      {numeral && <div style={{position: 'absolute', right: 140, top: 40, fontFamily: FONT_IMPACT, fontSize: 620, color: 'rgba(255,210,63,0.10)', lineHeight: 1}}>{numeral}</div>}
      <div style={{position: 'absolute', left: 0, right: 0, top: H * 0.33, textAlign: 'center', fontFamily: FONT_CAP, fontSize: 46, letterSpacing: 10, color: '#f2e6c8', opacity: clamp01((t - 0.1) / 0.3), transform: `translateY(${(1 - easeOut((t - 0.1) / 0.4)) * 18}px)`}}>{kicker}</div>
      <div style={{position: 'absolute', left: W * 0.5 - W * 0.3 * rule, width: W * 0.6 * rule, top: H * 0.33 + 78, height: 5, background: GOLD, borderRadius: 3}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: H * 0.40, textAlign: 'center', fontFamily: FONT_IMPACT, fontSize: 260, lineHeight: 1, letterSpacing: 8, whiteSpace: 'nowrap'}}>
        {letters.map((ch, i) => {
          const p = spring({frame: f - 6 - i * 2, fps, config: {damping: 9, stiffness: 200, mass: 0.6}});
          return <span key={i} style={{display: 'inline-block', color: GOLD, WebkitTextStroke: `22px ${INK}`, paintOrder: 'stroke fill', textShadow: `0 12px 0 ${INK}`, transform: `translateY(${(1 - p) * -140}px) scale(${0.4 + 0.6 * p}) rotate(${(1 - p) * (i % 2 ? 12 : -12)}deg)`, opacity: clamp01(p * 3), whiteSpace: 'pre'} as any}>{ch}</span>;
        })}
      </div>
      {sub && <div style={{position: 'absolute', left: 0, right: 0, top: H * 0.72, textAlign: 'center', fontFamily: FONT_CAP, fontSize: 52, color: '#fff', WebkitTextStroke: `8px ${INK}`, paintOrder: 'stroke fill', letterSpacing: 2, opacity: clamp01((t - 0.9) / 0.4)} as any}>{sub}</div>}
      <Sfx cues={[{at: 0, sfx: 'sting', vol: 0.75}]} />
    </AbsoluteFill>
  );
};

/** End card / tease: stormy painting, lightning, "next" tease, channel lockup. */
export const EndCard: React.FC<{kicker: string; title: string; dur: number}> = ({kicker, title, dur}) => {
  const f = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  const t = f / fps;
  const lines = title.split('\n');
  const flashT = [1.4, 3.9];
  const flashA = flashT.reduce((a, ft) => { const u = t - ft; return u >= 0 && u < 0.5 ? Math.max(a, u < 0.05 ? 0.8 : 0.8 * Math.pow(1 - (u - 0.05) / 0.45, 2)) : a; }, 0);
  const pill = spring({frame: f - 2.6 * fps, fps, config: {damping: 11, stiffness: 140}});
  return (
    <AbsoluteFill style={{background: '#0d0a10', overflow: 'hidden'}}>
      <Img src={BG('storm')} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', filter: 'blur(3px) brightness(0.5)', transform: `scale(${1.12 + t * 0.02})`}} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(10,6,14,0.1) 30%, rgba(10,6,14,0.75) 100%)'}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: H * 0.17, textAlign: 'center', fontFamily: FONT_CAP, fontSize: 56, letterSpacing: 12, color: GOLD, opacity: clamp01((t - 0.15) / 0.3)}}>{kicker}</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: H * 0.27, textAlign: 'center', fontFamily: FONT_IMPACT, fontSize: 200, lineHeight: 0.98, letterSpacing: 6, color: '#fff', WebkitTextStroke: `20px ${INK}`, paintOrder: 'stroke fill', textShadow: `0 10px 0 ${INK}`} as any}>
        {lines.map((l, i) => {
          const p = spring({frame: f - 0.3 * fps - i * 5, fps, config: {damping: 10, stiffness: 160, mass: 0.7}});
          return <div key={i} style={{transform: `scale(${0.3 + 0.7 * p})`, opacity: clamp01(p * 2.5)}}>{l}</div>;
        })}
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 170, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 28, opacity: clamp01((t - 1.8) / 0.4)}}>
        <Img src={IMG('avatar')} style={{width: 120, height: 120, borderRadius: '50%', border: `6px solid ${GOLD}`}} />
        <div style={{fontFamily: FONT_CAP, fontSize: 64, color: '#fff', WebkitTextStroke: `8px ${INK}`, paintOrder: 'stroke fill', letterSpacing: 3} as any}>THE MYTH LEDGER</div>
        <div style={{fontFamily: FONT_CAP, fontSize: 40, color: '#fff', background: '#e23b30', padding: '12px 32px', borderRadius: 40, border: `5px solid ${INK}`, transform: `scale(${Math.max(0, pill)})`}}>SUBSCRIBE</div>
      </div>
      {flashA > 0 && <AbsoluteFill style={{background: `rgba(255,255,255,${flashA})`}} />}
      <Sfx cues={[{at: 0.3, sfx: 'thud', vol: 0.8}, {at: 1.4, sfx: 'thunder', vol: 0.7}, {at: 3.9, sfx: 'thunder', vol: 0.6}, {at: 2.6, sfx: 'pop', vol: 0.6}]} />
    </AbsoluteFill>
  );
};

// ---------- catmull-rom path through points ----------
export const smoothPath = (pts: [number, number][]) => {
  let d = `M ${pts[0][0]} ${pts[0][1]}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C ${c1[0]} ${c1[1]} ${c2[0]} ${c2[1]} ${p2[0]} ${p2[1]}`;
  }
  return d;
};

export type MapPin = {label: string; nx: number; ny: number; at: number; kind?: 'dot' | 'x'; dx?: number; dy?: number};
/** Map shot: painting + animated dotted route with arrowhead, pins and a years counter. Coordinates are fractions of the map picture. */
export const MapShot: React.FC<{bg: string; imgAspect: number; route: [number, number][]; draw: [number, number]; pins: MapPin[]; counter?: {label: string; from: number; to: number}; extra?: SceneProps['extras']; dur: number}> = ({bg, imgAspect, route, draw, pins, counter, extra, dur}) => {
  const W = 1920, H = 1080;
  // object-fit: cover geometry for the map picture (no overscan)
  const dispW = Math.max(W, H * imgAspect), dispH = dispW / imgAspect, offX = (W - dispW) / 2, offY = (H - dispH) / 2;
  const P = (nx: number, ny: number): [number, number] => [offX + nx * dispW, offY + ny * dispH];
  const pts = route.map(([x, y]) => P(x, y));
  const d = smoothPath(pts);
  const len = getLength(d);
  return (
    <Scene bg={bg} bgOverscan={1} flatParallax dur={dur} vignette={0.3} grade="#f6ead2" cam={cam.pushIn(1.1, 0.5, 0.3, undefined, 1.03)}
      cues={[{at: 0, sfx: 'whoosh', vol: 0.35}]}
      world={({t}) => {
        const prog = easeInOut(clamp01((t - draw[0]) / (draw[1] - draw[0])));
        const tip = getPointAtLength(d, len * prog), tan = getTangentAtLength(d, Math.max(0.1, len * prog));
        const ang = Math.atan2(tan.y, tan.x) * 180 / Math.PI;
        return <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
          <defs><mask id="reveal"><path d={d} stroke="#fff" strokeWidth="30" fill="none" strokeDasharray={len} strokeDashoffset={len * (1 - prog)} strokeLinecap="round" /></mask></defs>
          <path d={d} stroke="#7a1f14" strokeWidth="11" fill="none" strokeDasharray="1 24" strokeLinecap="round" mask="url(#reveal)" />
          {t >= draw[0] && prog < 1.001 && <g transform={`translate(${tip.x} ${tip.y}) rotate(${ang})`}><path d="M 34 0 L -18 -26 L -6 0 L -18 26 Z" fill="#c62f22" stroke={INK} strokeWidth="6" strokeLinejoin="round" /></g>}
          {pins.map((pin, i) => {
            const u = t - pin.at; if (u < 0) return null;
            const s = Math.max(0, spring({frame: u * 30, fps: 30, config: {damping: 8, stiffness: 220, mass: 0.5}}));
            const [x, y] = P(pin.nx, pin.ny);
            return <g key={i} transform={`translate(${x} ${y}) scale(${s})`}>
              {pin.kind === 'x' ? <path d="M -26 -26 L 26 26 M 26 -26 L -26 26" stroke="#c62f22" strokeWidth="18" strokeLinecap="round" /> : <><circle r="20" fill="#ffd23f" stroke={INK} strokeWidth="7" /><circle r="7" fill={INK} /></>}
              <text x={pin.dx ?? 0} y={pin.dy ?? -42} textAnchor="middle" fontFamily={FONT_IMPACT} fontSize="64" fill="#fff" stroke={INK} strokeWidth="14" paintOrder="stroke" strokeLinejoin="round" letterSpacing="3">{pin.label}</text>
            </g>;
          })}
        </svg>;
      }}
      extras={(c) => {
        const prog = easeInOut(clamp01((c.t - draw[0]) / (draw[1] - draw[0])));
        const p = spring({frame: (c.t - 0.3) * 30, fps: 30, config: {damping: 12, stiffness: 150}});
        return <>
          {counter && <div style={{position: 'absolute', right: 70, top: 60, transform: `scale(${Math.max(0, p)})`, transformOrigin: 'top right', background: '#3a2316', border: `6px solid ${GOLD}`, borderRadius: 18, padding: '10px 34px', textAlign: 'center', boxShadow: '0 8px 0 rgba(0,0,0,0.35)'}}>
            <div style={{fontFamily: FONT_CAP, fontSize: 30, color: '#f2e6c8', letterSpacing: 4}}>{counter.label}</div>
            <div style={{fontFamily: FONT_IMPACT, fontSize: 120, color: GOLD, lineHeight: 1}}>{Math.round(counter.from + (counter.to - counter.from) * prog)}</div>
          </div>}
          {extra?.(c)}
        </>;
      }}
      cutouts={[]} />
  );
};

/** Lower-third name plate (info shot element). */
export const NamePlate: React.FC<{t: number; at: number; dur: number; name: string; sub?: string; x?: number; y?: number}> = ({t, at, dur, name, sub, x = 90, y = 800}) => {
  const u = t - at; if (u < 0 || u > dur) return null;
  const inP = easeOut(u / 0.3), outP = easeOut((dur - u) / 0.25);
  const k = Math.min(inP, outP);
  return <div style={{position: 'absolute', left: x, top: y, transform: `translateX(${(1 - k) * -700}px)`}}>
    <div style={{background: '#c62f22', border: `6px solid ${INK}`, padding: '8px 30px', fontFamily: FONT_IMPACT, fontSize: 96, color: '#fff', letterSpacing: 4, WebkitTextStroke: `7px ${INK}`, paintOrder: 'stroke fill', transform: 'rotate(-2deg)', boxShadow: '0 8px 0 rgba(0,0,0,0.35)'} as any}>{name}</div>
    {sub && <div style={{background: '#f2e6c8', border: `5px solid ${INK}`, padding: '4px 22px', fontFamily: FONT_CAP, fontSize: 34, color: INK, marginTop: -6, marginLeft: 26, display: 'inline-block', transform: 'rotate(1deg)'}}>{sub}</div>}
  </div>;
};

/** Big counter card, e.g. "22 WAGONS". */
export const CountCard: React.FC<{t: number; at: number; dur: number; n: number; label: string; x: number; y: number}> = ({t, at, dur, n, label, x, y}) => {
  const u = t - at; if (u < 0 || u > dur) return null;
  const p = spring({frame: u * 30, fps: 30, config: {damping: 9, stiffness: 200, mass: 0.6}});
  const out = clamp01((dur - u) / 0.2);
  const val = Math.round(n * easeOut(u / 0.7));
  return <div style={{position: 'absolute', left: `${x * 100}%`, top: `${y * 100}%`, transform: `translate(-50%,-50%) rotate(4deg) scale(${Math.max(0, p) * out})`, textAlign: 'center'}}>
    <div style={{fontFamily: FONT_IMPACT, fontSize: 300, lineHeight: 0.9, color: GOLD, WebkitTextStroke: `28px ${INK}`, paintOrder: 'stroke fill', textShadow: `0 14px 0 ${INK}`} as any}>{val}</div>
    <div style={{fontFamily: FONT_IMPACT, fontSize: 120, lineHeight: 1, color: '#fff', WebkitTextStroke: `16px ${INK}`, paintOrder: 'stroke fill', textShadow: `0 8px 0 ${INK}`} as any}>{label}</div>
  </div>;
};
