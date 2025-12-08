import { query } from './db';

interface FinanceEvent {
  source: string;
  amount_cents: number;
  currency: string;
  store_slug?: string;
  event_type: string;
  occurred_at: string;
  meta?: any;
}

const db = {
  finance_events: {
    async insert(event: FinanceEvent) {
      const result = await query(
        `INSERT INTO finance_events (source, amount_cents, currency, store_slug, event_type, occurred_at, meta)
         VALUES ($1, $2, $3, $4, $5, $6, $7)
         RETURNING *`,
        [
          event.source,
          event.amount_cents,
          event.currency,
          event.store_slug || null,
          event.event_type,
          event.occurred_at,
          event.meta ? JSON.stringify(event.meta) : null
        ]
      );
      return result.rows[0];
    },

    async aggregate(options: { by: string[]; sum: string[] }) {
      // Aggregate total revenue by currency
      const result = await query(
        `SELECT
           currency,
           SUM(amount_cents) as total_cents,
           COUNT(*) as transaction_count
         FROM finance_events
         GROUP BY currency
         ORDER BY total_cents DESC`
      );
      return result.rows;
    },

    async mrr() {
      // Calculate Monthly Recurring Revenue from subscription events
      const result = await query(
        `SELECT
           currency,
           SUM(amount_cents) as mrr_cents
         FROM finance_events
         WHERE event_type IN ('subscription_created', 'subscription_renewed')
           AND occurred_at >= NOW() - INTERVAL '30 days'
         GROUP BY currency`
      );
      return result.rows;
    }
  }
};

export const finance = {
  async ingest(event: FinanceEvent) {
    await db.finance_events.insert(event);
  },

  async summary() {
    const totals = await db.finance_events.aggregate({
      by: ['currency'],
      sum: ['amount_cents']
    });
    const mrr = await db.finance_events.mrr();
    return { totals, mrr };
  }
};
