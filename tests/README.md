# 🧪 Testing Infrastructure

This directory contains unit and integration tests for the Codex Dominion Council Seal architecture.

## Directory Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── core/               # Core layer tests
│   │   ├── councilSeal.test.ts
│   │   ├── sovereigns.test.ts
│   │   ├── custodians.test.ts
│   │   └── flows.test.ts
│   ├── agents/             # Agent layer tests
│   └── customers/          # Customer portal tests
│
├── integration/            # Integration tests
│   ├── api/               # API endpoint tests
│   ├── workflows/         # End-to-end workflow tests
│   └── governance/        # Policy enforcement tests
│
├── fixtures/              # Test data and mocks
│   ├── policies.json
│   ├── sovereigns.json
│   └── audit-logs.json
│
└── helpers/               # Test utilities
    ├── setup.ts
    ├── teardown.ts
    └── mocks.ts
```

## Running Tests

### All Tests
```bash
npm test
```

### Unit Tests Only
```bash
npm run test:unit
```

### Integration Tests Only
```bash
npm run test:integration
```

### Watch Mode
```bash
npm run test:watch
```

### Coverage Report
```bash
npm run test:coverage
```

## Writing Tests

### Unit Test Example
```typescript
import { CouncilSealAuthority } from '../../core/councilSeal';

describe('CouncilSealAuthority', () => {
  let councilSeal: CouncilSealAuthority;

  beforeEach(() => {
    councilSeal = CouncilSealAuthority.getInstance();
  });

  it('should enforce security policy', () => {
    const result = councilSeal.enforcePolicy('security-policy-001', {
      data: { classification: 'sensitive' }
    });

    expect(result.allowed).toBe(false);
    expect(result.actions).toContain('ENCRYPT');
  });
});
```

### Integration Test Example
```typescript
import { SovereignService } from '../../core/sovereigns';
import { councilSeal } from '../../core/councilSeal';

describe('Sovereign Deployment Flow', () => {
  it('should require Council Seal approval for production deployment', async () => {
    const sovereigns = new SovereignService();
    const result = await sovereigns.deploySovereign('sovereign-commerce', '2.0.0');

    expect(result.success).toBe(false);
    expect(result.message).toContain('Council Seal');
  });
});
```

## Test Coverage Goals

- **Core Layer**: 90%+ coverage
- **Agents**: 80%+ coverage
- **Applications**: 85%+ coverage
- **Packages**: 90%+ coverage

## CI/CD Integration

Tests run automatically on:
- Every pull request
- Every push to main branch
- Pre-deployment validation
- Scheduled nightly runs

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on writing and maintaining tests.
