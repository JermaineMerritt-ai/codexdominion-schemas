'use client'

import { DashboardTile } from '@/components'

interface Asset {
  id: string
  name: string
  type: 'image' | 'audio' | 'video'
  size: string
}

export default function AssetLibrary() {
  const assets: Asset[] = [
    { id: '1', name: 'Logo.png', type: 'image', size: '245 KB' },
    { id: '2', name: 'Background Music.mp3', type: 'audio', size: '3.2 MB' },
    { id: '3', name: 'Intro Clip.mp4', type: 'video', size: '12.5 MB' },
    { id: '4', name: 'Product Shot.jpg', type: 'image', size: '1.8 MB' },
    { id: '5', name: 'Voiceover.wav', type: 'audio', size: '5.6 MB' },
    { id: '6', name: 'B-Roll.mp4', type: 'video', size: '25.3 MB' },
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
    <DashboardTile title="Asset Library" icon="📚" action={{ label: "+ Upload", onClick: () => {} }}>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {assets.map((asset) => (
          <div
            key={asset.id}
            className="codex-panel hover:bg-codex-gold/10 cursor-pointer transition-all aspect-square flex flex-col items-center justify-center"
          >
            <span className="text-4xl mb-2">{getAssetIcon(asset.type)}</span>
            <span className="text-xs text-center text-codex-parchment">{asset.name}</span>
            <span className="text-xs text-codex-parchment/50">{asset.size}</span>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
