'use client'

import { SimpleBarChart, TrendLine } from '@/components'

interface EngineHistoryProps {
  engineId?: string
}

export default function EngineHistory({ engineId }: EngineHistoryProps) {
  const uptimeData = [98.5, 99.2, 99.1, 99.8, 99.5, 99.7, 99.8]
  const uptimeLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

  const performanceData = [
    { label: 'Requests', value: 45230, color: '#d4af37' },
    { label: 'Success', value: 44980, color: '#10b981' },
    { label: 'Errors', value: 125, color: '#ef4444' },
    { label: 'Retries', value: 125, color: '#f59e0b' },
  ]

  return (
    <div className="space-y-6">
      {/* Uptime Trend */}
      <div>
        <h4 className="text-sm font-semibold text-codex-gold mb-3">7-Day Uptime Trend</h4>
        <TrendLine
          data={uptimeData}
          labels={uptimeLabels}
          color="#d4af37"
        />
      </div>

      {/* Performance Stats */}
      <div>
        <h4 className="text-sm font-semibold text-codex-gold mb-3">Weekly Performance</h4>
        <SimpleBarChart
          data={performanceData}
        />
      </div>

      {/* Historical Events */}
      <div>
        <h4 className="text-sm font-semibold text-codex-gold mb-3">Recent Events</h4>
        <div className="space-y-2">
          <div className="codex-panel text-xs">
            <div className="flex justify-between mb-1">
              <span className="text-codex-parchment">Version Update</span>
              <span className="text-codex-parchment/50">2 days ago</span>
            </div>
            <p className="text-codex-parchment/70">Upgraded to v2.1.0 with performance improvements</p>
          </div>
          <div className="codex-panel text-xs">
            <div className="flex justify-between mb-1">
              <span className="text-codex-parchment">Configuration Change</span>
              <span className="text-codex-parchment/50">5 days ago</span>
            </div>
            <p className="text-codex-parchment/70">Increased worker pool size from 4 to 8</p>
          </div>
          <div className="codex-panel text-xs">
            <div className="flex justify-between mb-1">
              <span className="text-codex-parchment">Maintenance Window</span>
              <span className="text-codex-parchment/50">1 week ago</span>
            </div>
            <p className="text-codex-parchment/70">Scheduled downtime for database migration</p>
          </div>
        </div>
      </div>
    </div>
  )
}
