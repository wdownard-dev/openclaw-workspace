import React from 'react';
import {AbsoluteFill, Sequence, Img, staticFile, useCurrentFrame, interpolate} from 'remotion';
import TL from './timeline.json';

const FPS = (TL as any).fps as number;
const beats = (TL as any).beats as any[];
const TOTAL = (TL as any).total as number;

const Beat: React.FC<{b: any; dur: number}> = ({b, dur}) => {
  const f = useCurrentFrame();
  const scale = b.push ? 1 + 0.04 * Math.min(1, f / Math.max(1, dur - 1)) : 1;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {b.plate ? (
        <AbsoluteFill style={{overflow: 'hidden'}}>
          <Img src={staticFile(`p/${b.parts[Math.min(b.parts.length - 1, Math.floor((f / Math.max(1, dur)) * b.parts.length))]}.png`)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${scale})`}} />
        </AbsoluteFill>
      ) : (
        <AbsoluteFill style={{background: '#3b2a1a', color: '#c9a227', fontFamily: 'Permanent Marker', fontSize: 80, alignItems: 'center', justifyContent: 'center', display: 'flex'}}>MISSING {b.id}</AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

export const Video: React.FC = () => {
  const frame = useCurrentFrame();
  const fade = interpolate(frame, [TOTAL - 0.5 * FPS, TOTAL], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {beats.map((b, i) => {
        const from = Math.round(b.start * FPS);
        const to = i + 1 < beats.length ? Math.round(beats[i + 1].start * FPS) : TOTAL;
        return (
          <Sequence key={b.id} from={from} durationInFrames={Math.max(1, to - from)} layout="none">
            <Beat b={b} dur={to - from} />
          </Sequence>
        );
      })}
      <AbsoluteFill style={{background: '#000', opacity: fade}} />
    </AbsoluteFill>
  );
};
