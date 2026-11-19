import {staticFile} from 'remotion';
import dims from '../assetDims.json';
export const IMG = (n: string) => staticFile(`img/${n}.png`);
export const BG = (n: string) => staticFile(`bg/${n}.jpg`);
export const SFX = (n: string) => staticFile(`sfx/${n}.wav`);
export const dim = (n: string): {w: number; h: number} => (dims as any)[n];
