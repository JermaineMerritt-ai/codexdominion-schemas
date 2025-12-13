'use client'

import { useEffect, useState } from 'react'

interface RevenueMetric {
  label: string
  value: string
  change: number
  trend: 'up' | 'down' | 'stable'
}

export default function RevenueImpactPanel() {
  const [metrics, setMetrics] = useState<RevenueMetric[]>([])

  useEffect(() => {
    const mockMetrics: RevenueMetric[] = [
      { label: 'Today', value: '$127.50', change: 15.3, trend: 'up' },
      { label: 'This Week', value: '$892.00', change: 8.7, trend: 'up' },
      { label: 'This Month', value: '$3,456.00', change: -2.1, trend: 'down' },
      { label: 'MRR', value: '$2,150.00', change: 5.4, trend: 'up' },
    ]
    setMetrics(mockMetrics)
  }, [])

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return '📈'
      case 'down': return '📉'
      case 'stable': return '➡️'
      default: return '➡️'
    }
  }

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up': return 'text-green-400'
      case 'down': return 'text-red-400'
      case 'stable': return 'text-gray-400'
      default: return 'text-gray-400'
    }
  }

  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        💰 Revenue Impact
      </h2>

      <div className="space-y-4">
        {metrics.map((metric, idx) => (
          <div key={idx} className="codex-panel">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs text-codex-parchment/60">{metric.label}</span>
              <span className="text-lg">{getTrendIcon(metric.trend)}</span>
            </div>
            <div className="flex items-end justify-between">
              <span className="text-2xl font-bold text-codex-gold">{metric.value}</span>
              <span className={`text-sm ${getTrendColor(metric.trend)}`}>
                {metric.change > 0 ? '+' : ''}{metric.change.toFixed(1)}%
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-codex-gold/20">
        <button className="codex-button w-full text-sm">
          📊 View Full Treasury
        </button>
      </div>
    </div>
  )
}
