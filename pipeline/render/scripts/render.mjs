#!/usr/bin/env node
// scenes.json -> mp4 (Remotion). Kullanım:
//   node scripts/render.mjs <kanal> <video-klasörü> [--out dosya.mp4] [--frames 0-149] [--still 30]
// Fontlar .cache/fonts'tan (scripts/make_channel_art.py indirir) ve video assets/ klasörü
// geçici bir public dizinine kopyalanır. Ses yok: süreler scenes.json'daki duration_s'ten gelir.
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const renderDir = path.resolve(here, '..');
const repo = path.resolve(renderDir, '..', '..');

const args = process.argv.slice(2);
const [channel, video] = args;
if (!channel || !video) {
  console.error('Kullanım: node scripts/render.mjs <kanal> <video-klasörü> [--out f.mp4] [--frames a-b] [--still n]');
  process.exit(2);
}
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};

const videoDir = path.join(repo, 'channels', channel, 'videos', video);
const scenesFile = path.join(videoDir, 'scenes.render.json');
if (!fs.existsSync(scenesFile)) {
  console.error(`Yok: ${scenesFile} (render sahne dosyası; docs/ARCHITECTURE.md)`);
  process.exit(2);
}
const data = JSON.parse(fs.readFileSync(scenesFile, 'utf-8'));
const inputProps = {channel, fps: data.fps ?? 30, scenes: data.scenes};

// Geçici public dizini: fontlar + video assets
const pub = path.join(repo, '.cache', 'render-public');
fs.rmSync(pub, {recursive: true, force: true});
fs.mkdirSync(path.join(pub, 'fonts'), {recursive: true});
const fontSrc = path.join(repo, '.cache', 'fonts');
const fontMap = {
  'Bitter[wght].ttf': 'Bitter.ttf',
  'PlayfairDisplay[wght].ttf': 'PlayfairDisplay.ttf',
  'Lato-Regular.ttf': 'Lato-Regular.ttf',
  'Lato-Bold.ttf': 'Lato-Bold.ttf',
};
for (const [from, to] of Object.entries(fontMap)) {
  const p = path.join(fontSrc, from);
  if (!fs.existsSync(p)) {
    console.error(`Font yok: ${p} (önce python3 scripts/make_channel_art.py çalıştır)`);
    process.exit(2);
  }
  fs.copyFileSync(p, path.join(pub, 'fonts', to));
}
const assets = path.join(videoDir, 'assets');
if (fs.existsSync(assets)) fs.cpSync(assets, path.join(pub, 'assets'), {recursive: true});

const browserExecutable =
  process.env.REMOTION_BROWSER ||
  ['/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', '/opt/pw-browsers/chromium/chrome-linux/chrome']
    .find((p) => fs.existsSync(p));

const serveUrl = await bundle({entryPoint: path.join(renderDir, 'src', 'index.ts'), publicDir: pub});
const composition = await selectComposition({serveUrl, id: 'Episode', inputProps, browserExecutable});
console.log(`süre: ${(composition.durationInFrames / composition.fps).toFixed(1)} sn, ${composition.durationInFrames} kare`);

const out = path.resolve(opt('--out') ?? path.join(videoDir, 'render', 'preview.mp4'));
fs.mkdirSync(path.dirname(out), {recursive: true});

if (opt('--still')) {
  const png = out.replace(/\.mp4$/, `-frame${opt('--still')}.png`);
  await renderStill({composition, serveUrl, output: png, frame: Number(opt('--still')), inputProps, browserExecutable});
  console.log('kare:', png);
} else {
  const fr = opt('--frames');
  await renderMedia({
    composition,
    serveUrl,
    outputLocation: out,
    codec: 'h264',
    inputProps,
    browserExecutable,
    frameRange: fr ? fr.split('-').map(Number) : null,
    muted: true,
    onProgress: ({progress}) => process.stdout.write(`\rrender %${Math.round(progress * 100)}`),
  });
  console.log('\nvideo:', out);
}
