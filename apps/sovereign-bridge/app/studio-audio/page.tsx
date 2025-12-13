'use client'

import { useState } from 'react'
import { DashboardTile } from '@/components'
import AudioProjectCard from './components/AudioProjectCard'
import AudioRenderQueue from './components/AudioRenderQueue'
import VoiceLibrary from './components/VoiceLibrary'
import MusicTrackLibrary from './components/MusicTrackLibrary'
import NewAudioProjectModal from './components/NewAudioProjectModal'

export default function StudioAudioPage() {
  const [showNewProjectModal, setShowNewProjectModal] = useState(false)

  const projects = [
    { id: '1', name: 'Advent Meditation Music', status: 'rendering', progress: 43 },
    { id: '2', name: 'Podcast Episode 12', status: 'draft', progress: 0 },
    { id: '3', name: 'Christmas Hymn Remix', status: 'completed', progress: 100 },
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          🎵 Audio Production Studio
        </h1>
        <p className="text-proclamation">
          AI Voice Generation, Music Production & Audio Rendering
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <DashboardTile
            title="Audio Projects"
            icon="🎧"
            action={{ label: "➕ New Project", onClick: () => setShowNewProjectModal(true) }}
          >
            <div className="space-y-4">
              {projects.map((project) => (
                <AudioProjectCard key={project.id} project={project} />
              ))}
            </div>
          </DashboardTile>

          <MusicTrackLibrary />
        </div>

        <div className="space-y-6">
          <AudioRenderQueue />
          <VoiceLibrary />
        </div>
      </div>

      <NewAudioProjectModal
        isOpen={showNewProjectModal}
        onClose={() => setShowNewProjectModal(false)}
      />
    </div>
  )
}
