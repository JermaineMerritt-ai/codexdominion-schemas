'use client'

export default function MarketContentPanel() {
  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        📢 Marketing Content
      </h2>

      <div className="space-y-3">
        <button className="codex-button w-full text-sm">
          ✨ Generate Promo Content
        </button>
        <button className="codex-button w-full text-sm">
          📊 View Analytics
        </button>
        <button className="codex-button w-full text-sm">
          🔗 Create Tracking Link
        </button>
      </div>

      <div className="mt-6 codex-panel">
        <h3 className="font-semibold text-sm mb-2">Quick Stats</h3>
        <div className="space-y-2 text-xs">
          <div className="flex justify-between">
            <span className="text-codex-parchment/70">Total Revenue</span>
            <span className="font-bold text-codex-gold">$1,582.00</span>
          </div>
          <div className="flex justify-between">
            <span className="text-codex-parchment/70">Active Links</span>
            <span className="font-bold text-green-400">157</span>
          </div>
          <div className="flex justify-between">
            <span className="text-codex-parchment/70">Avg Commission</span>
            <span className="font-bold text-blue-400">12.5%</span>
          </div>
        </div>
      </div>
    </div>
  )
}
