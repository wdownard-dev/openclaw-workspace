import React from 'react';
import {Composition} from 'remotion';
import {Clip, StillComp, CLIP_DUR} from './Video';
import {Stage} from './lib/Stage';
import {PRESETS} from './stagePresets';
import timing from '../data/timing.json';
export const Root: React.FC = () => (
  <>
    <Composition id="BluePillV3aClip" component={Clip} width={1920} height={1080} fps={timing.fps} durationInFrames={Math.ceil(CLIP_DUR * timing.fps)} />
    <Composition id="BluePillV3aStill" component={StillComp as any} width={1920} height={1080} fps={timing.fps} durationInFrames={300} defaultProps={{which: 0}} />
    <Composition id="CheapStage" component={((p: any) => <Stage {...PRESETS[p.scene]} />) as any} width={1920} height={1080} fps={timing.fps} durationInFrames={90} defaultProps={{scene: 'fire'}} />
  </>
);
