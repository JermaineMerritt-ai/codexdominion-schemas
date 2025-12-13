'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface AuditEntry {
  id: string
  timestamp: string
  action: string
  user: string
  result: 'success' | 'pending' | 'active'
}

export default function AuditLog() {
  const logs: AuditEntry[] = [
    { id: '1', timestamp: 'Today 10:32 AM', action: 'Policy Review', user: 'System', result: 'success' },
    { id: '2', timestamp: 'Today 9:15 AM', action: 'Data Access', user: 'Admin', result: 'success' },
    { id: '3', timestamp: 'Yesterday 4:45 PM', action: 'Configuration Change', user: 'System', result: 'success' },
    { id: '4', timestamp: 'Yesterday 2:30 PM', action: 'Security Scan', user: 'System', result: 'success' },
    { id: '5', timestamp: 'Yesterday 1:15 PM', action: 'Backup Verification', user: 'System', result: 'success' },
  ] as const

  return (
    <DashboardTile title="Recent Audit Log" icon="📜" action={{ label: "📜 Full Log", onClick: () => {} }}>
      <div className="space-y-2">
        {logs.map((log) => (
          <div key={log.id} className="codex-panel text-xs hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-start justify-between mb-2">
              <span className="font-semibold text-codex-parchment">{log.action}</span>
              <StatusBadge status={log.result} />
            </div>
            <div className="flex justify-between text-codex-parchment/60">
              <span>{log.user}</span>
              <span>{log.timestamp}</span>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
