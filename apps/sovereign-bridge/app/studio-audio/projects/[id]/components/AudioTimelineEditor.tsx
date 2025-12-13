'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface TimelineSegment {
  id: string
  name: string
  type: 'voice' | 'music' | 'silence'
  startTime: number
  duration: number
}

interface AudioTimelineEditorProps {
  projectId: string
}

export default function AudioTimelineEditor({ projectId }: AudioTimelineEditorProps) {
  const segments: TimelineSegment[] = [
    { id: '1', name: 'Intro Voice', type: 'voice', startTime: 0, duration: 15 },
    { id: '2', name: 'Background Music', type: 'music', startTime: 5, duration: 120 },
    { id: '3', name: 'Main Content', type: 'voice', startTime: 15, duration: 180 },
    { id: '4', name: 'Music Break', type: 'music', startTime: 195, duration: 10 },
    { id: '5', name: 'Outro Voice', type: 'voice', startTime: 205, duration: 10 },
  ]

  const getSegmentIcon = (type: string) => {
    switch (type) {
      case 'voice': return '🎤'
      case 'music': return '🎵'
      case 'silence': return '🔇'
      default: return '📊'
    }
  }

  const getSegmentColor = (type: string) => {
    switch (type) {
      case 'voice': return 'bg-blue-500/20 border-blue-500/50'
      case 'music': return 'bg-purple-500/20 border-purple-500/50'
      case 'silence': return 'bg-gray-500/20 border-gray-500/50'
      default: return 'bg-codex-gold/20 border-codex-gold/50'
    }
  }

  return (
    <DashboardTile title="Audio Timeline" icon="📊" action={{ label: "+ Add Segment", onClick: () => {} }}>
      <div className="space-y-2">
        {segments.map((segment) => (
          <div key={segment.id} className={`p-3 rounded border ${getSegmentColor(segment.type)}`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-xl">{getSegmentIcon(segment.type)}</span>
                <div>
                  <div className="text-sm font-medium text-codex-parchment">{segment.name}</div>
                  <div className="text-xs text-codex-parchment/60">
                    {segment.startTime}s - {segment.startTime + segment.duration}s ({segment.duration}s)
                  </div>
                </div>
              </div>
              <button className="text-xs codex-button py-1 px-3">Edit</button>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 pt-4 border-t border-codex-gold/20 text-sm text-codex-parchment/70">
        Total Duration: {Math.max(...segments.map(s => s.startTime + s.duration))}s
      </div>
    </DashboardTile>
  )
}
