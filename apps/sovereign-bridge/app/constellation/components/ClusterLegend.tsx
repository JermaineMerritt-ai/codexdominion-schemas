'use client'

interface ClusterLegendProps {
  clusters?: Array<{ name: string; color: string; count: number }>
}

export default function ClusterLegend({ clusters }: ClusterLegendProps) {
  const defaultClusters = [
    { name: 'Content', color: 'bg-blue-500', count: 2 },
    { name: 'Business', color: 'bg-green-500', count: 2 },
    { name: 'Automation', color: 'bg-purple-500', count: 2 },
    { name: 'Media', color: 'bg-pink-500', count: 2 },
    { name: 'AI', color: 'bg-yellow-500', count: 2 },
    { name: 'Distribution', color: 'bg-orange-500', count: 1 },
    { name: 'Oversight', color: 'bg-red-500', count: 1 },
  ]

  const items = clusters || defaultClusters

  return (
    <div className="flex flex-wrap gap-3">
      {items.map((cluster, idx) => (
        <div
          key={idx}
          className="flex items-center gap-2 codex-panel py-1 px-3 text-sm"
        >
          <div className={`w-3 h-3 rounded-full ${cluster.color}`}></div>
          <span className="text-codex-parchment font-medium">{cluster.name}</span>
          <span className="text-codex-parchment/50">({cluster.count})</span>
        </div>
      ))}
    </div>
  )
}
