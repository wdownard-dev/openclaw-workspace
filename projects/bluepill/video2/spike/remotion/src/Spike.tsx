import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import TL from '../tl.json';
import * as A from '../../common/anim.js';

const med = require('../../common/med.json');
const FONT: React.CSSProperties = {fontFamily: '"Fira Sans Condensed", sans-serif', fontWeight: 800, position: 'absolute', whiteSpace: 'nowrap', lineHeight: 1};

const Event: React.FC<{e: any; t: number}> = ({e, t}) => {
  const dt = t - e.t;
  if (dt < 0) return null;
  if (e.kind === 'sprite') {
    return <Img src={staticFile(e.src)} style={{position: 'absolute', left: e.x, top: e.y, height: e.h, transform: `translate(-50%,-100%) scale(${A.popScale(dt)})`, transformOrigin: '50% 100%'}} />;
  }
  if (e.kind === 'label' || e.kind === 'counter') {
    const text = e.kind === 'label' ? e.text : String(A.counterValue(dt, e.dur, e.from, e.to));
    const s = e.kind === 'label' ? A.popScale(dt) : 1;
    return <div style={{...FONT, left: e.x, top: e.y, fontSize: e.size, color: e.color, WebkitTextStroke: e.stroke ? `${e.size * 0.09}px ${e.stroke}` : undefined, paintOrder: 'stroke fill', transform: `translate(-50%,-50%) rotate(${e.rot || 0}deg) scale(${s})`}}>{text}</div>;
  }
  if (e.kind === 'route') {
    const p = A.routeProgress(dt, e.dur);
    return <svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0}} dangerouslySetInnerHTML={{__html: A.routeSvgInner(e, p) + A.arrowHead(e, p)}} />;
  }
  return null;
};

const Shot: React.FC<{shot: any}> = ({shot}) => {
  const {fps} = useVideoConfig();
  const t = shot.t0 + useCurrentFrame() / fps;
  const bg = shot.bg;
  return (
    <AbsoluteFill style={{background: '#fff'}}>
      {bg.type === 'map' && <Img src={staticFile('map.png')} />}
      {bg.type === 'img' && <Img src={staticFile(bg.src)} style={{width: 1920, height: 1080, objectFit: 'cover', transform: `scale(${1 + ((TL as any).kb || 0) * (t - shot.t0) / (shot.t1 - shot.t0)})`}} />}
      {(TL.events as any[]).filter((e) => e.shot === shot.id).map((e, i) => <Event key={i} e={e} t={t} />)}
    </AbsoluteFill>
  );
};

export const Spike: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      {(TL.shots as any[]).map((s) => (
        <Sequence key={s.id} from={Math.round(s.t0 * fps)} durationInFrames={Math.round(s.t1 * fps) - Math.round(s.t0 * fps)}><Shot shot={s} /></Sequence>
      ))}
      <Audio src={staticFile((TL as any).audio || 'narr20.mp3')} />
    </AbsoluteFill>
  );
};
