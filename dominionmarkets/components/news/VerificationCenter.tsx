/**
 * Verification Center - Article Detail View
 * ==========================================
 * Full article with verification panel, sources, timeline, AI insights
 */

"use client"

import { useState, useEffect } from 'react'
import { ArrowLeft, Bookmark, BookmarkCheck, Share2, Download, Clock } from 'lucide-react'
import Link from 'next/link'
import VerificationBadge from '@/components/news/VerificationBadge'
import SourceList from '@/components/news/SourceList'
import Timeline from '@/components/news/Timeline'
import AISummary from '@/components/news/AISummary'
import RelatedCompanies from '@/components/news/RelatedCompanies'

interface VerificationCenterProps {
  articleId: string
  userTier: string
}

interface ArticleData {
  id: string
  title: string
  summary: string
  content: string
  published_at: string
  verification_score: number
  verification_status: string
  source_count: number
  agreement_rate: number
  category: string
  ticker_symbols: string[]
  has_conflicts: boolean
  sentiment_score: number | null
  sentiment_label: string | null
  view_count: number
  badge: {
    emoji: string
    label: string
    color: string
  }
  sources: Array<{
    id: string
    name: string
    trust_score: number
    tier: string
    bias_rating: string
  }>
  verification_breakdown: Array<{
    check_type: string
    score: number
    passed: boolean
    details: any
  }>
  is_bookmarked: boolean
  related_articles: Array<{
    id: string
    title: string
    verification_score: number
  }>
}

export default function VerificationCenter({ articleId, userTier }: VerificationCenterProps) {
  const [article, setArticle] = useState<ArticleData | null>(null)
  const [loading, setLoading] = useState(true)
  const [showFullVerification, setShowFullVerification] = useState(false)
  const [activeTab, setActiveTab] = useState<'content' | 'sources' | 'timeline'>('content')

  useEffect(() => {
    loadArticle()
  }, [articleId])

  const loadArticle = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/news/${articleId}`)
      const data = await response.json()
      setArticle(data)
    } catch (error) {
      console.error('Failed to load article:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleBookmark = async () => {
    if (!article) return

    try {
      if (article.is_bookmarked) {
        await fetch(`/api/news/${articleId}/bookmark`, { method: 'DELETE' })
      } else {
        await fetch(`/api/news/${articleId}/bookmark`, { method: 'POST' })
      }
      setArticle({
        ...article,
        is_bookmarked: !article.is_bookmarked
      })
    } catch (error) {
      console.error('Failed to toggle bookmark:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-6 bg-gray-200 rounded w-full mb-2"></div>
          <div className="h-6 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>
    )
  }

  if (!article) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Article not found</h2>
          <p className="text-gray-600 mb-6">This article may have been removed or is no longer available.</p>
          <Link href="/news" className="text-dominion-gold hover:underline">
            ← Back to News Feed
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Back Button */}
        <Link
          href="/news"
          className="inline-flex items-center text-gray-600 hover:text-dominion-gold mb-6 transition-colors"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to News Feed
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Header */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
              {/* Verification Badge */}
              <div className="flex items-center justify-between mb-4">
                <VerificationBadge
                  score={article.verification_score}
                  badge={article.badge}
                  size="large"
                />
                
                <div className="flex items-center gap-2">
                  <button
                    onClick={toggleBookmark}
                    className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
                  >
                    {article.is_bookmarked ? (
                      <BookmarkCheck className="h-5 w-5 text-dominion-gold" />
                    ) : (
                      <Bookmark className="h-5 w-5 text-gray-600" />
                    )}
                  </button>
                  <button className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors">
                    <Share2 className="h-5 w-5 text-gray-600" />
                  </button>
                  {userTier === 'pro' && (
                    <button className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors">
                      <Download className="h-5 w-5 text-gray-600" />
                    </button>
                  )}
                </div>
              </div>

              {/* Title */}
              <h1 className="text-3xl font-bold text-gray-900 mb-3">
                {article.title}
              </h1>

              {/* Metadata */}
              <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                <span className="flex items-center">
                  <Clock className="h-4 w-4 mr-1" />
                  {new Date(article.published_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
                <span>•</span>
                <span>{article.source_count} sources</span>
                <span>•</span>
                <span>{article.view_count} views</span>
              </div>

              {/* Summary */}
              {article.summary && (
                <p className="text-lg text-gray-700 mb-6 leading-relaxed">
                  {article.summary}
                </p>
              )}

              {/* Quick Verification Breakdown */}
              <button
                onClick={() => setShowFullVerification(!showFullVerification)}
                className="w-full text-left bg-gray-50 border border-gray-200 rounded-lg p-4 hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="font-semibold text-gray-900">Verification Breakdown</span>
                  <span className="text-sm text-dominion-gold">
                    {showFullVerification ? 'Hide Details' : 'Show Details'} →
                  </span>
                </div>
                
                <div className="grid grid-cols-3 gap-4">
                  {article.verification_breakdown.map(check => (
                    <div key={check.check_type} className="text-center">
                      <div className={`text-2xl font-bold mb-1 ${check.passed ? 'text-green-600' : 'text-red-600'}`}>
                        {check.score}
                      </div>
                      <div className="text-xs text-gray-600 capitalize">
                        {check.check_type.replace('_', ' ')}
                      </div>
                    </div>
                  ))}
                </div>

                {showFullVerification && (
                  <div className="mt-4 pt-4 border-t border-gray-200 space-y-3">
                    {article.verification_breakdown.map(check => (
                      <div key={check.check_type} className="flex items-start">
                        <div className={`w-2 h-2 rounded-full mt-1.5 mr-3 ${check.passed ? 'bg-green-500' : 'bg-red-500'}`}></div>
                        <div className="flex-1">
                          <div className="font-medium text-gray-900 capitalize mb-1">
                            {check.check_type.replace('_', ' ')}
                          </div>
                          <div className="text-sm text-gray-600">
                            {JSON.stringify(check.details)}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </button>
            </div>

            {/* Tabs */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
              <div className="border-b border-gray-200">
                <div className="flex">
                  <button
                    onClick={() => setActiveTab('content')}
                    className={`px-6 py-3 font-medium transition-colors ${
                      activeTab === 'content'
                        ? 'border-b-2 border-dominion-gold text-dominion-gold'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Article Content
                  </button>
                  <button
                    onClick={() => setActiveTab('sources')}
                    className={`px-6 py-3 font-medium transition-colors ${
                      activeTab === 'sources'
                        ? 'border-b-2 border-dominion-gold text-dominion-gold'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Sources ({article.source_count})
                  </button>
                  <button
                    onClick={() => setActiveTab('timeline')}
                    className={`px-6 py-3 font-medium transition-colors ${
                      activeTab === 'timeline'
                        ? 'border-b-2 border-dominion-gold text-dominion-gold'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Timeline
                  </button>
                </div>
              </div>

              <div className="p-6">
                {activeTab === 'content' && (
                  <div className="prose max-w-none">
                    <div dangerouslySetInnerHTML={{ __html: article.content || article.summary }} />
                    
                    <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800">
                      <strong>Compliance Notice:</strong> This content is for informational purposes only. 
                      DominionMarkets provides descriptive data, not financial advice or predictions.
                    </div>
                  </div>
                )}

                {activeTab === 'sources' && (
                  <SourceList sources={article.sources} articleId={article.id} userTier={userTier} />
                )}

                {activeTab === 'timeline' && (
                  <Timeline articleId={article.id} publishedAt={article.published_at} />
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* Related Companies */}
            {article.ticker_symbols && article.ticker_symbols.length > 0 && (
              <RelatedCompanies tickers={article.ticker_symbols} />
            )}

            {/* AI Summary (Premium) */}
            {userTier !== 'free' && article.sentiment_score !== null && (
              <AISummary
                sentimentScore={article.sentiment_score}
                sentimentLabel={article.sentiment_label}
                articleId={article.id}
                userTier={userTier}
              />
            )}

            {/* Related Articles */}
            {article.related_articles && article.related_articles.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="font-semibold text-gray-900 mb-4">Related Articles</h3>
                <div className="space-y-3">
                  {article.related_articles.map(related => (
                    <Link
                      key={related.id}
                      href={`/news/${related.id}`}
                      className="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <div className="text-sm font-medium text-gray-900 mb-1 line-clamp-2">
                        {related.title}
                      </div>
                      <VerificationBadge
                        score={related.verification_score}
                        badge={{ emoji: '✅', label: 'Verified', color: 'green' }}
                        size="small"
                        showLabel={false}
                      />
                    </Link>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
