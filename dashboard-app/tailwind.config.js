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
        codex: {
          purple: '#667eea',
          'purple-dark': '#764ba2',
          bg: '#f7f1e3',
          'bg-light': '#efe7d4',
        },
        // CodexDominion Sovereign Palette
        sovereign: {
          gold: '#F5C542',
          blue: '#3B82F6',
          emerald: '#10B981',
          obsidian: '#0F172A',
          slate: '#1E293B',
          violet: '#7C3AED',
          crimson: '#DC2626',
        },
      },
    },
  },
  plugins: [],
};
