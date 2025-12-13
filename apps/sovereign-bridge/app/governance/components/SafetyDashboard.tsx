'use client'

import { DashboardTile } from '@/components'

interface SafetyMetric {
  id: string
  value: string
  label: string
  color: string
}

export default function SafetyDashboard() {
  const metrics: SafetyMetric[] = [
    { id: '1', value: '100%', label: 'Compliance Rate', color: 'text-green-400' },
    { id: '2', value: '0', label: 'Active Incidents', color: 'text-green-400' },
    { id: '3', value: '847', label: 'Audits Passed', color: 'text-blue-400' },
    { id: '4', value: 'A+', label: 'Safety Score', color: 'text-codex-gold' },
  ] as const

  return (
    <DashboardTile title="Safety Status" icon="🛡️" action={{ label: "📋 Audit", onClick: () => {} }}>
      <div className="space-y-3">
        {metrics.map((metric) => (
          <div key={metric.id} className="codex-panel hover:bg-codex-gold/10">
            <div className={`text-2xl font-bold ${metric.color}`}>{metric.value}</div>
            <div className="text-xs text-codex-parchment/60">{metric.label}</div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
