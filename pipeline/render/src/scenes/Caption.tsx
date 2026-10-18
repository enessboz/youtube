import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Theme} from '../theme';

// Sessiz önizleme için altyazı: anlatıcı yerine senaryo cümlesi (en çok 2 satır).
export const Caption: React.FC<{theme: Theme; text: string}> = ({theme, text}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const o = interpolate(frame, [0, 6, durationInFrames - 6, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 54, opacity: o}}>
      <div
        style={{
          maxWidth: 1500,
          background: 'rgba(20,28,36,0.78)',
          color: '#FBF7EE',
          fontFamily: theme.bodyFont,
          fontWeight: 700,
          fontSize: 46,
          lineHeight: 1.25,
          textAlign: 'center',
          padding: '12px 36px',
          borderRadius: 6,
          display: '-webkit-box',
          WebkitLineClamp: 2,
          WebkitBoxOrient: 'vertical',
          overflow: 'hidden',
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
