'use client'

export default function ContentCalendar() {
  const scheduled = [
    { platform: 'Instagram', content: 'Advent Day 12 Quote', time: 'Today 3:00 PM', status: 'scheduled' },
    { platform: 'Pinterest', content: 'Christmas Coloring Pack Pin', time: 'Today 5:00 PM', status: 'scheduled' },
    { platform: 'YouTube', content: 'Homeschool Tips Video', time: 'Tomorrow 10:00 AM', status: 'scheduled' },
  ]

  return (
    <div className="codex-card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-serif text-codex-gold">
          Content Calendar
        </h2>
        <button className="codex-button">
          ➕ Schedule Post
        </button>
      </div>

      <div className="space-y-3">
        {scheduled.map((post, idx) => (
          <div key={idx} className="codex-panel border-l-2 border-blue-500">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="font-semibold text-sm">{post.content}</h3>
                <p className="text-xs text-codex-parchment/60">{post.platform} • {post.time}</p>
              </div>
              <span className="codex-badge bg-blue-500/20 text-blue-400 border-blue-500/30">
                SCHEDULED
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
