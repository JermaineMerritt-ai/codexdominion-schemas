module.exports = {
  preset: "ts-jest",
  testEnvironment: "node",
  roots: ["<rootDir>/apps", "<rootDir>/core", "<rootDir>/packages"],
  moduleFileExtensions: ["ts", "js", "json"],
  collectCoverage: true,
  coverageDirectory: "coverage"
};
