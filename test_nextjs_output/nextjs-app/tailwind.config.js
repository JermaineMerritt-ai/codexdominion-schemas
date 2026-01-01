/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '{'50': '#1a1a1a0D', '100': '#1a1a1a1A', '200': '#1a1a1a33', '300': '#1a1a1a4D', '400': '#1a1a1a80', '500': '#1a1a1a', '600': '#1a1a1a', '700': '#1a1a1a', '800': '#1a1a1a', '900': '#1a1a1a'}',
        secondary: '{'50': '#f7f1e30D', '100': '#f7f1e31A', '200': '#f7f1e333', '300': '#f7f1e34D', '400': '#f7f1e380', '500': '#f7f1e3', '600': '#f7f1e3', '700': '#f7f1e3', '800': '#f7f1e3', '900': '#f7f1e3'}',
        accent: '{'50': '#d4af370D', '100': '#d4af371A', '200': '#d4af3733', '300': '#d4af374D', '400': '#d4af3780', '500': '#d4af37', '600': '#d4af37', '700': '#d4af37', '800': '#d4af37', '900': '#d4af37'}',
      },
      fontFamily: {
        heading: ['Inter', 'sans-serif'],
        body: ['Open Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
