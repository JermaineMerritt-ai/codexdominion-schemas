'use client'

export default function AudioRenderQueue() {
  const queue = [
    { id: '1', name: 'Meditation Music', progress: 43, eta: '8 min' },
    { id: '2', name: 'Voice Narration', progress: 0, eta: 'Queued' },
  ]

  return (
    <div className="codex-card">
      <h2 className="text-xl font-serif text-codex-gold mb-4">
        🎼 Render Queue
      </h2>

      <div className="space-y-3">
        {queue.map((item) => (
          <div key={item.id} className="codex-panel">
            <div className="flex justify-between text-sm mb-2">
              <span className="font-semibold">{item.name}</span>
              <span className="text-codex-parchment/60">{item.eta}</span>
            </div>
            {item.progress > 0 && (
              <div className="w-full bg-codex-navy/50 rounded-full h-2">
                <div
                  className="bg-purple-500 h-2 rounded-full"
                  style={{ width: `${item.progress}%` }}
                ></div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
