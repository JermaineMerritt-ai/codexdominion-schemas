'use client'

interface Site {
  id: string
  name: string
  status: 'live' | 'building' | 'offline'
  visitors: number
}

interface SiteCardProps {
  site: Site
}

export default function SiteCard({ site }: SiteCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'live': return 'bg-green-500'
      case 'building': return 'bg-yellow-500 animate-pulse'
      case 'offline': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  return (
    <div className="codex-panel hover:bg-codex-gold/10 transition-all">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-semibold">{site.name}</h3>
          <p className="text-xs text-codex-parchment/60">{site.visitors.toLocaleString()} visitors</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${getStatusColor(site.status)}`}></div>
          <span className="text-xs capitalize">{site.status}</span>
        </div>
      </div>

      <div className="flex space-x-2">
        <button className="codex-button flex-1 text-sm">📊 Analytics</button>
        <button className="codex-button flex-1 text-sm">⚙️ Settings</button>
        <button className="codex-button flex-1 text-sm">🚀 Deploy</button>
      </div>
    </div>
  )
}
