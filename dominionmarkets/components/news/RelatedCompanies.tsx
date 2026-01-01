/**
 * Related Companies
 * =================
 * Stock tickers and company mentions in the article
 */

"use client"

import { TrendingUp, ExternalLink, Sparkles } from 'lucide-react'
import Link from 'next/link'

interface RelatedCompaniesProps {
  tickers: string[]
  identityType?: string
}

export default function RelatedCompanies({ tickers, identityType = 'all' }: RelatedCompaniesProps) {
  // Mock company data - in production, fetch from stock API
  const companies = tickers.slice(0, 5).map(ticker => ({
    ticker,
    name: getCompanyName(ticker),
    price: (Math.random() * 500 + 50).toFixed(2),
    change: ((Math.random() - 0.5) * 10).toFixed(2),
    changePercent: ((Math.random() - 0.5) * 5).toFixed(2),
    identityTag: getIdentityTag(ticker, identityType),
    culturalAlpha: (Math.random() * 20 - 10).toFixed(1)
  }))

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center mb-4">
        <TrendingUp className="h-5 w-5 text-dominion-gold mr-2" />
        <h3 className="font-semibold text-gray-900">Related Companies</h3>
      </div>

      <div className="space-y-3">
        {companies.map(company => (
          <Link
            key={company.ticker}
            href={`/stocks/${company.ticker}`}
            className="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors border border-gray-200"
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-mono font-semibold text-gray-900">
                    {company.ticker}
                  </span>
                  {company.identityTag && (
                    <span className="px-1.5 py-0.5 bg-blue-100 text-blue-700 text-xs font-medium rounded">
                      {company.identityTag}
                    </span>
                  )}
                </div>
                <div className="text-xs text-gray-600 line-clamp-1">
                  {company.name}
                </div>
              </div>
              <ExternalLink className="h-4 w-4 text-gray-400 flex-shrink-0 ml-2" />
            </div>

            <div className="flex items-center justify-between mb-2">
              <span className="text-lg font-semibold text-gray-900">
                ${company.price}
              </span>
              <span className={`text-sm font-semibold ${
                parseFloat(company.change) >= 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {parseFloat(company.change) >= 0 ? '+' : ''}{company.change} ({company.changePercent}%)
              </span>
            </div>

            {/* Cultural Alpha Preview */}
            <div className="flex items-center justify-between pt-2 border-t border-gray-200">
              <span className="text-xs text-gray-500 flex items-center">
                <Sparkles className="h-3 w-3 mr-1 text-dominion-gold" />
                Cultural Alpha™
              </span>
              <span className={`text-xs font-semibold ${
                parseFloat(company.culturalAlpha) >= 0 ? 'text-emerald-600' : 'text-gray-500'
              }`}>
                {parseFloat(company.culturalAlpha) >= 0 ? '+' : ''}{company.culturalAlpha}%
              </span>
            </div>
          </Link>
        ))}
      </div>

      {tickers.length > 5 && (
        <div className="mt-4 text-center">
          <button className="text-sm text-dominion-gold hover:underline">
            View all {tickers.length} companies →
          </button>
        </div>
      )}

      {/* Data Disclaimer */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          Price data is delayed by 15 minutes. For real-time quotes, upgrade to Pro.
        </p>
      </div>
    </div>
  )
}

function getCompanyName(ticker: string): string {
  const names: Record<string, string> = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'TSLA': 'Tesla Inc.',
    'NVDA': 'NVIDIA Corporation',
    'META': 'Meta Platforms Inc.',
    'JPM': 'JPMorgan Chase & Co.',
    'V': 'Visa Inc.',
    'WMT': 'Walmart Inc.'
  }
  return names[ticker] || `${ticker} Corporation`
}

function getIdentityTag(ticker: string, identityType: string): string | null {
  // Identity-relevant tags based on user type
  const diasporaTags: Record<string, string> = {
    'JPM': 'Global Banking',
    'V': 'Cross-Border',
  }
  
  const youthTags: Record<string, string> = {
    'AAPL': 'Beginner-Friendly',
    'NVDA': 'Tech Growth',
  }
  
  const creatorTags: Record<string, string> = {
    'META': 'Creator Economy',
    'GOOGL': 'Digital Platform',
  }
  
  const legacyTags: Record<string, string> = {
    'JPM': 'Dividend Stock',
    'WMT': 'Blue Chip',
  }
  
  if (identityType === 'diaspora') return diasporaTags[ticker] || null
  if (identityType === 'youth') return youthTags[ticker] || null
  if (identityType === 'creator') return creatorTags[ticker] || null
  if (identityType === 'legacy') return legacyTags[ticker] || null
  
  return null
}
