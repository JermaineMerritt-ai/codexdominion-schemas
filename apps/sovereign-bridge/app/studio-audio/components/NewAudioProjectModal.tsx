'use client'

import { useState } from 'react'
import { Modal } from '@/components'

interface NewAudioProjectModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function NewAudioProjectModal({ isOpen, onClose }: NewAudioProjectModalProps) {
  const [projectName, setProjectName] = useState('')
  const [projectType, setProjectType] = useState('podcast')
  const [voiceType, setVoiceType] = useState('single')
  const [duration, setDuration] = useState(60)

  const handleCreate = () => {
    console.log('Creating audio project:', { projectName, projectType, voiceType, duration })
    onClose()
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Create New Audio Project">
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Project Name
          </label>
          <input
            type="text"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            placeholder="Enter project name..."
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
            <option value="podcast">Podcast Episode</option>
            <option value="audiobook">Audiobook</option>
            <option value="meditation">Meditation Audio</option>
            <option value="voiceover">Voiceover</option>
            <option value="music">Music Production</option>
            <option value="soundscape">Soundscape</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Voice Configuration
          </label>
          <select
            value={voiceType}
            onChange={(e) => setVoiceType(e.target.value)}
            className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment"
          >
            <option value="single">Single Voice</option>
            <option value="dual">Dual Voice (Interview)</option>
            <option value="multi">Multi-Voice (Panel)</option>
            <option value="none">No Voice (Music Only)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Target Duration (seconds)
          </label>
          <input
            type="number"
            value={duration}
            onChange={(e) => setDuration(parseInt(e.target.value))}
            min="1"
            max="7200"
            className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment"
          />
        </div>
      </div>

      <div className="flex gap-3 mt-6">
        <button onClick={onClose} className="codex-button flex-1">
          Cancel
        </button>
        <button onClick={handleCreate} className="codex-button flex-1 bg-codex-gold text-codex-navy">
          Create Project
        </button>
      </div>
    </Modal>
  )
}
