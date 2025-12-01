module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['@testing-library/jest-dom'],
  testMatch: ['**/*.test.(js|jsx|ts|tsx)'],
  collectCoverage: true,
  coverageReporters: ['text', 'lcov'],
};
