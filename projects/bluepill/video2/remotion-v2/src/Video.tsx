import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import TL from './timeline.json';
import {C, W, H, onPaint, HAND} from './lib/theme';
import {Fonts} from './lib/Fonts';
import {CodeMap, Route} from './lib/Maps';
import {routeProgress} from './lib/anim';
import {Label, Counter, Chip, Stamp, Bubble} from './lib/Text';
import {Board, BoardPing} from './lib/Board';
import {Sprite, spriteStates, headOf} from './lib/Sprite';

const EV = (TL as any).events as any[];
const ART = (TL as any).board;

/** background by shot.bg.type: img (painted plate, cover, no camera), white (class B gets the tinted ground), board, map (file or code map), black */
const Ground: React.FC<{shot: any}> = ({shot}) => {
  const bg = shot.bg;
  if (bg.type === 'white') return <AbsoluteFill style={{background: shot.class === 'B' ? C.ground : C.white}} />;
  if (bg.type === 'black') return <AbsoluteFill style={{background: C.black}} />;
  if (bg.type === 'map') {
    if (bg.asset && bg.asset.kind === 'file') return <Img src={staticFile(bg.asset.src)} style={{width: W, height: H, objectFit: 'cover'}} />;
    return <CodeMap mapId={(bg.src || 'map_med_west').replace(/\.png$/, '')} />;
  }
  if (bg.type === 'board') return null; // drawn by the Board component from the latest board state
  if (bg.asset && bg.asset.kind === 'file') return <Img src={staticFile(bg.asset.src)} style={{width: W, height: H, objectFit: 'cover'}} />;
  return (
    <AbsoluteFill style={{background: C.placeholder, alignItems: 'center', justifyContent: 'center'}}>
      <div style={{fontFamily: 'DejaVu Sans, sans-serif', fontSize: 64, color: '#222', border: '8px dashed #555', padding: 40}}>MISSING PLATE: {bg.src}</div>
    </AbsoluteFill>
  );
};

const Shot: React.FC<{shot: any}> = ({shot}) => {
  const {fps} = useVideoConfig();
  const f = useCurrentFrame();
  const t = shot.t0 + f / fps;
  const paint = onPaint(shot.bg.type);
  const evs = EV.filter((e) => e.shot === shot.id);
  const sprites = spriteStates(EV, shot.id, t);
  const mapId = shot.bg.type === 'map' ? (shot.bg.src || '').replace(/\.png$/, '') : 'map_med_west';
  // board: latest state event at or before t
  let boardState = 'empty', boardT = shot.t0;
  for (const e of evs) if (e.kind === 'label' && e.style === 'board' && t >= e.t && !e.state.startsWith('ping_')) { boardState = e.state; boardT = e.t; }
  const bubbleTarget = (e: any): [number, number] | undefined => {
    const live = sprites.filter((s) => !s.gone && !s.e.src.startsWith('prop__'));
    if (!live.length) return undefined;
    let best = live[0], bd = 1e9;
    for (const s of live) { const d = Math.abs(s.e.x - e.x); if (d < bd) { bd = d; best = s; } }
    return headOf(best);
  };
  return (
    <AbsoluteFill style={{background: C.white, overflow: 'hidden'}}>
      <Ground shot={shot} />
      {shot.bg.type === 'board' && <Board state={boardState} dt={t - boardT} art={ART} earned={shot.earned || []} frame={f} />}
      {sprites.map((s) => <Sprite key={s.e.i} s={s} t={t} />)}
      {evs.map((e, i) => {
        const dt = t - e.t;
        if (dt < 0) return null;
        switch (e.kind) {
          case 'route': return <Route key={i} e={e} mapId={mapId} prog={routeProgress(dt, e.dur)} />;
          case 'counter': return <Counter key={i} e={e} dt={dt} paint={paint} />;
          case 'label':
            if (e.style === 'board') return e.state.startsWith('ping_') ? <BoardPing key={i} state={e.state} dt={dt} art={ART} earned={shot.earned || []} /> : null;
            if (e.style === 'bubble') return <Bubble key={i} e={e} dt={dt} paint={paint} tailTo={bubbleTarget(e)} />;
            return <Label key={i} e={e} dt={dt} paint={paint} />;
          case 'chip': return <Chip key={i} e={e} dt={dt} />;
          case 'stamp': { // stamps placed under 700 px apart on one line (the three verdicts across the world map) drop to the small size so they do not overlap
            const crowded = evs.some((o) => o !== e && o.kind === 'stamp' && Math.abs(o.y - e.y) < 60 && Math.abs(o.x - e.x) < 700);
            return <Stamp key={i} e={e} dt={dt} paint={paint} size={crowded ? (e.sub ? 44 : 64) : undefined} />;
          }
          case 'bubble': return <Bubble key={i} e={e} dt={dt} paint={paint} tailTo={bubbleTarget(e)} />;
          default: return null; // sprite/swap handled below; sfx is an audio hook only
        }
      })}
    </AbsoluteFill>
  );
};

export const Video: React.FC<{withAudio?: boolean}> = ({withAudio = false}) => (
  <Fonts>
    <AbsoluteFill style={{background: C.white}}>
      {((TL as any).shots as any[]).map((s) => (
        <Sequence key={s.id} from={s.f0} durationInFrames={Math.max(1, s.f1 - s.f0)} name={s.id}>
          <Shot shot={s} />
        </Sequence>
      ))}
      {withAudio && <Audio src={staticFile('narration.wav')} />}
    </AbsoluteFill>
  </Fonts>
);
