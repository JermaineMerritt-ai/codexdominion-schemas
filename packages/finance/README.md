# Finance Package

Revenue tracking and financial analytics for Codex Dominion.

## Features

- **Event Ingestion** - Record financial events from multiple sources (Stripe, Shopify, etc.)
- **Revenue Aggregation** - Calculate total revenue by currency
- **MRR Calculation** - Track Monthly Recurring Revenue from subscriptions
- **Multi-currency Support** - Handle transactions in different currencies

## Usage

```typescript
import { finance } from '@codex-dominion/finance';

// Ingest a payment event
await finance.ingest({
  source: 'stripe',
  amount_cents: 2999,
  currency: 'USD',
  store_slug: 'main-store',
  event_type: 'payment_succeeded',
  occurred_at: new Date().toISOString(),
  meta: { customer_id: 'cus_123', invoice_id: 'inv_456' }
});

// Get financial summary
const summary = await finance.summary();
// Returns: { totals: [...], mrr: [...] }
```

## Webhook Integration

Example webhook handlers (to be implemented):

```typescript
// apps/api/src/webhooks/stripe.ts
export async function handleStripeWebhook(event: StripeEvent) {
  await finance.ingest({
    source: 'stripe',
    amount_cents: event.amount_captured,
    currency: event.currency.toUpperCase(),
    event_type: 'payment_succeeded',
    occurred_at: new Date(event.created * 1000).toISOString(),
    meta: event
  });
}
```

## Development

```bash
npm install
npm run build
npm run dev  # watch mode
```
