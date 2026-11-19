import React from 'react';
import timing from '../data/timing.json';
import {Scene, CutoutSpec} from './lib/Scene';
import {cam} from './lib/camera';
import {CapPos} from './lib/Captions';
import {FONT_CAP, clamp01} from './lib/theme';

export type ShotDef = {id: string; idx: number; cap: CapPos; render: (dur: number) => React.ReactNode; stillT: number};
const clean = (w: string) => w.replace(/[^\w'-]/g, '').toLowerCase();
const rel = (i: number, word: string, nth = 0) => {
  const s = timing.shots[i].start, e = timing.shots[i].end;
  const hits = timing.words.filter((w) => w.start >= s - 1e-3 && w.start < e && clean(w.text) === word.toLowerCase());
  return hits[nth] ? Math.max(0, hits[nth].start - s) : 0.5;
};
const WARM = '#ffe6cc', DAWN = '#ffe3b4';
// crew variants: same art, shifted hue/brightness and size so they separate from the hero (compositing only)
const crew = (id: string, x: number, y: number, h: number, v: 0 | 1 | 2, extra: Partial<CutoutSpec> = {}): CutoutSpec => ({
  id, src: 'crew', x, y, h, z: -1,
  filter: ['saturate(0.9) brightness(0.9)', 'sepia(0.45) saturate(0.9) brightness(0.86)', 'saturate(0.75) brightness(0.84) contrast(1.05)'][v], ...extra});

const NamePlate: React.FC<{t: number; at: number; dur: number}> = ({t, at, dur}) => {
  const u = t - at; if (u < 0 || u > dur) return null;
  const o = clamp01(u / 0.4) * clamp01((dur - u) / 0.4);
  return <div style={{position: 'absolute', left: 84, top: 70, opacity: o, color: '#f6f1e6', fontFamily: FONT_CAP, textShadow: '0 2px 4px rgba(0,0,0,0.9), 0 0 12px rgba(0,0,0,0.7)'}}>
    <div style={{fontSize: 40, fontWeight: 700, letterSpacing: 6}}>POLYPHEMUS</div>
    <div style={{width: 220, height: 2, background: '#c9a24a', margin: '8px 0'}} />
    <div style={{fontSize: 20, letterSpacing: 4, opacity: 0.85}}>THE CYCLOPS · SON OF POSEIDON</div>
  </div>;
};

const nodes = {
  // a — establishing: hero and crew walk into the cave, sheep in the pen
  enter: (dur: number) =>
    <Scene dur={dur} bg="cave" bgPos="50% 62%" tint={WARM} grade="#fff0dc" cam={cam.pushIn(1.07, 0.35, 0.7)}
      cutouts={[
        {id: 'hero', src: 'ody', x: 0.38, y: 0.86, h: 0.47, at: 0, enter: 'left', enterDist: 0.15, bob: 2},
        crew('c1', 0.22, 0.83, 0.41, 0, {at: 0.15, enter: 'left', enterDist: 0.15}),
        crew('c2', 0.11, 0.81, 0.38, 1, {at: 0.3, enter: 'left', enterDist: 0.15, flip: true}),
        {id: 'sheep', src: 'sheep', x: 0.79, y: 0.85, h: 0.22, at: rel(4, 'sheep') - 0.3, enter: 'fade'},
      ]} />,
  mistake: (dur: number) =>
    <Scene dur={dur} bg="cave" bgFlip bgPos="40% 66%" tint={WARM} grade="#ffe9d0" cam={cam.pushIn(1.07, 0.42, 0.62)}
      cutouts={[
        crew('c1', 0.19, 0.79, 0.38, 0), crew('c2', 0.64, 0.77, 0.37, 2, {flip: true}),
        {id: 'hero', src: 'ody', x: 0.41, y: 0.86, h: 0.52, bob: 2},
      ]} />,
  owner: (dur: number) =>
    <Scene dur={dur} bg="cavedawn" bgPos="50% 62%" tint="#ffd9ae" cam={cam.pushIn(1.06, 0.7, 0.5, [{at: 1.1, px: 8, hz: 2.5, dur: 0.3}])}
      cues={[{at: 1.1, sfx: 'thud', vol: 0.4}]}
      cutouts={[
        {id: 'hero', src: 'ody', x: 0.24, y: 0.86, h: 0.40},
        {id: 'cy', src: 'cy', x: 0.70, y: 0.88, h: 0.78, at: 0.45, enter: 'right', enterDist: 0.2, bob: 2},
      ]}
      extras={({t}) => <NamePlate t={t} at={rel(6, 'polyphemus') - 0.3} dur={2.2} />} />,
  boulder: (dur: number) =>
    <Scene dur={dur} bg="cavedawn" bgPos="50% 38%" tint="#ffd9ae" cam={cam.pullOut(1.07, 0.5, 0.55, [{at: 1.2, px: 8, hz: 2.5, dur: 0.3}])}
      cues={[{at: 0.25, sfx: 'rumble', vol: 0.45}, {at: 1.2, sfx: 'thud', vol: 0.45}]}
      dimKeys={[[0, 0], [1.2, 0], [2.4, 0.3]]}
      cutouts={[
        {id: 'cy', src: 'cy', x: 0.25, y: 0.88, h: 0.78, bob: 2},
        {id: 'boulder', src: 'boulder3', x: 0.55, y: 0.80, h: 0.52, at: 0.25, enter: 'right', enterDist: 0.2, spin: 180, walk: false, noShadow: false},
        {id: 'hero', src: 'ody', x: 0.86, y: 0.86, h: 0.34},
      ]} />,
  wine: (dur: number) =>
    <Scene dur={dur} bg="cave" bgFlip bgPos="55% 60%" tint={WARM} grade="#fff0dc" cam={cam.pushIn(1.07, 0.3, 0.7)}
      cutouts={[
        {id: 'cy', src: 'cy', x: 0.76, y: 0.88, h: 0.78},
        {id: 'hero', src: 'ody', x: 0.21, y: 0.86, h: 0.44, bob: 2},
        {id: 'cup', src: 'cup', x: 0.32, y: 0.68, h: 0.11, at: rel(8, 'offers') - 0.1, enter: 'fade', noShadow: true, moveTo: {x: 0.56, y: 0.63, at: rel(8, 'cup') + 0.1, dur: 1.2}, z: 3},
      ]} />,
  loves: (dur: number) =>
    <Scene dur={dur} bg="cave" bgPos="70% 58%" tint={WARM} grade="#ffe9d0" cam={cam.pushIn(1.06, 0.4, 0.2)}
      cutouts={[
        {id: 'cy', src: 'cy', x: 0.38, y: 0.88, h: 0.82, bob: 2},
        {id: 'hero', src: 'ody', x: 0.80, y: 0.86, h: 0.42, flip: true},
      ]} />,
  // extra stills only
  blind: (dur: number) =>
    <Scene dur={dur} bg="cavedawn" bgFlip bgPos="60% 42%" tint={DAWN} cam={cam.hold([], 1.04)}
      cutouts={[
        {id: 'cy', src: 'cy_blind', x: 0.66, y: 0.92, h: 0.74},
        {id: 'sh0', src: 'sheep', x: 0.30, y: 0.90, h: 0.24, z: 2},
        {id: 'sh1', src: 'sheep', x: 0.14, y: 0.88, h: 0.20, z: 1, flip: true},
      ]} />,
  ship: (dur: number) =>
    <Scene dur={dur} bg="sea" bgFlip bgPos="50% 42%" tint={DAWN} cam={cam.hold([], 1.04)}
      cutouts={[
        {id: 'cy', src: 'cy_blind', x: 0.075, y: 0.335, h: 0.17, depth: 'bg', tint: '#d9bcb0', noShadow: true},
        {id: 'ship', src: 'ship3', x: 0.62, y: 0.90, h: 0.48, shadowW: 0.5},
        {id: 'hero', src: 'ody_shout', x: 0.62, y: 0.775, h: 0.40, noShadow: true, z: 2},
      ]} />,
};

// clip shots = timing shots 4..9
export const SHOTS: ShotDef[] = [
  {id: 'enter', idx: 4, cap: 'bottom', render: nodes.enter, stillT: 4.8},
  {id: 'mistake', idx: 5, cap: 'bottom', render: nodes.mistake, stillT: 2.4},
  {id: 'owner', idx: 6, cap: 'bottom', render: nodes.owner, stillT: 2.2},
  {id: 'boulder', idx: 7, cap: 'bottom', render: nodes.boulder, stillT: 2.0},
  {id: 'wine', idx: 8, cap: 'bottom', render: nodes.wine, stillT: 3.4},
  {id: 'loves', idx: 9, cap: 'bottom', render: nodes.loves, stillT: 2.0},
];
// six key stills (a-f)
export const STILLS: {id: string; render: (dur: number) => React.ReactNode; t: number}[] = [
  {id: 'a_establishing', render: nodes.enter, t: 2.2},
  {id: 'b_boulder', render: nodes.boulder, t: 2.0},
  {id: 'c_face_to_face', render: nodes.loves, t: 1.5},
  {id: 'd_cup', render: nodes.wine, t: 3.4},
  {id: 'e_blinded', render: nodes.blind, t: 1.5},
  {id: 'f_ship', render: nodes.ship, t: 1.5},
];
