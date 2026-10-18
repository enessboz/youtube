import React from 'react';
import {AbsoluteFill, OffthreadVideo, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Theme} from '../theme';
import type {ClipScene} from '../types';

// Kanalın renk dilinde hafif düzeltme: tüm stok klipler aynı "görünüme" oturur.
const GRADES: Record<string, string> = {
  warm: 'sepia(0.18) saturate(0.82) contrast(1.06) brightness(0.97)',
  neutral: 'saturate(0.9) contrast(1.04)',
  cool: 'saturate(0.8) contrast(1.05) hue-rotate(-6deg)',
};

export const Clip: React.FC<{theme: Theme; scene: ClipScene}> = ({theme, scene}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const slide = spring({frame: frame - 14, fps, config: {damping: 200}});
  const out = Math.min(1, (durationInFrames - frame) / 12);
  const grain = `url("data:image/svg+xml;utf8,${encodeURIComponent(
    `<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='${frame % 8}'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>`,
  )}")`;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <OffthreadVideo
        src={staticFile(scene.src)}
        startFrom={Math.round((scene.trim_start_s ?? 0) * fps)}
        playbackRate={scene.playback_rate ?? 1}
        muted
        style={{width: '100%', height: '100%', objectFit: 'cover', filter: GRADES[scene.grade ?? 'warm']}}
      />
      {/* vinyet + ince film greni */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(20,14,8,0.45) 100%)'}} />
      <AbsoluteFill style={{backgroundImage: grain, opacity: 0.1, mixBlendMode: 'overlay'}} />
      {scene.label && (
        <div
          style={{
            position: 'absolute',
            left: 90,
            bottom: 110,
            opacity: Math.min(slide, out),
            transform: `translateX(${(1 - slide) * -60}px)`,
          }}
        >
          <div style={{background: theme.ink, color: theme.paper, fontFamily: theme.titleFont, fontWeight: 800, fontSize: 72, padding: '10px 34px'}}>
            {scene.label.title}
          </div>
          {scene.label.subtitle && (
            <div style={{background: theme.main, color: '#fff', fontFamily: theme.bodyFont, fontSize: 34, padding: '8px 34px', display: 'inline-block'}}>
              {scene.label.subtitle}
            </div>
          )}
        </div>
      )}
    </AbsoluteFill>
  );
};
