import { query } from '../db';

interface CreatePromptInput {
  dashboard_id: string;
  issuer_id: string;
  title: string;
  body: string;
}

export const workflow = {
  async createPrompt(input: CreatePromptInput) {
    const result = await query(
      `INSERT INTO prompts (dashboard_id, issuer_id, title, body, status)
       VALUES ($1, $2, $3, $4, 'draft')
       RETURNING *`,
      [input.dashboard_id, input.issuer_id, input.title, input.body]
    );
    return result.rows[0];
  },

  async getPrompt(id: string) {
    const result = await query(
      `SELECT p.*,
              u.email as issuer_email,
              u.display_name as issuer_name,
              d.name as dashboard_name
       FROM prompts p
       LEFT JOIN users u ON p.issuer_id = u.id
       LEFT JOIN dashboards d ON p.dashboard_id = d.id
       WHERE p.id = $1`,
      [id]
    );
    return result.rows[0];
  },

  async executePrompt(id: string) {
    // Update status to executing
    await query(
      `UPDATE prompts SET status = 'executing', updated_at = NOW() WHERE id = $1`,
      [id]
    );

    // Simulate execution logic
    const prompt = await this.getPrompt(id);

    // In a real system, this would trigger AI processing
    // For now, we'll just update status to awaiting_approval
    await query(
      `UPDATE prompts SET status = 'awaiting_approval', updated_at = NOW() WHERE id = $1`,
      [id]
    );

    return {
      success: true,
      message: 'Prompt executed successfully',
      prompt: await this.getPrompt(id)
    };
  },

  async approvePrompt(id: string, user: any) {
    // Record approval
    const approval = await query(
      `INSERT INTO approvals (prompt_id, approver_id, decision)
       VALUES ($1, $2, 'approved')
       RETURNING *`,
      [id, user.sub]
    );

    // Update prompt status
    await query(
      `UPDATE prompts SET status = 'closed', updated_at = NOW() WHERE id = $1`,
      [id]
    );

    return {
      success: true,
      approval: approval.rows[0],
      prompt: await this.getPrompt(id)
    };
  },

  async listPrompts(filters?: { status?: string; dashboard_id?: string }) {
    let queryText = `
      SELECT p.*,
             u.email as issuer_email,
             u.display_name as issuer_name,
             d.name as dashboard_name
      FROM prompts p
      LEFT JOIN users u ON p.issuer_id = u.id
      LEFT JOIN dashboards d ON p.dashboard_id = d.id
      WHERE 1=1
    `;
    const params: any[] = [];

    if (filters?.status) {
      params.push(filters.status);
      queryText += ` AND p.status = $${params.length}`;
    }

    if (filters?.dashboard_id) {
      params.push(filters.dashboard_id);
      queryText += ` AND p.dashboard_id = $${params.length}`;
    }

    queryText += ` ORDER BY p.created_at DESC`;

    const result = await query(queryText, params);
    return result.rows;
  }
};
