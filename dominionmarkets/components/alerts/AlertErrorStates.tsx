/**
 * Alert Error States
 * ==================
 * Error and empty state components for Alerts Center
 */

"use client"

import { Bell, AlertTriangle, RefreshCw } from 'lucide-react'

interface ErrorStateProps {
  onRetry?: () => void
}

/**
 * Alerts Empty State
 * "No alerts created yet"
 */
export function AlertsEmptyState({ onCreate }: { onCreate: () => void }) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-16 text-center">
      <Bell className="h-20 w-20 text-gray-300 mx-auto mb-4" />
      <h3 className="text-2xl font-semibold text-gray-900 mb-2">
        No Alerts Yet
      </h3>
      <p className="text-gray-600 mb-2">
        Get notified about price changes, news, earnings, and more.
      </p>
      <p className="text-sm text-gray-500 mb-6">
        Create your first alert to start receiving market signals.
      </p>
      <button
        onClick={onCreate}
        className="px-8 py-3 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors"
      >
        Create Your First Alert
      </button>
    </div>
  )
}

/**
 * Alerts Load Error
 * "Unable to load alerts"
 */
export function AlertsLoadError({ onRetry }: ErrorStateProps) {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-sm border border-red-200 p-12 text-center">
          <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Unable to Load Alerts
          </h3>
          <p className="text-gray-600 mb-6">
            We're having trouble loading your alerts. Please try again.
          </p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="inline-flex items-center px-6 py-3 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Retry
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

/**
 * No Triggered Alerts
 * "Your alerts haven't triggered yet"
 */
export function NoTriggersState() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
      <div className="text-6xl mb-4">📭</div>
      <h3 className="text-xl font-semibold text-gray-900 mb-2">
        No Triggered Alerts
      </h3>
      <p className="text-gray-600">
        Your alerts haven't triggered yet. We'll notify you when they do.
      </p>
    </div>
  )
}

/**
 * Invalid Stock Symbol Error
 */
export function InvalidSymbolError({ symbol, onClose }: { symbol: string; onClose: () => void }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <div className="flex items-start">
        <AlertTriangle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h4 className="font-semibold text-red-900 mb-1">
            Invalid Stock Symbol
          </h4>
          <p className="text-sm text-red-800">
            The ticker "{symbol}" was not found. Please check the symbol and try again.
          </p>
        </div>
        <button
          onClick={onClose}
          className="text-red-600 hover:text-red-800 ml-3"
        >
          ✕
        </button>
      </div>
    </div>
  )
}

/**
 * Limit Reached Error
 */
export function LimitReachedError({ 
  alertType, 
  currentCount, 
  limit, 
  tier 
}: { 
  alertType: string
  currentCount: number
  limit: number
  tier: string
}) {
  return (
    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
      <div className="text-4xl mb-3">🔒</div>
      <h3 className="font-semibold text-yellow-900 mb-2">
        Alert Limit Reached
      </h3>
      <p className="text-sm text-yellow-800 mb-4">
        You've used all {limit} {alertType} alerts ({tier} tier).
      </p>
      <p className="text-sm text-yellow-700 mb-6">
        Upgrade to {tier === 'free' ? 'Premium' : 'Pro'} for {tier === 'free' ? '50' : 'unlimited'} {alertType} alerts.
      </p>
      <button className="px-6 py-2 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors">
        Upgrade Now
      </button>
    </div>
  )
}

/**
 * Alert Creation Failure
 * "Unable to create alert — try again"
 */
export function AlertCreationError({ message, onRetry }: { message?: string; onRetry: () => void }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <div className="flex items-start">
        <AlertTriangle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h4 className="font-semibold text-red-900 mb-1">
            Unable to create alert
          </h4>
          <p className="text-sm text-red-800 mb-3">
            {message || 'Something went wrong. Please try again.'}
          </p>
          <button
            onClick={onRetry}
            className="text-sm text-red-800 hover:text-red-900 font-medium underline"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>
  )
}

/**
 * Alert Update Failure
 * "Unable to update alert"
 */
export function AlertUpdateError({ message, onRetry }: { message?: string; onRetry: () => void }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <div className="flex items-start">
        <AlertTriangle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h4 className="font-semibold text-red-900 mb-1">
            Unable to update alert
          </h4>
          <p className="text-sm text-red-800 mb-3">
            {message || 'Failed to save changes. Please try again.'}
          </p>
          <button
            onClick={onRetry}
            className="text-sm text-red-800 hover:text-red-900 font-medium underline"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>
  )
}

/**
 * Data Failure
 * "Unable to load alert data"
 */
export function DataFailureError({ service, onRetry }: { service?: string; onRetry: () => void }) {
  return (
    <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
      <div className="flex items-start">
        <AlertTriangle className="h-5 w-5 text-orange-600 mr-3 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h4 className="font-semibold text-orange-900 mb-1">
            Unable to load alert data
          </h4>
          <p className="text-sm text-orange-800 mb-3">
            {service ? `Connection to ${service} failed.` : 'Data service unavailable.'} Your alerts are still active.
          </p>
          <button
            onClick={onRetry}
            className="text-sm text-orange-800 hover:text-orange-900 font-medium underline"
          >
            Refresh
          </button>
        </div>
      </div>
    </div>
  )
}
