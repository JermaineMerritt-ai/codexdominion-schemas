'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface Scene {
  id: string
  name: string
  duration: number
  status: 'draft' | 'active' | 'completed'
}

interface SceneEditorProps {
  projectId: string
}

export default function SceneEditor({ projectId }: SceneEditorProps) {
  const scenes: Scene[] = [
    { id: '1', name: 'Opening Sequence', duration: 5, status: 'completed' },
    { id: '2', name: 'Product Introduction', duration: 10, status: 'active' },
    { id: '3', name: 'Features Highlight', duration: 15, status: 'active' },
    { id: '4', name: 'Customer Testimonial', duration: 8, status: 'draft' },
    { id: '5', name: 'Call to Action', duration: 7, status: 'draft' },
  ]

  return (
    <DashboardTile title="Scene Editor" icon="🎞️" action={{ label: "+ Add Scene", onClick: () => {} }}>
      <div className="space-y-2">
        {scenes.map((scene, idx) => (
          <div key={scene.id} className="codex-panel flex items-center justify-between hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-center gap-3">
              <span className="text-codex-gold font-bold">{idx + 1}</span>
              <div>
                <div className="font-medium text-codex-parchment">{scene.name}</div>
                <div className="text-xs text-codex-parchment/60">{scene.duration}s duration</div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <StatusBadge
                status={scene.status === 'completed' ? 'success' : scene.status === 'active' ? 'active' : 'pending'}
              />
              <button className="text-xs codex-button py-1 px-3">Edit</button>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 pt-4 border-t border-codex-gold/20 flex justify-between text-sm">
        <span className="text-codex-parchment/70">Total Duration:</span>
        <span className="text-codex-gold font-semibold">{scenes.reduce((sum, s) => sum + s.duration, 0)}s</span>
      </div>
    </DashboardTile>
  )
}
