'use client'

import { useState } from 'react'
import { DashboardTile } from '@/components'
import EngineMetrics from './EngineMetrics'
import EngineTasks from './EngineTasks'
import EngineLogs from './EngineLogs'
import EngineConfig from './EngineConfig'
import EngineHistory from './EngineHistory'

type TabType = 'metrics' | 'tasks' | 'logs' | 'config' | 'history'

export default function EngineDashboard() {
  const [activeTab, setActiveTab] = useState<TabType>('metrics')
  const [selectedEngine] = useState('narrative')

  const tabs = [
    { id: 'metrics' as TabType, label: 'Metrics', icon: '📊' },
    { id: 'tasks' as TabType, label: 'Tasks', icon: '✓' },
    { id: 'logs' as TabType, label: 'Logs', icon: '📝' },
    { id: 'config' as TabType, label: 'Config', icon: '⚙️' },
    { id: 'history' as TabType, label: 'History', icon: '📈' },
  ]

  return (
    <DashboardTile title="Engine Dashboard" icon="🎛️">
      {/* Engine Selector */}
      <div className="mb-6 flex items-center gap-3">
        <span className="text-sm text-codex-parchment/70">Selected Engine:</span>
        <select className="bg-codex-navy/50 border border-codex-gold/30 rounded px-3 py-2 text-codex-parchment">
          <option value="narrative">Narrative Engine</option>
          <option value="education">Education Engine</option>
          <option value="commerce">Commerce Engine</option>
          <option value="orchestration">Orchestration Engine</option>
          <option value="automation">Automation Engine</option>
          <option value="video">Video Production</option>
          <option value="audio">Audio Production</option>
          <option value="knowledge">Knowledge RAG</option>
          <option value="avatars">Avatar System</option>
          <option value="social">Social Networks</option>
          <option value="affiliate">Affiliate Networks</option>
          <option value="governance">Governance Layer</option>
        </select>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-codex-gold/20 mb-6">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 flex items-center gap-2 transition-all ${
              activeTab === tab.id
                ? 'border-b-2 border-codex-gold text-codex-gold'
                : 'text-codex-parchment/60 hover:text-codex-parchment'
            }`}
          >
            <span>{tab.icon}</span>
            <span className="text-sm font-medium">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="min-h-[400px]">
        {activeTab === 'metrics' && <EngineMetrics engineId={selectedEngine} />}
        {activeTab === 'tasks' && <EngineTasks engineId={selectedEngine} />}
        {activeTab === 'logs' && <EngineLogs engineId={selectedEngine} />}
        {activeTab === 'config' && <EngineConfig engineId={selectedEngine} />}
        {activeTab === 'history' && <EngineHistory engineId={selectedEngine} />}
      </div>
    </DashboardTile>
  )
}
