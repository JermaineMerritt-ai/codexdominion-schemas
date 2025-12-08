# Shared Package

Shared utilities, database mocks, and common types for Codex Dominion packages.

## Features

- **Database Mock Layer** - Lightweight table interface for testing
- **Common Types** - Shared TypeScript interfaces
- **Utilities** - Helper functions used across packages

## Usage

```typescript
import { db } from '@codex-dominion/shared';

// Mock database operations
const prompt = await db.prompts.insert({
  title: 'Deploy Feature',
  body: 'Deploy new dashboard',
  status: 'in_review'
});

const act = await db.acts.get('act-id-123');
```

## Mock Interface

Each table provides:
- `insert(row)` - Create with auto-generated ID
- `get(id)` - Retrieve by ID
- `update(id, patch)` - Update fields
- `findBy(query)` - Query records
- `groupBy(key)` - Aggregate by field
- `aggregate(options)` - Complex aggregations
- `mrr()` - Monthly recurring revenue (finance_events only)

## Production Replacement

Replace with real ORM:
- **Prisma** - Type-safe ORM with migrations
- **Drizzle** - Lightweight TypeScript ORM
- **Knex** - SQL query builder

## Development

```bash
npm install
npm run build
npm run dev  # watch mode
```
