import React from 'react';
import timing from '../data/timing.json';
import {Scene, Mark} from './lib/Scene';
import {cam} from './lib/camera';
import {TitleCard, EndCard, MapShot, NamePlate, CountCard} from './lib/Cards';
import {CapPos} from './lib/Captions';

export type Trans = 'cut' | 'whip' | 'fade' | 'flash';
export type ShotDef = {id: string; cap: CapPos; trans: Trans; render: (dur: number) => React.ReactNode};

const clean = (w: string) => w.replace(/[^\w'-]/g, '').toLowerCase();
/** time (s) of the nth occurrence of a word, relative to the start of shot i; keeps cues glued to the narration if it is re-timed */
const rel = (i: number, word: string, nth = 0) => {
  const s = timing.shots[i].start, e = timing.shots[i].end;
  const hits = timing.words.filter((w) => w.start >= s - 1e-3 && w.start < e && clean(w.text) === word.toLowerCase());
  if (!hits[nth]) { console.warn(`shot ${i}: word '${word}' not found`); return 0.5; }
  return Math.max(0, hits[nth].start - s);
};

// crew = same hero art, shrunk and shaded so they read as background men
const CREW = '#9a8fa4';
const WARM = '#ffe2c2', DAWN = '#ffe3b0', NIGHT = '#8c9bd6', DUSK = '#ffd9b8';

export const SHOTS: ShotDef[] = [
  // 0 — hook line 1: crew walks up the path toward the cave
  {id: 'hook-walk', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="island" bgPos="50% 60%" tint={DUSK} grade="#ffe9d4" cam={cam.pan(-1, 0.035, 1.1)}
      cutouts={[
        {id: 'hero', src: 'hero', x: 0.40, y: 0.84, h: 0.36, at: 0.0, enter: 'left', enterDist: 0.6},
        {id: 'c1', src: 'hero', x: 0.27, y: 0.80, h: 0.29, at: 0.15, enter: 'left', enterDist: 0.6, tint: CREW, z: -1},
        {id: 'c2', src: 'hero', x: 0.16, y: 0.78, h: 0.27, at: 0.3, enter: 'left', enterDist: 0.6, tint: CREW, z: -2},
      ]} />},
  // 1 — hook line 2 (punchline): hard cut, giant silhouette, "SIX"
  {id: 'hook-six', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="cavedark" bgPos="50% 50%" tint="#e8d6c8" grade="#c9b8c8" cam={cam.hold([{at: 0.02, amp: 0.02, dur: 0.6}], 1.08, 0.6, 0.5)}
      cutouts={[
        {id: 'cy', src: 'cyclops', x: 0.68, y: 1.0, h: 0.86, at: 0.05, enter: 'rise', tint: '#2a1d2c', noShadow: true, bob: 4},
        {id: 'hero', src: 'hero', x: 0.26, y: 0.86, h: 0.34, tint: '#cdbfbf', marks: [{at: 0.1, kind: '!', fx: 0.5, fy: -0.07, size: 0.2}], react: [{at: 0.05, kind: 'recoil'}]},
      ]}
      impacts={[{text: 'SIX', at: 0.0, x: 0.32, y: 0.3, size: 360, color: '#ff4b3e', rot: -7, sfx: 'thud', dur: 1.7}]} />},
  // 2 — chapter title card
  {id: 'title', cap: 'none', trans: 'fade', render: (dur) =>
    <TitleCard dur={dur} kicker="CHAPTER 1  ·  THE ODYSSEY" title="THE CYCLOPS" numeral="I" sub="Twelve men. One cave. One lie." bg="cavedawn" />},
  // 3 — map with animated route arrow and years counter
  {id: 'map', cap: 'bottom', trans: 'whip', render: (dur) =>
    <MapShot dur={dur} bg="map" imgAspect={1536 / 1024}
      route={[[0.55, 0.16], [0.51, 0.30], [0.47, 0.46], [0.41, 0.60], [0.33, 0.69], [0.24, 0.67], [0.18, 0.58], [0.26, 0.52], [0.20, 0.45], [0.165, 0.385]]}
      draw={[0.9, Math.min(dur - 0.3, 3.5)]}
      pins={[{label: 'TROY', nx: 0.55, ny: 0.16, at: rel(3, 'troy'), dx: 0, dy: 92}, {label: 'HOME', nx: 0.165, ny: 0.385, at: rel(3, 'home'), dx: 30, dy: 82}]}
      counter={{label: 'YEARS AT SEA', from: 0, to: 10}} />},
  // 4 — enter the cave, sheep pop in
  {id: 'cave-enter', cap: 'bottom', trans: 'whip', render: (dur) =>
    <Scene dur={dur} bg="cave" bgPos="50% 62%" tint={WARM} grade="#fff0dc" cam={cam.pan(-1, 0.035, 1.1)}
      cutouts={[
        {id: 'hero', src: 'hero', x: 0.34, y: 0.86, h: 0.40, at: 0.0, enter: 'left', enterDist: 0.5, react: [{at: rel(4, 'cheese'), kind: 'hop'}], marks: [{at: rel(4, 'huge'), kind: '!', fx: 0.5, fy: -0.07, size: 0.2}]},
        {id: 'c1', src: 'hero', x: 0.20, y: 0.83, h: 0.32, at: 0.35, enter: 'left', enterDist: 0.5, tint: CREW, z: -1},
        {id: 'c2', src: 'hero', x: 0.12, y: 0.81, h: 0.29, at: 0.65, enter: 'left', enterDist: 0.5, tint: CREW, z: -2},
        {id: 'sheep', src: 'sheep', x: 0.80, y: 0.86, h: 0.24, at: rel(4, 'sheep') - 0.2, enter: 'pop', sfx: 'pop', bob: 3},
      ]} />},
  // 5 — punchline "first mistake", hard cut, shake
  {id: 'mistake', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="cave" bgFlip bgPos="40% 66%" tint={WARM} grade="#ffe6cc" cam={cam.pushIn(1.14, 0.42, 0.62, [{at: rel(5, 'mistake'), amp: 0.018, dur: 0.6}])}
      cutouts={[
        {id: 'c1', src: 'hero', x: 0.20, y: 0.80, h: 0.31, tint: CREW, z: -1, marks: [{at: 0.5, kind: '?', fx: 0.5, fy: 0, size: 0.14}]},
        {id: 'c2', src: 'hero', x: 0.62, y: 0.78, h: 0.30, tint: CREW, z: -1, marks: [{at: 0.8, kind: '?', fx: 0.5, fy: 0, size: 0.14}]},
        {id: 'hero', src: 'hero', x: 0.40, y: 0.86, h: 0.46, marks: [{at: 0.2, kind: 'sweat', fx: 0.82, fy: 0.12, size: 0.12}], react: [{at: rel(5, 'mistake'), kind: 'recoil'}]},
      ]}
      impacts={[{text: 'MISTAKE', at: rel(5, 'mistake'), x: 0.66, y: 0.30, size: 250, rot: -6, sfx: 'thud', dur: 1.2, color: '#ff4b3e'}]} />},
  // 6 — the owner returns: giant slams in, name plate
  {id: 'owner', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="cavedawn" bgPos="50% 62%" tint="#ffcf9a" cam={cam.pushIn(1.12, 0.7, 0.5, [{at: 0.8, amp: 0.022, dur: 0.6}])}
      cues={[{at: 0.78, sfx: 'thud', vol: 0.9}, {at: 0.25, sfx: 'whoosh', vol: 0.5}]}
      cutouts={[
        {id: 'hero', src: 'hero', x: 0.27, y: 0.86, h: 0.36, marks: [{at: 0.85, kind: '!', fx: 0.5, fy: -0.07, size: 0.2}], react: [{at: 0.85, kind: 'hop'}]},
        {id: 'cy', src: 'cyclops', x: 0.70, y: 0.90, h: 0.70, at: 0.3, enter: 'right', enterDist: 0.6, walk: false},
      ]}
      extras={({t}) => <NamePlate t={t} at={rel(6, 'polyphemus') - 0.2} dur={2.0} name="POLYPHEMUS" sub="THE CYCLOPS  ·  SON OF POSEIDON" x={80} y={70} />} />},
  // 7 — boulder rolls across the entrance, 22 wagons
  {id: 'boulder', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="cavedawn" bgPos="50% 38%" tint="#ffcf9a" cam={cam.pullOut(1.2, 0.5, 0.55, [{at: 1.35, amp: 0.026, dur: 0.7}])}
      cues={[{at: 0.25, sfx: 'rumble', vol: 0.7}, {at: 1.35, sfx: 'thud', vol: 1.0}]}
      dimKeys={[[0, 0], [1.3, 0], [1.9, 0.5]]}
      cutouts={[
        {id: 'cy', src: 'cyclops', x: 0.25, y: 0.88, h: 0.70, react: [{at: 1.3, kind: 'squash', dur: 0.5}]},
        {id: 'boulder', src: 'boulder', x: 0.53, y: 0.80, h: 0.62, at: 0.25, enter: 'right', enterDist: 0.6, spin: 480, walk: false, bob: 0, noShadow: false},
        {id: 'hero', src: 'hero', x: 0.84, y: 0.88, h: 0.32, marks: [{at: 1.5, kind: 'sweat', fx: 0.2, fy: 0.1, size: 0.12}, {at: 1.4, kind: '!', fx: 0.5, fy: -0.07, size: 0.2}], react: [{at: 1.4, kind: 'recoil'}]},
      ]}
      extras={({t}) => <CountCard t={t} at={rel(7, 'twenty-two') - 0.1} dur={2.6} n={22} label="WAGONS" x={0.5} y={0.3} />} />},
  // 8 — offering the wine (hero tiny vs giant)
  {id: 'wine', cap: 'bottom', trans: 'whip', render: (dur) =>
    <Scene dur={dur} bg="cave" bgFlip bgPos="55% 60%" tint={WARM} grade="#fff0dc" cam={cam.pushIn(1.16, 0.3, 0.7)}
      cutouts={[
        {id: 'cy', src: 'cyclops', x: 0.74, y: 0.90, h: 0.72},
        {id: 'hero', src: 'hero', x: 0.20, y: 0.86, h: 0.30, marks: [{at: 0.3, kind: 'sweat', fx: 0.82, fy: 0.12, size: 0.14}]},
        {id: 'cup', src: 'cup', x: 0.30, y: 0.66, h: 0.11, at: rel(8, 'offers') - 0.1, enter: 'pop', sfx: 'ding', noShadow: true, bob: 0, moveTo: {x: 0.52, y: 0.62, at: rel(8, 'cup') + 0.1, dur: 0.9}, z: 3},
      ]} />},
  // 9 — the giant loves it and asks the name
  {id: 'loves', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="cave" bgPos="70% 58%" tint={WARM} grade="#ffe9d0" cam={cam.pushIn(1.08, 0.4, 0.2)}
      cutouts={[
        {id: 'cy', src: 'cyclops', x: 0.38, y: 0.88, h: 0.76, react: [{at: rel(9, 'loves') + 0.1, kind: 'hop', dur: 0.5}, {at: rel(9, 'name'), kind: 'wobble'}], marks: [{at: rel(9, 'name'), kind: '?', fx: 0.46, fy: -0.03, size: 0.1, dur: 1.8}]},
        {id: 'hero', src: 'hero', x: 0.80, y: 0.88, h: 0.30, enter: 'right', at: 0.0, enterDist: 0.2, flip: true},
      ]} />},
  // 10 — "Nobody" punchline
  {id: 'nobody', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="cavedark" bgPos="50% 60%" tint="#f1e0d0" grade="#d8c8c0" cam={cam.pushIn(1.16, 0.4, 0.55, [{at: rel(10, 'nobody'), amp: 0.015, dur: 0.5}])}
      cutouts={[
        {id: 'cy', src: 'cyclops', x: 0.82, y: 0.84, h: 0.55, z: -1, marks: [{at: rel(10, 'nobody') + 0.2, kind: '?', fx: 0.46, fy: -0.04, size: 0.1}]},
        {id: 'hero', src: 'hero', x: 0.32, y: 0.88, h: 0.52, react: [{at: rel(10, 'nobody'), kind: 'hop'}]},
      ]}
      impacts={[{text: 'NOBODY', at: rel(10, 'nobody'), x: 0.56, y: 0.26, size: 300, rot: -5, sfx: 'pop', dur: 1.5}]} />},
  // 11 — eat Nobody last, falls asleep
  {id: 'asleep', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="cave" bgFlip bgPos="20% 62%" tint={WARM} grade="#ffe2c4" cam={cam.pan(1, 0.03, 1.1)}
      cues={[{at: rel(11, 'asleep') - 0.6, sfx: 'thud', vol: 0.6}]}
      cutouts={[
        {id: 'cy', src: 'cyclops', x: 0.66, y: 0.88, h: 0.62, bob: 5, react: [{at: rel(11, 'promises'), kind: 'wobble'}], rotateTo: {at: rel(11, 'falls'), deg: -88, lift: 0.22}, shadowW: 0.7},
        {id: 'hero', src: 'hero', x: 0.12, y: 0.88, h: 0.34, at: 0.1, enter: 'left', enterDist: 0.2, marks: [{at: rel(11, 'asleep'), kind: 'shh', fx: 0.5, fy: -0.07, size: 0.2, dur: 1.6}]},
      ]}
      extras={({t}) => <div style={{position: 'absolute', left: 560, top: 360, width: 300, height: 300}}><Mark m={{at: rel(11, 'asleep') + 0.3, kind: 'zzz', fx: 0.5, fy: 0.5, size: 150, dur: 3, color: '#cfe3ff'}} t={t} boxW={300} boxH={300} /></div>} />},
  // 12 — night, crew sharpens the stake
  {id: 'stake', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="cavedark" bgPos="45% 55%" tint={NIGHT} grade="#8a98d0" cam={cam.pan(-1, 0.03, 1.1)}
      cues={[{at: 0.25, sfx: 'scrape', vol: 0.6}]}
      cutouts={[
        {id: 'cy', src: 'cyclops', x: 0.88, y: 0.72, h: 0.30, depth: 'bg', rot: -88, tint: '#5a6290', noShadow: true, bob: 2},
        {id: 'c1', src: 'hero', x: 0.20, y: 0.84, h: 0.33, tint: '#5c6490', z: -1},
        {id: 'c2', src: 'hero', x: 0.62, y: 0.84, h: 0.33, tint: '#5c6490', z: -1},
        {id: 'hero', src: 'hero', x: 0.40, y: 0.88, h: 0.44, react: [{at: 0.3, kind: 'squash', dur: 0.4}, {at: 0.9, kind: 'squash', dur: 0.4}]},
        {id: 'stake', src: 'stake', x: 0.50, y: 0.78, h: 0.30, at: 0.2, enter: 'pop', rot: -22, noShadow: true, bob: 0, tint: '#ffffff', z: 3, marks: [{at: 0.4, kind: 'sparks', fx: 0.88, fy: 0.78, size: 0.5, dur: 2.4}]},
      ]} />},
  // 13 — the giant is blind (flash cut, impact word)
  {id: 'blind', cap: 'bottom', trans: 'flash', render: (dur) =>
    <Scene dur={dur} bg="cavedawn" bgPos="50% 55%" tint="#ffd2a6" grade="#e8d0c0" cam={cam.pushIn(1.16, 0.5, 0.3, [{at: 0.05, amp: 0.02, dur: 0.6}])}
      dimKeys={[[0, 0.12]]}
      cutouts={[
        {id: 'boulder', src: 'boulder', x: 0.50, y: 0.80, h: 0.95, depth: 'bg', tint: '#8a7a80', noShadow: true},
        {id: 'cy', src: 'cyclops', x: 0.50, y: 0.87, h: 0.74, react: [{at: 0.05, kind: 'wobble', dur: 1.0}, {at: rel(13, 'waiting'), kind: 'wobble', dur: 0.9}], marks: [{at: 0.15, kind: 'x', fx: 0.455, fy: 0.155, size: 0.11, dur: 6}]},
      ]}
      impacts={[{text: 'BLIND!', at: rel(13, 'blind'), x: 0.2, y: 0.3, size: 260, rot: -8, color: '#ff4b3e', sfx: 'thud', dur: 1.4}]} />},
  // 14 — dawn: sheep file out past the blinded giant
  {id: 'sheep-out', cap: 'bottom', trans: 'whip', render: (dur) =>
    <Scene dur={dur} bg="cavedawn" bgFlip bgPos="60% 42%" tint={DAWN} cam={cam.pan(1, 0.04, 1.1)}
      cutouts={[
        {id: 'cy', src: 'cyclops', x: 0.76, y: 0.87, h: 0.70, marks: [{at: 0.2, kind: 'x', fx: 0.455, fy: 0.155, size: 0.11, dur: 6}], react: [{at: 1.0, kind: 'wobble'}, {at: 2.4, kind: 'wobble'}]},
        ...[0.1, 0.65, 1.2, 1.75, 2.3].map((a, i) => ({id: 'sh' + i, src: 'sheep', x: -0.1, y: 0.86 - (i % 2) * 0.012, h: 0.22 + (i % 2) * 0.02, moveTo: {x: 1.15, at: a, dur: 3.0}, bob: 0, z: 2})),
      ]} />},
  // 15 — hiding underneath: hero peeks out from behind a sheep
  {id: 'hiding', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="cavedawn" bgPos="30% 55%" tint={DAWN} cam={cam.pushIn(1.12, 0.5, 0.6)}
      cutouts={[
        {id: 'hero', src: 'hero', x: 0.47, y: 0.86, h: 0.48, at: 0.15, enter: 'rise', z: 1, marks: [{at: 0.8, kind: 'shh', fx: 0.2, fy: -0.07, size: 0.2, dur: 1.8}]},
        {id: 'sheep', src: 'sheep', x: 0.60, y: 0.86, h: 0.54, z: 2, bob: 4},
        {id: 'c1', src: 'hero', x: 0.88, y: 0.84, h: 0.36, tint: CREW, z: 0, at: 0.5, enter: 'rise'},
        {id: 'sheep2', src: 'sheep', x: 0.90, y: 0.86, h: 0.32, z: 3, bob: 3},
      ]} />},
  // 16 — punchline "the plan works": ship with hero
  {id: 'plan-works', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="sea" bgPos="50% 62%" tint={DAWN} cam={cam.hold([{at: 0.4, amp: 0.008, dur: 0.4}], 1.08)}
      cues={[{at: 0.05, sfx: 'whoosh', vol: 0.6}]}
      cutouts={[
        {id: 'ship', src: 'ship', x: 0.42, y: 0.84, h: 0.44, at: 0.0, enter: 'left', enterDist: 0.7, walk: false, bob: 0, noShadow: true},
        {id: 'hero', src: 'hero', x: 0.42, y: 0.745, h: 0.25, at: 0.0, enter: 'left', enterDist: 0.7, walk: false, bob: 0, noShadow: true, z: 2, react: [{at: 0.6, kind: 'hop', dur: 0.5}]},
      ]} />},
  // 17 — pulling away; shouting his name
  {id: 'shout', cap: 'bottom', trans: 'cut', render: (dur) =>
    <Scene dur={dur} bg="sea" bgFlip bgPos="50% 42%" tint={DAWN} cam={cam.pullOut(1.2, 0.4, 0.7)}
      cutouts={[
        {id: 'cy', src: 'cyclops', x: 0.075, y: 0.36, h: 0.15, depth: 'bg', tint: '#d2b4aa', noShadow: true, bob: 1, marks: [{at: rel(17, 'name') - 0.4, kind: '!', fx: 0.5, fy: -0.03, size: 0.2}]},
        {id: 'ship', src: 'ship', x: 0.62, y: 0.86, h: 0.44, noShadow: true, bob: 0, moveTo: {x: 0.76, at: 0.0, dur: dur}, noWalkHop: true},
        {id: 'hero', src: 'hero', x: 0.62, y: 0.765, h: 0.25, noShadow: true, bob: 0, z: 2, moveTo: {x: 0.76, at: 0.0, dur: dur}, noWalkHop: true, react: [{at: rel(17, 'shouting'), kind: 'hop', dur: 0.5}, {at: rel(17, 'name'), kind: 'hop', dur: 0.5}]},
      ]}
      impacts={[{text: 'ODYSSEUS!', at: rel(17, 'real'), x: 0.5, y: 0.2, size: 210, rot: -4, color: '#ffd23f', sfx: 'pop', dur: 1.6}]} />},
  // 18 — storm shot; foreshadows the rest of the journey
  {id: 'storm', cap: 'bottom', trans: 'flash', render: (dur) =>
    <Scene dur={dur} bg="storm" bgPos="40% 50%" tint="#cfd6ee" cam={cam.pullOut(1.25, 0.45, 0.55)}
      flash={[1.0, 3.2]} cues={[{at: 1.0, sfx: 'thunder', vol: 0.8}, {at: 3.2, sfx: 'thunder', vol: 0.65}]}
      impacts={[{text: 'PRIDE', at: rel(18, 'pride'), x: 0.74, y: 0.28, size: 260, rot: -6, color: '#ff4b3e', sfx: 'thud', dur: 1.5}]} />},
  // 19 — end card / tease
  {id: 'end', cap: 'bottom', trans: 'fade', render: (dur) =>
    <EndCard dur={dur} kicker="NEXT TIME" title={'POSEIDON\nWANTS REVENGE'} />},
];
