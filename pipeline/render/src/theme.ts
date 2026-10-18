export type Theme = {
  paper: string;
  ink: string;
  main: string;
  second: string;
  accent: string;
  titleFont: string;
  bodyFont: string;
};

// Renkler channels/<kanal>/brand/visual-style.md ile aynı tutulur.
export const themes: Record<string, Theme> = {
  'gestern-gabs-das': {
    paper: '#F3EBDD',
    ink: '#22303C',
    main: '#B24A33',
    second: '#2F6F73',
    accent: '#D9A441',
    titleFont: 'Bitter',
    bodyFont: 'Lato',
  },
  'quando-eravamo-noi': {
    paper: '#F4ECDD',
    ink: '#23344E',
    main: '#C8643B',
    second: '#6B7A3A',
    accent: '#D98F8F',
    titleFont: 'Playfair Display',
    bodyFont: 'Lato',
  },
};
