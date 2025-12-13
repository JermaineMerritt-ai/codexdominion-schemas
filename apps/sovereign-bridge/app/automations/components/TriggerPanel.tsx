'use client'

import { DashboardTile } from '@/components'

interface Trigger {
  id: string
  type: 'schedule' | 'event' | 'webhook'
  name: string
  icon: string
}

export default function TriggerPanel() {
  const triggers: Trigger[] = [
    { id: '1', type: 'schedule', name: 'Time-based Schedule', icon: '⏰' },
    { id: '2', type: 'event', name: 'System Event', icon: '⚡' },
    { id: '3', type: 'webhook', name: 'Webhook Trigger', icon: '🔗' },
    { id: '4', type: 'event', name: 'File Upload', icon: '📁' },
    { id: '5', type: 'event', name: 'Database Change', icon: '💾' },
    { id: '6', type: 'schedule', name: 'Cron Expression', icon: '🕐' },
  ] as const

  return (
    <DashboardTile title="Trigger Types" icon="🎯">
      <div className="grid grid-cols-2 gap-3">
        {triggers.map((trigger) => (
          <div
            key={trigger.id}
            className="codex-panel hover:bg-codex-gold/10 cursor-pointer text-center"
          >
            <div className="text-3xl mb-2">{trigger.icon}</div>
            <div className="text-xs text-codex-parchment font-medium">{trigger.name}</div>
          </div>
        ))}
      </div>
      <div className="mt-4 pt-4 border-t border-codex-gold/20">
        <button className="codex-button w-full text-sm">
          ➕ Create Trigger
        </button>
      </div>
    </DashboardTile>
  )
}
