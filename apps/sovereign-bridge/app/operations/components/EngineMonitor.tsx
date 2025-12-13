'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface Engine {
  id: string
  name: string
  category: 'core' | 'specialized'
  status: 'active' | 'inactive' | 'pending'
  metrics: {
    requests24h: number
    errorRate: number
    avgLatencyMs: number
  }
  lastHeartbeat: string
}

export default function EngineMonitor() {
  const engines: Engine[] = [
    {
      id: 'rag_retrieval',
      name: 'RAG Retrieval Engine',
      category: 'core',
      status: 'active',
      metrics: { requests24h: 1023, errorRate: 0.01, avgLatencyMs: 150 },
      lastHeartbeat: '2 min ago'
    },
    {
      id: 'narrative_engine',
      name: 'Narrative Generation',
      category: 'specialized',
      status: 'active',
      metrics: { requests24h: 456, errorRate: 0.02, avgLatencyMs: 320 },
      lastHeartbeat: '1 min ago'
    },
    {
      id: 'visual_engine',
      name: 'Visual Prompt Engine',
      category: 'specialized',
      status: 'active',
      metrics: { requests24h: 789, errorRate: 0.0, avgLatencyMs: 210 },
      lastHeartbeat: '3 min ago'
    },
    {
      id: 'audio_engine',
      name: 'Audio Processing',
      category: 'specialized',
      status: 'active',
      metrics: { requests24h: 234, errorRate: 0.01, avgLatencyMs: 180 },
      lastHeartbeat: '1 min ago'
    },
  ] as const

  return (
    <DashboardTile title="AI Engines" icon="🔧" action={{ label: "⚙️ Manage", onClick: () => {} }}>
      <div className="space-y-3">
        {engines.map((engine) => (
          <div key={engine.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-semibold text-sm text-codex-parchment">{engine.name}</h3>
                  <StatusBadge status={engine.status === 'active' ? 'success' : engine.status} />
                </div>
                <p className="text-xs text-codex-parchment/60">
                  {engine.category} • Heartbeat: {engine.lastHeartbeat}
                </p>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-2 text-center text-xs">
              <div>
                <div className="font-bold text-blue-400">{engine.metrics.requests24h}</div>
                <div className="text-codex-parchment/60">Requests/24h</div>
              </div>
              <div>
                <div className="font-bold text-green-400">{(engine.metrics.errorRate * 100).toFixed(1)}%</div>
                <div className="text-codex-parchment/60">Error Rate</div>
              </div>
              <div>
                <div className="font-bold text-purple-400">{engine.metrics.avgLatencyMs}ms</div>
                <div className="text-codex-parchment/60">Avg Latency</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
