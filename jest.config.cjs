module.exports = {
  testMatch: ['**/?(*.)+(spec|test).[jt]s?(x)'],
  setupFilesAfterEnv: ['@testing-library/jest-dom'],
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.[jt]sx?$': 'babel-jest',
  },
  globals: {
    'babel-jest': {
      presets: ['@babel/preset-react'],
      plugins: ['@babel/plugin-syntax-jsx'],
    },
  },
};
