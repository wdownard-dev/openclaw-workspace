import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {C, FONT, clamp01, easeOut, easeInOut, lerp, ramp} from './theme';
import {CardBg, Kicker, Stamp, Tick, reveal, useT} from './ui';
import {wordAt} from './timing';
import {SicilyInset} from './Maps';
import dims from '../data/dims.json';

/* ------------------------------------------------------------------ elephant skull, front view (original vector drawing) */
const SKULL = 'M500 70 C330 70 170 160 128 330 C108 410 112 480 150 540 C200 610 260 640 300 690 L330 780 C345 830 400 850 440 840 L460 805 L540 805 L560 840 C600 850 655 830 670 780 L700 690 C740 640 800 610 850 540 C888 480 892 410 872 330 C830 160 670 70 500 70 Z';
const NASAL = 'M500 300 C420 300 378 360 378 432 C378 505 430 565 500 585 C570 565 622 505 622 432 C622 360 580 300 500 300 Z';
export const SkullArt: React.FC<{ox: number; oy: number; k: number; ringNasal?: number; ringOrbits?: number; ghost?: number; labelNasal?: number; labelOrbits?: number; ghostLabel?: number; pulse?: number; dim?: number}> = ({ox, oy, k, ringNasal = 0, ringOrbits = 0, ghost = 0, labelNasal = 0, labelOrbits = 0, ghostLabel = 0, pulse = 0}) => {
  const T = (x: number, y: number): [number, number] => [ox + k * x, oy + k * y];
  const [nx, ny] = T(500, 440);
  const dashN = 1700;
  return (
    <svg width={1920} height={940} viewBox="0 0 1920 940" style={{position: 'absolute', left: 0, top: 0, fontFamily: FONT}}>
      <defs>
        <radialGradient id="bone" cx="50%" cy="38%" r="70%"><stop offset="0" stopColor="#e1d5b3" /><stop offset="0.7" stopColor="#bba983" /><stop offset="1" stopColor="#8f7e5c" /></radialGradient>
      </defs>
      <g transform={`translate(${ox} ${oy}) scale(${k})`}>
        <path d={SKULL} fill="url(#bone)" stroke="#241b12" strokeWidth={6 / k * 0.8} strokeLinejoin="round" />
        {/* dome shading, sutures and cheek arches: simple line work */}
        <path d="M330 170 C420 128 580 128 670 170" fill="none" stroke="#7a6a4b" strokeWidth={4} strokeLinecap="round" opacity={0.7} />
        <path d="M250 250 C300 205 360 185 400 180" fill="none" stroke="#7a6a4b" strokeWidth={3} strokeLinecap="round" opacity={0.5} />
        <path d="M750 250 C700 205 640 185 600 180" fill="none" stroke="#7a6a4b" strokeWidth={3} strokeLinecap="round" opacity={0.5} />
        <path d="M500 90 L500 292" fill="none" stroke="#7a6a4b" strokeWidth={3} strokeDasharray="8 10" opacity={0.55} />
        <path d="M160 560 C215 590 270 590 318 650" fill="none" stroke="#6e5f43" strokeWidth={5} strokeLinecap="round" opacity={0.7} />
        <path d="M840 560 C785 590 730 590 682 650" fill="none" stroke="#6e5f43" strokeWidth={5} strokeLinecap="round" opacity={0.7} />
        {/* short tusk stubs and sockets */}
        <path d="M352 790 C340 850 330 895 310 932 C336 942 368 934 384 914 C408 870 430 830 446 800 Z" fill="#efe6cc" stroke="#241b12" strokeWidth={5} strokeLinejoin="round" />
        <path d="M648 790 C660 850 670 895 690 932 C664 942 632 934 616 914 C592 870 570 830 554 800 Z" fill="#efe6cc" stroke="#241b12" strokeWidth={5} strokeLinejoin="round" />
        {/* tusk sockets */}
        <ellipse cx={398} cy={792} rx={50} ry={38} fill="#2b2016" stroke="#241b12" strokeWidth={5} />
        <ellipse cx={602} cy={792} rx={50} ry={38} fill="#2b2016" stroke="#241b12" strokeWidth={5} />
        {/* orbits: small, low, at the sides */}
        <ellipse cx={178} cy={500} rx={40} ry={46} fill="#130e09" stroke="#241b12" strokeWidth={5} />
        <ellipse cx={822} cy={500} rx={40} ry={46} fill="#130e09" stroke="#241b12" strokeWidth={5} />
        {/* the single central (nasal) opening */}
        <path d={NASAL} fill="#3a2d1e" stroke="#241b12" strokeWidth={6} />
        <path d={NASAL} fill="#0f0b07" transform="translate(500 450) scale(0.86) translate(-500 -450)" />
      </g>
      {/* human-style eye placement, for comparison only */}
      {ghost > 0 && (<g opacity={ghost}>
        {[T(372, 215), T(628, 215)].map(([x, y], i) => <ellipse key={i} cx={x} cy={y} rx={34 * k / 0.78} ry={28 * k / 0.78} fill="none" stroke={C.paper} strokeWidth={3} strokeDasharray="9 8" />)}
      </g>)}
      {/* rings and labels */}
      {ringNasal > 0 && (() => { const [cx, cy] = T(500, 442); const rx = 148 * k, ry = 172 * k; return (
        <g>
          <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="none" stroke={C.rustHi} strokeWidth={7} strokeDasharray={dashN} strokeDashoffset={dashN * (1 - ringNasal)} transform={`rotate(-90 ${cx} ${cy})`} opacity={1} />
          {pulse > 0 && <ellipse cx={cx} cy={cy} rx={rx + 22 * pulse} ry={ry + 22 * pulse} fill="none" stroke={C.rustHi} strokeWidth={3} opacity={0.5 * (1 - pulse)} />}
        </g>); })()}
      {labelNasal > 0 && (() => { const [x, y] = T(622, 420); const [lx, ly] = T(950, 300); return (
        <g opacity={labelNasal}>
          <polyline points={`${x + 6},${y} ${lx - 20},${ly + 14} ${lx},${ly + 14}`} fill="none" stroke={C.paper} strokeWidth={3} />
          <text x={lx + 10} y={ly + 4} fill={C.paper} fontSize={48} fontWeight={700}>trunk opening</text>
          <text x={lx + 10} y={ly + 46} fill={C.muted} fontSize={30} fontStyle="italic">one huge central hole</text>
        </g>); })()}
      {ringOrbits > 0 && [T(178, 500), T(822, 500)].map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r={54 * k / 0.78 * 0.78 + 14} fill="none" stroke={C.rustHi} strokeWidth={6} strokeDasharray={420} strokeDashoffset={420 * (1 - ringOrbits)} transform={`rotate(-90 ${x} ${y})`} />
      ))}
      {labelOrbits > 0 && (<g opacity={labelOrbits}>
        {(() => { const [x, y] = T(178, 500); return (<g><line x1={x - 36} y1={y + 24} x2={x - 120} y2={y + 80} stroke={C.paper} strokeWidth={3} /><text x={x - 128} y={y + 100} fill={C.paper} fontSize={40} fontWeight={700} textAnchor="end">eye socket</text><text x={x - 128} y={y + 138} fill={C.muted} fontSize={26} fontStyle="italic" textAnchor="end">small, low, at the side</text></g>); })()}
        {(() => { const [x, y] = T(822, 500); return (<g><line x1={x + 36} y1={y + 24} x2={x + 120} y2={y + 80} stroke={C.paper} strokeWidth={3} /><text x={x + 128} y={y + 100} fill={C.paper} fontSize={40} fontWeight={700}>eye socket</text></g>); })()}
      </g>)}
      {ghostLabel > 0 && (() => { const [x, y] = T(662, 215); const [lx, ly] = T(950, 215); return (
        <g opacity={ghostLabel}>
          <line x1={x + 6} y1={y} x2={lx - 8} y2={ly} stroke={C.muted} strokeWidth={2} strokeDasharray="6 6" />
          <text x={lx + 6} y={ly - 4} fill={C.muted} fontSize={30} fontStyle="italic">where a face would</text>
          <text x={lx + 6} y={ly + 34} fill={C.muted} fontSize={30} fontStyle="italic">put two eyes</text>
        </g>); })()}
    </svg>
  );
};

export const SkullNote: React.FC<{t: number}> = ({t}) => (
  <div style={{position: 'absolute', left: 84, top: 820, width: 380, fontSize: 21, lineHeight: 1.35, fontStyle: 'italic', color: C.muted, fontFamily: FONT, opacity: easeOut(ramp(t, 0.4, 0.9))}}>Illustration: simplified front view of a dwarf-elephant skull, not a scan; proportions approximate.</div>
);

export type SkullState = {ringNasalAt?: number; labelNasalAt?: number; ringOrbitsAt?: number; labelOrbitsAt?: number; ghostAt?: number; ghostOutAt?: number; stamp?: {text: string; at: number}; inset?: boolean; zoom?: [number, number]; dur?: number; k?: number};
/** the one skull plate (DG-01), driven by state times so shots 3, 64-66, 124-125, 136, 143 stay visually identical */
export const SkullPlate: React.FC<SkullState> = ({ringNasalAt, labelNasalAt, ringOrbitsAt, labelOrbitsAt, ghostAt, ghostOutAt, stamp, inset, zoom = [1, 1.03], dur = 5, k = 0.92}) => {
  const t = useT();
  const p = (a?: number, d = 0.7) => (a === undefined ? 0 : easeOut(ramp(t, a, a + d)));
  const ghost = ghostAt === undefined ? 0 : p(ghostAt, 0.5) * (ghostOutAt === undefined ? 1 : 1 - p(ghostOutAt, 0.4));
  const s = lerp(zoom[0], zoom[1], easeInOut(clamp01(t / dur)));
  const ox = 960 - 500 * k, oy = 40;
  const pulse = ringNasalAt === undefined ? 0 : ramp(t, ringNasalAt + 0.7, ringNasalAt + 1.7);
  return (
    <CardBg>
      <div style={{position: 'absolute', inset: 0, transformOrigin: '960px 440px', transform: `scale(${s})`}}>
        <SkullArt ox={ox} oy={oy} k={k} ringNasal={p(ringNasalAt)} pulse={pulse} labelNasal={p(labelNasalAt, 0.5)} ringOrbits={p(ringOrbitsAt)} labelOrbits={p(labelOrbitsAt, 0.5)} ghost={ghost} ghostLabel={ghost} />
      </div>
      <SkullNote t={t} />
      {stamp && <Stamp text={stamp.text} t={t} at={stamp.at} size={70} style={{left: 1230, top: 700}} />}
      {inset && <IslandInset t={t} />}
    </CardBg>
  );
};

/** small island-dot inset for shot 124 */
const IslandInset: React.FC<{t: number}> = ({t}) => {
  const dots: [number, number, string][] = [[0.18, 0.40, 'Sicily'], [0.20, 0.62, 'Malta'], [0.55, 0.62, 'Crete'], [0.62, 0.42, 'Tilos'], [0.9, 0.70, 'Cyprus']];
  return (
    <div style={{position: 'absolute', right: 84, top: 120, width: 520, height: 300, border: `2px solid ${C.lineStrong}`, background: '#0b1117', opacity: easeOut(ramp(t, 0.3, 0.8))}}>
      <svg width={520} height={300} viewBox="0 0 520 300" style={{fontFamily: FONT}}>
        {dots.map(([x, y, n], i) => (<g key={i} opacity={easeOut(ramp(t, 0.5 + i * 0.25, 0.9 + i * 0.25))}><circle cx={x * 520} cy={y * 300} r={9} fill={C.rustHi} /><text x={x * 520} y={y * 300 - 18} fill={C.paper} fontSize={22} textAnchor="middle" fontWeight={700}>{n}</text></g>))}
      </svg>
      <div style={{position: 'absolute', left: 14, bottom: 8, fontSize: 17, letterSpacing: 4, fontWeight: 700, color: C.muted}}>DWARF-ELEPHANT ISLANDS</div>
    </div>
  );
};

/** shot 6: skull plate beside a crop of the Cyclops eye */
export const SplitSkullEye: React.FC<{dur: number}> = ({dur}) => {
  const t = useT();
  const w = 760, h = 620;
  const u = easeOut(ramp(t, 0.5, 1.4));
  return (
    <CardBg>
      <div style={{position: 'absolute', left: 120, top: 150, width: w, height: h, border: `2px solid ${C.lineStrong}`, overflow: 'hidden', background: C.bg2, ...reveal(t, 0.2, 0.5, 0)}}>
        <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 940}}><SkullArt ox={w / 2 - 500 * 0.64} oy={(h - 850 * 0.64) / 2 - 20} k={0.64} /></div>
      </div>
      <div style={{position: 'absolute', left: 120, top: h + 170, width: w, textAlign: 'center', fontSize: 34, fontWeight: 700, color: C.paper, ...reveal(t, 0.5)}}>Elephant skull, front view<div style={{fontSize: 22, fontStyle: 'italic', color: C.muted, fontWeight: 400, marginTop: 6}}>illustration</div></div>
      <div style={{position: 'absolute', right: 120, top: 150, width: w, height: h, border: `2px solid ${C.lineStrong}`, overflow: 'hidden', opacity: u}}>
        <Img src={staticFile('img/NB01.jpg')} style={{position: 'absolute', width: 2304 * 1.12, height: 1296 * 1.12, left: w / 2 - 0.47 * 2304 * 1.12, top: h / 2 - 0.30 * 1296 * 1.12, filter: 'saturate(0.94) contrast(1.05)'}} />
      </div>
      <div style={{position: 'absolute', right: 120, top: h + 170, width: w, textAlign: 'center', fontSize: 34, fontWeight: 700, color: C.paper, opacity: u}}>Homer's Cyclops<div style={{fontSize: 22, fontStyle: 'italic', color: C.muted, fontWeight: 400, marginTop: 6}}>our artwork</div></div>
      <div style={{position: 'absolute', left: 960 - 38, top: 150 + h / 2 - 36, width: 76, textAlign: 'center', fontSize: 64, color: C.rustHi, fontWeight: 700, opacity: u}}>?</div>
    </CardBg>
  );
};

/* ------------------------------------------------------------------ pictogram cards */
const Wagon: React.FC<{x: number; y: number; o: number}> = ({x, y, o}) => (
  <g transform={`translate(${x} ${y})`} opacity={o}>
    <rect x={0} y={20} width={96} height={34} rx={4} fill="#7b6a4d" stroke={C.paper} strokeWidth={2.5} />
    <rect x={10} y={4} width={76} height={18} rx={3} fill="none" stroke={C.paper} strokeWidth={2.5} />
    <circle cx={16} cy={64} r={12} fill={C.bg} stroke={C.paper} strokeWidth={3} /><circle cx={34} cy={64} r={12} fill={C.bg} stroke={C.paper} strokeWidth={3} />
    <circle cx={62} cy={64} r={12} fill={C.bg} stroke={C.paper} strokeWidth={3} /><circle cx={80} cy={64} r={12} fill={C.bg} stroke={C.paper} strokeWidth={3} />
  </g>
);
export const WagonCount: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  const a = wordAt(t0, t1, 'twenty-two', 0, 1.2);
  const n = Math.min(22, Math.max(0, Math.floor((t - a) / 0.09) + 1));
  const rock = 'M260 700 C200 640 190 520 240 430 C290 330 400 280 520 300 C650 320 730 420 740 540 C750 650 690 740 580 770 C470 790 320 770 260 700Z';
  return (
    <CardBg>
      <svg width={1920} height={940} viewBox="0 0 1920 940" style={{position: 'absolute', left: 0, top: 0, fontFamily: FONT}}>
        <path d={rock} fill="#3a3226" stroke={C.paper} strokeWidth={4} opacity={easeOut(ramp(t, 0.2, 0.8))} />
        <path d="M330 420 C380 380 450 372 520 392 M300 540 C380 500 470 520 560 540 M360 660 C440 630 540 640 620 670" fill="none" stroke={C.dim} strokeWidth={3} opacity={easeOut(ramp(t, 0.2, 0.8))} />
        <text x={500} y={830} fill={C.muted} fontSize={30} textAnchor="middle" fontStyle="italic" opacity={easeOut(ramp(t, 0.4, 0.9))}>the stone at the cave mouth</text>
        {Array.from({length: 22}).map((_, i) => <Wagon key={i} x={880 + (i % 6) * 168} y={190 + Math.floor(i / 6) * 128} o={i < n ? 1 : 0.0} />)}
        {Array.from({length: 24 - 22}).map((_, i) => null)}
      </svg>
      <div style={{position: 'absolute', left: 880, top: 700, ...reveal(t, a, 0.4)}}>
        <span style={{fontSize: 120, fontWeight: 700, color: C.rustHi}}>{n}</span>
        <span style={{fontSize: 42, color: C.paper, marginLeft: 26}}>four-wheeled wagons</span>
        <div style={{fontSize: 28, fontStyle: 'italic', color: C.muted, marginTop: 4}}>could not have moved it (Odyssey 9)</div>
      </div>
    </CardBg>
  );
};

export const TallySix: React.FC = () => {
  const t = useT();
  const xs = [0, 1, 3, 4, 6, 7];
  return (
    <CardBg>
      <svg width={1920} height={940} viewBox="0 0 1920 940" style={{position: 'absolute', left: 0, top: 0}}>
        {xs.map((g, i) => { const u = easeOut(ramp(t, 0.5 + i * 0.28, 0.8 + i * 0.28)); const x = 520 + g * 120 + (g >= 3 ? 30 : 0) + (g >= 6 ? 30 : 0); return <line key={i} x1={x} x2={x} y1={250 + 300 * (1 - u)} y2={550} stroke={C.paper} strokeWidth={16} strokeLinecap="butt" opacity={0.95} />; })}
      </svg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 640, textAlign: 'center', fontFamily: FONT, fontSize: 40, color: C.muted, fontStyle: 'italic', ...reveal(t, 2.0)}}>six men, two at a time</div>
    </CardBg>
  );
};

export const MixCard: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  const a = wordAt(t0, t1, 'twenty', 0, 2.0);
  const water = Math.floor(clamp01((t - a) / 1.3) * 20);
  const cw = 76, x0 = 960 - (21 * cw) / 2;
  return (
    <CardBg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 160, textAlign: 'center'}}><Kicker>Odyssey 9: the wine</Kicker></div>
      <svg width={1920} height={940} viewBox="0 0 1920 940" style={{position: 'absolute', left: 0, top: 0, fontFamily: FONT}}>
        <path d="M760 310 L1160 310 C1150 430 1090 500 960 505 C830 500 770 430 760 310Z" fill="#2c2318" stroke={C.paper} strokeWidth={5} />
        <path d="M770 345 L1150 345 C1140 440 1085 490 960 495 C835 490 780 440 770 345Z" fill={C.rust} opacity={easeOut(ramp(t, 0.5, 1.2)) * 0.9} />
        <rect x={925} y={505} width={70} height={40} fill="#2c2318" stroke={C.paper} strokeWidth={4} /><path d="M860 560 L1060 560" stroke={C.paper} strokeWidth={6} />
        {Array.from({length: 21}).map((_, i) => <rect key={i} x={x0 + i * cw + 3} y={650} width={cw - 6} height={90} fill={i === 0 ? C.rust : '#5b7384'} opacity={i === 0 ? easeOut(ramp(t, 0.6, 1.0)) : (i <= water ? 1 : 0.14)} stroke={C.bg} strokeWidth={1} />)}
        <text x={x0 + cw / 2} y={792} fill={C.rustHi} fontSize={34} textAnchor="middle" fontWeight={700} opacity={easeOut(ramp(t, 0.8, 1.3))}>1</text>
        <text x={x0 + cw / 2} y={832} fill={C.paper} fontSize={28} textAnchor="middle" opacity={easeOut(ramp(t, 0.8, 1.3))}>wine</text>
        <text x={960 + cw / 2} y={792} fill={C.paper} fontSize={34} textAnchor="middle" fontWeight={700} opacity={easeOut(ramp(t, a, a + 0.5))}>20</text>
        <text x={960 + cw / 2} y={832} fill={C.paper} fontSize={28} textAnchor="middle" opacity={easeOut(ramp(t, a, a + 0.5))}>measures of water</text>
      </svg>
    </CardBg>
  );
};

/** shots 76-77: which came first? */
export const WhichFirst: React.FC<{t77: number}> = ({t77}) => {
  const t = useT();
  const sel = easeOut(ramp(t, t77, t77 + 0.6));
  const Row: React.FC<{y: number; from: string; to: string; at: number; hot: number; dimmed: number}> = ({y, from, to, at, hot, dimmed}) => {
    const col = hot > 0.5 ? C.rustHi : C.paper;
    const box = (x: number, text: string) => <div style={{position: 'absolute', left: x, top: 0, width: 400, height: 120, border: `3px solid ${hot > 0.5 ? C.rustHi : C.lineStrong}`, color: col, fontSize: 52, fontWeight: 700, letterSpacing: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'rgba(30,24,17,0.7)'}}>{text}</div>;
    return (
      <div style={{position: 'absolute', left: 0, top: y, width: 1920, height: 120, opacity: easeOut(ramp(t, at, at + 0.5)) * (1 - 0.62 * dimmed)}}>
        {box(300, from)}
        <svg width={420} height={120} viewBox="0 0 420 120" style={{position: 'absolute', left: 750, top: 0}}>
          <line x1={20} y1={60} x2={360} y2={60} stroke={col} strokeWidth={hot > 0.5 ? 9 : 5} />
          <path d="M338 36 L384 60 L338 84" fill="none" stroke={col} strokeWidth={hot > 0.5 ? 9 : 5} />
        </svg>
        {box(1220, to)}
      </div>
    );
  };
  return (
    <CardBg>
      <div style={{position: 'absolute', left: 0, right: 0, top: 160, textAlign: 'center'}}><Kicker>Which came first?</Kicker></div>
      <Row y={330} from="MYTH" to="BONES?" at={0.3} hot={sel} dimmed={0} />
      <Row y={540} from="BONES" to="MYTH?" at={0.9} hot={0} dimmed={sel} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 740, textAlign: 'center', fontSize: 34, fontStyle: 'italic', color: C.muted, opacity: easeOut(ramp(t, 1.8, 2.4))}}>Mayor: &ldquo;We don't know which comes first.&rdquo;</div>
    </CardBg>
  );
};

/* ------------------------------------------------------------------ image panels */
const Panel: React.FC<{img: string; x: number; y: number; w: number; h: number; focus: [number, number]; label: string; at: number; t: number; zoom?: number; sub?: string}> = ({img, x, y, w, h, focus, label, at, t, zoom = 1, sub}) => {
  const iw = h * (16 / 9) * zoom, ih = h * zoom;
  const left = Math.max(w - iw, Math.min(0, w / 2 - focus[0] * iw)), top = Math.max(h - ih, Math.min(0, h / 2 - focus[1] * ih));
  const u = easeOut(ramp(t, at, at + 0.5));
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, opacity: u}}>
      <div style={{width: w, height: h, overflow: 'hidden', border: `2px solid ${C.lineStrong}`, position: 'relative'}}>
        <Img src={staticFile(`img/${img}.jpg`)} style={{position: 'absolute', left, top, width: iw, height: ih, filter: 'saturate(0.93) contrast(1.04)'}} />
        <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(to bottom, rgba(0,0,0,0) 70%, rgba(0,0,0,0.5) 100%)'}} />
      </div>
      <div style={{marginTop: 18, fontFamily: FONT, fontSize: 38, fontWeight: 700, color: C.paper, textAlign: 'center'}}>{label}</div>
      {sub && <div style={{fontFamily: FONT, fontSize: 24, fontStyle: 'italic', color: C.muted, textAlign: 'center', marginTop: 4}}>{sub}</div>}
    </div>
  );
};
export const SplitTwo: React.FC = () => {
  const t = useT();
  return (<CardBg>
    <Panel img="RC02" x={150} y={150} w={780} h={600} focus={[0.5, 0.5]} label="The shepherd" sub="Homer" at={0.2} t={t} zoom={1.0} />
    <Panel img="NB22" x={990} y={150} w={780} h={600} focus={[0.5, 0.5]} label="The smith" sub="Hesiod" at={wordAt(0, 9, 'same', 0, 0.9)} t={t} zoom={1.0} />
    <div style={{position: 'absolute', left: 930, top: 400, width: 60, textAlign: 'center', fontFamily: FONT, fontSize: 56, fontWeight: 700, color: C.rustHi, opacity: easeOut(ramp(t, 1.2, 1.7))}}>=</div>
  </CardBg>);
};
export const ThreeCols: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  return (<CardBg>
    <div style={{position: 'absolute', left: 0, right: 0, top: 130, textAlign: 'center'}}><Kicker>Three stories, kept apart</Kicker></div>
    <Panel img="RC02" x={110} y={200} w={540} h={600} focus={[0.5, 0.5]} label="Shepherd" sub="Homer" at={0.5} t={t} zoom={1.0} />
    <Panel img="NB22" x={690} y={200} w={540} h={600} focus={[0.5, 0.5]} label="Smith" sub="Hesiod" at={1.4} t={t} zoom={1.0} />
    <Panel img="NBG07" x={1270} y={200} w={540} h={600} focus={[0.5, 0.5]} label="Wall-builders" sub="Pausanias" at={2.3} t={t} zoom={1.0} />
  </CardBg>);
};
export const FourPanel: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  const w = 740, h = 400;
  const at = [wordAt(t0, t1, 'Hesiod', 0, 0.3), wordAt(t0, t1, 'Homer', 0, 1.4), wordAt(t0, t1, 'volcano', 0, 2.6), Math.max(wordAt(t0, t1, 'Sicilian', 0, 3.3) + 0.9, 4.2)];
  const P: [string, string, number, number][] = [['NB22', "Hesiod's smiths", 240, 90], ['RC02', "Homer's shepherd", 1060, 90], ['NBG05', 'Sicilian tradition', 240, 520], ['NBG07', 'Walls you can touch', 1060, 520]];
  return (<CardBg tag={false}>
    {P.map(([img, label, x, y], i) => (
      <div key={i} style={{position: 'absolute', left: x - 60, top: y, width: w, opacity: easeOut(ramp(t, at[i], at[i] + 0.5))}}>
        <div style={{width: w, height: h, overflow: 'hidden', border: `2px solid ${i === 3 ? C.rust : C.lineStrong}`, position: 'relative'}}>
          <Img src={staticFile(`img/${img}.jpg`)} style={{width: w, height: h, objectFit: 'cover', filter: 'saturate(0.93) contrast(1.04)'}} />
          <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, padding: '28px 22px 12px', background: 'linear-gradient(to top, rgba(0,0,0,0.8), rgba(0,0,0,0))', fontFamily: FONT, fontSize: 34, fontWeight: 700, color: C.paper}}>{label}</div>
        </div>
      </div>
    ))}
  </CardBg>);
};

/* ------------------------------------------------------------------ paper scale chart (shots 2, 61, 62) and prop / cutout plates */
export const ScaleChart: React.FC<{mode: 'a' | 'zoom' | 'b'; dur: number}> = ({mode, dur}) => {
  const t = useT();
  const u = easeInOut(clamp01(t / dur));
  const S = mode === 'zoom' ? lerp(330, 118, u) : 330;
  const ground = mode === 'zoom' ? 800 : 860;
  const man = {h: 1.7 * S, w: 1.7 * S * dims.ody[0] / dims.ody[1]};
  const eH = (1.0 / 0.88) * 0.9 * S, eW = eH * dims.NP01[0] / dims.NP01[1];
  const gH = (4 / 0.88) * S, gW = gH * dims.NP01[0] / dims.NP01[1];
  const shoulderY = ground - 0.9 * S;
  const ue = easeOut(u); const gx = 680, ex = mode === 'zoom' ? lerp(900, 1340, ue) : 900, mx = mode === 'zoom' ? lerp(1500, 1580, ue) : 1500;
  const showBig = mode === 'zoom' ? easeOut((u - 0.84) / 0.12) : 0;
  return (
    <CardBg paper tag={false}>
      <svg width={1920} height={940} viewBox="0 0 1920 940" style={{position: 'absolute', left: 0, top: 0, fontFamily: FONT}}>
        <line x1={110} y1={ground} x2={1810} y2={ground} stroke={C.ink} strokeWidth={4} />
        {/* man, 1.7 m */}
        <image href={staticFile('img/ody.png')} x={mx - man.w / 2} y={ground - man.h} width={man.w} height={man.h} />
        <line x1={mx + man.w / 2 + 30} y1={ground - man.h} x2={mx + man.w / 2 + 30} y2={ground} stroke={C.ink} strokeWidth={3} />
        <line x1={mx + man.w / 2 + 18} y1={ground - man.h} x2={mx + man.w / 2 + 42} y2={ground - man.h} stroke={C.ink} strokeWidth={3} />
        <text x={mx + man.w / 2 + 52} y={ground - man.h / 2} fill={C.ink} fontSize={34} fontWeight={700}>1.7 m</text>
        <text x={mx + man.w / 2 + 52} y={ground - man.h / 2 + 34} fill="rgba(36,29,21,0.65)" fontSize={22} fontStyle="italic">a man</text>
        {/* dwarf elephant */}
        <image href={staticFile('img/NP01.png')} x={ex - eW / 2} y={ground - eH} width={eW} height={eH} />
        {(mode !== 'zoom' || u > 0.84) && <g opacity={mode === 'zoom' ? easeOut((u - 0.84) / 0.12) : easeOut(ramp(t, 0.4, 0.9))}>
          <line x1={ex - eW / 2 - 20} y1={shoulderY} x2={mode === 'b' ? mx - man.w / 2 : ex + eW / 2 + 20} y2={shoulderY} stroke={C.rust} strokeWidth={4} strokeDasharray="12 8" />
          {mode !== 'zoom' && <text x={ex - eW / 2 - 28} y={shoulderY - 10} fill={C.rust} fontSize={mode === 'zoom' ? 24 : 32} fontWeight={700} textAnchor="end">under 1 m at the shoulder</text>}
        </g>}
        {/* straight-tusked elephant, 4 m, appears in shot 61 */}
        {mode === 'zoom' && <g opacity={showBig}>
          <image href={staticFile('img/NP01.png')} x={gx - gW / 2} y={ground - gH} width={gW} height={gH} />
          <line x1={gx - gW / 2 - 24} y1={ground - 4 * S} x2={gx - gW / 2 - 24} y2={ground} stroke={C.ink} strokeWidth={3} />
          <line x1={gx - gW / 2 - 36} y1={ground - 4 * S} x2={gx - gW / 2 - 12} y2={ground - 4 * S} stroke={C.ink} strokeWidth={3} />
          <text x={gx} y={Math.max(ground - gH - 18, 100)} fill={C.ink} fontSize={38} fontWeight={700} textAnchor="middle">about 4 m</text>
          <text x={gx} y={ground + 46} fill="rgba(36,29,21,0.8)" fontSize={26} textAnchor="middle" fontStyle="italic">straight-tusked ancestor (same drawing, enlarged)</text>
        </g>}
        <text x={ex} y={ground + 46} fill="rgba(36,29,21,0.8)" fontSize={26} textAnchor="middle" fontStyle="italic" opacity={mode === 'zoom' ? easeOut((u - 0.84) / 0.12) : 1}>island dwarf elephant</text>
        <text x={1810} y={905} fill="rgba(36,29,21,0.6)" fontSize={20} textAnchor="end" fontStyle="italic">proportions simplified</text>
      </svg>
    </CardBg>
  );
};

/** prop or cutout alone on warm paper (shots 41, 42, 57) */
export const PaperProp: React.FC<{src: string; aspect: number; h: number; dur: number; ground?: number; line?: boolean}> = ({src, aspect, h, dur, ground = 560, line = false}) => {
  const t = useT();
  const s = lerp(1, 1.03, easeInOut(clamp01(t / dur)));
  return (
    <CardBg paper tag={false}>
      <div style={{position: 'absolute', inset: 0, transform: `scale(${s})`, transformOrigin: '960px 500px'}}>
        {line && <div style={{position: 'absolute', left: 150, right: 150, top: 890, height: 3, background: C.ink}} />}
        <Img src={staticFile(src)} style={{position: 'absolute', left: 960 - (h * aspect) / 2, top: line ? 890 - h : ground - h / 2, width: h * aspect, height: h}} />
      </div>
    </CardBg>
  );
};
export {SicilyInset};
