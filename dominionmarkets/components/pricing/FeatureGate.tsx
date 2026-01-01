/**
 * Feature Gate Component
 * ======================
 * Upgrade prompts at natural trigger points
 */

"use client"

import { Lock, TrendingUp, BarChart3, FileText, Bell, Crown, Zap } from 'lucide-react'

interface FeatureGateProps {
  feature: 'diversification' | 'volatility' | 'full_heatmap' | 'earnings_calendar' | 
           'cultural_alpha' | 'multi_source' | 'unlimited_alerts' | 'csv_export' | 
           'multi_portfolio' | 'sector_concentration' | 'earnings_alerts'
  requiredTier: 'premium' | 'pro'
  currentTier: string
  onUpgrade: () => void
  compact?: boolean
}

const FEATURE_CONFIG = {
  diversification: {
    icon: BarChart3,
    title: 'Diversification Score',
    description: 'See how well-balanced your portfolio is across sectors and asset types',
    benefit: 'Understand your risk exposure'
  },
  volatility: {
    icon: TrendingUp,
    title: 'Volatility Summary',
    description: 'Track price fluctuations and market stability indicators',
    benefit: 'Make informed decisions'
  },
  full_heatmap: {
    icon: BarChart3,
    title: 'Full Market Heatmap',
    description: 'See all sectors, industries, and stocks in one comprehensive view',
    benefit: 'Spot market trends instantly'
  },
  earnings_calendar: {
    icon: FileText,
    title: 'Full Earnings Calendar',
    description: 'Track all upcoming earnings releases across the market',
    benefit: 'Stay ahead of announcements'
  },
  cultural_alpha: {
    icon: Zap,
    title: 'Cultural Alpha™ Deep-Dives',
    description: 'Full identity-based market insights and opportunity analysis',
    benefit: 'Discover identity-aligned investments'
  },
  multi_source: {
    icon: FileText,
    title: 'Multi-Source News Breakdown',
    description: 'See which sources confirm each story with trust scores',
    benefit: 'Verify news authenticity'
  },
  unlimited_alerts: {
    icon: Bell,
    title: 'Unlimited Alerts',
    description: 'Create as many price, news, and volume alerts as you need',
    benefit: 'Never miss important movements'
  },
  csv_export: {
    icon: FileText,
    title: 'CSV Export',
    description: 'Download your portfolio data for analysis and record-keeping',
    benefit: 'Analyze data your way'
  },
  multi_portfolio: {
    icon: BarChart3,
    title: 'Multi-Portfolio Support',
    description: 'Track multiple portfolios with institutional-grade analytics',
    benefit: 'Manage complex strategies'
  },
  sector_concentration: {
    icon: BarChart3,
    title: 'Sector Concentration',
    description: 'Analyze your exposure across market sectors',
    benefit: 'Balance your allocations'
  },
  earnings_alerts: {
    icon: Bell,
    title: 'Earnings Alerts',
    description: 'Get notified before and after earnings releases',
    benefit: 'Stay informed on earnings'
  }
}

export default function FeatureGate({ feature, requiredTier, currentTier, onUpgrade, compact = false }: FeatureGateProps) {
  const config = FEATURE_CONFIG[feature]
  const Icon = config.icon
  const tierPrice = requiredTier === 'premium' ? '$14.99/mo' : '$29.99/mo'

  if (compact) {
    return (
      <div className="bg-yellow-50 border-2 border-dominion-gold rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Lock className="h-5 w-5 text-dominion-gold" />
            <div>
              <p className="font-semibold text-gray-900">{config.title}</p>
              <p className="text-sm text-gray-600">
                {requiredTier === 'premium' ? 'Premium' : 'Pro'} feature
              </p>
            </div>
          </div>
          <button
            onClick={onUpgrade}
            className="px-4 py-2 bg-dominion-gold text-dominion-obsidian font-semibold rounded-lg hover:bg-yellow-500 transition-colors text-sm"
          >
            Upgrade
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 border-2 border-dominion-gold rounded-xl p-8">
      <div className="text-center max-w-md mx-auto">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-dominion-gold bg-opacity-20 mb-4">
          <Icon className="h-10 w-10 text-dominion-gold" />
        </div>

        {/* Title */}
        <h3 className="text-2xl font-bold text-gray-900 mb-2 flex items-center justify-center gap-2">
          <Lock className="h-6 w-6 text-dominion-gold" />
          {config.title}
        </h3>

        {/* Description */}
        <p className="text-gray-700 mb-4">{config.description}</p>

        {/* Benefit */}
        <div className="bg-white bg-opacity-50 rounded-lg p-3 mb-6">
          <p className="text-sm text-gray-800">
            <span className="font-semibold">✨ {config.benefit}</span>
          </p>
        </div>

        {/* Tier Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-sm mb-6">
          <Crown className="h-4 w-4 text-dominion-gold" />
          <span className="text-sm font-semibold text-gray-900">
            {requiredTier === 'premium' ? 'Premium' : 'Pro'} • {tierPrice}
          </span>
        </div>

        {/* CTA */}
        <button
          onClick={onUpgrade}
          className="w-full px-8 py-4 bg-dominion-gold text-dominion-obsidian font-bold rounded-lg hover:bg-yellow-500 transition-all shadow-lg hover:shadow-xl text-lg"
        >
          Upgrade to {requiredTier === 'premium' ? 'Premium' : 'Pro'}
        </button>

        {/* Fine Print */}
        <p className="text-xs text-gray-600 mt-4">
          Cancel anytime. Access until end of billing cycle.
        </p>
      </div>
    </div>
  )
}

/**
 * Inline Feature Lock
 * ===================
 * Small lock indicator for disabled features
 */
interface InlineFeatureLockProps {
  featureName: string
  requiredTier: 'premium' | 'pro'
  onUpgrade: () => void
}

export function InlineFeatureLock({ featureName, requiredTier, onUpgrade }: InlineFeatureLockProps) {
  return (
    <div className="inline-flex items-center gap-2 px-3 py-1 bg-yellow-50 border border-dominion-gold rounded-full">
      <Lock className="h-3 w-3 text-dominion-gold" />
      <span className="text-xs font-medium text-gray-700">{featureName}</span>
      <button
        onClick={onUpgrade}
        className="text-xs font-semibold text-dominion-gold hover:text-yellow-600 underline"
      >
        Upgrade
      </button>
    </div>
  )
}

/**
 * Alert Limit Reached Gate
 * =========================
 * Specific to alerts hitting tier limits
 */
interface AlertLimitGateProps {
  currentCount: number
  limit: number
  alertType: string
  onUpgrade: () => void
}

export function AlertLimitGate({ currentCount, limit, alertType, onUpgrade }: AlertLimitGateProps) {
  return (
    <div className="bg-yellow-50 border-2 border-dominion-gold rounded-lg p-6">
      <div className="text-center">
        <div className="text-4xl mb-3">🔒</div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">Alert Limit Reached</h3>
        <p className="text-gray-700 mb-4">
          You've used <span className="font-bold">{currentCount}/{limit}</span> {alertType} alerts
        </p>
        <p className="text-sm text-gray-600 mb-6">
          Upgrade to Premium for <span className="font-semibold">unlimited alerts</span>
        </p>
        <button
          onClick={onUpgrade}
          className="px-8 py-3 bg-dominion-gold text-dominion-obsidian font-semibold rounded-lg hover:bg-yellow-500 transition-colors"
        >
          Upgrade to Premium ($14.99/mo)
        </button>
      </div>
    </div>
  )
}
