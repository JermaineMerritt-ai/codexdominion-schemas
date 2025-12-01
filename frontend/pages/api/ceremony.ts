import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

interface CeremonialCycle {
  cycle_id: string;
  timestamp: string;
  ceremony_type: string;
  kind: 'proclamation' | 'silence' | 'blessing';
  message: string;
  proclamation?: string;
  rite: string;
  flame_status: string;
  recorded_by: string;
  sacred_checksum: string;
}

interface CeremonialData {
  codex_festival_status: string;
  created: string;
  cycles: CeremonialCycle[];
  total_ceremonies: number;
  last_ceremony?: string;
  last_updated?: string;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Try to read from the ceremonial inscriptions backup file
    const ceremonialFilePath = path.join(
      process.cwd(),
      '..',
      'ceremonial_inscriptions_backup.json'
    );

    let ceremonialData: CeremonialData;

    if (fs.existsSync(ceremonialFilePath)) {
      const fileContent = fs.readFileSync(ceremonialFilePath, 'utf-8');
      ceremonialData = JSON.parse(fileContent);
    } else {
      // Return empty state if no ceremonial data exists
      ceremonialData = {
        codex_festival_status: 'AWAITING_FIRST_CEREMONY',
        created: new Date().toISOString(),
        cycles: [],
        total_ceremonies: 0,
      };
    }

    // Parse query parameters
    const { limit, kind } = req.query;

    let cycles = ceremonialData.cycles || [];

    // Filter by ceremony kind if specified
    if (
      kind &&
      typeof kind === 'string' &&
      ['proclamation', 'silence', 'blessing'].includes(kind)
    ) {
      cycles = cycles.filter((cycle) => cycle.kind === kind);
    }

    // Apply limit if specified
    if (limit && typeof limit === 'string') {
      const limitNum = parseInt(limit, 10);
      if (!isNaN(limitNum) && limitNum > 0) {
        cycles = cycles.slice(-limitNum); // Get most recent cycles
      }
    }

    // Sort by timestamp (most recent first)
    cycles.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

    // Calculate ceremonial statistics
    const ceremonialStats = cycles.reduce(
      (acc, cycle) => {
        acc[cycle.kind] = (acc[cycle.kind] || 0) + 1;
        return acc;
      },
      {} as Record<string, number>
    );

    const response = {
      status: ceremonialData.codex_festival_status,
      total_ceremonies: ceremonialData.total_ceremonies,
      last_ceremony: ceremonialData.last_ceremony,
      last_updated: ceremonialData.last_updated,
      cycles: cycles,
      metadata: {
        filtered_count: cycles.length,
        total_count: ceremonialData.total_ceremonies,
        ceremonial_kinds: Object.keys(ceremonialStats),
        ceremonial_stats: ceremonialStats,
        flame_status:
          cycles.length > 0 ? cycles[cycles.length - 1].flame_status : 'awaiting_first_ceremony',
      },
    };

    res.status(200).json(response);
  } catch (error) {
    console.error('Error reading ceremonial data:', error);

    // Return graceful error response
    res.status(500).json({
      error: 'Failed to read ceremonial data',
      status: 'ERROR',
      cycles: [],
      total_ceremonies: 0,
      message: 'The sacred altar is temporarily unavailable - ceremonial data cannot be accessed',
    });
  }
}
