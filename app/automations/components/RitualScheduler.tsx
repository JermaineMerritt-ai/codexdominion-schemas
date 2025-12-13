'use client'

export default function RitualScheduler() {
  const schedules = [
    { time: '05:00 AM', ritual: 'Dawn Dispatch', frequency: 'Daily' },
    { time: '06:00 AM', ritual: 'Signals Daily', frequency: 'Daily' },
    { time: '08:00 AM', ritual: 'Treasury Audit', frequency: 'Monday' },
    { time: '09:00 AM', ritual: 'Sovereignty Bulletin', frequency: 'Daily' },
    { time: '10:00 AM', ritual: 'Education Matrix', frequency: 'Tue/Thu' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        🔮 Ritual Schedule
      </h2>

      <div className="space-y-3">
        {schedules.map((sched, idx) => (
          <div key={idx} className="codex-panel border-l-2 border-codex-gold/50">
            <div className="flex items-center justify-between mb-1">
              <span className="font-semibold text-sm">{sched.time}</span>
              <span className="text-xs text-codex-parchment/60">{sched.frequency}</span>
            </div>
            <p className="text-xs text-codex-parchment/70">{sched.ritual}</p>
          </div>
        ))}
      </div>

      <button className="codex-button w-full mt-4 text-sm">
        ⚙️ Edit Schedule
      </button>
    </div>
  )
}
