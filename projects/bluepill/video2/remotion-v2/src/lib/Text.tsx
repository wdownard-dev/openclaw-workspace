import React from 'react';
import {C, HAND, TYPE, SZ, W, H} from './theme';
import {popScale, stampScale, counterValue, tiltOf} from './anim';

const base: React.CSSProperties = {position: 'absolute', whiteSpace: 'nowrap', lineHeight: 1, fontFamily: HAND, textAlign: 'center'};
/** cream with an ink outline on paint; solid ink blue on white */
const fillFor = (paint: boolean, size: number, color?: string): React.CSSProperties => paint
  ? {color: C.cream, WebkitTextStroke: `${size * 0.1}px ${C.outline}`, paintOrder: 'stroke fill'} as any
  : {color: color || C.ink};

/** Impact / place / title / crossout labels. Centre-anchored at (x,y). */
export const Label: React.FC<{e: any; dt: number; paint: boolean}> = ({e, dt, paint}) => {
  if (dt < 0 || (e.dur && dt > e.dur)) return null;
  const size = e.size || SZ.impact;
  const st = e.style;
  const sc = popScale(dt);
  if (st === 'crossout') {
    const s = size;
    return <svg width={s * 1.3} height={s} style={{position: 'absolute', left: e.x - s * 0.65, top: e.y - s / 2, transform: `scale(${sc})`}} viewBox="0 0 130 100"><g stroke={C.gold} strokeWidth={16} strokeLinecap="round"><path d="M12 10 Q70 45 118 90" fill="none" /><path d="M118 10 Q70 55 12 90" fill="none" /></g></svg>;
  }
  if (st === 'chip_title') { // suspect title riding at the top centre for its dur, typewriter in a verdigris pill
    return <div style={{...base, fontFamily: TYPE, left: e.x, top: e.y, fontSize: size, color: C.cream, background: C.verd, padding: `${size * 0.25}px ${size * 0.6}px`, borderRadius: size, transform: `translate(-50%,-50%) scale(${sc})`}}>{e.text}</div>;
  }
  let fill: React.CSSProperties;
  if (st === 'title') fill = {color: C.cream};
  else if (st === 'place') fill = paint ? fillFor(true, size) : {color: C.verd};
  else fill = fillFor(paint, size);
  const rot = st === 'impact' ? tiltOf(e.text) : 0;
  return <div style={{...base, left: e.x, top: e.y, fontSize: size, ...fill, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(${sc})`}}>{e.text}</div>;
};

/** Counter: big number, unit word under it (or inline for ': 1', '+ VERSIONS', 'BC'); ticks in 15 fps steps. */
export const Counter: React.FC<{e: any; dt: number; paint: boolean}> = ({e, dt, paint}) => {
  if (dt < 0) return null;
  const v = counterValue(dt, e.dur, e.from, e.to);
  const size = e.size || 220;
  const unit: string = e.unit || '';
  const inline = /^:/.test(unit) || unit === 'BC'; // '20 : 1' and '700 BC' read inline; word units ('MEN', '+ VERSIONS') sit under the number
  const sc = e.from === e.to ? popScale(dt) : 1;
  const numStyle = fillFor(paint, size);
  const unitStyle: React.CSSProperties = paint ? fillFor(true, size * 0.45) : {color: C.verd};
  return (
    <div style={{...base, left: e.x, top: e.y, transform: `translate(-50%,-50%) scale(${sc})`}}>
      <div style={{fontSize: size, ...numStyle}}>{v}{inline && unit ? <span style={{fontSize: size * 0.55, marginLeft: size * 0.12, ...(paint ? fillFor(true, size * 0.55) : {color: C.verd})}}>{unit}</span> : null}</div>
      {!inline && unit ? <div style={{fontSize: size * 0.45, marginTop: size * 0.08, ...unitStyle}}>{unit}</div> : null}
    </div>
  );
};

/** Source chip: typewriter face in a verdigris pill, fixed bottom-left corner (60 px margins), 2.5 s. Long chips wrap to two lines. */
export const Chip: React.FC<{e: any; dt: number}> = ({e, dt}) => {
  if (dt < 0 || dt > (e.dur || 2.5)) return null;
  const size = SZ.chip;
  const lines = wrap(e.text, 40);
  const right = e.corner && e.corner.includes('right');
  const top = e.corner && e.corner.includes('top');
  return (
    <div style={{position: 'absolute', [right ? 'right' : 'left']: 60, [top ? 'top' : 'bottom']: 60, fontFamily: TYPE, fontSize: size, lineHeight: 1.15, color: C.cream, background: C.verd, padding: `${size * 0.3}px ${size * 0.7}px`, borderRadius: size * 1.2, whiteSpace: 'nowrap', transform: `scale(${popScale(dt)})`, transformOrigin: `${right ? '100%' : '0%'} ${top ? '0%' : '100%'}`}}>
      {lines.map((l, i) => <div key={i}>{l}</div>)}
    </div>
  );
};
export const wrap = (text: string, maxChars: number): string[] => {
  const words = text.split(' '), out: string[] = []; let cur = '';
  for (const w of words) { if (cur && (cur + ' ' + w).length > maxChars) { out.push(cur); cur = w; } else cur = cur ? cur + ' ' + w : w; }
  if (cur) out.push(cur);
  return out;
};

/** Rubber stamp: deep gold, double rounded border, rotated 3-6 deg, 0.2 s slam; 85% cream halo over paint. */
export const Stamp: React.FC<{e: any; dt: number; paint: boolean; size?: number}> = ({e, dt, paint, size}) => {
  if (dt < 0) return null;
  const lines: string[] = e.sub ? [e.text, e.sub] : [e.text];
  const sz = size || (lines.length > 1 ? SZ.stampSmall : SZ.stamp);
  const rot = e.rot ?? -4;
  const sc = stampScale(dt);
  const op = dt < 0.2 ? 0.55 + 0.45 * (dt / 0.2) : 1;
  return (
    <div style={{position: 'absolute', left: e.x, top: e.y, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(${sc})`, opacity: op}}>
      <div style={{padding: `${sz * 0.22}px ${sz * 0.45}px`, borderRadius: sz * 0.22, background: paint ? 'rgba(243,233,210,0.85)' : 'transparent'}}>
        <div style={{border: `${sz * 0.09}px solid ${C.gold}`, borderRadius: sz * 0.18, padding: sz * 0.04}}>
          <div style={{border: `${sz * 0.035}px solid ${C.gold}`, borderRadius: sz * 0.12, padding: `${sz * 0.12}px ${sz * 0.35}px`, fontFamily: HAND, fontSize: sz, lineHeight: 1.05, color: C.gold, textAlign: 'center', whiteSpace: 'nowrap', opacity: 0.93}}>
            {lines.map((l, i) => <div key={i}>{l}</div>)}
          </div>
        </div>
      </div>
    </div>
  );
};

/** Bubble: hand-lettered line(s), no box, a thin curved tail toward the speaker's head. Breaks after 4 words. */
export const Bubble: React.FC<{e: any; dt: number; paint: boolean; tailTo?: [number, number]}> = ({e, dt, paint, tailTo}) => {
  if (dt < 0 || (e.dur && dt > e.dur)) return null;
  const size = e.size || SZ.bubble;
  const words = e.text.split(' ');
  const lines: string[] = [];
  for (let i = 0; i < words.length; i += 4) lines.push(words.slice(i, i + 4).join(' '));
  const sc = popScale(dt);
  const fill = paint ? fillFor(true, size) : {color: C.ink};
  const h = lines.length * size * 1.1;
  let tail: React.ReactNode = null;
  if (tailTo) {
    const sx = e.x + (tailTo[0] < e.x ? -size * 1.2 : size * 1.2), sy = e.y + h / 2 + size * 0.1;
    const cx = (sx + tailTo[0]) / 2 + (tailTo[0] < e.x ? -size : size) * 0.8, cy = sy + (tailTo[1] - sy) * 0.3;
    tail = <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none'}}><path d={`M${sx} ${sy} Q${cx} ${cy} ${tailTo[0]} ${tailTo[1]}`} fill="none" stroke={paint ? C.cream : C.ink} strokeWidth={paint ? 7 : 4} strokeLinecap="round" />{paint && <path d={`M${sx} ${sy} Q${cx} ${cy} ${tailTo[0]} ${tailTo[1]}`} fill="none" stroke={C.outline} strokeWidth={3} strokeLinecap="round" />}</svg>;
  }
  return (
    <div style={{position: 'absolute', left: 0, top: 0, transform: `scale(${sc})`, transformOrigin: `${e.x}px ${e.y}px`}}>
      {tail}
      <div style={{...base, left: e.x, top: e.y, fontSize: size, lineHeight: 1.1, ...fill, transform: 'translate(-50%,-50%) rotate(-1.5deg)'}}>{lines.map((l, i) => <div key={i}>{l}</div>)}</div>
    </div>
  );
};
