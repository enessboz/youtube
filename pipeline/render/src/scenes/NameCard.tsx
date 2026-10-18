import React from 'react';
import {AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Theme} from '../theme';
import type {NameCardScene} from '../types';

const LABEL = (theme: Theme): React.CSSProperties => ({
  fontSize: 24,
  letterSpacing: 4,
  color: theme.main,
  textTransform: 'uppercase',
});

// "Namens-Karteikarte": satırlı kart, kırmızı başlık çizgisi, gravür, damga.
export const NameCard: React.FC<{theme: Theme; scene: NameCardScene}> = ({theme, scene}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const card = spring({frame, fps, config: {damping: 18, stiffness: 120}});
  const text = spring({frame: frame - 12, fps, config: {damping: 200}});
  const pic = spring({frame: frame - 18, fps, config: {damping: 200}});
  const stamp = spring({frame: frame - 30, fps, config: {damping: 10, stiffness: 140}});
  const drift = (frame / durationInFrames) * 0.06;
  const hasImage = Boolean(scene.image);
  const stampWord = scene.job.split(/[ ,/(]/)[0];
  const stampSize = Math.max(20, Math.min(34, Math.floor(150 / (0.72 * stampWord.length))));
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <div
        style={{
          width: 1560,
          height: 820,
          background: '#FBF7EE',
          borderRadius: 14,
          boxShadow: '0 30px 70px rgba(34,48,60,0.28)',
          transform: `translateY(${(1 - card) * 120}px) rotate(${(1 - card) * -2 - 0.5}deg)`,
          opacity: card,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* kart çizgileri */}
        <div style={{position: 'absolute', left: 0, right: 0, top: 150, height: 6, background: theme.main}} />
        {Array.from({length: 10}).map((_, i) => (
          <div
            key={i}
            style={{position: 'absolute', left: 60, right: 60, top: 236 + i * 58, height: 2, background: '#D5DDE0'}}
          />
        ))}
        {/* başlık */}
        <div style={{position: 'absolute', left: 60, top: 30, display: 'flex', alignItems: 'baseline', gap: 28}}>
          <div style={{fontFamily: theme.titleFont, fontWeight: 800, fontSize: 98, color: theme.ink}}>{scene.name}</div>
          {scene.number && (
            <div style={{fontFamily: theme.bodyFont, fontSize: 34, color: theme.main, letterSpacing: 4}}>{scene.number}</div>
          )}
        </div>
        {/* sol sütun */}
        <div
          style={{
            position: 'absolute',
            left: 60,
            top: 178,
            width: hasImage ? 820 : 1100,
            opacity: text,
            transform: `translateY(${(1 - text) * 20}px)`,
          }}
        >
          <div style={{fontFamily: theme.titleFont, fontWeight: 700, fontSize: 52, color: theme.second}}>= {scene.job}</div>
          <div style={{fontFamily: theme.bodyFont, fontSize: 40, lineHeight: '58px', color: theme.ink, marginTop: 16}}>
            {scene.body}
          </div>
          <div style={{display: 'flex', gap: 56, marginTop: 34, fontFamily: theme.bodyFont, fontSize: 32, color: theme.ink}}>
            {scene.variants && scene.variants.length > 0 && (
              <div>
                <div style={LABEL(theme)}>Varianten</div>
                <div style={{marginTop: 6}}>{scene.variants.join(' · ')}</div>
              </div>
            )}
            {scene.region && (
              <div>
                <div style={LABEL(theme)}>Verbreitung</div>
                <div style={{marginTop: 6}}>{scene.region}</div>
              </div>
            )}
          </div>
        </div>
        {/* gravür */}
        {hasImage && (
          <div
            style={{
              position: 'absolute',
              right: 60,
              top: 190,
              width: 560,
              height: 580,
              opacity: pic,
              transform: `rotate(1.2deg) translateY(${(1 - pic) * 30}px)`,
              boxShadow: '0 12px 30px rgba(34,48,60,0.25)',
              background: '#F1E9D6',
              padding: 14,
            }}
          >
            <div style={{width: '100%', height: 510, overflow: 'hidden', background: '#EFE6D0'}}>
              <Img
                src={staticFile(scene.image!)}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  mixBlendMode: 'multiply',
                  transform: `scale(${1.02 + drift})`,
                }}
              />
            </div>
            {scene.image_caption && (
              <div style={{fontFamily: theme.bodyFont, fontSize: 21, color: theme.ink, marginTop: 8, textAlign: 'center'}}>
                {scene.image_caption}
              </div>
            )}
          </div>
        )}
        {/* damga */}
        <div
          style={{
            position: 'absolute',
            left: 560,
            bottom: 56,
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
            fontSize: stampSize,
            textTransform: 'uppercase',
            textAlign: 'center',
            lineHeight: 1.1,
            padding: 14,
            transform: `scale(${0.6 + stamp * 0.4}) rotate(${-14 + stamp * 4}deg)`,
            opacity: stamp * 0.9,
          }}
        >
          {stampWord}
        </div>
      </div>
    </AbsoluteFill>
  );
};
