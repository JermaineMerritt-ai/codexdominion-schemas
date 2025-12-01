import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { filter } = req.query;

  const allLogs = [
    {
      id: 'log-1',
      timestamp: new Date().toISOString(),
      actor: 'CouncilSeal',
      action: 'POLICY_ENFORCEMENT',
      resource: 'security-policy-001',
      status: 'SUCCESS',
      severity: 'critical'
    },
    {
      id: 'log-2',
      timestamp: new Date(Date.now() - 300000).toISOString(),
      actor: 'sovereign-chatbot',
      action: 'SEND_MESSAGE',
      resource: 'agent-healthcare',
      status: 'SUCCESS',
      severity: 'low'
    },
    {
      id: 'log-3',
      timestamp: new Date(Date.now() - 600000).toISOString(),
      actor: 'CouncilSeal',
      action: 'APPROVE_CHANGE',
      resource: 'deploy-sovereign-commerce-v2.0.1',
      status: 'SUCCESS',
      severity: 'high'
    },
    {
      id: 'log-4',
      timestamp: new Date(Date.now() - 900000).toISOString(),
      actor: 'CustodianService',
      action: 'UPDATE_PACKAGE',
      resource: 'custodian-ui',
      status: 'SUCCESS',
      severity: 'medium'
    },
    {
      id: 'log-5',
      timestamp: new Date(Date.now() - 1200000).toISOString(),
      actor: 'agent-cybersecurity',
      action: 'THREAT_DETECTED',
      resource: 'system-firewall',
      status: 'FAILURE',
      severity: 'critical'
    },
    {
      id: 'log-6',
      timestamp: new Date(Date.now() - 1500000).toISOString(),
      actor: 'sovereign-observatory',
      action: 'HEALTH_CHECK',
      resource: 'all-sovereigns',
      status: 'SUCCESS',
      severity: 'low'
    }
  ];

  const filteredLogs = filter === 'all' 
    ? allLogs 
    : allLogs.filter(log => log.severity === filter);

  res.status(200).json({ logs: filteredLogs });
}
