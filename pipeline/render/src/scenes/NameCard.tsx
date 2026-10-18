import React from 'react';
import {AbsoluteFill, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Theme} from '../theme';
import type {NameCardScene} from '../types';

// "Namens-Karteikarte": satırlı kart, kırmızı başlık çizgisi, damga.
export const NameCard: React.FC<{theme: Theme; scene: NameCardScene}> = ({theme, scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const card = spring({frame, fps, config: {damping: 18, stiffness: 120}});
  const text = spring({frame: frame - 12, fps, config: {damping: 200}});
  const stamp = spring({frame: frame - 24, fps, config: {damping: 10, stiffness: 140}});
  const lines = Array.from({length: 9});
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <div
        style={{
          width: 1500,
          height: 780,
          background: '#FBF7EE',
          borderRadius: 14,
          boxShadow: '0 30px 70px rgba(34,48,60,0.28)',
          transform: `translateY(${(1 - card) * 120}px) rotate(${(1 - card) * -2 - 0.6}deg)`,
          opacity: card,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <div style={{position: 'absolute', left: 0, right: 0, top: 150, height: 6, background: theme.main}} />
        {lines.map((_, i) => (
          <div
            key={i}
            style={{position: 'absolute', left: 60, right: 60, top: 240 + i * 62, height: 2, background: '#CFD8DC'}}
          />
        ))}
        <div style={{position: 'absolute', left: 60, top: 36, display: 'flex', alignItems: 'baseline', gap: 28}}>
          <div style={{fontFamily: theme.titleFont, fontWeight: 800, fontSize: 96, color: theme.ink}}>
            {scene.name}
          </div>
          {scene.number && (
            <div style={{fontFamily: theme.bodyFont, fontSize: 34, color: theme.main, letterSpacing: 4}}>
              {scene.number}
            </div>
          )}
        </div>
        <div
          style={{
            position: 'absolute',
            left: 60,
            right: 460,
            top: 190,
            opacity: text,
            transform: `translateY(${(1 - text) * 20}px)`,
          }}
        >
          <div style={{fontFamily: theme.titleFont, fontWeight: 700, fontSize: 54, color: theme.second}}>
            = {scene.job}
          </div>
          <div style={{fontFamily: theme.bodyFont, fontSize: 40, lineHeight: '62px', color: theme.ink, marginTop: 18}}>
            {scene.body}
          </div>
        </div>
        {(scene.variants?.length || scene.region) && (
          <div
            style={{
              position: 'absolute',
              right: 56,
              top: 190,
              width: 330,
              fontFamily: theme.bodyFont,
              fontSize: 30,
              color: theme.ink,
              opacity: text,
              textAlign: 'right',
              lineHeight: '44px',
            }}
          >
            {scene.variants && scene.variants.length > 0 && (
              <div>
                <div style={{fontSize: 24, letterSpacing: 4, color: theme.main, textTransform: 'uppercase'}}>Varianten</div>
                {scene.variants.join(' · ')}
              </div>
            )}
            {scene.region && (
              <div style={{marginTop: 26}}>
                <div style={{fontSize: 24, letterSpacing: 4, color: theme.main, textTransform: 'uppercase'}}>Verbreitung</div>
                {scene.region}
              </div>
            )}
          </div>
        )}
        <div
          style={{
            position: 'absolute',
            right: 60,
            bottom: 50,
            width: 190,
            height: 190,
            borderRadius: '50%',
            border: `8px solid ${theme.main}`,
            color: theme.main,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontFamily: theme.titleFont,
            fontWeight: 800,
            fontSize: 34,
            textTransform: 'uppercase',
            textAlign: 'center',
            lineHeight: 1.1,
            padding: 14,
            transform: `scale(${0.6 + stamp * 0.4}) rotate(${-14 + stamp * 4}deg)`,
            opacity: stamp * 0.9,
          }}
        >
          {scene.job.split(/[ ,/]/)[0]}
        </div>
      </div>
    </AbsoluteFill>
  );
};
