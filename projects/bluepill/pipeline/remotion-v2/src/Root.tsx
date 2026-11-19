import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import timing from '../data/timing.json';
export const Root: React.FC = () => (
  <Composition id="MythLedgerCyclopsV2" component={Video} width={1920} height={1080} fps={timing.fps}
    durationInFrames={Math.ceil(timing.duration * timing.fps)} />
);
