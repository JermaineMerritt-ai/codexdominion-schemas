/**
 * AI Summary
 * ==========
 * AI-generated article summary with sentiment analysis (Premium)
 */

"use client"

import { useState } from 'react'
import { Sparkles, TrendingUp, TrendingDown, Minus, AlertTriangle } from 'lucide-react'

interface AISummaryProps {
  sentimentScore: number | null
  sentimentLabel: string | null
  articleId: string
  userTier: string
  dailySummariesUsed?: number
}

export default function AISummary({ sentimentScore, sentimentLabel, articleId, userTier, dailySummariesUsed = 0 }: AISummaryProps) {
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState<string | null>(null)
  const [summariesUsed, setSummariesUsed] = useState(dailySummariesUsed)
  
  const dailyLimit = 5
  const canGenerate = userTier !== 'free' || summariesUsed < dailyLimit

  const generateSummary = async () => {
    if (!canGenerate) return

    try {
      setLoading(true)
      const response = await fetch(`/api/news/${articleId}/ai-summary`, {
        method: 'POST'
      })
      const data = await response.json()
      setSummary(data.summary)
      if (userTier === 'free') {
        setSummariesUsed(prev => prev + 1)
      }
    } catch (error) {
      console.error('Failed to generate summary:', error)
    } finally {
      setLoading(false)
    }
  }

  const getSentimentIcon = () => {
    if (!sentimentScore) return Minus
    if (sentimentScore > 0.2) return TrendingUp
    if (sentimentScore < -0.2) return TrendingDown
    return Minus
  }

  const getSentimentColor = () => {
    if (!sentimentScore) return 'text-gray-600'
    if (sentimentScore > 0.2) return 'text-green-600'
    if (sentimentScore < -0.2) return 'text-red-600'
    return 'text-gray-600'
  }

  const getSentimentBgColor = () => {
    if (!sentimentScore) return 'bg-gray-50 border-gray-200'
    if (sentimentScore > 0.2) return 'bg-green-50 border-green-200'
    if (sentimentScore < -0.2) return 'bg-red-50 border-red-200'
    return 'bg-gray-50 border-gray-200'
  }

  const SentimentIcon = getSentimentIcon()

  if (userTier === 'free' && summariesUsed >= dailyLimit) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <Sparkles className="h-5 w-5 text-dominion-gold mr-2" />
            <h3 className="font-semibold text-gray-900">AI Insights</h3>
          </div>
          <span className="px-2 py-1 bg-red-100 text-red-800 text-xs font-semibold rounded">
            {summariesUsed}/{dailyLimit} Used
          </span>
        </div>

        <div className="relative">
          <div className="blur-sm pointer-events-none">
            <p className="text-gray-600 mb-4">
              AI-powered analysis reveals key market sentiment indicators and provides context from similar historical events...
            </p>
          </div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="bg-white rounded-lg p-6 shadow-lg border-2 border-dominion-gold text-center">
              <Sparkles className="h-8 w-8 text-dominion-gold mx-auto mb-3" />
              <h4 className="font-semibold text-gray-900 mb-2">Daily Limit Reached</h4>
              <p className="text-sm text-gray-600 mb-4">
                Free tier: {dailyLimit} AI summaries per day<br />
                Upgrade for unlimited access
              </p>
              <button className="px-4 py-2 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors">
                Upgrade to Premium ($14.99/mo)
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <Sparkles className="h-5 w-5 text-dominion-gold mr-2" />
          <h3 className="font-semibold text-gray-900">AI Insights</h3>
        </div>
        {userTier === 'free' && (
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded">
            {summariesUsed}/{dailyLimit} Used Today
          </span>
        )}
        {userTier === 'premium' && (
          <span className="px-2 py-1 bg-emerald-100 text-emerald-800 text-xs font-semibold rounded">
            Unlimited
          </span>
        )}
        {userTier === 'pro' && (
          <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs font-semibold rounded">
            Pro • Multi-Event
          </span>
        )}
      </div>

      {/* Sentiment Analysis */}
      {sentimentScore !== null && (
        <div className={`border rounded-lg p-4 mb-4 ${getSentimentBgColor()}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Market Sentiment</span>
            <SentimentIcon className={`h-5 w-5 ${getSentimentColor()}`} />
          </div>
          
          <div className="flex items-center gap-3 mb-2">
            <div className="flex-1 bg-white rounded-full h-2 overflow-hidden">
              <div
                className={`h-full ${sentimentScore >= 0 ? 'bg-green-500' : 'bg-red-500'}`}
                style={{ width: `${Math.abs(sentimentScore) * 100}%` }}
              ></div>
            </div>
            <span className={`text-sm font-semibold ${getSentimentColor()}`}>
              {(sentimentScore * 100).toFixed(0)}%
            </span>
          </div>

          {sentimentLabel && (
            <p className="text-sm text-gray-600">
              Sentiment: <span className="font-semibold">{sentimentLabel}</span>
            </p>
          )}
        </div>
      )}

      {/* AI Summary */}
      {!summary && !loading && (
        <button
          onClick={generateSummary}
          disabled={!canGenerate}
          className={`w-full py-3 rounded-lg font-semibold transition-colors flex items-center justify-center ${
            canGenerate 
              ? 'bg-dominion-gold text-gray-900 hover:bg-yellow-500' 
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }`}
        >
          <Sparkles className="h-4 w-4 mr-2" />
          {canGenerate ? 'Generate AI Summary' : 'Daily Limit Reached'}
        </button>
      )}

      {loading && (
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-gray-200 rounded w-full"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6"></div>
          <div className="h-4 bg-gray-200 rounded w-4/6"></div>
        </div>
      )}

      {summary && (
        <div>
          <div className="prose prose-sm max-w-none text-gray-700 mb-4">
            {summary}
          </div>
          <button
            onClick={generateSummary}
            disabled={loading}
            className="text-sm text-dominion-gold hover:underline"
          >
            Regenerate Summary
          </button>
        </div>
      )}

      {/* Compliance Notice */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="flex items-start">
          <AlertTriangle className="h-4 w-4 text-blue-600 mr-2 flex-shrink-0 mt-0.5" />
          <div className="text-xs text-gray-600">
            <p className="font-medium text-gray-700 mb-1">Descriptive Summary Only</p>
            <p>
              AI summaries describe events and data from verified sources. 
              This is not financial advice, predictions, or recommendations.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
