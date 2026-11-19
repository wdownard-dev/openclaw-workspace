import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import TL from './timeline.json';

export const Root: React.FC = () => (
  <>
    <Composition id="BluePill" component={Video} width={1920} height={1080} fps={(TL as any).fps} durationInFrames={(TL as any).frames} defaultProps={{withAudio: false}} />
  </>
);
