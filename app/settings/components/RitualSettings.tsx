'use client'

export default function RitualSettings() {
  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        Ritual Settings
      </h2>
      <div className="space-y-2">
        <button className="codex-button w-full text-sm">⚙️ Configure Rituals</button>
        <button className="codex-button w-full text-sm">📅 Edit Schedule</button>
      </div>
    </div>
  )
}
