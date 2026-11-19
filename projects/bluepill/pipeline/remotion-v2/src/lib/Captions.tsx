import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {FONT_CAP, INK, clamp01} from './theme';

export type Word = {text: string; start: number; end: number};
export type Chunk = {from: number; to: number; text: string; words: string[]};
export type CapPos = 'bottom' | 'top' | 'none';

const WEAK = new Set(['a', 'an', 'the', 'of', 'to', 'and', 'but', 'is', 'his', 'her', 'their', 'that', 'he', 'she', 'they', 'so', 'in', 'on', 'at', 'for', 'with', 'as', 'it', 'or', 'into', 'every', 'this']);
const clean = (w: string) => w.replace(/[^\w'-]/g, '').toLowerCase();
const MAX_WORDS = 6, MAX_CHARS = 36;
const len = (ws: Word[]) => ws.map((x) => x.text).join(' ').length;

/** Phrase chunks: break at punctuation first, then split long clauses into balanced parts that never end on a weak word (the, a, of...),
 *  never leave a 1-word orphan, and never cross a shot boundary (caption position is fixed per shot). */
export const buildChunks = (words: Word[], shotStarts: number[], shotEnds: number[]): Chunk[] => {
  const out: Chunk[] = [];
  shotStarts.forEach((s, si) => {
    const ws = words.filter((w) => w.start >= s - 1e-3 && w.start < shotEnds[si] - 1e-3);
    if (!ws.length) return;
    // 1. clauses at punctuation
    let clauses: Word[][] = []; let cur: Word[] = [];
    ws.forEach((w) => { cur.push(w); if (/[.,!?:;]$/.test(w.text)) { clauses.push(cur); cur = []; } });
    if (cur.length) clauses.push(cur);
    // 2. one-word clauses join a neighbour
    for (let i = 0; i < clauses.length; i++) {
      if (clauses[i].length === 1 && clauses.length > 1) {
        if (i + 1 < clauses.length) { clauses[i + 1] = [...clauses[i], ...clauses[i + 1]]; clauses.splice(i, 1); i--; }
        else { clauses[i - 1] = [...clauses[i - 1], ...clauses[i]]; clauses.splice(i, 1); }
      }
    }
    // 3. balanced split of long clauses
    const groups: Word[][] = [];
    clauses.forEach((c) => {
      const k = Math.max(1, Math.ceil(Math.max(c.length / MAX_WORDS, len(c) / MAX_CHARS)));
      if (k === 1) { groups.push(c); return; }
      let start = 0;
      for (let j = 1; j <= k; j++) {
        let end = j === k ? c.length : Math.round((c.length * j) / k);
        if (j < k) {
          let e2 = end;
          while (e2 > start + 2 && WEAK.has(clean(c[e2 - 1].text))) e2--;
          if (WEAK.has(clean(c[e2 - 1].text))) { e2 = end; while (e2 < c.length - 2 && WEAK.has(clean(c[e2 - 1].text))) e2++; }
          end = e2;
        }
        groups.push(c.slice(start, end)); start = end;
      }
    });
    groups.forEach((g, gi) => {
      const next = groups[gi + 1];
      const to = Math.min(shotEnds[si], next ? next[0].start : g[g.length - 1].end + 0.55);
      out.push({from: g[0].start - 0.04, to, text: g.map((w) => w.text.replace(/[.,!?:;]+$/, '')).join(' '), words: g.map((w) => clean(w.text))});
    });
  });
  return out;
};

export const Captions: React.FC<{chunks: Chunk[]; posAt: (t: number) => CapPos; emph: string[]}> = ({chunks, posAt, emph}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const c = chunks.find((k) => t >= k.from && t < k.to);
  const pos = posAt(t);
  if (!c || pos === 'none') return null;
  const u = clamp01((t - c.from) / 0.12);
  const parts = c.text.split(' ');
  return (
    <AbsoluteFill style={{justifyContent: pos === 'top' ? 'flex-start' : 'flex-end', alignItems: 'center', paddingBottom: 46, paddingTop: 46}}>
      <div style={{fontFamily: FONT_CAP, fontSize: 58, letterSpacing: 1.5, textTransform: 'uppercase', whiteSpace: 'nowrap', opacity: u, transform: `translateY(${(1 - u) * (pos === 'top' ? -10 : 10)}px)`,
        color: '#fff', WebkitTextStroke: `10px ${INK}`, paintOrder: 'stroke fill', textShadow: `0 4px 0 ${INK}`} as any}>
        {parts.map((p, i) => <span key={i} style={{color: emph.includes(c.words[i]) ? '#ffd23f' : '#fff'}}>{p}{i < parts.length - 1 ? ' ' : ''}</span>)}
      </div>
    </AbsoluteFill>
  );
};
