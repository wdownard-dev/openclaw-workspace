import React from 'react';
import {AbsoluteFill, Sequence, Img, staticFile, useCurrentFrame} from 'remotion';
import TL from './slice_timeline.json';

const FPS = (TL as any).fps as number;
const cuts = (TL as any).cuts as any[];
const IW = 1536, IH = 1024, FW = 1920, FH = 1080;
// full frame = 16:9 window centred vertically on the 3:2 plate
const FULL = {x: 0, y: (IH - IW * 9 / 16) / 2, w: IW};

const Cut: React.FC<{c: any; dur: number}> = ({c, dur}) => {
  const f = useCurrentFrame();
  const t = Math.min(1, f / Math.max(1, dur - 1));
  let r = c.crop_rect ? {x: c.crop_rect[0], y: c.crop_rect[1], w: c.crop_rect[2]} : {...FULL};
  let z = 1, dx = 0, dy = 0;
  if (c.move === 'push_in') z = 1 + 0.06 * t;
  else if (c.move === 'pull_out') z = 1.06 - 0.06 * t;
  else if (c.move === 'pan_up') { z = 1.12; dy = (0.05 - 0.10 * t) * (r.w * 9 / 16); }
  else if (c.move === 'pan_right' || c.move === 'pan') { z = 1.06; dx = (-0.02 + 0.04 * t) * r.w; }
  const h = r.w * 9 / 16;
  const w2 = r.w / z, h2 = h / z;
  const x = r.x + (r.w - w2) / 2 + dx, y = r.y + (h - h2) / 2 + dy;
  const s = FW / w2;
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <Img src={staticFile(`s/${c.image}`)} style={{position: 'absolute', left: -x * s, top: -y * s, width: IW * s, height: IH * s}} />
      {c.image2 ? (
        <Img src={staticFile(`s/${c.image2}`)} style={{position: 'absolute', left: -x * s, top: -y * s, width: IW * s, height: IH * s, opacity: Math.max(0, Math.min(1, (f - (c.swap_frac ?? 0.55) * dur) / 6))}} />
      ) : null}
    </AbsoluteFill>
  );
};

export const Slice: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    {cuts.map((c) => {
      const from = Math.round(c.start_s * FPS);
      const to = Math.round(c.end_s * FPS);
      return (
        <Sequence key={c.beat} from={from} durationInFrames={Math.max(1, to - from)} layout="none">
          <Cut c={c} dur={to - from} />
        </Sequence>
      );
    })}
  </AbsoluteFill>
);
