import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import timing from '../data/timing.json';
import {SHOTS, Trans} from './shots';
import {Captions, buildChunks, CapPos} from './lib/Captions';
import {Sfx} from './lib/Scene';
import {useFonts, easeOut, clamp01} from './lib/theme';

const T = 7; // frames a transition takes
const EMPH = ['six', 'mistake', 'boulder', 'wine', 'nobody', 'blind', 'pride', 'polyphemus', 'wagons', 'stake', 'underneath', 'haunt', 'real', 'twelve'];

const shots = timing.shots;
const chunks = buildChunks(timing.words, shots.map((s) => s.start), shots.map((s) => s.end));
const posAt = (t: number): CapPos => { const i = shots.findIndex((s) => t >= s.start && t < s.end); return i < 0 ? 'none' : SHOTS[i].cap; };

// voice-activity intervals for music ducking
const voice: [number, number][] = [];
timing.paras.forEach((p) => { const a = p.start - 0.15, b = p.end + 0.3; if (voice.length && a - voice[voice.length - 1][1] < 0.6) voice[voice.length - 1][1] = b; else voice.push([a, b]); });
const duck = (t: number) => {
  let d = 9;
  for (const [a, b] of voice) d = Math.min(d, t < a ? a - t : t > b ? t - b : 0);
  return 1 - clamp01(d / 0.45); // 1 = voice present
};
const MUSIC_BASE = 0.34, MUSIC_DUCK = 0.12;

const TransWrap: React.FC<{kind: Trans; children: React.ReactNode}> = ({kind, children}) => {
  const f = useCurrentFrame();
  if (kind === 'cut') return <>{children}</>;
  const u = clamp01(f / T);
  if (kind === 'whip') {
    const e = easeOut(u);
    return <AbsoluteFill style={{transform: `translateX(${(1 - e) * 100}%)`, filter: u < 1 ? `blur(${(1 - e) * 14}px)` : undefined}}>{children}</AbsoluteFill>;
  }
  if (kind === 'fade') return <AbsoluteFill style={{opacity: clamp01(f / 10)}}>{children}</AbsoluteFill>;
  // flash: white pop over the incoming shot
  return <AbsoluteFill>{children}<AbsoluteFill style={{background: '#fff', opacity: 1 - clamp01(f / 6)}} /></AbsoluteFill>;
};

export const Video: React.FC = () => {
  useFonts();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: '#0d0a10'}}>
      {shots.map((s, i) => {
        const from = Math.round(s.start * fps), end = Math.round(s.end * fps);
        const next = SHOTS[i + 1]?.trans;
        const extra = next === 'whip' || next === 'fade' ? T + 3 : 0; // outgoing shot stays under the incoming one while it slides/fades in
        const def = SHOTS[i];
        return (
          <Sequence key={i} from={from} durationInFrames={end - from + extra} name={def.id}>
            <TransWrap kind={def.trans}>{def.render(s.end - s.start)}</TransWrap>
            {def.trans === 'whip' && <Sfx cues={[{at: 0, sfx: 'whoosh', vol: 0.55}]} />}
            {def.trans === 'fade' && i !== 2 && <Sfx cues={[{at: 0, sfx: 'whoosh', vol: 0.3}]} />}
          </Sequence>
        );
      })}
      <Captions chunks={chunks} posAt={posAt} emph={EMPH} />
      {timing.paras.map((p) => (
        <Sequence key={p.i} from={Math.round(p.offset * fps)}><Audio src={staticFile(`vo/vo_${p.i}.mp3`)} volume={1} /></Sequence>
      ))}
      <Audio src={staticFile('music/bed.wav')} volume={(f) => { const t = f / fps; return (MUSIC_BASE + (MUSIC_DUCK - MUSIC_BASE) * duck(t)) * clamp01((timing.duration - t) / 2.5); }} />
    </AbsoluteFill>
  );
};
