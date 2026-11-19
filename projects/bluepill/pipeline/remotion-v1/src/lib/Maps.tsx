import React, {useMemo} from 'react';
import {AbsoluteFill} from 'remotion';
import med from '../data/med.json';
import world from '../data/world.json';
import {C, FONT, clamp01, easeOut, easeInOut, lerp, ramp} from './theme';
import {CardBg, reveal, useT} from './ui';
import {wordAt} from './timing';

type LL = [number, number];
type BBox = [number, number, number, number];
const MED = med as unknown as number[][][];
const WORLD = world as unknown as number[][][];

const pip = (pt: LL, ring: number[][]) => {
  let c = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i], [xj, yj] = ring[j];
    if ((yi > pt[1]) !== (yj > pt[1]) && pt[0] < ((xj - xi) * (pt[1] - yi)) / (yj - yi) + xi) c = !c;
  }
  return c;
};

export const makeProj = (bbox: BBox, w: number, h: number) => {
  const [lo0, la0, lo1, la1] = bbox;
  const cosf = Math.cos((((la0 + la1) / 2) * Math.PI) / 180);
  const sy = Math.min(h / (la1 - la0), w / ((lo1 - lo0) * cosf));
  const sx = sy * cosf;
  const ox = (w - (lo1 - lo0) * sx) / 2, oy = (h - (la1 - la0) * sy) / 2;
  const P = (ll: LL): [number, number] => [ox + (ll[0] - lo0) * sx, oy + (la1 - ll[1]) * sy];
  return {P, sx, sy};
};

export type Hi = {pt: LL; at: number; fill?: string};

export const MapBase: React.FC<{data?: 'med' | 'world'; bbox: BBox; w: number; h: number; t: number; hi?: Hi[]; grat?: number; fill?: string; children?: (P: (ll: LL) => [number, number], t: number) => React.ReactNode; strokeW?: number; seaLabel?: {text: string; ll: LL; size?: number}}> = ({data = 'med', bbox, w, h, t, hi = [], grat = 5, fill = C.land, children, strokeW = 1.2, seaLabel}) => {
  const {P} = useMemo(() => makeProj(bbox, w, h), [bbox.join(','), w, h]);
  const rings = data === 'med' ? MED : WORLD;
  const paths = useMemo(() => rings.map((r) => {
    let d = '';
    r.forEach((p, i) => { const [x, y] = P(p as LL); d += (i ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1); });
    return d + 'Z';
  }), [data, bbox.join(','), w, h]);
  const hiIdx = useMemo(() => hi.map((hh) => rings.findIndex((r) => pip(hh.pt, r))), [data, hi.map((x) => x.pt.join()).join('|')]);
  const lines: React.ReactNode[] = [];
  for (let lo = Math.ceil(bbox[0] / grat) * grat; lo <= bbox[2]; lo += grat) { const [x] = P([lo, bbox[1]]); lines.push(<line key={'m' + lo} x1={x} x2={x} y1={0} y2={h} stroke="rgba(233,222,198,0.07)" strokeWidth={1} />); }
  for (let la = Math.ceil(bbox[1] / grat) * grat; la <= bbox[3]; la += grat) { const [, y] = P([bbox[0], la]); lines.push(<line key={'p' + la} x1={0} x2={w} y1={y} y2={y} stroke="rgba(233,222,198,0.07)" strokeWidth={1} />); }
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{position: 'absolute', left: 0, top: 0, fontFamily: FONT}}>
      <defs><linearGradient id={'sea' + w} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#121c24" /><stop offset="1" stopColor="#0b1117" /></linearGradient></defs>
      <rect width={w} height={h} fill={`url(#sea${w})`} />
      {lines}
      {paths.map((d, i) => <path key={i} d={d} fill={fill} stroke={C.coast} strokeWidth={strokeW} strokeLinejoin="round" />)}
      {hi.map((hh, k) => hiIdx[k] >= 0 && <path key={'h' + k} d={paths[hiIdx[k]]} fill={hh.fill ?? C.rust} fillOpacity={0.82 * easeOut(ramp(t, hh.at, hh.at + 0.6))} stroke={C.rustHi} strokeOpacity={easeOut(ramp(t, hh.at, hh.at + 0.6))} strokeWidth={strokeW * 1.6} strokeLinejoin="round" />)}
      {seaLabel && <text x={P(seaLabel.ll)[0]} y={P(seaLabel.ll)[1]} fill="rgba(233,222,198,0.22)" fontSize={seaLabel.size ?? 34} letterSpacing={14} textAnchor="middle" fontWeight={700}>{seaLabel.text}</text>}
      {children?.(P, t)}
    </svg>
  );
};

/** dot + label that fade in at `at` (seconds); no bounce */
export const Marker: React.FC<{P: (ll: LL) => [number, number]; ll: LL; t: number; at: number; label: string; dx?: number; dy?: number; anchor?: 'start' | 'middle' | 'end'; size?: number; r?: number; ring?: boolean; dot?: boolean}> = ({P, ll, t, at, label, dx = 18, dy = -14, anchor = 'start', size = 34, r = 9, ring = true, dot = true}) => {
  const u = easeOut(ramp(t, at, at + 0.4));
  const [x, y] = P(ll);
  const pu = ramp(t, at, at + 1.1);
  return (
    <g opacity={u}>
      {ring && <circle cx={x} cy={y} r={r + 26 * pu} fill="none" stroke={C.rustHi} strokeWidth={2} strokeOpacity={0.7 * (1 - pu)} />}
      {dot && <circle cx={x} cy={y} r={r} fill={C.rustHi} stroke={C.bg} strokeWidth={3} />}
      <text x={x + dx} y={y + dy} fill={C.paper} fontSize={size} fontWeight={700} textAnchor={anchor} stroke={C.bg} strokeWidth={8} strokeLinejoin="round" paintOrder="stroke">{label}</text>
    </g>
  );
};

const Label: React.FC<{P: (ll: LL) => [number, number]; ll: LL; text: string; size?: number; op?: number}> = ({P, ll, text, size = 24, op = 0.34}) => {
  const [x, y] = P(ll);
  return <text x={x} y={y} fill={`rgba(233,222,198,${op})`} fontSize={size} letterSpacing={6} textAnchor="middle" fontWeight={700}>{text}</text>;
};

const MapFrame: React.FC<{children: React.ReactNode; caption?: string}> = ({children, caption}) => (
  <AbsoluteFill style={{background: '#0b1117', fontFamily: FONT}}>
    {children}
    <div style={{position: 'absolute', inset: 46, border: `1.5px solid ${C.line}`, pointerEvents: 'none'}} />
    <div style={{position: 'absolute', left: 84, top: 70, fontSize: 19, letterSpacing: 6, color: C.muted, fontWeight: 700}}>THE MYTH LEDGER</div>
    {caption && <div style={{position: 'absolute', right: 84, top: 70, fontSize: 19, letterSpacing: 4, color: C.muted}}>{caption}</div>}
  </AbsoluteFill>
);
const noteStyle: React.CSSProperties = {position: 'absolute', right: 84, top: 110, fontSize: 18, color: C.dim, fontStyle: 'italic'};

const SCALE = (z0: number, z1: number, dur: number, t: number, o: [number, number]) => {
  const s = lerp(z0, z1, easeInOut(clamp01(t / dur)));
  return {transform: `scale(${s})`, transformOrigin: `${o[0]}px ${o[1]}px`} as React.CSSProperties;
};

/** Mediterranean with Sicily highlighted; slow push toward Sicily */
export const MedMap: React.FC<{dur: number; z0?: number; z1?: number; t0?: number; t1?: number}> = ({dur, z0 = 1.0, z1 = 1.14}) => {
  const t = useT();
  const bbox: BBox = [-8, 29.5, 37, 46.5];
  const {P} = makeProj(bbox, 1920, 1080);
  const sic = P([14.1, 37.5]);
  return (
    <MapFrame caption="THE MEDITERRANEAN">
      <div style={{position: 'absolute', inset: 0, ...SCALE(z0, z1, dur, t, sic)}}>
        <MapBase bbox={bbox} w={1920} h={1080} t={t} hi={[{pt: [14.1, 37.5], at: 0.5}]} seaLabel={{text: 'MEDITERRANEAN SEA', ll: [18.5, 34.3], size: 30}}>
          {(P2, tt) => (<>
            <Label P={P2} ll={[2, 40.6]} text="SPAIN" /> <Label P={P2} ll={[12.5, 42.9]} text="ITALY" size={20} /> <Label P={P2} ll={[22.5, 39.8]} text="GREECE" /> <Label P={P2} ll={[28.8, 38.9]} text="TURKEY" /> <Label P={P2} ll={[16, 31.6]} text="LIBYA" /> <Label P={P2} ll={[9.2, 33.2]} text="TUNISIA" size={20} />
            <Marker P={P2} ll={[14.1, 37.5]} t={tt} at={0.9} label="SICILY" dx={22} dy={-18} size={40} r={0} dot={false} />
          </>)}
        </MapBase>
      </div>
    </MapFrame>
  );
};

export const DwarfMap: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  const bbox: BBox = [9, 31.2, 37.5, 40.2];
  const isl: {n: string; ll: LL; w: string; dx?: number; dy?: number; a?: 'start' | 'middle' | 'end'}[] = [
    {n: 'Sicily', ll: [14.1, 37.5], w: 'Sicily', dx: -18, dy: -22, a: 'end'}, {n: 'Malta', ll: [14.4, 35.9], w: 'Malta', dx: 20, dy: 40}, {n: 'Crete', ll: [24.9, 35.25], w: 'Crete', dx: 0, dy: 52, a: 'middle'},
    {n: 'Tilos (Aegean)', ll: [27.37, 36.43], w: 'Aegean', dx: 4, dy: -26, a: 'middle'}, {n: 'Cyprus', ll: [33.2, 35.0], w: 'Cyprus', dx: 0, dy: 56, a: 'middle'}];
  const dotAt = (i: number) => 1.0 + i * 0.75;
  const mid = (t1 - t0);
  const labAt = isl.map((x, i) => wordAt(t0, t1, x.w, 0, dotAt(i)));
  const links: [number, number][] = [[0, 1], [1, 2], [2, 3], [3, 4]];
  return (
    <MapFrame caption="DWARF ELEPHANTS OF THE ICE AGE">
      <MapBase bbox={bbox} w={1920} h={1080} t={t} grat={5}>
        {(P, tt) => (<>
          {links.map(([a, b], k) => {
            const [x1, y1] = P(isl[a].ll), [x2, y2] = P(isl[b].ll);
            const L = Math.hypot(x2 - x1, y2 - y1); const u = ramp(tt, Math.max(labAt[b], dotAt(b)) - 0.2, Math.max(labAt[b], dotAt(b)) + 0.7);
            return <line key={k} x1={x1} y1={y1} x2={x2} y2={y2} stroke={C.rustHi} strokeWidth={2.5} strokeDasharray="10 9" strokeDashoffset={0} opacity={0.75} style={{strokeDasharray: `${L * u} ${L}`}} />;
          })}
          {isl.map((x, i) => <Marker key={i} P={P} ll={x.ll} t={tt} at={Math.min(dotAt(i), labAt[i])} label={i === 3 ? 'Aegean islands' : x.n.split(' ')[0]} dx={x.dx} dy={x.dy} anchor={x.a} size={36} r={i === 3 ? 7 : 11} />)}
          <Label P={P} ll={[19, 33.2]} text="MEDITERRANEAN SEA" size={26} op={0.2} />
        </>)}
      </MapBase>
      <div style={noteStyle}>Fossil sites on islands; positions approximate</div>
    </MapFrame>
  );
};

export const EtnaMap: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  const bbox: BBox = [11.8, 36.2, 17.2, 39.2];
  const aeoAt = wordAt(t0, t1, 'Virgil', 0, 2.0), etnaAt = wordAt(t0, t1, 'Etna', 0, 5.0);
  return (
    <MapFrame caption="SICILY AND THE AEOLIAN ISLANDS">
      <MapBase bbox={bbox} w={1920} h={1080} t={t} hi={[{pt: [14.1, 37.5], at: 0.3, fill: '#4a3a2a'}]} grat={2}>
        {(P, tt) => (<>
          <Label P={P} ll={[13.4, 37.2]} text="SICILY" size={34} op={0.55} />
          <Marker P={P} ll={[14.99, 37.75]} t={tt} at={etnaAt} label="Mount Etna" dx={-24} dy={8} anchor="end" size={38} r={12} />
          <Marker P={P} ll={[14.95, 38.45]} t={tt} at={aeoAt} label="Lipari, Vulcano" dx={26} dy={-8} size={36} r={9} />
          <Marker P={P} ll={[15.21, 38.79]} t={tt} at={aeoAt + 0.4} label="Stromboli" dx={24} dy={10} size={28} r={6} ring={false} />
          <Label P={P} ll={[13.2, 38.9]} text="TYRRHENIAN SEA" size={22} op={0.2} />
        </>)}
      </MapBase>
      <div style={noteStyle}>Aeolian Islands: Thucydides' forge belief (6.2)</div>
    </MapFrame>
  );
};

export const ArgolidMap: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  const bbox: BBox = [21.95, 37.22, 23.65, 38.02];
  const sites: {n: string; ll: LL; at: number; dx: number; dy: number; a: 'start' | 'end' | 'middle'}[] = [
    {n: 'Mycenae', ll: [22.756, 37.730], at: 0.4, dx: 24, dy: -20, a: 'start'}, {n: 'Tiryns', ll: [22.800, 37.600], at: 1.3, dx: 26, dy: 10, a: 'start'}, {n: 'Argos', ll: [22.730, 37.632], at: 2.2, dx: -26, dy: 12, a: 'end'}];
  return (
    <MapFrame caption="THE ARGOLID, GREECE">
      <MapBase bbox={bbox} w={1920} h={1080} t={t} grat={0.5}>
        {(P, tt) => (<>
          <Label P={P} ll={[22.88, 37.43]} text="GULF OF ARGOLIS" size={24} op={0.25} />
          {sites.map((s, i) => <Marker key={i} P={P} ll={s.ll} t={tt} at={s.at} label={s.n} dx={s.dx} dy={s.dy} anchor={s.a} size={42} r={12} />)}
        </>)}
      </MapBase>
      <div style={noteStyle}>Bronze Age walls: the style archaeologists call cyclopean</div>
    </MapFrame>
  );
};

export const WorldPair: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  const bbox: BBox = [-170, -56, 180, 80];
  return (
    <MapFrame caption="A WORLD-WIDE PATTERN">
      <div style={{position: 'absolute', left: 0, top: 30, width: 1920, height: 900}}>
        <MapBase data="world" bbox={bbox} w={1920} h={900} t={t} grat={30} fill="#2a241b" strokeW={1}>{() => null}</MapBase>
      </div>
      <div style={{position: 'absolute', left: 190, top: 330, ...reveal(t, wordAt(t0, t1, 'Elephant', 0, 0.3), 0.5)}}>
        <div style={{fontSize: 58, fontWeight: 700, color: C.paper, background: 'rgba(14,11,8,0.82)', border: `2px solid ${C.lineStrong}`, padding: '14px 36px'}}>Elephant fossils</div>
      </div>
      <div style={{position: 'absolute', right: 190, top: 560, ...reveal(t, wordAt(t0, t1, 'one-eyed', 0, 1.6), 0.5)}}>
        <div style={{fontSize: 58, fontWeight: 700, color: C.paper, background: 'rgba(14,11,8,0.82)', border: `2px solid ${C.rust}`, padding: '14px 36px'}}>One-eyed monsters</div>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 460, textAlign: 'center', fontSize: 34, letterSpacing: 8, fontWeight: 700, color: C.rustHi, ...reveal(t, wordAt(t0, t1, 'world', 0, 3.0), 0.6)}}>ALL OVER THE WORLD</div>
    </MapFrame>
  );
};

export const FolkMap: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  const bbox: BBox = [-170, -56, 180, 80];
  const pts: {n: string; ll: LL; dx?: number; dy?: number; a?: 'start' | 'end' | 'middle'}[] = [
    {n: 'Iceland', ll: [-19, 65], dx: -4, dy: -22, a: 'middle'}, {n: 'Britain and Ireland', ll: [-3.5, 54], dx: -22, dy: -14, a: 'end'}, {n: 'Portugal', ll: [-8, 39.6], dx: -22, dy: 30, a: 'end'},
    {n: 'Africa', ll: [20, 3], dx: 0, dy: 50, a: 'middle'}, {n: 'Turkey', ll: [34, 39.2], dx: 4, dy: 48, a: 'middle'}, {n: 'Russia', ll: [60, 61], dx: 0, dy: -24, a: 'middle'},
    {n: 'Arabia', ll: [45, 24], dx: 4, dy: 48, a: 'middle'}, {n: 'Korea', ll: [127.5, 37], dx: -4, dy: 50, a: 'middle'}];
  const base = wordAt(t0, t1, 'Scholars', 0, 1.0);
  const counterAt = wordAt(t0, t1, 'two', 0, 2.8);
  const cu = easeOut(ramp(t, counterAt, counterAt + 1.4));
  return (
    <MapFrame caption="THE BLINDING FOLKTALE">
      <div style={{position: 'absolute', left: 0, top: 30, width: 1920, height: 900}}>
        <MapBase data="world" bbox={bbox} w={1920} h={900} t={t} grat={30} fill="#2a241b" strokeW={1}>
          {(P, tt) => pts.map((p, i) => <Marker key={i} P={P} ll={p.ll} t={tt} at={base + i * 0.45} label={p.n} dx={p.dx} dy={p.dy} anchor={p.a} size={30} r={9} />)}
        </MapBase>
      </div>
      <div style={{position: 'absolute', left: 120, bottom: 120, opacity: easeOut(ramp(t, counterAt - 0.1, counterAt + 0.4)), background: 'rgba(14,11,8,0.86)', border: `2px solid ${C.rust}`, padding: '10px 36px 14px', fontFamily: FONT}}>
        <span style={{fontSize: 92, fontWeight: 700, color: C.rustHi}}>{Math.round(200 * cu)}{cu >= 0.999 ? '+' : ''}</span>
        <span style={{fontSize: 34, color: C.paper, marginLeft: 22}}>versions of the tale</span>
      </div>
      <div style={noteStyle}>Regional markers only; not exact sites</div>
    </MapFrame>
  );
};

/** small inset on a picture shot */
export const SicilyInset: React.FC<{t: number}> = ({t}) => {
  const w = 600, h = 430;
  return (
    <div style={{position: 'absolute', right: 84, top: 84, width: w, height: h, border: `2px solid ${C.lineStrong}`, background: '#0b1117', overflow: 'hidden', opacity: easeOut(ramp(t, 0.5, 1.0)), fontFamily: FONT}}>
      <MapBase bbox={[14.2, 36.7, 16.2, 38.4]} w={w} h={h} t={t} grat={1} strokeW={1.6}>
        {(P, tt) => (<>
          <Marker P={P} ll={[15.16, 37.56]} t={tt} at={1.2} label="Aci Trezza" dx={-22} dy={-16} anchor="end" size={34} r={9} />
          <Label P={P} ll={[15.0, 37.9]} text="ETNA" size={20} op={0.35} />
        </>)}
      </MapBase>
      <div style={{position: 'absolute', left: 14, bottom: 10, fontSize: 18, letterSpacing: 4, fontWeight: 700, color: C.muted}}>EASTERN SICILY</div>
    </div>
  );
};
