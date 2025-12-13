'use client';

import { useRouter } from 'next/router';
import Link from 'next/link';
import { useEffect, useState } from 'react';

function OrderSuccess() {
  const router = useRouter();
  const { session_id } = router.query;
  const [orderDetails, setOrderDetails] = useState<any>(null);

  useEffect(() => {
    if (session_id) {
      // TODO: Fetch order details from Stripe using session_id
      // For now, show generic success message
      setOrderDetails({ sessionId: session_id });
    }
  }, [session_id]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 flex items-center justify-center">
      <div className="max-w-2xl mx-auto px-6 text-center">
        <div className="bg-gradient-to-br from-gray-800/90 to-purple-900/80 rounded-3xl p-12 border-4 border-gold-500/50 shadow-2xl">
          <div className="text-8xl mb-6">✓</div>

          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-gold-300 via-yellow-300 to-gold-400 bg-clip-text text-transparent">
            Order Successful!
          </h1>

          <p className="text-xl text-purple-200 mb-8">
            Thank you for your purchase! Your order has been confirmed.
          </p>

          <div className="bg-gray-900/60 rounded-xl p-6 mb-8 border-2 border-purple-600/50">
            <h2 className="text-2xl font-bold text-gold-300 mb-4">What's Next?</h2>
            <ul className="space-y-3 text-left text-purple-200">
              <li className="flex items-start">
                <span className="text-gold-400 mr-3 text-2xl">📧</span>
                <span>Check your email for order confirmation and download links</span>
              </li>
              <li className="flex items-start">
                <span className="text-gold-400 mr-3 text-2xl">⬇️</span>
                <span>Download your products immediately (links never expire)</span>
              </li>
              <li className="flex items-start">
                <span className="text-gold-400 mr-3 text-2xl">📚</span>
                <span>Access your purchases anytime from your account</span>
              </li>
              <li className="flex items-start">
                <span className="text-gold-400 mr-3 text-2xl">💬</span>
                <span>Need help? Contact support@codexdominion.app</span>
              </li>
            </ul>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/products">
              <button className="px-8 py-4 bg-gradient-to-r from-gold-500 to-amber-500 hover:from-gold-600 hover:to-amber-600 rounded-xl font-bold text-lg transition-all duration-300 shadow-lg">
                Continue Shopping
              </button>
            </Link>
            <Link href="/">
              <button className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-xl font-bold text-lg transition-all duration-300 shadow-lg border-2 border-purple-400">
                Return Home
              </button>
            </Link>
          </div>

          {/* Order Details */}
          {session_id && (
            <div className="mt-8 text-sm text-purple-300">
              <p>Order Reference: {session_id}</p>
            </div>
          )}
        </div>

        {/* Testimonial */}
        <div className="mt-12 bg-gray-800/60 rounded-xl p-6 border-2 border-purple-600/30">
          <p className="text-purple-200 italic mb-4">
            "I absolutely love the Daily Flame devotional! It's transformed my morning routine and given me
            so much clarity for my business decisions. Worth every penny!"
          </p>
          <p className="text-white font-bold">— Sarah M., Customer</p>
        </div>
      </div>
    </div>
  );
}

export default OrderSuccess;

export async function getServerSideProps() {
  return { props: {} };
}
