module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier'
  ],
  plugins: ['react', '@typescript-eslint'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'react/no-inline-styles': 'off', // Disabled for production efficiency
  },
  ignorePatterns: [
    'node_modules/',
    'dist/',
    'build/',
    '*.config.js',
    '**/test/**',
    '**/*.test.*',
    '**/demo/**',
  ],
};
