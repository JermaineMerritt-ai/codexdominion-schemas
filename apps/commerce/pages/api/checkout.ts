import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { items } = req.body;

  if (!items || !Array.isArray(items) || items.length === 0) {
    return res.status(400).json({ error: 'Invalid cart items' });
  }

  // Simulate order processing
  const orderId = `order-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

  res.status(200).json({
    success: true,
    orderId,
    items: items.length,
    message: 'Order processed successfully'
  });
}
