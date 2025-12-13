/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'codex-navy': '#0f2b4a',
        'codex-parchment': '#f7f1e3',
        'codex-gold': '#d4af37',
        'codex-bronze': '#cd7f32',
        'codex-crimson': '#8b0000',
      },
    },
  },
  plugins: [],
}
