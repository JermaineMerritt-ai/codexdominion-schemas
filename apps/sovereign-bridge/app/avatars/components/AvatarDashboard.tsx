'use client'

export default function AvatarDashboard() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div className="codex-panel">
        <div className="text-2xl font-bold text-codex-gold">4</div>
        <div className="text-xs text-codex-parchment/60">Active Avatars</div>
      </div>
      <div className="codex-panel">
        <div className="text-2xl font-bold text-green-400">5,718</div>
        <div className="text-xs text-codex-parchment/60">Total Interactions</div>
      </div>
      <div className="codex-panel">
        <div className="text-2xl font-bold text-blue-400">97.3%</div>
        <div className="text-xs text-codex-parchment/60">Success Rate</div>
      </div>
      <div className="codex-panel">
        <div className="text-2xl font-bold text-purple-400">1.8s</div>
        <div className="text-xs text-codex-parchment/60">Avg Response</div>
      </div>
    </div>
  )
}
