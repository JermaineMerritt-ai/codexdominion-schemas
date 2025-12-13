'use client'

import { MetricCard, MetricCardGrid } from '@/components'

interface EngineMetricsProps {
  engineId?: string
}

export default function EngineMetrics({ engineId }: EngineMetricsProps) {
  const metrics = [
    { label: 'Uptime', value: '99.8%', icon: '⏱️', trend: 'up' as const, trendValue: '+0.2%', color: 'green' as const },
    { label: 'Throughput', value: '1.2K/s', icon: '⚡', trend: 'up' as const, trendValue: '+15%', color: 'blue' as const },
    { label: 'Response Time', value: '45ms', icon: '🚀', trend: 'down' as const, trendValue: '-12ms', color: 'gold' as const },
    { label: 'Error Rate', value: '0.02%', icon: '⚠️', trend: 'down' as const, trendValue: '-0.01%', color: 'green' as const },
    { label: 'Memory Usage', value: '2.1GB', icon: '💾', trend: 'neutral' as const, color: 'purple' as const },
    { label: 'CPU Load', value: '34%', icon: '🔥', trend: 'neutral' as const, color: 'blue' as const },
  ]

  return (
    <MetricCardGrid cols={3}>
      {metrics.map((metric, idx) => (
        <MetricCard
          key={idx}
          label={metric.label}
          value={metric.value}
          icon={metric.icon}
          trend={metric.trend}
          trendValue={metric.trendValue}
          color={metric.color}
        />
      ))}
    </MetricCardGrid>
  )
}
