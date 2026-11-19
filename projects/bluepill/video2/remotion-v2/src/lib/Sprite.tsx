import React from 'react';
import {Img, staticFile} from 'remotion';
import {C} from './theme';
import {popScale, slideIn, slideOut} from './anim';
import {CodeProp, Placeholder} from './CodeProps';

/** resolved sprite state at time t: which src is showing after swaps, and whether it is leaving */
export type SpriteState = {e: any; asset: any; src: string; gone: boolean; swapT: number | null; sliding: boolean};
export const spriteStates = (events: any[], shotId: string, t: number): SpriteState[] => {
  const sprites = events.filter((x) => x.shot === shotId && x.kind === 'sprite' && t >= x.t);
  return sprites.map((e) => {
    const st: SpriteState = {e, asset: e.asset, src: e.src, gone: false, swapT: null, sliding: false};
    for (const sw of events.filter((x) => x.shot === shotId && x.kind === 'swap' && x.targetIndex === e.i && t >= x.t)) {
      st.swapT = sw.t;
      if (sw.src === 'none') { st.gone = true; st.sliding = false; }
      else if (sw.src === 'slide_out_left') { st.sliding = true; if (t - sw.t > 0.15) st.gone = true; }
      else { st.src = sw.src; st.asset = sw.asset; st.gone = false; st.sliding = false; }
    }
    return st;
  });
};

const Art: React.FC<{asset: any; name: string; h: number}> = ({asset, name, h}) => {
  if (!asset || asset.kind === 'missing') return <Placeholder name={name} h={h} />;
  if (asset.kind === 'code') return <CodeProp code={asset.code} h={h} base={asset.base} />;
  // very wide art (the Greek line, group sheets) is capped to the safe width; objectFit keeps the aspect
  return <Img src={staticFile(asset.src)} style={{height: h, maxWidth: 1760, objectFit: 'contain', display: 'block'}} />;
};

/** Sprite: bottom-anchored at (x,y) with height h; pops at onset (or slides 160 px when enter:'slide'); hard swaps; optional mirror; inset = framed picture-in-picture, centre-anchored. */
export const Sprite: React.FC<{s: SpriteState; t: number}> = ({s, t}) => {
  const {e} = s;
  if (s.gone) return null;
  const dt = t - e.t;
  const enterSlide = e.enter === 'slide';
  const sc = enterSlide ? 1 : popScale(dt);
  let dx = enterSlide ? slideIn(dt) * (e.x < 960 ? -1 : 1) : 0;
  if (s.sliding && s.swapT !== null) dx += slideOut(t - s.swapT);
  const mirror = e.mirror ? ' scaleX(-1)' : '';
  if (e.inset) {
    const pad = 18;
    return (
      <div style={{position: 'absolute', left: e.x + dx, top: e.y, transform: `translate(-50%,-50%) scale(${sc})`}}>
        <div style={{background: C.cream, border: `6px solid ${C.outline}`, padding: pad, boxShadow: '0 8px 20px rgba(0,0,0,0.35)', transform: 'rotate(-2deg)'}}>
          <div style={{transform: mirror || undefined}}><Art asset={s.asset} name={s.src} h={e.h} /></div>
        </div>
      </div>
    );
  }
  return (
    <div style={{position: 'absolute', left: e.x + dx, top: e.y, transform: `translate(-50%,-100%) scale(${sc})${mirror}`, transformOrigin: '50% 100%'}}>
      <Art asset={s.asset} name={s.src} h={e.h} />
    </div>
  );
};
/** head position guess for bubble tails: top of the sprite, slightly inside */
export const headOf = (s: SpriteState): [number, number] => [s.e.x, s.e.inset ? s.e.y - s.e.h * 0.5 : s.e.y - s.e.h * 0.88];
