'use client'

export default function ChannelOverview() {
  const channels = [
    { name: 'Instagram', followers: '12.8K', posts: 847, engagement: '4.2%', status: 'active' },
    { name: 'Pinterest', followers: '8.9K', posts: 1523, engagement: '3.8%', status: 'active' },
    { name: 'YouTube', followers: '5.2K', posts: 67, engagement: '6.1%', status: 'active' },
    { name: 'TikTok', followers: '3.4K', posts: 234, engagement: '5.3%', status: 'active' },
    { name: 'Facebook', followers: '7.6K', posts: 456, engagement: '2.9%', status: 'active' },
    { name: 'Threads', followers: '1.2K', posts: 189, engagement: '3.4%', status: 'active' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-2xl font-serif text-codex-gold mb-6">
        Social Channels
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {channels.map((channel, idx) => (
          <div key={idx} className="codex-panel hover:bg-codex-gold/10 transition-all">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold">{channel.name}</h3>
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
            </div>
            <div className="grid grid-cols-3 gap-2 text-center text-xs">
              <div>
                <div className="font-bold text-codex-gold">{channel.followers}</div>
                <div className="text-codex-parchment/60">Followers</div>
              </div>
              <div>
                <div className="font-bold text-green-400">{channel.posts}</div>
                <div className="text-codex-parchment/60">Posts</div>
              </div>
              <div>
                <div className="font-bold text-blue-400">{channel.engagement}</div>
                <div className="text-codex-parchment/60">Engage</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
