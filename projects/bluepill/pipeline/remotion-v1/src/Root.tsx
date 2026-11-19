import React from 'react';
import {Composition} from 'remotion';
import {Video, TOTAL_FRAMES} from './Video';
import {FPS} from './lib/timing';
export const Root: React.FC = () => (
  <>
    <Composition id="Video1Draft" component={Video as any} width={1920} height={1080} fps={FPS} durationInFrames={TOTAL_FRAMES} defaultProps={{withAudio: true}} />
    <Composition id="Video1Silent" component={Video as any} width={1920} height={1080} fps={FPS} durationInFrames={TOTAL_FRAMES} defaultProps={{withAudio: false}} />
  </>
);
