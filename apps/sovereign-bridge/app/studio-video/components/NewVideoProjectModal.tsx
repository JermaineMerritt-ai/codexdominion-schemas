'use client'

import { Modal } from '@/components'
import { useState } from 'react'

interface NewVideoProjectModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function NewVideoProjectModal({ isOpen, onClose }: NewVideoProjectModalProps) {
  const [projectName, setProjectName] = useState('')
  const [projectType, setProjectType] = useState('promotional')
  const [resolution, setResolution] = useState('1080p')
  const [duration, setDuration] = useState('60')

  const handleCreate = () => {
    // In production, create project via API
    console.log('Creating project:', { projectName, projectType, resolution, duration })
    onClose()
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Create New Video Project"
      size="lg"
      footer={
        <div className="flex gap-3">
          <button onClick={onClose} className="codex-button flex-1">
            Cancel
          </button>
          <button onClick={handleCreate} className="codex-button bg-codex-gold/30 flex-1">
            Create Project
          </button>
        </div>
      }
    >
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Project Name
          </label>
          <input
            type="text"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            placeholder="My Awesome Video"
            className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Project Type
          </label>
          <select
            value={projectType}
            onChange={(e) => setProjectType(e.target.value)}
            className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment"
          >
            <option value="promotional">Promotional Video</option>
            <option value="tutorial">Tutorial/Educational</option>
            <option value="testimonial">Testimonial</option>
            <option value="animation">Animation</option>
            <option value="social">Social Media Clip</option>
            <option value="ad">Advertisement</option>
          </select>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-codex-parchment mb-2">
              Resolution
            </label>
            <select
              value={resolution}
              onChange={(e) => setResolution(e.target.value)}
              className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment"
            >
              <option value="4k">4K (3840x2160)</option>
              <option value="1080p">Full HD (1920x1080)</option>
              <option value="720p">HD (1280x720)</option>
              <option value="480p">SD (854x480)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-codex-parchment mb-2">
              Duration (seconds)
            </label>
            <input
              type="number"
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              min="1"
              max="600"
              className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Template (Optional)
          </label>
          <select className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment">
            <option value="">Blank Project</option>
            <option value="product-showcase">Product Showcase</option>
            <option value="testimonial">Testimonial Template</option>
            <option value="intro-outro">Intro/Outro Template</option>
            <option value="social-stories">Social Stories</option>
          </select>
        </div>
      </div>
    </Modal>
  )
}
