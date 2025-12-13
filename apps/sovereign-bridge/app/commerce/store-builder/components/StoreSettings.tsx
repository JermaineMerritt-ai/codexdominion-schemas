'use client'

import { DashboardTile } from '@/components'

export default function StoreSettings() {
  const settings = [
    { key: 'Store Name', value: 'Codex Dominion Store' },
    { key: 'Currency', value: 'USD ($)' },
    { key: 'Tax Rate', value: '8.5%' },
    { key: 'Shipping', value: 'Digital Only' },
    { key: 'Payment Gateway', value: 'Stripe' },
    { key: 'Checkout Type', value: 'Express' },
  ]

  return (
    <DashboardTile title="Store Settings" icon="⚙️" action={{ label: "Edit All", onClick: () => {} }}>
      <div className="space-y-2">
        {settings.map((setting, idx) => (
          <div key={idx} className="flex items-center justify-between py-2 border-b border-codex-gold/10 last:border-0">
            <span className="text-sm text-codex-parchment/70">{setting.key}</span>
            <span className="text-sm font-medium text-codex-parchment">{setting.value}</span>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
