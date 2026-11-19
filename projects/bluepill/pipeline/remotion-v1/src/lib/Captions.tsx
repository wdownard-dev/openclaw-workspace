import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, FONT, clamp01} from './theme';
import {WORDS, Word} from './timing';

export type CapPos = 'bottom' | 'top' | 'none';
export type Chunk = {from: number; to: number; text: string; pos: CapPos; tone: 'light' | 'dark'};

const WEAK = new Set(['a', 'an', 'the', 'of', 'to', 'and', 'but', 'is', 'his', 'her', 'their', 'that', 'he', 'she', 'they', 'so', 'in', 'on', 'at', 'for', 'with', 'as', 'it', 'or', 'into', 'every', 'this', 'its', 'by', 'than', 'who', 'was', 'are', 'from']);
const clean = (w: string) => w.replace(/[^\w'-]/g, '').toLowerCase();
const MAX_WORDS = 8, MAX_CHARS = 50;
const len = (ws: Word[]) => ws.map((x) => x.text).join(' ').length;

/** Phrase chunks: split at punctuation, then balance long clauses; never end a chunk on a weak word, never leave a one-word orphan, never cross a segment boundary. */
export const buildChunks = (segs: {start: number; end: number; pos: CapPos; tone?: 'light' | 'dark'}[]): Chunk[] => {
  const out: Chunk[] = [];
  segs.forEach((seg) => {
    if (seg.pos === 'none') return;
    const ws = WORDS.filter((w) => w.start >= seg.start - 1e-3 && w.start < seg.end - 1e-3);
    if (!ws.length) return;
    const clauses: Word[][] = []; let cur: Word[] = [];
    ws.forEach((w) => { cur.push(w); if (/[.,!?:;]$/.test(w.text)) { clauses.push(cur); cur = []; } });
    if (cur.length) clauses.push(cur);
    for (let i = 0; i < clauses.length; i++) {
      if (clauses[i].length === 1 && clauses.length > 1) {
        if (i + 1 < clauses.length) { clauses[i + 1] = [...clauses[i], ...clauses[i + 1]]; clauses.splice(i, 1); i--; }
        else { clauses[i - 1] = [...clauses[i - 1], ...clauses[i]]; clauses.splice(i, 1); }
      }
    }
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
      const to = Math.min(seg.end, next ? next[0].start : g[g.length - 1].end + 0.5);
      out.push({from: g[0].start - 0.04, to, text: g.map((w) => w.text.replace(/[.,!?:;]+$/, '')).join(' '), pos: seg.pos, tone: seg.tone ?? 'light'});
    });
  });
  return out;
};

export const Captions: React.FC<{chunks: Chunk[]}> = ({chunks}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const c = chunks.find((k) => t >= k.from && t < k.to);
  if (!c) return null;
  const u = clamp01((t - c.from) / 0.1) * clamp01((c.to - t) / 0.08 + 0.001);
  return (
    <AbsoluteFill style={{justifyContent: c.pos === 'top' ? 'flex-start' : 'flex-end', alignItems: 'center', paddingBottom: 50, paddingTop: 50}}>
      <div style={{fontFamily: FONT, fontWeight: 700, fontSize: 40, letterSpacing: 0.4, whiteSpace: 'nowrap', opacity: Math.min(1, u), color: c.tone === 'dark' ? '#241d15' : '#f3ecdc',
        textShadow: c.tone === 'dark' ? '0 1px 2px rgba(255,250,235,0.85), 0 0 10px rgba(240,230,205,0.9)' : '0 2px 3px rgba(0,0,0,0.92), 0 0 12px rgba(0,0,0,0.78), 0 0 2px #000'}}>{c.text}</div>
    </AbsoluteFill>
  );
};
