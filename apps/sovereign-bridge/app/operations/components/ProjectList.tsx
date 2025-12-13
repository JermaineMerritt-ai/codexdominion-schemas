'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface Project {
  id: string
  type: 'video' | 'audio' | 'document'
  title: string
  status: 'pending' | 'active' | 'success'
  realm: string
  owner: string
  updatedAt: string
}

export default function ProjectList() {
  const projects: Project[] = [
    {
      id: 'video_001',
      type: 'video',
      title: 'Kids Christmas Story – Episode 1',
      status: 'active',
      realm: 'kids_realm',
      owner: 'jermaine',
      updatedAt: '5 min ago'
    },
    {
      id: 'video_002',
      type: 'video',
      title: 'Wedding Planning Guide',
      status: 'active',
      realm: 'wedding_realm',
      owner: 'jermaine',
      updatedAt: '1 hour ago'
    },
    {
      id: 'audio_001',
      type: 'audio',
      title: 'Advent Devotional Day 12',
      status: 'success',
      realm: 'kids_realm',
      owner: 'jermaine',
      updatedAt: '2 hours ago'
    },
    {
      id: 'doc_001',
      type: 'document',
      title: 'Homeschool Curriculum Plan',
      status: 'pending',
      realm: 'education_realm',
      owner: 'jermaine',
      updatedAt: '10 min ago'
    },
  ] as const

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'video': return '🎥'
      case 'audio': return '🎵'
      case 'document': return '📄'
      default: return '📦'
    }
  }

  return (
    <DashboardTile title="Active Projects" icon="📁" action={{ label: "+ New Project", onClick: () => {} }}>
      <div className="space-y-3">
        {projects.map((project) => (
          <div key={project.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-start gap-3">
              <span className="text-2xl">{getTypeIcon(project.type)}</span>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-semibold text-sm text-codex-parchment">{project.title}</h3>
                  <StatusBadge status={project.status} />
                </div>
                <p className="text-xs text-codex-parchment/60">
                  {project.realm} • {project.owner} • {project.updatedAt}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
