import { query } from '../db';

export const finance = {
  async summary() {
    // Get total revenue by source
    const revenueBySource = await query(
      `SELECT source,
              SUM(amount_cents) as total_cents,
              COUNT(*) as transaction_count,
              currency
       FROM finance_events
       WHERE event_type = 'charge'
       GROUP BY source, currency
       ORDER BY total_cents DESC`
    );

    // Get total revenue
    const totalRevenue = await query(
      `SELECT SUM(amount_cents) as total_cents,
              currency
       FROM finance_events
       WHERE event_type = 'charge'
       GROUP BY currency`
    );

    // Get recent events
    const recentEvents = await query(
      `SELECT *
       FROM finance_events
       ORDER BY occurred_at DESC
       LIMIT 10`
    );

    // Get revenue by store
    const revenueByStore = await query(
      `SELECT store_slug,
              SUM(amount_cents) as total_cents,
              COUNT(*) as transaction_count,
              currency
       FROM finance_events
       WHERE event_type = 'charge' AND store_slug IS NOT NULL
       GROUP BY store_slug, currency
       ORDER BY total_cents DESC`
    );

    return {
      total_revenue: totalRevenue.rows,
      revenue_by_source: revenueBySource.rows,
      revenue_by_store: revenueByStore.rows,
      recent_events: recentEvents.rows,
      summary: {
        total_transactions: recentEvents.rowCount,
        timestamp: new Date().toISOString()
      }
    };
  },

  async recordEvent(event: {
    source: string;
    amount_cents: number;
    currency: string;
    store_slug?: string;
    event_type: string;
    occurred_at: Date;
    meta?: any;
  }) {
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
        JSON.stringify(event.meta || {})
      ]
    );
    return result.rows[0];
  }
};
