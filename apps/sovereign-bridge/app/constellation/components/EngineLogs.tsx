'use client'

import { StatusBadge } from '@/components'

interface LogEntry {
  timestamp: string
  level: 'info' | 'warning' | 'error' | 'success'
  message: string
}

interface EngineLogsProps {
  engineId?: string
}

export default function EngineLogs({ engineId }: EngineLogsProps) {
  const logs: LogEntry[] = [
    { timestamp: '2025-12-12 20:45:32', level: 'info', message: 'Engine initialized successfully' },
    { timestamp: '2025-12-12 20:45:28', level: 'success', message: 'Configuration loaded from disk' },
    { timestamp: '2025-12-12 20:45:25', level: 'info', message: 'Connecting to data sources...' },
    { timestamp: '2025-12-12 20:45:20', level: 'warning', message: 'Retry attempt 2/3 for external API' },
    { timestamp: '2025-12-12 20:45:15', level: 'error', message: 'Connection timeout to cache server' },
    { timestamp: '2025-12-12 20:45:10', level: 'info', message: 'Processing batch job #1247' },
    { timestamp: '2025-12-12 20:45:05', level: 'success', message: 'Health check passed' },
  ]

  const getLevelStatus = (level: string): 'info' | 'warning' | 'error' | 'success' => {
    return level as 'info' | 'warning' | 'error' | 'success'
  }

  return (
    <div className="space-y-2 max-h-96 overflow-y-auto">
      {logs.map((log, idx) => (
        <div key={idx} className="codex-panel hover:bg-codex-navy/90 transition-all flex items-start gap-3">
          <span className="text-xs text-codex-parchment/50 font-mono whitespace-nowrap">
            {log.timestamp}
          </span>
          <StatusBadge status={getLevelStatus(log.level)} size="sm" />
          <span className="text-sm text-codex-parchment flex-1">{log.message}</span>
        </div>
      ))}
    </div>
  )
}
