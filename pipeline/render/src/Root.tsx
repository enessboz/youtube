import React from 'react';
import {Composition, Sequence} from 'remotion';
import {loadFonts} from './fonts';
import {themes} from './theme';
import {Frame} from './scenes/Frame';
import {Title} from './scenes/Title';
import {NameCard} from './scenes/NameCard';
import {Photo} from './scenes/Photo';
import {Clip} from './scenes/Clip';
import type {EpisodeProps, Scene} from './types';

const FPS = 30;

const renderScene = (theme: (typeof themes)[string], scene: Scene) => {
  switch (scene.type) {
    case 'title':
      return <Title theme={theme} scene={scene} />;
    case 'namecard':
      return <NameCard theme={theme} scene={scene} />;
    case 'photo':
      return <Photo theme={theme} scene={scene} />;
    case 'clip':
      return <Clip theme={theme} scene={scene} />;
  }
};

const Episode: React.FC<EpisodeProps> = ({channel, fps, scenes}) => {
  loadFonts();
  const theme = themes[channel];
  let from = 0;
  return (
    <>
      {scenes.map((s) => {
        const d = Math.max(1, Math.round(s.duration_s * fps));
        const el = (
          <Sequence key={s.id} from={from} durationInFrames={d}>
            <Frame theme={theme}>{renderScene(theme, s)}</Frame>
          </Sequence>
        );
        from += d;
        return el;
      })}
    </>
  );
};

export const Root: React.FC = () => (
  <Composition
    id="Episode"
    component={Episode}
    width={1920}
    height={1080}
    fps={FPS}
    durationInFrames={FPS * 5}
    defaultProps={{channel: 'gestern-gabs-das', fps: FPS, scenes: [] as Scene[]}}
    calculateMetadata={({props}) => ({
      fps: props.fps,
      durationInFrames: Math.max(
        1,
        props.scenes.reduce((n, s) => n + Math.max(1, Math.round(s.duration_s * props.fps)), 0),
      ),
    })}
  />
);
