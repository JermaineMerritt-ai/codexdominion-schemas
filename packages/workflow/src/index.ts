import { query } from './db';

interface CreatePromptInput {
  dashboard_id: string;
  issuer_id: string;
  title: string;
  body: string;
}

interface Prompt {
  id: string;
  dashboard_id: string;
  issuer_id: string;
  title: string;
  body: string;
  status: string;
  created_at: Date;
  updated_at: Date;
}

// Simple in-memory queue for now
const taskQueue: Array<{ type: string; data: any }> = [];

const queue = {
  async enqueue(type: string, data: any) {
    taskQueue.push({ type, data });
    console.log(`[Queue] Enqueued ${type}:`, data);
    // In production, this would push to Redis/Bull/etc.
    return { queued: true, position: taskQueue.length };
  }
};

const db = {
  prompts: {
    async insert(data: CreatePromptInput & { status: string }) {
      const result = await query(
        `INSERT INTO prompts (dashboard_id, issuer_id, title, body, status)
         VALUES ($1, $2, $3, $4, $5)
         RETURNING *`,
        [data.dashboard_id, data.issuer_id, data.title, data.body, data.status]
      );
      return result.rows[0] as Prompt;
    },

    async get(id: string) {
      const result = await query(
        `SELECT * FROM prompts WHERE id = $1`,
        [id]
      );
      if (result.rows.length === 0) {
        throw new Error(`Prompt ${id} not found`);
      }
      return result.rows[0] as Prompt;
    },

    async update(id: string, data: { status: string }) {
      const result = await query(
        `UPDATE prompts SET status = $1, updated_at = NOW() WHERE id = $2 RETURNING *`,
        [data.status, id]
      );
      return result.rows[0] as Prompt;
    }
  },

  approvals: {
    async insert(data: { prompt_id: string; approver_id: string; decision: string }) {
      const result = await query(
        `INSERT INTO approvals (prompt_id, approver_id, decision)
         VALUES ($1, $2, $3)
         RETURNING *`,
        [data.prompt_id, data.approver_id, data.decision]
      );
      return result.rows[0];
    }
  }
};

const ledger = {
  async createAct(data: {
    type: string;
    title: string;
    cycle: string;
    status: string;
    lineage_tags: string[];
    payload: any;
  }) {
    const result = await query(
      `INSERT INTO acts (type, title, cycle, status, lineage_tags, payload)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [data.type, data.title, data.cycle, data.status, data.lineage_tags, JSON.stringify(data.payload)]
    );
    return result.rows[0];
  },

  async sealAct(actId: string, userId: string) {
    const sealCode = `LEDGER-SEAL-${Math.random().toString(36).substring(2, 10).toUpperCase()}`;
    const result = await query(
      `INSERT INTO seals (act_id, seal_code, stamped_by)
       VALUES ($1, $2, $3)
       RETURNING *`,
      [actId, sealCode, userId]
    );

    await query(
      `UPDATE acts SET status = 'sealed' WHERE id = $1`,
      [actId]
    );

    return result.rows[0];
  }
};

export const workflow = {
  async createPrompt(input: CreatePromptInput) {
    return db.prompts.insert({
      ...input,
      status: 'in_review'
    });
  },

  async executePrompt(promptId: string) {
    const prompt = await db.prompts.get(promptId);

    if (!['in_review', 'executing'].includes(prompt.status)) {
      throw new Error(`Invalid state: ${prompt.status}. Must be 'in_review' or 'executing'`);
    }

    await db.prompts.update(promptId, { status: 'executing' });

    // Enqueue real work (site/store rebuilds, social posting, etc.)
    await queue.enqueue('prompt-execution', { promptId });

    return { ok: true, status: 'executing' };
  },

  async approvePrompt(promptId: string, user: any) {
    const prompt = await db.prompts.get(promptId);

    await db.approvals.insert({
      prompt_id: promptId,
      approver_id: user.sub,
      decision: 'approved'
    });

    await db.prompts.update(promptId, { status: 'closed' });

    const act = await ledger.createAct({
      type: 'closure',
      title: `Closure: ${prompt.title}`,
      cycle: 'daily',
      status: 'approved',
      lineage_tags: ['Closure Scroll', 'Prompt'],
      payload: { prompt }
    });

    await ledger.sealAct(act.id, user.sub);

    return { ok: true, sealed_act_id: act.id };
  }
};
