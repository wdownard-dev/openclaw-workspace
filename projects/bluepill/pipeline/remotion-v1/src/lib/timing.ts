import shotsJ from '../data/shots_timed.json';
import wordsJ from '../data/words.json';

export const FPS = 30;
export type Shot = {shot: number; start: number; end: number; sec: number; type: string; asset: string; cam: string; note: string; narration: string; chapter: string};
export type Word = {text: string; start: number; end: number};
export const SHOTS: Shot[] = (shotsJ as any).shot_list;
export const WORDS: Word[] = wordsJ as any;
export const TOTAL: number = (shotsJ as any).total_sec;
export const shotOf = (n: number) => SHOTS.find((s) => s.shot === n)!;

export const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9Ͱ-Ͽ'’-]/g, '');
/** seconds after t0 at which the nth word matching `token` (prefix match, case/punctuation-insensitive) inside [t0,t1) starts; fallback if absent */
export const wordAt = (t0: number, t1: number, token: string, nth = 0, fallback = 0) => {
  const k = norm(token);
  let c = 0;
  for (const w of WORDS) {
    if (w.start < t0 - 1e-3 || w.start >= t1 - 1e-3) continue;
    if (norm(w.text).startsWith(k)) { if (c === nth) return Math.max(0, w.start - t0); c++; }
  }
  return fallback;
};
