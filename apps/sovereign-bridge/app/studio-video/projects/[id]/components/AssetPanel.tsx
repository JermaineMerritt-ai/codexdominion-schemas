'use client'

import { DashboardTile } from '@/components'

interface Asset {
  id: string
  name: string
  type: 'image' | 'audio' | 'video'
  usedInScenes: number[]
}

interface AssetPanelProps {
  projectId: string
}

export default function AssetPanel({ projectId }: AssetPanelProps) {
  const assets: Asset[] = [
    { id: '1', name: 'Logo.png', type: 'image', usedInScenes: [1, 5] },
    { id: '2', name: 'Background.mp3', type: 'audio', usedInScenes: [1, 2, 3, 4, 5] },
    { id: '3', name: 'Product Demo.mp4', type: 'video', usedInScenes: [2] },
    { id: '4', name: 'Testimonial.mp4', type: 'video', usedInScenes: [4] },
  ]

  const getAssetIcon = (type: string) => {
    switch (type) {
      case 'image': return '🖼️'
      case 'audio': return '🎵'
      case 'video': return '🎬'
      default: return '📁'
    }
  }

  return (
    <DashboardTile title="Project Assets" icon="📦" action={{ label: "+ Add Asset", onClick: () => {} }}>
      <div className="space-y-2">
        {assets.map((asset) => (
          <div key={asset.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-2xl">{getAssetIcon(asset.type)}</span>
              <div>
                <div className="text-sm font-medium text-codex-parchment">{asset.name}</div>
                <div className="text-xs text-codex-parchment/60">
                  Used in {asset.usedInScenes.length} scene{asset.usedInScenes.length !== 1 ? 's' : ''}
                </div>
              </div>
            </div>
            <button className="text-xs codex-button py-1 px-3">Manage</button>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
