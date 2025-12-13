'use client'

export default function IncidentPanel() {
  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        🚨 Incident Response
      </h2>
      <div className="text-center py-8">
        <div className="text-4xl mb-2">✅</div>
        <p className="text-sm text-codex-parchment/70">No active incidents</p>
      </div>
    </div>
  )
}
