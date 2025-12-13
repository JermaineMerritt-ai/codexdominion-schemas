'use client'

import { DashboardTile } from '@/components'

interface Collection {
  id: string
  name: string
  productCount: number
  icon: string
}

export default function CollectionBuilder() {
  const collections: Collection[] = [
    { id: '1', name: 'Bible Stories', productCount: 12, icon: '📖' },
    { id: '2', name: 'Wedding Planning', productCount: 8, icon: '💍' },
    { id: '3', name: 'Homeschool', productCount: 15, icon: '🎓' },
    { id: '4', name: 'Seasonal', productCount: 6, icon: '🎄' },
  ]

  return (
    <DashboardTile title="Collections" icon="📚" action={{ label: "+ Create Collection", onClick: () => {} }}>
      <div className="grid grid-cols-2 gap-3">
        {collections.map((collection) => (
          <div
            key={collection.id}
            className="codex-panel hover:bg-codex-gold/10 cursor-pointer text-center"
          >
            <div className="text-3xl mb-2">{collection.icon}</div>
            <div className="text-sm font-medium text-codex-parchment">{collection.name}</div>
            <div className="text-xs text-codex-parchment/60 mt-1">{collection.productCount} products</div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
