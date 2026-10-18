import {continueRender, delayRender, staticFile} from 'remotion';

// render.mjs fontları public/fonts altına bu adlarla kopyalar.
const FILES: Record<string, {file: string; weight: string}> = {
  Bitter: {file: 'fonts/Bitter.ttf', weight: '100 900'},
  'Playfair Display': {file: 'fonts/PlayfairDisplay.ttf', weight: '400 900'},
  Lato: {file: 'fonts/Lato-Regular.ttf', weight: '400'},
  'Lato Bold': {file: 'fonts/Lato-Bold.ttf', weight: '700'},
};

let started = false;
export const loadFonts = () => {
  if (started) return;
  started = true;
  const handle = delayRender('fonts');
  Promise.all(
    Object.entries(FILES).map(async ([family, {file, weight}]) => {
      const face = new FontFace(family, `url(${staticFile(file)})`, {weight});
      await face.load();
      document.fonts.add(face);
    }),
  )
    .catch((e) => console.error('font yüklenemedi', e))
    .finally(() => continueRender(handle));
};
