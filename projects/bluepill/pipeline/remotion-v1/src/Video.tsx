import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, delayRender, continueRender} from 'remotion';
import {buildSegs, Seg} from './spec';
import {Captions, buildChunks} from './lib/Captions';
import {useFonts, clamp01} from './lib/theme';
import {FPS, TOTAL} from './lib/timing';

export const TOTAL_FRAMES = Math.ceil(TOTAL * FPS);
const fadeLen = (a: Seg, b: Seg) => (a.chapter || b.chapter ? 12 : (a.kind === 'pic') !== (b.kind === 'pic') ? 9 : 0);
const FadeIn: React.FC<{frames: number; children: React.ReactNode}> = ({frames, children}) => {
  const f = useCurrentFrame();
  const o = frames > 0 ? clamp01((f + 0.5) / frames) : 1;
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

const OverflowCheck: React.FC = () => {
  const f = useCurrentFrame();
  React.useEffect(() => {
    const h = delayRender('overflow-check');
    setTimeout(() => {
      const bad: string[] = [];
      document.querySelectorAll('body *').forEach((el) => {
        if (el.children.length === 0 && (el.textContent || '').trim()) {
          const rg = document.createRange(); rg.selectNodeContents(el); const r = rg.getBoundingClientRect();
          if (r.width > 0 && (r.left < 60 || r.right > 1860 || r.top < 50 || r.bottom > 1040)) bad.push(`${(el.textContent || '').trim().slice(0, 40)} [${Math.round(r.left)},${Math.round(r.top)},${Math.round(r.right)},${Math.round(r.bottom)}]`);
        }
      });
      console.log('OVERFLOW_CHECK ' + f + ' ' + JSON.stringify(bad));
      if ((window as any).__dbg !== 0) console.log('OVERFLOW_DBG leaf=' + document.querySelectorAll('body *').length);
      continueRender(h);
    }, 400);
  }, []);
  return null;
};

export const Video: React.FC<{withAudio?: boolean; check?: boolean}> = ({withAudio = true, check = false}) => {
  useFonts();
  const segs = useMemo(buildSegs, []);
  const chunks = useMemo(() => buildChunks(segs.map((s) => ({start: s.start, end: s.end, pos: s.cap, tone: s.tone}))), [segs]);
  const fr = (t: number) => Math.round(t * FPS);
  return (
    <AbsoluteFill style={{background: '#0c0a08'}}>
      {segs.map((s, i) => {
        const from = fr(s.start), to = i + 1 < segs.length ? fr(segs[i + 1].start) : TOTAL_FRAMES;
        const ext = i + 1 < segs.length ? fadeLen(s, segs[i + 1]) : 0;
        const fin = i > 0 ? fadeLen(segs[i - 1], s) : 0;
        return (
          <Sequence key={i} from={from} durationInFrames={Math.max(1, to - from + ext)} name={`shot ${s.n0}${s.n1 !== s.n0 ? '-' + s.n1 : ''}`}>
            <FadeIn frames={fin}>{s.entry.render({dur: s.end - s.start, t0: s.start, t1: s.end, ts: s.ts})}</FadeIn>
          </Sequence>
        );
      })}
      <Captions chunks={chunks} />
      {check && <OverflowCheck />}
      {withAudio && <Audio src={staticFile('audio/mix.wav')} />}
    </AbsoluteFill>
  );
};
