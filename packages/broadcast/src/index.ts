import { email } from './email';
import { channels } from './channels';
import { query } from './db';

interface BroadcastAssets {
  welcomeBanner: string;
  replayAnnouncement: string;
  invocationScript: string;
  cycleHymn: string;
  performanceGuide: string;
}

interface DispatchInput {
  targets: string[]; // emails, channel slugs, portal IDs
  assets: BroadcastAssets;
  schedule?: { cycle: 'daily' | 'seasonal' | 'epochal'; at?: string };
}

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

  async sealAct(actId: string, userId: string | null) {
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

export const broadcast = {
  async dispatchCapsule(input: DispatchInput) {
    // Email
    await email.send({
      to: input.targets.filter(t => t.includes('@')),
      subject: 'CodexDominion Broadcast Capsule',
      html: renderCapsule(input.assets)
    });

    // Social / channels
    await channels.dispatch({
      targets: input.targets.filter(t => !t.includes('@')),
      content: input.assets
    });

    const act = await ledger.createAct({
      type: 'broadcast',
      title: 'Ceremonial Broadcast Capsule',
      cycle: input.schedule?.cycle ?? 'daily',
      status: 'approved',
      lineage_tags: ['Broadcast Capsule', 'Invocation', 'Hymn', 'Performance'],
      payload: input
    });
    await ledger.sealAct(act.id, null);

    return { ok: true, act_id: act.id };
  }
};

const renderCapsule = (a: BroadcastAssets) => `
<h1>Welcome Banner</h1><p>${a.welcomeBanner}</p>
<h2>Replay Announcement</h2><p>${a.replayAnnouncement}</p>
<h2>Invocation Script</h2><pre>${a.invocationScript}</pre>
<h2>Cycle Hymn</h2><pre>${a.cycleHymn}</pre>
<h2>Performance Guide</h2><pre>${a.performanceGuide}</pre>
`;
