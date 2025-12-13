'use client'

import { useState } from 'react'
import { DashboardTile } from '@/components'

interface MusicTrack {
  id: string
  name: string
  volume: number
  fadeIn: number
  fadeOut: number
}

interface MusicTrackEditorProps {
  projectId: string
}

export default function MusicTrackEditor({ projectId }: MusicTrackEditorProps) {
  const [tracks, setTracks] = useState<MusicTrack[]>([
    { id: '1', name: 'Background Music.mp3', volume: 70, fadeIn: 2, fadeOut: 3 },
    { id: '2', name: 'Intro Jingle.mp3', volume: 100, fadeIn: 0, fadeOut: 1 },
  ])

  const updateTrack = (id: string, field: keyof MusicTrack, value: number) => {
    setTracks(tracks.map(t => t.id === id ? { ...t, [field]: value } : t))
  }

  return (
    <DashboardTile title="Music Tracks" icon="🎶" action={{ label: "+ Add Track", onClick: () => {} }}>
      <div className="space-y-4">
        {tracks.map((track) => (
          <div key={track.id} className="codex-panel">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className="text-xl">🎵</span>
                <span className="text-sm font-medium text-codex-parchment">{track.name}</span>
              </div>
              <button className="text-xs codex-button py-1 px-3">Remove</button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-xs text-codex-parchment/70 mb-1">
                  Volume: {track.volume}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={track.volume}
                  onChange={(e) => updateTrack(track.id, 'volume', parseInt(e.target.value))}
                  className="w-full"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-codex-parchment/70 mb-1">
                    Fade In: {track.fadeIn}s
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="10"
                    value={track.fadeIn}
                    onChange={(e) => updateTrack(track.id, 'fadeIn', parseInt(e.target.value))}
                    className="w-full px-2 py-1 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment text-xs"
                  />
                </div>
                <div>
                  <label className="block text-xs text-codex-parchment/70 mb-1">
                    Fade Out: {track.fadeOut}s
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="10"
                    value={track.fadeOut}
                    onChange={(e) => updateTrack(track.id, 'fadeOut', parseInt(e.target.value))}
                    className="w-full px-2 py-1 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment text-xs"
                  />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
