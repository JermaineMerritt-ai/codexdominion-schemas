'use client'

export default function PolicyDashboard() {
  const policies = [
    { name: 'Content Safety Policy', status: 'enforced', lastReview: '2024-12-01', violations: 0 },
    { name: 'Data Privacy Policy', status: 'enforced', lastReview: '2024-11-15', violations: 0 },
    { name: 'AI Usage Guidelines', status: 'enforced', lastReview: '2024-12-10', violations: 0 },
    { name: 'Revenue Compliance', status: 'enforced', lastReview: '2024-11-30', violations: 0 },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-2xl font-serif text-codex-gold mb-6">
        Active Policies
      </h2>

      <div className="space-y-3">
        {policies.map((policy, idx) => (
          <div key={idx} className="codex-panel border-l-2 border-green-500">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="font-semibold text-sm">{policy.name}</h3>
                <p className="text-xs text-codex-parchment/60">Last review: {policy.lastReview}</p>
              </div>
              <span className="codex-badge-success">{policy.status.toUpperCase()}</span>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span className="text-codex-parchment/70">Violations</span>
              <span className="font-bold text-green-400">{policy.violations}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
