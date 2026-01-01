/**
 * Premium Error States
 * ====================
 * Payment and subscription error handling
 */

"use client"

import { AlertCircle, CreditCard, RefreshCw, XCircle } from 'lucide-react'

/**
 * Payment Failure Error
 * "Payment method could not be processed."
 */
export function PaymentFailureError({ onRetry, onUpdatePayment }: { onRetry: () => void; onUpdatePayment: () => void }) {
  return (
    <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
      <div className="flex items-start gap-4">
        <div className="p-3 bg-red-100 rounded-full">
          <CreditCard className="h-6 w-6 text-red-600" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-red-900 mb-2">
            Payment method could not be processed
          </h3>
          <p className="text-red-800 mb-4">
            Your payment failed. Please update your payment method or try again.
          </p>
          <div className="flex gap-3">
            <button
              onClick={onUpdatePayment}
              className="px-6 py-2.5 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors"
            >
              Update Payment Method
            </button>
            <button
              onClick={onRetry}
              className="px-6 py-2.5 border-2 border-red-600 text-red-600 font-semibold rounded-lg hover:bg-red-50 transition-colors flex items-center gap-2"
            >
              <RefreshCw className="h-4 w-4" />
              Try Again
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

/**
 * Upgrade Failure Error
 * "Unable to upgrade — try again."
 */
export function UpgradeFailureError({ onRetry, onContactSupport }: { onRetry: () => void; onContactSupport: () => void }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
      <AlertCircle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
      <div className="flex-1">
        <h4 className="font-semibold text-red-900 mb-1">Unable to upgrade</h4>
        <p className="text-sm text-red-800 mb-3">
          Something went wrong while processing your upgrade. Please try again or contact support.
        </p>
        <div className="flex gap-3">
          <button
            onClick={onRetry}
            className="text-sm text-red-800 hover:text-red-900 font-medium underline"
          >
            Try Again
          </button>
          <button
            onClick={onContactSupport}
            className="text-sm text-red-800 hover:text-red-900 font-medium underline"
          >
            Contact Support
          </button>
        </div>
      </div>
    </div>
  )
}

/**
 * Subscription Load Failure
 * "Unable to load subscription details."
 */
export function SubscriptionLoadError({ onRetry }: { onRetry: () => void }) {
  return (
    <div className="bg-orange-50 border border-orange-200 rounded-lg p-12 text-center">
      <XCircle className="h-12 w-12 text-orange-600 mx-auto mb-4" />
      <h3 className="text-xl font-semibold text-gray-900 mb-2">
        Unable to load subscription details
      </h3>
      <p className="text-gray-600 mb-6">
        We're having trouble loading your subscription. Please try again.
      </p>
      <button
        onClick={onRetry}
        className="px-8 py-3 bg-orange-600 text-white font-semibold rounded-lg hover:bg-orange-700 transition-colors flex items-center gap-2 mx-auto"
      >
        <RefreshCw className="h-5 w-5" />
        Retry
      </button>
    </div>
  )
}

/**
 * Downgrade Confirmation
 * Shows what user will lose when downgrading
 */
export function DowngradeConfirmation({ 
  fromTier, 
  toTier, 
  onConfirm, 
  onCancel 
}: { 
  fromTier: string
  toTier: string
  onConfirm: () => void
  onCancel: () => void
}) {
  const featureLoss = {
    'premium-to-free': [
      'Unlimited alerts → 5 alerts max',
      'Unlimited AI summaries → 5/day',
      'Earnings alerts',
      'Full analytics',
      'Multi-source news breakdown'
    ],
    'pro-to-premium': [
      'Multi-portfolio support',
      'CSV export',
      'Institutional-grade charts',
      'Priority support'
    ],
    'pro-to-free': [
      'All Premium features',
      'All Pro features',
      'Multi-portfolio support',
      'CSV export',
      'Priority support'
    ]
  }

  const lossKey = fromTier === 'pro' && toTier === 'premium' ? 'pro-to-premium' :
                  fromTier === 'pro' && toTier === 'free' ? 'pro-to-free' :
                  'premium-to-free'

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-3">Confirm Downgrade</h3>
        <p className="text-gray-600 mb-4">
          You're downgrading from <span className="font-semibold">{fromTier}</span> to <span className="font-semibold">{toTier}</span>.
        </p>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <p className="text-sm font-semibold text-yellow-900 mb-2">You'll lose access to:</p>
          <ul className="space-y-1">
            {featureLoss[lossKey].map((feature, index) => (
              <li key={index} className="text-sm text-yellow-800">• {feature}</li>
            ))}
          </ul>
          <p className="text-xs text-yellow-700 mt-3">
            Changes take effect at the end of your current billing cycle.
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={onCancel}
            className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors"
          >
            Keep {fromTier}
          </button>
          <button
            onClick={onConfirm}
            className="flex-1 px-6 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors"
          >
            Confirm Downgrade
          </button>
        </div>
      </div>
    </div>
  )
}

/**
 * Cancellation Confirmation
 * Shows retention offer and confirms cancellation
 */
export function CancellationConfirmation({ 
  currentTier, 
  onConfirm, 
  onCancel 
}: { 
  currentTier: string
  onConfirm: () => void
  onCancel: () => void
}) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-3">Cancel Subscription?</h3>
        <p className="text-gray-600 mb-6">
          We're sorry to see you go! You'll retain access to {currentTier} features until the end of your billing cycle.
        </p>
        
        {/* Retention Offer */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <p className="text-sm font-semibold text-blue-900 mb-2">Before you go...</p>
          <p className="text-sm text-blue-800">
            Is there anything we can improve? <a href="/feedback" className="underline font-medium">Send us feedback</a> and help make DominionMarkets better.
          </p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onCancel}
            className="flex-1 px-6 py-3 bg-dominion-gold text-dominion-obsidian font-semibold rounded-lg hover:bg-yellow-500 transition-colors"
          >
            Keep Subscription
          </button>
          <button
            onClick={onConfirm}
            className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors"
          >
            Cancel Anyway
          </button>
        </div>
      </div>
    </div>
  )
}
