/**
 * Premium Gate Overlay
 * ====================
 * Paywall for premium features
 */

"use client"

import { Crown, X, Check } from 'lucide-react'

interface PremiumGateOverlayProps {
  feature: string
  requiredTier: 'premium' | 'pro'
  currentTier: string
  onClose: () => void
  onUpgrade: () => void
}

const TIER_BENEFITS = {
  premium: {
    price: '$14.99/mo',
    benefits: [
      'Earnings alerts',
      'Custom alert conditions',
      'Unlimited price & news alerts',
      'Volume spike alerts',
      'Multi-source news alerts',
      'Historical volume context',
      'Identity-filtered alerts',
      '50+ alerts per type'
    ]
  },
  pro: {
    price: '$29.99/mo',
    benefits: [
      'Everything in Premium, plus:',
      'SMS notifications',
      'CSV alert export',
      'Multi-portfolio alert sets',
      'Priority support',
      'Advanced analytics',
      'Unlimited alerts',
      'Early access to features'
    ]
  }
}

const FEATURE_DESCRIPTIONS: Record<string, string> = {
  'earnings_alert': 'Get notified before and after earnings releases with detailed summaries',
  'custom_conditions': 'Create complex alert conditions with multiple triggers and thresholds',
  'volume_spike': 'Track unusual trading activity with historical volume context',
  'multi_source_news': 'Receive alerts only when multiple sources confirm the same story',
  'unlimited_alerts': 'Create as many alerts as you need without restrictions',
  'sms_notifications': 'Get instant SMS alerts for time-sensitive market events',
  'csv_export': 'Export your alert history and analysis to CSV for record-keeping',
  'multi_portfolio_alerts': 'Set up alert sets across multiple portfolios simultaneously'
}

export default function PremiumGateOverlay({
  feature,
  requiredTier,
  currentTier,
  onClose,
  onUpgrade
}: PremiumGateOverlayProps) {
  const tierInfo = TIER_BENEFITS[requiredTier]
  const featureDescription = FEATURE_DESCRIPTIONS[feature] || 'This feature requires a premium subscription'

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="relative p-6 bg-gradient-to-br from-dominion-gold via-yellow-400 to-dominion-gold">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors"
          >
            <X className="h-5 w-5 text-white" />
          </button>
          
          <div className="flex items-center gap-4">
            <div className="p-4 rounded-xl bg-white bg-opacity-20 backdrop-blur">
              <Crown className="h-10 w-10 text-white" />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-white mb-1">
                Upgrade to {requiredTier.charAt(0).toUpperCase() + requiredTier.slice(1)}
              </h2>
              <p className="text-yellow-100 text-lg">
                {tierInfo.price}
              </p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Feature Description */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-gray-800 font-medium">
              {featureDescription}
            </p>
          </div>

          {/* Current Tier Status */}
          {currentTier !== 'free' && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <p className="text-sm text-gray-600">
                You're currently on <span className="font-semibold">{currentTier.charAt(0).toUpperCase() + currentTier.slice(1)}</span> plan. 
                {requiredTier === 'pro' ? ' Upgrade to Pro to unlock this feature.' : ' Consider upgrading for more features.'}
              </p>
            </div>
          )}

          {/* Benefits List */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              What you'll get:
            </h3>
            <div className="grid gap-3">
              {tierInfo.benefits.map((benefit, index) => (
                <div key={index} className="flex items-start gap-3">
                  <div className="mt-0.5 p-1 rounded-full bg-green-100">
                    <Check className="h-4 w-4 text-green-600" />
                  </div>
                  <p className="text-gray-700">{benefit}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Comparison Table */}
          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-gray-900">Feature</th>
                  <th className="px-4 py-3 text-center font-semibold text-gray-900">Free</th>
                  <th className="px-4 py-3 text-center font-semibold text-gray-900 bg-yellow-50">
                    {requiredTier === 'premium' ? 'Premium' : 'Pro'}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr>
                  <td className="px-4 py-3 text-gray-700">Price Alerts</td>
                  <td className="px-4 py-3 text-center text-gray-600">5</td>
                  <td className="px-4 py-3 text-center font-semibold text-gray-900 bg-yellow-50">
                    {requiredTier === 'pro' ? 'Unlimited' : '50'}
                  </td>
                </tr>
                <tr>
                  <td className="px-4 py-3 text-gray-700">News Alerts</td>
                  <td className="px-4 py-3 text-center text-gray-600">3</td>
                  <td className="px-4 py-3 text-center font-semibold text-gray-900 bg-yellow-50">
                    {requiredTier === 'pro' ? 'Unlimited' : '20'}
                  </td>
                </tr>
                <tr>
                  <td className="px-4 py-3 text-gray-700">Earnings Alerts</td>
                  <td className="px-4 py-3 text-center text-gray-600">—</td>
                  <td className="px-4 py-3 text-center font-semibold text-gray-900 bg-yellow-50">✓</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 text-gray-700">Volume Spike</td>
                  <td className="px-4 py-3 text-center text-gray-600">—</td>
                  <td className="px-4 py-3 text-center font-semibold text-gray-900 bg-yellow-50">✓</td>
                </tr>
                {requiredTier === 'pro' && (
                  <>
                    <tr>
                      <td className="px-4 py-3 text-gray-700">SMS Notifications</td>
                      <td className="px-4 py-3 text-center text-gray-600">—</td>
                      <td className="px-4 py-3 text-center font-semibold text-gray-900 bg-yellow-50">✓</td>
                    </tr>
                    <tr>
                      <td className="px-4 py-3 text-gray-700">CSV Export</td>
                      <td className="px-4 py-3 text-center text-gray-600">—</td>
                      <td className="px-4 py-3 text-center font-semibold text-gray-900 bg-yellow-50">✓</td>
                    </tr>
                  </>
                )}
              </tbody>
            </table>
          </div>

          {/* Money-Back Guarantee */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
            <p className="text-green-900 font-medium">
              ✅ 30-Day Money-Back Guarantee
            </p>
            <p className="text-sm text-green-700 mt-1">
              Not satisfied? Get a full refund within 30 days, no questions asked.
            </p>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex items-center gap-3 p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={onClose}
            className="flex-1 px-6 py-3 bg-white border-2 border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors"
          >
            Maybe Later
          </button>
          <button
            onClick={onUpgrade}
            className="flex-1 px-6 py-3 bg-gradient-to-r from-dominion-gold to-yellow-400 text-dominion-obsidian font-bold rounded-lg hover:shadow-lg transition-all flex items-center justify-center gap-2"
          >
            <Crown className="h-5 w-5" />
            Upgrade to {requiredTier.charAt(0).toUpperCase() + requiredTier.slice(1)}
          </button>
        </div>
      </div>
    </div>
  )
}
