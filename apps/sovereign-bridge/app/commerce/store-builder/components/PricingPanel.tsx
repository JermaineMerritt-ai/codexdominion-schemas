'use client'

import { useState } from 'react'
import { DashboardTile } from '@/components'

interface PricingTier {
  id: string
  name: string
  price: number
  interval: string
}

export default function PricingPanel() {
  const [tiers, setTiers] = useState<PricingTier[]>([
    { id: '1', name: 'Basic Plan', price: 9.99, interval: 'month' },
    { id: '2', name: 'Pro Plan', price: 19.99, interval: 'month' },
    { id: '3', name: 'Enterprise', price: 49.99, interval: 'month' },
  ])

  return (
    <DashboardTile title="Pricing Tiers" icon="💰" action={{ label: "+ Add Tier", onClick: () => {} }}>
      <div className="space-y-3">
        {tiers.map((tier) => (
          <div key={tier.id} className="codex-panel">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-codex-parchment">{tier.name}</span>
              <button className="text-xs codex-button py-1 px-3">Edit</button>
            </div>
            <div className="flex items-baseline gap-1">
              <span className="text-2xl text-codex-gold font-bold">${tier.price}</span>
              <span className="text-sm text-codex-parchment/60">/ {tier.interval}</span>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
