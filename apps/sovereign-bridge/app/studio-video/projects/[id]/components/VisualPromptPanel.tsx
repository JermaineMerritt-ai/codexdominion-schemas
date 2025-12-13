'use client'

import { useState } from 'react'
import { DashboardTile } from '@/components'

interface VisualPromptPanelProps {
  projectId: string
}

export default function VisualPromptPanel({ projectId }: VisualPromptPanelProps) {
  const [prompt, setPrompt] = useState('')
  const [style, setStyle] = useState('realistic')
  const [generatedImages, setGeneratedImages] = useState<string[]>([])

  const handleGenerate = () => {
    // In production, call AI image generation API
    console.log('Generating images with prompt:', prompt, 'style:', style)
  }

  return (
    <DashboardTile title="Visual Prompt Panel" icon="🎨">
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-codex-parchment mb-2">
            Visual Description
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe the visual scene you want to generate... e.g., 'A modern office space with natural lighting, minimalist design, professional atmosphere'"
            className="w-full h-24 px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment text-sm resize-none"
          />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-codex-parchment mb-2">
              Style
            </label>
            <select
              value={style}
              onChange={(e) => setStyle(e.target.value)}
              className="w-full px-3 py-2 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment text-sm"
            >
              <option value="realistic">Realistic</option>
              <option value="illustration">Illustration</option>
              <option value="anime">Anime</option>
              <option value="3d">3D Render</option>
              <option value="watercolor">Watercolor</option>
              <option value="sketch">Sketch</option>
            </select>
          </div>

          <div className="flex items-end">
            <button onClick={handleGenerate} className="codex-button w-full">
              ✨ Generate Images
            </button>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-2 min-h-[200px]">
          {generatedImages.length === 0 ? (
            <div className="col-span-3 flex items-center justify-center text-codex-parchment/40 text-sm">
              Generated images will appear here
            </div>
          ) : (
            generatedImages.map((img, idx) => (
              <div key={idx} className="aspect-square codex-panel bg-codex-navy/50"></div>
            ))
          )}
        </div>
      </div>
    </DashboardTile>
  )
}
