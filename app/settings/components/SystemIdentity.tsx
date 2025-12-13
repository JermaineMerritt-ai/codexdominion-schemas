'use client'

export default function SystemIdentity() {
  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        System Identity
      </h2>

      <div className="space-y-4">
        <div className="codex-panel text-center">
          <div className="text-5xl mb-2">🔥</div>
          <h3 className="font-serif text-ceremonial text-lg">Codex Dominion</h3>
          <p className="text-xs text-codex-parchment/60 mt-1">Council Seal Authority</p>
        </div>

        <div className="codex-panel">
          <div className="text-xs space-y-2">
            <div className="flex justify-between">
              <span className="text-codex-parchment/70">Version</span>
              <span className="font-semibold">2.0.0</span>
            </div>
            <div className="flex justify-between">
              <span className="text-codex-parchment/70">Build</span>
              <span className="font-semibold">2025.12.12</span>
            </div>
            <div className="flex justify-between">
              <span className="text-codex-parchment/70">Omega Seal</span>
              <span className="font-semibold text-green-400">Active</span>
            </div>
            <div className="flex justify-between">
              <span className="text-codex-parchment/70">Run Level</span>
              <span className="font-semibold text-codex-gold">5</span>
            </div>
          </div>
        </div>

        <div className="text-center text-xs text-codex-parchment/60 italic">
          "The Flame Burns Sovereign and Eternal"
        </div>
      </div>
    </div>
  )
}
