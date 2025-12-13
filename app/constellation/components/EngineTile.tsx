'use client'

interface Engine {
  id: string
  name: string
  type: string
  status: 'active' | 'idle' | 'error'
  connections: string[]
}

interface EngineTileProps {
  engine: Engine
}

export default function EngineTile({ engine }: EngineTileProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'border-green-500/50 bg-green-500/10'
      case 'idle': return 'border-gray-500/50 bg-gray-500/10'
      case 'error': return 'border-red-500/50 bg-red-500/10'
      default: return 'border-gray-500/50 bg-gray-500/10'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'content': return '📝'
      case 'business': return '💼'
      case 'automation': return '⚙️'
      case 'media': return '🎬'
      case 'ai': return '🤖'
      case 'distribution': return '📡'
      case 'oversight': return '👁️'
      default: return '⭐'
    }
  }

  return (
    <div className={`codex-panel border-2 ${getStatusColor(engine.status)} hover:scale-105 transition-all cursor-pointer`}>
      <div className="flex items-start justify-between mb-3">
        <span className="text-3xl">{getTypeIcon(engine.type)}</span>
        <div className={`w-2 h-2 rounded-full ${engine.status === 'active' ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`}></div>
      </div>
      <h3 className="font-semibold text-sm mb-1">{engine.name}</h3>
      <p className="text-xs text-codex-parchment/60 capitalize mb-2">{engine.type}</p>
      <div className="flex items-center justify-between text-xs">
        <span className="text-codex-parchment/50">{engine.connections.length} links</span>
        <span className={`px-2 py-1 rounded ${getStatusColor(engine.status)}`}>
          {engine.status}
        </span>
      </div>
    </div>
  )
}
