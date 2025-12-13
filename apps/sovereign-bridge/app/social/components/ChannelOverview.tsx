'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface Channel {
  id: string
  name: string
  platform: string
  followers: string
  engagement: string
  status: 'active' | 'inactive'
  icon: string
}

export default function ChannelOverview() {
  const channels: Channel[] = [
    { id: '1', name: 'Instagram', platform: 'instagram', followers: '12.5K', engagement: '4.2%', status: 'active', icon: '📸' },
    { id: '2', name: 'Facebook', platform: 'facebook', followers: '8.3K', engagement: '3.1%', status: 'active', icon: '👥' },
    { id: '3', name: 'Pinterest', platform: 'pinterest', followers: '5.7K', engagement: '5.8%', status: 'active', icon: '📌' },
    { id: '4', name: 'YouTube', platform: 'youtube', followers: '3.2K', engagement: '6.4%', status: 'active', icon: '🎥' },
    { id: '5', name: 'TikTok', platform: 'tiktok', followers: '15.8K', engagement: '8.9%', status: 'active', icon: '🎵' },
    { id: '6', name: 'Twitter', platform: 'twitter', followers: '4.1K', engagement: '2.3%', status: 'inactive', icon: '🐦' },
  ] as const

  return (
    <DashboardTile title="Social Channels" icon="📱" action={{ label: "+ Connect Channel", onClick: () => {} }}>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {channels.map((channel) => (
          <div key={channel.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl">{channel.icon}</span>
              <StatusBadge status={channel.status === 'active' ? 'success' : 'inactive'} />
            </div>
            <div className="text-sm font-medium text-codex-parchment mb-1">{channel.name}</div>
            <div className="flex justify-between text-xs text-codex-parchment/60">
              <span>{channel.followers}</span>
              <span>{channel.engagement} eng.</span>
            </div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
