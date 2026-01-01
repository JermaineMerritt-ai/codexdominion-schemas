/**
 * AI Portfolio Summary Component
 * Identity-aware portfolio interpretation with compliance guardrails
 */

"use client"

import { useState, useEffect } from 'react'
import { Bot, RefreshCw, Download, Lock } from 'lucide-react'

interface AIPortfolioSummaryProps {
  portfolioId: string
  identityType: string
  userTier: string
}

export default function AIPortfolioSummary({ portfolioId, identityType, userTier }: AIPortfolioSummaryProps) {
  const [summary, setSummary] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [generatedAt, setGeneratedAt] = useState<string | null>(null)
  const [showFullSummary, setShowFullSummary] = useState(false)

  useEffect(() => {
    loadSummary()
  }, [portfolioId])

  const loadSummary = async () => {
    try {
      const response = await fetch(`/api/portfolio/${portfolioId}/analytics`)
      const data = await response.json()
      if (data.ai_summary) {
        setSummary(data.ai_summary)
        setGeneratedAt(data.ai_summary_generated_at)
      }
    } catch (error) {
      console.error('Failed to load AI summary:', error)
    }
  }

  const generateNewSummary = async () => {
    if (userTier === 'free') return

    try {
      setLoading(true)
      const response = await fetch(`/api/portfolio/${portfolioId}/ai-summary`, {
        method: 'POST'
      })
      const data = await response.json()
      setSummary(data.summary)
      setGeneratedAt(data.generated_at)
    } catch (error) {
      console.error('Failed to generate AI summary:', error)
    } finally {
      setLoading(false)
    }
  }

  const getIdentityGreeting = () => {
    switch (identityType) {
      case 'diaspora':
        return 'Building wealth across borders'
      case 'youth':
        return 'Growing your financial future'
      case 'creator':
        return 'Creative capital at work'
      case 'legacy-builder':
        return 'Generational wealth strategy'
      default:
        return 'Your portfolio insights'
    }
  }

  // Split summary into paragraphs
  const paragraphs = summary ? summary.split('\n\n') : []
  const firstParagraph = paragraphs[0] || ''
  const remainingParagraphs = paragraphs.slice(1).join('\n\n')

  const isPremium = userTier === 'premium' || userTier === 'pro'

  return (
    <div className="mt-6 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <div className="p-2 bg-dominion-gold rounded-lg mr-3">
            <Bot className="h-5 w-5 text-gray-900" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">AI Portfolio Summary</h3>
            <p className="text-sm text-gray-600">{getIdentityGreeting()}</p>
          </div>
        </div>

        {isPremium && (
          <div className="flex items-center gap-2">
            <button
              onClick={generateNewSummary}
              disabled={loading}
              className="flex items-center px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              Regenerate
            </button>
            
            {userTier === 'pro' && (
              <button className="flex items-center px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
                <Download className="h-4 w-4 mr-2" />
                Download PDF
              </button>
            )}
          </div>
        )}
      </div>

      {loading ? (
        <div className="py-8 text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-dominion-gold mb-2"></div>
          <p className="text-sm text-gray-600">Generating AI insights...</p>
        </div>
      ) : summary ? (
        <div className="prose prose-sm max-w-none">
          {/* First paragraph always visible */}
          <p className="text-gray-700 leading-relaxed mb-4">{firstParagraph}</p>

          {/* Remaining content - premium gated for free users */}
          {isPremium ? (
            <div className="text-gray-700 leading-relaxed whitespace-pre-line">
              {remainingParagraphs}
            </div>
          ) : (
            <div className="relative">
              {/* Blurred preview */}
              <div className="filter blur-sm pointer-events-none select-none">
                <p className="text-gray-700 leading-relaxed">{remainingParagraphs.substring(0, 200)}...</p>
              </div>

              {/* Upgrade prompt */}
              <div className="mt-4 p-4 bg-gradient-to-r from-dominion-gold to-yellow-500 rounded-lg text-center">
                <Lock className="h-5 w-5 text-gray-900 mx-auto mb-2" />
                <p className="text-sm font-semibold text-gray-900 mb-2">
                  Unlock Full AI Insights
                </p>
                <p className="text-xs text-gray-800 mb-3">
                  Get complete portfolio analysis and identity-aware recommendations
                </p>
                <button
                  onClick={() => window.location.href = '/premium'}
                  className="px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors"
                >
                  Upgrade to Premium - $14.99/mo
                </button>
              </div>
            </div>
          )}

          {/* Footer */}
          <div className="mt-6 pt-4 border-t border-gray-200">
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>Generated {generatedAt ? new Date(generatedAt).toLocaleString() : 'recently'}</span>
              <span className="flex items-center">
                <span className="inline-block w-2 h-2 bg-emerald-500 rounded-full mr-1"></span>
                Compliance-verified • No financial advice
              </span>
            </div>
          </div>
        </div>
      ) : (
        <div className="py-8 text-center">
          <Bot className="h-12 w-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-600 mb-4">No AI summary available yet</p>
          {isPremium && (
            <button
              onClick={generateNewSummary}
              className="px-4 py-2 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors"
            >
              Generate AI Summary
            </button>
          )}
          {!isPremium && (
            <p className="text-sm text-gray-500">Upgrade to Premium to unlock AI insights</p>
          )}
        </div>
      )}

      {/* Compliance Disclaimer */}
      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
        <p className="text-xs text-gray-600 leading-relaxed">
          <strong>Compliance Note:</strong> This AI-generated summary provides descriptive portfolio analysis only. 
          It does not constitute financial advice, investment recommendations, or performance predictions. 
          All investment decisions are your responsibility. DominionMarkets is not a financial advisor.
        </p>
      </div>
    </div>
  )
}
