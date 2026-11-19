import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import timing from '../data/timing.json';

const FADE = 9;
// per-shot camera moves: [startScale, endScale, startX, endX, startY, endY] in px
const MOVES: number[][] = [
  [1.04, 1.16, -20, 30, 0, -10],
  [1.16, 1.04, 30, -20, -10, 0],
  [1.05, 1.17, 0, 0, 10, -10],
  [1.12, 1.04, -30, 20, 0, 0],
  [1.04, 1.16, 30, -30, 10, -10],
  [1.15, 1.04, 0, 30, -10, 10],
];

const Shot: React.FC<{image: string; index: number; frames: number}> = ({image, index, frames}) => {
  const f = useCurrentFrame();
  const m = MOVES[index % MOVES.length];
  const t = interpolate(f, [0, frames], [0, 1], {easing: Easing.inOut(Easing.ease), extrapolateRight: 'clamp'});
  const lerp = (a: number, b: number) => a + (b - a) * t;
  const opacity = interpolate(f, [0, FADE], [index === 0 ? 1 : 0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity, overflow: 'hidden', background: '#111'}}>
      <Img src={staticFile(image)} style={{
        width: '100%', height: '100%', objectFit: 'cover',
        transform: `translate(${lerp(m[2], m[3])}px, ${lerp(m[4], m[5])}px) scale(${lerp(m[0], m[1])})`,
      }} />
    </AbsoluteFill>
  );
};

// Fixed caption chunks (max 3 words, break at punctuation) so the text never slides or re-wraps while a chunk is on screen.
const MAX_WORDS = 3;
const CHUNKS = (() => {
  const out: {from: number; to: number; words: typeof timing.words}[] = [];
  let cur: typeof timing.words = [];
  timing.words.forEach((w, i) => {
    cur.push(w);
    const last = i === timing.words.length - 1;
    if (cur.length >= MAX_WORDS || /[.,!?]$/.test(w.text) || last) {
      out.push({from: cur[0].start, to: cur[cur.length - 1].end, words: cur});
      cur = [];
    }
  });
  // each chunk stays up until the next one starts
  out.forEach((c, i) => { c.to = i < out.length - 1 ? out[i + 1].from : c.to + 0.8; });
  return out;
})();

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const now = frame / fps;
  const chunk = CHUNKS.find((c) => now >= c.from && now < c.to);
  if (!chunk) return null;
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 70}}>
      <div style={{display: 'flex', gap: 24, whiteSpace: 'nowrap', justifyContent: 'center',
        fontFamily: 'Impact, "Arial Black", "DejaVu Sans", sans-serif', fontWeight: 900, fontSize: 88, textTransform: 'uppercase', letterSpacing: 2}}>
        {chunk.words.map((w, i) => {
          const active = now >= w.start && now < w.end + 0.12;
          return <span key={i} style={{color: active ? '#ffd23f' : '#ffffff', WebkitTextStroke: '14px #111', paintOrder: 'stroke fill',
            textShadow: '0 6px 0 #111', display: 'inline-block'}}>{w.text.replace(/[.,!?]$/, '')}</span>;
        })}
      </div>
    </AbsoluteFill>
  );
};

export const Proof: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: '#111'}}>
      {timing.shots.map((s, i) => {
        const from = Math.round(s.start * fps) - (i === 0 ? 0 : FADE);
        const end = Math.round(s.end * fps);
        return (
          <Sequence key={i} from={from} durationInFrames={end - from + 1}>
            <Shot image={s.image} index={i} frames={end - from} />
          </Sequence>
        );
      })}
      <Captions />
      <Audio src={staticFile('narration.mp3')} />
    </AbsoluteFill>
  );
};
