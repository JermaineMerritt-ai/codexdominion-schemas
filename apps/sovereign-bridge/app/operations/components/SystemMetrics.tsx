'use client'

import { DashboardTile } from '@/components'

interface Metric {
  id: string
  label: string
  value: string
  trend: string
  color: string
}

export default function SystemMetrics() {
  const metrics: Metric[] = [
    { id: '1', label: 'Active Engines', value: '4', trend: '↑', color: 'text-green-400' },
    { id: '2', label: 'Running Tasks', value: '3', trend: '→', color: 'text-blue-400' },
    { id: '3', label: 'Total Projects', value: '12', trend: '↑', color: 'text-purple-400' },
    { id: '4', label: 'System Uptime', value: '99.9%', trend: '↑', color: 'text-codex-gold' },
  ] as const

  return (
    <DashboardTile title="System Overview" icon="📊">
      <div className="grid grid-cols-2 gap-3">
        {metrics.map((metric) => (
          <div key={metric.id} className="codex-panel text-center hover:bg-codex-gold/10">
            <div className={`text-2xl font-bold ${metric.color} mb-1`}>
              {metric.value}
              <span className="text-sm ml-1">{metric.trend}</span>
            </div>
            <div className="text-xs text-codex-parchment/60">{metric.label}</div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
