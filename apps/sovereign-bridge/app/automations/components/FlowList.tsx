'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface AutomationFlow {
  id: string
  name: string
  trigger: string
  status: 'active' | 'inactive' | 'pending'
  runs: number
}

export default function FlowList() {
  const flows: AutomationFlow[] = [
    { id: '1', name: 'Daily Dawn Dispatch', trigger: 'Schedule: 5:00 AM', status: 'active', runs: 847 },
    { id: '2', name: 'Product Upload Pipeline', trigger: 'Event: New Product', status: 'active', runs: 127 },
    { id: '3', name: 'Treasury Audit', trigger: 'Schedule: Mon 8:00 AM', status: 'active', runs: 52 },
    { id: '4', name: 'Social Media Repurposing', trigger: 'Event: Content Created', status: 'active', runs: 456 },
    { id: '5', name: 'Backup System', trigger: 'Schedule: Daily 11:00 PM', status: 'pending', runs: 0 },
  ] as const

  return (
    <DashboardTile title="Automation Flows" icon="⚡" action={{ label: "+ Create Flow", onClick: () => {} }}>
      <div className="space-y-3">
        {flows.map((flow) => (
          <div key={flow.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-start justify-between mb-2">
              <div className="flex-1">
                <h3 className="font-semibold text-codex-parchment">{flow.name}</h3>
                <p className="text-xs text-codex-parchment/60 mt-1">{flow.trigger}</p>
              </div>
              <StatusBadge status={flow.status === 'active' ? 'success' : flow.status} />
            </div>
            <div className="flex items-center justify-between text-sm mt-3">
              <span className="text-codex-parchment/70">{flow.runs} total runs</span>
              <button className="codex-button text-xs">▶️ Run Now</button>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
