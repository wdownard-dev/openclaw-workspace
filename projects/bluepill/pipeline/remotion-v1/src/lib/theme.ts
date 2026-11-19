import {staticFile, delayRender, continueRender} from 'remotion';

// One family for ALL text: Noto Serif (SIL Open Font License, free for commercial use).
export const FONT = '"Noto Serif", Georgia, serif';
export const C = {
  bg: '#14100c', bg2: '#1d1812', paper: '#e9dec6', paperBg: '#e6dcc6', ink: '#241d15', muted: '#a99c83', dim: '#6f6452',
  rust: '#b8472a', rustHi: '#d2593a', sea: '#0f171e', land: '#2d271e', coast: '#8a7d65',
  line: 'rgba(233,222,198,0.30)', lineStrong: 'rgba(233,222,198,0.62)',
};

let loaded = false;
export const useFonts = () => {
  if (!loaded && typeof document !== 'undefined') {
    loaded = true;
    const h = delayRender('fonts');
    const f = (file: string, weight: string, style: string) => new FontFace('Noto Serif', `url(${staticFile('fonts/' + file)})`, {weight, style}).load();
    Promise.all([f('NotoSerif-Regular.ttf', '400', 'normal'), f('NotoSerif-Bold.ttf', '700', 'normal'), f('NotoSerif-Italic.ttf', '400', 'italic'), f('NotoSerif-BoldItalic.ttf', '700', 'italic')])
      .then((fs) => { fs.forEach((x) => (document as any).fonts.add(x)); continueRender(h); })
      .catch(() => continueRender(h));
  }
};

export const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
export const ramp = (t: number, a: number, b: number) => clamp01((t - a) / Math.max(1e-6, b - a));
export const easeOut = (u: number) => 1 - Math.pow(1 - clamp01(u), 3);
export const easeInOut = (u: number) => 0.5 - 0.5 * Math.cos(Math.PI * clamp01(u));
export const lerp = (a: number, b: number, u: number) => a + (b - a) * u;
