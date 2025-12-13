'use client'

export default function FlowList() {
  const flows = [
    { id: '1', name: 'Daily Dawn Dispatch', trigger: 'Schedule: 5:00 AM', status: 'active', runs: 847 },
    { id: '2', name: 'Product Upload Pipeline', trigger: 'Event: New Product', status: 'active', runs: 127 },
    { id: '3', name: 'Treasury Audit', trigger: 'Schedule: Mon 8:00 AM', status: 'active', runs: 52 },
    { id: '4', name: 'Social Media Repurposing', trigger: 'Event: Content Created', status: 'active', runs: 456 },
  ]

  return (
    <div className="codex-card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-serif text-codex-gold">
          Automation Flows
        </h2>
        <button className="codex-button">
          ➕ Create Flow
        </button>
      </div>

      <div className="space-y-4">
        {flows.map((flow) => (
          <div key={flow.id} className="codex-panel hover:bg-codex-gold/10 transition-all cursor-pointer">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="font-semibold">{flow.name}</h3>
                <p className="text-xs text-codex-parchment/60">{flow.trigger}</p>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                <span className="text-xs">{flow.status}</span>
              </div>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-codex-parchment/70">{flow.runs} total runs</span>
              <button className="codex-button text-xs">▶️ Run Now</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
