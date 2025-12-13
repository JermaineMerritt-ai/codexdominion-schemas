'use client'

import { DashboardTile } from '@/components'

interface IncidentStat {
  id: string
  label: string
  value: string
  icon: string
}

export default function IncidentPanel() {
  const stats: IncidentStat[] = [
    { id: '1', label: 'Active Incidents', value: '0', icon: '✅' },
    { id: '2', label: 'Resolved This Week', value: '3', icon: '✔️' },
    { id: '3', label: 'Avg Response Time', value: '12m', icon: '⏱️' },
    { id: '4', label: 'Resolution Rate', value: '100%', icon: '📈' },
  ] as const

  return (
    <DashboardTile title="Incident Response" icon="🚨" action={{ label: "+ Report", onClick: () => {} }}>
      <div className="text-center py-4 mb-4 codex-panel bg-green-500/10 border-green-500/30">
        <div className="text-4xl mb-2">✅</div>
        <p className="text-sm text-codex-parchment/70">No active incidents</p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {stats.map((stat) => (
          <div key={stat.id} className="codex-panel text-center hover:bg-codex-gold/10">
            <div className="text-2xl mb-1">{stat.icon}</div>
            <div className="text-lg font-bold text-codex-gold">{stat.value}</div>
            <div className="text-xs text-codex-parchment/60">{stat.label}</div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
