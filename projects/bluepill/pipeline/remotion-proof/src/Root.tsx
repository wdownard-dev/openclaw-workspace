import React from 'react';
import {Composition} from 'remotion';
import {Proof} from './Proof';
import timing from '../data/timing.json';
export const Root: React.FC = () => (
  <Composition id="Proof16x9" component={Proof} width={1920} height={1080} fps={timing.fps}
    durationInFrames={Math.ceil(timing.duration * timing.fps)} />
);
