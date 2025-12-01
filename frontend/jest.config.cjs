module.exports = {
  testMatch: ['**/?(*.)+(spec|test).[jt]s?(x)'],
  setupFilesAfterEnv: ['../node_modules/@testing-library/jest-dom/extend-expect'],
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
