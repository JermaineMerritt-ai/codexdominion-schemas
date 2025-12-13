'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface FunnelStep {
  id: string
  name: string
  conversionRate: string
  status: 'active' | 'pending'
}

export default function FunnelBuilder() {
  const steps: FunnelStep[] = [
    { id: '1', name: 'Landing Page', conversionRate: '45%', status: 'active' },
    { id: '2', name: 'Product Page', conversionRate: '32%', status: 'active' },
    { id: '3', name: 'Checkout', conversionRate: '78%', status: 'active' },
    { id: '4', name: 'Upsell', conversionRate: '25%', status: 'pending' },
  ]

  return (
    <DashboardTile title="Sales Funnel" icon="🎯" action={{ label: "⚙️ Configure", onClick: () => {} }}>
      <div className="space-y-3">
        {steps.map((step, idx) => (
          <div key={step.id} className="codex-panel">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <span className="text-codex-gold font-bold text-lg">{idx + 1}</span>
                <div>
                  <div className="text-sm font-medium text-codex-parchment">{step.name}</div>
                  <div className="text-xs text-codex-parchment/60">Conversion: {step.conversionRate}</div>
                </div>
              </div>
              <StatusBadge status={step.status === 'active' ? 'success' : 'pending'} />
            </div>
            {idx < steps.length - 1 && (
              <div className="ml-4 mt-2 flex items-center gap-2">
                <div className="w-0.5 h-4 bg-codex-gold/30" />
                <span className="text-xs text-codex-parchment/40">↓</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
