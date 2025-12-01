import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const metrics = [
    {
      name: 'Requests/sec',
      value: 600 + Math.random() * 100,
      change: (Math.random() - 0.5) * 20,
      unit: ''
    },
    {
      name: 'Response Time',
      value: 250 + Math.random() * 100,
      change: (Math.random() - 0.5) * 15,
      unit: 'ms'
    },
    {
      name: 'Error Rate',
      value: Math.random() * 2,
      change: (Math.random() - 0.5) * 10,
      unit: '%'
    },
    {
      name: 'CPU Usage',
      value: 45 + Math.random() * 30,
      change: (Math.random() - 0.5) * 15,
      unit: '%'
    },
    {
      name: 'Memory Usage',
      value: 60 + Math.random() * 20,
      change: (Math.random() - 0.5) * 10,
      unit: '%'
    },
    {
      name: 'Active Users',
      value: 1200 + Math.random() * 300,
      change: (Math.random() - 0.5) * 25,
      unit: ''
    }
  ];

  res.status(200).json({ metrics });
}
