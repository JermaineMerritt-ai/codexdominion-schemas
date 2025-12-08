# Workflow Package

Workflow management system for Codex Dominion.

## Features

- **Prompt Creation** - Create AI prompts with review status
- **Prompt Execution** - Execute prompts and enqueue background tasks
- **Prompt Approval** - Approve prompts and create sealed acts in ledger
- **Database Integration** - Direct PostgreSQL access
- **Queue System** - Task queue for background processing

## Usage

```typescript
import { workflow } from '@codex-dominion/workflow';

// Create prompt
const prompt = await workflow.createPrompt({
  dashboard_id: 'uuid',
  issuer_id: 'uuid',
  title: 'Deploy new feature',
  body: 'Details about the deployment'
});

// Execute prompt
await workflow.executePrompt(prompt.id);

// Approve prompt (creates sealed act)
const result = await workflow.approvePrompt(prompt.id, { sub: 'user-uuid' });
```

## Development

```bash
npm install
npm run build
npm run dev  # watch mode
```
