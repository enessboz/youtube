import React from 'react';
import {Composition, Sequence} from 'remotion';
import {loadFonts} from './fonts';
import {themes} from './theme';
import {Frame} from './scenes/Frame';
import {Title} from './scenes/Title';
import {NameCard} from './scenes/NameCard';
import {Photo} from './scenes/Photo';
import {Clip} from './scenes/Clip';
import {Caption} from './scenes/Caption';
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

const Episode: React.FC<EpisodeProps> = ({channel, fps, scenes, crossfade_s}) => {
  loadFonts();
  const theme = themes[channel];
  const xf = Math.round((crossfade_s ?? 0) * fps);
  let from = 0;
  const bodies: React.ReactNode[] = [];
  const captions: React.ReactNode[] = [];
  scenes.forEach((s, i) => {
    const d = Math.max(1, Math.round(s.duration_s * fps));
    const last = i === scenes.length - 1;
    // Çapraz geçiş: sahne, sonrakinin başladığı yere xf kare taşar; sonraki üstte yumuşakça belirir.
    const ext = last || xf === 0 ? 0 : xf;
    bodies.push(
      <Sequence key={s.id} from={from} durationInFrames={d + ext}>
        <Frame theme={theme} fadeIn={xf > 0 ? (i === 0 ? 0 : xf) : undefined} fadeOut={xf > 0 ? (last ? xf : 0) : undefined}>
          {renderScene(theme, s)}
        </Frame>
      </Sequence>,
    );
    if (s.captions && s.captions.length) {
      let off = 0;
      s.captions.forEach((c, k) => {
        const cd = Math.max(1, Math.round(c.duration_s * fps));
        captions.push(
          <Sequence key={`c-${s.id}-${k}`} from={from + off} durationInFrames={cd}>
            <Caption theme={theme} text={c.text} />
          </Sequence>,
        );
        off += cd;
      });
    } else if (s.caption) {
      captions.push(
        <Sequence key={`c-${s.id}`} from={from} durationInFrames={d}>
          <Caption theme={theme} text={s.caption} />
        </Sequence>,
      );
    }
    from += d;
  });
  return (
    <>
      {bodies}
      {captions}
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
    defaultProps={{channel: 'gestern-gabs-das', fps: FPS, scenes: [] as Scene[], crossfade_s: 0}}
    calculateMetadata={({props}) => ({
      fps: props.fps,
      durationInFrames: Math.max(
        1,
        props.scenes.reduce((n, s) => n + Math.max(1, Math.round(s.duration_s * props.fps)), 0),
      ),
    })}
  />
);
