'use client'

import { DashboardTile } from '@/components'

export default function QuickActionsDock() {
  const actions = [
    { icon: '🎄', label: 'Generate Product', href: '/commerce' },
    { icon: '🎬', label: 'New Video', href: '/studio-video' },
    { icon: '🎵', label: 'New Audio', href: '/studio-audio' },
    { icon: '🌐', label: 'New Website', href: '/websites' },
    { icon: '📱', label: 'Social Post', href: '/social' },
    { icon: '⚡', label: 'Run Ritual', href: '/automations' },
    { icon: '📚', label: 'Add Knowledge', href: '/knowledge' },
    { icon: '🤖', label: 'Deploy Avatar', href: '/avatars' },
  ]

  return (
    <DashboardTile title="Quick Actions" icon="⚡">
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        {actions.map((action, idx) => (
          <a
            key={idx}
            href={action.href}
            className="codex-panel hover:bg-codex-gold/20 transition-all hover:scale-105 flex flex-col items-center justify-center py-4 text-center cursor-pointer"
          >
            <span className="text-3xl mb-2">{action.icon}</span>
            <span className="text-xs font-medium">{action.label}</span>
          </a>
        ))}
      </div>
    </DashboardTile>
  )
}
