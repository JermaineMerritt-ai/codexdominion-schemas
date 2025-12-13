'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface AffiliateProgram {
  id: string
  name: string
  products: number
  clicks: number
  conversions: number
  revenue: string
  status: 'active' | 'pending'
}

export default function AffiliateProgramList() {
  const programs: AffiliateProgram[] = [
    { id: '1', name: 'Amazon Associates', products: 89, clicks: 2847, conversions: 156, revenue: '$892.00', status: 'active' },
    { id: '2', name: 'ShareASale', products: 45, clicks: 1523, conversions: 78, revenue: '$456.00', status: 'active' },
    { id: '3', name: 'ClickBank', products: 23, clicks: 892, conversions: 34, revenue: '$234.00', status: 'active' },
    { id: '4', name: 'CJ Affiliate', products: 12, clicks: 456, conversions: 18, revenue: '$156.00', status: 'pending' },
  ] as const

  return (
    <DashboardTile title="Affiliate Programs" icon="🤝" action={{ label: "+ Add Program", onClick: () => {} }}>
      <div className="space-y-3">
        {programs.map((program) => (
          <div key={program.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-codex-parchment">{program.name}</h3>
              <StatusBadge status={program.status === 'active' ? 'success' : 'pending'} />
            </div>
            <div className="grid grid-cols-4 gap-3 text-center text-xs">
              <div>
                <div className="font-bold text-codex-gold">{program.products}</div>
                <div className="text-codex-parchment/60">Products</div>
              </div>
              <div>
                <div className="font-bold text-blue-400">{program.clicks.toLocaleString()}</div>
                <div className="text-codex-parchment/60">Clicks</div>
              </div>
              <div>
                <div className="font-bold text-green-400">{program.conversions}</div>
                <div className="text-codex-parchment/60">Sales</div>
              </div>
              <div>
                <div className="font-bold text-purple-400">{program.revenue}</div>
                <div className="text-codex-parchment/60">Revenue</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
