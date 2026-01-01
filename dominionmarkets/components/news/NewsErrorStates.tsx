/**
 * News Error States
 * =================
 * Error and empty state components for News Verification Center
 */

"use client"

import { AlertTriangle, RefreshCw, Wifi, Database, Inbox } from 'lucide-react'

interface ErrorStateProps {
  onRetry?: () => void
}

/**
 * News Load Failure
 * "News temporarily unavailable — retry."
 */
export function NewsLoadFailure({ onRetry }: ErrorStateProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-red-200 p-12 text-center">
      <Wifi className="h-16 w-16 text-red-500 mx-auto mb-4" />
      <h3 className="text-xl font-semibold text-gray-900 mb-2">
        News Temporarily Unavailable
      </h3>
      <p className="text-gray-600 mb-6">
        We're having trouble loading news stories. Please try again.
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
  )
}

/**
 * Verification Engine Failure
 * "Unable to verify this story."
 */
export function VerificationEngineFailure({ onRetry }: ErrorStateProps) {
  return (
    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-8 text-center">
      <AlertTriangle className="h-12 w-12 text-yellow-600 mx-auto mb-4" />
      <h3 className="text-lg font-semibold text-yellow-900 mb-2">
        Unable to Verify This Story
      </h3>
      <p className="text-sm text-yellow-800 mb-4">
        Our verification engine couldn't confirm this story with multiple sources. 
        This doesn't mean the story is false — just unverified.
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center px-4 py-2 bg-yellow-600 text-white rounded-lg font-semibold hover:bg-yellow-700 transition-colors"
        >
          <RefreshCw className="h-4 w-4 mr-2" />
          Retry Verification
        </button>
      )}
    </div>
  )
}

/**
 * Source Load Failure
 * "Unable to load sources."
 */
export function SourceLoadFailure({ onRetry }: ErrorStateProps) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-6">
      <div className="flex items-start">
        <Database className="h-6 w-6 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h4 className="font-semibold text-red-900 mb-1">
            Unable to Load Sources
          </h4>
          <p className="text-sm text-red-800 mb-3">
            We couldn't load the source information for this article. 
            The article content is available, but source verification is temporarily unavailable.
          </p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="text-sm text-red-700 font-semibold hover:underline"
            >
              Try Again
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

/**
 * Empty State
 * "No news available — check back later."
 */
export function NewsEmptyState() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-16 text-center">
      <Inbox className="h-20 w-20 text-gray-300 mx-auto mb-4" />
      <h3 className="text-2xl font-semibold text-gray-900 mb-2">
        No News Available
      </h3>
      <p className="text-gray-600 mb-2">
        There are no verified news stories matching your filters right now.
      </p>
      <p className="text-sm text-gray-500">
        Check back later or adjust your filters to see more content.
      </p>
    </div>
  )
}

/**
 * Generic Error Boundary
 */
export function NewsErrorBoundary({ error, onRetry }: { error: string; onRetry?: () => void }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-8 text-center">
      <AlertTriangle className="h-12 w-12 text-red-600 mx-auto mb-4" />
      <h3 className="text-lg font-semibold text-red-900 mb-2">
        Something Went Wrong
      </h3>
      <p className="text-sm text-red-800 mb-4 font-mono">
        {error}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-6 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  )
}
