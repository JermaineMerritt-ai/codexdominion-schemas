'use client'

export default function AuditLog() {
  const logs = [
    { timestamp: 'Today 10:32 AM', action: 'Policy Review', user: 'System', result: 'Passed' },
    { timestamp: 'Today 9:15 AM', action: 'Data Access', user: 'Admin', result: 'Approved' },
    { timestamp: 'Yesterday 4:45 PM', action: 'Configuration Change', user: 'System', result: 'Applied' },
    { timestamp: 'Yesterday 2:30 PM', action: 'Security Scan', user: 'System', result: 'Clear' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-2xl font-serif text-codex-gold mb-6">
        Recent Audit Log
      </h2>

      <div className="space-y-2">
        {logs.map((log, idx) => (
          <div key={idx} className="codex-panel text-xs">
            <div className="flex items-start justify-between mb-1">
              <span className="font-semibold">{log.action}</span>
              <span className="codex-badge-success">{log.result}</span>
            </div>
            <div className="flex justify-between text-codex-parchment/60">
              <span>{log.user}</span>
              <span>{log.timestamp}</span>
            </div>
          </div>
        ))}
      </div>

      <button className="codex-button w-full mt-4 text-sm">
        📜 View Full Log
      </button>
    </div>
  )
}
