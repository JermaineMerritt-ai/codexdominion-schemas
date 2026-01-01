/**
 * Identity Filters
 * ================
 * Identity-aware content filtering for personalized news feed
 */

"use client"

interface IdentityFiltersProps {
  currentIdentity: string
  onChange: (identity: string) => void
  userIdentity: string
}

export default function IdentityFilters({ currentIdentity, onChange, userIdentity }: IdentityFiltersProps) {
  const identities = [
    {
      value: 'all',
      label: 'All News',
      emoji: '📰',
      description: 'View all verified articles'
    },
    {
      value: 'diaspora',
      label: 'Global Investors',
      emoji: '🌍',
      description: 'International markets, forex, cross-border investing',
      topics: ['Emerging markets', 'Currency trends', 'Global trade']
    },
    {
      value: 'youth',
      label: 'Young Investors',
      emoji: '📚',
      description: 'Beginner-friendly content, ETFs, tech stocks',
      topics: ['Getting started', 'Index funds', 'Retirement planning']
    },
    {
      value: 'creator',
      label: 'Creators',
      emoji: '💡',
      description: 'IPOs, creator economy, business tax strategies',
      topics: ['Startup funding', 'Creator platforms', 'Small business']
    },
    {
      value: 'legacy',
      label: 'Legacy Builders',
      emoji: '👑',
      description: 'Dividends, estate planning, value investing',
      topics: ['Dividend aristocrats', 'Estate planning', 'Wealth transfer']
    }
  ]

  const selectedIdentity = identities.find(i => i.value === currentIdentity)

  return (
    <div className="mb-6">
      {/* Filter Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-2">
        <div className="flex gap-2 overflow-x-auto">
          {identities.map(identity => (
            <button
              key={identity.value}
              onClick={() => onChange(identity.value)}
              className={`flex items-center px-4 py-2 rounded-lg whitespace-nowrap transition-all ${
                currentIdentity === identity.value
                  ? 'bg-dominion-gold text-gray-900 font-semibold'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
              }`}
            >
              <span className="text-xl mr-2">{identity.emoji}</span>
              {identity.label}
            </button>
          ))}
        </div>
      </div>

      {/* Identity Description */}
      {selectedIdentity && selectedIdentity.value !== 'all' && (
        <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start">
            <span className="text-3xl mr-3">{selectedIdentity.emoji}</span>
            <div className="flex-1">
              <h3 className="font-semibold text-blue-900 mb-1">
                {selectedIdentity.label}
              </h3>
              <p className="text-sm text-blue-800 mb-2">
                {selectedIdentity.description}
              </p>
              {selectedIdentity.topics && (
                <div className="flex flex-wrap gap-2">
                  {selectedIdentity.topics.map(topic => (
                    <span
                      key={topic}
                      className="px-2 py-1 bg-blue-100 rounded text-xs font-medium text-blue-700"
                    >
                      {topic}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* User Identity Indicator */}
      {userIdentity && userIdentity !== 'all' && currentIdentity === 'all' && (
        <div className="mt-3 text-center">
          <button
            onClick={() => onChange(userIdentity)}
            className="text-sm text-dominion-gold hover:underline"
          >
            Show me {identities.find(i => i.value === userIdentity)?.label} content →
          </button>
        </div>
      )}
    </div>
  )
}
