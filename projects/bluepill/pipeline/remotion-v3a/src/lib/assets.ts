import {staticFile} from 'remotion';
import dims from '../assetDims.json';
import dims3 from '../assetDims3.json';
const A: any = dims3;
export const IMG = (n: string) => (A[n] ? staticFile(`img3/${n}.png`) : staticFile(`img/${n}.png`));
export const BG = (n: string) => staticFile(`bg/${n}.jpg`);
export const SFX = (n: string) => staticFile(`sfx/${n}.wav`);
export const dim = (n: string): {w: number; h: number} => A[n] ?? (dims as any)[n];
