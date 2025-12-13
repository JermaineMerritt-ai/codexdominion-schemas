'use client'

export default function RunLevelSelector() {
  const runLevels = [
    { level: 0, name: 'Shutdown', description: 'System halted', color: 'bg-red-500' },
    { level: 1, name: 'Single User', description: 'Maintenance mode', color: 'bg-yellow-500' },
    { level: 2, name: 'Multi User', description: 'No network', color: 'bg-blue-500' },
    { level: 3, name: 'Full Multi User', description: 'With network', color: 'bg-green-500' },
    { level: 5, name: 'Full Operational', description: 'All services', color: 'bg-green-600' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-2xl font-serif text-codex-gold mb-6">
        Run Level Configuration
      </h2>

      <div className="space-y-3">
        {runLevels.map((rl) => (
          <div key={rl.level} className="codex-panel hover:bg-codex-gold/10 transition-all cursor-pointer">
            <div className="flex items-center space-x-4">
              <div className={`w-4 h-4 rounded-full ${rl.color} ${rl.level === 5 ? 'animate-pulse' : ''}`}></div>
              <div className="flex-1">
                <h3 className="font-semibold text-sm">Level {rl.level}: {rl.name}</h3>
                <p className="text-xs text-codex-parchment/60">{rl.description}</p>
              </div>
              {rl.level === 5 && <span className="codex-badge-success">CURRENT</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
