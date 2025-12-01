import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const products = [
    {
      id: 'prod-1',
      name: 'AI Development Suite',
      price: 299.99,
      description: 'Complete AI development toolkit with pre-trained models'
    },
    {
      id: 'prod-2',
      name: 'Healthcare Agent License',
      price: 499.99,
      description: 'Enterprise healthcare automation agent'
    },
    {
      id: 'prod-3',
      name: 'Legal Compliance System',
      price: 799.99,
      description: 'Automated legal compliance and audit system'
    },
    {
      id: 'prod-4',
      name: 'Cybersecurity Shield',
      price: 599.99,
      description: 'Advanced AI-powered cybersecurity monitoring'
    },
    {
      id: 'prod-5',
      name: 'Commerce Analytics Platform',
      price: 399.99,
      description: 'Real-time e-commerce analytics and insights'
    },
    {
      id: 'prod-6',
      name: 'Observatory Dashboard',
      price: 199.99,
      description: 'Comprehensive system monitoring and observability'
    }
  ];

  res.status(200).json({ products });
}
