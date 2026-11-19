import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import timing from '../data/timing.json';
import {SHOTS, STILLS} from './shots3';
import {Captions, buildChunks, CapPos} from './lib/Captions';
import {useFonts, clamp01} from './lib/theme';

const T0 = timing.shots[4].start, T1 = timing.shots[9].end;
export const CLIP_DUR = T1 - T0;
const ids = SHOTS.map((s) => s.idx);
const sh = ids.map((i) => timing.shots[i]);
const chunks = buildChunks(timing.words, sh.map((s) => s.start), sh.map((s) => s.end));
const posAt = (t: number): CapPos => { const i = sh.findIndex((s) => t >= s.start && t < s.end); return i < 0 ? 'none' : SHOTS[i].cap; };
const voice: [number, number][] = [];
timing.paras.forEach((p) => { const a = p.start - 0.15, b = p.end + 0.3; if (voice.length && a - voice[voice.length - 1][1] < 0.6) voice[voice.length - 1][1] = b; else voice.push([a, b]); });
const duck = (t: number) => { let d = 9; for (const [a, b] of voice) d = Math.min(d, t < a ? a - t : t > b ? t - b : 0); return 1 - clamp01(d / 0.45); };

export const Clip: React.FC = () => {
  useFonts();
  const {fps} = useVideoConfig();
  const off = Math.round(T0 * fps);
  return (
    <AbsoluteFill style={{background: '#0d0a10'}}>
      <Sequence from={-off}>
        {sh.map((s, i) => {
          const from = Math.round(s.start * fps), end = Math.round(s.end * fps);
          return <Sequence key={i} from={from} durationInFrames={end - from} name={SHOTS[i].id}>{SHOTS[i].render(s.end - s.start)}</Sequence>;
        })}
        <Captions chunks={chunks} posAt={posAt} emph={[]} />
        {timing.paras.filter((p) => p.i >= 1 && p.i <= 3).map((p) => (
          <Sequence key={p.i} from={Math.round(p.offset * fps)}><Audio src={staticFile(`vo/vo_${p.i}.mp3`)} volume={1} /></Sequence>
        ))}
        <Audio src={staticFile('music/bed.wav')} volume={(f) => { const t = (f) / fps; return (0.16 + (0.06 - 0.16) * duck(t)) * clamp01((T1 + 1 - t) / 1.5); }} />
      </Sequence>
    </AbsoluteFill>
  );
};

export const StillComp: React.FC<{which: number}> = ({which}) => {
  useFonts();
  const {fps} = useVideoConfig();
  const st = STILLS[which];
  return <AbsoluteFill>{st.render(5)}</AbsoluteFill>;
};
