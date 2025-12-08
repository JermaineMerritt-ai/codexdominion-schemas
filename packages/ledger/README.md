# Ledger Package

Sovereign ledger system for creating acts and cryptographic seals in Codex Dominion.

## Features

- **Act Creation** - Create sovereign acts with type, cycle, lineage tags, and payload
- **Act Sealing** - Generate cryptographic seal codes and mark acts as sealed
- **Type Indexing** - Aggregate acts by type for analytics
- **Lineage Tracking** - Tag acts with lineage for genealogy
- **Audit Trail** - Track who stamped each seal

## Usage

```typescript
import { ledger } from '@codex-dominion/ledger';

// Create an act
const act = await ledger.createAct({
  type: 'closure',
  title: 'Daily Cycle Closure',
  cycle: 'daily',
  status: 'approved',
  lineage_tags: ['Closure Scroll', 'Prompt'],
  payload: { summary: 'All systems operational' }
});

// Seal the act
const seal = await ledger.sealAct(act.id, 'user-uuid-here');
// Returns seal with code like: LEDGER-SEAL-A3F9K2

// Index acts by type
const index = await ledger.indexByType();
// Returns: [{ type: 'closure', count: 15 }, { type: 'broadcast', count: 8 }, ...]
```

## Act Types

Common act types:
- `closure` - Prompt closure acts
- `broadcast` - Ceremonial broadcast capsules
- `invocation` - System invocations
- `performance` - Performance recordings
- `cycle` - Cycle transitions

## Seal Format

Seals follow the pattern: `LEDGER-SEAL-XXXXXX`
- 6 random alphanumeric characters (uppercase)
- Cryptographically unique for audit purposes
- Immutable once stamped

## Development

```bash
npm install
npm run build
npm run dev  # watch mode
```
