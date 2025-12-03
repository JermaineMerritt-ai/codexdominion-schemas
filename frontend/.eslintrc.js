module.exports = {
  extends: ['eslint:recommended', '@typescript-eslint/recommended', 'next/core-web-vitals'],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint', 'react'],
  root: true,
  env: {
    browser: true,
    node: true,
    es2022: true,
  },
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  rules: {
    '@typescript-eslint/no-unused-vars': 'warn',
    '@typescript-eslint/no-explicit-any': 'warn',
    'no-console': 'warn',
    'prefer-const': 'error',
    'react/no-inline-styles': 'off', // Disabled for production - inline styles allowed
  },
  ignorePatterns: [
    'node_modules/',
    '.next/',
    'out/',
    'dist/',
    '*.config.js',
    '**/test/**',
    '**/tests/**',
    '**/*.test.*',
    '**/*.spec.*',
    '**/demo/**',
    '**/demos/**',
    '**/*demo*.tsx',
    '**/*demo*.ts',
  ],
};
