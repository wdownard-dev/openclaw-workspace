import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, FONT, clamp01, easeOut, ramp} from './theme';

export const useT = () => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return f / fps; };

/** gentle reveal: opacity + small rise, no overshoot */
export const reveal = (t: number, at: number, d = 0.45, rise = 14) => {
  const u = easeOut(ramp(t, at, at + d));
  return {opacity: u, transform: `translateY(${(1 - u) * rise}px)`} as React.CSSProperties;
};

export const Grain: React.FC<{alpha?: number}> = ({alpha = 0.05}) => {
  const f = useCurrentFrame();
  const k = Math.floor(f / 2);
  return <div style={{position: 'absolute', inset: 0, backgroundImage: `url(${staticFile('img/grain.png')})`, backgroundSize: '256px 256px', backgroundPosition: `${(k * 61) % 256}px ${(k * 97) % 256}px`, opacity: alpha, pointerEvents: 'none'}} />;
};

/** Dark ledger card: ink ground, hairline frame, small channel tag. */
export const CardBg: React.FC<{children?: React.ReactNode; tag?: boolean; paper?: boolean}> = ({children, tag = true, paper = false}) => (
  <AbsoluteFill style={{background: paper ? `radial-gradient(ellipse at 50% 45%, #efe6d2 0%, ${C.paperBg} 55%, #cfc4aa 100%)` : `radial-gradient(ellipse at 50% 42%, ${C.bg2} 0%, ${C.bg} 62%, #0c0a07 100%)`, fontFamily: FONT}}>
    <div style={{position: 'absolute', inset: 46, border: `1.5px solid ${paper ? 'rgba(36,29,21,0.35)' : C.line}`}} />
    {tag && <div style={{position: 'absolute', left: 84, top: 70, fontSize: 19, letterSpacing: 6, color: paper ? 'rgba(36,29,21,0.6)' : C.muted, fontWeight: 700}}>THE MYTH LEDGER</div>}
    {children}
    <Grain alpha={paper ? 0.04 : 0.05} />
  </AbsoluteFill>
);

export const Kicker: React.FC<{children: React.ReactNode; style?: React.CSSProperties; paper?: boolean}> = ({children, style, paper}) => (
  <div style={{fontFamily: FONT, fontSize: 26, letterSpacing: 7, fontWeight: 700, color: C.rust, textTransform: 'uppercase', ...style}}>{children}</div>
);

export const Rule: React.FC<{w: number | string; style?: React.CSSProperties; color?: string}> = ({w, style, color = C.lineStrong}) => <div style={{height: 2, width: w, background: color, ...style}} />;

/** drawn check mark */
export const Tick: React.FC<{size?: number; p?: number; color?: string}> = ({size = 56, p = 1, color = C.rustHi}) => (
  <svg width={size} height={size} viewBox="0 0 56 56"><path d="M8 30 L22 44 L48 12" fill="none" stroke={color} strokeWidth={7} strokeLinecap="square" strokeDasharray={80} strokeDashoffset={80 * (1 - clamp01(p))} /></svg>
);

/** restrained stamp (static tilt, no motion) */
export const Stamp: React.FC<{text: string; t: number; at: number; size?: number; style?: React.CSSProperties}> = ({text, t, at, size = 64, style}) => {
  const u = easeOut(ramp(t, at, at + 0.35));
  return (
    <div style={{position: 'absolute', border: `5px solid ${C.rustHi}`, color: C.rustHi, fontFamily: FONT, fontWeight: 700, fontSize: size, letterSpacing: 10, padding: '10px 34px', transform: `rotate(-5deg)`, opacity: u * 0.94, background: 'rgba(20,16,12,0.55)', ...style}}>{text}</div>
  );
};

/** lower-third plate, top-left safe zone so it never meets the captions */
export const LowerThird: React.FC<{label?: string; text: React.ReactNode; t: number; at?: number; w?: number; size?: number; style?: React.CSSProperties; lang?: boolean}> = ({label, text, t, at = 0.3, w = 920, size = 40, style}) => (
  <div style={{position: 'absolute', left: 84, top: 84, width: w, padding: '18px 28px 20px 30px', background: 'rgba(16,12,9,0.78)', borderLeft: `6px solid ${C.rust}`, fontFamily: FONT, color: C.paper, ...reveal(t, at, 0.5, 10), ...style}}>
    {label && <div style={{fontSize: 21, letterSpacing: 6, fontWeight: 700, color: C.rustHi, marginBottom: 8, textTransform: 'uppercase'}}>{label}</div>}
    <div style={{fontSize: size, lineHeight: 1.28}}>{text}</div>
  </div>
);

/** quote over a darkened lower band (captions are off for these shots) */
export const QuoteBlock: React.FC<{quote: string; credit: string; t: number; at?: number; size?: number; top?: number}> = ({quote, credit, t, at = 0.25, size = 54, top = 640}) => (
  <>
    <AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(10,8,6,0) 36%, rgba(10,8,6,0.82) 66%, rgba(10,8,6,0.9) 100%)', opacity: easeOut(ramp(t, at - 0.1, at + 0.4))}} />
    <div style={{position: 'absolute', left: 200, right: 200, top, fontFamily: FONT, textAlign: 'center', ...reveal(t, at, 0.55, 12)}}>
      <div style={{fontSize: size, fontStyle: 'italic', lineHeight: 1.3, color: C.paper, textShadow: '0 2px 6px rgba(0,0,0,0.8)'}}>&ldquo;{quote}&rdquo;</div>
      <div style={{marginTop: 26, fontSize: 25, letterSpacing: 3, color: C.muted, fontWeight: 700}}>{credit}</div>
    </div>
  </>
);

export const Img2: React.FC<{src: string; style?: React.CSSProperties}> = ({src, style}) => <Img src={staticFile(src)} style={style} />;
