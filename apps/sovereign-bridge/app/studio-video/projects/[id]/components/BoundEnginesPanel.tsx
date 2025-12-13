'use client'

import { DashboardTile, StatusList } from '@/components'

interface BoundEnginesPanelProps {
  projectId: string
}

export default function BoundEnginesPanel({ projectId }: BoundEnginesPanelProps) {
  const engines = [
    { label: 'Narrative Engine', status: 'active' as const },
    { label: 'Video Production Engine', status: 'active' as const },
    { label: 'Audio Synthesis Engine', status: 'active' as const },
    { label: 'AI Image Generation', status: 'active' as const },
    { label: 'Render Queue Manager', status: 'active' as const },
    { label: 'Asset Storage Engine', status: 'active' as const },
  ]

  return (
    <DashboardTile title="Bound Engines" icon="🔗">
      <StatusList items={engines} title="" />
      <div className="mt-4 pt-4 border-t border-codex-gold/20">
        <button className="codex-button w-full text-sm">
          ⚙️ Configure Engines
        </button>
      </div>
    </DashboardTile>
  )
}
