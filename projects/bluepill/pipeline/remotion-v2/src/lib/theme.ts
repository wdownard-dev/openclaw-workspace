import {staticFile, delayRender, continueRender} from 'remotion';

export const FONT_IMPACT = 'Bangers, Impact, sans-serif';   // hand-lettered impact words and titles (SIL OFL, Google Fonts)
export const FONT_CAP = '"Lilita One", "Arial Black", sans-serif'; // captions and labels (SIL OFL, Google Fonts)
export const INK = '#1b1520';
export const GOLD = '#ffd23f';
export const RED = '#ff4b3e';

let loaded = false;
export const useFonts = () => {
  // idempotent; blocks the first frame until both fonts are ready
  if (!loaded && typeof document !== 'undefined') {
    loaded = true;
    const h = delayRender('fonts');
    Promise.all([
      new FontFace('Bangers', `url(${staticFile('fonts/Bangers.ttf')})`).load(),
      new FontFace('Lilita One', `url(${staticFile('fonts/LilitaOne.ttf')})`).load(),
    ]).then((fs) => { fs.forEach((f) => (document as any).fonts.add(f)); continueRender(h); })
      .catch(() => continueRender(h));
  }
};

export const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
export const easeOut = (u: number) => 1 - Math.pow(1 - clamp01(u), 3);
export const easeInOut = (u: number) => { u = clamp01(u); return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };
export const hash = (s: string) => { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return Math.abs(h); };
