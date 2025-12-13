'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface Policy {
  id: string
  name: string
  status: 'active' | 'pending' | 'success'
  lastReview: string
  violations: number
}

export default function PolicyDashboard() {
  const policies: Policy[] = [
    { id: '1', name: 'Content Safety Policy', status: 'success', lastReview: '2024-12-01', violations: 0 },
    { id: '2', name: 'Data Privacy Policy', status: 'success', lastReview: '2024-11-15', violations: 0 },
    { id: '3', name: 'AI Usage Guidelines', status: 'success', lastReview: '2024-12-10', violations: 0 },
    { id: '4', name: 'Revenue Compliance', status: 'success', lastReview: '2024-11-30', violations: 0 },
    { id: '5', name: 'Security Standards', status: 'active', lastReview: '2024-12-05', violations: 0 },
  ] as const

  return (
    <DashboardTile title="Active Policies" icon="📋" action={{ label: "+ New Policy", onClick: () => {} }}>
      <div className="space-y-3">
        {policies.map((policy) => (
          <div key={policy.id} className="codex-panel border-l-2 border-green-500 hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-start justify-between mb-2">
              <div className="flex-1">
                <h3 className="font-semibold text-sm text-codex-parchment">{policy.name}</h3>
                <p className="text-xs text-codex-parchment/60 mt-1">Last review: {policy.lastReview}</p>
              </div>
              <StatusBadge status={policy.status} />
            </div>
            <div className="flex items-center justify-between text-xs">
              <span className="text-codex-parchment/70">Violations</span>
              <span className="font-bold text-green-400">{policy.violations}</span>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
