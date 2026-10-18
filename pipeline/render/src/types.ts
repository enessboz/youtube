export type SceneBase = {
  id: string;
  duration_s: number;
  // Senaryodaki söylenen cümle (kelime-görsel eşleşmesi için)
  text_anchor?: string;
};

export type TitleScene = SceneBase & {
  type: 'title';
  kicker?: string;
  title: string;
  subtitle?: string;
};

export type NameCardScene = SceneBase & {
  type: 'namecard';
  number?: string; // "3/13"
  name: string;
  variants?: string[];
  job: string;
  body: string;
  region?: string;
};

export type PhotoScene = SceneBase & {
  type: 'photo';
  src: string; // assets/ altındaki dosya (video klasörü)
  caption?: string;
  credit?: string;
  motion?: 'pushin' | 'panleft' | 'panright';
};

export type Scene = TitleScene | NameCardScene | PhotoScene;

export type EpisodeProps = {
  channel: string;
  fps: number;
  scenes: Scene[];
};
