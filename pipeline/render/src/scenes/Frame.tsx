import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Theme} from '../theme';

// Kağıt zemin + yarım ton köşe deseni + yumuşak giriş/çıkış.
export const Frame: React.FC<{theme: Theme; children: React.ReactNode; fadeIn?: number; fadeOut?: number}> = ({
  theme,
  children,
  fadeIn,
  fadeOut,
}) => {
  const frame = useCurrentFrame();
  const {durationInFrames, fps} = useVideoConfig();
  const fin = fadeIn ?? Math.round(0.4 * fps);
  const fout = fadeOut ?? Math.round(0.4 * fps);
  const opacity = Math.min(
    fin > 0 ? interpolate(frame, [0, fin], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1,
    fout > 0
      ? interpolate(frame, [durationInFrames - fout, durationInFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
      : 1,
  );
  const dots = (corner: 'tl' | 'br') => (
    <svg
      width={620}
      height={420}
      style={{position: 'absolute', [corner === 'tl' ? 'left' : 'right']: 0, [corner === 'tl' ? 'top' : 'bottom']: 0}}
    >
      {Array.from({length: 14 * 22}).map((_, i) => {
        const x = i % 22;
        const y = Math.floor(i / 22);
        const cx = corner === 'tl' ? x * 28 + (y % 2) * 14 : 620 - (x * 28 + (y % 2) * 14);
        const cy = corner === 'tl' ? y * 28 : 420 - y * 28;
        const k = 1 - Math.min(1, (x / 22 + y / 14) / 1.1);
        return <circle key={i} cx={cx} cy={cy} r={Math.max(0, 10 * k)} fill={theme.second} opacity={0.35} />;
      })}
    </svg>
  );
  return (
    <AbsoluteFill style={{backgroundColor: theme.paper, opacity}}>
      {dots('tl')}
      {dots('br')}
      {children}
    </AbsoluteFill>
  );
};
