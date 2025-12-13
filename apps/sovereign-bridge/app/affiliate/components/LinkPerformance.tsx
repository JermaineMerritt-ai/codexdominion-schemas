'use client'

import { DashboardTile } from '@/components'

interface PerformingLink {
  id: string
  product: string
  clicks: number
  conversions: number
  ctr: string
  revenue: string
}

export default function LinkPerformance() {
  const links: PerformingLink[] = [
    { id: '1', product: 'Kids Bible Story Pack', clicks: 847, conversions: 45, ctr: '5.3%', revenue: '$67.50' },
    { id: '2', product: 'Wedding Printables Bundle', clicks: 623, conversions: 34, ctr: '5.5%', revenue: '$101.66' },
    { id: '3', product: 'Homeschool Starter Kit', clicks: 456, conversions: 23, ctr: '5.0%', revenue: '$45.77' },
    { id: '4', product: 'Christmas Coloring Pack', clicks: 389, conversions: 19, ctr: '4.9%', revenue: '$38.00' },
  ] as const

  return (
    <DashboardTile title="Top Performing Links" icon="🔗" action={{ label: "📊 View All", onClick: () => {} }}>
      <div className="space-y-3">
        {links.map((link) => (
          <div key={link.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-start justify-between mb-3">
              <h3 className="font-semibold text-sm text-codex-parchment">{link.product}</h3>
              <span className="text-lg font-bold text-codex-gold">{link.revenue}</span>
            </div>
            <div className="grid grid-cols-3 gap-3 text-center text-xs">
              <div>
                <div className="font-bold text-blue-400">{link.clicks}</div>
                <div className="text-codex-parchment/60">Clicks</div>
              </div>
              <div>
                <div className="font-bold text-green-400">{link.conversions}</div>
                <div className="text-codex-parchment/60">Sales</div>
              </div>
              <div>
                <div className="font-bold text-purple-400">{link.ctr}</div>
                <div className="text-codex-parchment/60">CTR</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
