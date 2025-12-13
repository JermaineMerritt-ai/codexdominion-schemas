'use client'

import { DashboardTile } from '@/components'

interface MusicTrack {
  id: string
  name: string
  genre: string
  duration: string
  bpm: number
}

export default function MusicTrackLibrary() {
  const tracks: MusicTrack[] = [
    { id: '1', name: 'Peaceful Morning', genre: 'Ambient', duration: '3:45', bpm: 60 },
    { id: '2', name: 'Corporate Uplift', genre: 'Corporate', duration: '2:30', bpm: 120 },
    { id: '3', name: 'Epic Journey', genre: 'Cinematic', duration: '4:20', bpm: 90 },
    { id: '4', name: 'Happy Ukulele', genre: 'Acoustic', duration: '2:15', bpm: 110 },
    { id: '5', name: 'Dark Tension', genre: 'Suspense', duration: '3:00', bpm: 75 },
    { id: '6', name: 'Soft Piano', genre: 'Classical', duration: '5:30', bpm: 70 },
  ]

  return (
    <DashboardTile title="Music Track Library" icon="🎵" action={{ label: "+ Upload Track", onClick: () => {} }}>
      <div className="space-y-2">
        {tracks.map((track) => (
          <div
            key={track.id}
            className="codex-panel hover:bg-codex-gold/10 cursor-pointer flex items-center justify-between"
          >
            <div className="flex items-center gap-3">
              <span className="text-xl">🎶</span>
              <div>
                <div className="text-sm font-medium text-codex-parchment">{track.name}</div>
                <div className="text-xs text-codex-parchment/60">{track.genre} • {track.duration} • {track.bpm} BPM</div>
              </div>
            </div>
            <button className="text-xs codex-button py-1 px-3">Preview</button>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
