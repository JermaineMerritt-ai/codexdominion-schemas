/**
 * Pricing Page
 * ============
 * Three-tier subscription comparison
 */

"use client"

import { Check, Crown, Zap, Sparkles, Globe, Sprout, Lightbulb, Crown as LegacyIcon } from 'lucide-react'

interface PricingPageProps {
  currentTier: string
  identityType: string
  onSelectTier: (tier: string) => void
}

export default function PricingPage({ currentTier, identityType, onSelectTier }: PricingPageProps) {
  const tiers = [
    {
      id: 'free',
      name: 'Free',
      price: '$0',
      period: 'forever',
      description: 'Powerful starting point for beginners',
      icon: Sparkles,
      color: 'border-gray-200',
      buttonClass: 'bg-gray-200 text-gray-700 hover:bg-gray-300',
      features: [
        'Dashboard & Markets',
        'Portfolio (basic)',
        'News feed (limited)',
        '5 alerts max',
        '5 AI summaries/day',
        'Identity-based widgets',
        'Cultural Alpha preview',
        'Diaspora Flow Maps preview',
        'Creator Index preview',
        'Youth learning badges',
        'Legacy-builder charts (basic)'
      ],
      limitations: [
        'Limited news verification',
        'Limited analytics',
        'No earnings alerts',
        'No CSV export',
        'No multi-portfolio'
      ]
    },
    {
      id: 'premium',
      name: 'Premium',
      price: '$14.99',
      period: '/month',
      description: 'Full DominionMarkets experience',
      icon: Zap,
      color: 'border-dominion-gold',
      buttonClass: 'bg-dominion-gold text-dominion-obsidian hover:bg-yellow-500',
      popular: true,
      features: [
        '✨ Everything in Free, plus:',
        'Diversification score',
        'Volatility summary',
        'Sector concentration',
        'Identity alignment insights',
        'Cultural Alpha full score',
        'Diaspora Flow Maps (full)',
        'Unlimited verified news',
        'Multi-source breakdown',
        'Historical timelines',
        'Unlimited alerts',
        'Custom alert conditions',
        'Earnings alerts',
        'Unlimited AI summaries',
        'Identity-aware interpretations',
        'Full heatmap',
        'Full movers list',
        'Full earnings calendar'
      ]
    },
    {
      id: 'pro',
      name: 'Pro',
      price: '$29.99',
      period: '/month',
      description: 'Advanced tools for power users',
      icon: Crown,
      color: 'border-purple-500',
      buttonClass: 'bg-gradient-to-r from-purple-600 to-purple-700 text-white hover:from-purple-700 hover:to-purple-800',
      features: [
        '👑 Everything in Premium, plus:',
        'Multi-portfolio support',
        'CSV export',
        'Institutional-grade charts',
        'Multi-portfolio analytics',
        'Multi-portfolio alert sets',
        'Advanced alert conditions',
        'Institutional sector analytics',
        'Deep-dive cultural heatmaps',
        'Multi-portfolio AI summaries',
        'Advanced identity insights',
        'Historical datasets',
        'Priority support',
        'Early feature access'
      ]
    }
  ]

  const getIdentityBenefits = (tierId: string) => {
    const benefits: Record<string, Record<string, string[]>> = {
      diaspora: {
        premium: [
          'Full Diaspora Flow Maps',
          'Regional sector analytics',
          'Diaspora-linked company insights'
        ],
        pro: [
          'Multi-region comparisons',
          'Historical diaspora trends'
        ]
      },
      youth: {
        premium: [
          'Advanced learning modules',
          'Unlimited mock portfolios',
          'Youth-focused analytics'
        ],
        pro: [
          'CSV export for school projects',
          'Multi-portfolio comparisons'
        ]
      },
      creator: {
        premium: [
          'Creator-economy deep-dives',
          'AI-tool sector analytics',
          'Digital-product platform insights'
        ],
        pro: [
          'Multi-portfolio creator tracking',
          'CSV export for business planning'
        ]
      },
      legacy: {
        premium: [
          'Dividend analytics',
          'Long-term stability insights',
          'Wealth-preservation indicators'
        ],
        pro: [
          'Multi-portfolio retirement planning',
          'Institutional-grade charts'
        ]
      }
    }

    return benefits[identityType]?.[tierId] || []
  }

  const getIdentityIcon = () => {
    switch (identityType) {
      case 'diaspora': return Globe
      case 'youth': return Sprout
      case 'creator': return Lightbulb
      case 'legacy': return LegacyIcon
      default: return Sparkles
    }
  }

  const IdentityIcon = getIdentityIcon()
  const identityLabel = identityType.charAt(0).toUpperCase() + identityType.slice(1)

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-16 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600 mb-4">
            Keep the platform accessible. Deliver meaningful value at every level.
          </p>
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white rounded-full shadow-sm border border-gray-200">
            <IdentityIcon className="h-5 w-5 text-dominion-gold" />
            <span className="text-sm font-medium text-gray-700">
              Personalized for {identityLabel}
            </span>
          </div>
        </div>

        {/* Tier Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {tiers.map((tier) => {
            const Icon = tier.icon
            const isCurrentTier = currentTier === tier.id
            const identityBenefits = getIdentityBenefits(tier.id)

            return (
              <div
                key={tier.id}
                className={`relative bg-white rounded-2xl shadow-xl border-2 ${tier.color} p-8 ${
                  tier.popular ? 'md:scale-105 z-10' : ''
                }`}
              >
                {/* Popular Badge */}
                {tier.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="px-4 py-1 bg-dominion-gold text-dominion-obsidian text-sm font-bold rounded-full shadow-lg">
                      MOST POPULAR
                    </span>
                  </div>
                )}

                {/* Current Tier Badge */}
                {isCurrentTier && (
                  <div className="absolute top-6 right-6">
                    <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full">
                      Current Plan
                    </span>
                  </div>
                )}

                {/* Header */}
                <div className="text-center mb-6">
                  <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full ${
                    tier.id === 'free' ? 'bg-gray-100' :
                    tier.id === 'premium' ? 'bg-yellow-100' :
                    'bg-purple-100'
                  } mb-4`}>
                    <Icon className={`h-8 w-8 ${
                      tier.id === 'free' ? 'text-gray-600' :
                      tier.id === 'premium' ? 'text-dominion-gold' :
                      'text-purple-600'
                    }`} />
                  </div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-2">{tier.name}</h2>
                  <p className="text-gray-600 mb-4">{tier.description}</p>
                  <div className="mb-6">
                    <span className="text-5xl font-bold text-gray-900">{tier.price}</span>
                    <span className="text-gray-600 text-lg">{tier.period}</span>
                  </div>
                  <button
                    onClick={() => onSelectTier(tier.id)}
                    disabled={isCurrentTier}
                    className={`w-full px-6 py-3 rounded-lg font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed ${tier.buttonClass}`}
                  >
                    {isCurrentTier ? 'Current Plan' : 
                     tier.id === 'free' ? 'Get Started' : 
                     `Upgrade to ${tier.name}`}
                  </button>
                </div>

                {/* Features */}
                <div className="space-y-3 mb-6">
                  {tier.features.map((feature, index) => (
                    <div key={index} className="flex items-start gap-3">
                      <Check className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                      <span className="text-sm text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>

                {/* Limitations (Free tier only) */}
                {tier.limitations && (
                  <div className="pt-6 border-t border-gray-200">
                    <p className="text-xs font-semibold text-gray-500 mb-3 uppercase">Limitations</p>
                    <div className="space-y-2">
                      {tier.limitations.map((limitation, index) => (
                        <p key={index} className="text-xs text-gray-500">• {limitation}</p>
                      ))}
                    </div>
                  </div>
                )}

                {/* Identity-Specific Benefits */}
                {identityBenefits.length > 0 && (
                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <div className="flex items-center gap-2 mb-3">
                      <IdentityIcon className="h-4 w-4 text-dominion-gold" />
                      <p className="text-sm font-semibold text-gray-900">For {identityLabel}</p>
                    </div>
                    <div className="space-y-2">
                      {identityBenefits.map((benefit, index) => (
                        <div key={index} className="flex items-start gap-2">
                          <Sparkles className="h-4 w-4 text-dominion-gold flex-shrink-0 mt-0.5" />
                          <span className="text-sm text-gray-700">{benefit}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {/* No Predictions Disclaimer */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center max-w-3xl mx-auto">
          <p className="text-sm text-gray-600 mb-2">
            <span className="font-semibold">No Predictions. No Recommendations. No Advice.</span>
          </p>
          <p className="text-xs text-gray-500">
            All tiers provide descriptive insights only. DominionMarkets never offers predictions, recommendations, or financial advice at any price point.
          </p>
        </div>

        {/* FAQ */}
        <div className="mt-16 max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">Frequently Asked Questions</h2>
          <div className="space-y-6">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Can I cancel anytime?</h3>
              <p className="text-gray-600">Yes. You retain access until the end of your billing cycle.</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">What payment methods do you accept?</h3>
              <p className="text-gray-600">We accept all major credit cards via our payment processor.</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Can I switch between Premium and Pro?</h3>
              <p className="text-gray-600">Yes. Upgrades are immediate. Downgrades take effect at the end of your billing cycle.</p>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Do you offer refunds?</h3>
              <p className="text-gray-600">Refunds are handled by our payment processor on a case-by-case basis.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
