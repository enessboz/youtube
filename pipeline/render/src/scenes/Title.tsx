import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Theme} from '../theme';
import type {TitleScene} from '../types';

export const Title: React.FC<{theme: Theme; scene: TitleScene}> = ({theme, scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const rise = (delay: number) => {
    const p = spring({frame: frame - delay, fps, config: {damping: 200}});
    return {opacity: p, transform: `translateY(${(1 - p) * 40}px)`};
  };
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', padding: 140, textAlign: 'center'}}>
      {scene.kicker && (
        <div
          style={{
            ...rise(4),
            fontFamily: theme.bodyFont,
            fontSize: 38,
            letterSpacing: 8,
            textTransform: 'uppercase',
            color: theme.main,
            marginBottom: 28,
          }}
        >
          {scene.kicker}
        </div>
      )}
      <div
        style={{
          ...rise(10),
          fontFamily: theme.titleFont,
          fontWeight: 800,
          fontSize: 118,
          lineHeight: 1.08,
          color: theme.ink,
          maxWidth: 1500,
        }}
      >
        {scene.title}
      </div>
      <div style={{...rise(14), width: 260, height: 8, background: theme.main, margin: '42px 0'}} />
      {scene.subtitle && (
        <div style={{...rise(20), fontFamily: theme.bodyFont, fontSize: 46, color: theme.second, maxWidth: 1400}}>
          {scene.subtitle}
        </div>
      )}
    </AbsoluteFill>
  );
};
