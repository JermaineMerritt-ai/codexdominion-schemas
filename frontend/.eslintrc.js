module.exports = {
  extends: ['next/core-web-vitals'],
  root: true,
  rules: {
    'no-console': 'warn',
    'prefer-const': 'error',
    'react/no-inline-styles': 'off',
  },
  ignorePatterns: [
    'node_modules/',
    '.next/',
    'out/',
    'dist/',
    '*.config.js',
  ],
};
