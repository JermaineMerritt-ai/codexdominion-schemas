import { query } from '../db';
import { ledger } from './ledger';

interface DispatchCapsuleInput {
  title: string;
  message: string;
  lineage_tags?: string[];
  target_dashboards?: string[];
}

export const broadcast = {
  async dispatchCapsule(input: DispatchCapsuleInput) {
    // Create a broadcast act
    const act = await ledger.createAct({
      type: 'broadcast',
      title: input.title,
      lineage_tags: input.lineage_tags || ['broadcast', 'capsule'],
      cycle: 'daily',
      status: 'approved',
      payload: {
        message: input.message,
        target_dashboards: input.target_dashboards || [],
        dispatched_at: new Date().toISOString()
      }
    });

    // In a real system, this would trigger notifications
    // to all target dashboards via WebSocket, email, etc.

    return {
      success: true,
      act,
      message: 'Broadcast capsule dispatched successfully'
    };
  },

  async listBroadcasts(limit: number = 20) {
    const result = await query(
      `SELECT a.*,
              s.seal_code,
              s.stamped_at
       FROM acts a
       LEFT JOIN seals s ON s.act_id = a.id
       WHERE a.type = 'broadcast'
       ORDER BY a.created_at DESC
       LIMIT $1`,
      [limit]
    );
    return result.rows;
  }
};
