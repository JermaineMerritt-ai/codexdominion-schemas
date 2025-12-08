import { query } from './db';

interface CreateActInput {
  type: string;
  title: string;
  cycle: string;
  status: string;
  lineage_tags?: string[];
  payload?: any;
}

const db = {
  acts: {
    async insert(input: CreateActInput) {
      const result = await query(
        `INSERT INTO acts (type, title, cycle, status, lineage_tags, payload)
         VALUES ($1, $2, $3, $4, $5, $6)
         RETURNING *`,
        [
          input.type,
          input.title,
          input.cycle,
          input.status,
          input.lineage_tags || [],
          input.payload ? JSON.stringify(input.payload) : null
        ]
      );
      return result.rows[0];
    },

    async update(actId: string, data: { status: string }) {
      const result = await query(
        `UPDATE acts SET status = $1, updated_at = NOW() WHERE id = $2 RETURNING *`,
        [data.status, actId]
      );
      return result.rows[0];
    },

    async groupBy(field: string) {
      const result = await query(
        `SELECT ${field}, COUNT(*) as count
         FROM acts
         GROUP BY ${field}
         ORDER BY count DESC`
      );
      return result.rows;
    }
  },

  seals: {
    async insert(data: { act_id: string; seal_code: string; stamped_by: string | null }) {
      const result = await query(
        `INSERT INTO seals (act_id, seal_code, stamped_by)
         VALUES ($1, $2, $3)
         RETURNING *`,
        [data.act_id, data.seal_code, data.stamped_by]
      );
      return result.rows[0];
    }
  }
};

export const ledger = {
  async createAct(input: CreateActInput) {
    return db.acts.insert({ ...input });
  },

  async sealAct(actId: string, stampedBy: string | null) {
    const seal_code = `LEDGER-SEAL-${Math.random().toString(36).slice(2, 8).toUpperCase()}`;
    const seal = await db.seals.insert({ act_id: actId, seal_code, stamped_by: stampedBy });
    await db.acts.update(actId, { status: 'sealed' });
    return seal;
  },

  async indexByType() {
    return db.acts.groupBy('type');
  }
};
