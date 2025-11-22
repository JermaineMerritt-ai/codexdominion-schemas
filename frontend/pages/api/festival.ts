import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

interface FestivalCycle {
  cycle_id: string;
  timestamp: string;
  ceremony_type: string;
  proclamation: string;
  rite: string;
  flame_status: string;
  recorded_by: string;
  sacred_checksum: string;
}

interface FestivalData {
  codex_festival_status: string;
  created: string;
  cycles: FestivalCycle[];
  total_ceremonies: number;
  last_ceremony?: string;
  last_updated?: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Try to read from both festival backup files
    const festivalFilePath = path.join(process.cwd(), '..', 'festival_local_backup.json');
    const ceremonialFilePath = path.join(process.cwd(), '..', 'ceremonial_inscriptions_backup.json');
    
    let festivalData: FestivalData = {
      codex_festival_status: 'AWAITING_FIRST_CEREMONY',
      created: new Date().toISOString(),
      cycles: [],
      total_ceremonies: 0
    };
    
    // Load regular festival data
    if (fs.existsSync(festivalFilePath)) {
      const fileContent = fs.readFileSync(festivalFilePath, 'utf-8');
      festivalData = JSON.parse(fileContent);
    }
    
    // Load and merge ceremonial inscriptions
    if (fs.existsSync(ceremonialFilePath)) {
      const ceremonialContent = fs.readFileSync(ceremonialFilePath, 'utf-8');
      const ceremonialData = JSON.parse(ceremonialContent);
      
      if (ceremonialData.cycles && ceremonialData.cycles.length > 0) {
        // Merge ceremonial cycles with festival cycles
        festivalData.cycles = [...(festivalData.cycles || []), ...ceremonialData.cycles];
        festivalData.total_ceremonies = festivalData.cycles.length;
        
        // Update status to reflect combined data
        if (festivalData.codex_festival_status === 'AWAITING_FIRST_CEREMONY') {
          festivalData.codex_festival_status = 'ACTIVE_WITH_CEREMONIAL';
        }
      }
    }

    // Parse query parameters
    const { limit, ceremony_type } = req.query;
    
    let cycles = festivalData.cycles || [];
    
    // Filter by ceremony type if specified
    if (ceremony_type && typeof ceremony_type === 'string') {
      cycles = cycles.filter(cycle => cycle.ceremony_type === ceremony_type);
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

    const response = {
      status: festivalData.codex_festival_status,
      total_ceremonies: festivalData.total_ceremonies,
      last_ceremony: festivalData.last_ceremony,
      last_updated: festivalData.last_updated,
      cycles: cycles,
      metadata: {
        filtered_count: cycles.length,
        total_count: festivalData.total_ceremonies,
        ceremony_types: Array.from(new Set(festivalData.cycles.map(c => c.ceremony_type))),
        flame_status: festivalData.cycles.length > 0 
          ? festivalData.cycles[festivalData.cycles.length - 1].flame_status 
          : 'awaiting_ignition'
      }
    };

    res.status(200).json(response);
    
  } catch (error) {
    console.error('Error reading festival data:', error);
    
    // Return graceful error response
    res.status(500).json({
      error: 'Failed to read festival data',
      status: 'ERROR',
      cycles: [],
      total_ceremonies: 0,
      message: 'The eternal flame flickers - festival data temporarily unavailable'
    });
  }
}