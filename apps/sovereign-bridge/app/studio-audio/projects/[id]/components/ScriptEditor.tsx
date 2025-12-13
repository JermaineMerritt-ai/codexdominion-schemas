'use client'

import { useState } from 'react'
import { DashboardTile } from '@/components'

interface ScriptEditorProps {
  projectId: string
}

export default function ScriptEditor({ projectId }: ScriptEditorProps) {
  const [script, setScript] = useState(`[HOST INTRO]
Welcome back to the podcast! Today we're diving into an exciting topic...

[SEGMENT 1: Main Discussion]
Let's start by exploring the key concepts...

[MUSIC BREAK - 5 seconds]

[SEGMENT 2: Deep Dive]
Now let's get into the details...

[HOST OUTRO]
Thanks for listening! Don't forget to subscribe...`)

  const wordCount = script.split(/\s+/).length
  const estimatedMinutes = Math.ceil(wordCount / 150)

  return (
    <DashboardTile title="Audio Script" icon="📝" action={{ label: "Save Script", onClick: () => {} }}>
      <textarea
        value={script}
        onChange={(e) => setScript(e.target.value)}
        className="w-full h-80 px-4 py-3 bg-codex-navy/30 border border-codex-gold/30 rounded text-codex-parchment font-mono text-sm resize-none"
        placeholder="Write your audio script here..."
      />
      <div className="mt-3 flex justify-between text-xs text-codex-parchment/60">
        <span>{script.split('\n').length} lines</span>
        <span>{wordCount} words</span>
        <span>~{estimatedMinutes} min speaking time</span>
      </div>
    </DashboardTile>
  )
}
