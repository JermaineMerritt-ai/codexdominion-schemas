'use client'

import { DashboardTile, StatusBadge } from '@/components'

interface ScheduledPost {
  id: string
  platform: string
  content: string
  scheduledFor: string
  status: 'pending' | 'active' | 'success'
  icon: string
}

export default function ContentCalendar() {
  const posts: ScheduledPost[] = [
    { id: '1', platform: 'Instagram', content: 'Christmas Product Showcase', scheduledFor: 'Dec 15, 2:00 PM', status: 'pending', icon: '📸' },
    { id: '2', platform: 'Pinterest', content: 'Holiday Gift Guide Pins', scheduledFor: 'Dec 15, 4:30 PM', status: 'pending', icon: '📌' },
    { id: '3', platform: 'TikTok', content: 'Behind the Scenes Video', scheduledFor: 'Dec 16, 10:00 AM', status: 'pending', icon: '🎵' },
    { id: '4', platform: 'Facebook', content: 'Customer Testimonial Post', scheduledFor: 'Dec 16, 3:00 PM', status: 'pending', icon: '👥' },
    { id: '5', platform: 'YouTube', content: 'Product Demo Short', scheduledFor: 'Dec 17, 12:00 PM', status: 'pending', icon: '🎥' },
  ] as const

  return (
    <DashboardTile title="Content Calendar" icon="📅" action={{ label: "+ Schedule Post", onClick: () => {} }}>
      <div className="space-y-2">
        {posts.map((post) => (
          <div key={post.id} className="codex-panel hover:bg-codex-gold/10 cursor-pointer">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-xl">{post.icon}</span>
                <div>
                  <div className="text-sm font-medium text-codex-parchment">{post.content}</div>
                  <div className="text-xs text-codex-parchment/60">{post.platform}</div>
                </div>
              </div>
              <StatusBadge status={post.status} />
            </div>
            <div className="text-xs text-codex-parchment/50">{post.scheduledFor}</div>
          </div>
        ))}
      </div>
    </DashboardTile>
  )
}
