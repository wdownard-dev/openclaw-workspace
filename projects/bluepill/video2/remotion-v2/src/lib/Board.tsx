import React from 'react';
import {Img, staticFile} from 'remotion';
import {C, HAND, W, H} from './theme';
import {CodeMap} from './Maps';
import {Stamp} from './Text';
import {Placeholder} from './CodeProps';

export const CARDS: [number, number][] = [[560, 420], [1360, 420], [560, 820], [1360, 820]];
const CW = 640, CH = 340;
const FRAME_LABEL = ['ELEPHANT', 'SMITHS', 'WALLS', 'FOLKTALE'];
const PING_CARD: Record<string, number> = {ping_elephant: 0, ping_smiths: 1, ping_walls: 2};

type Card = 'blank' | 'q' | 'skull' | 'anvil' | 'wall' | 'world';
type BState = {cards: Card[]; full?: 'world' | 'blank'; dim?: number[]; jitter?: number; flicker?: number; stampAll?: boolean};
/** board states named in the storyboard (label style "board"). Earned verdict stamps are added by the caller from shot.earned. */
export const STATES: Record<string, BState> = {
  empty: {cards: ['blank', 'blank', 'blank', 'blank']},
  frame1_skull: {cards: ['skull', 'blank', 'blank', 'blank']},
  frame3_wall_flicker: {cards: ['skull', 'blank', 'wall', 'blank'], flicker: 2},
  four_questions: {cards: ['q', 'q', 'q', 'q']},
  four_questions_skull: {cards: ['skull', 'q', 'q', 'q']},
  frame1_skull_jitter: {cards: ['skull', 'q', 'q', 'q'], jitter: 0},
  four_frames_skull: {cards: ['skull', 'q', 'q', 'q']},
  four_frames_skull_anvil: {cards: ['skull', 'anvil', 'q', 'q']},
  four_frames_skull_anvil_wall: {cards: ['skull', 'anvil', 'wall', 'q']},
  frame1_dim: {cards: ['skull', 'anvil', 'wall', 'q'], dim: [0]},
  frame4_full_world: {cards: ['skull', 'anvil', 'wall', 'world'], full: 'world'},
  frame4_blank: {cards: ['skull', 'anvil', 'wall', 'world'], full: 'blank'},
  four_stamped: {cards: ['skull', 'anvil', 'wall', 'world'], stampAll: true},
};
const ALL_STAMPS = [{card: 0, text: 'UNPROVEN'}, {card: 1, text: 'PLAUSIBLE'}, {card: 2, text: 'REAL'}, {card: 3, text: 'PROBABLY OLDER', sub: 'THAN HOMER'}];

const CardArt: React.FC<{kind: Card; art: any; w: number; h: number}> = ({kind, art, w, h}) => {
  const fit: React.CSSProperties = {width: w, height: h, objectFit: 'cover'};
  if (kind === 'blank') return null;
  if (kind === 'q') return <div style={{fontFamily: HAND, fontSize: h * 0.7, color: C.ink, lineHeight: 1}}>?</div>;
  if (kind === 'world') return <div style={{width: w, height: h, overflow: 'hidden', position: 'relative'}}><div style={{transform: `scale(${w / W})`, transformOrigin: '0 0', width: W, height: H}}><CodeMap mapId="map_world" /></div></div>;
  const a = art[kind];
  if (a && a.kind === 'file') return <Img src={staticFile(a.src)} style={kind === 'wall' ? fit : {maxWidth: w * 0.9, maxHeight: h * 0.9}} />;
  return <Placeholder name={kind === 'skull' ? 'skull_front_pd_small' : kind === 'anvil' ? 'prop__anvil__a' : 'NBG07'} h={h * 0.8} w={w * 0.7} />;
};

/** The case board (bg type "board"): cork, wood frame, four pinned cream cards 2x2, clear top strip. */
export const Board: React.FC<{state: string; dt: number; art: any; earned: {card: number; text: string; sub?: string}[]; frame: number}> = ({state, dt, art, earned, frame}) => {
  const st = STATES[state] || STATES.empty;
  if (st.full) {
    return (
      <div style={{position: 'absolute', inset: 0, background: C.cream}}>
        {st.full === 'world' && <CodeMap mapId="map_world" />}
        <div style={{position: 'absolute', inset: 0, boxShadow: `inset 0 0 0 ${28}px ${C.wood}`}} />
      </div>
    );
  }
  const stamps = st.stampAll ? ALL_STAMPS : earned;
  return (
    <div style={{position: 'absolute', inset: 0, background: C.cork}}>
      <div style={{position: 'absolute', inset: 0, backgroundImage: 'radial-gradient(rgba(0,0,0,0.08) 1px, transparent 1.5px)', backgroundSize: '9px 9px'}} />
      <div style={{position: 'absolute', inset: 0, boxShadow: `inset 0 0 0 28px ${C.wood}`}} />
      {CARDS.map(([cx, cy], i) => {
        const kind = st.cards[i];
        let dx = 0, dy = 0, show = true;
        if (st.jitter === i && dt < 0.5) { const k = Math.floor(dt * 15); dx = ((k * 7) % 5) - 2; dy = ((k * 11) % 5) - 2; dx *= 4; dy *= 4; }
        if (st.flicker === i && dt < 0.6) show = Math.floor(dt * 15) % 2 === 0;
        const dim = st.dim && st.dim.includes(i);
        const stamp = stamps.find((s) => s.card === i);
        return (
          <div key={i} style={{position: 'absolute', left: cx - CW / 2 + dx, top: cy - CH / 2 + dy, width: CW, height: CH, background: C.cream, boxShadow: '0 6px 14px rgba(0,0,0,0.35)', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden'}}>
            {show && <CardArt kind={kind} art={art} w={CW} h={CH} />}
            <div style={{position: 'absolute', left: 14, bottom: 8, fontFamily: HAND, fontSize: 26, color: C.verd}}>{i + 1}. {FRAME_LABEL[i]}</div>
            <div style={{position: 'absolute', left: CW / 2 - 12, top: -4, width: 24, height: 24, borderRadius: 12, background: C.brass, boxShadow: '0 2px 3px rgba(0,0,0,0.5)'}} />
            {dim && <div style={{position: 'absolute', inset: 0, background: 'rgba(30,30,30,0.55)'}} />}
            {stamp && <Stamp e={{x: CW / 2, y: CH / 2, text: stamp.text, sub: stamp.sub, rot: -4}} dt={1} paint size={stamp.sub ? 44 : 60} />}
          </div>
        );
      })}
    </div>
  );
};

/** Board ping (beats 13, 36, 44): corner inset of the board, the named frame glowing for 0.5 s, no stamp. Inset stays 1.5 s. */
export const BoardPing: React.FC<{state: string; dt: number; art: any; earned: any[]}> = ({state, dt, art, earned}) => {
  if (dt < 0 || dt > 1.5) return null;
  const card = PING_CARD[state] ?? 0;
  const iw = 480, ih = 270, sc = iw / W;
  const glow = dt < 0.5 ? 0.6 + 0.4 * Math.sin((dt / 0.5) * Math.PI) : 0;
  const [cx, cy] = CARDS[card];
  return (
    <div style={{position: 'absolute', right: 40, top: 40, width: iw, height: ih, overflow: 'hidden', border: `6px solid ${C.cream}`, boxShadow: '0 8px 20px rgba(0,0,0,0.4)', transform: `scale(${popScaleFast(dt)})`, transformOrigin: '100% 0%'}}>
      <div style={{transform: `scale(${sc})`, transformOrigin: '0 0', width: W, height: H}}>
        <Board state="four_frames_skull_anvil_wall" dt={9} art={art} earned={earned} frame={0} />
        <div style={{position: 'absolute', left: cx - CW / 2 - 16, top: cy - CH / 2 - 16, width: CW + 32, height: CH + 32, border: `18px solid ${C.gold}`, boxShadow: `0 0 60px 30px rgba(201,162,39,${glow})`, opacity: glow > 0 ? 1 : 0.5}} />
      </div>
    </div>
  );
};
const popScaleFast = (dt: number) => { if (dt < 0) return 0; const u = Math.min(1, dt / 0.2), c = 1.3; return 1 + (c + 1) * Math.pow(u - 1, 3) + c * Math.pow(u - 1, 2); };
