'use client'

import { useState } from 'react'
import { DashboardTile } from '@/components'

interface ScriptEditorProps {
  projectId: string
}

export default function ScriptEditor({ projectId }: ScriptEditorProps) {
  const [script, setScript] = useState(`SCENE 1: INTRODUCTION
[Upbeat music fades in]

Welcome to our amazing product showcase! Today we're excited to show you...

SCENE 2: PRODUCT DEMO
[Cut to product display]

Let me show you the incredible features...

SCENE 3: CALL TO ACTION
[Music swells]

Ready to get started? Visit our website today!`)

  return (
    <DashboardTile title="Script Editor" icon="📝" action={{ label: "Save", onClick: () => {} }}>
      <textarea
        value={script}
        onChange={(e) => setScript(e.target.value)}
        className="w-full h-96 px-4 py-3 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment font-mono text-sm resize-none"
        placeholder="Write your video script here..."
      />
      <div className="mt-3 flex justify-between text-xs text-codex-parchment/60">
        <span>{script.split('\n').length} lines</span>
        <span>{script.split(/\s+/).length} words</span>
        <span>~{Math.ceil(script.split(/\s+/).length / 150)} min read time</span>
      </div>
    </DashboardTile>
  )
}
