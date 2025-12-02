module.exports = {
  projects: [
    {
      displayName: 'node',
      testEnvironment: "node",
      testMatch: [
        '<rootDir>/packages/**/?(*.)+(spec|test).[jt]s',
        '<rootDir>/template/**/?(*.)+(spec|test).[jt]s',
      ],
      moduleFileExtensions: ["ts", "js", "json", "node"],
      passWithNoTests: true,
      collectCoverage: false,
      modulePathIgnorePatterns: ['<rootDir>/dist/', '<rootDir>/node_modules/']
    },
    {
      displayName: 'react',
      testEnvironment: "jsdom",
      testMatch: [
        '<rootDir>/frontend/**/?(*.)+(spec|test).[jt]sx?',
        '<rootDir>/apps/**/?(*.)+(spec|test).[jt]sx?',
      ],
      moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json", "node"],
      passWithNoTests: true,
      collectCoverage: false,
      modulePathIgnorePatterns: ['<rootDir>/dist/', '<rootDir>/node_modules/'],
      setupFilesAfterEnv: ['<rootDir>/jest.setup.js']
    }
  ],
  collectCoverageFrom: [
    '**/*.{js,jsx,ts,tsx}',
    '!**/*.d.ts',
    '!**/node_modules/**',
    '!**/.next/**',
    '!**/dist/**',
    '!**/coverage/**'
  ]
};
