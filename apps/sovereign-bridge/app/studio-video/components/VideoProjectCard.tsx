'use client'

import Link from 'next/link'

interface VideoProject {
  id: string
  name: string
  status: 'draft' | 'rendering' | 'completed' | 'error'
  progress: number
}

interface VideoProjectCardProps {
  project: VideoProject
}

export default function VideoProjectCard({ project }: VideoProjectCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
      case 'rendering': return 'bg-blue-500/20 text-blue-400 border-blue-500/30'
      case 'completed': return 'bg-green-500/20 text-green-400 border-green-500/30'
      case 'error': return 'bg-red-500/20 text-red-400 border-red-500/30'
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    }
  }

  return (
    <Link href={`/studio-video/projects/${project.id}`}>
      <div className="codex-panel hover:bg-codex-gold/10 transition-all cursor-pointer">
        <div className="flex items-start justify-between mb-3">
          <div>
            <h3 className="font-semibold">{project.name}</h3>
            <p className="text-xs text-codex-parchment/60">Project ID: {project.id}</p>
          </div>
          <span className={`codex-badge ${getStatusColor(project.status)}`}>
            {project.status.toUpperCase()}
          </span>
        </div>

        {project.status === 'rendering' && (
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span>Rendering...</span>
              <span>{project.progress}%</span>
            </div>
            <div className="w-full bg-codex-navy/50 rounded-full h-2">
              <div
                className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${project.progress}%` }}
              ></div>
            </div>
          </div>
        )}
      </div>
    </Link>
  )
}
