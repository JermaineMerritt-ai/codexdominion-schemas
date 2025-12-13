'use client'

import Link from 'next/link'
import ScriptEditor from './components/ScriptEditor'
import SceneEditor from './components/SceneEditor'
import VisualPromptPanel from './components/VisualPromptPanel'
import AssetPanel from './components/AssetPanel'
import RenderHistory from './components/RenderHistory'
import BoundEnginesPanel from './components/BoundEnginesPanel'

export default function VideoProjectDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-serif text-ceremonial mb-2">
            Video Project Editor
          </h1>
          <p className="text-proclamation">
            Project ID: {params.id}
          </p>
        </div>
        <div className="flex gap-3">
          <button className="codex-button">🎬 Render</button>
          <button className="codex-button">💾 Save</button>
          <button className="codex-button">📤 Export</button>
          <Link href="/studio-video">
            <button className="codex-button">← Back</button>
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Script & Scenes */}
        <div className="lg:col-span-2 space-y-6">
          <ScriptEditor projectId={params.id} />
          <SceneEditor projectId={params.id} />
          <VisualPromptPanel projectId={params.id} />
          <RenderHistory projectId={params.id} />
        </div>

        {/* Right Column - Assets & Engines */}
        <div className="space-y-6">
          <AssetPanel projectId={params.id} />
          <BoundEnginesPanel projectId={params.id} />
        </div>
      </div>
    </div>
  )
}
