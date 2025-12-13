'use client'

import { StatusBadge } from '@/components'

interface ConfigItem {
  key: string
  value: string
  editable: boolean
  sensitive: boolean
}

interface EngineConfigProps {
  engineId?: string
}

export default function EngineConfig({ engineId }: EngineConfigProps) {
  const configItems: ConfigItem[] = [
    { key: 'engine.name', value: 'Narrative Engine', editable: false, sensitive: false },
    { key: 'engine.version', value: '2.1.0', editable: false, sensitive: false },
    { key: 'engine.environment', value: 'production', editable: false, sensitive: false },
    { key: 'engine.max_workers', value: '8', editable: true, sensitive: false },
    { key: 'engine.timeout_ms', value: '5000', editable: true, sensitive: false },
    { key: 'engine.retry_attempts', value: '3', editable: true, sensitive: false },
    { key: 'api.base_url', value: 'https://api.codexdominion.app', editable: true, sensitive: false },
    { key: 'api.key', value: '••••••••••••••••', editable: false, sensitive: true },
    { key: 'cache.enabled', value: 'true', editable: true, sensitive: false },
    { key: 'cache.ttl_seconds', value: '3600', editable: true, sensitive: false },
  ]

  return (
    <div className="space-y-2">
      {configItems.map((item, idx) => (
        <div
          key={idx}
          className="codex-panel hover:bg-codex-navy/90 transition-all flex items-center justify-between"
        >
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <span className="font-mono text-sm text-codex-gold">{item.key}</span>
              {item.sensitive && (
                <StatusBadge status="warning" label="SENSITIVE" size="sm" />
              )}
            </div>
            <span className="text-xs text-codex-parchment/70 font-mono">{item.value}</span>
          </div>
          {item.editable && (
            <button className="text-xs codex-button py-1 px-3">
              Edit
            </button>
          )}
        </div>
      ))}
    </div>
  )
}
