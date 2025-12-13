'use client'

import { DashboardTile } from '@/components'

interface RepurposingTemplate {
  id: string
  from: string
  to: string
  description: string
}

export default function RepurposingPanel() {
  const templates: RepurposingTemplate[] = [
    { id: '1', from: '🎥', to: '📸 🐦 📌', description: 'YouTube → Clips for IG/Twitter/Pinterest' },
    { id: '2', from: '📝', to: '📸 📌', description: 'Blog Post → Social Graphics' },
    { id: '3', from: '🎙️', to: '🎥 📝', description: 'Podcast → Video + Blog Article' },
    { id: '4', from: '📸', to: '🎵 📌', description: 'Instagram → TikTok + Pinterest' },
  ] as const

  return (
    <DashboardTile title="Content Repurposing" icon="🔄" action={{ label: "⚙️ Configure", onClick: () => {} }}>
      <div className="space-y-3">
        {templates.map((template) => (
          <div key={template.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-2xl">{template.from}</span>
              <span className="text-codex-gold">→</span>
              <span className="text-lg">{template.to}</span>
            </div>
            <div className="text-xs text-codex-parchment/60">{template.description}</div>
          </div>
        ))}
      </div>
      <div className="mt-4 pt-4 border-t border-codex-gold/20">
        <button className="codex-button w-full text-sm">
          ✨ Create Repurposing Rule
        </button>
      </div>
    </DashboardTile>
  )
}
