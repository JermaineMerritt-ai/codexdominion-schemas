import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgres://codex:codex@localhost:5432/dominion',
});

export const query = async (text: string, params?: any[]) => {
  const start = Date.now();
  const res = await pool.query(text, params);
  const duration = Date.now() - start;
  console.log('[Ledger DB]', { text: text.substring(0, 50), duration, rows: res.rowCount });
  return res;
};

export default { query };
