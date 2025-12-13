'use client'

import { useEffect, useState } from 'react'

interface Ritual {
  name: string
  schedule: string
  lastRun: string
  nextRun: string
  status: 'active' | 'disabled' | 'error'
}

export default function RitualsPanel() {
  const [rituals, setRituals] = useState<Ritual[]>([])

  useEffect(() => {
    const mockRituals: Ritual[] = [
      { name: 'Dawn Dispatch', schedule: 'Daily 5:00 AM', lastRun: 'Today 5:00 AM', nextRun: 'Tomorrow 5:00 AM', status: 'active' },
      { name: 'Signals Daily', schedule: 'Daily 6:00 AM', lastRun: 'Today 6:00 AM', nextRun: 'Tomorrow 6:00 AM', status: 'active' },
      { name: 'Treasury Audit', schedule: 'Mon 8:00 AM', lastRun: 'Dec 9, 8:00 AM', nextRun: 'Dec 16, 8:00 AM', status: 'active' },
      { name: 'Sovereignty Bulletin', schedule: 'Daily 9:00 AM', lastRun: 'Today 9:00 AM', nextRun: 'Tomorrow 9:00 AM', status: 'active' },
      { name: 'Education Matrix', schedule: 'Tue/Thu 10:00 AM', lastRun: 'Dec 10, 10:00 AM', nextRun: 'Dec 12, 10:00 AM', status: 'active' },
    ]
    setRituals(mockRituals)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400'
      case 'disabled': return 'text-gray-400'
      case 'error': return 'text-red-400'
      default: return 'text-gray-400'
    }
  }

  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        🔮 Active Rituals
      </h2>

      <div className="space-y-3">
        {rituals.map((ritual, idx) => (
          <div key={idx} className="codex-panel border-l-2 border-codex-gold/50">
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-semibold text-sm">{ritual.name}</h3>
              <div className={`w-2 h-2 rounded-full ${ritual.status === 'active' ? 'bg-green-500' : 'bg-gray-500'}`}></div>
            </div>
            <p className="text-xs text-codex-parchment/60 mb-1">{ritual.schedule}</p>
            <div className="flex justify-between text-xs text-codex-parchment/50">
              <span>Last: {ritual.lastRun}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-codex-gold/20">
        <button className="codex-button w-full text-sm">
          ⚙️ Manage Rituals
        </button>
      </div>
    </div>
  )
}
