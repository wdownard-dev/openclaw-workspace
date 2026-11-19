import React from 'react';
import {Img, staticFile} from 'remotion';
import {C, HAND} from './theme';

/** Grey card with the asset name: the never-fail placeholder for a missing sprite/prop. */
export const Placeholder: React.FC<{name: string; h: number; w?: number}> = ({name, h, w}) => {
  const ww = w || Math.max(h * 0.45, 120);
  return (
    <div style={{width: ww, height: h, background: C.placeholder, border: '4px dashed #555', borderRadius: 18, boxSizing: 'border-box', display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 8, color: '#222', fontFamily: 'DejaVu Sans, sans-serif', fontSize: Math.max(16, Math.min(28, h / 10)), wordBreak: 'break-all'}}>
      MISSING<br />{name}
    </div>
  );
};

/** Code-drawn icons and overlays (ASSET-PLAN 3.2). Each is an SVG of height h, bottom-anchored by the caller. */
export const CodeProp: React.FC<{code: string; h: number; base?: string}> = ({code, h, base}) => {
  const s = h; // unit = height
  const img = (extra: React.CSSProperties = {}) => base ? <Img src={staticFile(base)} style={{height: h, ...extra}} /> : <Placeholder name={code} h={h} />;
  switch (code) {
    case 'prop__ring_small__a':
    case 'prop__ring_large__a':
      return <svg width={s} height={s} viewBox="0 0 100 100"><circle cx={50} cy={50} r={44} fill="none" stroke={C.gold} strokeWidth={8} /><circle cx={50} cy={50} r={44} fill="none" stroke={C.cream} strokeWidth={3} strokeDasharray="6 6" /></svg>;
    case 'prop__eye_icon__a':
    case 'prop__oneeye_crossed__a':
      return <svg width={s * 1.6} height={s} viewBox="0 0 160 100"><path d="M8 50 Q80 -10 152 50 Q80 110 8 50Z" fill={C.cream} stroke={C.outline} strokeWidth={6} /><circle cx={80} cy={50} r={22} fill={C.ink} /><circle cx={80} cy={50} r={9} fill={C.outline} />{code.includes('crossed') && <g stroke={C.gold} strokeWidth={12} strokeLinecap="round"><line x1={20} y1={10} x2={140} y2={90} /><line x1={140} y1={10} x2={20} y2={90} /></g>}</svg>;
    case 'prop__ship_icon__a':
      return base ? img() : <svg width={s * 1.6} height={s} viewBox="0 0 160 100"><path d="M10 70 L150 70 L130 95 L30 95Z" fill={C.ink} /><rect x={78} y={10} width={6} height={60} fill={C.outline} /><path d="M84 14 L130 50 L84 50Z" fill={C.cream} stroke={C.outline} strokeWidth={3} /></svg>;
    case 'prop__ship_crossed__a':
      return <div style={{position: 'relative', height: h, width: h * 1.6}}>{base ? <Img src={staticFile(base)} style={{height: h}} /> : <CodeProp code="prop__ship_icon__a" h={h} />}<svg width={s * 1.6} height={s} viewBox="0 0 160 100" style={{position: 'absolute', left: 0, top: 0}}><g stroke={C.gold} strokeWidth={14} strokeLinecap="round"><line x1={15} y1={10} x2={145} y2={90} /><line x1={145} y1={10} x2={15} y2={90} /></g></svg></div>;
    case 'NP04_listing':
      return <div style={{height: h, transform: 'rotate(12deg)', transformOrigin: '50% 80%'}}>{img()}</div>;
    case 'prop__height_line__a':
      return <svg width={s * 0.3} height={s} viewBox="0 0 30 100" preserveAspectRatio="none"><line x1={15} y1={2} x2={15} y2={98} stroke={C.verd} strokeWidth={4} strokeDasharray="4 3" /><line x1={2} y1={3} x2={28} y2={3} stroke={C.verd} strokeWidth={4} /><line x1={2} y1={97} x2={28} y2={97} stroke={C.verd} strokeWidth={4} /></svg>;
    case 'prop__person_silhouette__a':
      return <svg width={s * 0.4} height={s} viewBox="0 0 40 100"><circle cx={20} cy={10} r={8} fill="#8a8a8a" /><path d="M8 22 H32 L36 55 H30 L30 98 H23 L20 70 L17 98 H10 L10 55 H4Z" fill="#8a8a8a" /></svg>;
    case 'prop__waterdrops__a':
      return <svg width={s} height={s} viewBox="0 0 100 100">{[[25, 40], [55, 25], [75, 60]].map(([x, y], i) => <path key={i} d={`M${x} ${y - 18} Q${x + 14} ${y + 2} ${x} ${y + 14} Q${x - 14} ${y + 2} ${x} ${y - 18}Z`} fill={C.sea} stroke={C.ink} strokeWidth={3} />)}</svg>;
    case 'prop__pin__a':
    case 'prop__bone_pin__a':
      return <svg width={s * 0.6} height={s} viewBox="0 0 60 100"><path d="M30 98 L12 50 A22 22 0 1 1 48 50Z" fill={C.gold} stroke={C.outline} strokeWidth={4} /><circle cx={30} cy={36} r={9} fill={C.cream} />{code.includes('bone') && <g transform="translate(30 36) rotate(-30)"><rect x={-14} y={-3} width={28} height={6} fill={C.cream} stroke={C.outline} strokeWidth={2} /><circle cx={-14} cy={-3} r={4} fill={C.cream} stroke={C.outline} strokeWidth={2} /><circle cx={-14} cy={3} r={4} fill={C.cream} stroke={C.outline} strokeWidth={2} /><circle cx={14} cy={-3} r={4} fill={C.cream} stroke={C.outline} strokeWidth={2} /><circle cx={14} cy={3} r={4} fill={C.cream} stroke={C.outline} strokeWidth={2} /></g>}</svg>;
    case 'prop__book_icon__a':
      return <svg width={s * 0.8} height={s} viewBox="0 0 80 100"><rect x={8} y={6} width={64} height={88} rx={4} fill={C.ink} stroke={C.outline} strokeWidth={4} /><rect x={16} y={6} width={6} height={88} fill={C.cream} opacity={0.5} /><rect x={30} y={30} width={34} height={6} fill={C.cream} /><rect x={30} y={44} width={34} height={6} fill={C.cream} /></svg>;
    case 'prop__arrow_left__a':
    case 'prop__pointer__a':
      return <svg width={s * 2} height={s} viewBox="0 0 200 100"><path d={code === 'prop__arrow_left__a' ? 'M190 50 L60 50 L60 20 L10 50 L60 80 L60 50' : 'M10 50 L140 50 L140 20 L190 50 L140 80 L140 50'} fill={C.ink} stroke={C.cream} strokeWidth={6} strokeLinejoin="round" /></svg>;
    case 'prop__heart__a':
      return <svg width={s} height={s} viewBox="0 0 100 100"><path d="M50 90 L15 52 A20 20 0 0 1 50 25 A20 20 0 0 1 85 52Z" fill="#c0392b" stroke={C.outline} strokeWidth={4} /></svg>;
    case 'prop__flame_glow__a':
      return <svg width={s} height={s} viewBox="0 0 100 100"><defs><radialGradient id="fg"><stop offset="0" stopColor="#ffb347" stopOpacity={0.9} /><stop offset="1" stopColor="#ff7a00" stopOpacity={0} /></radialGradient></defs><circle cx={50} cy={50} r={50} fill="url(#fg)" /></svg>;
    case 'prop__dustpuff__a':
      return <svg width={s * 1.4} height={s} viewBox="0 0 140 100">{[[30, 70, 26], [60, 55, 32], [95, 65, 28], [120, 78, 18], [70, 85, 22]].map(([x, y, r], i) => <circle key={i} cx={x} cy={y} r={r} fill="#d8cdb8" stroke={C.outline} strokeWidth={3} />)}</svg>;
    case 'prop__source_slip_empty__a':
      return <svg width={s * 1.5} height={s} viewBox="0 0 150 100"><rect x={4} y={4} width={142} height={92} fill={C.cream} stroke={C.outline} strokeWidth={4} transform="rotate(-3 75 50)" />{[30, 48, 66].map((y) => <line key={y} x1={20} y1={y} x2={130} y2={y} stroke="#b9ad93" strokeWidth={3} />)}</svg>;
    case 'prop__etna_icon__a':
      return <svg width={s * 1.2} height={s} viewBox="0 0 120 100"><path d="M5 98 L45 35 L75 35 L115 98Z" fill="#7a6a58" stroke={C.outline} strokeWidth={4} /><path d="M50 35 Q60 5 75 20 Q95 0 90 30" fill="none" stroke="#777" strokeWidth={10} strokeLinecap="round" /></svg>;
    case 'prop__whirlpool__a':
      return <svg width={s} height={s} viewBox="0 0 100 100">{[44, 32, 20, 9].map((r, i) => <circle key={i} cx={50} cy={50} r={r} fill="none" stroke={C.sea} strokeWidth={6} strokeDasharray={`${r * 4} ${r * 1.5}`} />)}</svg>;
    case 'polyphemus__silhouette__a':
    case 'cyc2__trio_silhouette__a':
      return base ? <Img src={staticFile(base)} style={{height: h, filter: 'brightness(0) saturate(0)', opacity: 0.92}} /> : <svg width={s * 0.55} height={s} viewBox="0 0 55 100"><path d="M27 0 Q45 0 46 22 Q55 30 55 60 L50 100 L5 100 L0 60 Q0 30 8 22 Q9 0 27 0Z" fill="#141210" /></svg>;
    case 'crew__line12__a':
    case 'crew__huddle4__a':
    case 'crew__workers_group__a': {
      const n = code.includes('12') ? 12 : code.includes('4') ? 4 : 6, step = h * 0.42;
      return <div style={{position: 'relative', height: h, width: step * (n - 1) + h * 0.5}}>{Array.from({length: n}).map((_, i) => <div key={i} style={{position: 'absolute', left: i * step, bottom: (i % 2) * h * 0.02, transform: i % 3 === 1 ? 'scaleX(-1)' : undefined}}>{base ? <Img src={staticFile(base)} style={{height: h}} /> : <Placeholder name={`crew x${n}`} h={h} />}</div>)}</div>;
    }
    default:
      return <Placeholder name={code} h={h} />;
  }
};
/** label used by the Board for a blank card */
export const Hand: React.FC<{size: number; color?: string; children: React.ReactNode; style?: React.CSSProperties}> = ({size, color = C.ink, children, style}) => <div style={{fontFamily: HAND, fontSize: size, color, lineHeight: 1, whiteSpace: 'nowrap', ...style}}>{children}</div>;
