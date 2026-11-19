import {StageProps} from './lib/Stage';
// One preset per scene = one grade, one key light shared by background and cutouts.
export const PRESETS: Record<string, StageProps> = {
  // moment 1: Odysseus and the Cyclops face to face in the cave, key light = campfire (frame x 0.717, y 0.62)
  fire: {
    bg: 'cave_inked_fire', bgPos: '50% 78%', bgBlur: 2, bgGrade: '#a4928c',
    light: {x: 0.717, y: 0.62, color: '#ff8f35', glow: 0.28, rim: 1.0, uplight: 0.12, pool: {r: 0.36, a: 0.5}},
    shade: '#3f3446', lit: '#ffe9d4',
    shadowDir: {sx: -1.15, sy: 0.14, alpha: 0.5, blur: 7},
    haze: {color: '#5a4a52', alpha: 0.3, horizon: 0.5}, grade: {color: '#e8903e', alpha: 0.16}, grain: 0.24, vignette: 0.6,
    figs: [
      {id: 'sh1', src: 'sheep', x: 0.465, y: 0.555, h: 0.13, blur: 1.2, haze: 0.18, shadow: 0.5, rim: 0.7},
      {id: 'sh2', src: 'sheep_f', x: 0.545, y: 0.565, h: 0.125, blur: 1.2, haze: 0.18, shadow: 0.5, rim: 0.7},
      {id: 'ody', src: 'ody', x: 0.60, y: 0.87, h: 0.40},
      {id: 'cy', src: 'cy', x: 0.28, y: 0.97, h: 0.84},
    ],
  },
  // moment 2: blinded Cyclops at the cave mouth, key light = low sun behind-left (frame x 0.34, y 0.44), rim from the sun
  sunrise: {
    bg: 'cave_inked_sunrise', bgPos: '50% 80%', bgBlur: 1.6, bgGrade: '#e6d6c4',
    light: {x: 0.34, y: 0.44, color: '#ffe3a0', glow: 0.3, rim: 1.0, pool: {r: 0.3, a: 0.22}},
    shade: '#3a3042', lit: '#d8c0ac',
    shadowDir: {sx: 0.55, sy: 0.33, alpha: 0.5, blur: 8},
    haze: {color: '#f6e2bd', alpha: 0.30, horizon: 0.52}, grade: {color: '#ffd9a0', alpha: 0.22}, grain: 0.2, vignette: 0.42,
    figs: [
      {id: 'sh3', src: 'sheep_f', x: 0.13, y: 0.84, h: 0.17, blur: 1.2, haze: 0.15, shadow: 0.6},
      {id: 'sh1', src: 'sheep_f', x: 0.40, y: 0.84, h: 0.19, blur: 0.6},
      {id: 'sh2', src: 'sheep_f', x: 0.255, y: 0.91, h: 0.25},
      {id: 'cy', src: 'cy_blind', x: 0.70, y: 0.96, h: 0.76},
    ],
  },
};
