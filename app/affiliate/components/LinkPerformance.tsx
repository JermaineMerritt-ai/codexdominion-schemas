'use client'

export default function LinkPerformance() {
  const links = [
    { product: 'Kids Bible Story Pack', clicks: 847, conversions: 45, ctr: '5.3%', revenue: '$67.50' },
    { product: 'Wedding Printables Bundle', clicks: 623, conversions: 34, ctr: '5.5%', revenue: '$101.66' },
    { product: 'Homeschool Starter Kit', clicks: 456, conversions: 23, ctr: '5.0%', revenue: '$45.77' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-2xl font-serif text-codex-gold mb-6">
        Top Performing Links
      </h2>

      <div className="space-y-3">
        {links.map((link, idx) => (
          <div key={idx} className="codex-panel">
            <div className="flex items-start justify-between mb-3">
              <h3 className="font-semibold text-sm">{link.product}</h3>
              <span className="text-lg font-bold text-codex-gold">{link.revenue}</span>
            </div>
            <div className="grid grid-cols-3 gap-2 text-center text-xs">
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
    </div>
  )
}
