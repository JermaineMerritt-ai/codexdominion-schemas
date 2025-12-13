'use client'

import { useState } from 'react'
import { DashboardTile, InlineMetric } from '@/components'
import EngineTile from './EngineTile'
import ClusterLegend from './ClusterLegend'

interface Engine {
  id: string
  name: string
  type: string
  status: 'active' | 'idle' | 'error'
  connections: string[]
}

export default function ConstellationMap() {
  const [engines] = useState<Engine[]>([
    { id: 'narrative', name: 'Narrative Engine', type: 'content', status: 'active', connections: ['education', 'commerce'] },
    { id: 'education', name: 'Education Engine', type: 'content', status: 'active', connections: ['narrative', 'knowledge'] },
    { id: 'commerce', name: 'Commerce Engine', type: 'business', status: 'active', connections: ['narrative', 'affiliate'] },
    { id: 'orchestration', name: 'Orchestration Engine', type: 'automation', status: 'active', connections: ['automation', 'governance'] },
    { id: 'automation', name: 'Automation Engine', type: 'automation', status: 'active', connections: ['orchestration', 'social'] },
    { id: 'video', name: 'Video Production', type: 'media', status: 'active', connections: ['audio', 'social'] },
    { id: 'audio', name: 'Audio Production', type: 'media', status: 'active', connections: ['video', 'social'] },
    { id: 'knowledge', name: 'Knowledge RAG', type: 'ai', status: 'active', connections: ['education', 'avatars'] },
    { id: 'avatars', name: 'Avatar System', type: 'ai', status: 'active', connections: ['knowledge', 'social'] },
    { id: 'social', name: 'Social Networks', type: 'distribution', status: 'active', connections: ['video', 'audio', 'affiliate'] },
    { id: 'affiliate', name: 'Affiliate Networks', type: 'business', status: 'active', connections: ['commerce', 'social'] },
    { id: 'governance', name: 'Governance Layer', type: 'oversight', status: 'active', connections: ['orchestration'] },
  ])

  return (
    <DashboardTile title="System Constellation Map" icon="⭐">
      <div className="relative">
        {/* Cluster Legend */}
        <div className="mb-6">
          <ClusterLegend />
        </div>

        {/* Constellation Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {engines.map((engine) => (
            <EngineTile key={engine.id} engine={engine} />
          ))}
        </div>

        {/* Connection Stats */}
        <div className="mt-8 pt-6 border-t border-codex-gold/20 flex flex-wrap gap-4">
          <InlineMetric label="Total Engines" value={engines.length.toString()} icon="🏛️" />
          <InlineMetric label="Active" value={engines.filter(e => e.status === 'active').length.toString()} icon="✅" />
          <InlineMetric label="Connections" value={engines.reduce((sum, e) => sum + e.connections.length, 0).toString()} icon="🔗" />
          <InlineMetric label="Categories" value={new Set(engines.map(e => e.type)).size.toString()} icon="📁" />
        </div>
      </div>
    </DashboardTile>
  )
}
