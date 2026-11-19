import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {C, FONT, clamp01, easeOut, ramp} from './theme';
import {CardBg, Grain, Kicker, Rule, Stamp, Tick, reveal, useT} from './ui';
import {wordAt} from './timing';

/** five chapter cards: numeral, rule, title; the card itself is cross-faded by Video.tsx */
export const ChapterCard: React.FC<{num: string; title: string}> = ({num, title}) => {
  const t = useT();
  return (
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 45%, ${C.bg2} 0%, ${C.bg} 60%, #0b0906 100%)`, fontFamily: FONT}}>
      <div style={{position: 'absolute', inset: 46, border: `1.5px solid ${C.line}`}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 215, textAlign: 'center', fontSize: 24, letterSpacing: 14, fontWeight: 700, color: C.muted, ...reveal(t, 0.1, 0.5, 0)}}>CHAPTER</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 255, textAlign: 'center', fontSize: 250, lineHeight: 1, fontWeight: 700, color: C.rust, ...reveal(t, 0.15, 0.5, 10)}}>{num}</div>
      <div style={{position: 'absolute', left: 960 - 300 * easeOut(ramp(t, 0.3, 0.9)), width: 600 * easeOut(ramp(t, 0.3, 0.9)), top: 575, height: 2, background: C.lineStrong}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 620, textAlign: 'center', fontSize: 96, fontWeight: 700, color: C.paper, letterSpacing: 2, ...reveal(t, 0.4, 0.55, 12)}}>{title}</div>
      <Grain alpha={0.05} />
    </AbsoluteFill>
  );
};

export type Line = {text: string; at?: number | string; size?: number; color?: string; italic?: boolean; bold?: boolean; gap?: number};
/** generic typographic card: kicker, big title, supporting lines */
export const NameCard: React.FC<{t0: number; t1: number; kicker?: string; title: string; titleSize?: number; italic?: boolean; lines?: Line[]; note?: string; top?: number; titleColor?: string}> = ({t0, t1, kicker, title, titleSize = 120, italic, lines = [], note, top = 300, titleColor = C.paper}) => {
  const t = useT();
  const at = (a: number | string | undefined, fb: number) => (typeof a === 'string' ? wordAt(t0, t1, a, 0, fb) : a ?? fb);
  return (
    <CardBg>
      <div style={{position: 'absolute', left: 150, right: 150, top: top - 90, textAlign: 'center', ...reveal(t, 0.15, 0.5, 0)}}>{kicker && <Kicker>{kicker}</Kicker>}</div>
      <div style={{position: 'absolute', left: 150, right: 150, top, textAlign: 'center', fontSize: titleSize, fontWeight: italic ? 400 : 700, fontStyle: italic ? 'italic' : 'normal', lineHeight: 1.12, color: titleColor, ...reveal(t, 0.3, 0.6, 14)}}>{title}</div>
      <div style={{position: 'absolute', left: 150, right: 150, top: top + titleSize * 1.12 * (title.length > 28 && titleSize > 90 ? 2 : 1) + 36, textAlign: 'center'}}>
        {lines.map((l, i) => (
          <div key={i} style={{fontSize: l.size ?? 42, color: l.color ?? C.muted, fontStyle: l.italic ? 'italic' : 'normal', fontWeight: l.bold ? 700 : 400, marginTop: l.gap ?? 16, lineHeight: 1.3, ...reveal(t, at(l.at, 0.9 + i * 0.7), 0.5, 10)}}>{l.text}</div>
        ))}
      </div>
      {note && <div style={{position: 'absolute', left: 84, bottom: 80, fontSize: 21, fontStyle: 'italic', color: C.dim, ...reveal(t, 1.0, 0.5, 0)}}>{note}</div>}
    </CardBg>
  );
};

export type Row = {label: string; value?: string; to?: string; sub?: string; mark?: 'tick' | 'blank' | 'dash' | 'dashrow'; at?: number | string; accent?: boolean; num?: string; dashed?: boolean; lateMark?: number};
/** ledger table: rows reveal in turn at spoken words */
export const Ledger: React.FC<{t0: number; t1: number; kicker?: string; title?: string; rows: Row[]; cols?: [string, string]; rowH?: number; top?: number; stamp?: {text: string; at: number | string; left?: number; top?: number}; labelSize?: number; footer?: string; hotAt?: number; labelW?: number}> = ({t0, t1, kicker, title, rows, cols, rowH = 128, top = 300, stamp, labelSize = 60, footer, hotAt, labelW = 900}) => {
  const t = useT();
  const at = (a: number | string | undefined, fb: number) => (typeof a === 'string' ? wordAt(t0, t1, a, 0, fb) : a ?? fb);
  const hot = hotAt === undefined ? 0 : easeOut(ramp(t, hotAt, hotAt + 0.5));
  return (
    <CardBg>
      {kicker && <div style={{position: 'absolute', left: 220, top: 160, ...reveal(t, 0.1, 0.5, 0)}}><Kicker>{kicker}</Kicker></div>}
      {title && <div style={{position: 'absolute', left: 220, top: 205, fontSize: 56, fontWeight: 700, color: C.paper, ...reveal(t, 0.2, 0.5, 0)}}>{title}</div>}
      <div style={{position: 'absolute', left: 220, right: 220, top: top - (cols ? 70 : 0)}}>
        {cols && (<div style={{display: 'flex', height: 60, borderBottom: `2px solid ${C.lineStrong}`, fontSize: 22, letterSpacing: 8, fontWeight: 700, color: hot > 0.5 ? C.rustHi : C.muted, opacity: easeOut(ramp(t, 0.1, 0.6))}}>
          <div style={{width: labelW}}>{cols[0]}</div><div style={{flex: 1, color: hot > 0.5 ? C.rustHi : C.muted}}>{cols[1]}</div></div>)}
        {rows.map((r, i) => {
          const a = at(r.at, 0.5 + i * 0.7);
          const col = r.accent ? C.rustHi : C.paper;
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', height: rowH, borderBottom: `1.5px ${r.dashed ? 'dashed' : 'solid'} ${r.dashed ? C.dim : C.line}`, ...reveal(t, a, 0.5, 12)}}>
              {r.num && <div style={{width: 110, fontSize: labelSize * 0.9, fontWeight: 700, color: C.rust}}>{r.num}</div>}
              <div style={{width: labelW - (r.num ? 110 : 0), fontSize: labelSize, fontWeight: 700, color: r.dashed ? C.muted : col, lineHeight: 1.1}}>
                {r.label}{r.sub && <div style={{fontSize: 27, fontWeight: 400, fontStyle: 'italic', color: C.muted, marginTop: 6}}>{r.sub}</div>}
              </div>
              {r.to !== undefined && (<div style={{display: 'flex', alignItems: 'center', fontSize: labelSize, fontWeight: 700, color: r.dashed ? C.muted : col}}>
                <svg width={150} height={40} viewBox="0 0 150 40" style={{marginRight: 26}}><line x1={4} y1={20} x2={120} y2={20} stroke={r.dashed ? C.dim : C.rustHi} strokeWidth={6} strokeDasharray={r.dashed ? '14 10' : undefined} /><path d="M104 6 L134 20 L104 34" fill="none" stroke={r.dashed ? C.dim : C.rustHi} strokeWidth={6} /></svg>{r.to}</div>)}
              {r.value !== undefined && <div style={{flex: 1, fontSize: labelSize * 0.9, fontWeight: 700, color: C.rustHi}}>{r.value}</div>}
              {r.mark === 'tick' && <div style={{flex: 1}}><Tick p={easeOut(ramp(t, a + 0.15, a + 0.55))} /></div>}
              {r.mark === 'dash' && <div style={{flex: 1, fontSize: labelSize * 0.85, color: C.muted, fontStyle: 'italic'}}>implied</div>}
              {r.mark === 'blank' && (<div style={{flex: 1}}><div style={{width: 340, height: 64, border: `2px dashed ${C.dim}`, position: 'relative'}}>
                {hot > 0 && <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', color: C.rustHi, fontSize: 40, fontWeight: 700, opacity: hot}}>none</div>}</div></div>)}
            </div>
          );
        })}
      </div>
      {stamp && <Stamp text={stamp.text} t={t} at={at(stamp.at, 1.5)} size={64} style={{left: stamp.left ?? 1040, top: stamp.top ?? 700}} />}
      {footer && <div style={{position: 'absolute', left: 220, bottom: 140, fontSize: 24, fontStyle: 'italic', color: C.dim, ...reveal(t, 1.2, 0.5, 0)}}>{footer}</div>}
    </CardBg>
  );
};

/** shot 121: two columns, SOLID / NOT SOLID */
export const SolidNot: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  const a = wordAt(t0, t1, 'solid', 0, 2.2);
  return (
    <CardBg>
      <div style={{position: 'absolute', left: 960, top: 190, width: 2, height: 640, background: C.line}} />
      <div style={{position: 'absolute', left: 150, width: 760, top: 300, textAlign: 'center', ...reveal(t, 0.3, 0.6)}}>
        <div style={{fontSize: 110, fontWeight: 700, color: C.paper, letterSpacing: 4}}>SOLID</div>
        <div style={{display: 'flex', justifyContent: 'center', marginTop: 24, opacity: easeOut(ramp(t, a, a + 0.4))}}><Tick size={90} p={easeOut(ramp(t, a, a + 0.6))} /></div>
      </div>
      <div style={{position: 'absolute', left: 1010, width: 760, top: 300, textAlign: 'center', ...reveal(t, 0.9, 0.6)}}>
        <div style={{fontSize: 110, fontWeight: 700, color: C.muted, letterSpacing: 4}}>NOT SOLID</div>
        <div style={{width: 200, height: 64, margin: '30px auto 0', border: `2px dashed ${C.dim}`}} />
      </div>
    </CardBg>
  );
};

export const EndCard: React.FC<{t0: number; t1: number}> = ({t0, t1}) => {
  const t = useT();
  return (
    <CardBg tag={false}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 150, textAlign: 'center', ...reveal(t, 0.2, 0.6, 0)}}><Kicker>Next time</Kicker></div>
      <div style={{position: 'absolute', left: 200, right: 200, top: 215, textAlign: 'center', fontSize: 70, fontWeight: 700, color: C.paper, lineHeight: 1.2, ...reveal(t, 0.4, 0.6, 12)}}>The winds, the witch, and the other monsters of the Odyssey</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 500, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 44, ...reveal(t, 1.0, 0.7, 10)}}>
        <Img src={staticFile('img/avatar.png')} style={{width: 190, height: 190, borderRadius: '50%', border: `3px solid ${C.lineStrong}`}} />
        <div>
          <div style={{fontSize: 92, fontWeight: 700, color: C.paper, letterSpacing: 4, lineHeight: 1}}>THE MYTH LEDGER</div>
          <div style={{fontSize: 34, fontStyle: 'italic', color: C.muted, marginTop: 16}}>Subscribe if you would like us to keep checking.</div>
        </div>
      </div>
      <Rule w={760} style={{position: 'absolute', left: 580, top: 760, opacity: easeOut(ramp(t, 1.4, 2))}} />
    </CardBg>
  );
};
