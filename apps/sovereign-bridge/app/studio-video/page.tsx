'use client'

import { useState } from 'react'
import { DashboardTile, Modal } from '@/components'
import VideoProjectCard from './components/VideoProjectCard'
import RenderQueue from './components/RenderQueue'
import AssetLibrary from './components/AssetLibrary'
import NewVideoProjectModal from './components/NewVideoProjectModal'

export default function StudioVideoPage() {
  const [showNewProjectModal, setShowNewProjectModal] = useState(false)

  const projects = [
    { id: '1', name: 'Advent Promo Video', status: 'rendering', progress: 67 },
    { id: '2', name: 'Kids Bible Story Animation', status: 'draft', progress: 0 },
    { id: '3', name: 'Wedding Testimonial', status: 'completed', progress: 100 },
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          🎬 Video Production Studio
        </h1>
        <p className="text-proclamation">
          AI-Powered Video Creation, Rendering & Asset Management
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <DashboardTile
            title="Video Projects"
            icon="🎬"
            action={{ label: "➕ New Project", onClick: () => setShowNewProjectModal(true) }}
          >
            <div className="space-y-4">
              {projects.map((project) => (
                <VideoProjectCard key={project.id} project={project} />
              ))}
            </div>
          </DashboardTile>

          <AssetLibrary />
        </div>

        <div>
          <RenderQueue />
        </div>
      </div>

      <NewVideoProjectModal
        isOpen={showNewProjectModal}
        onClose={() => setShowNewProjectModal(false)}
      />
    </div>
  )
}
