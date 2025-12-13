'use client'

import { DashboardTile } from '@/components'

export default function MarketContentPanel() {
  const actions = [
    { id: '1', icon: '✨', label: 'Generate Promo Content' },
    { id: '2', icon: '📊', label: 'View Analytics' },
    { id: '3', icon: '🔗', label: 'Create Tracking Link' },
    { id: '4', icon: '📧', label: 'Email Templates' },
  ] as const

  const stats = [
    { label: 'Total Revenue', value: '$1,582.00', color: 'text-codex-gold' },
    { label: 'Active Links', value: '157', color: 'text-green-400' },
    { label: 'Avg Commission', value: '12.5%', color: 'text-blue-400' },
    { label: 'This Month', value: '+28%', color: 'text-purple-400' },
  ] as const

  return (
    <DashboardTile title="Marketing Content" icon="📢">
      <div className="space-y-3 mb-6">
        {actions.map((action) => (
          <button key={action.id} className="codex-button w-full text-sm justify-start">
            <span className="mr-2">{action.icon}</span>
            {action.label}
          </button>
        ))}
      </div>

      <div className="codex-panel">
        <h3 className="font-semibold text-sm mb-3 text-codex-parchment">Quick Stats</h3>
        <div className="space-y-2 text-xs">
          {stats.map((stat, idx) => (
            <div key={idx} className="flex justify-between items-center">
              <span className="text-codex-parchment/70">{stat.label}</span>
              <span className={`font-bold ${stat.color}`}>{stat.value}</span>
            </div>
          ))}
        </div>
      </div>
    </DashboardTile>
  )
}
