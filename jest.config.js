module.exports = {
  projects: [
    {
      displayName: 'node',
      testEnvironment: "node",
      testMatch: [
        '<rootDir>/packages/**/__tests__/**/*.[jt]s?(x)',
        '<rootDir>/packages/**/?(*.)+(spec|test).[jt]s',
        '<rootDir>/template/**/?(*.)+(spec|test).[jt]s',
        '<rootDir>/codexdominion-schemas/templates/tests/**/?(*.)+(spec|test).[jt]s',
      ],
      testPathIgnorePatterns: ['/node_modules/', '/dist/'],
      moduleFileExtensions: ["ts", "js", "json", "node"],
    },
    {
      displayName: 'react',
      testEnvironment: "jsdom",
      testMatch: [
        '<rootDir>/frontend/**/?(*.)+(spec|test).[jt]sx?',
        '<rootDir>/codexdominion-schemas/frontend/**/?(*.)+(spec|test).[jt]sx?',
      ],
      testPathIgnorePatterns: ['/node_modules/', '/dist/'],
      moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json", "node"],
      setupFilesAfterEnv: ['<rootDir>/jest.setup.js']
    }
  ],
  watchPathIgnorePatterns: ['/node_modules/', '/dist/', '/\\.git/'],
  collectCoverageFrom: [
    '**/*.{js,jsx,ts,tsx}',
    '!**/*.d.ts',
    '!**/node_modules/**',
    '!**/.next/**',
    '!**/dist/**',
    '!**/coverage/**'
  ]
};
