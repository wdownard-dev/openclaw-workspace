import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import {Slice} from './Slice';
import TL from './timeline.json';
import SL from './slice_timeline.json';

export const Root: React.FC = () => (
  <>
    <Composition id="BluePill" component={Video} width={1920} height={1080} fps={(TL as any).fps} durationInFrames={(TL as any).total} />
    <Composition id="Slice" component={Slice} width={1920} height={1080} fps={(SL as any).fps} durationInFrames={(SL as any).total} />
  </>
);
