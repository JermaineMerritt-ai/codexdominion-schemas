'use client'

import { DashboardTile } from '@/components'

interface FlowStep {
  id: string
  type: 'trigger' | 'action' | 'condition'
  name: string
  icon: string
}

export default function FlowEditor() {
  const steps: FlowStep[] = [
    { id: '1', type: 'trigger', name: 'Schedule Trigger', icon: '⏰' },
    { id: '2', type: 'condition', name: 'Check Conditions', icon: '❓' },
    { id: '3', type: 'action', name: 'Execute Task', icon: '⚡' },
    { id: '4', type: 'action', name: 'Send Notification', icon: '🔔' },
  ] as const

  return (
    <DashboardTile title="Flow Editor" icon="🛠️" action={{ label: "💾 Save", onClick: () => {} }}>
      <div className="space-y-3">
        {steps.map((step, index) => (
          <div key={step.id}>
            <div className="codex-panel hover:bg-codex-gold/10 cursor-pointer">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{step.icon}</span>
                <div className="flex-1">
                  <div className="text-sm font-medium text-codex-parchment">{step.name}</div>
                  <div className="text-xs text-codex-parchment/50 capitalize">{step.type}</div>
                </div>
                <button className="text-codex-parchment/50 hover:text-codex-gold">✏️</button>
              </div>
            </div>
            {index < steps.length - 1 && (
              <div className="flex justify-center py-2">
                <span className="text-codex-gold text-xl">↓</span>
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="mt-4 pt-4 border-t border-codex-gold/20">
        <button className="codex-button w-full text-sm">
          ➕ Add Step
        </button>
      </div>
    </DashboardTile>
  )
}
