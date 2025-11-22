import { NextApiRequest, NextApiResponse } from 'next';

const AVAILABLE_CAPSULES = [
  {
    slug: 'signals-daily',
    name: 'Daily Market Signals Analysis',
    description: 'Comprehensive market analysis with strategic positioning recommendations',
    schedule: '0 6 * * *',
    archive_type: 'snapshot'
  },
  {
    slug: 'dawn-dispatch',
    name: 'Dawn Sovereignty Dispatch',
    description: 'System status and operational sovereignty bulletin',
    schedule: '0 6 * * *',
    archive_type: 'bulletin'
  },
  {
    slug: 'treasury-audit',
    name: 'Treasury Sovereignty Audit',
    description: 'Financial portfolio analysis and risk assessment',
    schedule: '0 0 1 * *',
    archive_type: 'analysis_report'
  },
  {
    slug: 'sovereignty-bulletin',
    name: 'Sovereignty Status Bulletin',
    description: 'System independence and operational autonomy report',
    schedule: '0 12 * * *',
    archive_type: 'bulletin'
  },
  {
    slug: 'education-matrix',
    name: 'Educational Sovereignty Matrix',
    description: 'Learning competency assessment and knowledge gap analysis',
    schedule: '0 0 * * 1',
    archive_type: 'analysis_report'
  }
];

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  res.status(200).json({
    capsules: AVAILABLE_CAPSULES,
    total: AVAILABLE_CAPSULES.length,
    last_updated: new Date().toISOString()
  });
}