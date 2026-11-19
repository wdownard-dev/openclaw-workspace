import React from 'react';
import {Composition} from 'remotion';
import {Spike} from './Spike';
import TL from '../tl.json';
export const Root: React.FC = () => (
  <Composition id="Spike" component={Spike} width={1920} height={1080} fps={TL.fps} durationInFrames={Math.round(TL.duration * TL.fps)} />
);
