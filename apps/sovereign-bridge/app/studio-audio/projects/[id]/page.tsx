'use client'

import Link from 'next/link'
import ScriptEditor from './components/ScriptEditor'
import VoiceSelector from './components/VoiceSelector'
import AudioTimelineEditor from './components/AudioTimelineEditor'
import MusicTrackEditor from './components/MusicTrackEditor'
import RenderHistory from './components/RenderHistory'
import BoundEnginesPanel from './components/BoundEnginesPanel'

export default function AudioProjectDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-serif text-ceremonial mb-2">
            Audio Project Editor
          </h1>
          <p className="text-proclamation">
            Project ID: {params.id}
          </p>
        </div>
        <div className="flex gap-3">
          <button className="codex-button">🎧 Render</button>
          <button className="codex-button">💾 Save</button>
          <button className="codex-button">📤 Export</button>
          <Link href="/studio-audio">
            <button className="codex-button">← Back</button>
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Script & Timeline */}
        <div className="lg:col-span-2 space-y-6">
          <ScriptEditor projectId={params.id} />
          <AudioTimelineEditor projectId={params.id} />
          <MusicTrackEditor projectId={params.id} />
          <RenderHistory projectId={params.id} />
        </div>
        {/* Right Column - Voice & Engines */}
        <div className="space-y-6">
          <VoiceSelector projectId={params.id} />
          <BoundEnginesPanel projectId={params.id} />
        </div>
      </div>
    </div>
  )
}
