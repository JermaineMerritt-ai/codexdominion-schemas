/**
 * Source List
 * ===========
 * List of sources reporting the story with trust ratings
 */

"use client"

import { useState } from 'react'
import { ExternalLink, AlertTriangle } from 'lucide-react'

interface Source {
  id: string
  name: string
  trust_score: number
  tier: string
  bias_rating: string
  reported_at?: string
  content_url?: string
}

function calculateVerificationWeight(tier: string, trustScore: number): number {
  const tierWeights: Record<string, number> = {
    'AAA': 1.0,
    'AA': 0.9,
    'A': 0.75,
    'B': 0.6,
    'C': 0.4
  }
  const baseWeight = tierWeights[tier] || 0.5
  return Math.round(baseWeight * (trustScore / 100) * 100)
}

interface SourceListProps {
  sources: Source[]
  articleId: string
  userTier: string
}

export default function SourceList({ sources, articleId, userTier }: SourceListProps) {
  const [showComparison, setShowComparison] = useState(false)
  const [comparisonData, setComparisonData] = useState<any>(null)
  const [loadingComparison, setLoadingComparison] = useState(false)

  const loadComparison = async () => {
    if (userTier === 'free') {
      return // Show upgrade prompt instead
    }

    try {
      setLoadingComparison(true)
      const response = await fetch(`/api/news/${articleId}/sources`)
      const data = await response.json()
      setComparisonData(data)
      setShowComparison(true)
    } catch (error) {
      console.error('Failed to load comparison:', error)
    } finally {
      setLoadingComparison(false)
    }
  }

  const getTierColor = (tier: string) => {
    const colors: Record<string, string> = {
      'AAA': 'bg-emerald-100 text-emerald-800 border-emerald-200',
      'AA': 'bg-green-100 text-green-800 border-green-200',
      'A': 'bg-blue-100 text-blue-800 border-blue-200',
      'B': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'C': 'bg-orange-100 text-orange-800 border-orange-200'
    }
    return colors[tier] || 'bg-gray-100 text-gray-800 border-gray-200'
  }

  const getBiasColor = (bias: string) => {
    const colors: Record<string, string> = {
      'left': 'bg-blue-100 text-blue-800',
      'center-left': 'bg-blue-50 text-blue-700',
      'center': 'bg-gray-100 text-gray-800',
      'center-right': 'bg-red-50 text-red-700',
      'right': 'bg-red-100 text-red-800',
      'varies': 'bg-purple-100 text-purple-800'
    }
    return colors[bias] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div>
      {/* Source List */}
      <div className="space-y-3 mb-6">
        {sources.map(source => {
          const verificationWeight = calculateVerificationWeight(source.tier, source.trust_score)
          
          return (
            <div
              key={source.id}
              className="flex items-start justify-between p-4 bg-gray-50 rounded-lg border border-gray-200"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h4 className="font-semibold text-gray-900">{source.name}</h4>
                  <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${getTierColor(source.tier)}`}>
                    {source.tier}
                  </span>
                </div>
                
                <div className="flex items-center gap-3 text-sm mb-2">
                  <div className="flex items-center">
                    <span className="text-gray-600 mr-1">Trust:</span>
                    <span className="font-semibold text-gray-900">{source.trust_score}/100</span>
                  </div>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${getBiasColor(source.bias_rating)}`}>
                    {source.bias_rating}
                  </span>
                  <div className="flex items-center">
                    <span className="text-gray-600 mr-1">Weight:</span>
                    <span className="font-semibold text-dominion-gold">{verificationWeight}%</span>
                  </div>
                </div>

                {source.reported_at && (
                  <p className="text-xs text-gray-500">
                    Published: {new Date(source.reported_at).toLocaleString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                )}
              </div>

              <a
                href={source.content_url || '#'}
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-lg bg-white hover:bg-gray-100 transition-colors border border-gray-200"
                title="View original article"
              >
                <ExternalLink className="h-4 w-4 text-gray-600" />
              </a>
            </div>
          )
        })}
      </div>

      {/* Source Comparison (Premium) */}
      {!showComparison && (
        <button
          onClick={loadComparison}
          disabled={loadingComparison}
          className={`w-full py-3 rounded-lg font-semibold transition-colors ${
            userTier === 'free'
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-dominion-gold text-gray-900 hover:bg-yellow-500'
          }`}
        >
          {loadingComparison ? 'Loading...' : 
           userTier === 'free' ? '🔒 Source Comparison (Premium)' : 
           'Compare Sources'}
        </button>
      )}

      {/* Premium Upgrade Prompt */}
      {userTier === 'free' && (
        <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div className="flex items-start">
            <AlertTriangle className="h-5 w-5 text-yellow-600 mr-3 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-yellow-900 mb-1">
                Upgrade to Premium
              </h4>
              <p className="text-sm text-yellow-800 mb-3">
                Compare how different sources report this story side-by-side and see conflict detection.
              </p>
              <button className="px-4 py-2 bg-dominion-gold text-gray-900 rounded-lg text-sm font-semibold hover:bg-yellow-500 transition-colors">
                Upgrade to Premium ($14.99/mo)
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Source Comparison Panel */}
      {showComparison && comparisonData && (
        <div className="mt-6 border border-gray-200 rounded-lg overflow-hidden">
          <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
            <h3 className="font-semibold text-gray-900">Source Comparison</h3>
          </div>
          
          <div className="p-4 space-y-4">
            {comparisonData.conflicts && comparisonData.conflicts.length > 0 && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-start">
                  <AlertTriangle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-semibold text-red-900 mb-2">
                      {comparisonData.conflict_count} Conflict{comparisonData.conflict_count !== 1 ? 's' : ''} Detected
                    </h4>
                    <div className="space-y-3">
                      {comparisonData.conflicts.map((conflict: any, index: number) => (
                        <div key={index} className="text-sm text-red-800">
                          <div className="font-medium mb-1">{conflict.description}</div>
                          <div className="text-xs text-red-700">
                            Severity: {conflict.severity}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {comparisonData.sources && comparisonData.sources.length > 0 && (
              <div className="grid grid-cols-1 gap-4">
                {comparisonData.sources.map((source: any) => (
                  <div key={source.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold text-gray-900">{source.name}</h4>
                      <span className={`px-2 py-0.5 rounded text-xs font-semibold border ${getTierColor(source.tier)}`}>
                        {source.tier}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 line-clamp-3">
                      {source.excerpt || 'Content excerpt not available'}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
