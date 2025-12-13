'use client'

import { useState } from 'react'
import { DashboardTile, StatusBadge } from '@/components'

interface Voice {
  id: string
  name: string
  type: string
  preview: string
}

interface VoiceSelectorProps {
  projectId: string
}

export default function VoiceSelector({ projectId }: VoiceSelectorProps) {
  const [selectedVoice, setSelectedVoice] = useState('1')

  const voices: Voice[] = [
    { id: '1', name: 'Sarah', type: 'Female - Professional', preview: 'Clear and authoritative' },
    { id: '2', name: 'James', type: 'Male - Narrator', preview: 'Deep and engaging' },
    { id: '3', name: 'Maria', type: 'Female - Conversational', preview: 'Warm and friendly' },
    { id: '4', name: 'Chen', type: 'Male - Calm', preview: 'Soothing and peaceful' },
  ]

  return (
    <DashboardTile title="Voice Selection" icon="🎙️">
      <div className="space-y-2">
        {voices.map((voice) => (
          <div
            key={voice.id}
            onClick={() => setSelectedVoice(voice.id)}
            className={`codex-panel cursor-pointer flex items-center justify-between ${
              selectedVoice === voice.id ? 'ring-2 ring-codex-gold' : ''
            } hover:bg-codex-gold/10`}
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl">🎤</span>
              <div>
                <div className="text-sm font-medium text-codex-parchment">{voice.name}</div>
                <div className="text-xs text-codex-parchment/60">{voice.type}</div>
                <div className="text-xs text-codex-parchment/40 italic">{voice.preview}</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {selectedVoice === voice.id && <StatusBadge status="active" />}
              <button className="text-xs codex-button py-1 px-3">▶ Preview</button>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
