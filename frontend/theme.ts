import 'styled-components';

declare module 'styled-components' {
  export interface DefaultTheme {
    colors: {
      primary: string;
      secondary: string;
    };
    spacing: {
      md: string;
    };
  }
}
export const theme = {
  colors: {
    primary: '#0044cc',
    secondary: '#888',
  },
  spacing: {
    md: '10px',
  },
};

export type ThemeType = typeof theme;
