/**
 * News Item Card
 * ==============
 * Individual article card with verification badge and metadata
 */

"use client"

import Link from 'next/link'
import { Clock, Bookmark, BookmarkCheck, AlertTriangle } from 'lucide-react'
import VerificationBadge from '@/components/news/VerificationBadge'

interface NewsItemProps {
  article: {
    id: string
    title: string
    summary: string
    published_at: string
    verification_score: number
    source_count: number
    category: string
    ticker_symbols: string[]
    has_conflicts: boolean
    badge: {
      emoji: string
      label: string
      color: string
    }
    is_bookmarked: boolean
  }
}

export default function NewsItem({ article }: NewsItemProps) {
  const timeAgo = getTimeAgo(article.published_at)
  const categoryLabel = getCategoryLabel(article.category)

  return (
    <Link href={`/news/${article.id}`}>
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-dominion-gold transition-all cursor-pointer">
        {/* Header Row */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-3 flex-1">
            <VerificationBadge
              score={article.verification_score}
              badge={article.badge}
            />
            
            {article.has_conflicts && (
              <div className="flex items-center px-2 py-1 bg-yellow-50 border border-yellow-200 rounded text-xs font-medium text-yellow-800">
                <AlertTriangle className="h-3 w-3 mr-1" />
                Conflicts
              </div>
            )}

            {article.category && (
              <span className="px-2 py-1 bg-gray-100 rounded text-xs font-medium text-gray-700">
                {categoryLabel}
              </span>
            )}
          </div>

          <button
            onClick={(e) => {
              e.preventDefault()
              // Toggle bookmark
            }}
            className="text-gray-400 hover:text-dominion-gold transition-colors"
          >
            {article.is_bookmarked ? (
              <BookmarkCheck className="h-5 w-5 text-dominion-gold" />
            ) : (
              <Bookmark className="h-5 w-5" />
            )}
          </button>
        </div>

        {/* Title */}
        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 hover:text-dominion-gold transition-colors">
          {article.title}
        </h3>

        {/* Summary */}
        {article.summary && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {article.summary}
          </p>
        )}

        {/* Tickers */}
        {article.ticker_symbols && article.ticker_symbols.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-3">
            {article.ticker_symbols.slice(0, 5).map(ticker => (
              <span
                key={ticker}
                className="px-2 py-1 bg-blue-50 border border-blue-200 rounded text-xs font-mono font-semibold text-blue-700"
              >
                {ticker}
              </span>
            ))}
            {article.ticker_symbols.length > 5 && (
              <span className="px-2 py-1 bg-gray-50 text-xs text-gray-500">
                +{article.ticker_symbols.length - 5} more
              </span>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center gap-4">
            <span className="flex items-center">
              <Clock className="h-3 w-3 mr-1" />
              {timeAgo}
            </span>
            <span>
              {article.source_count} source{article.source_count !== 1 ? 's' : ''}
            </span>
          </div>
          
          <span className="text-dominion-gold font-medium hover:underline">
            Read More →
          </span>
        </div>
      </div>
    </Link>
  )
}

function getTimeAgo(publishedAt: string): string {
  const now = new Date()
  const published = new Date(publishedAt)
  const diffMs = now.getTime() - published.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMins / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`
  if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} week${Math.floor(diffDays / 7) !== 1 ? 's' : ''} ago`
  return published.toLocaleDateString()
}

function getCategoryLabel(category: string): string {
  const labels: Record<string, string> = {
    'market_news': 'Market News',
    'earnings': 'Earnings',
    'policy': 'Policy',
    'ipo': 'IPO',
    'mergers': 'M&A',
    'dividends': 'Dividends',
    'analyst': 'Analyst'
  }
  return labels[category] || category
}
