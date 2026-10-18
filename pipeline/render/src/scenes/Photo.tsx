import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Theme} from '../theme';
import type {PhotoScene} from '../types';

// Arşiv fotoğrafı: kağıt çerçeve, yavaş hareket, kaynak etiketi.
export const Photo: React.FC<{theme: Theme; scene: PhotoScene}> = ({theme, scene}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const t = interpolate(frame, [0, durationInFrames], [0, 1]);
  const motion = scene.motion ?? 'pushin';
  const scale = motion === 'pushin' ? 1.04 + t * 0.1 : 1.12;
  const tx = motion === 'panleft' ? (0.5 - t) * 80 : motion === 'panright' ? (t - 0.5) * 80 : 0;
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <div
        style={{
          width: 1560,
          height: 860,
          padding: 22,
          background: '#FBF7EE',
          boxShadow: '0 30px 70px rgba(34,48,60,0.3)',
          transform: 'rotate(-0.6deg)',
          position: 'relative',
        }}
      >
        <div style={{width: '100%', height: '100%', overflow: 'hidden', background: '#999'}}>
          <Img
            src={staticFile(scene.src)}
            style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${scale}) translateX(${tx}px)`}}
          />
        </div>
        {scene.caption && (
          <div
            style={{
              position: 'absolute',
              left: 22,
              bottom: 22,
              background: theme.ink,
              color: theme.paper,
              fontFamily: theme.bodyFont,
              fontSize: 36,
              padding: '14px 28px',
            }}
          >
            {scene.caption}
          </div>
        )}
        {scene.credit && (
          <div
            style={{
              position: 'absolute',
              right: 30,
              bottom: 30,
              fontFamily: theme.bodyFont,
              fontSize: 22,
              color: '#fff',
              textShadow: '0 1px 4px rgba(0,0,0,0.8)',
            }}
          >
            {scene.credit}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
