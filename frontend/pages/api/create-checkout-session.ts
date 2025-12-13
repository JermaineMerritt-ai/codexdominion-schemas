import type { NextApiRequest, NextApiResponse } from 'next';

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).end('Method Not Allowed');
  }

  try {
    const { productId, priceId, productName, productPrice } = req.body;

    // Create Checkout Session
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: priceId, // Stripe Price ID from products.json
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `${req.headers.origin}/order/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.headers.origin}/products/${productId}`,
      metadata: {
        product_id: productId,
        product_name: productName,
      },
    });

    res.status(200).json({ sessionId: session.id });
  } catch (err: any) {
    console.error('Stripe error:', err);
    res.status(500).json({ error: err.message });
  }
}
