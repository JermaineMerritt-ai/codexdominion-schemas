# Identity Package

Identity and role-based authorization system for Codex Dominion.

## Features

- **User Management** - Get or create users by email
- **Role-Based Access Control (RBAC)** - Enforce role permissions
- **JWT Integration** - Works with Fastify JWT plugin
- **Sovereign Override** - Sovereign role bypasses all restrictions
- **Auto-provisioning** - New users default to steward role

## Roles

1. **sovereign** - Full system access (bypasses all restrictions)
2. **council** - Strategic oversight and approvals
3. **steward** - Day-to-day operations (default for new users)
4. **finance** - Financial tracking and reporting
5. **guest** - Read-only access

## Usage

```typescript
import { identity } from '@codex-dominion/identity';

// Get or create user
const user = await identity.getOrCreateUser('user@example.com');
// Returns: { id, email, role: { id, name, description } }

// Protect routes with role requirements
app.post('/prompts', {
  preValidation: identity.requireRole('steward', 'council', 'sovereign')
}, async (req, reply) => {
  // req.user is now available with verified role
  const user = (req as any).user;
  // ... handle request
});

// Sovereign-only endpoint
app.delete('/system/reset', {
  preValidation: identity.requireRole('sovereign')
}, async (req, reply) => {
  // Only sovereign can access
});
```

## Fastify Integration

```typescript
import Fastify from 'fastify';
import jwt from '@fastify/jwt';
import { identity } from '@codex-dominion/identity';

const app = Fastify();
await app.register(jwt, { secret: process.env.JWT_SECRET! });

// Login endpoint
app.post('/auth/login', async (req, reply) => {
  const { email } = req.body as { email: string };
  const user = await identity.getOrCreateUser(email);
  const token = app.jwt.sign({ sub: user.id, role: user.role });
  return { token, user };
});

// Protected endpoint
app.post('/prompts', {
  preValidation: identity.requireRole('steward', 'council')
}, async (req, reply) => {
  // User authenticated and authorized
});
```

## Development

```bash
npm install
npm run build
npm run dev  # watch mode
```
