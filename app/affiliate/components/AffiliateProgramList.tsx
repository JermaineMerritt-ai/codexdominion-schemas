'use client'

export default function AffiliateProgramList() {
  const programs = [
    { name: 'Amazon Associates', products: 89, clicks: 2847, conversions: 156, revenue: '$892.00' },
    { name: 'ShareASale', products: 45, clicks: 1523, conversions: 78, revenue: '$456.00' },
    { name: 'ClickBank', products: 23, clicks: 892, conversions: 34, revenue: '$234.00' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-2xl font-serif text-codex-gold mb-6">
        Affiliate Programs
      </h2>

      <div className="space-y-4">
        {programs.map((program, idx) => (
          <div key={idx} className="codex-panel hover:bg-codex-gold/10 transition-all">
            <h3 className="font-semibold mb-3">{program.name}</h3>
            <div className="grid grid-cols-4 gap-2 text-center text-xs">
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
    </div>
  )
}
