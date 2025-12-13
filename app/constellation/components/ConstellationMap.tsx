'use client'

import { useState } from 'react'
import EngineTile from './EngineTile'

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
    <div className="codex-card">
      <h2 className="text-2xl font-serif text-codex-gold mb-6">
        System Constellation Map
      </h2>

      <div className="relative">
        {/* Constellation Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {engines.map((engine) => (
            <EngineTile key={engine.id} engine={engine} />
          ))}
        </div>

        {/* Connection Stats */}
        <div className="mt-8 pt-6 border-t border-codex-gold/20 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-codex-gold">{engines.length}</div>
            <div className="text-xs text-codex-parchment/60">Total Engines</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-400">{engines.filter(e => e.status === 'active').length}</div>
            <div className="text-xs text-codex-parchment/60">Active</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-400">
              {engines.reduce((sum, e) => sum + e.connections.length, 0)}
            </div>
            <div className="text-xs text-codex-parchment/60">Connections</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-400">
              {new Set(engines.map(e => e.type)).size}
            </div>
            <div className="text-xs text-codex-parchment/60">Categories</div>
          </div>
        </div>
      </div>
    </div>
  )
}
