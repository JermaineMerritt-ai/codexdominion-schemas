/**
 * News Feed - Main Component
 * ===========================
 * Displays verified financial news with identity-aware filtering
 */

"use client"

import { useState, useEffect } from 'react'
import { Search, Filter, SlidersHorizontal } from 'lucide-react'
import NewsItem from '@/components/news/NewsItem'
import IdentityFilters from '@/components/news/IdentityFilters'

interface NewsArticle {
  id: string
  title: string
  summary: string
  published_at: string
  verification_score: number
  verification_status: string
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

interface NewsFeedProps {
  userTier: string
  identityType: string
}

export default function NewsFeed({ userTier, identityType }: NewsFeedProps) {
  const [articles, setArticles] = useState<NewsArticle[]>([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)
  
  // Filters
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [selectedTicker, setSelectedTicker] = useState<string | null>(null)
  const [minScore, setMinScore] = useState(0)
  const [sortBy, setSortBy] = useState('published')
  const [showFilters, setShowFilters] = useState(false)
  const [identityFilter, setIdentityFilter] = useState(identityType)

  useEffect(() => {
    loadArticles()
  }, [selectedCategory, selectedTicker, minScore, sortBy, identityFilter])

  const loadArticles = async (append = false) => {
    try {
      setLoading(true)
      const params = new URLSearchParams({
        page: append ? (page + 1).toString() : '1',
        limit: '20',
        sort: sortBy
      })

      if (selectedCategory) params.append('category', selectedCategory)
      if (selectedTicker) params.append('ticker', selectedTicker)
      if (minScore > 0) params.append('min_score', minScore.toString())
      if (identityFilter && identityFilter !== 'all') {
        params.append('identity', identityFilter)
      }

      const response = await fetch(`/api/news?${params}`)
      const data = await response.json()

      if (append) {
        setArticles(prev => [...prev, ...data.articles])
        setPage(prev => prev + 1)
      } else {
        setArticles(data.articles)
        setPage(1)
      }

      setHasMore(data.pagination.page < data.pagination.pages)
    } catch (error) {
      console.error('Failed to load articles:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadArticles()
      return
    }

    try {
      setLoading(true)
      const response = await fetch(`/api/news/search?q=${encodeURIComponent(searchQuery)}`)
      const data = await response.json()
      setArticles(data.results)
      setHasMore(false)
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const categories = [
    { value: 'market_news', label: 'Market News' },
    { value: 'earnings', label: 'Earnings' },
    { value: 'policy', label: 'Policy & Regulation' },
    { value: 'ipo', label: 'IPOs' },
    { value: 'mergers', label: 'M&A' },
    { value: 'dividends', label: 'Dividends' },
    { value: 'analyst', label: 'Analyst Updates' }
  ]

  // Identity-aware sections
  const topVerifiedArticles = articles.filter(a => a.verification_score >= 90)
  const identityRelevantArticles = articles.filter(a => {
    // This would be pre-filtered by backend, but we can also sort client-side
    return true
  })

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            News Verification Center
          </h1>
          <p className="text-gray-600">
            Multi-source verified financial news • No predictions • No advice
          </p>
        </div>

        {/* Search & Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search Bar */}
            <div className="flex-1 flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  placeholder="Search articles, tickers, or topics..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold focus:border-transparent"
                />
              </div>
              <button
                onClick={handleSearch}
                className="px-6 py-2 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors"
              >
                Search
              </button>
            </div>

            {/* Filter Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <SlidersHorizontal className="h-5 w-5 mr-2" />
              Filters
            </button>
          </div>

          {/* Expanded Filters */}
          {showFilters && (
            <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Category Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category
                </label>
                <select
                  value={selectedCategory || ''}
                  onChange={(e) => setSelectedCategory(e.target.value || null)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold"
                >
                  <option value="">All Categories</option>
                  {categories.map(cat => (
                    <option key={cat.value} value={cat.value}>{cat.label}</option>
                  ))}
                </select>
              </div>

              {/* Min Verification Score */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Min Verification Score: {minScore}
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  step="10"
                  value={minScore}
                  onChange={(e) => setMinScore(parseInt(e.target.value))}
                  className="w-full"
                />
              </div>

              {/* Sort By */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sort By
                </label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-dominion-gold"
                >
                  <option value="published">Latest First</option>
                  <option value="verification">Verification Score</option>
                  <option value="bookmarks">Most Bookmarked</option>
                </select>
              </div>
            </div>
          )}
        </div>

        {/* Identity Filters */}
        <IdentityFilters
          currentIdentity={identityFilter}
          onChange={setIdentityFilter}
          userIdentity={identityType}
        />

        {/* Loading State */}
        {loading && articles.length === 0 && (
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map(i => (
              <div key={i} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
                <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
                <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-5/6"></div>
              </div>
            ))}
          </div>
        )}

        {/* Top Verified Stories */}
        {!loading && topVerifiedArticles.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <span className="text-2xl mr-2">📰</span>
              Top Verified Stories
            </h2>
            <div className="space-y-4">
              {topVerifiedArticles.slice(0, 3).map(article => (
                <NewsItem key={article.id} article={article} />
              ))}
            </div>
          </div>
        )}

        {/* Identity-Relevant Section */}
        {!loading && identityFilter !== 'all' && (
          <div className="mb-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <span className="text-2xl mr-2">🎯</span>
              Relevant for {getIdentityLabel(identityFilter)}
            </h2>
            <div className="space-y-4">
              {articles.slice(0, 5).map(article => (
                <NewsItem key={article.id} article={article} />
              ))}
            </div>
          </div>
        )}

        {/* All Articles */}
        {!loading && articles.length > 0 && (
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              All Articles
            </h2>
            <div className="space-y-4">
              {articles.map(article => (
                <NewsItem key={article.id} article={article} />
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && articles.length === 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
            <div className="text-6xl mb-4">📭</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No articles found
            </h3>
            <p className="text-gray-600 mb-6">
              Try adjusting your filters or search for different topics
            </p>
            <button
              onClick={() => {
                setSelectedCategory(null)
                setSelectedTicker(null)
                setMinScore(0)
                setSearchQuery('')
                loadArticles()
              }}
              className="px-6 py-2 bg-dominion-gold text-gray-900 rounded-lg font-semibold hover:bg-yellow-500 transition-colors"
            >
              Clear Filters
            </button>
          </div>
        )}

        {/* Load More */}
        {!loading && hasMore && articles.length > 0 && (
          <div className="mt-8 text-center">
            <button
              onClick={() => loadArticles(true)}
              className="px-8 py-3 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
            >
              Load More Articles
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

function getIdentityLabel(identity: string): string {
  const labels = {
    'diaspora': 'Global Investors',
    'youth': 'Young Investors',
    'creator': 'Creators & Entrepreneurs',
    'legacy': 'Legacy Builders',
    'all': 'All Users'
  }
  return labels[identity as keyof typeof labels] || 'You'
}
