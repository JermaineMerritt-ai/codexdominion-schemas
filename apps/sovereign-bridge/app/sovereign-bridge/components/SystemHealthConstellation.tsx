'use client'

import { useEffect, useState } from 'react'
import { DashboardTile, StatusBadge, HealthIndicator } from '@/components'

interface HealthMetric {
  category: string
  status: 'active' | 'degraded' | 'error'
  details: string
}

export default function SystemHealthConstellation() {
  const [health, setHealth] = useState<HealthMetric[]>([])
  const [overallHealth, setOverallHealth] = useState<string>('GOOD')

  useEffect(() => {
    // In production, fetch from /api/ritual-status
    const mockHealth: HealthMetric[] = [
      { category: 'GitHub Workflows', status: 'active', details: '41 workflows' },
      { category: 'Docker Containers', status: 'active', details: '3/3 running' },
      { category: 'Scheduled Capsules', status: 'active', details: '5/5 operational' },
      { category: 'Ledger Integrity', status: 'active', details: '5/5 valid' },
      { category: 'Background Processes', status: 'active', details: '8 processes' },
      { category: 'System Services', status: 'active', details: '7 services' },
      { category: 'Scheduled Tasks', status: 'active', details: '2 tasks' },
    ]
    setHealth(mockHealth)
    setOverallHealth('GOOD')
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400 border-green-500/30 bg-green-500/10'
      case 'degraded': return 'text-yellow-400 border-yellow-500/30 bg-yellow-500/10'
      case 'error': return 'text-red-400 border-red-500/30 bg-red-500/10'
      default: return 'text-gray-400 border-gray-500/30 bg-gray-500/10'
    }
  }

  const getHealthEmoji = (health: string) => {
    switch (health) {
      case 'EXCELLENT': return '✅'
      case 'GOOD': return '🟢'
      case 'FAIR': return '🟡'
      case 'NEEDS_ATTENTION': return '🔴'
      default: return '❓'
    }
  }

  return (
    <div className="codex-card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-serif text-codex-gold">
          System Health Constellation
        </h2>
        <div className="flex items-center space-x-2">
          <span className="text-2xl">{getHealthEmoji(overallHealth)}</span>
          <span className="text-lg font-semibold">{overallHealth}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {health.map((metric, idx) => (
          <div
            key={idx}
            className={`codex-panel border ${getStatusColor(metric.status)} transition-all hover:scale-105`}
          >
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-semibold text-sm">{metric.category}</h3>
              <span className={`text-xs px-2 py-1 rounded ${getStatusColor(metric.status)}`}>
                {metric.status.toUpperCase()}
              </span>
            </div>
            <p className="text-xs text-codex-parchment/70">{metric.details}</p>
          </div>
        ))}
      </div>

      <div className="mt-6 pt-6 border-t border-codex-gold/20">
        <div className="flex items-center justify-between text-sm">
          <span className="text-codex-parchment/70">Active Rituals</span>
          <span className="font-semibold text-green-400">7/7 (100%)</span>
        </div>
        <div className="w-full bg-codex-navy/50 rounded-full h-2 mt-2">
          <div className="bg-green-500 h-2 rounded-full" style={{ width: '100%' }}></div>
        </div>
      </div>
    </div>
  )
}
