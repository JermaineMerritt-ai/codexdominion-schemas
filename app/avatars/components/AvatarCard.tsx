'use client'

interface Avatar {
  id: string
  name: string
  type: string
  status: 'active' | 'idle' | 'error'
  interactions: number
}

interface AvatarCardProps {
  avatar: Avatar
}

export default function AvatarCard({ avatar }: AvatarCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500'
      case 'idle': return 'bg-gray-500'
      case 'error': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'support': return '💬'
      case 'sales': return '💼'
      case 'analytics': return '📊'
      case 'workflow': return '⚙️'
      default: return '🤖'
    }
  }

  return (
    <div className="codex-panel hover:bg-codex-gold/10 transition-all">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <span className="text-4xl">{getTypeIcon(avatar.type)}</span>
          <div>
            <h3 className="font-semibold">{avatar.name}</h3>
            <p className="text-xs text-codex-parchment/60 capitalize">{avatar.type}</p>
          </div>
        </div>
        <div className={`w-3 h-3 rounded-full ${getStatusColor(avatar.status)} ${avatar.status === 'active' ? 'animate-pulse' : ''}`}></div>
      </div>

      <div className="flex items-center justify-between">
        <span className="text-sm text-codex-parchment/70">Total Interactions</span>
        <span className="text-xl font-bold text-codex-gold">{avatar.interactions.toLocaleString()}</span>
      </div>

      <div className="mt-4 flex space-x-2">
        <button className="codex-button flex-1 text-sm">View Logs</button>
        <button className="codex-button flex-1 text-sm">Configure</button>
      </div>
    </div>
  )
}
