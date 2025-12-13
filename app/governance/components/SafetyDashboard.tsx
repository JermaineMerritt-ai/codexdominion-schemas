'use client'

export default function SafetyDashboard() {
  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        🛡️ Safety Status
      </h2>

      <div className="space-y-4">
        <div className="codex-panel">
          <div className="text-2xl font-bold text-green-400">100%</div>
          <div className="text-xs text-codex-parchment/60">Compliance Rate</div>
        </div>

        <div className="codex-panel">
          <div className="text-2xl font-bold text-green-400">0</div>
          <div className="text-xs text-codex-parchment/60">Active Incidents</div>
        </div>

        <div className="codex-panel">
          <div className="text-2xl font-bold text-blue-400">847</div>
          <div className="text-xs text-codex-parchment/60">Audits Passed</div>
        </div>

        <div className="codex-panel">
          <div className="text-2xl font-bold text-codex-gold">A+</div>
          <div className="text-xs text-codex-parchment/60">Safety Score</div>
        </div>
      </div>

      <button className="codex-button w-full mt-4 text-sm">
        📋 Run Safety Audit
      </button>
    </div>
  )
}
