'use client'

import { DashboardTile } from '@/components'

interface RitualSchedule {
  id: string
  time: string
  ritual: string
  frequency: string
}

export default function RitualScheduler() {
  const schedules: RitualSchedule[] = [
    { id: '1', time: '05:00 AM', ritual: 'Dawn Dispatch', frequency: 'Daily' },
    { id: '2', time: '06:00 AM', ritual: 'Signals Daily', frequency: 'Daily' },
    { id: '3', time: '08:00 AM', ritual: 'Treasury Audit', frequency: 'Monday' },
    { id: '4', time: '09:00 AM', ritual: 'Sovereignty Bulletin', frequency: 'Daily' },
    { id: '5', time: '10:00 AM', ritual: 'Education Matrix', frequency: 'Tue/Thu' },
  ] as const

  return (
    <DashboardTile title="Ritual Schedule" icon="🔮" action={{ label: "⚙️ Edit", onClick: () => {} }}>
      <div className="space-y-3">
        {schedules.map((sched) => (
          <div key={sched.id} className="codex-panel border-l-2 border-codex-gold/50 hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-center justify-between mb-1">
              <span className="font-semibold text-sm text-codex-parchment">{sched.time}</span>
              <span className="text-xs text-codex-parchment/60">{sched.frequency}</span>
            </div>
            <p className="text-xs text-codex-parchment/70">{sched.ritual}</p>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
