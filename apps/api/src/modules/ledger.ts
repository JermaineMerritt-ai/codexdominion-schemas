import { query } from '../db';

interface CreateActInput {
  type: string;
  title: string;
  lineage_tags?: string[];
  cycle: string;
  status: string;
  payload?: any;
}

export const ledger = {
  async createAct(input: CreateActInput) {
    const result = await query(
      `INSERT INTO acts (type, title, lineage_tags, cycle, status, payload)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [
        input.type,
        input.title,
        input.lineage_tags || [],
        input.cycle,
        input.status,
        JSON.stringify(input.payload || {})
      ]
    );
    return result.rows[0];
  },

  async getAct(id: string) {
    const result = await query(
      `SELECT a.*,
              s.seal_code,
              s.stamped_at,
              u.display_name as stamped_by_name
       FROM acts a
       LEFT JOIN seals s ON s.act_id = a.id
       LEFT JOIN users u ON s.stamped_by = u.id
       WHERE a.id = $1`,
      [id]
    );
    return result.rows[0];
  },

  async sealAct(actId: string, userId: string) {
    // Generate seal code
    const sealCode = `LEDGER-SEAL-${Math.random().toString(36).substring(2, 10).toUpperCase()}`;

    const result = await query(
      `INSERT INTO seals (act_id, seal_code, stamped_by)
       VALUES ($1, $2, $3)
       RETURNING *`,
      [actId, sealCode, userId]
    );

    // Update act status to sealed
    await query(
      `UPDATE acts SET status = 'sealed' WHERE id = $1`,
      [actId]
    );

    return {
      success: true,
      seal: result.rows[0],
      act: await this.getAct(actId)
    };
  },

  async listActs(filters?: { type?: string; cycle?: string; status?: string }) {
    let queryText = `
      SELECT a.*,
             s.seal_code,
             s.stamped_at,
             u.display_name as stamped_by_name
      FROM acts a
      LEFT JOIN seals s ON s.act_id = a.id
      LEFT JOIN users u ON s.stamped_by = u.id
      WHERE 1=1
    `;
    const params: any[] = [];

    if (filters?.type) {
      params.push(filters.type);
      queryText += ` AND a.type = $${params.length}`;
    }

    if (filters?.cycle) {
      params.push(filters.cycle);
      queryText += ` AND a.cycle = $${params.length}`;
    }

    if (filters?.status) {
      params.push(filters.status);
      queryText += ` AND a.status = $${params.length}`;
    }

    queryText += ` ORDER BY a.created_at DESC`;

    const result = await query(queryText, params);
    return result.rows;
  }
};
