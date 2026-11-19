// G2 theme (LOOK-G2.md): ink blue accent, verdigris chips, deep gold stamps on a cream halo.
export const C = {
  ink: '#1f3a5f',
  verd: '#2e7d73',
  gold: '#a8841c',
  cream: '#f3e9d2',
  outline: '#1a1204',
  white: '#ffffff',
  ground: '#f6f1e8', // class B cutaway ground (G2 decision: faintly tinted, not pure white)
  black: '#0b0a08',
  placeholder: '#9a9a9a',
  land: '#e8dfc3',
  coast: '#3a2f22',
  sea: '#7f98ab',
  cork: '#b98b5e',
  wood: '#4a2f1b',
  brass: '#c9a227',
};
export const HAND = '"Permanent Marker", "Comic Sans MS", cursive';
export const TYPE = '"Special Elite", "Courier New", monospace';
export const SZ = {chip: 48, stamp: 96, stampSmall: 64, bubble: 64, impact: 160};
export const W = 1920, H = 1080;
/** true when the ground is a painting, map, board or black: text goes cream with an ink outline, stamps get a halo */
export const onPaint = (bgType: string) => bgType !== 'white';
